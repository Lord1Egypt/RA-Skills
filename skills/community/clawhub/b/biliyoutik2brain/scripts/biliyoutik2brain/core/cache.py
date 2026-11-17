"""
BiliYouTik2Brain — 统一缓存管理

三种缓存类型，各自独立文件/目录，方便单独清理：
  1. LLM结果缓存  — `~/.biliyoutik2brain_cache.json`
      key=(bvid|domain|speaker|title_salt), value=corrected_text+analysis
  2. 原始转录缓存 — `~/.biliyoutik2brain_raw.json`
      key=bvid, value=raw_text+segments+low_conf_words
  3. 音频缓存     — `~/.biliyoutik2brain_audio_cache/{bvid}.mp3`
      同BVID不重复下载

**使用示例**:
    from .cache import get_llm_cached, set_llm_cached
    cached = get_llm_cached(bvid, domain, speaker)
"""

import os
import json
import time
import shutil
from typing import Dict, Optional, List, Tuple

# ── 缓存文件路径 ──
CACHE_DIR = os.path.expanduser("~/.biliyoutik2brain")
LLM_CACHE_FILE = os.path.join(CACHE_DIR, "llm_cache.json")
RAW_CACHE_FILE = os.path.join(CACHE_DIR, "raw_cache.json")
AUDIO_CACHE_DIR = os.path.join(CACHE_DIR, "audio")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# 通用缓存 I/O
# ═══════════════════════════════════════════════════════════════

def _load_json(path: str) -> Dict:
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def _save_json(cache: Dict, path: str):
    try:
        with open(path, "w") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


# ═══════════════════════════════════════════════════════════════
# 1. LLM 结果缓存
# ═══════════════════════════════════════════════════════════════

def _llm_cache_key(bvid: str, domain: str, speaker: str, title_salt: str = "") -> str:
    salt = f"|{hash(title_salt) % 100000}" if title_salt else ""
    return f"{bvid}|{domain}|{speaker}{salt}"

def get_llm_cached(bvid: str, domain: str, speaker: str, title_salt: str = "") -> Optional[Dict]:
    cache = _load_json(LLM_CACHE_FILE)
    key = _llm_cache_key(bvid, domain, speaker, title_salt)
    if key in cache:
        return cache[key]
    broad_key = _llm_cache_key(bvid, domain, "", title_salt)
    return cache.get(broad_key)

def set_llm_cached(bvid: str, domain: str, speaker: str, data: Dict, title_salt: str = ""):
    cache = _load_json(LLM_CACHE_FILE)
    key = _llm_cache_key(bvid, domain, speaker, title_salt)
    cache[key] = {
        "corrected_text": data.get("corrected_text", ""),
        "analysis": data.get("analysis", {}),
        "cached_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    _save_json(cache, LLM_CACHE_FILE)

def clear_llm_cache():
    """清空LLM缓存（prompt升级后使用）"""
    if os.path.exists(LLM_CACHE_FILE):
        os.remove(LLM_CACHE_FILE)


# ═══════════════════════════════════════════════════════════════
# 2. 原始转录缓存
# ═══════════════════════════════════════════════════════════════

def _raw_cache_key(bvid: str) -> str:
    return f"{bvid}"

def get_raw_cached(bvid: str) -> Optional[Dict]:
    cache = _load_json(RAW_CACHE_FILE)
    key = _raw_cache_key(bvid)
    return cache.get(key)

def set_raw_cached(bvid: str, data: Dict):
    cache = _load_json(RAW_CACHE_FILE)
    key = _raw_cache_key(bvid)
    cache[key] = {
        "text": data.get("text", ""),
        "segments": data.get("segments", []),
        "low_conf_words": data.get("low_conf_words", []),
        "cached_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    _save_json(cache, RAW_CACHE_FILE)

def clear_raw_cache():
    """清空原始转录缓存（whisper参数变了之后）"""
    if os.path.exists(RAW_CACHE_FILE):
        os.remove(RAW_CACHE_FILE)


# ═══════════════════════════════════════════════════════════════
# 3. 音频缓存（断点续传）
# ═══════════════════════════════════════════════════════════════

def _audio_cache_path(bvid: str) -> str:
    return os.path.join(AUDIO_CACHE_DIR, f"{bvid}.mp3")

def get_audio_cached(bvid: str) -> Optional[str]:
    path = _audio_cache_path(bvid)
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return path
    return None

def set_audio_cached(bvid: str, src_path: str):
    if not src_path or not os.path.exists(src_path):
        return
    dst = _audio_cache_path(bvid)
    try:
        shutil.copy2(src_path, dst)
    except Exception:
        pass  # 缓存失败不影响主流程
