#!/usr/bin/env python3
"""
查询任务历史记录 v3
改进点：
1. 扫描所有候选路径，合并多路径数据（兜底保障）
2. 去重（按 task_id）
3. 显示数据来源路径
"""
import sys
import json
import os
from pathlib import Path

try:
    from path_detector import get_task_history_path, get_all_history_files
except ImportError:
    # Fallback
    ANCHOR_FILE = Path.home() / '.skill-logger' / '.anchor'

    def _get_candidate_bases():
        candidates = [
            str(Path.home()),
            os.getenv('PERSISTENT_DIR'),
            os.getenv('DATA_DIR'),
            os.getenv('WORKSPACE_DIR'),
            os.getenv('WORKSPACE_PATH'),
            os.getenv('WORK_DIR'),
            os.getcwd(),
            '/var/tmp',
            '/tmp',
        ]
        seen = set()
        result = []
        for p in candidates:
            if p and p not in seen:
                seen.add(p)
                result.append(p)
        return result

    def _test_writable(path):
        try:
            os.makedirs(path, exist_ok=True)
            test_file = os.path.join(path, '.test_write')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return True
        except (PermissionError, OSError):
            return False

    def _save_anchor(history_file):
        try:
            ANCHOR_FILE.parent.mkdir(parents=True, exist_ok=True)
            ANCHOR_FILE.write_text(history_file)
        except Exception:
            pass

    def get_task_history_path():
        candidate_bases = _get_candidate_bases()
        if ANCHOR_FILE.exists():
            try:
                anchored_path = ANCHOR_FILE.read_text().strip()
                if _test_writable(str(Path(anchored_path).parent)):
                    return anchored_path
            except Exception:
                pass
        for base_path in candidate_bases:
            history_file = os.path.join(base_path, '.skill-logger', 'task_history.json')
            if os.path.exists(history_file) and _test_writable(os.path.dirname(history_file)):
                _save_anchor(history_file)
                return history_file
        for base_path in candidate_bases:
            history_dir = os.path.join(base_path, '.skill-logger')
            history_file = os.path.join(history_dir, 'task_history.json')
            if _test_writable(history_dir):
                _save_anchor(history_file)
                return history_file
        raise RuntimeError("无法找到可写入的存储路径")

    def get_all_history_files():
        found = []
        seen = set()
        for base_path in _get_candidate_bases():
            history_file = os.path.join(base_path, '.skill-logger', 'task_history.json')
            real_path = os.path.realpath(history_file)
            if os.path.exists(history_file) and real_path not in seen:
                seen.add(real_path)
                found.append(history_file)
        return found


def query_tasks(task_type=None, status=None, limit=10):
    try:
        # 扫描所有路径，合并数据
        all_files = get_all_history_files()
        primary_file = get_task_history_path()

        all_records = []
        seen_ids = set()
        sources = []

        for history_file in all_files:
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    records = json.load(f)
                new_count = 0
                for r in records:
                    tid = r.get('task_id')
                    if tid and tid not in seen_ids:
                        all_records.append(r)
                        seen_ids.add(tid)
                        new_count += 1
                sources.append({"path": history_file, "records": new_count})
            except Exception as e:
                sources.append({"path": history_file, "error": str(e)})

        if not all_records:
            print(json.dumps({
                "success": True,
                "tasks": [],
                "total": 0,
                "message": "暂无任务记录",
                "storage_path": str(primary_file),
                "sources": sources,
            }, ensure_ascii=False, indent=2))
            return

        # 过滤
        filtered = all_records
        if task_type:
            filtered = [t for t in filtered if t.get('task_type') == task_type]
        if status:
            filtered = [t for t in filtered if t.get('status') == status]

        # 按时间倒序
        filtered.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        if limit:
            filtered = filtered[:limit]

        print(json.dumps({
            "success": True,
            "tasks": filtered,
            "total": len(filtered),
            "total_all": len(all_records),
            "storage_path": str(primary_file),
            "sources": sources,
        }, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='查询任务历史记录 v3')
    parser.add_argument('--task-type', help='任务类型过滤')
    parser.add_argument('--status', help='状态过滤')
    parser.add_argument('--limit', type=int, default=10, help='返回数量限制')

    args = parser.parse_args()
    query_tasks(
        task_type=args.task_type,
        status=args.status,
        limit=args.limit,
    )
