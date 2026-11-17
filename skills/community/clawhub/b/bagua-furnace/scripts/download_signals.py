#!/usr/bin/env python3
"""Wave B L2 跨设备信号同步（download_signals.py）——把云端历史信号拉回本地合并。

规划：docs/review/wave-b-cloud-levers-plan-2026-08-21.md §4.1。
设计（与 upload_signals.py 同风格）：
  - pull：读本地 .anon_id → GET {aggregate_url}/aggregate/restore?anon_id= → 合并进 signals-log.jsonl
  - 合并按 client_signal_id 去重（幂等，可重复跑）；本地已有优先（不覆盖）
  - 失败静默、零阻塞：网络/限流/无 anon_id → 本地不动，仅日志
  - 端点完全来自外部配置（cloud_config.json aggregate_url / 环境变量 CJG_AGGREGATE_URL），零硬编码

用法：
  python download_signals.py pull [--dir <技能目录>]   # 拉取并合并本技能信号
"""
import json
import os
import sys
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DIR = os.path.dirname(HERE)
RESTORE_PATH = "/aggregate/restore"


def _read_file(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return None


def resolve_aggregate_url(skill_dir):
    """聚合端点完全来自外部配置（环境变量 CJG_AGGREGATE_URL → cloud_config.json → secrets），零硬编码。"""
    env = os.environ.get("CJG_AGGREGATE_URL")
    if env:
        return env.strip().rstrip("/")
    cands = [
        os.path.join(skill_dir, "cloud_config.json"),
        os.path.expanduser("~/.workbuddy/secrets/cjg-evo/cloud_config.json"),
    ]
    for cc in cands:
        if os.path.exists(cc):
            try:
                with open(cc, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                u = (cfg.get("aggregate_url") or "").strip()
                if u:
                    return u.rstrip("/")
            except Exception:
                pass
    return None


def _read_log(dir_):
    path = os.path.join(dir_, "signals-log.jsonl")
    if not os.path.exists(path):
        return [], path
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [json.loads(l) for l in f if l.strip()], path
    except Exception:
        return [], path


def _merge_remote(dir_, remote_rows):
    """按 signal_id（优先；与 upload_signals.client_signal_id 的幂等键语义一致）去重合并；
    本地已有优先，只追加缺失。返回新增数。"""
    lines, path = _read_log(dir_)
    existing = set()
    for l in lines:
        cid = l.get("signal_id") or l.get("client_signal_id")
        if cid:
            existing.add(cid)
    added = 0
    with open(path, "a", encoding="utf-8") as f:
        for r in remote_rows:
            cid = r.get("signal_id") or r.get("client_signal_id")
            if not cid or cid in existing:
                continue
            local = {
                "ts": (r.get("created_at") or "").replace(" ", "T"),
                "signal_id": cid,
                "client_signal_id": cid,
                "skill_slug": r.get("skill_slug"),
                "skill_version": r.get("skill_version"),
                "method_layer": r.get("method_layer"),
                "event": r.get("event"),
                "weight": r.get("weight"),
            }
            # G1 客观指标透传（行业无关，无 PII）
            if r.get("metric_json"):
                try:
                    local["metric"] = json.loads(r["metric_json"])
                except Exception:
                    pass
            f.write(json.dumps(local, ensure_ascii=False) + "\n")
            existing.add(cid)
            added += 1
            if added % 50 == 0:
                f.flush()
    return added


def cmd_pull(dir_):
    skill_dir = os.path.abspath(dir_)
    anon_id = _read_file(os.path.join(skill_dir, ".anon_id"))
    if not anon_id:
        print("[download] 无 .anon_id（从未采集过信号），跳过同步")
        return 0
    base = resolve_aggregate_url(skill_dir)
    if not base:
        print("[download] 未配置聚合端点（cloud_config.json 缺 aggregate_url），跳过云端同步（本地照常）")
        return 0
    url = f"{base}{RESTORE_PATH}?anon_id={anon_id}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[download] 云端返回 {e.code}，跳过（失败静默，本地不动）")
        return 0
    except Exception as e:
        print(f"[download] 网络异常 {type(e).__name__}，跳过（本地不动）")
        return 0
    rows = (data or {}).get("signals") or []
    if not rows:
        print("[download] 云端无历史信号（或均为本机已有），无需合并")
        return 0
    added = _merge_remote(skill_dir, rows)
    print(f"[download] 已从云端合并 {added} 条历史信号（去重后新增），共 {len(rows)} 条云端记录")
    return added


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        print("用法：python download_signals.py pull [--dir <技能目录>]")
        sys.exit(0 if args and args[0] in ("-h", "--help") else 2)
    if args[0] != "pull":
        print(__doc__)
        print("用法：python download_signals.py pull [--dir <技能目录>]")
        sys.exit(2)
    dir_ = DEFAULT_DIR
    rest = args[1:]
    if "--dir" in rest:
        try:
            dir_ = rest[rest.index("--dir") + 1]
        except Exception:
            pass
    sys.exit(0 if cmd_pull(dir_) is not None else 2)


if __name__ == "__main__":
    main()
