"""
BiliYouTik2Brain — 采集节点

职责：
  1. 平台识别 + 适配器调用
  2. 音频缓存断点续传（按 BVID）
  3. 不碰转录/LLM
"""

import os, sys, re, json, time
from typing import Dict, Optional, List, Tuple
from urllib.parse import urlparse

from .schemas import CollectResult
from .config import PlatformRegistry
from .cache import get_audio_cached, set_audio_cached


def _ensure_platforms():
    """确保平台模块已加载（注册到 PlatformRegistry）"""
    if PlatformRegistry.list_platforms():
        return
    try:
        from biliyoutik2brain.platforms import bilibili, douyin, xiaohongshu, youtube
    except ImportError:
        pass


def collect(url: str) -> CollectResult:
    """采集数据：自动识别平台并采集"""
    _ensure_platforms()
    extractor_cls = PlatformRegistry.identify(url)
    if not extractor_cls:
        print(f"  ❌ 不支持的平台: {url}")
        from biliyoutik2brain.core.schemas import CollectResult
        return CollectResult(
            video=None, audio=None, subtitle=None, comments=None
        )
    
    extractor = extractor_cls()
    platform = extractor.platform if hasattr(extractor, 'platform') else "未知"
    print(f"  [平台] {platform}")
    return extractor.collect(url)


def _node_collect(url: str, **kw) -> CollectResult:
    """节点：采集数据（含音频缓存断点续传）"""
    print(f"  [采集] {url}")
    
    # 提取BVID用于音频缓存检查
    bvid = ""
    if "bilibili.com/video/" in url:
        m_bv = re.search(r'BV\w+', urlparse(url).path)
        if m_bv:
            bvid = m_bv.group(0)
            cached = get_audio_cached(bvid)
            if cached:
                print(f"  [音频] 📦 命中缓存: {bvid}.mp3 ({os.path.getsize(cached)//1024}KB)")
                collected = collect(url)
                collected.audio.file_path = cached
                print(f"  [视频] {collected.video.title}")
                print(f"  [时长] {collected.video.duration}s | UP主: {collected.video.uploader}")
                return collected
    
    collected = collect(url)
    vi = collected.video
    print(f"  [视频] {vi.title}")
    print(f"  [时长] {vi.duration}s | UP主: {vi.uploader}")
    if not collected.audio.success:
        raise RuntimeError(f"音频采集失败: {collected.audio.error}")
    
    # 缓存音频
    if bvid and collected.audio.file_path and os.path.exists(collected.audio.file_path):
        set_audio_cached(bvid, collected.audio.file_path)
        print(f"  [音频] 已缓存: {bvid}.mp3")
    
    return collected


# ================================================================
# 移植自 ZIP v1.x: node_collect.py 扩展内容
# ================================================================

def _read_env(ctx: Dict) -> Dict:
    """从 ctx 读取 L0 环境参数（安全 fallback）"""
    env = ctx.get("environment", {})
    if not isinstance(env, dict):
        return {}
    return {
        "max_concurrency": env.get("max_download_concurrency", 2),
        "timeout_s": env.get("download_timeout_s", 120),
        "retry_count": env.get("retry_count", 3),
        "enable_ocr": env.get("enable_ocr", True),
        "enable_bleep": env.get("enable_bleep", True),
        "whisper_model": env.get("whisper_model", "base"),
        "disk_free_gb": env.get("disk_free_gb", 10),
        "network_latency_ms": env.get("network_latency_ms", 200),
        "proxy_available": env.get("proxy_available", True),
    }



def _run_preflight(url: str) -> dict:
    """下载前预检：适配器/版本/反爬/磁盘。
    
    接 auto_fixer.preflight()，在采集真正开始前做 6 项检查，
    有问题早发现早报错，不等 yt-dlp 跑到一半才炸。
    
    Returns:
        {"ok": bool, "warnings": [...], "errors": [...]} — ok=False 时有阻断性错误
    """
    from urllib.parse import urlparse
    hostname = urlparse(url).hostname or ""
    
    # 平台路由
    if "youtube.com" in hostname or "youtu.be" in hostname:
        platform = "youtube"
    elif "bilibili.com" in hostname:
        platform = "bilibili"
    elif "douyin.com" in hostname or "v.douyin.com" in hostname:
        platform = "douyin"
    elif "xiaohongshu.com" in hostname or "xhslink.com" in hostname:
        platform = "xiaohongshu"
    else:
        platform = "unknown"
    
    try:
        from .auto_fixer import preflight
        result = preflight(platform, url)
    except ImportError:
        result = {"ok": True, "warnings": ["preflight 不可用，跳过"], "errors": []}
    
    if result.get("warnings"):
        for w in result["warnings"]:
            print(f"  [预检] ⚠️ {w}")
    if result.get("errors"):
        for e in result["errors"]:
            print(f"  [预检] ❌ {e}")
        # 阻断性错误 → 抛 ResourceError
        raise ResourceError(
            f"下载前预检失败: {'; '.join(result['errors'])}",
            ErrorTier.ENVIRONMENT
        )
    
    if result.get("ok"):
        print(f"  [预检] ✅ {platform} 通过")
    
    return result



def _run_anti_crawl_defense(url: str, cooldown_s: int = None) -> dict:
    """反爬统一防御（预检 → 自愈 → 熔断三层）。
    
    在 _run_preflight 之后、collect() 采集之前调用。
    用 anti_crawl.defend() 做平台针对性反爬判断。
    
    Args:
        url: 视频URL
        cooldown_s: SystemOrchestrator 动态冷却时间（可选，None=默认）
    
    Returns:
        {"ok": bool, "action": "pass"|"healed"|"throttled"|"blocked", "detail": str}
    """
    from .anti_crawl import defend
    result = defend(url, cooldown_s=cooldown_s)
    
    if result.get("action") == "pass":
        print(f"  [反爬] ✅ {result['platform']}")
    elif result.get("action") == "healed":
        print(f"  [反爬] ✅ 已自愈: {result['detail']}")
    elif result.get("action") == "throttled":
        print(f"  [反爬] 🚫 熔断: {result['detail']}")
    else:
        print(f"  [反爬] ⛔ 拦截: {result['detail']}")
    
    return result

