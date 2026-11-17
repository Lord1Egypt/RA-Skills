"""
语音与字幕模块 — TTS 合成 + SRT 字幕生成
"""
from __future__ import annotations
import json, logging, os, re, subprocess, sys, wave
from typing import Optional

from modules.config import _script_path, _sounds_dir


def _sounds(project: str) -> str:
    p = _sounds_dir(project)
    os.makedirs(p, exist_ok=True)
    return p


def load_script(project: str) -> dict:
    with open(_script_path(project), encoding="utf-8") as f:
        return json.load(f)


def shot_durations(project: str, shot_count: int) -> list[dict[str, float]]:
    """返回每个镜头时长列表（简单 concat 模式，无 xfade 重叠）"""
    s = load_script(project)
    shot_map = {sh["id"]: float(sh.get("duration_seconds", 5)) for sh in s.get("shots", [])}
    raws = [shot_map.get(i, 5) for i in range(1, shot_count + 1)]

    # 简单 concat：镜头依次排列，无 xfade 重叠
    starts = [0.0]
    for i in range(shot_count - 1):
        starts.append(round(starts[-1] + raws[i], 3))
    ends = [round(starts[i] + raws[i], 3) for i in range(shot_count)]
    return [{"start": starts[i], "end": ends[i], "raw": raws[i]} for i in range(shot_count)]


def _char_per_sec(text: str) -> float:
    """中文字幕阅读速度：约 4 字/秒"""
    cn = len(re.findall(r'[\u4e00-\u9fff]', text))
    en = len(re.findall(r'[a-zA-Z]', text))
    return max(cn / 4 + en / 8, 1.0)


def _wav_duration(wav_path: str) -> float:
    """读取 WAV 文件实际时长（秒）。失败时返回估算值。"""
    try:
        with wave.open(wav_path, 'rb') as w:
            frames = w.getnframes()
            rate = w.getframerate()
            return frames / rate
    except Exception:
        return 0.0


def _subtitle_format(text: str) -> str:
    """字幕格式化：标点替换为空格作为视觉分隔。"""
    t = re.sub(r'[。！？]', '\u3000\u3000', text)
    t = re.sub(r'[，、：；]', '\u3000', t)
    t = re.sub(r'[u201c\u201d\u2018\u2019\u2014\u2013\u2026\u00b7\uff08\uff09\u300a\u300b\u3008\u3009\\\'\"]', '', t)
    return t.strip()


# ── TTS ──────────────────────────────────────────────────

def check_tts() -> bool:
    """检查 edge-tts 是否可用（惰性导入，只检查一次）"""
    if not hasattr(check_tts, "_result"):
        try:
            import edge_tts as _
            check_tts._result = True
        except ImportError:
            print("  [WARN] edge-tts 未安装，TTS 功能不可用。请运行: pip install edge-tts")
            check_tts._result = False
    return check_tts._result


def generate_tts(text: str, output_path: str, voice: str = "zh-CN-XiaoxiaoNeural") -> bool:
    """
    用 edge-tts 生成中文语音 WAV。
    voice: zh-CN-XiaoxiaoNeural（女声）/ zh-CN-YunxiNeural（男声）
    """
    if not check_tts():
        return False
    import asyncio
    import edge_tts
    try:
        asyncio.run(edge_tts.Communicate(text, voice).save(output_path))
        return os.path.isfile(output_path)
    except Exception:
        return False


def generate_all_voiceovers(project: str, shot_count: int) -> list[dict]:
    """
    收集所有旁白/对话的语音和字幕数据。

    voice_over → 生成 TTS WAV + 字幕（视频无自带人声）
    dialogue   → 只产字幕（Agnes 视频已自带人物对话声音）
    返回：[{shot_id, wav_path|None, start_time, end_time, text, source}, ...]
    """
    if not check_tts():
        print("  [TTS] edge-tts 未安装，跳过语音生成")
        print("  ↳ pip install edge-tts")

    s = load_script(project)
    shot_map = {sh["id"]: sh for sh in s.get("shots", [])}
    timing = shot_durations(project, shot_count)
    sounds_dir = _sounds(project)
    results = []

    for i in range(shot_count):
        sid = i + 1
        shot = shot_map.get(sid, {})
        vo = shot.get("voice_over", "").strip()
        dialogue = shot.get("dialogue", "").strip()

        # 决策规则：
        #   voice_over → 旁白/解说，视频不包含这些人声 → 需要 TTS WAV + SRT 字幕
        #   dialogue   → 角色对白，Agnes 生成的视频已自带人物声音 → 仅 SRT 字幕，不产 TTS
        #   description 中的"台词:xxx" → 降级为字幕 only（语义模糊时走 safest 路径）
        if vo:
            # voice_over: 需要 TTS 音频 + 字幕
            wav_path = os.path.join(sounds_dir, f"voice_{sid:02d}.wav")
            if os.path.isfile(wav_path):
                print(f"  [TTS] ⏭️ shot_{sid:02d} 已有语音")
            else:
                if check_tts():
                    print(f"  [TTS] shot_{sid:02d} 生成中 ({len(vo)}字)...")
                    ok = generate_tts(vo, wav_path)
                    if not ok:
                        print(f"  [TTS] ❌ shot_{sid:02d} 失败")
                        continue
                    print(f"  [TTS] ✅ shot_{sid:02d}")
                else:
                    # TTS 不可用，降级为字幕 only
                    print(f"  [TTS] ⏭️ shot_{sid:02d} TTS 不可用，仅生成字幕")
                    results.append({
                        "shot_id": sid, "wav_path": None,
                        "start_time": timing[i]["start"],
                        "end_time": timing[i]["end"],
                        "text": vo, "source": "subtitle_only",
                    })
                    continue

            results.append({
                "shot_id": sid, "wav_path": wav_path,
                "start_time": timing[i]["start"],
                "end_time": timing[i]["end"],
                "text": vo,
                "actual_duration": _wav_duration(wav_path),
                "source": "tts",
            })

        elif dialogue:
            # dialogue: 只产字幕，不生成 TTS（视频已自带对话声）
            print(f"  [字幕] 📝 shot_{sid:02d} dialogue（仅字幕）")
            results.append({
                "shot_id": sid, "wav_path": None,
                "start_time": timing[i]["start"],
                "end_time": timing[i]["end"],
                "text": dialogue, "source": "subtitle_only",
            })

        else:
            # 兼容 description 中的 台词:xxx
            desc = shot.get("description", "")
            if "台词:" in desc:
                after = desc.split("台词:")[-1]
                desc_text = after.split("。")[0].strip()
                for sep in ["，", "。", "！", "？", "……"]:
                    if sep in desc_text and len(desc_text.split(sep)[0]) >= 2:
                        desc_text = desc_text.split(sep)[0]
                        break
                if desc_text:
                    print(f"  [字幕] 📝 shot_{sid:02d} 描述台词（仅字幕）")
                    results.append({
                        "shot_id": sid, "wav_path": None,
                        "start_time": timing[i]["start"],
                        "end_time": timing[i]["end"],
                        "text": desc_text, "source": "subtitle_only",
                    })
    return results


# ── 字幕 ─────────────────────────────────────────────────

def generate_srt(project: str, shot_count: int, voices: list[dict],
                 actual_durations: Optional[list[float]] = None) -> Optional[str]:
    """
    从 voice_over / dialogue 生成 SRT 字幕文件。
    长文本按时间均匀切分为多段（复刻'按时间均匀显示'风格），避免一整段堆满屏幕。

    参数:
        actual_durations: 可选，各镜头实际视频时长（ffprobe）。
            传入时，SRT 时间轴使用实际时长（与 HF 组合/ffmpeg concat 对齐），
            否则使用 script.json 的计划时长。
    返回 SRT 文件路径。
    """
    if not voices:
        return None

    s = load_script(project)
    if actual_durations:
        # 用实际视频时长计算时间轴（与 HF 组合/ffmpeg concat 对齐）
        timing = []
        cum = 0.0
        for i, raw in enumerate(actual_durations[:shot_count]):
            timing.append({"start": round(cum, 3), "end": round(cum + raw, 3), "raw": raw})
            cum += raw
    else:
        timing = shot_durations(project, shot_count)

    srt_path = os.path.join(_sounds(project), "subtitles.srt")
    entries = []
    idx = 1

    def _to_srt(sec: float) -> str:
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        ss = sec % 60
        return f"{h:02d}:{m:02d}:{ss:06.3f}".replace(".", ",")

    for v in voices:
        sid = v["shot_id"]
        text = v["text"]
        t = timing[sid - 1]
        avail = round(t["end"] - t["start"], 3)

        # 字幕窗口：优先用实际 TTS 朗读时长（更贴合人声节奏）
        actual_dur = v.get("actual_duration", 0.0)
        window = actual_dur if (actual_dur > 0.0 and actual_dur <= avail) else avail

        # ⭐ 格式化后按时间均匀切分为多段
        fmt = _subtitle_format(text)
        segs = _split_long_subtitle(fmt, t["start"], window)
        for (seg_text, seg_start, seg_end) in segs:
            entries.append(f"{idx}\n{_to_srt(seg_start)} --> {_to_srt(seg_end)}\n{seg_text}\n")
            idx += 1

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(entries))

    print(f"  [字幕] ✅ 生成 {len(entries)} 条: {srt_path}")
    return srt_path


def _split_long_subtitle(text: str, base_start: float, total_dur: float,
                         max_chars: int = 15, min_seg_dur: float = 1.0) -> list[tuple[str, float, float]]:
    """长字幕按词边界（空格分隔）切分为多段，确保每个完整词不被截断。
    
    输入文本以空格分隔词语（如"少年 抬头 望向天空"），
    每段在词边界处切分，避免劈开一个完整词/短语。
    - max_chars：单段最大字数（默认15字约一行），超过则在词边界切分
    - min_seg_dur：每段最短显示时间，内容太短时合并到最后一段
    - 时间轴均匀：每段占 total_dur / n
    """
    text = (text or "").strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [(text, base_start, round(base_start + total_dur, 3))]

    # 按空格分词
    words = text.split()
    if len(words) <= 1:
        return [(text, base_start, round(base_start + total_dur, 3))]

    # 按词边界合并成段，确保不劈开一个词
    seg_texts = []
    cur = []
    cur_len = 0
    for w in words:
        # +1 代表空格
        new_len = cur_len + len(w) + (1 if cur else 0)
        if new_len > max_chars and cur:
            seg_texts.append(" ".join(cur))
            cur = [w]
            cur_len = len(w)
        else:
            cur.append(w)
            cur_len += len(w) + (0 if cur_len == 0 else 1)
    if cur:
        seg_texts.append(" ".join(cur))

    # 合并太短的段（内容少且显示时间不足 min_seg_dur）
    n = len(seg_texts)
    while n > 1 and (total_dur / n) < min_seg_dur:
        seg_texts[-2] = seg_texts[-2] + " " + seg_texts[-1]
        seg_texts.pop()
        n -= 1

    # 均匀分配时间
    seg_dur = total_dur / n
    segs = []
    for i, chunk in enumerate(seg_texts):
        seg_start = base_start + i * seg_dur
        seg_end = base_start + total_dur if i == n - 1 else base_start + (i + 1) * seg_dur
        segs.append((chunk, round(seg_start, 3), round(seg_end, 3)))
    return segs
