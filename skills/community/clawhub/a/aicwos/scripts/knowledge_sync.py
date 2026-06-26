#!/usr/bin/env python3
"""
知识库云端同步

从云端拉取公共知识库，采用公共层+私有层架构：
- 公共层：云端权威，同步时覆盖；用户想定制就复制到私有层
- 私有层：纯本地，云端不管不碰
- 同名覆盖：私有层优先级 > 公共层

同步流程（无需凭证）：
1. 下载 COS 上的 manifest.txt（每行一个文件路径，无时间戳）
2. 对每个文件发 HEAD 请求，获取 COS Last-Modified
3. 与本地文件 st_mtime 比对，增量下载更新的文件
4. 本地有但 manifest 中没有的公共层文件标记 .offline

云端维护者只需在 COS 上维护 manifest.txt（追加新文件路径即可），
时间戳由 COS 自动管理，零手工维护。

用法:
  python scripts/knowledge_sync.py --data-dir ./控制台
  python scripts/knowledge_sync.py --data-dir ./控制台 --force
  python scripts/knowledge_sync.py --data-dir ./控制台 --dry-run
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

SKILL_ROOT = str(Path(__file__).resolve().parent.parent)
if SKILL_ROOT not in sys.path:
    sys.path.insert(0, SKILL_ROOT)


def load_workspace(data_dir: Path) -> dict:
    ws_path = data_dir / "workspace.json"
    if ws_path.exists():
        return json.loads(ws_path.read_text(encoding="utf-8"))
    return {}


def download_text(url: str, timeout: int = 15) -> str:
    """下载文本内容（公共读，无需凭证）。"""
    req = urllib.request.Request(url, headers={"User-Agent": "aicwos-sync/2.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def download_bytes(url: str, timeout: int = 30) -> bytes:
    """下载二进制内容（公共读，无需凭证）。"""
    req = urllib.request.Request(url, headers={"User-Agent": "aicwos-sync/2.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def head_last_modified(url: str, timeout: int = 10) -> str:
    """
    HEAD 请求获取 COS 对象的 Last-Modified。

    返回原始 header 值（如 "Wed, 16 Apr 2026 09:00:00 GMT"）。
    失败返回空字符串。
    """
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "aicwos-sync/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.headers.get("Last-Modified", "")
    except Exception:
        return ""


def parse_http_date(date_str: str) -> datetime:
    """解析 HTTP Date header（RFC 2822）为 UTC datetime。"""
    if not date_str:
        return datetime(2000, 1, 1, tzinfo=timezone.utc)
    try:
        return parsedate_to_datetime(date_str)
    except (ValueError, TypeError):
        return datetime(2000, 1, 1, tzinfo=timezone.utc)


def local_mtime_utc(path: Path) -> datetime:
    """获取本地文件的 UTC 修改时间。"""
    if not path.exists():
        return datetime(2000, 1, 1, tzinfo=timezone.utc)
    mtime = path.stat().st_mtime
    return datetime.fromtimestamp(mtime, tz=timezone.utc)


def fetch_manifest(base_url: str, timeout: int = 15) -> list:
    """
    下载并解析 COS 上的 manifest.txt。

    manifest.txt 格式：每行一个文件相对路径，无时间戳。
    空行和 # 开头的行被忽略。

    返回: ["产品目录/御草千金方/产品属性.txt", ...]
    """
    manifest_url = f"{base_url.rstrip('/')}/manifest.txt"
    try:
        content = download_text(manifest_url, timeout=timeout)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []  # 无 manifest.txt → 远程无知识库
        raise
    except Exception:
        raise

    paths = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        paths.append(line)
    return paths


def sync_knowledge(data_dir: Path, force: bool = False, dry_run: bool = False) -> dict:
    """
    执行知识库同步。

    流程（无需凭证）：
    1. HEAD manifest.txt → 如果 Last-Modified 未变且非 force → 整批跳过
    2. 下载 manifest.txt → 获取远程文件路径列表
    3. 新文件直接下载；已有文件 HEAD 检查 Last-Modified vs st_mtime
    4. 本地公共层有但 manifest 中没有的文件 → .offline
    """
    ws = load_workspace(data_dir)
    sync_cfg = ws.get("knowledge_sync", {})
    base_url = sync_cfg.get("base_url", "").rstrip("/")

    if not base_url:
        return {
            "status": "no_config",
            "message": "workspace.json中未配置knowledge_sync.base_url。"
                       "请向用户询问云端知识库地址，然后写入workspace.json的knowledge_sync.base_url字段。",
        }

    public_dir = data_dir / "知识库集" / "公共"
    manifest_url = f"{base_url.rstrip('/')}/manifest.txt"

    # 快速跳过：HEAD manifest.txt，如果 Last-Modified 未变 → 无需扫描
    if not force:
        last_mtime = sync_cfg.get("_last_manifest_mtime", "")
        if last_mtime:
            lm_str = head_last_modified(manifest_url)
            if lm_str:
                remote_dt = parse_http_date(lm_str)
                local_dt = parse_http_date(last_mtime)
                if remote_dt <= local_dt or (remote_dt - local_dt).total_seconds() <= 1:
                    return {
                        "status": "up_to_date",
                        "message": "manifest.txt 未更新，跳过扫描",
                        "files_checked": 0,
                        "added": [],
                        "updated": [],
                        "skipped": [],
                        "removed": [],
                        "errors": [],
                    }
                # HEAD 成功且远程更新 → 继续下载
            # HEAD 返回空（远程不存在/网络问题）→ 不跳过，继续尝试下载

    # 下载 manifest.txt
    try:
        remote_paths = fetch_manifest(base_url)
    except urllib.error.HTTPError as e:
        return {"status": "error", "message": f"下载 manifest.txt 失败: HTTP {e.code} {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": f"下载 manifest.txt 失败: {e}"}

    if not remote_paths:
        return {"status": "up_to_date", "message": "远程 manifest.txt 为空或不存在", "files_checked": 0}

    # 更新 workspace.json 中的 _last_manifest_mtime（用于下次快速跳过）
    if not dry_run:
        lm_str = head_last_modified(manifest_url)
        if lm_str:
            ws["knowledge_sync"]["_last_manifest_mtime"] = lm_str
            ws_path = data_dir / "workspace.json"
            ws_path.write_text(json.dumps(ws, ensure_ascii=False, indent=2), encoding="utf-8")

    added = []
    updated = []
    skipped = []
    removed = []
    errors = []

    # 遍历远程文件列表
    for rel_path in remote_paths:
        local_file = public_dir / rel_path
        file_url = f"{base_url}/{urllib.parse.quote(rel_path, safe='/')}"

        if not local_file.exists():
            # 新文件：直接下载（无需 HEAD）
            if dry_run:
                added.append(rel_path)
                continue
            try:
                content = download_bytes(file_url)
                local_file.parent.mkdir(parents=True, exist_ok=True)
                local_file.write_bytes(content)
                added.append(rel_path)
            except Exception as e:
                errors.append(f"下载失败 {rel_path}: {e}")
            continue

        if force:
            action = "update"
        else:
            # 已有文件：HEAD 检查 Last-Modified
            lm_str = head_last_modified(file_url)
            if not lm_str:
                # HEAD 失败，安全起见跳过
                skipped.append(rel_path)
                continue

            remote_dt = parse_http_date(lm_str)
            local_dt = local_mtime_utc(local_file)

            # 远程更新时间 > 本地修改时间 → 需要下载（留 1s 容差）
            if remote_dt > local_dt and (remote_dt - local_dt).total_seconds() > 1:
                action = "update"
            else:
                skipped.append(rel_path)
                continue

        if dry_run:
            updated.append(rel_path)
            continue

        # 下载更新
        try:
            content = download_bytes(file_url)
            local_file.write_bytes(content)
            updated.append(rel_path)
        except Exception as e:
            errors.append(f"下载失败 {rel_path}: {e}")

    # 远程已删除的公共层文件 → .offline
    remote_set = set(remote_paths)
    if public_dir.exists():
        for f in sorted(public_dir.rglob("*")):
            if not f.is_file() or f.name.endswith(".offline"):
                continue
            rel_path = str(f.relative_to(public_dir)).replace("\\", "/")
            if rel_path not in remote_set:
                if dry_run:
                    removed.append(rel_path)
                else:
                    offline_file = Path(str(f) + ".offline")
                    f.rename(offline_file)
                    removed.append(rel_path)

    return {
        "status": "synced" if not dry_run else "dry_run",
        "files_checked": len(remote_paths),
        "added": added,
        "updated": updated,
        "skipped": skipped,
        "removed": removed,
        "errors": errors,
    }


def generate_manifest(data_dir: Path) -> dict:
    """
    从本地公共层目录生成 manifest.txt（供云端维护者上传到 COS）。

    生成格式：每行一个文件相对路径，无时间戳。
    输出到 stdout，云端维护者将输出内容保存为 manifest.txt 上传到 COS。

    用法: python scripts/knowledge_sync.py --data-dir ./控制台 --generate
    """
    public_dir = data_dir / "知识库集" / "公共"
    if not public_dir.exists():
        return {"status": "error", "message": "公共层目录不存在"}

    paths = []
    for f in sorted(public_dir.rglob("*")):
        if not f.is_file() or f.name.endswith(".offline"):
            continue
        rel = str(f.relative_to(public_dir)).replace("\\", "/")
        paths.append(rel)

    # 输出到 stdout（方便重定向到文件）
    content = "\n".join(paths) + "\n" if paths else ""
    print(content, end="")

    return {"status": "generated", "file_count": len(paths), "paths": paths}


def main():
    parser = argparse.ArgumentParser(description="知识库云端同步（manifest.txt + HEAD，无需凭证）")
    parser.add_argument("--data-dir", required=True, help="数据目录路径（含workspace.json）")
    parser.add_argument("--force", action="store_true", help="强制重新下载所有文件")
    parser.add_argument("--dry-run", action="store_true", help="仅检查，不下载")
    parser.add_argument("--generate", action="store_true", help="从本地公共层生成 manifest.txt（供云端维护者上传到 COS）")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    if args.generate:
        result = generate_manifest(data_dir)
        # generate_manifest 已输出到 stdout，这里只输出统计信息到 stderr
        if result["status"] == "error":
            print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        else:
            info = {k: v for k, v in result.items() if k != "paths"}
            print(json.dumps(info, ensure_ascii=False), file=sys.stderr)
        return
    result = sync_knowledge(data_dir, force=args.force, dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
