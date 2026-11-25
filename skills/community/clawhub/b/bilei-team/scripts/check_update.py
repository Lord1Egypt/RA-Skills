#!/usr/bin/env python3
"""避雷.skill 版本自检。

比对本地 SKILL.md 与 GitHub 远端版本，24 小时缓存一次，失败静默。

用法:
    python3 scripts/check_update.py            # 人类可读
    python3 scripts/check_update.py --json     # 机器可读
    python3 scripts/check_update.py --force    # 忽略缓存
    python3 scripts/check_update.py --simulate-remote 9.9.9   # 测试用

退出码恒为 0：版本检查永远不阻断主流程。
"""
import json
import os
import re
import sys
import time
import urllib.request

SOURCES = [
    ("github-raw", "https://raw.githubusercontent.com/zhashushu/bilei-team/main/SKILL.md"),
    ("jsdelivr", "https://cdn.jsdelivr.net/gh/zhashushu/bilei-team@main/SKILL.md"),
]
CACHE_DIR = os.path.expanduser("~/.cache/bilei-team")
CACHE_FILE = os.path.join(CACHE_DIR, "update-check.json")
TTL_SECONDS = 24 * 3600
TIMEOUT_SECONDS = 4


def read_local_version():
    here = os.path.dirname(os.path.abspath(__file__))
    skill_md = os.path.join(here, "..", "SKILL.md")
    try:
        text = open(skill_md, encoding="utf-8").read()
    except OSError:
        return None
    match = re.search(r'^version:\s*"([^"]+)"', text, re.M)
    return match.group(1) if match else None


def fetch_remote_version():
    """按优先级尝试多个源，返回 (version, source_name)。"""
    last_error = None
    for name, url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bilei-update-check"})
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                text = resp.read().decode("utf-8", "replace")
            match = re.search(r'^version:\s*"([^"]+)"', text, re.M)
            if match:
                return match.group(1), name
        except Exception as exc:  # 换下一个源
            last_error = exc
    raise last_error if last_error else RuntimeError("no source available")


def parse_ver(v):
    try:
        return tuple(int(x) for x in str(v).split(".")[:3])
    except (ValueError, AttributeError):
        return None


def classify(local, remote):
    """返回 (has_update, level)：level 为 major / minor / patch。"""
    l, r = parse_ver(local), parse_ver(remote)
    if not l or not r or r <= l:
        return False, None
    if r[0] > l[0]:
        return True, "major"
    if r[1] > l[1]:
        return True, "minor"
    return True, "patch"


def load_cache():
    try:
        return json.load(open(CACHE_FILE, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def save_cache(data):
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        json.dump(data, open(CACHE_FILE, "w", encoding="utf-8"), ensure_ascii=False)
    except OSError:
        pass


def main():
    args = sys.argv[1:]
    as_json = "--json" in args
    force = "--force" in args

    simulate = None
    for i, a in enumerate(args):
        if a == "--simulate-remote" and i + 1 < len(args):
            simulate = args[i + 1]
        elif a.startswith("--simulate-remote="):
            simulate = a.split("=", 1)[1]

    local = read_local_version()
    now = int(time.time())
    result = {
        "status": "ok",
        "local": local,
        "remote": None,
        "has_update": False,
        "level": None,
        "checked_at": time.strftime("%Y-%m-%d %H:%M", time.localtime(now)),
        "source": "github-raw",
        "cached": False,
    }

    if not local:
        result.update(status="skipped", reason="本地 SKILL.md 缺少 version 字段")
    else:
        cached = None if force else load_cache()
        if cached and now - int(cached.get("ts", 0)) < TTL_SECONDS and cached.get("remote"):
            result.update(remote=cached["remote"], cached=True, source=cached.get("source", "github-raw"))
        elif simulate:
            # 测试模式不写缓存，避免污染真实检查结果
            result.update(remote=simulate, source="simulated")
        else:
            try:
                remote, src = fetch_remote_version()
                result.update(remote=remote, source=src)
                save_cache({"ts": now, "remote": remote, "source": src})
            except Exception as exc:  # 网络失败一律静默
                result.update(status="skipped", reason="远端不可达: %s" % type(exc).__name__)

        if result["remote"]:
            has, level = classify(local, result["remote"])
            result.update(has_update=has, level=level)

    if as_json:
        print(json.dumps(result, ensure_ascii=False))
        return 0

    if result["status"] != "ok":
        print("版本自检：跳过（%s）" % result.get("reason", ""))
    elif result["has_update"]:
        print("发现新版本：本地 v%s → 远端 v%s（%s 级更新）"
              % (result["local"], result["remote"], result["level"]))
        print("更新方式：SkillHub 重新安装 @indiv-huto/bilei-team；GitHub 仓库 git pull")
    else:
        print("版本自检：已是最新 v%s" % result["local"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
