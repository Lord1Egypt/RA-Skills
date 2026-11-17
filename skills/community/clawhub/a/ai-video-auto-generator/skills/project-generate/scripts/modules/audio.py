"""
音效与环境音频模块 — FreeSound 搜索下载 + ffmpeg 噪音降级

依赖：requests（可选，无 API Key 时降级到 ffmpeg 噪音）
"""
from __future__ import annotations
import hashlib, json, os, subprocess
from typing import Optional

from modules.config import _script_path, _sounds_dir

# FreeSound API 配置（可选）
FS_SEARCH_URL = "https://freesound.org/apiv2/search/text/"
FS_DOWNLOAD_URL = "https://freesound.org/apiv2/sounds/{sid}/download/"

# 场景/动作 → 搜索关键词映射
ENV_KEYWORDS = {
    "战场": "battle ambient",
    "战争": "war ambience",
    "号角": "war horn",
    "风声": "wind howling",
    "风沙": "wind sand desert",
    "刀剑": "sword clash",
    "森林": "forest ambience",
    "虫鸣": "cricket night",
    "雨声": "rain heavy",
    "雷声": "thunder storm",
    "马蹄": "horse gallop",
    "火焰": "fire burning",
    "流水": "river stream water",
    "城镇": "town market ambience",
    "室内": "indoor room tone",
    "悬疑": "suspense dark ambient",
    "庄严": "epic orchestral",
}

# 预生成的 ffmpeg 噪音类型
NOISE_TYPES = {
    "wind": 'anoisesrc=color=brown:duration={dur}:sample_rate=44100,lowpass=f=200',
    "rain": 'anoisesrc=color=pink:duration={dur}:sample_rate=44100,lowpass=f=2000,volume=0.3',
    "rumble": 'anoisesrc=color=brown:duration={dur}:sample_rate=44100,lowpass=f=80,volume=0.5',
    "hiss": 'anoisesrc=color=white:duration={dur}:sample_rate=44100,lowpass=f=4000,volume=0.1',
    "hum": 'sine=f=60:duration={dur}:sample_rate=44100,volume=0.05',
}


def _sounds(project: str) -> str:
    p = _sounds_dir(project)
    os.makedirs(p, exist_ok=True)
    return p


def load_script(project: str) -> dict:
    with open(_script_path(project), encoding="utf-8") as f:
        return json.load(f)


# ── FreeSound API ────────────────────────────────────────

def _get_fs_key() -> Optional[str]:
    """加载 FreeSound API Key（config Layer 2 优先级链 → ~/.freesound-api-key → FREESOUND_API_KEY）。"""
    # 优先用 _shared_tools 统一配置读取（走 Layer 2 优先级链）
    try:
        from _shared_tools import get
        key = get("freesound", "api_key")
        if key:
            return key.strip()
    except ImportError:
        pass

    # 降级到传统共享凭证文件/环境变量（同账号多平台共用，非平台级配置）
    legacy = os.path.expanduser("~/.freesound-api-key")
    if os.path.isfile(legacy):
        with open(legacy) as f:
            return f.read().strip()
    return os.environ.get("FREESOUND_API_KEY")


def search_sounds(query: str, max_results: int = 3, duration_max: int = 30) -> list[dict]:
    """
    搜索 FreeSound 音效。
    返回：[{id, name, preview_url, duration}, ...]
    """
    key = _get_fs_key()
    if not key:
        print(f"  [音效] ⚠️ 未配置 FreeSound API Key (~/.freesound-api-key)")
        return []

    try:
        import requests
    except ImportError:
        print("  [音效] ⚠️ requests 未安装，无法搜索 FreeSound。请运行: pip install requests")
        return []
    try:
        r = requests.get(FS_SEARCH_URL, params={
            "query": query,
            "fields": "id,name,previews,duration",
            "filter": f"duration:[0 TO {duration_max}]",
            "page_size": max_results,
        }, headers={"Authorization": f"Token {key}"}, timeout=15)
        if r.status_code != 200:
            print(f"  [音效] ⚠️ FreeSound 搜索失败: HTTP {r.status_code}")
            return []

        results = []
        for s in r.json().get("results", []):
            previews = s.get("previews", {})
            url = previews.get("preview-lq-mp3") or previews.get("preview-hq-mp3")
            if url:
                results.append({
                    "id": s["id"],
                    "name": s.get("name", ""),
                    "preview_url": url,
                    "duration": s.get("duration", 0),
                })
        return results
    except Exception as e:
        print(f"  [音效] ⚠️ FreeSound 异常: {e}")
        return []


def download_preview(url: str, output_path: str) -> bool:
    """下载 FreeSound 预览音频到本地"""
    import requests
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(r.content)
            return os.path.isfile(output_path)
    except Exception:
        pass
    return False


# ── ffmpeg 噪音生成（降级） ──────────────────────────────

def _get_ffmpeg() -> str:
    try:
        from moviepy.config import FFMPEG_BINARY
        return FFMPEG_BINARY
    except Exception:
        return "ffmpeg"


def generate_ffmpeg_ambient(description: str, duration: float, output_path: str) -> bool:
    """
    根据描述匹配噪音类型，用 ffmpeg 生成环境音。

    匹配逻辑：简单关键词映射（雨→rain, 风→wind, 室内→hum 等）。
    当 FreeSound 搜索为空或不可用时作为降级方案。
    关键词匹配可能不准确，建议改进为语义分析。
    """
    desc = description.lower()
    # 匹配噪音类型
    noise_type = "wind"  # default
    if any(k in desc for k in ["战场", "战争", "号角"]):
        noise_type = "rumble"
    elif any(k in desc for k in ["雨", "雷"]):
        noise_type = "rain"
    elif any(k in desc for k in ["风", "沙"]):
        noise_type = "wind"
    elif any(k in desc for k in ["室内", "大殿", "房间"]):
        noise_type = "hum"
    elif any(k in desc for k in ["森林", "虫", "流水"]):
        noise_type = "hiss"

    ffmpeg = _get_ffmpeg()
    filter_exp = NOISE_TYPES[noise_type].format(dur=duration)
    cmd = [ffmpeg, "-y", "-filter_complex", filter_exp, "-c:a", "aac", "-b:a", "64k", output_path]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    if r.returncode == 0 and os.path.isfile(output_path):
        print(f"  [音效] ⏺ 生成 {noise_type} 环境音 ({duration}s)")
        return True
    return False


# ── 主函数 ───────────────────────────────────────────────

def generate_ambient(project: str, scene_id: int, description: str, duration: float) -> Optional[str]:
    """
    生成场景环境音。优先 FreeSound 搜索下载，降级到 ffmpeg 噪音。
    返回 WAV/MP3 路径。
    """
    sounds_dir = _sounds(project)
    out_path = os.path.join(sounds_dir, f"ambient_scene{scene_id:02d}.mp3")

    # 如果已存在，直接返回
    if os.path.isfile(out_path):
        return out_path

    # 提取英文搜索关键词
    kw = ENV_KEYWORDS.get(description, description)
    if not kw:
        kw = description

    # 尝试 FreeSound
    results = search_sounds(kw, duration_max=int(duration) + 5)
    for r in results[:1]:
        ok = download_preview(r["preview_url"], out_path)
        if ok:
            print(f"  [音效] ✅ FreeSound: {r['name']}")
            return out_path

    # 降级到 ffmpeg 噪音
    ok = generate_ffmpeg_ambient(kw, duration, out_path)
    return out_path if ok else None


def generate_all_ambients(project: str, shot_count: int) -> list[dict]:
    """
    读取 script.json 的 scene_cards，为每个场景生成环境音。
    返回：[{scene, path, start_time, duration}, ...]
    """
    s = load_script(project)
    scenes = s.get("scene_cards", [])
    if not scenes:
        return []

    # 从 shot_groups 获取每个 scene 覆盖的时间范围
    groups = s.get("shot_groups", [])
    shot_durs = {sh["id"]: float(sh.get("duration_seconds", 5)) for sh in s.get("shots", [])}

    # 计算每个 group 的起止时间
    group_timing = []
    cur = 0.0
    for g in groups:
        g_shots = g.get("shots", [])
        g_dur = sum(shot_durs.get(sid, 5) for sid in g_shots)
        # 减去转场重叠
        tdur = float(g.get("transition_duration", 0.3))
        transition_overlap = tdur * (len(g_shots) - 1)
        g_actual = g_dur - transition_overlap
        group_timing.append({
            "name": g.get("name", ""),
            "start": cur,
            "end": cur + g_actual,
            "duration": g_actual,
        })
        cur += g_actual

    results = []
    for i, scene in enumerate(scenes):
        desc = scene.get("audio_env", "")
        if not desc:
            continue

        # 找到对应的 group（按顺序匹配）
        timing = group_timing[i] if i < len(group_timing) else None
        if not timing:
            continue

        path = generate_ambient(project, i + 1, desc, timing["duration"])
        if path:
            results.append({
                "scene": scene.get("scene", f"scene_{i+1:02d}"),
                "path": path,
                "start_time": timing["start"],
                "duration": timing["duration"],
            })

    return results


# ── BGM ──────────────────────────────────────────────────

BGM_KEYWORDS = {
    "古风": "guzheng chinese traditional",
    "战场": "epic orchestral battle",
    "史诗": "epic orchestral cinematic",
    "悬疑": "dark suspense ambient",
    "悲伤": "sad piano melancholic",
    "宫廷": "chinese court traditional",
    "宁静": "calm piano nature ambient",
    "战斗": "action intense orchestral",
    "紧张": "tense suspense thriller",
}


def tone_to_bgm_keyword(tone: str) -> str:
    for cn, en in BGM_KEYWORDS.items():
        if cn in tone:
            return en
    return "cinematic ambient background music"


def _bgm_cache_path(project: str, keyword: str) -> str:
    """按 keyword 生成确定性文件名，不同 tone→不同文件→各自缓存"""
    h = hashlib.md5(keyword.encode()).hexdigest()[:8]
    return os.path.join(project, "sounds", f"bgm_{h}.mp3")


def generate_bgm(project: str, total_duration: float) -> Optional[str]:
    """根据 script.tone 生成 BGM，优先使用自定义 bgm_custom.mp3"""
    sounds_dir = os.path.join(project, "sounds")

    # 优先检查自定义 BGM
    custom = os.path.join(sounds_dir, "bgm_custom.mp3")
    if os.path.isfile(custom):
        print(f"  [BGM] ✅ 自定义: bgm_custom.mp3")
        return custom

    s = load_script(project)
    tone = s.get("script", {}).get("tone", "")
    keyword = tone_to_bgm_keyword(tone)
    out_path = _bgm_cache_path(project, keyword)

    if os.path.isfile(out_path):
        print(f"  [BGM] ✅ 缓存命中: {os.path.basename(out_path)}")
        return out_path

    sounds_dir = os.path.join(project, "sounds")
    os.makedirs(sounds_dir, exist_ok=True)

    results = search_sounds(keyword, max_results=5, duration_max=int(total_duration) + 10)
    if not results:
        print(f"  [BGM] ⚠️ 未搜索到匹配音乐，跳过")
        return None

    best = min(results, key=lambda r: abs(float(r.get("duration", 0)) - total_duration))
    ok = download_preview(best["preview_url"], out_path)
    if ok:
        print(f"  [BGM] ✅ {best['name']} ({best.get('duration', 0)}s) → {os.path.basename(out_path)}")
        return out_path
    return None


# ── 逐镜头音效（audio_cue） ─────────────────────────────

import re as _re

_AE = _re.compile(r"[→➜,،、，。；;！!？?]+")

def generate_shot_cues(project: str, shot_count: int) -> list[dict]:
    """
    读取每个 shot 的 audio_cue，搜索 FreeSound 下载，返回每条 cue 的时间信息。
    audio_cue 用 → 或 、分割多个独立音效，均匀分布在 shot 时长内。
    返回：[{shot_id, path, start_time, duration}, ...]
    """
    s = load_script(project)
    shots_map = {sh["id"]: sh for sh in s.get("shots", [])}
    from speech import shot_durations as _sd
    timing = _sd(project, shot_count)
    results = []

    for i in range(shot_count):
        sid = i + 1
        shot = shots_map.get(sid, {})
        cue_raw = shot.get("audio_cue", "").strip()
        if not cue_raw:
            continue

        # 分割独立音效
        cues = [c.strip() for c in _AE.split(cue_raw) if c.strip()]
        n = len(cues)
        if n == 0:
            continue

        shot_t = timing[i]
        duration = shot_t["end"] - shot_t["start"]
        if duration <= 0:
            continue

        for j, cue_text in enumerate(cues):
            out_path = os.path.join(project, "sounds", f"cue_{sid:02d}_{j:02d}.mp3")
            if not os.path.isfile(out_path):
                kw = cue_text[:40]
                hits = search_sounds(kw, max_results=3, duration_max=10)
                downloaded = False
                for hit in hits[:1]:
                    downloaded = download_preview(hit["preview_url"], out_path)
                    if downloaded:
                        print(f"  [音效] ✅ shot_{sid:02d}: {hit['name']}")
                        break
                if not downloaded:
                    continue
            else:
                print(f"  [音效] ⏭️ shot_{sid:02d} cue_{j:02d} 已有缓存")

            # 均匀分布在 shot 时长内
            offset = shot_t["start"] + (duration * j / max(n, 1))
            results.append({
                "shot_id": sid,
                "path": out_path,
                "start_time": round(offset, 3),
                "duration": min(duration / n, 5),
            })

    return results
