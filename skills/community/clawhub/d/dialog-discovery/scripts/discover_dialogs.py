#!/usr/bin/env python3
"""
对话数据挖掘一键执行脚本（重构版）

流程：
1. normalize
2. template match / feature extract
3. score
4. bucket profile
5. extract candidate rules
6. write report + manifest
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from common import WORKSPACE_DIR, create_run, update_manifest

DISCOVERY_DIR = os.path.join(WORKSPACE_DIR, "discovery")
os.makedirs(DISCOVERY_DIR, exist_ok=True)


def run_step(cmd, step_name):
    print("\n" + "=" * 60)
    print(step_name)
    print("=" * 60)
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        raise RuntimeError(f"步骤失败: {step_name}")


def path_with_ts(prefix, ext):
    return os.path.join(DISCOVERY_DIR, f"{prefix}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.{ext}")


def merge_report(scene, normalized_path, match_path, score_path, cluster_path, candidate_path, report_path):
    with open(match_path, "r", encoding="utf-8") as f:
        match_data = json.load(f)
    with open(score_path, "r", encoding="utf-8") as f:
        score_data = json.load(f)
    with open(cluster_path, "r", encoding="utf-8") as f:
        cluster_data = json.load(f)

    content = f"""# 对话挖掘报告\n\n> 场景：{scene}\n> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n## 一、产物\n- 标准化数据：`{normalized_path}`\n- 模板/特征结果：`{match_path}`\n- 评分结果：`{score_path}`\n- 聚类结果：`{cluster_path}`\n- 候选规则：`{candidate_path}`\n\n## 二、模板筛选结果\n- 总数：{match_data.get('stats', {}).get('total', 0)}\n- badcase：{match_data.get('stats', {}).get('badcase', 0)}\n- goodcase候选：{match_data.get('stats', {}).get('goodcase候选', 0)}\n- 灰度：{match_data.get('stats', {}).get('灰度', 0)}\n\n## 三、评分结果\n- 总数：{score_data.get('total', 0)}\n\n## 四、聚类结果\n- goodcase：{cluster_data.get('stats', {}).get('goodcase', 0)}\n- badcase：{cluster_data.get('stats', {}).get('badcase', 0)}\n- grayzone：{cluster_data.get('stats', {}).get('grayzone', 0)}\n\n## 五、建议\n1. 先人工 review 候选规则\n2. 再接 verify 流程做晋升\n3. 对高频 badcase 单独补约束\n"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="对话数据挖掘一键执行（重构版）")
    parser.add_argument("--input", required=True, help="输入对话文件")
    parser.add_argument("--scene", required=True, help="场景")
    parser.add_argument("--score-mode", default="hybrid", choices=["rules", "llm", "hybrid"])
    parser.add_argument("--model-name", default=None)
    args = parser.parse_args()

    manifest = create_run(target_scene=args.scene, source_type="raw_dialog_discovery")
    run_id = manifest["run_id"]
    update_manifest(run_id, status="DISCOVERY_RUNNING", note="开始执行对话挖掘")

    normalized_path = path_with_ts(f"normalized_{args.scene}", "json")
    match_path = path_with_ts(f"template_match_{args.scene}", "json")
    score_path = path_with_ts(f"batch_score_{args.scene}", "json")
    cluster_path = path_with_ts(f"cluster_{args.scene}", "json")
    candidate_path = path_with_ts(f"candidate_rules_{args.scene}", "md")
    report_path = path_with_ts(f"discovery_report_{args.scene}", "md")

    try:
        run_step([
            sys.executable, os.path.join(SCRIPT_DIR, "normalize_dialogs.py"),
            "--input", args.input,
            "--scene", args.scene,
            "--output", normalized_path,
        ], "第一步：标准化与角色分离")

        run_step([
            sys.executable, os.path.join(SCRIPT_DIR, "template_match_dialogs.py"),
            "--input", normalized_path,
            "--scene", args.scene,
            "--output", match_path,
        ], "第二步：特征提取与模板筛选")

        grayzone_path = match_path.replace(".json", "-grayzone.json")
        run_step([
            sys.executable, os.path.join(SCRIPT_DIR, "batch_score_dialogs.py"),
            "--input", grayzone_path,
            "--scene", args.scene,
            "--output", score_path,
            "--mode", args.score_mode,
            *( ["--model-name", args.model_name] if args.model_name else [] )
        ], "第三步：批量评分")

        run_step([
            sys.executable, os.path.join(SCRIPT_DIR, "cluster_dialogs.py"),
            "--scores", score_path,
            "--scene", args.scene,
            "--output", cluster_path,
        ], "第四步：分桶与聚类画像")

        cluster_dialogs_path = cluster_path.replace(".json", "-clusters.json")
        run_step([
            sys.executable, os.path.join(SCRIPT_DIR, "extract_rules_from_cluster.py"),
            "--clusters", cluster_dialogs_path,
            "--scene", args.scene,
            "--output", candidate_path,
        ], "第五步：候选规则提取")

        merge_report(args.scene, normalized_path, match_path, score_path, cluster_path, candidate_path, report_path)

        update_manifest(
            run_id,
            status="DISCOVERY_DONE",
            artifacts={
                "normalized": normalized_path,
                "template_match": match_path,
                "scores": score_path,
                "clusters": cluster_path,
                "candidate_rules": candidate_path,
                "report": report_path,
            },
            note="对话挖掘完成",
        )
        print("\n✅ 挖掘完成")
        print(f"报告: {report_path}")
        print(f"候选规则: {candidate_path}")
    except Exception as e:
        update_manifest(run_id, status="DISCOVERY_FAILED", note=str(e))
        raise


if __name__ == "__main__":
    main()
