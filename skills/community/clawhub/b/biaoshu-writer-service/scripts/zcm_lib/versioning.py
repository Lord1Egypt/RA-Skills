"""Skill version-check helpers."""

import json
import os
import time
import urllib.request


def cmp_semver(a, b):
    """Compare MAJOR.MINOR.PATCH versions."""
    def _parse(value):
        parts = str(value).strip().split(".")
        if len(parts) != 3:
            raise ValueError("非法版本号: %r" % (value,))
        return tuple(int(x) for x in parts)

    ta, tb = _parse(a), _parse(b)
    return (ta > tb) - (ta < tb)


def fetch_latest_version(base_url, app_key, channel="", timeout=2.0):
    """GET /skill/version and return (latest, notice), or None on any failure."""
    try:
        if not app_key:
            return None
        url = base_url.rstrip("/") + "/skill/version"
        if channel:
            url += "?channel=" + channel
        req = urllib.request.Request(
            url, headers={"User-Agent": "zcm-client", "X-App-Key": app_key}, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
        data = json.loads(raw.decode("utf-8")) if raw else {}
        latest = data.get("latest")
        if not latest:
            return None
        return str(latest), data.get("notice")
    except Exception:
        return None


def maybe_check_update(
    *,
    skill_version,
    channel,
    base_url_fn,
    creds_path_fn,
    load_creds_file_fn,
    save_creds_file_fn,
    log_fn,
    force=False,
    verbose=False,
):
    """Check latest skill version once per day; never block the command."""
    try:
        if not os.path.exists(creds_path_fn()):
            if verbose:
                log_fn("未配置 Api Key，无法检查版本更新。")
            return {"checked": False, "reason": "missing_credentials"}
        creds = load_creds_file_fn()
        today = time.strftime("%Y-%m-%d")
        if not force:
            if creds.get("last_version_check") == today:
                if verbose:
                    log_fn("今天已经检查过版本更新，本次跳过。")
                return {"checked": False, "reason": "checked_today"}
            creds["last_version_check"] = today
            try:
                save_creds_file_fn(creds)
            except Exception:
                pass
        app_key = os.environ.get("ZCM_APP_KEY", "").strip() or str(creds.get("app_key", "")).strip()
        got = fetch_latest_version(base_url_fn(), app_key, channel=channel)
        if not got:
            if verbose:
                log_fn("未获取到平台版本号：可能是网络不可达、接口未配置，或平台暂未返回 latest。")
            return {"checked": True, "update_available": False, "reason": "latest_unavailable"}
        latest, notice = got
        try:
            if cmp_semver(latest, skill_version) <= 0:
                if verbose:
                    log_fn("当前已是最新版：本地 v%s，平台 v%s。" % (skill_version, latest))
                return {"checked": True, "update_available": False, "latest": latest}
        except ValueError:
            if verbose:
                log_fn("平台版本号格式异常：%s" % (latest,))
            return {"checked": True, "update_available": False, "reason": "invalid_latest", "latest": latest}
        log_fn("📢 「百炼®标书」检测到新版本 v%s（当前 v%s）。是否需要更新到最新版？（用户同意后，我会保留 config.json，只更新本 skill 的内容文件。）"
               % (latest, skill_version))
        if notice:
            log_fn("   说明：%s" % (notice,))
        return {"checked": True, "update_available": True, "latest": latest, "notice": notice}
    except Exception:
        if verbose:
            log_fn("版本检查失败：已静默跳过，不影响当前任务。")
        return {"checked": False, "reason": "error"}
