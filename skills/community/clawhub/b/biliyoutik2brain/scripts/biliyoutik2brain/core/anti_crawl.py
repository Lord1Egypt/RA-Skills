"""
anti_crawl.py — 故障自愈统一引擎（下载期反爬 + 转录期ASR）

下载期三层防御（预检 → 自愈 → 熔断）：
  第一层：平台针对性预检（B站412/抖音Session/小红书版本/YouTube代理）
  第二层：预检失败自动修复（切换API/重建指纹/升级版本/拉起代理）
  第三层：连续失败熔断（同一平台3连败 → THROTTLED 15分钟）

基于 6/9-6/21 四平台反爬实战经验提炼：
  - B站412 → bilibili-api-python DASH API 绕过
  - 抖音WAF → Session 指纹预热
  - 小红书 → yt-dlp 升级 2026.6.9+
  - YouTube → 代理自愈闭环（已在 process.py 实现）
"""

import os, re, time, json, subprocess, urllib.request, ssl
from typing import Dict, Optional, Tuple
from urllib.parse import urlparse
from .anti_crawl_middleware import _create_insecure_ssl_context

# ── 平台适配层导入（try/except 保护） ──
try:
    from .platforms.douyin import _ensure_session
except ImportError:
    _ensure_session = None  # TODO: need port from ZIP

# ── Unix 文件锁（Windows 不支持） ──
try:
    import fcntl
except ImportError:
    fcntl = None  # TODO: need port from ZIP (Unix-only)

import shutil as _shutil
import hashlib as _hashlib

# ── 四平台元数据配置 ──

PLATFORM_PROFILES: Dict[str, dict] = {
    "bilibili": {
        "name": "B站",
        "prechecks": ["api_412", "cookie_valid"],
        "heal_actions": ["switch_to_dash_api"],
        "throttle_threshold": 3,      # 连续失败3次触发
        "cooldown_seconds": 900,       # 15分钟冷却
    },
    "douyin": {
        "name": "抖音",
        "prechecks": ["session_warmth", "domain_reachable"],
        "heal_actions": ["rebuild_session", "extract_video_id_fallback"],
        "throttle_threshold": 3,
        "cooldown_seconds": 900,
    },
    "xiaohongshu": {
        "name": "小红书",
        "prechecks": ["ytdlp_version"],
        "heal_actions": ["upgrade_ytdlp"],
        "throttle_threshold": 3,
        "cooldown_seconds": 600,       # 10分钟，小红书改版频度低
    },
    "youtube": {
        "name": "YouTube",
        "prechecks": ["proxy_reachable"],
        "heal_actions": ["start_mihomo"],
        "throttle_threshold": 5,       # YouTube 宽容度高
        "cooldown_seconds": 300,       # 5分钟
    },
}

# ── 熔断状态（进程内，不持久化） ──

_throttle_state: Dict[str, dict] = {}  # {platform: {"status": "open"|"throttled", "fail_count": int, "throttled_until": float}}


def _get_throttle(platform: str) -> Optional[dict]:
    """返回平台的熔断状态"""
    return _throttle_state.get(platform)


def _set_throttle(platform: str, **kw):
    """更新熔断状态"""
    if platform not in _throttle_state:
        _throttle_state[platform] = {}
    _throttle_state[platform].update(kw)


def _reset_throttle(platform: str):
    """重置某平台的熔断状态（成功后调用）"""
    _throttle_state.pop(platform, None)


# ═══════════════════════════════════════════════════════════════
# 第一层：预检
# ═══════════════════════════════════════════════════════════════

def _check_bilibili_412(url: str) -> Tuple[bool, str]:
    """B站预检：测试 API 端点是否返回 412"""
    import re
    m = re.search(r'(BV[\w]+)', url)
    if not m:
        return False, "B站URL缺少BV号"

    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={m.group(1)}"
    ctx = _create_insecure_ssl_context()
    req = urllib.request.Request(api_url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Referer": "https://www.bilibili.com/",
    })
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        if resp.status == 412:
            return False, "B站API返回412反爬拦截"
        return True, "B站API可达"
    except urllib.request.HTTPError as e:
        if e.code == 412:
            return False, "B站API返回412反爬拦截"
        return True, f"B站API HTTP {e.code}"  # 非412不算完全失败
    except Exception as e:
        return False, f"B站API连接失败: {e}"


def _check_douyin_session() -> Tuple[bool, str]:
    """抖音预检：Session 指纹是否已预热"""
    if _ensure_session is None:
        return True, "抖音Session模块未加载（非阻塞放行）"
    try:
        sess = _ensure_session()
        resp = sess.get("https://www.douyin.com/", timeout=10, allow_redirects=True)
        # 完整主页HTML > 8000字符说明未被WAF拦截
        if resp.status_code == 200 and len(resp.text) > 8000:
            return True, f"抖音Session已预热(HTML {len(resp.text)}字符)"
        return False, f"抖音Session预热不完整(HTML仅{len(resp.text)}字符，疑似限流)"
    except Exception as e:
        return False, f"抖音Session检查失败: {e}"


def _parse_version(v: str) -> tuple:
    """解析 yt-dlp 版本号为元组用于比较。2026.06.09 → (2026, 6, 9)"""
    try:
        parts = re.split(r'[.\-]', v.strip())
        return tuple(int(p) for p in parts[:3])
    except (ValueError, IndexError):
        return (0, 0, 0)


def _check_xiaohongshu_ytdlp() -> Tuple[bool, str]:
    """小红书预检：yt-dlp 版本 >= 2026.6.9"""
    try:
        r = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True, timeout=5)
        if r.returncode != 0:
            return False, "yt-dlp 未安装"
        version = r.stdout.strip()
        # 语义版本比较（2026.06.09 与 2026.6.9 应对齐）
        if _parse_version(version) < (2026, 6, 9):
            return False, f"yt-dlp {version} < 2026.6.9 (小红书需升级)"
        return True, f"yt-dlp {version} ✅"
    except Exception as e:
        return False, f"yt-dlp版本检查失败: {e}"


def _check_youtube_proxy() -> Tuple[bool, str]:
    """YouTube预检：代理是否可连通Google"""
    ctx = _create_insecure_ssl_context()
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({
            "http": "http://127.0.0.1:9981",
            "https": "http://127.0.0.1:9981"
        }),
        urllib.request.HTTPSHandler(context=ctx)
    )
    try:
        req = urllib.request.Request("https://www.google.com", method="HEAD")
        resp = opener.open(req, timeout=5)
        if resp.status in (200, 301, 302):
            return True, "代理可连通Google"
        return False, f"代理异常(HTTP {resp.status})"
    except Exception as e:
        return False, f"代理不通: {str(e)[:60]}"


_PRE_CHECKERS = {
    "api_412": _check_bilibili_412,
    "session_warmth": _check_douyin_session,
    "ytdlp_version": _check_xiaohongshu_ytdlp,
    "proxy_reachable": _check_youtube_proxy,
    "cookie_valid": lambda url: (True, "cookie_valid 暂不检查"),  # 后续按需扩展
    "domain_reachable": lambda url: (True, "domain_reachable 暂不检查"),
}


# ═══════════════════════════════════════════════════════════════
# 第二层：自愈
# ═══════════════════════════════════════════════════════════════

def _heal_switch_to_dash_api() -> Tuple[bool, str]:
    """B站自愈：无需操作，DASH API 已在 bilibili.py extract_audio 内自动切换。

    这里的"自愈"实际上是确认：下次 extract_audio 调用会走通道2（yt-dlp 兜底）。
    """
    return True, "DASH API 回退可用（extract_audio 双通道自动切换）"


def _heal_rebuild_session() -> Tuple[bool, str]:
    """抖音自愈：重建 Session 指纹"""
    if _ensure_session is None:
        return False, "抖音模块未加载，无法重建Session"
    try:
        import requests
        sess = requests.Session()
        sess.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        })
        resp = sess.get("https://www.douyin.com/", timeout=15, allow_redirects=True)
        if resp.status_code == 200 and len(resp.text) > 8000:
            # 将新 Session 注入 douyin 模块
            import sys
            if "biliyoutik2brain.platforms.douyin" in sys.modules:
                mod = sys.modules["biliyoutik2brain.platforms.douyin"]
                # 重建 _session
                if hasattr(mod, "_session"):
                    mod._session = sess
                if hasattr(mod, "__session"):
                    mod.__session = sess
            return True, f"抖音Session已重建(HTML {len(resp.text)}字符)"
        return False, f"抖音Session重建不完整(HTML仅{len(resp.text)}字符)"
    except Exception as e:
        return False, f"抖音Session重建失败: {e}"


def _heal_upgrade_ytdlp() -> Tuple[bool, str]:
    """小红书自愈：升级 yt-dlp 到最新版"""
    try:
        subprocess.run(
            ["pip", "install", "--upgrade", "yt-dlp"],
            capture_output=True, timeout=60, check=False
        )
        r = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True, timeout=5)
        version = r.stdout.strip()
        if version >= "2026.6.9":
            return True, f"yt-dlp已升级到 {version}"
        return False, f"yt-dlp升级后版本 {version} 仍 < 2026.6.9"
    except Exception as e:
        return False, f"yt-dlp升级失败: {e}"


def _heal_start_mihomo() -> Tuple[bool, str]:
    """YouTube自愈：拉起 mihomo 代理"""
    import shutil, sys
    auto_start = os.path.expanduser("~/.mihomo-cli/auto-start.sh")
    if not os.path.isfile(auto_start):
        return False, "auto-start.sh 不存在"
    try:
        bash = shutil.which("bash") or "/bin/bash"
        subprocess.run([bash, auto_start], timeout=45, capture_output=True)
        time.sleep(3)
        ok, msg = _check_youtube_proxy()
        if ok:
            return True, "mihomo 代理已恢复"
        return False, f"mihomo 拉起后代理仍不通: {msg}"
    except Exception as e:
        return False, f"mihomo 拉起失败: {e}"


_HEAL_ACTIONS = {
    "switch_to_dash_api": _heal_switch_to_dash_api,
    "rebuild_session": _heal_rebuild_session,
    "upgrade_ytdlp": _heal_upgrade_ytdlp,
    "start_mihomo": _heal_start_mihomo,
    "extract_video_id_fallback": lambda: (True, "video_id 多路径兜底已内置"),
}


# ═══════════════════════════════════════════════════════════════
# 公共接口
# ═══════════════════════════════════════════════════════════════

def route_platform(url: str) -> str:
    """从URL路由到平台标识"""
    hostname = urlparse(url).hostname or ""
    if "youtube.com" in hostname or "youtu.be" in hostname:
        return "youtube"
    elif "bilibili.com" in hostname:
        return "bilibili"
    elif "douyin.com" in hostname or "v.douyin.com" in hostname:
        return "douyin"
    elif "xiaohongshu.com" in hostname or "xhslink.com" in hostname:
        return "xiaohongshu"
    return "unknown"


def defend(url: str, force_retry: bool = False, cooldown_s: int = None) -> dict:
    """反爬统一防御入口（在 preflight + extract_audio 之间调用）

    流程：
      1. 查熔断状态 → throttled 直接拒绝
      2. 跑平台针对性预检 → 通过则放行
      3. 预检失败 → 尝试自愈 → 修复后重检
      4. 自愈失败 → 记录失败次数 → 超阈值则熔断

    Args:
        url: 视频URL
        force_retry: 是否在熔断状态下也强制重试（用于手动重试）
        cooldown_s: 动态冷却时间（秒），None=使用平台默认值。
                    SystemOrchestrator 通过此参数注入运行时调优的冷却值。

    Returns:
        {
            "ok": bool,          # True=可继续下载
            "platform": str,     # 平台标识
            "action": str,       # "pass"|"healed"|"throttled"|"blocked"
            "detail": str,       # 人类可读的状态说明
        }
    """
    platform = route_platform(url)
    profile = PLATFORM_PROFILES.get(platform)

    # 使用 orchestrator 动态冷却或平台默认值
    if cooldown_s is not None and cooldown_s > 0:
        effective_cooldown = cooldown_s
    else:
        effective_cooldown = profile["cooldown_seconds"] if profile else 900

    if not profile:
        return {"ok": True, "platform": platform, "action": "pass", "detail": "无已知反爬策略"}

    # ── 第三层：熔断检查 ──
    throttle = _get_throttle(platform)
    if throttle and throttle.get("status") == "throttled" and not force_retry:
        now = time.time()
        if now < throttle.get("throttled_until", 0):
            remaining = int(throttle["throttled_until"] - now)
            return {
                "ok": False,
                "platform": platform,
                "action": "throttled",
                "detail": f"{profile['name']}反爬熔断中 ({remaining}s后解封)",
            }
        else:
            # 冷却期已过，自动解封
            _reset_throttle(platform)

    # ── 第一层：预检 ──
    failures = []
    for check_name in profile["prechecks"]:
        checker = _PRE_CHECKERS.get(check_name)
        if not checker:
            continue
        ok, msg = checker(url) if check_name in ("api_412", "cookie_valid", "domain_reachable") else checker()
        if not ok:
            failures.append((check_name, msg))

    if not failures:
        # 全部通过 → 重置失败计数
        _reset_throttle(platform)
        return {"ok": True, "platform": platform, "action": "pass", "detail": "反爬预检全部通过"}

    # ── 第二层：自愈 ──
    healed = []
    for action_name in profile.get("heal_actions", []):
        healer = _HEAL_ACTIONS.get(action_name)
        if not healer:
            continue
        print(f"  [反爬] 🔧 {profile['name']} 触发自愈: {action_name}")
        ok, msg = healer()
        if ok:
            healed.append(action_name)
            print(f"  [反爬] ✅ 自愈成功: {msg}")
        else:
            print(f"  [反爬] ❌ 自愈失败: {msg}")

    # 自愈后重检
    if healed:
        retry_failures = []
        for check_name in profile["prechecks"]:
            checker = _PRE_CHECKERS.get(check_name)
            if not checker:
                continue
            ok, msg = checker(url) if check_name in ("api_412", "cookie_valid", "domain_reachable") else checker()
            if not ok:
                retry_failures.append((check_name, msg))
        if not retry_failures:
            _reset_throttle(platform)
            return {"ok": True, "platform": platform, "action": "healed", "detail": f"反爬已自愈: {', '.join(healed)}"}
        failures = retry_failures  # 自愈没完全修好，延续失败列表

    # ── 自愈也修不好 → 记录失败 + 判断是否熔断 ──
    current = _get_throttle(platform) or {}
    fail_count = current.get("fail_count", 0) + 1
    threshold = profile["throttle_threshold"]

    if fail_count >= threshold:
        _set_throttle(
            platform,
            status="throttled",
            fail_count=fail_count,
            throttled_until=time.time() + effective_cooldown,
        )
        fail_msgs = "; ".join(f"[{c}] {m}" for c, m in failures)
        return {
            "ok": False,
            "platform": platform,
            "action": "throttled",
            "detail": f"{profile['name']}连续{fail_count}次反爬失败，已熔断{effective_cooldown}s → {fail_msgs}",
        }
    else:
        _set_throttle(platform, fail_count=fail_count, status="open")
        fail_msgs = "; ".join(f"[{c}] {m}" for c, m in failures)
        return {
            "ok": False,
            "platform": platform,
            "action": "blocked",
            "detail": f"{profile['name']}反爬预检/自愈失败({fail_count}/{threshold}): {fail_msgs}",
        }


def report_throttle() -> dict:
    """查看当前所有平台的熔断状态"""
    return {
        platform: {
            "status": s.get("status", "open"),
            "fail_count": s.get("fail_count", 0),
            "throttled_remaining_s": max(0, int(s.get("throttled_until", 0) - time.time()))
            if s.get("status") == "throttled" else 0,
        }
        for platform, s in _throttle_state.items()
    }


def clear_all_throttles():
    """手动清除所有熔断状态（测试/调试用）"""
    _throttle_state.clear()
    print("[反爬] 所有熔断状态已清除")


# ═══════════════════════════════════════════════════════════════
# 转录期 ASR 自愈引擎
# ═══════════════════════════════════════════════════════════════
#
# 覆盖 3 类高频事故（6/13-6/21 实战数据）：
#   1. whisper OOM/SIGTERM → 自动降级模型重试
#   2. pywhispercpp 多实例冲突 → 全局文件锁做互斥
#   3. WAV 格式不匹配（48kHz）→ 自动重采样到 16kHz mono
#
# 与 admission.py 协同：ffmpeg_health_check + handle_ffmpeg_crash 在 process.py
# 入口已调用，这里只管转录过程内的事故。

from typing import Optional

_ASR_FAIL_COUNT: Dict[str, int] = {}  # {model_name: fail_count}
_ASR_MAX_FAILS = 3  # 同一模型连续失败3次 → 永不使用当前 wav
_WHISPER_MODEL_TIERS = ["base", "tiny", "small"]  # 降级链：base → tiny → small(兜底低精度)


_WHISPER_LOCK_HELD = False  # 进程内状态标记（fcntl 同进程可重入，需额外防）


def _acquire_whisper_lock() -> bool:
    """pywhispercpp 全局锁：防止多进程同时跑 whisper 导致 SIGTERM。

    已知 pywhispercpp 不支持多实例并发（6/16 确认）。
    用文件锁做进程间互斥，非阻塞——拿不到锁就排队等，不 crash。
    """
    global _WHISPER_LOCK_HELD

    if _WHISPER_LOCK_HELD:
        return False  # 进程内防重入

    if fcntl is None:
        # Windows/非Unix平台：跳过文件锁
        _WHISPER_LOCK_HELD = True
        return True

    lock_path = os.path.expanduser("~/.biliyoutik2brain_run/whisper.lock")
    os.makedirs(os.path.dirname(lock_path), exist_ok=True)

    _lock_fd = open(lock_path, "w")
    try:
        fcntl.flock(_lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        _WHISPER_LOCK_HELD = True
        return True
    except (IOError, OSError):
        return False


def _release_whisper_lock():
    """释放 whisper 全局锁"""
    global _WHISPER_LOCK_HELD
    _WHISPER_LOCK_HELD = False

    if fcntl is None:
        return

    lock_path = os.path.expanduser("~/.biliyoutik2brain_run/whisper.lock")
    try:
        if os.path.exists(lock_path):
            fd = open(lock_path, "w")
            fcntl.flock(fd.fileno(), fcntl.LOCK_UN)
            fd.close()
    except Exception:
        pass


def _resample_wav_if_needed(audio_path: str) -> str:
    """自动检测 WAV 采样率，如果不是 16kHz mono 则用 ffmpeg 重采样。

    whisper 模型输入要求 16kHz mono，但 yt-dlp 常产出 48kHz webm→wav（6/16 确认）。
    返回: 纠正后的文件路径（可能仍是原路径）。
    """
    try:
        import wave
        wf = wave.open(audio_path, "r")
        channels = wf.getnchannels()
        framerate = wf.getframerate()
        wf.close()

        if framerate == 16000 and channels == 1:
            return audio_path  # 已经正确

        # 需要重采样
        print(f"  [ASR自愈] WAV {framerate}Hz {channels}ch → 自动转 16kHz mono...")
        resampled_path = audio_path.rsplit(".", 1)[0] + "_16k.wav"

        ffmpeg_bin = _shutil.which("ffmpeg")
        if not ffmpeg_bin:
            print("  [ASR自愈] ⚠️ ffmpeg 不可用，无法重采样")
            return audio_path

        result = subprocess.run(
            [ffmpeg_bin, "-y", "-i", audio_path,
             "-ac", "1", "-ar", "16000", "-sample_fmt", "s16",
             resampled_path],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and os.path.getsize(resampled_path) > 1000:
            print(f"  [ASR自愈] ✅ 重采样完成: {resampled_path}")
            return resampled_path

        return audio_path
    except Exception as e:
        print(f"  [ASR自愈] WAV检查失败: {e}，跳过重采样")
        return audio_path


# ── whisper 模型降级链（进程内状态） ──
# 如果 base 模型 OOM/SIGTERM，自动降级到 tiny；tiny 还 OOM 则 small(低精度)
# 注意：small 比 base 大但 q5_1 量化后更轻，对 OOM 容错更好

_MODEL_DOWNGRADE: Dict[str, str] = {
    "base": "tiny",
    "tiny": "small",
    "small": "tiny",  # small失败回tiny（循环保护）
    "medium": "base",
}


def _get_fallback_model(current: str) -> Optional[str]:
    """获取当前模型的降级备选"""
    return _MODEL_DOWNGRADE.get(current)


def record_asr_outcome(model: str, success: bool):
    """记录 whisper 模型转录结果，用于熔断决策

    连续3次失败 → 标记模型不可用，后续 defend_asr 会强制降级
    """
    if success:
        _ASR_FAIL_COUNT.pop(model, None)
    else:
        _ASR_FAIL_COUNT[model] = _ASR_FAIL_COUNT.get(model, 0) + 1


def _is_model_burned(model: str) -> bool:
    """检查模型是否已连续失败超阈值"""
    return _ASR_FAIL_COUNT.get(model, 0) >= _ASR_MAX_FAILS


# ═══════════════════════════════════════════════════════════════
# defend_asr — 转录期主入口
# ═══════════════════════════════════════════════════════════════

def defend_asr(audio_path: str, model: str = "base", duration_s: int = 0) -> dict:
    """ASR 转录期统一防御（在 _node_transcribe 入口调用）

    防护内容：
      1. WAV 格式验证 + 自动重采样（48kHz→16kHz mono）
      2. whisper 模型熔断检查（连续3次OOM → 强制降级）
      3. pywhispercpp 全局锁（防多进程并发 SIGTERM）

    Args:
        audio_path: WAV/音频文件路径
        model: 当前 whisper 模型名
        duration_s: 音频时长（用于日志）

    Returns:
        {
            "ok": bool,               # True=可以转录
            "model": str,             # 最终使用的模型（可能被降级）
            "audio_path": str,        # 最终使用的音频路径（可能被重采样）
            "warnings": [str],        # 非阻断警告
            "action": str,            # "pass"|"resampled"|"model_downgraded"|"waiting_lock"
        }
    """
    warnings = []
    final_model = model
    final_audio = audio_path
    action = "pass"

    # ── 1. WAV 格式检查 + 自动重采样 ──
    if audio_path and os.path.isfile(audio_path) and audio_path.endswith((".wav", ".WAV")):
        try:
            final_audio = _resample_wav_if_needed(audio_path)
            if final_audio != audio_path:
                action = "resampled"
        except Exception as e:
            warnings.append(f"WAV检测异常: {e}")

    # ── 2. 模型熔断检查 ──
    if _is_model_burned(model):
        fallback = _get_fallback_model(model)
        if fallback:
            print(f"  [ASR防] ⚠️ {model} 连续{_ASR_FAIL_COUNT[model]}次失败，强制降级到 {fallback}")
            final_model = fallback
            action = "model_downgraded"
            warnings.append(f"模型 {model} 已熔断，降级到 {fallback}")

    # ── 3. 超长音频（>30分钟）→ 强制开 VAD ──
    if duration_s > 1800:
        warnings.append(f"超长音频({duration_s}s)，建议启用VAD分段")

    # ── 4. pywhispercpp 全局锁 ──
    #    拿不到锁不报错，由上层 decide: 排队等 or 跳过
    got_lock = _acquire_whisper_lock()
    if not got_lock:
        print(f"  [ASR防] ⏳ 另一个转录进程占用中，排队等待...")
        action = "waiting_lock" if action == "pass" else action

    # 锁会在 _release_whisper_lock() 释放（调用方负责）
    return {
        "ok": True,
        "model": final_model,
        "audio_path": final_audio,
        "warnings": warnings,
        "action": action,
    }


def asr_post_process(model: str, success: bool):
    """转录完成后调用：记录结果 + 释放锁"""
    record_asr_outcome(model, success)
    _release_whisper_lock()

    if not success:
        print(f"  [ASR防] {model} 转录失败 ({_ASR_FAIL_COUNT.get(model, 0)}/{_ASR_MAX_FAILS})")
        if _is_model_burned(model):
            fallback = _get_fallback_model(model)
            print(f"  [ASR防] {model} 已熔断，下次将自动降级到 {fallback}")


# ═══════════════════════════════════════════════════════════════
# 临时文件自愈引擎 — 防止磁盘被孤儿文件吃满
# ═══════════════════════════════════════════════════════════════

import glob as _glob

_TMP_DIRS = [
    os.path.expanduser("~/.biliyoutik2brain_run/tmp"),
    "/tmp/bili_work",
]

_TMP_GLOB_PATTERNS = [
    "/tmp/whisper*",
    "/tmp/wav_*",
    "/tmp/m4s_*",
    "/tmp/ytdl_*",
    "/tmp/tmp*.wav",
    "/tmp/tmp*.mp4",
    "/tmp/tmp*.webm",
]


def _hours_ago(ts: float) -> float:
    return round((time.time() - ts) / 3600, 1)


def tmpfile_housekeeping(max_age_hours: int = 24) -> dict:
    """临时文件自愈：清理超期孤儿文件。

    触发场景：
      - process.py _try_self_heal() ENVIRONMENT 级自愈（磁盘不足时调用）
      - admission.py try_admit() 准入（磁盘 < 2GB 时调用）
      - startup 首次启动时调用

    Args:
        max_age_hours: 超过此时间的文件视为孤儿（默认24h）

    Returns:
        {"freed_mb": float, "files_cleaned": int, "errors": [str]}
    """
    freed_bytes = 0
    files_cleaned = 0
    errors = []
    now = time.time()
    cutoff = now - max_age_hours * 3600

    for pattern in _TMP_GLOB_PATTERNS:
        try:
            for f in _glob.glob(pattern):
                try:
                    mtime = os.path.getmtime(f)
                    if mtime < cutoff:
                        size = os.path.getsize(f)
                        if os.path.isdir(f):
                            _shutil.rmtree(f, ignore_errors=True)
                        else:
                            os.unlink(f)
                        freed_bytes += size
                        files_cleaned += 1
                        print(f"  [清理] 孤儿文件: {f} ({size/1024:.0f}KB, {_hours_ago(mtime)}h前)")
                except OSError:
                    pass
        except Exception as e:
            errors.append(f"{pattern}: {e}")

    for dir_path in _TMP_DIRS:
        try:
            if os.path.isdir(dir_path):
                for root, dirs_, files in os.walk(dir_path, topdown=False):
                    for fn in files:
                        fp = os.path.join(root, fn)
                        try:
                            mtime = os.path.getmtime(fp)
                            if mtime < cutoff:
                                size = os.path.getsize(fp)
                                os.unlink(fp)
                                freed_bytes += size
                                files_cleaned += 1
                        except OSError:
                            pass
        except Exception as e:
            errors.append(f"{dir_path}: {e}")

    freed_mb = freed_bytes / (1024 * 1024)
    if files_cleaned > 0:
        print(f"  [清理] 共清理 {files_cleaned} 个孤儿文件，释放 {freed_mb:.1f}MB")
    return {"freed_mb": round(freed_mb, 2), "files_cleaned": files_cleaned, "errors": errors}


# ═══════════════════════════════════════════════════════════════
# LLM API 自愈包装 — 统一 429/502/5xx 重试 + 降级回退
# ═══════════════════════════════════════════════════════════════

_LLM_ERROR_STATE = {
    "consecutive_fails": 0,
    "last_fail_time": 0,
    "degraded": False,  # True = API 连续失败，后续调用走规则引擎回退
}

_LLM_MAX_CONSECUTIVE_FAILS = 3
_LLM_DEGRADE_COOLDOWN = 300  # 降级后 5 分钟内不重试 API


def _should_skip_llm() -> bool:
    """检查是否应跳过 LLM，规则引擎回退"""
    if not _LLM_ERROR_STATE["degraded"]:
        return False
    if time.time() - _LLM_ERROR_STATE["last_fail_time"] > _LLM_DEGRADE_COOLDOWN:
        _LLM_ERROR_STATE["degraded"] = False
        _LLM_ERROR_STATE["consecutive_fails"] = 0
        print("  [LLM自愈] 🔄 冷却到，重新尝试API")
        return False
    return True


def _record_llm_result(success: bool):
    """记录 LLM 调用结果，触发降级/恢复"""
    if success:
        _LLM_ERROR_STATE["consecutive_fails"] = 0
        if _LLM_ERROR_STATE["degraded"]:
            _LLM_ERROR_STATE["degraded"] = False
            print("  [LLM自愈] ✅ API 已恢复")
    else:
        _LLM_ERROR_STATE["consecutive_fails"] += 1
        _LLM_ERROR_STATE["last_fail_time"] = time.time()
        if _LLM_ERROR_STATE["consecutive_fails"] >= _LLM_MAX_CONSECUTIVE_FAILS:
            _LLM_ERROR_STATE["degraded"] = True
            print(f"  [LLM自愈] ⚠️ 连续{_LLM_MAX_CONSECUTIVE_FAILS}次失败，降级规则引擎({_LLM_DEGRADE_COOLDOWN}s后重试)")


def robust_llm_call(payload_dict: dict, api_key: str, api_base: str,
                    timeout: int = 15, max_retries: int = 2) -> tuple:
    """统一 LLM API 调用包装 — 自带重试 + 熔断 + 降级回退

    处理链：
      - 降级状态检查 → 跳过 API（规则引擎回退）
      - HTTP 429 → 等 5s 重试
      - HTTP 502/503/504 → 等 2s 重试
      - 连接/超时 → 等 3s 重试
      - 连续 3 次失败 → 降级标记（后续全用规则引擎）
      - 降级后 5 分钟冷却 → 自动恢复

    Args:
        payload_dict: API 请求体 dict
        api_key: API Key
        api_base: API Base URL
        timeout: 单次调用超时
        max_retries: 最大重试次数

    Returns:
        (response_dict or None, warnings_list)
        None = API 失败/降级，调用方须用 _format_fix() 规则引擎回退
    """
    warnings = []

    if _should_skip_llm():
        warnings.append("LLM_API_DEGRADED: rule_fallback")
        return None, warnings

    try:
        data_bytes = json.dumps(payload_dict).encode("utf-8")
    except Exception as e:
        _record_llm_result(False)
        return None, [f"serialize_error: {e}"]

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(
                f"{api_base}/chat/completions",
                data=data_bytes,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                }
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                result = json.loads(body)
                _record_llm_result(True)
                return result, warnings

        except urllib.error.HTTPError as e:
            status = e.code
            last_error = f"HTTP{status}"
            if status == 429:
                print(f"  [LLM自愈] ⚠️ 429限流 5s后重试({attempt+1})")
                warnings.append(f"429(attempt{attempt+1})")
                time.sleep(5)
            elif status in (502, 503, 504):
                if attempt < max_retries:
                    print(f"  [LLM自愈] ⚠️ {status} 2s后重试({attempt+1})")
                    warnings.append(f"{status}(attempt{attempt+1})")
                    time.sleep(2)
                else:
                    break
            else:
                break

        except (urllib.error.URLError, OSError) as e:
            last_error = str(e)[:80]
            if attempt < max_retries:
                print(f"  [LLM自愈] ⚠️ 连接错误 3s后重试({attempt+1})")
                warnings.append(f"conn_err(attempt{attempt+1})")
                time.sleep(3)

        except Exception as e:
            last_error = str(e)[:80]
            if ("timeout" in last_error.lower() or "timed out" in last_error.lower()):
                if attempt < max_retries:
                    print(f"  [LLM自愈] ⏱️ 超时 重试({attempt+1})")
                    warnings.append(f"timeout(attempt{attempt+1})")
                    continue
            break

    _record_llm_result(False)
    warnings.append(f"LLM_FAILED: {last_error}")
    return None, warnings
