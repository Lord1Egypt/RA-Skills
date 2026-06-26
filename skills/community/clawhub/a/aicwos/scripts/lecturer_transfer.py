#!/usr/bin/env python3
"""
讲师导入导出工具

处理讲师数据的跨用户迁移，解决重名冲突、知识引用缺失等边界问题。

用法:
  # 导出讲师（打包到指定目录）
  python scripts/lecturer_transfer.py --action export --lecturer 讲师A --data-dir ./控制台 --output ./导出

  # 导入讲师（从目录导入，默认合并模式 + 自动同步DB）
  python scripts/lecturer_transfer.py --action import --source ./导出/讲师A --data-dir ./控制台

  # 导入讲师（覆盖模式，同名讲师直接替换）
  python scripts/lecturer_transfer.py --action import --source ./导出/讲师A --data-dir ./控制台 --overwrite

  # 导入仅到文件系统，跳过数据库同步
  python scripts/lecturer_transfer.py --action import --source ./导出/讲师A --data-dir ./控制台 --no-sync
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

SKILL_ROOT = str(Path(__file__).resolve().parent.parent)
if SKILL_ROOT not in sys.path:
    sys.path.insert(0, SKILL_ROOT)

from scripts.core.db_manager import DatabaseManager, resolve_db_path
from scripts.core.lecturer_service import LecturerService


def export_lecturer(lecturer_id: str, data_dir: Path, output_dir: Path) -> dict:
    """
    导出讲师数据到指定目录

    导出内容:
      {output_dir}/{lecturer_id}/
        profile.json         — 画像
        样本/                 — 样本文案
        系列文案/             — 系列文案（如有）
        单章文案/             — 单章文案（如有）
    """
    src_dir = data_dir / "讲师列表" / lecturer_id
    if not src_dir.exists():
        return {"status": "error", "message": f"讲师 {lecturer_id} 不存在"}

    dest_dir = output_dir / lecturer_id
    if dest_dir.exists():
        shutil.rmtree(dest_dir)

    # 复制整个讲师目录
    shutil.copytree(src_dir, dest_dir)

    # 统计导出内容
    items = {}
    profile = dest_dir / "profile.json"
    if profile.exists():
        p = json.loads(profile.read_text(encoding="utf-8"))
        items["profile.json"] = f"画像 (版本{p.get('profile_version', '?')}, 样本{p.get('sample_stats', {}).get('total_samples', 0)}篇)"

    samples_dir = dest_dir / "样本"
    if samples_dir.exists():
        count = len(list(samples_dir.glob("*.txt")))
        items["样本"] = f"{count}篇"

    series_dir = dest_dir / "系列文案"
    if series_dir.exists():
        series_list = [d.name for d in series_dir.iterdir() if d.is_dir()]
        items["系列文案"] = f"{len(series_list)}个系列"

    single_dir = dest_dir / "单章文案"
    if single_dir.exists():
        count = len(list(single_dir.glob("*.txt")))
        if count > 0:
            items["单章文案"] = f"{count}篇"

    return {
        "status": "ok",
        "lecturer": lecturer_id,
        "output": str(dest_dir),
        "items": items,
    }


def import_lecturer(source: Path, data_dir: Path, overwrite: bool = False) -> dict:
    """
    导入讲师数据

    处理边界:
    1. 同名讲师 → 默认合并（样本增量添加，画像更新），--overwrite 则替换
    2. profile.json 完整性校验
    3. 知识引用缺失检测（系列计划中引用的知识是否在目标知识库中存在）
    """
    # 校验源目录
    if not source.exists():
        return {"status": "error", "message": f"源目录不存在: {source}"}

    profile_file = source / "profile.json"
    profile = {}
    warnings = []

    if not profile_file.exists():
        warnings.append("源目录缺少 profile.json，建议导入后执行 lecturer_analyzer.py 分析样本生成画像")
    else:
        # 校验 profile.json 完整性
        try:
            profile = json.loads(profile_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            warnings.append(f"profile.json 格式错误: {e}，导入后需重新分析样本生成画像")
            profile = {}

        required_fields = ["lecturer_id", "lecturer_name", "qualitative", "persona_mapping"]
        missing = [f for f in required_fields if f not in profile]
        if missing:
            warnings.append(
                f"profile.json 缺少字段: {missing}，建议导入后执行 "
                f"lecturer_analyzer.py 重新分析样本生成完整画像"
            )

    lecturer_id = profile.get("lecturer_id") or source.name
    dest_dir = data_dir / "讲师列表" / lecturer_id

    merged_items = {}

    if dest_dir.exists():
        if overwrite:
            # 覆盖模式：删除目标目录，完整复制
            shutil.rmtree(dest_dir)
            shutil.copytree(source, dest_dir)
            merged_items["mode"] = "覆盖"
        else:
            # 合并模式：增量合并
            merged_items["mode"] = "合并"

            # 1. 更新 profile.json（用源覆盖目标）
            if profile_file.exists():
                shutil.copy2(profile_file, dest_dir / "profile.json")
                merged_items["profile.json"] = "已更新"

            # 2. 增量复制样本（跳过同名文件）
            src_samples = source / "样本"
            dst_samples = dest_dir / "样本"
            if src_samples.exists():
                dst_samples.mkdir(exist_ok=True)
                added = 0
                skipped = 0
                for f in src_samples.glob("*.txt"):
                    dst = dst_samples / f.name
                    if dst.exists():
                        skipped += 1
                    else:
                        shutil.copy2(f, dst)
                        added += 1
                merged_items["样本"] = f"新增{added}篇, 跳过{skipped}篇同名"

            # 3. 增量复制系列文案
            src_series = source / "系列文案"
            dst_series = dest_dir / "系列文案"
            if src_series.exists():
                dst_series.mkdir(exist_ok=True)
                added_series = 0
                for s_dir in src_series.iterdir():
                    if not s_dir.is_dir():
                        continue
                    dst_s = dst_series / s_dir.name
                    if dst_s.exists():
                        # 同名系列：增量复制集文件
                        for ep_file in s_dir.glob("E*.txt"):
                            dst_ep = dst_s / ep_file.name
                            if not dst_ep.exists():
                                shutil.copy2(ep_file, dst_ep)
                        added_series += 1
                    else:
                        shutil.copytree(s_dir, dst_s)
                        added_series += 1
                if added_series > 0:
                    merged_items["系列文案"] = f"合并{added_series}个系列"

            # 4. 增量复制单章文案
            src_single = source / "单章文案"
            dst_single = dest_dir / "单章文案"
            if src_single.exists():
                dst_single.mkdir(exist_ok=True)
                added_single = 0
                for f in src_single.glob("*.txt"):
                    dst = dst_single / f.name
                    if not dst.exists():
                        shutil.copy2(f, dst)
                        added_single += 1
                if added_single > 0:
                    merged_items["单章文案"] = f"新增{added_single}篇"

            warnings.append(f"讲师 {lecturer_id} 已存在，已合并数据。如需完全替换，使用 --overwrite")
    else:
        # 全新导入：直接复制
        shutil.copytree(source, dest_dir)
        merged_items["mode"] = "新建"

        samples_dir = dest_dir / "样本"
        sample_count = len(list(samples_dir.glob("*.txt"))) if samples_dir.exists() else 0
        merged_items["样本"] = f"{sample_count}篇"

    # 检测知识引用缺失
    knowledge_refs = _check_knowledge_refs(profile, data_dir)
    if knowledge_refs["missing"]:
        warnings.append(
            f"系列计划引用了 {len(knowledge_refs['missing'])} 条知识，目标知识库中不存在: "
            f"{knowledge_refs['missing'][:5]}"
            + ("..." if len(knowledge_refs["missing"]) > 5 else "")
        )

    result = {
        "status": "ok",
        "lecturer": lecturer_id,
        "destination": str(dest_dir),
        "merged": merged_items,
    }
    if warnings:
        result["warnings"] = warnings
    if knowledge_refs["existing"]:
        result["knowledge_refs_found"] = len(knowledge_refs["existing"])

    return result


def _sync_to_db(lecturer_id: str, data_dir: Path, overwrite: bool = False) -> dict:
    """
    导入后同步到数据库（使用 Write-Through 的 LecturerService）

    策略与文件系统层一致：
    - 同名不存在 → 新增
    - 同名存在 + 非overwrite → 合并（INSERT OR REPLACE，profile以导入版为准）
    - 同名存在 + overwrite → 替换（同上，INSERT OR REPLACE语义）
    """
    try:
        resolved_db = resolve_db_path(None, str(data_dir))
        db = DatabaseManager(resolved_db)
        svc = LecturerService(db, data_dir=str(data_dir))

        sync_results = {"lecturer": None, "samples": 0, "series": None}

        # 1. 同步讲师画像（Write-Through: DB + profile.json）
        profile_file = data_dir / "讲师列表" / lecturer_id / "profile.json"
        if profile_file.exists():
            profile = json.loads(profile_file.read_text(encoding="utf-8"))
            svc.add_lecturer(lecturer_id, profile)
            sync_results["lecturer"] = "synced"
        else:
            sync_results["lecturer"] = "no_profile"

        # 2. 同步样本（Write-Through: DB + 样本文件）
        samples_dir = data_dir / "讲师列表" / lecturer_id / "样本"
        if samples_dir.exists():
            for sf in samples_dir.glob("*.txt"):
                content = sf.read_text(encoding="utf-8").strip()
                if content:
                    try:
                        svc.add_sample(lecturer_id, sf.name, content)
                        sync_results["samples"] += 1
                    except Exception:
                        pass  # 跳过重复样本

        # 3. 同步系列文案（通过 db_sync）
        from scripts.db_sync import sync_series_to_db
        series_result = sync_series_to_db(data_dir, db, lecturer_id=lecturer_id)
        sync_results["series"] = series_result

        db.close()
        return {"status": "ok", "sync": sync_results}

    except Exception as e:
        return {"status": "error", "message": str(e)}


def _check_knowledge_refs(profile: dict, data_dir: Path) -> dict:
    """检查 profile 中系列计划引用的知识是否在目标知识库中存在"""
    existing = []
    missing = []

    # 从 reference_scripts 提取知识引用（如果有 knowledge_refs 字段）
    # 也检查系列文案目录下的计划相关内容
    knowledge_dir = data_dir / "知识库集" / "公共"
    private_dir = data_dir / "知识库集" / "私有"

    # 收集已有知识文件路径
    known_files = set()
    for kd in [knowledge_dir, private_dir]:
        if kd.exists():
            for f in kd.rglob("*.txt"):
                rel = f.relative_to(kd)
                known_files.add(str(rel).replace("\\", "/"))

    # 从 profile 的 merge_history 等字段中提取引用（如有）
    # 目前 profile 中没有直接的 knowledge_refs，但系列计划中可能有
    # 这里主要检查系列文案目录
    lecturer_id = profile.get("lecturer_id", "")
    series_dir = data_dir / "讲师列表" / lecturer_id / "系列文案"
    if series_dir.exists():
        for plan_file in series_dir.rglob("*.json"):
            try:
                plan = json.loads(plan_file.read_text(encoding="utf-8"))
                for ep in plan.get("episodes", []):
                    for ref in ep.get("knowledge_refs", []):
                        if ref in known_files:
                            existing.append(ref)
                        else:
                            missing.append(ref)
            except (json.JSONDecodeError, KeyError):
                pass

    return {"existing": list(set(existing)), "missing": list(set(missing))}


def main():
    parser = argparse.ArgumentParser(description="讲师导入导出工具")
    parser.add_argument("--action", required=True, choices=["import", "export"],
                        help="操作: import=导入讲师, export=导出讲师")
    parser.add_argument("--source", default=None,
                        help="导入时: 源讲师目录路径")
    parser.add_argument("--lecturer", default=None,
                        help="导出时: 讲师名称")
    parser.add_argument("--output", default=None,
                        help="导出时: 输出目录路径")
    parser.add_argument("--data-dir", default=None,
                        help="控制台数据目录路径")
    parser.add_argument("--overwrite", action="store_true",
                        help="导入时: 同名讲师直接覆盖（默认合并）")
    parser.add_argument("--no-sync", action="store_true",
                        help="跳过数据库同步（仅导入到文件系统）")
    args = parser.parse_args()

    if not args.data_dir:
        print(json.dumps({"status": "error", "message": "必须指定 --data-dir"}, ensure_ascii=False))
        return

    data_dir = Path(args.data_dir)

    if args.action == "export":
        if not args.lecturer:
            print(json.dumps({"status": "error", "message": "导出时必须指定 --lecturer"}, ensure_ascii=False))
            return
        output_dir = Path(args.output) if args.output else data_dir / "导出"
        output_dir.mkdir(parents=True, exist_ok=True)
        result = export_lecturer(args.lecturer, data_dir, output_dir)

    elif args.action == "import":
        if not args.source:
            print(json.dumps({"status": "error", "message": "导入时必须指定 --source"}, ensure_ascii=False))
            return
        source = Path(args.source)
        result = import_lecturer(source, data_dir, overwrite=args.overwrite)

        # 默认同步到数据库（Write-Through: DB + 文件系统）
        if not args.no_sync and result.get("status") == "ok":
            sync_result = _sync_to_db(result["lecturer"], data_dir, overwrite=args.overwrite)
            result["db_sync"] = sync_result

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
