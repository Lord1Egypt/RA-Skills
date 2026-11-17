"""
升级拼接模块 — 支持 xfade 转场（叠化/黑场/溶解等）
降级到简单 concat（如果所有转场都是硬切）

作为拼接 Provider 使用，通过 stitch.py 入口自动注册。
"""
from __future__ import annotations
import json, os, shutil, subprocess
from typing import Any, Optional

from modules.config import _script_path, _videos_dir, _output_dir
from stitch_base import BaseStitcher, StitcherRegistry


class FfmpegStitcher(BaseStitcher):
    name = "ffmpeg"

    @staticmethod
    def check_available() -> bool:
        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg:
            return True
        try:
            from imageio_ffmpeg import get_ffmpeg_exe
            get_ffmpeg_exe()
            return True
        except Exception:
            return False

    @staticmethod
    def run(project: str, shot_count: int = 0,
            script_config: Optional[dict] = None) -> Optional[str]:
        return _run_stitch(project, shot_count)

    @staticmethod
    def _embed_to_doc(docx_token: str, video_path: str) -> str:
        return _embed_to_doc(docx_token, video_path)


StitcherRegistry.register(FfmpegStitcher)
StitcherRegistry.register(FfmpegStitcher)

# 转场 xfade 路径已移除（Windows xfade 兼容性问题），留此占位供后续优化参考。
# 被移函数和常量：TRANSITION_MAP / DEF_TRANS / DEF_DUR / _get_transitions /
#   _has_any_transition / _build_xfade_filter / run_with_transitions /
#   _get_durations / _seg_duration

def _probe_actual_durations(project: str, shot_count: int) -> list[float]:
    """用 ffprobe 获取各视频的实际时长，替代 script.json 的计划时长。"""
    import json as _json, subprocess as _sp
    vdir = _videos_dir(project)
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        try:
            from imageio_ffmpeg import get_ffmpeg_exe as _gf
            ffprobe = _gf().replace("ffmpeg.exe", "ffprobe.exe").replace("ffmpeg", "ffprobe")
        except Exception:
            pass
    durs = []
    for i in range(1, shot_count + 1):
        vp = os.path.join(vdir, f"shot_{i:02d}.mp4")
        if not os.path.isfile(vp):
            durs.append(5.0)
            continue
        try:
            r = _sp.run(
                [ffprobe, "-v", "quiet", "-print_format", "json",
                 "-show_entries", "format=duration", vp],
                capture_output=True, text=True, timeout=10,
            )
            info = _json.loads(r.stdout)
            dur = float(info["format"]["duration"])
            durs.append(max(dur, 0.5))
        except Exception:
            durs.append(5.0)
    return durs


def _build_audio_filter(project: str, shot_count: int):
    """准备所有音频素材并构建 filter graph，返回 (inputs, filter_str, srt_path, temp_dir)"""
    import speech as sp
    import audio as au
    import tempfile

    voices = sp.generate_all_voiceovers(project, shot_count)
    # 用实际视频时长重新计算时间轴（与 HF 组合/ffmpeg concat 对齐）
    actual_durs = _probe_actual_durations(project, shot_count)
    srt_path = sp.generate_srt(project, shot_count, voices, actual_durs)
    ambients = au.generate_all_ambients(project, shot_count)
    total_dur = sum(actual_durs[:shot_count])
    bgm = au.generate_bgm(project, total_dur)
    shot_cues = au.generate_shot_cues(project, shot_count)

    lines = []
    audio_labels = ["0:a"]  # 包含原始视频音频
    extra_inputs = []
    input_idx = 1

    for v in voices:
        if v.get("source") == "subtitle_only":
            # dialogue 字幕 only：不生成 TTS 音频，视频已自带人物声音
            continue
        extra_inputs.append(v["wav_path"])
        delay_ms = int(v["start_time"] * 1000)
        lbl = f"v{input_idx - 1}"
        lines.append(f"[{input_idx}:a]adelay={delay_ms}:all=1[{lbl}]")
        audio_labels.append(lbl)
        input_idx += 1

    for a in ambients:
        extra_inputs.append(a["path"])
        delay_ms = int(a["start_time"] * 1000)
        lbl = f"a{input_idx - 1 - len(voices)}"
        lines.append(f"[{input_idx}:a]adelay={delay_ms}:all=1[{lbl}]")
        audio_labels.append(lbl)
        input_idx += 1

    if bgm:
        extra_inputs.append(bgm)
        lines.append(f"[{input_idx}:a]volume=0.3[bgm]")
        audio_labels.append("bgm")
        input_idx += 1

    for c in shot_cues:
        extra_inputs.append(c["path"])
        delay_ms = int(c["start_time"] * 1000)
        lbl = f"c{input_idx - 1 - len(voices) - len(ambients) - (1 if bgm else 0)}"
        lines.append(f"[{input_idx}:a]adelay={delay_ms}:all=1[{lbl}]")
        audio_labels.append(lbl)
        input_idx += 1

    n_audio = len(audio_labels)
    amix_in = "".join(f"[{l}]" for l in audio_labels)
    lines.append(f"{amix_in}amix=inputs={n_audio}:dropout_transition=2,volume=2.0[aout]")

    # 写入临时 filter 文件
    filters_dir = tempfile.mkdtemp(prefix="vc_")
    filter_file = os.path.join(filters_dir, "f.txt")
    with open(filter_file, "w", encoding="utf-8") as ff:
        ff.write(";\n".join(lines))

    return extra_inputs, filter_file, srt_path, filters_dir


def _run_ffmpeg(ffmpeg: str, input_path: str, out_path: str,
                extra_inputs: list, filter_file: str, srt_path: str) -> bool:
    """执行 ffmpeg 音频混合 + 字幕叠加"""
    inputs = ["-i", input_path]
    for e in extra_inputs:
        inputs.extend(["-i", e])

    cmd = [
        ffmpeg, "-y", *inputs,
        "-filter_complex_script", filter_file,
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k",
    ]
    if srt_path:
        # subtitles 滤镜复制干净路径 + filter_complex 方式
        import uuid, shutil
        _tmpdir = os.path.join(os.environ.get("TEMP", os.path.expanduser("~")),
                               f"cb_{uuid.uuid4().hex[:8]}")
        os.makedirs(_tmpdir, exist_ok=True)
        _srttmp = os.path.join(_tmpdir, "subs.srt")
        shutil.copy2(srt_path, _srttmp)
        # 方法：直接在 filter_complex_script 中追加 subtitles 滤镜
        _srt_esc = _srttmp.replace("\\", "\\\\").replace(":", "\\:")
        with open(filter_file, "a", encoding="utf-8") as ff:
            ff.write(f";[0:v]subtitles='{_srt_esc}':force_style='FontName=Microsoft YaHei,FontSize=14,PrimaryColour=&H00FFFFFF,Outline=1,Shadow=1'[vsub]")
        # 替换 video map 为 vsub
        v_idx = None
        for idx, a in enumerate(cmd):
            if a == "0:v" and idx > 0 and cmd[idx-1] == "-map":
                v_idx = idx
                break
        if v_idx is not None:
            cmd[v_idx] = "[vsub]"
    # 确保输出采样率 48kHz 立体声
    cmd.extend(["-ar", "48000", "-ac", "2"])
    cmd.append(out_path)

    print("  [音频+字幕] 叠加旁白和字幕...")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    if r.returncode != 0:
        print(f"  ⚠️ ffmpeg 返回 {r.returncode}")
        if r.stderr:
            # 跳过 build config 行
            err_lines = [l for l in r.stderr.split(chr(10)) if '--enable-' not in l and 'built with' not in l and 'configuration' not in l and 'ffmpeg version' not in l]
            print(f"  stderr: {chr(10).join(err_lines)[:500]}")
    return r.returncode == 0


def _apply_audio_and_subs(project: str, input_path: str, ffmpeg: str, shot_count: int = 6) -> Optional[str]:
    """第二遍：准备音频素材 → ffmpeg 合成 → 输出最终版"""
    extra_inputs, filter_file, srt_path, filters_dir = _build_audio_filter(
        project, shot_count)

    if not extra_inputs and not srt_path:
        return input_path

    odir = _output_dir(project)
    out_path = os.path.join(odir, "final.mp4")
    ok = _run_ffmpeg(ffmpeg, input_path, out_path, extra_inputs, filter_file, srt_path)

    try:
        os.unlink(filter_file); os.rmdir(filters_dir)
    except Exception:
        pass

    if not ok:
        print(f"  ⚠️ 合成失败, 返回未处理版本")
        return input_path

    mb = os.path.getsize(out_path) // (1024 * 1024)
    print(f"  ✅ 最终成片: {out_path} ({mb}MB)")
    return out_path


def _run_stitch(project: str, shot_count: int) -> Optional[str]:
    """
    拼接所有视频 → 叠加旁白和字幕。
    自动检测 xiaoyunqiao_segments，切换到 segment 级拼接。
    """
    import shutil
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        try:
            from imageio_ffmpeg import get_ffmpeg_exe
            ffmpeg = get_ffmpeg_exe()
        except Exception:
            pass
    if not ffmpeg:
        print("  [ERROR] ffmpeg 未找到，请安装 ffmpeg 或检查环境变量 PATH")
        return None

    odir = _output_dir(project)
    os.makedirs(odir, exist_ok=True)
    vdir = _videos_dir(project)

    # 检测 segment 模式
    sp = _script_path(project)
    segments = []
    if os.path.isfile(sp):
        with open(sp, encoding="utf-8") as f:
            script = json.load(f)
        segments = script.get("xiaoyunqiao_segments", [])

    use_segments = bool(segments)
    if use_segments:
        clip_count = len(segments)
        prefix = "seg"
    else:
        clip_count = shot_count
        prefix = "shot"

    # 收集可用视频
    clips = []
    for i in range(1, clip_count + 1):
        vp = os.path.join(vdir, f"{prefix}_{i:02d}.mp4")
        if os.path.isfile(vp):
            clips.append(vp)
        else:
            print(f"  ⚠️ 缺少 {prefix}_{i:02d}.mp4")
    if not clips:
        print("  ❌ 无可用视频"); return None
    actual_count = len(clips)

    # 第一遍：拼接（xfade 或 concat）
    temp_path = os.path.join(odir, "_temp.mp4")
    # ⚠️ xfade 在 Windows 上有音视频漂移问题，暂时禁用，全用简单 concat。
    # 转场相关的 _get_durations/_get_transitions/durations/trans_types 计算已移除——
    # 它们只为被禁用的 xfade 路径服务，run_simple_concat 只消费 clips 列表。
    print("  [ffmpeg] 简单 concat...")
    ok = run_simple_concat(project, actual_count, temp_path, ffmpeg, clips)

    if not ok or not os.path.isfile(temp_path):
        return None

    mb = os.path.getsize(temp_path) // (1024 * 1024)
    print(f"  ✅ 拼接完成 ({mb}MB)")

    # 第二遍：叠加 voice_over 音频 + 字幕
    final_path = _apply_audio_and_subs(project, temp_path, ffmpeg, actual_count)

    # 清理临时文件
    if final_path != temp_path and os.path.isfile(temp_path):
        try:
            os.unlink(temp_path)
        except Exception as _e:
            # 托管 Python 的 safe-delete 钩子在沙箱无回收站时会抛异常；
            # 临时文件删不掉不影响成片，仅警告，不向上传播致命错误。
            print(f"  [warn] 清理临时文件失败(可忽略): {_e}")

    if os.path.isfile(final_path):
        mb2 = os.path.getsize(final_path) // (1024 * 1024)
        print(f"  ✅ 最终成片: {final_path} ({mb2}MB)")
    return final_path


# ── 文档嵌入（不变） ───────────────────────────────────────

def _embed_to_doc(docx_token: str, video_path: str) -> str:
    """上传视频到飞书文档（可选功能，无飞书环境时返回空字符串）。
    
    使用 lark-cli docs +media-insert 嵌入视频到文档。
    --file 必须为相对路径（相对于项目目录），否则 lark-cli 拒绝。
    """
    try:
        from feishu import LARK_EXE
    except ImportError:
        print("  [文档] ⚠️ feishu 模块不可用，跳过文档嵌入")
        return ""
    print("  [文档] 嵌入成片...")
    
    # 计算相对于项目目录的相对路径
    abs_path = os.path.abspath(video_path)
    project_dir = os.path.dirname(abs_path) if os.path.isfile(abs_path) else os.getcwd()
    # 从 project 根找相对路径：output/final.mp4
    parent = os.path.dirname(abs_path)  # .../output/
    grandparent = os.path.dirname(parent)  # project root
    if grandparent and os.path.isdir(grandparent):
        rel = os.path.relpath(abs_path, grandparent)
    else:
        rel = os.path.basename(abs_path)
    
    r = subprocess.run(
        [LARK_EXE, "docs", "+media-insert", "--doc", docx_token,
         "--file", rel, "--type", "file", "--as", "user"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=300, cwd=grandparent if os.path.isdir(grandparent) else None,
    )
    if r.returncode == 0:
        try:
            jdata = json.loads(r.stdout)
            ft = jdata.get("data", {}).get("file_token", "")
            if ft:
                print(f"  ✅ 嵌入成功 (file_token: {ft})")
                return f"https://drive/{ft}"
        except Exception:
            pass
    print(f"  ⚠️ 嵌入失败: {(r.stderr or r.stdout)[:200]}")
    # 返回本地路径作为 fallback（后续可手动上传）
    return f"file://{abs_path}"
