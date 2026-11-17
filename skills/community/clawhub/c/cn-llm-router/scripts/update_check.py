"""技能更新提醒（本地版本比对 + 可选远程清单，离线安全）。

- 本地：比较「技能包内置版本」与「本机已见版本」，发现新版本主动提示升级。
- 远程（可选）：若 config.json 配置了 update_url（版本清单 JSON），拉取最新版本对比；
  离线 / 不可达时静默跳过，绝不报错、绝不阻塞主流程。
- 已见版本缓存于用户主目录，避免重复打扰。
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import urllib.request

import meta

SEEN_PATH = os.path.join(os.path.expanduser("~"), ".cn_llm_router", "seen_version.json")


def _semver(v):
    """把 '1.2.3' 转成 (1,2,3) 用于比较；非法返回 (0,0,0)。"""
    try:
        return tuple(int(x) for x in str(v).split(".") if x.isdigit())
    except Exception:
        return (0, 0, 0)


def _load_seen():
    try:
        with open(SEEN_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_seen(data):
    try:
        os.makedirs(os.path.dirname(SEEN_PATH), exist_ok=True)
        with open(SEEN_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass


def check_remote(update_url, timeout=10):
    """拉取远程版本清单。返回 dict 或 None（离线/失败）。"""
    if not update_url:
        return None
    try:
        req = urllib.request.Request(update_url, headers={"User-Agent": "cn-llm-router"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except Exception:
        return None


def run(current_version=None, update_url="", homepage=""):
    """返回 (has_update, latest, message)。始终成功返回，不抛异常。"""
    cur = current_version or meta.VERSION
    # 1) 远程清单优先
    remote = check_remote(update_url)
    latest = cur
    notes = ""
    if remote and remote.get("version"):
        latest = remote["version"]
        notes = remote.get("notes", "")
        if remote.get("homepage"):
            homepage = remote.get("homepage")

    has_update = _semver(latest) > _semver(cur)

    # 2) 本地已见版本去重
    seen = _load_seen()
    last_seen = seen.get("last_seen_version")
    if has_update and last_seen == latest:
        # 已经提示过，不打扰
        return (False, latest, "已提醒过新版本 %s，本次不再重复。" % latest)
    if has_update:
        _save_seen({"last_seen_version": latest})
        msg = ("🔔 发现新版本 v%s（当前 v%s）。\n"
               "更新内容：%s\n"
               "前往查看：%s\n"
               "有更好建议请联系：%s" % (latest, cur, notes or "详见发布页", homepage or "SkillHub", meta.AUTHOR_EMAIL))
        return (True, latest, msg)

    # 无更新：记录当前版本
    seen["last_seen_version"] = cur
    _save_seen(seen)
    if remote is None and update_url:
        return (False, cur, "当前为最新 v%s（未配置/无法访问更新源，仅本地比对）。" % cur)
    return (False, cur, "✅ 当前已是最新 v%s。" % cur)
