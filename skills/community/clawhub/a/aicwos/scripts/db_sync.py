#!/usr/bin/env python3
"""
文件↔数据库同步

将文本文件同步到SQLite数据库，支持双向同步。

用法:
  # 从文件同步到数据库
  python scripts/db_sync.py --direction to-db --data-dir ./控制台
  python scripts/db_sync.py --direction to-db --data-dir ./控制台 --category 产品目录

  # 从数据库导出到文件
  python scripts/db_sync.py --direction to-files --data-dir ./控制台
  python scripts/db_sync.py --direction to-files --data-dir ./控制台 --lecturer 讲师A
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SKILL_ROOT = str(Path(__file__).resolve().parent.parent)
if SKILL_ROOT not in sys.path:
    sys.path.insert(0, SKILL_ROOT)

from scripts.core.db_manager import DatabaseManager, resolve_db_path
from scripts.core.lecturer_service import LecturerService
from scripts.core.knowledge_service import KnowledgeService
from scripts.core.copywriting_service import CopywritingService


def _iter_knowledge_files(knowledge_dir: Path, category: str = None):
    """
    遍历知识库集文件，公共层+私有层架构，私有层优先

    目录结构：
      知识库集/
        公共/  {分类}/...  ← 云端同步
        私有/  {分类}/...  ← 本地管理

    同名文件私有层覆盖公共层（不合并，私有为准）
    """
    public_dir = knowledge_dir / "公共"
    private_dir = knowledge_dir / "私有"

    # 收集私有层文件（相对路径 → 绝对路径）
    private_files = {}
    if private_dir.exists():
        for f in private_dir.rglob("*"):
            if f.is_file() and not f.name.endswith(".offline"):
                rel = f.relative_to(private_dir)
                private_files[str(rel).replace("\\", "/")] = f

    # 收集公共层文件
    public_files = {}
    if public_dir.exists():
        for f in public_dir.rglob("*"):
            if f.is_file() and not f.name.endswith(".offline"):
                rel = f.relative_to(public_dir)
                public_files[str(rel).replace("\\", "/")] = f

    # 合并：私有覆盖公共，同时记录每个文件的层来源
    all_files = {}  # rel_path → (fpath, layer)
    for path, fpath in public_files.items():
        all_files[path] = (fpath, "公共")
    for path, fpath in private_files.items():
        all_files[path] = (fpath, "私有")  # 私有优先

    # 按分类过滤和返回
    for rel_path, (fpath, layer) in sorted(all_files.items()):
        parts = Path(rel_path).parts
        cat_name = parts[0] if parts else ""
        if category and cat_name != category:
            continue
        # 公共行为目录不走知识检索管道，由 CopywritingService.load_behavior_rules() 独立加载
        if cat_name == "公共行为":
            continue
        yield cat_name, rel_path, fpath, layer


def sync_knowledge_to_db(data_dir: Path, db: DatabaseManager, category: str = None) -> dict:
    """将知识库集文件同步到数据库（公共层+私有层，私有优先）"""
    svc = KnowledgeService(db)
    knowledge_dir = data_dir / "知识库集"
    if not knowledge_dir.exists():
        return {"status": "no_knowledge_dir", "synced": 0}

    synced = 0
    errors = []

    for cat_name, rel_path, fpath, layer in _iter_knowledge_files(knowledge_dir, category):
        parts = Path(rel_path).parts
        # 判断是扁平分类还是产品子目录
        # 如 "产品目录/产品A/产品背书.txt" → category=产品目录, product=产品A
        # 如 "企业文化/公司使命.txt" → category=企业文化, product=None
        product = parts[1] if len(parts) > 2 else None
        filename = parts[-1]

        try:
            content = fpath.read_text(encoding="utf-8").strip()
            svc.add_doc(category=cat_name, filename=filename,
                        content=content, product=product, layer=layer)
            synced += 1
        except Exception as e:
            errors.append(f"{rel_path}: {e}")

    return {"status": "ok", "synced": synced, "errors": errors}


def sync_lecturers_to_db(data_dir: Path, db: DatabaseManager, lecturer_id: str = None) -> dict:
    """将讲师文件同步到数据库"""
    svc = LecturerService(db, data_dir=str(data_dir))
    lecturers_dir = data_dir / "讲师列表"
    if not lecturers_dir.exists():
        return {"status": "no_lecturers_dir", "synced": 0}

    synced = 0
    errors = []

    for lec_dir in sorted(lecturers_dir.iterdir()):
        if not lec_dir.is_dir():
            continue
        lid = lec_dir.name
        if lecturer_id and lid != lecturer_id:
            continue

        profile_file = lec_dir / "profile.json"
        if not profile_file.exists():
            errors.append(f"{lid}: profile.json不存在")
            continue

        try:
            profile = json.loads(profile_file.read_text(encoding="utf-8"))
            svc.add_lecturer(lid, profile)

            samples_dir = lec_dir / "样本"
            if samples_dir.exists():
                for sf in sorted(samples_dir.glob("样本_*.txt")):
                    content = sf.read_text(encoding="utf-8").strip()
                    is_ref = any(
                        r.get("file") == sf.name
                        for r in profile.get("reference_scripts", [])
                    )
                    svc.add_sample(lid, sf.name, content, is_ref)

            synced += 1
        except Exception as e:
            errors.append(f"{lid}: {e}")

    return {"status": "ok", "synced": synced, "errors": errors}


def sync_series_to_db(data_dir: Path, db: DatabaseManager, lecturer_id: str = None) -> dict:
    """将系列文案从文件同步到数据库

    文件结构:
      讲师列表/{讲师}/系列文案/{系列名}/
        E{集号}_{标题}.txt  — 纯正文（用户直接查看/编辑）

    DB存元数据（摘要、hook_next），正文留在文件中。
    """
    lecturers_dir = data_dir / "讲师列表"
    if not lecturers_dir.exists():
        return {"status": "no_lecturers_dir", "synced": 0}

    synced = 0
    episodes_synced = 0
    errors = []

    for lec_dir in sorted(lecturers_dir.iterdir()):
        if not lec_dir.is_dir():
            continue
        lid = lec_dir.name
        if lecturer_id and lid != lecturer_id:
            continue

        series_dir = lec_dir / "系列文案"
        if not series_dir.exists():
            continue

        for s_dir in sorted(series_dir.iterdir()):
            if not s_dir.is_dir():
                continue
            series_id = s_dir.name

            try:
                now = datetime.now().isoformat(timespec="seconds")
                csvc = CopywritingService(db, data_dir=str(data_dir))

                # 统计集文案文件
                ep_files = sorted(s_dir.glob("E*.txt"))
                if not ep_files:
                    continue

                total = len(ep_files)

                # 写系列计划（如果DB中不存在）
                existing = db.query_one(
                    "SELECT series_id FROM series_plans WHERE series_id=?", (series_id,)
                )
                if not existing:
                    db.execute(
                        "INSERT OR REPLACE INTO series_plans "
                        "(series_id, lecturer_id, title, plan_json, total_episodes, "
                        "completed, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (series_id, lid, series_id, "{}", total, 0, now, now),
                    )

                # 读取集文案并写入DB元数据
                for ep_file in ep_files:
                    match = re.match(r"E(\d+)_(.+)\.txt$", ep_file.name)
                    if not match:
                        errors.append(f"{lid}/{series_id}/{ep_file.name}: 文件名格式不符")
                        continue

                    ep_num = int(match.group(1))
                    ep_title = match.group(2)
                    content = ep_file.read_text(encoding="utf-8").strip()

                    # 自动生成摘要（取前100字）
                    summary = content[:100].replace("\n", " ") if content else ""
                    word_count = sum(1 for c in content
                                     if "\u4e00" <= c <= "\u9fff" or c.isalpha())

                    db.execute(
                        "INSERT OR REPLACE INTO episodes "
                        "(series_id, episode_num, title, summary, "
                        "hook_next, word_count, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (series_id, ep_num, ep_title, summary, "", word_count, now),
                    )
                    episodes_synced += 1

                # 更新completed
                max_ep = db.query_one(
                    "SELECT MAX(episode_num) as m FROM episodes WHERE series_id=?",
                    (series_id,),
                )
                completed = max_ep["m"] if max_ep and max_ep["m"] else 0
                db.execute(
                    "UPDATE series_plans SET completed=?, total_episodes=? WHERE series_id=?",
                    (completed, total, series_id),
                )
                db.commit()
                synced += 1

            except Exception as e:
                errors.append(f"{lid}/{series_id}: {e}")

    return {"status": "ok", "synced": synced, "episodes": episodes_synced, "errors": errors}


def sync_db_to_files(data_dir: Path, db: DatabaseManager, lecturer_id: str = None) -> dict:
    """从数据库导出到文件（讲师画像+样本；文案正文已由save_episode直接写文件）"""
    svc = LecturerService(db, data_dir=str(data_dir))
    exported = 0
    errors = []

    lecturers = svc.list_lecturers()
    for lec_info in lecturers:
        lid = lec_info["lecturer_id"]
        if lecturer_id and lid != lecturer_id:
            continue

        lec_dir = data_dir / "讲师列表" / lid
        lec_dir.mkdir(parents=True, exist_ok=True)

        profile = svc.get_profile(lid)
        if profile:
            (lec_dir / "profile.json").write_text(
                json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
            )

        samples = svc.get_samples(lid)
        samples_dir = lec_dir / "样本"
        samples_dir.mkdir(exist_ok=True)
        for s in samples:
            (samples_dir / s["sample_name"]).write_text(s["content"], encoding="utf-8")

        exported += 1

    return {"status": "ok", "exported": exported, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description="文件↔数据库同步")
    parser.add_argument("--direction", required=True, choices=["to-db", "to-files"],
                        help="同步方向")
    parser.add_argument("--data-dir", required=True, help="控制台目录路径")
    parser.add_argument("--category", default=None, help="仅同步指定知识分类")
    parser.add_argument("--lecturer", default=None, help="仅同步指定讲师")
    args = parser.parse_args()

    try:
        resolved_db = resolve_db_path(None, args.data_dir)
    except ValueError as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        return

    db = DatabaseManager(resolved_db)
    data_dir = Path(args.data_dir)

    if args.direction == "to-db":
        k_result = sync_knowledge_to_db(data_dir, db, args.category)
        l_result = sync_lecturers_to_db(data_dir, db, args.lecturer)
        s_result = sync_series_to_db(data_dir, db, args.lecturer)
        result = {"knowledge": k_result, "lecturers": l_result, "series": s_result}
    else:
        result = sync_db_to_files(data_dir, db, args.lecturer)

    db.close()
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
