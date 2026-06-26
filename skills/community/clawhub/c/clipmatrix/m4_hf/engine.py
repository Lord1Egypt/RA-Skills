"""
M4 HF Engine v1.0 — HyperFrames-native template rendering.
Replaces m4_hyperframes.py entirely.

Architecture:
  Python: clip prep + data JSON → inject into HF template
  HF template: JS reads data → builds DOM + GSAP timeline → render

Zero HTML string concatenation in Python.
"""
import os, json, shutil, subprocess, logging
from pathlib import Path

logger = logging.getLogger(__name__)

# ── Paths ──
_PROJECT_ROOT = Path(__file__).resolve().parent.parent  # pandajourneys/
_TEMPLATE_DIR = _PROJECT_ROOT / "m4_hf" / "templates" / "travel_video"
_WORK_DIR = _PROJECT_ROOT / "m4_hf" / "work"

# 中→英场景名映射
CN2EN = {
    "洪崖洞": "Hongya Cave", "长江索道": "Yangtze Cableway",
    "南滨路": "Nanbin Road", "解放碑": "Liberation Monument",
    "山城步道": "Mountain City Trail", "南山一棵树": "Nanshan Viewpoint",
    "九寨沟": "Jiuzhaigou Valley", "黄龙": "Huanglong Pools",
    "都江堰": "Dujiangyan", "青城山": "Qingcheng Mountain",
    "大熊猫基地": "Panda Base", "文殊院": "Wenshu Monastery",
    "太古里": "Taikoo Li", "宽窄巷子": "Kuanzhai Alleys",
    "康定": "Kangding", "塔公草原": "Tagong Grassland",
    "木雅大寺": "Muyadasi", "墨石公园": "Moshi Park",
    "鱼子西": "Yuzixi", "四姑娘山": "Siguniang Mountain",
    "丹巴藏寨": "Danba Village", "折多山": "Zheduo Pass",
    "色达": "Seda", "木格措": "Mugecuo Lake",
    "泸沽湖": "Lugu Lake", "沙溪古镇": "Shaxi Ancient Town",
    "松潘古城": "Songpan Fortress", "大足石刻": "Dazu Rock Carvings",
    "自贡恐龙博物馆": "Zigong Dino Museum", "新都桥": "Xinduqiao",
}

HF_BIN = "/opt/homebrew/bin/hyperframes"
HF_NODE = "/opt/homebrew/Cellar/node@22/22.22.2_2/bin/node"

# ── Style palettes ──
STYLE_PALETTES = {
    "velvet":       {"accent": "#FFD700", "accentDark": "#B8860B"},
    "soft_signal":  {"accent": "#E8775C", "accentDark": "#C4553A"},
    "shadow_cut":   {"accent": "#F59E0B", "accentDark": "#B45309"},
    "swiss_pulse":  {"accent": "#3B82F6", "accentDark": "#1D4ED8"},
    "comparison":   {"accent": "#C53030", "accentDark": "#9B2C2C"},
}


# ═══════════════════════════════════════════════════
#  PUBLIC: build_and_render — identical signature to old M4
# ═══════════════════════════════════════════════════

def build_and_render(scenes, speech_audio, bgm_audio, tts_duration,
                     style="velvet", hook_text="", cta_text="",
                     output_path=None, total_dur=None, quality="high",
                     orientation="portrait", why_us="", direction="city_intro",
                     word_timeline=None, account_id=""):
    """
    Build and render a travel video using HyperFrames native template.
    
    Parameters match the old m4_hyperframes.build_and_render() exactly.
    """
    if total_dur is None:
        total_dur = tts_duration

    # ── Clean slate ──
    if output_path and os.path.exists(output_path):
        os.unlink(output_path)

    # ── Set up work directory ──
    _setup_workdir(style)

    # ── Asset preparation ──
    assets_dir = _WORK_DIR / "assets"
    assets_dir.mkdir(exist_ok=True)

    # Determine output resolution for video trimming
    is_landscape = orientation == "landscape"
    scale_filter = "scale=1920:-2" if is_landscape else "scale=1080:-2"
    
    video_items = _prepare_videos(scenes, assets_dir, scale_filter)
    if not video_items:
        raise RuntimeError("No valid video clips after preparation")

    total_clip_dur = sum(v["duration"] for v in video_items)
    
    # ── Extend last clip to cover full speech if needed ──
    # (prevents black frames when TTS is longer than video clips)
    if tts_duration > total_clip_dur and video_items:
        gap = tts_duration - total_clip_dur
        # Distribute gap across clips proportionally
        total_extra = 0.0
        for i, vi in enumerate(video_items):
            # Last clip gets the bulk, earlier clips get proportional share
            if i == len(video_items) - 1:
                extra = gap - total_extra  # remaining goes to last
            else:
                extra = round(gap * vi["duration"] / total_clip_dur, 2)
            
            if extra > 0:
                src = vi.get("_src_path", "")
                if src and os.path.exists(src):
                    old_dur = vi["duration"]
                    new_dur = old_dur + extra
                    clip_name = f"clip_{i}.mp4"
                    clip_path = assets_dir / clip_name
                    # Re-trim with extended duration
                    src_dur = _get_duration(src)
                    start_sec = scenes[i].get("start_sec", 0) if i < len(scenes) else 0
                    avail = src_dur - start_sec
                    actual_extra = min(extra, max(0, avail - old_dur))
                    if actual_extra > 0.3:
                        new_dur = old_dur + actual_extra
                        _trim_video(src, start_sec, new_dur, clip_path, scale_filter)
                        vi["duration"] = _get_duration(str(clip_path))
                        logger.info(f"  🔧 clip_{i} extended by {actual_extra:.1f}s → {vi['duration']:.1f}s")
                    total_extra += extra
        
        # Recalculate total
        total_clip_dur = sum(v["duration"] for v in video_items)
    
    # 🔧 (2026-05-31) 素材不足时延长最后一段素材并冻结最后一帧
    gap_remaining = tts_duration - total_clip_dur
    if gap_remaining > 0.5 and video_items:
        last_clip = video_items[-1]
        last_path = assets_dir / f"clip_{len(video_items)-1}.mp4"
        if os.path.exists(last_path):
            old_dur = last_clip["duration"]
            new_dur = old_dur + gap_remaining
            # 用tpad冻结最后一帧来填充时长
            _trim_video_frozen(last_path, new_dur)
            last_clip["duration"] = _get_duration(str(last_path))
            logger.info(f"  🧊 clip_{len(video_items)-1} frozen-extended by {gap_remaining:.1f}s → {last_clip['duration']:.1f}s")
    
    # 🔧 (2026-05-31) 重新计算所有clip的start时间，确保无空隙无重叠
    cumulative_t = 0.0
    for vi in video_items:
        vi["start"] = round(cumulative_t, 2)
        cumulative_t += vi["duration"]
    total_clip_dur = round(cumulative_t, 2)
    
    composition_dur = max(total_clip_dur, tts_duration)

    # Copy audio
    speech_local = _copy_audio(speech_audio, assets_dir, "speech.wav")
    bgm_local = _copy_audio(bgm_audio, assets_dir, "bgm.mp3")

    # ── Build data JSON ──
    hf_data = {
        "duration": composition_dur,
        "width": 1920 if orientation == "landscape" else 1080,
        "height": 1080 if orientation == "landscape" else 1920,
        "style": STYLE_PALETTES.get(style, STYLE_PALETTES["velvet"]),
        "scenes": video_items,
        "words": _build_word_data(word_timeline, video_items),
        "cta": {
            "text": cta_text or "📥 DM us for free itinerary",
            "start": max(0, total_clip_dur - 4),
        },
        "brand": {
            "emoji": "🐼",
            "domain": "Panda-Journeys.com",
            "follow": "+ Follow 🌏",
        },
        "audio": {
            "speech": speech_local,
            "bgm": bgm_local,
            "speech_dur": tts_duration,
        },
    }

    # ── Inject data + audio into template ──
    _inject_data(hf_data)

    # ── Render ──
    return _render(output_path or str(_PROJECT_ROOT / "output" / "m4_output.mp4"),
                   orientation, quality)


# ═══════════════════════════════════════════════════
#  INTERNAL
# ═══════════════════════════════════════════════════

def _setup_workdir(style="velvet"):
    """Copy clean template to work dir."""
    if _WORK_DIR.exists():
        shutil.rmtree(_WORK_DIR)
    # Select template by style (fallback to travel_video/velvet)
    STYLE_DIRS = {
        "velvet": "travel_video",
        "soft_signal": "soft_signal",
        "shadow_cut": "shadow_cut",
        "swiss_pulse": "swiss_pulse",
        "comparison": "comparison",
    }
    template_dir = _PROJECT_ROOT / "m4_hf" / "templates" / STYLE_DIRS.get(style, "travel_video")
    shutil.copytree(template_dir, _WORK_DIR,
                    ignore=shutil.ignore_patterns('node_modules', '.git'))
    logger.info(f"  📁 Work dir [{style}]: {_WORK_DIR}")


def _prepare_videos(scenes, assets_dir, scale_filter="scale=1080:-2"):
    """Trim and copy video clips. Returns list of scene dicts."""
    video_items = []
    cumulative_t = 0.0

    for i, s in enumerate(scenes):
        src = s.get("path", "")
        if not src or not os.path.exists(src):
            logger.warning(f"  ⚠️ Scene {i} has no video path, skipping")
            continue

        src_dur = _get_duration(src)
        start_sec = s.get("start_sec", 0)
        end_sec = s.get("end_sec", min(start_sec + 10, src_dur))
        seg_dur = end_sec - start_sec  # 原始M2分镜时长

        # Guard: if start too close to end of source
        if start_sec + 1.5 > src_dur:
            start_sec = 0
            logger.info(f"  ⚠️ scene{i} start too late, using full clip")

        # clip时长 = 原始分镜+1s缓冲, 但不超过素材可用长度
        clip_dur = min(seg_dur + 1.0, src_dur - start_sec)

        clip_name = f"clip_{i}.mp4"
        clip_path = assets_dir / clip_name

        _trim_video(src, start_sec, clip_dur, clip_path, scale_filter)

        if clip_path.exists() and clip_path.stat().st_size > 1000:
            actual_dur = _get_duration(str(clip_path))
            scene_name = s.get("scene", f"Scene {i}")
            scene_name_en = CN2EN.get(scene_name, scene_name)
            vp = s.get("visual_plan", {}) or {}

            video_items.append({
                "name": scene_name_en,
                "video": f"assets/{clip_name}",
                "_src_path": str(src),
                "headline": vp.get("headline", "") or scene_name_en,
                "subtitle": vp.get("subtitle", ""),
                "tags": (vp.get("selling_points", []) or [])[:3],
                "effects": s.get("effects", []),
                "start": cumulative_t,
                "duration": actual_dur,
            })
            cumulative_t += actual_dur
            logger.info(f"  🎬 clip_{i}: {scene_name} {actual_dur:.1f}s")
        else:
            logger.warning(f"  ❌ clip_{i} trim failed or too small")

    return video_items


def _get_duration(path):
    """Get media duration via ffprobe."""
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, timeout=10,
        )
        return float(r.stdout.strip())
    except Exception:
        return 10.0


def _trim_video(src, start_sec, duration, output_path, scale_filter="scale=1080:-2"):
    """Trim video clip with ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_sec), "-i", str(src),
        "-t", str(duration),
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        "-vf", scale_filter + ",setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709",
        "-g", "30", "-keyint_min", "30",
        "-preset", "fast", "-an",
        str(output_path),
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        logger.warning(f"  ⏱️ ffmpeg timeout for {src}")
    except Exception as e:
        logger.warning(f"  ❌ ffmpeg error: {e}")


def _trim_video_frozen(existing_clip_path, target_duration):
    """延长已有素材：冻结最后一帧填充时长 (2026-05-31)"""
    # ffmpeg tpad: 在视频末尾冻结最后一帧
    cmd = [
        "ffmpeg", "-y",
        "-i", str(existing_clip_path),
        "-vf", f"tpad=stop_mode=clone:stop_duration={target_duration - _get_duration(existing_clip_path):.1f}",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        "-preset", "ultrafast", "-an",
        str(existing_clip_path) + ".tmp.mp4"
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=120)
        tmp = str(existing_clip_path) + ".tmp.mp4"
        if os.path.exists(tmp):
            os.replace(tmp, str(existing_clip_path))
    except Exception as e:
        logger.warning(f"  ⚠️ freeze-frame extend failed: {e}")


def _copy_audio(path, assets_dir, name):
    """Copy audio file to work dir. Returns relative path or ''."""
    if not path or not os.path.exists(path):
        return ""
    dest = assets_dir / name
    shutil.copy2(path, dest)
    return f"assets/{name}"


def _build_word_data(word_timeline, video_items):
    """Convert word_timeline to scenes-anchored word data."""
    if not word_timeline or not video_items:
        return []

    words = []
    for w in word_timeline:
        t = w.get("start", 0)
        # Find scene
        si = 0
        for vi, v in enumerate(video_items):
            if t >= v["start"] and t < v["start"] + v["duration"]:
                si = vi
                break
        words.append({
            "text": w.get("word", w.get("text", "")),
            "start": t,
            "end": w.get("end", t + 0.35),
            "scene": si,
        })
    logger.info(f"  📝 Words: {len(words)} across {len(video_items)} scenes")
    return words


def _inject_data(hf_data):
    """Inject data JSON + video + audio elements into template index.html."""
    index_path = _WORK_DIR / "index.html"
    html = index_path.read_text()

    # Replace hardcoded dimension placeholders with actual values
    w = hf_data.get("width", 1080)
    h = hf_data.get("height", 1920)
    html = html.replace('data-width="1080"', f'data-width="{w}"')
    html = html.replace('data-height="1920"', f'data-height="{h}"')
    # Also update the viewport meta and body size
    html = html.replace('width=1080, height=1920', f'width={w}, height={h}')
    html = html.replace('width: 1080px; height: 1920px', f'width: {w}px; height: {h}px')

    # Inject data block before </body>
    data_json = json.dumps(hf_data, indent=2, ensure_ascii=False)
    html = html.replace(
        "</body>",
        f'  <script id="hf-data" type="application/json">\n{data_json}\n  </script>\n</body>',
    )

    # Inject video elements INSIDE root div (after vignette, before cards)
    video_html = ""
    for i, s in enumerate(hf_data["scenes"]):
        video_html += (
            f'\n    <video class="clip scene-video" id="v{i}" '
            f'data-start="{s["start"]}" data-duration="{s["duration"]}" '
            f'data-track-index="{i}" '
            f'muted playsinline preload="auto" '
            f'src="{s["video"]}"></video>'
        )

    # Insert videos after vignette div (first visible child of root)
    html = html.replace(
        '<div id="vignette"></div>',
        f'<div id="vignette"></div>{video_html}',
    )

    # Inject audio elements before close of root div
    audio_html = ""
    if hf_data["audio"]["speech"]:
        audio_html += (
            f'\n    <audio id="speech" src="{hf_data["audio"]["speech"]}" '
            f'data-start="0" data-duration="{hf_data["audio"]["speech_dur"]:.1f}" '
            f'data-volume="1.0" data-track-index="90"></audio>'
        )
    if hf_data["audio"]["bgm"]:
        audio_html += (
            f'\n    <audio id="bgm" src="{hf_data["audio"]["bgm"]}" '
            f'data-start="0" data-duration="{hf_data["duration"]:.1f}" '
            f'data-volume="0.12" data-track-index="91"></audio>'
        )
    if audio_html:
        html = html.replace(
            '</div>\n\n<script>',
            f'{audio_html}\n  </div>\n\n<script>',
        )

    index_path.write_text(html)
    logger.info(f"  ✏️ Template injected: {len(data_json)} bytes data")


def _render(output_path, orientation, quality):
    """Call hyperframes render CLI."""
    resolution = "landscape" if orientation == "landscape" else "portrait"
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    for attempt in range(3):
        try:
            r = subprocess.run(
                [HF_NODE, HF_BIN, "render", "-o", output_path,
                 "--resolution", resolution, "--quality", quality,
                 "--fps", "30", str(_WORK_DIR)],
                capture_output=True, text=True, timeout=600,
            )
            # Log last few lines
            lines = (r.stdout or "").strip().split("\n")
            for line in lines[-5:]:
                if line.strip():
                    logger.info(f"  🎬 {line.strip()}")

            if r.returncode != 0 and r.stderr:
                logger.warning(f"  HF stderr: {r.stderr[-300:]}")

            if os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
                logger.info(f"  ✅ Rendered: {os.path.getsize(output_path)} bytes → {output_path}")
                return True
            else:
                sz = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                logger.warning(f"  ⚠️ Attempt {attempt+1}: output {sz} bytes")
        except subprocess.TimeoutExpired:
            logger.warning(f"  ⏱️ Timeout attempt {attempt+1}")
        except Exception as e:
            logger.error(f"  ❌ Error attempt {attempt+1}: {e}")

    return False
