#!/usr/bin/env python3
"""
数据操作审计追踪器 (Data Audit) v1.1.0

功能:
    --snapshot        生成目录快照（SHA256 + 元数据）
    --compare         对比两个快照，输出变更报告
    --log             记录一条操作日志
    --history         查看操作历史
    --validate        检查数据目录健康状态
    --export-csv      将快照或对比报告导出为 CSV

新增 v1.1.0:
    --filter          按扩展名过滤（如 .csv,.json）
    --ignore          忽略模式（支持 .gitignore 语法）
    --depth           递归深度限制
    --ignore-file     从文件加载忽略模式
    --export-csv      CSV 格式导出
    --progress        大目录显示进度
    --config          从配置文件加载参数

用法:
    python3 scripts/auditor.py --snapshot ./data/ --output snapshot.json
    python3 scripts/auditor.py --snapshot ./data/ --filter .csv,.json --depth 3
    python3 scripts/auditor.py --snapshot ./data/ --ignore-file .auditignore
    python3 scripts/auditor.py --compare old.json new.json --output report.json
    python3 scripts/auditor.py --compare old.json new.json --export-csv changes.csv
    python3 scripts/auditor.py --log "初始化数据库" --target ./data/db/
    python3 scripts/auditor.py --history
    python3 scripts/auditor.py --validate ./data/
    python3 scripts/auditor.py --snapshot ./data/ --config .auditconfig.json
"""

import argparse
import csv
import fnmatch
import hashlib
import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# === Constants ===
LOG_DIR = Path.home() / ".data-audit-logs"
LOG_FILE = LOG_DIR / "audit_history.json"
VERSION = "1.1.0"
EXTS_TEXT = {'.txt', '.csv', '.json', '.xml', '.yaml', '.yml', '.md', '.log',
             '.html', '.js', '.py', '.sh', '.conf', '.cfg', '.ini', '.env'}
EXTS_BINARY = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.pdf', '.doc', '.docx',
               '.xls', '.xlsx', '.zip', '.gz', '.tar', '.db', '.sqlite', '.bin'}
EXTS_HIDDEN = {'.pyc', '.o', '.so', '.dylib', '.DS_Store'}

# === Config ===
DEFAULT_CONFIG = {
    "filter_extensions": [],
    "ignore_patterns": [],
    "max_depth": -1,
    "show_progress": False,
    "skip_hidden": True,
    "skip_symlinks": True,
}


def load_config(config_path):
    """从 JSON 配置文件加载参数。"""
    try:
        with open(config_path) as f:
            cfg = json.load(f)
        config = DEFAULT_CONFIG.copy()
        config.update(cfg)
        print(f"   ⚙️  加载配置: {config_path}")
        return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"   ⚠️  配置加载失败: {e}，使用默认配置")
        return DEFAULT_CONFIG.copy()


def load_ignore_file(path):
    """从文件加载忽略模式（类似 .gitignore 语法）。"""
    patterns = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    except FileNotFoundError:
        print(f"   ⚠️  忽略文件未找到: {path}")
    return patterns


def should_ignore(relative_path, ignore_patterns):
    """检查路径是否匹配任意忽略模式（支持 glob 通配符）。"""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(relative_path, pattern):
            return True
        # 也匹配路径的一部分（如 __pycache__ 匹配任何位置）
        if "/" + pattern in relative_path or relative_path.startswith(pattern):
            return True
    return False


def hash_file(filepath):
    """计算文件 SHA256 哈希。"""
    h = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                h.update(chunk)
        return h.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None


def file_metadata(filepath, relative_path):
    """获取文件完整元数据。"""
    try:
        stat = os.stat(filepath)
    except (PermissionError, FileNotFoundError):
        return None
    ext = Path(filepath).suffix.lower()
    return {
        "path": relative_path,
        "name": os.path.basename(filepath),
        "size": stat.st_size,
        "ext": ext,
        "type": "binary" if ext in EXTS_BINARY else "text" if ext in EXTS_TEXT else "other",
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "created": datetime.fromtimestamp(stat.st_birthtime).isoformat() if hasattr(stat, 'st_birthtime') else "",
        "hash": hash_file(filepath),
    }


def take_snapshot(directory, filter_exts=None, ignore_patterns=None, max_depth=-1, show_progress=False, skip_hidden=True, skip_symlinks=True):
    """对目录下的数据文件生成快照，支持过滤和深度限制。"""
    basedir = os.path.abspath(directory)
    if not os.path.exists(basedir):
        return {"error": f"Directory not found: {basedir}"}

    filter_exts = set(f".{e.lstrip('.')}" for e in (filter_exts or []))
    ignore_patterns = ignore_patterns or []

    snap = {
        "snapshot_time": datetime.now().isoformat(),
        "directory": basedir,
        "total_files": 0,
        "total_size": 0,
        "files": [],
        "tool_version": VERSION,
    }

    visited = 0
    start_time = time.time()

    for root, dirs, names in os.walk(basedir):
        # 深度限制
        rel_root = os.path.relpath(root, basedir)
        if rel_root != ".":
            depth = rel_root.count(os.sep) + 1
            if 0 <= max_depth < depth:
                dirs.clear()
                continue

        # 跳过隐藏目录
        if skip_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]

        # 跳过符号链接
        if skip_symlinks:
            dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]

        for name in sorted(names):
            fpath = os.path.join(root, name)

            # 跳过隐藏文件
            if skip_hidden and name.startswith('.'):
                continue

            # 跳过符号链接
            if skip_symlinks and os.path.islink(fpath):
                continue

            if not os.path.isfile(fpath):
                continue

            rpath = os.path.relpath(fpath, basedir)

            # 忽略模式过滤
            if should_ignore(rpath, ignore_patterns):
                continue

            # 扩展名过滤
            ext = Path(fpath).suffix.lower()
            if filter_exts and ext not in filter_exts:
                continue

            meta = file_metadata(fpath, rpath)
            if meta is None:
                continue

            snap["files"].append(meta)
            snap["total_files"] += 1
            snap["total_size"] += meta.get("size", 0)
            visited += 1

            if show_progress and visited % 500 == 0:
                elapsed = time.time() - start_time
                print(f"   📊 已扫描 {visited} 个文件... ({elapsed:.1f}s)", end="\r", file=sys.stderr)

    if show_progress:
        elapsed = time.time() - start_time
        print(f"   {' ' * 50}", end="\r", file=sys.stderr)

    snap["size_human"] = _format_size(snap["total_size"])
    snap["elapsed_seconds"] = round(time.time() - start_time, 2)
    return snap


def _format_size(size_bytes):
    """格式化文件大小。"""
    size_bytes = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def compare_snapshots(old_path, new_path):
    """比较两个快照，找出文件变化。"""
    try:
        with open(old_path) as f:
            old = json.load(f)
        with open(new_path) as f:
            new = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {"error": str(e)}

    if "error" in old or "error" in new:
        return {"error": "Snapshot contains errors"}

    old_map = {f["path"]: f for f in old.get("files", [])}
    new_map = {f["path"]: f for f in new.get("files", [])}

    old_paths = set(old_map.keys())
    new_paths = set(new_map.keys())

    report = {
        "compare_time": datetime.now().isoformat(),
        "old_snapshot": old.get("snapshot_time", "unknown"),
        "new_snapshot": new.get("snapshot_time", "unknown"),
        "old_directory": old.get("directory", ""),
        "new_directory": new.get("directory", ""),
        "total_changes": 0,
        "by_type": {"added": 0, "deleted": 0, "modified": 0},
        "changes": [],
        "tool_version": VERSION,
    }

    # 新增文件
    for p in sorted(new_paths - old_paths):
        f = new_map[p]
        report["changes"].append({
            "type": "added", "file": p, "size": f["size"],
            "size_human": _format_size(f["size"]), "ext": f["ext"]
        })
        report["by_type"]["added"] += 1

    # 删除文件
    for p in sorted(old_paths - new_paths):
        f = old_map[p]
        report["changes"].append({
            "type": "deleted", "file": p, "size": f["size"],
            "size_human": _format_size(f["size"]), "ext": f["ext"]
        })
        report["by_type"]["deleted"] += 1

    # 修改文件（大小或哈希变化）
    for p in sorted(old_paths & new_paths):
        of = old_map[p]
        nf = new_map[p]
        if of["hash"] != nf["hash"]:
            diff_human = f"{_format_size(of['size'])} → {_format_size(nf['size'])}"
            report["changes"].append({
                "type": "modified", "file": p,
                "size_before": of["size"], "size_after": nf["size"],
                "diff_human": diff_human, "ext": of["ext"]
            })
            report["by_type"]["modified"] += 1

    report["total_changes"] = sum(report["by_type"].values())
    return report


def log_operation(action, target=""):
    """记录一条操作日志到本地文件。"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    history = []
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE) as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "target": target,
    }
    history.append(entry)

    # 只保留最近 1000 条
    if len(history) > 1000:
        history = history[-1000:]

    with open(LOG_FILE, "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    entry["total"] = len(history)
    return entry


def view_history(limit=50):
    """查看操作历史。"""
    if not LOG_FILE.exists():
        return {"total": 0, "entries": []}
    try:
        with open(LOG_FILE) as f:
            history = json.load(f)
    except json.JSONDecodeError:
        return {"total": 0, "entries": []}
    return {
        "total": len(history),
        "entries": history[-limit:],
    }


def validate_directory(directory):
    """检查数据目录健康状态。"""
    basedir = os.path.abspath(directory)
    if not os.path.exists(basedir):
        return {"error": f"Directory not found: {basedir}"}

    issues = []
    total_files = 0
    total_dirs = 0
    total_size = 0
    empty_dirs = 0

    for root, dirs, names in os.walk(basedir):
        total_dirs += 1
        if not names and not dirs:
            empty_dirs += 1
        for name in names:
            fpath = os.path.join(root, name)
            if not os.path.isfile(fpath):
                continue
            total_files += 1
            try:
                size = os.path.getsize(fpath)
                total_size += size
                if size == 0:
                    issues.append({"type": "empty_file", "path": os.path.relpath(fpath, basedir)})
            except (PermissionError, FileNotFoundError):
                issues.append({"type": "unreadable", "path": os.path.relpath(fpath, basedir)})

        # 检查不可读目录
        for d in dirs:
            dpath = os.path.join(root, d)
            if not os.access(dpath, os.R_OK):
                issues.append({"type": "inaccessible_dir", "path": os.path.relpath(dpath, basedir)})

    # 计算健康评分
    health_score = "healthy"
    issue_count = len(issues)
    if issue_count > 0:
        health_score = "warning" if issue_count < total_files * 0.1 else "poor"

    return {
        "health": health_score,
        "directory": basedir,
        "stats": {
            "total_files": total_files,
            "total_dirs": total_dirs,
            "total_size": total_size,
            "size_human": _format_size(total_size),
            "empty_dirs": empty_dirs,
        },
        "issues": issues[:100],  # 限制输出
        "total_issues": issue_count,
        "check_time": datetime.now().isoformat(),
    }


# === Output printers ===

def print_snapshot(result):
    """打印快照摘要。"""
    if "error" in result:
        print(f"❌ {result['error']}")
        return
    elapsed = result.get("elapsed_seconds", 0)
    print(f"\n📸 数据快照")
    print(f"   {'=' * 45}")
    print(f"   目录: {result['directory']}")
    print(f"   文件数: {result['total_files']:,}")
    print(f"   总大小: {result['size_human']}")
    print(f"   时间: {result['snapshot_time'][:19]}")
    if elapsed:
        print(f"   耗时: {elapsed:.2f}s")


def print_compare(report):
    """打印对比报告。"""
    if "error" in report:
        print(f"❌ {report['error']}")
        return
    print(f"\n📊 审计对比结果")
    print(f"   {'=' * 45}")
    by = report['by_type']
    print(f"   新增: {by['added']}   删除: {by['deleted']}   修改: {by['modified']}   总计: {report['total_changes']}")
    print(f"   时间窗口: {report['old_snapshot'][:10]} → {report['new_snapshot'][:10]}")
    print()
    if report['changes']:
        print(f"   变更明细:")
        for c in report['changes'][:20]:
            icon = {"added": "🟢", "deleted": "🔴", "modified": "🟡"}.get(c['type'], "•")
            detail = c.get('diff_human', c.get('size_human', c.get('size', '')))
            print(f"   {icon} {c['type']:<8} {c['file']} ({detail})")
        if len(report['changes']) > 20:
            print(f"   ... 及 {len(report['changes']) - 20} 项更多")


def print_validate(result):
    """打印健康检查报告。"""
    if "error" in result:
        print(f"❌ {result['error']}")
        return
    health_icon = {"healthy": "✅", "warning": "⚠️", "poor": "❌"}
    s = result['stats']
    print(f"\n🔍 数据健康检查 — {health_icon.get(result['health'], '•')} {result['health']}")
    print(f"   {'=' * 45}")
    print(f"   目录: {result['directory']}")
    print(f"   文件数: {s['total_files']:,}")
    print(f"   总大小: {s['size_human']}")
    print(f"   目录数: {s['total_dirs']}")
    print(f"   空目录: {s['empty_dirs']}")
    if result['issues']:
        print(f"\n   问题 ({result['total_issues']}):")
        for issue in result['issues'][:15]:
            print(f"   ⚠️  {issue['type']}: {issue['path']}")
        if len(result['issues']) > 15:
            print(f"   ... 及 {len(result['issues']) - 15} 项更多")


def print_history(hist):
    """打印操作历史。"""
    if hist['total'] == 0:
        print("   (暂无操作记录)")
        return
    print(f"\n📋 操作历史 (最近{len(hist['entries'])}条/共{hist['total']}条)")
    print(f"   {'=' * 45}")
    for entry in reversed(hist['entries']):
        print(f"   [{entry['timestamp'][:19]}] {entry['action']} → {entry['target']}")


def export_csv(data, output_path, data_type="changes"):
    """将数据导出为 CSV 格式。"""
    try:
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            if data_type == "changes" and "changes" in data:
                writer = csv.DictWriter(f, fieldnames=["type", "file", "size", "size_before", "size_after", "diff_human", "ext"])
                writer.writeheader()
                for row in data["changes"]:
                    writer.writerow(row)
                print(f"   📄 对比报告已导出 CSV: {output_path} ({len(data['changes'])} 条)")
            elif data_type == "snapshot" and "files" in data:
                writer = csv.DictWriter(f, fieldnames=["path", "name", "size", "ext", "type", "modified", "hash"])
                writer.writeheader()
                for row in data["files"]:
                    writer.writerow(row)
                print(f"   📄 快照已导出 CSV: {output_path} ({len(data['files'])} 文件)")
            elif data_type == "validate" and "issues" in data:
                writer = csv.DictWriter(f, fieldnames=["type", "path"])
                writer.writeheader()
                for row in data["issues"]:
                    writer.writerow(row)
                print(f"   📄 健康检查已导出 CSV: {output_path} ({len(data['issues'])} 项)")
            else:
                print(f"   ⚠️  未找到可导出的数据")
    except (IOError, PermissionError) as e:
        print(f"   ❌ CSV 导出失败: {e}")


def save_json(data, output_path):
    """将数据保存为 JSON 文件。"""
    try:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except (IOError, PermissionError) as e:
        print(f"   ❌ 保存失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description=f"数据操作审计追踪器 v{VERSION}",
        epilog="示例: python3 scripts/auditor.py --snapshot ./data/ --progress --filter .csv,.json"
    )
    parser.add_argument("--snapshot", help="对目录生成快照")
    parser.add_argument("--compare", nargs=2, metavar=("OLD", "NEW"), help="比较两个快照")
    parser.add_argument("--log", help="记录操作日志", metavar="ACTION")
    parser.add_argument("--target", help="操作目标（配合 --log）")
    parser.add_argument("--history", action="store_true", help="查看操作历史")
    parser.add_argument("--validate", help="检查数据目录健康状态", metavar="DIR")
    parser.add_argument("--output", help="JSON 输出路径")
    parser.add_argument("--export-csv", help="CSV 导出路径")
    parser.add_argument("--json", action="store_true", help="终端 JSON 输出")
    parser.add_argument("--filter", help="扩展名过滤，逗号分隔（如 .csv,.json）")
    parser.add_argument("--ignore", help="忽略模式，逗号分隔（如 __pycache__,*.tmp）")
    parser.add_argument("--ignore-file", help="从文件加载忽略模式")
    parser.add_argument("--depth", type=int, default=-1, help="递归深度限制（默认无限制）")
    parser.add_argument("--progress", action="store_true", help="大目录显示进度")
    parser.add_argument("--config", help="从 JSON 配置文件加载参数")
    parser.add_argument("--version", action="store_true", help="显示版本号")
    parser.add_argument("--init-config", help="生成默认配置文件模板", metavar="PATH")

    args = parser.parse_args()

    # 版本号
    if args.version:
        print(f"Data Audit v{VERSION}")
        return

    # 生成配置模板
    if args.init_config:
        with open(args.init_config, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置文件模板已生成: {args.init_config}")
        return

    # 加载配置文件
    config = DEFAULT_CONFIG.copy()
    if args.config:
        config = load_config(args.config)

    # 合并命令行参数和配置文件
    filter_exts = _parse_filter(args.filter) or config.get("filter_extensions", [])
    ignore_patterns = config.get("ignore_patterns", [])
    if args.ignore:
        ignore_patterns.extend(p.strip() for p in args.ignore.split(",") if p.strip())
    if args.ignore_file:
        ignore_patterns.extend(load_ignore_file(args.ignore_file))
    max_depth = args.depth if args.depth != -1 else config.get("max_depth", -1)
    show_progress = args.progress or config.get("show_progress", False)

    # === Snapshot ===
    if args.snapshot:
        result = take_snapshot(args.snapshot, filter_exts=filter_exts,
                               ignore_patterns=ignore_patterns,
                               max_depth=max_depth,
                               show_progress=show_progress,
                               skip_hidden=config.get("skip_hidden", True),
                               skip_symlinks=config.get("skip_symlinks", True))
        if args.json or args.output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_snapshot(result)
        if args.output:
            if save_json(result, args.output):
                print(f"   📄 快照已保存: {args.output}")
        if args.export_csv:
            export_csv(result, args.export_csv, data_type="snapshot")

    # === Compare ===
    elif args.compare:
        result = compare_snapshots(args.compare[0], args.compare[1])
        if args.json or args.output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_compare(result)
        if args.output:
            if save_json(result, args.output):
                print(f"   📄 报告已保存: {args.output}")
        if args.export_csv:
            export_csv(result, args.export_csv, data_type="changes")

    # === Log ===
    elif args.log:
        entry = log_operation(args.log, args.target or "")
        print(f"✅ 操作已记录: [{entry['timestamp'][:19]}] {entry['action']}")

    # === History ===
    elif args.history:
        hist = view_history()
        print_history(hist)

    # === Validate ===
    elif args.validate:
        result = validate_directory(args.validate)
        if args.json or args.output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_validate(result)
        if args.output:
            if save_json(result, args.output):
                print(f"   📄 报告已保存: {args.output}")
        if args.export_csv:
            export_csv(result, args.export_csv, data_type="validate")

    else:
        parser.print_help()


def _parse_filter(filter_str):
    """解析扩展名过滤字符串。"""
    if not filter_str:
        return []
    return [f".{e.strip().lstrip('.')}" for e in filter_str.split(",") if e.strip()]


if __name__ == "__main__":
    main()
