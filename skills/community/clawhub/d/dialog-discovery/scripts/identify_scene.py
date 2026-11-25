#!/usr/bin/env python3
"""
场景识别预处理脚本

用途：扫描对话数据，识别场景分布，支持混合场景处理
"""
import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Tuple

# 添加脚本目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from common import WORKSPACE_DIR

# 挖掘工作目录
DISCOVERY_DIR = os.path.join(WORKSPACE_DIR, "discovery")
os.makedirs(DISCOVERY_DIR, exist_ok=True)


# 场景识别关键词
SCENE_KEYWORDS = {
    "loan": {
        "name": "金条额度激活",
        "keywords": ["金条", "额度", "白条", "免息券", "备用金", "借款", "京东金融", "激活额度"],
        "weight": 1.0,
    },
    "exhibition": {
        "name": "会展邀约",
        "keywords": ["会展", "参展", "邀请函", "博览会", "展位", "展会", "参展商", "主办方"],
        "weight": 1.0,
    },
    "collection": {
        "name": "催收",
        "keywords": ["还款", "逾期", "欠款", "催收", "账单", "征信", "起诉", "律师函", "外包"],
        "weight": 1.0,
    },
}


def load_dialogs(input_path: str) -> List[Dict[str, Any]]:
    """加载对话数据"""
    dialogs = []
    
    if input_path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(input_path)
        ws = wb.active
        
        # 找到对话内容列
        content_col = None
        for col in range(1, ws.max_column + 1):
            header = ws.cell(1, col).value
            if header and any(kw in str(header) for kw in ["对话", "内容", "dialog", "content", "文本"]):
                content_col = col
                break
        
        if not content_col:
            # 尝试找第一列有内容的
            for col in range(1, ws.max_column + 1):
                sample = ws.cell(2, col).value
                if sample and len(str(sample)) > 50:
                    content_col = col
                    break
        
        if not content_col:
            print(f"❌ 未找到对话内容列")
            sys.exit(1)
        
        # 检查是否有场景列
        scene_col = None
        for col in range(1, ws.max_column + 1):
            header = ws.cell(1, col).value
            if header and any(kw in str(header) for kw in ["场景", "scene", "类型", "type"]):
                scene_col = col
                break
        
        for row in range(2, ws.max_row + 1):
            content = ws.cell(row, content_col).value
            if content and len(str(content)) > 10:
                dialog = {
                    "id": f"dialog_{row}",
                    "content": str(content),
                    "row": row,
                }
                if scene_col:
                    dialog["scene_tag"] = ws.cell(row, scene_col).value
                dialogs.append(dialog)
    
    elif input_path.endswith(".json"):
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if isinstance(data, list):
            dialogs = [{"id": d.get("id", f"dialog_{i}"), "content": d.get("content", ""), "scene_tag": d.get("scene")} 
                      for i, d in enumerate(data) if d.get("content")]
        elif isinstance(data, dict) and "dialogs" in data:
            dialogs = [{"id": d.get("id", f"dialog_{i}"), "content": d.get("content", ""), "scene_tag": d.get("scene")} 
                      for i, d in enumerate(data["dialogs"]) if d.get("content")]
    
    elif input_path.endswith(".csv"):
        import csv
        with open(input_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                content = row.get("对话内容") or row.get("dialog_content") or row.get("content") or row.get("文本") or ""
                if content and len(content) > 10:
                    dialog = {
                        "id": f"dialog_{i}",
                        "content": content,
                        "scene_tag": row.get("场景") or row.get("scene") or row.get("类型"),
                    }
                    dialogs.append(dialog)
    
    return dialogs


def identify_scene_for_dialog(dialog: Dict[str, Any]) -> Tuple[str, float, Dict[str, float]]:
    """识别单条对话的场景"""
    content = dialog.get("content", "")
    
    # 如果有场景标签，直接使用
    scene_tag = dialog.get("scene_tag")
    if scene_tag:
        scene_tag_lower = str(scene_tag).lower()
        if "金条" in scene_tag_lower or "loan" in scene_tag_lower:
            return "loan", 1.0, {}
        elif "会展" in scene_tag_lower or "exhibition" in scene_tag_lower:
            return "exhibition", 1.0, {}
        elif "催收" in scene_tag_lower or "collection" in scene_tag_lower:
            return "collection", 1.0, {}
    
    # 关键词匹配
    scene_scores = {}
    
    for scene_id, scene_config in SCENE_KEYWORDS.items():
        keywords = scene_config["keywords"]
        weight = scene_config["weight"]
        
        # 计算匹配关键词数量
        matched_keywords = [kw for kw in keywords if kw in content]
        score = len(matched_keywords) * weight
        
        if score > 0:
            scene_scores[scene_id] = score
    
    # 选择得分最高的场景
    if scene_scores:
        best_scene = max(scene_scores, key=scene_scores.get)
        confidence = scene_scores[best_scene] / sum(scene_scores.values())
        return best_scene, confidence, scene_scores
    
    # 无法识别
    return "unknown", 0.0, {}


def analyze_scene_distribution(dialogs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """分析场景分布"""
    scene_counts = {}
    scene_dialogs = {}
    confidence_stats = {}
    
    print(f"📊 开始场景识别，共 {len(dialogs)} 条对话")
    
    for dialog in dialogs:
        scene, confidence, scores = identify_scene_for_dialog(dialog)
        
        scene_counts[scene] = scene_counts.get(scene, 0) + 1
        
        if scene not in scene_dialogs:
            scene_dialogs[scene] = []
        scene_dialogs[scene].append({
            "id": dialog["id"],
            "content": dialog["content"],
            "confidence": confidence,
            "matched_scene": scene,
        })
        
        # 记录置信度
        if scene != "unknown":
            if scene not in confidence_stats:
                confidence_stats[scene] = []
            confidence_stats[scene].append(confidence)
    
    # 统计
    total = len(dialogs)
    distribution = {}
    
    for scene, count in scene_counts.items():
        pct = count / total * 100
        avg_confidence = sum(confidence_stats.get(scene, [1.0])) / len(confidence_stats.get(scene, [1.0]))
        distribution[scene] = {
            "count": count,
            "percentage": pct,
            "avg_confidence": avg_confidence,
            "scene_name": SCENE_KEYWORDS.get(scene, {}).get("name", "未知场景"),
        }
    
    # 打印结果
    print(f"\n📊 场景分布:")
    for scene, stats in sorted(distribution.items(), key=lambda x: x[1]["count"], reverse=True):
        print(f"  {stats['scene_name']} ({scene}): {stats['count']} 条 ({stats['percentage']:.1f}%)")
        if stats["avg_confidence"] < 1.0:
            print(f"    平均置信度: {stats['avg_confidence']:.2f}")
    
    # 建议
    dominant_scene = max(distribution.keys(), key=lambda s: distribution[s]["count"])
    
    if distribution[dominant_scene]["percentage"] > 80:
        suggestion = f"建议使用单一场景模式，场景: {dominant_scene}"
    elif len(distribution) > 2 and distribution.get("unknown", {}).get("percentage", 0) > 30:
        suggestion = "建议人工标注场景或使用混合模式"
    else:
        suggestion = f"建议使用混合场景模式，分别处理各场景数据"
    
    print(f"\n💡 建议: {suggestion}")
    
    return {
        "total": total,
        "distribution": distribution,
        "scene_dialogs": scene_dialogs,
        "dominant_scene": dominant_scene,
        "suggestion": suggestion,
    }


def split_by_scene(dialogs: List[Dict[str, Any]], analysis: Dict[str, Any]) -> Dict[str, str]:
    """按场景拆分数据"""
    output_files = {}
    
    scene_dialogs = analysis.get("scene_dialogs", {})
    
    for scene, scene_data in scene_dialogs.items():
        if scene == "unknown":
            continue
        
        output_path = os.path.join(
            DISCOVERY_DIR,
            f"scene_{scene}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        )
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({
                "scene": scene,
                "scene_name": SCENE_KEYWORDS.get(scene, {}).get("name", scene),
                "total": len(scene_data),
                "dialogs": scene_data,
                "created_at": datetime.now().isoformat(),
            }, f, ensure_ascii=False, indent=2)
        
        output_files[scene] = output_path
        print(f"✅ 场景 {scene} 数据已保存: {output_path} ({len(scene_data)} 条)")
    
    return output_files


def save_analysis_report(analysis: Dict[str, Any], output_path: str) -> None:
    """保存分析报告"""
    report_content = f"""# 场景识别分析报告

> 分析时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}
> 总对话数：{analysis["total"]} 条

---

## 场景分布

| 场景 | 名称 | 数量 | 占比 | 平均置信度 |
|------|------|------|------|----------|
"""
    
    for scene, stats in sorted(analysis["distribution"].items(), key=lambda x: x[1]["count"], reverse=True):
        report_content += f"| {scene} | {stats['scene_name']} | {stats['count']} | {stats['percentage']:.1f}% | {stats['avg_confidence']:.2f} |\n"
    
    report_content += f"""

---

## 建议

{analysis['suggestion']}

**主导场景**: {analysis['dominant_scene']} ({analysis['distribution'][analysis['dominant_scene']]['percentage']:.1f}%)

---

## 下一步

1. 如果单一场景占比 >80%，直接使用 `--scene {analysis['dominant_scene']}` 进行挖掘
2. 如果混合场景，按场景拆分数据后分别挖掘
3. 如果 unknown 占比 >30%，建议人工标注场景

---

*生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"✅ 分析报告已保存: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="场景识别预处理")
    parser.add_argument("--input", required=True, help="输入对话数据文件（xlsx/json/csv）")
    parser.add_argument("--output", required=False, help="输出分析报告文件（md）")
    parser.add_argument("--split", action="store_true", help="按场景拆分数据")
    
    args = parser.parse_args()
    
    # 加载对话数据
    dialogs = load_dialogs(args.input)
    print(f"✅ 已加载对话数据: {len(dialogs)} 条")
    
    # 分析场景分布
    analysis = analyze_scene_distribution(dialogs)
    
    # 输出路径
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.join(
            DISCOVERY_DIR,
            f"scene_analysis_{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        )
    
    # 保存分析报告
    save_analysis_report(analysis, output_path)
    
    # 拆分数据（可选）
    if args.split:
        output_files = split_by_scene(dialogs, analysis)
        print(f"\n✅ 已拆分 {len(output_files)} 个场景的数据文件")


if __name__ == "__main__":
    main()