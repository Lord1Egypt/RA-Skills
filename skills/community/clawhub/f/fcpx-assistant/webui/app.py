#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FCPX Assistant WebUI - 一键视频生产界面
Made by Steve & Steven (≧∇≦)
"""

import gradio as gr
import subprocess
import os
import json
from pathlib import Path
from datetime import datetime

# 配置
FCPX_ASSISTANT_DIR = Path(os.path.expanduser("~/.openclaw/workspace/skills/fcpx-assistant"))
SCRIPTS_DIR = FCPX_ASSISTANT_DIR / "scripts"
OUTPUT_DIR = Path(os.path.expanduser("~/Movies/fcpx-assistant-outputs"))

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────
# 通用工具函数
# ─────────────────────────────────────────

def run_command(cmd, cwd=None, timeout=3600):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd,
            capture_output=True, timeout=timeout
        )
        # 用 errors='replace' 处理非 UTF-8 字节（如 ffmpeg 的 ANSI 颜色码）
        stdout = result.stdout.decode('utf-8', errors='replace')
        stderr = result.stderr.decode('utf-8', errors='replace')
        return result.returncode == 0, stdout + stderr
    except subprocess.TimeoutExpired:
        return False, "⏰ 任务超时"
    except Exception as e:
        return False, f"❌ 执行错误：{str(e)}"


def run_osascript(script_name, *args):
    """运行 AppleScript"""
    script_path = SCRIPTS_DIR / script_name
    cmd = f'osascript "{script_path}"'
    for arg in args:
        cmd += f' "{arg}"'
    return run_command(cmd, timeout=30)


def create_project_structure(project_name, output_dir):
    """创建项目目录结构"""
    project_path = Path(output_dir) / project_name
    for sub in ["videos", "music", "voiceover", "meta"]:
        (project_path / sub).mkdir(parents=True, exist_ok=True)
    return str(project_path)


def ensure_output_path(filename):
    """确保输出路径存在"""
    path = OUTPUT_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


# ─────────────────────────────────────────
# Tab 1: 一键成片
# ─────────────────────────────────────────

def generate_script(topic, style, duration, output_path=None):
    """生成 AI 文案"""
    cmd = f'bash "{SCRIPTS_DIR}/ai-script-generator.sh" --topic "{topic}" --style "{style}" --duration {duration} --keywords'
    if output_path:
        cmd += f' --output "{output_path}"'
    success, output = run_command(cmd)
    return success, f"✅ 文案生成成功！\n\n{output}" if success else f"❌ 文案生成失败：{output}"


def translate_keywords_to_english(keywords):
    """检测中文关键词并翻译为英文（Pexels/Pixabay 只支持英文搜索）"""
    import re
    if not re.search(r'[\u4e00-\u9fff]', keywords):
        return keywords  # 已经是英文
    # 简单中英映射 + 通用翻译
    common_map = {
        "咖啡": "coffee", "制作": "making", "教程": "tutorial", "烹饪": "cooking",
        "美食": "food", "旅行": "travel", "自然": "nature", "城市": "city",
        "科技": "technology", "音乐": "music", "运动": "sports", "游戏": "gaming",
        "动物": "animal", "风景": "landscape", "海洋": "ocean", "山": "mountain",
        "日落": "sunset", "日出": "sunrise", "夜景": "night city", "花": "flower",
        "雨": "rain", "雪": "snow", "森林": "forest", "沙漠": "desert",
        "办公": "office", "工作": "work", "学习": "study", "阅读": "reading",
        "编程": "coding", "电脑": "computer", "手机": "phone", "汽车": "car",
        "飞机": "airplane", "火车": "train", "建筑": "architecture", "艺术": "art",
        "舞蹈": "dance", "健身": "fitness", "瑜伽": "yoga", "跑步": "running",
    }
    translated = []
    for word in keywords.split():
        word = word.strip()
        if word in common_map:
            translated.append(common_map[word])
        elif re.search(r'[\u4e00-\u9fff]', word):
            # 未知中文词，用拼音或跳过
            translated.append(word)  # 保留，可能 API 也能处理
        else:
            translated.append(word)
    result = " ".join(translated)
    return result


def collect_media(keywords, count, output_path):
    en_keywords = translate_keywords_to_english(keywords)
    if en_keywords != keywords:
        info = f"🌐 关键词已翻译：{keywords} → {en_keywords}\n"
    else:
        info = ""
    cmd = f'bash "{SCRIPTS_DIR}/media-collector.sh" --keywords "{en_keywords}" --count {int(count)} --output "{output_path}"'
    success, output = run_command(cmd)
    return f"{info}✅ 素材搜集成功！\n\n{output}" if success else f"{info}❌ 素材搜集失败：{output}"


def collect_music(keywords, count, output_path):
    en_keywords = translate_keywords_to_english(keywords)
    cmd = f'bash "{SCRIPTS_DIR}/music-collector.sh" --keywords "{en_keywords}" --count {int(count)} --output "{output_path}"'
    success, output = run_command(cmd)
    return f"✅ 音乐搜集成功！\n\n{output}" if success else f"❌ 音乐搜集失败：{output}"


def generate_voiceover(script_text, project_path, voice="zh-CN-YunxiNeural"):
    voiceover_dir = Path(project_path) / "voiceover"
    voiceover_dir.mkdir(parents=True, exist_ok=True)
    script_file = Path(project_path) / "script.txt"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_text)
    cmd = f'bash "{SCRIPTS_DIR}/tts-voiceover.sh" --script-file "{script_file}" --output "{voiceover_dir}" --voice "{voice}" --merge'
    success, output = run_command(cmd)
    return f"✅ 配音生成成功！\n\n{output}" if success else f"❌ 配音生成失败：{output}"


def assemble_video(project_path, style, resolution, with_color_grade, with_broll):
    script_file = Path(project_path) / "script.txt"
    voiceover_dir = Path(project_path) / "voiceover"
    output_file = Path(project_path) / "final.mp4"
    cmd = f'bash "{SCRIPTS_DIR}/auto-video-maker.sh" --project "{project_path}" --script-file "{script_file}" --voiceover "{voiceover_dir}" --style "{style}" --output "{output_file}"'
    if with_color_grade:
        cmd += f' && bash "{SCRIPTS_DIR}/auto-color-grade.sh" "{output_file}" "{output_file}"'
    if with_broll:
        cmd += f' && bash "{SCRIPTS_DIR}/auto-broll-insert.sh" "{output_file}" "{project_path}" "{output_file}"'
    success, output = run_command(cmd)
    return f"✅ 视频组装成功！\n输出：{output_file}\n\n{output}" if success else f"❌ 视频组装失败：{output}"


def auto_video_pipeline(topic, style, duration, keywords, music_keywords,
                        voice_instr, resolution, with_color_grade, with_broll):
    project_name = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    log = ""

    def append(msg):
        nonlocal log
        log += msg + "\n"
        return log

    try:
        yield append("━━━ [1/6] 📁 创建项目结构...")
        project_path = create_project_structure(project_name, str(OUTPUT_DIR))
        yield append(f"  ✅ 项目路径：{project_path}\n")

        yield append("━━━ [2/6] 📝 生成 AI 文案...")
        script_file = Path(project_path) / "script.txt"
        ok, r = generate_script(topic, style, duration, output_path=str(script_file))
        if not ok:
            yield append(f"  {r}"); return
        yield append(f"  {r}\n")

        script_text = script_file.read_text(encoding='utf-8') if script_file.exists() else topic

        yield append("━━━ [3/6] 🔍 搜集视频素材...")
        r = collect_media(keywords, max(5, duration // 10), project_path)
        if "❌" in r:
            yield append(f"  {r}"); return
        yield append(f"  {r}\n")

        yield append("━━━ [4/6] 🎵 搜集背景音乐...")
        if music_keywords.strip():
            r = collect_music(music_keywords, 3, project_path)
            if "❌" in r:
                yield append(f"  ⚠️ 音乐搜集失败（跳过，不影响成片）：{r}\n")
            else:
                yield append(f"  {r}\n")
        else:
            yield append("  ⏭️ 未指定音乐关键词，跳过\n")

        yield append("━━━ [5/6] 🎤 TTS 配音 (edge-tts)...")
        r = generate_voiceover(script_text, project_path, voice_instr)
        if "❌" in r:
            yield append(f"  ⚠️ 配音失败（跳过，不影响成片）：{r}\n")
        else:
            yield append(f"  {r}\n")

        yield append("━━━ [6/6] 🎞️ 组装视频...")
        script_file_path = Path(project_path) / "script.txt"
        output_file = Path(project_path) / "final.mp4"
        cmd = f'bash "{SCRIPTS_DIR}/auto-video-maker.sh" --project "{project_path}" --script-file "{script_file_path}" --style "{style}" --duration {int(duration)} --output "{output_file}"'
        if with_color_grade:
            cmd += f' && bash "{SCRIPTS_DIR}/auto-color-grade.sh" "{output_file}" "{output_file}"'
        if with_broll:
            cmd += f' && bash "{SCRIPTS_DIR}/auto-broll-insert.sh" "{output_file}" "{project_path}" "{output_file}"'
        success, output = run_command(cmd)
        r = f"✅ 视频组装成功！\n输出：{output_file}\n\n{output}" if success else f"❌ 视频组装失败：{output}"
        if "❌" in r:
            yield append(f"  {r}"); return
        yield append(f"  {r}\n")

        yield append(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 视频生产完成！
📁 项目路径：{project_path}
🎬 输出文件：{Path(project_path) / 'final.mp4'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")
    except Exception as e:
        yield append(f"\n❌ 发生错误：{str(e)}")


# ─────────────────────────────────────────
# Tab 3: 剪辑辅助
# ─────────────────────────────────────────

def scene_detect(video_path):
    """场景检测"""
    cmd = f'bash "{SCRIPTS_DIR}/scene-detect.sh" "{video_path}"'
    success, output = run_command(cmd, timeout=300)
    return f"✅ 场景分析完成！\n\n{output}" if success else f"❌ 场景分析失败：{output}"


def auto_rough_cut(video_path):
    """自动粗剪（去除静音段）"""
    output_file = str(Path(video_path).with_stem(Path(video_path).stem + "_roughcut"))
    cmd = f'bash "{SCRIPTS_DIR}/auto-rough-cut.sh" "{video_path}" "{output_file}"'
    success, output = run_command(cmd, timeout=600)
    return f"✅ 粗剪完成！\n输出：{output_file}\n\n{output}" if success else f"❌ 粗剪失败：{output}"


def smart_tagger(media_folder):
    """智能标签"""
    cmd = f'bash "{SCRIPTS_DIR}/smart-tagger.sh" "{media_folder}"'
    success, output = run_command(cmd, timeout=300)
    return f"✅ 智能标签完成！\n\n{output}" if success else f"❌ 标签生成失败：{output}"


def auto_chapter_marker(video_path):
    """自动章节标记"""
    cmd = f'bash "{SCRIPTS_DIR}/auto-chapter-marker.sh" "{video_path}"'
    success, output = run_command(cmd, timeout=300)
    return f"✅ 章节标记完成！\n\n{output}" if success else f"❌ 章节标记失败：{output}"


# ─────────────────────────────────────────
# Tab 4: 音频处理
# ─────────────────────────────────────────

def audio_normalize(video_path):
    """音频标准化 (-23 LUFS)"""
    output_file = str(Path(video_path).with_stem(Path(video_path).stem + "_normalized"))
    cmd = f'bash "{SCRIPTS_DIR}/audio-normalizer.sh" "{video_path}" "{output_file}"'
    success, output = run_command(cmd, timeout=300)
    return f"✅ 音频标准化完成！\n输出：{output_file}\n\n{output}" if success else f"❌ 音频标准化失败：{output}"


def single_voiceover(text, output_path, voice="zh-CN-YunxiNeural"):
    """单文件配音"""
    if not output_path.strip():
        output_path = ensure_output_path(f"voiceover_{datetime.now().strftime('%H%M%S')}.wav")
    cmd = f'bash "{SCRIPTS_DIR}/auto-voiceover.sh" --voice "{voice}" "{text}" "{output_path}"'
    success, output = run_command(cmd, timeout=120)
    return f"✅ 配音生成成功！\n输出：{output_path}\n\n{output}" if success else f"❌ 配音生成失败：{output}"


# ─────────────────────────────────────────
# Tab 5: 字幕 & 缩略图
# ─────────────────────────────────────────

def multi_lang_subtitles(video_path, target_lang):
    """多语言字幕"""
    cmd = f'bash "{SCRIPTS_DIR}/multi-lang-subtitles.sh" "{video_path}" "{target_lang}"'
    success, output = run_command(cmd, timeout=600)
    return f"✅ 字幕生成完成！\n\n{output}" if success else f"❌ 字幕生成失败：{output}"


def auto_thumbnail(video_path, output_folder):
    """自动缩略图"""
    if not output_folder.strip():
        output_folder = ensure_output_path("thumbnails")
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    cmd = f'bash "{SCRIPTS_DIR}/auto-thumbnail.sh" "{video_path}" "{output_folder}"'
    success, output = run_command(cmd, timeout=120)
    return f"✅ 缩略图生成完成！\n输出目录：{output_folder}\n\n{output}" if success else f"❌ 缩略图生成失败：{output}"


# ─────────────────────────────────────────
# 新功能：视频分析 / BGM / 多平台 / 字幕样式 / 片头片尾 / 封面
# ─────────────────────────────────────────

def video_analyze(video_path):
    """视频质量分析"""
    cmd = f'bash "{SCRIPTS_DIR}/video-analyzer.sh" "{video_path}"'
    success, output = run_command(cmd, timeout=300)
    return f"✅ 分析完成！\n\n{output}" if success else f"❌ 分析失败：{output}"


def bgm_match(video_path, music_path, volume=15, fade_in=2, fade_out=3, no_original=False):
    """智能 BGM 匹配"""
    output_path = str(Path(video_path).with_stem(Path(video_path).stem + "_bgm"))
    cmd = f'bash "{SCRIPTS_DIR}/auto-bgm-match.sh" --video "{video_path}" --music "{music_path}" --output "{output_path}" --volume {int(volume)} --fade-in {int(fade_in)} --fade-out {int(fade_out)}'
    if no_original:
        cmd += ' --no-original'
    success, output = run_command(cmd, timeout=300)
    return f"✅ BGM 合成完成！\n输出：{output_path}\n\n{output}" if success else f"❌ BGM 合成失败：{output}"


def platform_export(video_path, platforms, mode="pad", quality="high"):
    """多平台适配导出"""
    output_dir = str(Path(video_path).parent / "exports")
    platform_args = " ".join(platforms)
    cmd = f'bash "{SCRIPTS_DIR}/multi-platform-export.sh" "{video_path}" --platforms {platform_args} --mode {mode} --quality {quality} --output "{output_dir}"'
    success, output = run_command(cmd, timeout=600)
    return f"✅ 多平台导出完成！\n输出目录：{output_dir}\n\n{output}" if success else f"❌ 导出失败：{output}"


def style_subtitles(srt_path, style, video_path="", burn=False, font_size=48):
    """字幕样式增强"""
    cmd = f'bash "{SCRIPTS_DIR}/subtitle-styler.sh" --srt "{srt_path}" --style {style} --font-size {int(font_size)}'
    if video_path.strip() and burn:
        cmd += f' --video "{video_path}" --burn'
    success, output = run_command(cmd, timeout=300)
    return f"✅ 字幕处理完成！\n\n{output}" if success else f"❌ 字幕处理失败：{output}"


def generate_intro_outro(title, type_val="intro", template="fade", subtitle="", duration=5, bg_color="black", social=""):
    """片头片尾生成"""
    output_file = ensure_output_path(f"{type_val}_{template}_{datetime.now().strftime('%H%M%S')}.mp4")
    cmd = f'bash "{SCRIPTS_DIR}/intro-outro-generator.sh" --title "{title}" --type {type_val} --template {template} --duration {int(duration)} --bg-color {bg_color} --output "{output_file}"'
    if subtitle.strip():
        cmd += f' --subtitle "{subtitle}"'
    if social.strip():
        cmd += f' --social "{social}"'
    success, output = run_command(cmd, timeout=120)
    return f"✅ {type_val} 生成完成！\n输出：{output_file}\n\n{output}" if success else f"❌ 生成失败：{output}"


def generate_cover(video_path, title, subtitle="", platforms=None, style="overlay"):
    """封面图生成"""
    if platforms is None:
        platforms = ["bilibili", "youtube"]
    output_dir = str(Path(video_path).parent / "covers")
    platform_args = " ".join(platforms)
    cmd = f'bash "{SCRIPTS_DIR}/cover-generator.sh" --video "{video_path}" --title "{title}" --style {style} --platforms {platform_args} --output "{output_dir}"'
    if subtitle.strip():
        cmd += f' --subtitle "{subtitle}"'
    success, output = run_command(cmd, timeout=120)
    return f"✅ 封面生成完成！\n输出目录：{output_dir}\n\n{output}" if success else f"❌ 封面生成失败：{output}"


# ─────────────────────────────────────────
# Tab 6: 调色 & B-roll
# ─────────────────────────────────────────

def quick_color_grade(video_path, style_preset, intensity, preview_only):
    """快速调色"""
    output_file = str(Path(video_path).with_stem(Path(video_path).stem + f"_{style_preset}"))
    cmd = f'bash "{SCRIPTS_DIR}/auto-color-grade.sh" "{video_path}" "{output_file}" --style "{style_preset}" --intensity {intensity}'
    if preview_only:
        cmd += " --preview"
    success, output = run_command(cmd, timeout=600)
    return f"✅ 调色成功！\n输出：{output_file}\n\n{output}" if success else f"❌ 调色失败：{output}"


def insert_broll(main_video, broll_folder, transition, min_dur, max_dur, audio_mode):
    """插入 B-roll"""
    output_file = str(Path(main_video).with_stem(Path(main_video).stem + "_broll"))
    cmd = (f'bash "{SCRIPTS_DIR}/auto-broll-insert.sh" "{main_video}" "{broll_folder}" "{output_file}"'
           f' --transition {transition} --min-duration {min_dur} --max-duration {max_dur} --audio {audio_mode}')
    success, output = run_command(cmd, timeout=600)
    return f"✅ B-roll 插入成功！\n输出：{output_file}\n\n{output}" if success else f"❌ B-roll 插入失败：{output}"


# ─────────────────────────────────────────
# Tab 7: FCP 项目管理
# ─────────────────────────────────────────

def check_fcp():
    """检查 FCP 状态"""
    success, output = run_osascript("check-fcp.scpt")
    return f"✅ FCP 状态：\n{output}" if success else f"❌ 检查失败（FCP 可能未运行）：{output}"


def list_fcp_projects():
    """列出 FCP 项目"""
    success, output = run_osascript("list-projects.scpt")
    return f"📁 项目列表：\n{output}" if success else f"❌ 获取失败（FCP 可能未运行）：{output}"


def open_fcp_project(project_name):
    """打开 FCP 项目"""
    success, output = run_osascript("open-project.scpt", project_name)
    return f"✅ 已打开项目：{project_name}\n{output}" if success else f"❌ 打开失败：{output}"


def import_temp_media():
    """导入临时素材"""
    success, output = run_osascript("import-temp-media.scpt")
    return f"✅ 素材导入成功！\n{output}" if success else f"❌ 导入失败：{output}"


def project_time_tracking():
    """项目时间追踪"""
    success, output = run_osascript("project-time-tracking.scpt")
    return f"⏱️ 时间追踪：\n{output}" if success else f"❌ 追踪失败：{output}"


def list_scripts():
    """列出文案"""
    success, output = run_osascript("list-scripts.scpt")
    return f"📝 文案列表：\n{output}" if success else f"❌ 获取失败：{output}"


def create_script_note(title, content):
    """创建文案到备忘录"""
    success, output = run_osascript("create-script.scpt", title, content)
    return f"✅ 文案已创建：{title}\n{output}" if success else f"❌ 创建失败：{output}"


# ─────────────────────────────────────────
# Tab 8: 自动发布
# ─────────────────────────────────────────

def auto_publish(video_path, platform, title, tags, description):
    """自动发布"""
    cmd = (f'bash "{SCRIPTS_DIR}/auto-publish.sh"'
           f' --video "{video_path}" --platform "{platform}"'
           f' --title "{title}" --tags "{tags}" --description "{description}"')
    success, output = run_command(cmd, timeout=600)
    return f"✅ 发布成功！\n平台：{platform}\n\n{output}" if success else f"❌ 发布失败：{output}"


# ─────────────────────────────────────────
# Tab 9: 项目历史
# ─────────────────────────────────────────

def list_projects():
    if not OUTPUT_DIR.exists():
        return "暂无项目"
    projects = []
    for item in sorted(OUTPUT_DIR.iterdir(), reverse=True):
        if item.is_dir():
            final_mp4 = item / "final.mp4"
            status = "✅" if final_mp4.exists() else "⏳"
            size_info = ""
            if final_mp4.exists():
                size_mb = final_mp4.stat().st_size / 1024 / 1024
                mtime = datetime.fromtimestamp(final_mp4.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                size_info = f" ({size_mb:.1f} MB, {mtime})"
            # 列出子文件夹内容
            contents = []
            for sub in ["videos", "music", "voiceover"]:
                sub_path = item / sub
                if sub_path.exists():
                    count = len(list(sub_path.iterdir()))
                    if count > 0:
                        contents.append(f"{sub}: {count}")
            content_str = f"\n   内容：{', '.join(contents)}" if contents else ""
            projects.append(f"{status} {item.name}{size_info}{content_str}")
    return "\n\n".join(projects) if projects else "暂无项目"


# ═══════════════════════════════════════════
# 构建 Gradio 界面
# ═══════════════════════════════════════════

with gr.Blocks(title="FCPX Assistant") as demo:
    gr.Markdown("""
    # 🎬 FCPX Assistant WebUI
    **从主题到成片，一键搞定！** Made by Steve & Steven (≧∇≦)
    """)

    with gr.Tabs():

        # ═══ Tab 1: 一键成片 ═══
        with gr.TabItem("🚀 一键成片"):
            gr.Markdown("### 输入主题，自动完成所有步骤！")
            with gr.Row():
                with gr.Column():
                    topic_input = gr.Textbox(label="视频主题", placeholder="例如：如何制作一杯完美的咖啡", lines=2)
                    style_input = gr.Dropdown(label="视频风格", choices=["vlog", "科普", "教程", "带货", "故事", "cinematic", "fast"], value="vlog")
                    duration_input = gr.Slider(label="目标时长（秒）", minimum=30, maximum=600, value=90, step=10)
                    keywords_input = gr.Textbox(label="素材搜索关键词", placeholder="咖啡 制作 教程", lines=2)
                    music_keywords_input = gr.Textbox(label="音乐风格关键词", placeholder="轻松 愉快 日常")
                    voice_instr_input = gr.Dropdown(
                        label="配音声音",
                        choices=[
                            ("男-阳光活泼 (YunxiNeural)", "zh-CN-YunxiNeural"),
                            ("男-激情有力 (YunjianNeural)", "zh-CN-YunjianNeural"),
                            ("男-专业新闻 (YunyangNeural)", "zh-CN-YunyangNeural"),
                            ("女-温暖亲切 (XiaoxiaoNeural)", "zh-CN-XiaoxiaoNeural"),
                            ("女-活泼可爱 (XiaoyiNeural)", "zh-CN-XiaoyiNeural"),
                        ],
                        value="zh-CN-YunxiNeural"
                    )
                    resolution_input = gr.Dropdown(label="分辨率", choices=["1920x1080", "1080x1920", "3840x2160", "1280x720"], value="1920x1080")
                    with gr.Row():
                        color_grade_check = gr.Checkbox(label="✨ 自动调色", value=True)
                        broll_check = gr.Checkbox(label="🎬 自动 B-roll", value=True)
                    run_button = gr.Button("🚀 开始生产", variant="primary", size="lg")
                with gr.Column():
                    pipeline_output = gr.Textbox(label="生产日志", lines=25, max_lines=50)
            run_button.click(
                auto_video_pipeline,
                inputs=[topic_input, style_input, duration_input, keywords_input,
                        music_keywords_input, voice_instr_input, resolution_input,
                        color_grade_check, broll_check],
                outputs=pipeline_output
            )

        # ═══ Tab 2: 分步工具 ═══
        with gr.TabItem("🛠️ 分步工具"):
            gr.Markdown("### 单独执行生产流程中的各个步骤")
            with gr.Tabs():

                with gr.TabItem("📝 生成文案"):
                    with gr.Row():
                        with gr.Column():
                            gen_topic = gr.Textbox(label="主题", lines=2)
                            gen_style = gr.Dropdown(label="风格", choices=["vlog", "科普", "教程", "带货", "故事"], value="vlog")
                            gen_duration = gr.Slider(30, 600, 90, step=10, label="时长（秒）")
                            gen_btn = gr.Button("📝 生成文案", variant="primary")
                        gen_output = gr.Textbox(label="结果", lines=15)
                    def gen_script_ui(topic, style, duration):
                        _, result = generate_script(topic, style, duration)
                        return result
                    gen_btn.click(gen_script_ui, inputs=[gen_topic, gen_style, gen_duration], outputs=gen_output)

                with gr.TabItem("🔍 搜集素材"):
                    with gr.Row():
                        with gr.Column():
                            media_kw = gr.Textbox(label="关键词（空格分隔）", placeholder="nature ocean sunset")
                            media_cnt = gr.Slider(1, 20, 5, step=1, label="数量")
                            media_out = gr.Textbox(label="输出目录", value=str(OUTPUT_DIR), lines=1)
                            media_btn = gr.Button("🔍 搜集素材", variant="primary")
                        media_result = gr.Textbox(label="结果", lines=15)
                    media_btn.click(collect_media, inputs=[media_kw, media_cnt, media_out], outputs=media_result)

                with gr.TabItem("🎵 搜集音乐"):
                    with gr.Row():
                        with gr.Column():
                            mus_kw = gr.Textbox(label="音乐风格关键词", placeholder="chill lofi piano")
                            mus_cnt = gr.Slider(1, 10, 3, step=1, label="数量")
                            mus_out = gr.Textbox(label="输出目录", value=str(OUTPUT_DIR / "music"), lines=1)
                            mus_btn = gr.Button("🎵 搜集音乐", variant="primary")
                        mus_result = gr.Textbox(label="结果", lines=15)
                    mus_btn.click(collect_music, inputs=[mus_kw, mus_cnt, mus_out], outputs=mus_result)

                with gr.TabItem("🎤 生成配音"):
                    with gr.Row():
                        with gr.Column():
                            vo_script = gr.Textbox(label="文案（每段一行）", lines=5, placeholder="第一段文案\n第二段文案\n第三段文案")
                            vo_proj = gr.Textbox(label="项目目录", value=str(OUTPUT_DIR))
                            vo_voice = gr.Dropdown(
                                label="声音",
                                choices=[
                                    ("男-阳光活泼", "zh-CN-YunxiNeural"),
                                    ("男-激情有力", "zh-CN-YunjianNeural"),
                                    ("男-专业新闻", "zh-CN-YunyangNeural"),
                                    ("女-温暖亲切", "zh-CN-XiaoxiaoNeural"),
                                    ("女-活泼可爱", "zh-CN-XiaoyiNeural"),
                                ],
                                value="zh-CN-YunxiNeural"
                            )
                            vo_btn = gr.Button("🎤 生成配音", variant="primary")
                        vo_result = gr.Textbox(label="结果", lines=10)
                    vo_btn.click(generate_voiceover, inputs=[vo_script, vo_proj, vo_voice], outputs=vo_result)

        # ═══ Tab 3: 剪辑辅助 ═══
        with gr.TabItem("✂️ 剪辑辅助"):
            gr.Markdown("### 视频分析与自动剪辑工具")
            with gr.Tabs():

                with gr.TabItem("🔎 场景分析"):
                    gr.Markdown("分析视频中的场景切换点，生成场景列表。")
                    with gr.Row():
                        with gr.Column():
                            sd_video = gr.Textbox(label="视频文件路径", placeholder="/path/to/video.mp4")
                            sd_btn = gr.Button("🔎 开始分析", variant="primary")
                        sd_result = gr.Textbox(label="分析结果", lines=15)
                    sd_btn.click(scene_detect, inputs=[sd_video], outputs=sd_result)

                with gr.TabItem("✂️ 自动粗剪"):
                    gr.Markdown("自动去除视频中的静音段落，生成粗剪版本。")
                    with gr.Row():
                        with gr.Column():
                            rc_video = gr.Textbox(label="视频文件路径", placeholder="/path/to/video.mp4")
                            rc_btn = gr.Button("✂️ 开始粗剪", variant="primary")
                        rc_result = gr.Textbox(label="结果", lines=10)
                    rc_btn.click(auto_rough_cut, inputs=[rc_video], outputs=rc_result)

                with gr.TabItem("🏷️ 智能标签"):
                    gr.Markdown("扫描素材文件夹，自动生成智能标签和分类。")
                    with gr.Row():
                        with gr.Column():
                            st_folder = gr.Textbox(label="素材文件夹路径", placeholder="/path/to/media/")
                            st_btn = gr.Button("🏷️ 生成标签", variant="primary")
                        st_result = gr.Textbox(label="结果", lines=15)
                    st_btn.click(smart_tagger, inputs=[st_folder], outputs=st_result)

                with gr.TabItem("📑 章节标记"):
                    gr.Markdown("自动检测视频结构，生成章节标记（适合 YouTube 等平台）。")
                    with gr.Row():
                        with gr.Column():
                            cm_video = gr.Textbox(label="视频文件路径", placeholder="/path/to/video.mp4")
                            cm_btn = gr.Button("📑 生成章节", variant="primary")
                        cm_result = gr.Textbox(label="结果", lines=15)
                    cm_btn.click(auto_chapter_marker, inputs=[cm_video], outputs=cm_result)

                with gr.TabItem("📊 视频分析"):
                    gr.Markdown("分析视频画面亮度、色温、音频响度，输出质量评分和改进建议。")
                    with gr.Row():
                        with gr.Column():
                            va_video = gr.Textbox(label="视频文件路径", placeholder="/path/to/video.mp4")
                            va_btn = gr.Button("📊 开始分析", variant="primary")
                        va_result = gr.Textbox(label="分析报告", lines=20)
                    va_btn.click(video_analyze, inputs=[va_video], outputs=va_result)

        # ═══ Tab 4: 音频处理 ═══
        with gr.TabItem("🔊 音频处理"):
            gr.Markdown("### 音频标准化与配音工具")
            with gr.Tabs():

                with gr.TabItem("📊 音频标准化"):
                    gr.Markdown("将音频标准化到 -23 LUFS（广播标准），让音量一致。")
                    with gr.Row():
                        with gr.Column():
                            an_video = gr.Textbox(label="视频/音频文件路径", placeholder="/path/to/video.mp4")
                            an_btn = gr.Button("📊 标准化", variant="primary")
                        an_result = gr.Textbox(label="结果", lines=10)
                    an_btn.click(audio_normalize, inputs=[an_video], outputs=an_result)

                with gr.TabItem("🎤 快速配音"):
                    gr.Markdown("输入一段文字，快速生成单个配音文件。(edge-tts)")
                    with gr.Row():
                        with gr.Column():
                            sv_text = gr.Textbox(label="文本内容", lines=3, placeholder="输入要配音的文字...")
                            sv_voice = gr.Dropdown(
                                label="声音",
                                choices=[
                                    ("男-阳光活泼", "zh-CN-YunxiNeural"),
                                    ("男-激情有力", "zh-CN-YunjianNeural"),
                                    ("女-温暖亲切", "zh-CN-XiaoxiaoNeural"),
                                    ("女-活泼可爱", "zh-CN-XiaoyiNeural"),
                                ],
                                value="zh-CN-YunxiNeural"
                            )
                            sv_output = gr.Textbox(label="输出路径（留空自动生成）", placeholder="/path/to/output.wav")
                            sv_btn = gr.Button("🎤 生成配音", variant="primary")
                        sv_result = gr.Textbox(label="结果", lines=10)
                    sv_btn.click(single_voiceover, inputs=[sv_text, sv_output, sv_voice], outputs=sv_result)

                with gr.TabItem("🎵 BGM 匹配"):
                    gr.Markdown("自动匹配 BGM 到视频，支持淡入淡出和音量控制。")
                    with gr.Row():
                        with gr.Column():
                            bgm_video = gr.Textbox(label="视频文件路径", placeholder="/path/to/video.mp4")
                            bgm_music = gr.Textbox(label="BGM 文件或目录", placeholder="/path/to/music/ 或 track.mp3")
                            bgm_volume = gr.Slider(5, 50, 15, step=5, label="BGM 音量 (%)")
                            with gr.Row():
                                bgm_fadein = gr.Slider(0, 10, 2, step=1, label="淡入 (秒)")
                                bgm_fadeout = gr.Slider(0, 10, 3, step=1, label="淡出 (秒)")
                            bgm_no_orig = gr.Checkbox(label="去掉原始音频（仅保留 BGM）", value=False)
                            bgm_btn = gr.Button("🎵 合成 BGM", variant="primary")
                        bgm_result = gr.Textbox(label="结果", lines=10)
                    bgm_btn.click(bgm_match, inputs=[bgm_video, bgm_music, bgm_volume, bgm_fadein, bgm_fadeout, bgm_no_orig], outputs=bgm_result)

        # ═══ Tab 5: 字幕 & 缩略图 ═══
        with gr.TabItem("🌍 字幕 & 缩略图"):
            gr.Markdown("### 多语言字幕生成与自动缩略图")
            with gr.Tabs():

                with gr.TabItem("🌍 多语言字幕"):
                    gr.Markdown("为视频生成指定语言的字幕文件。")
                    with gr.Row():
                        with gr.Column():
                            sub_video = gr.Textbox(label="视频文件路径", placeholder="/path/to/video.mp4")
                            sub_lang = gr.Dropdown(
                                label="目标语言",
                                choices=[("英语", "en"), ("日语", "ja"), ("韩语", "ko"),
                                         ("法语", "fr"), ("德语", "de"), ("西班牙语", "es")],
                                value="en"
                            )
                            sub_btn = gr.Button("🌍 生成字幕", variant="primary")
                        sub_result = gr.Textbox(label="结果", lines=10)
                    sub_btn.click(multi_lang_subtitles, inputs=[sub_video, sub_lang], outputs=sub_result)

                with gr.TabItem("🖼️ 自动缩略图"):
                    gr.Markdown("从视频中提取关键帧作为缩略图，并生成联系人表。")
                    with gr.Row():
                        with gr.Column():
                            th_video = gr.Textbox(label="视频文件路径", placeholder="/path/to/video.mp4")
                            th_output = gr.Textbox(label="输出目录（留空自动生成）", placeholder="/path/to/thumbs/")
                            th_btn = gr.Button("🖼️ 生成缩略图", variant="primary")
                        th_result = gr.Textbox(label="结果", lines=10)
                    th_btn.click(auto_thumbnail, inputs=[th_video, th_output], outputs=th_result)

                with gr.TabItem("🔤 字幕样式"):
                    gr.Markdown("为 SRT 字幕添加样式效果（电影感/卡拉OK/霓虹等），支持烧入视频。")
                    with gr.Row():
                        with gr.Column():
                            ss_srt = gr.Textbox(label="SRT 字幕文件", placeholder="/path/to/subtitle.srt")
                            ss_style = gr.Dropdown(label="样式", choices=[
                                ("默认-白字描边", "default"), ("电影感", "cinematic"), ("卡拉OK", "karaoke"),
                                ("现代", "modern"), ("顶部弹幕", "top"), ("大字居中", "big"),
                                ("粗描边", "outline"), ("霓虹发光", "neon")
                            ], value="cinematic")
                            ss_fontsize = gr.Slider(24, 96, 48, step=4, label="字号")
                            ss_video = gr.Textbox(label="视频文件（烧入时需要）", placeholder="/path/to/video.mp4")
                            ss_burn = gr.Checkbox(label="烧入视频", value=False)
                            ss_btn = gr.Button("🔤 生成字幕", variant="primary")
                        ss_result = gr.Textbox(label="结果", lines=10)
                    def style_sub_ui(srt, style, fontsize, video, burn):
                        return style_subtitles(srt, style, video, burn, fontsize)
                    ss_btn.click(style_sub_ui, inputs=[ss_srt, ss_style, ss_fontsize, ss_video, ss_burn], outputs=ss_result)

        # ═══ Tab 6: 调色 & B-roll ═══
        with gr.TabItem("🎨 调色 & B-roll"):
            gr.Markdown("### 后期调色与 B-roll 自动插入")
            with gr.Tabs():

                with gr.TabItem("🎨 调色"):
                    gr.Markdown("为视频应用电影级调色预设。")
                    with gr.Row():
                        with gr.Column():
                            cg_video = gr.Textbox(label="视频文件路径", placeholder="/path/to/video.mp4")
                            cg_style = gr.Dropdown(
                                label="调色风格",
                                choices=[("自然", "natural"), ("电影", "cinematic"), ("复古", "vintage"),
                                         ("清新", "fresh"), ("暖色", "warm"), ("冷色", "cool")],
                                value="natural"
                            )
                            cg_intensity = gr.Slider(0.0, 1.0, 0.7, step=0.1, label="强度")
                            cg_preview = gr.Checkbox(label="仅预览前 10 秒", value=False)
                            cg_btn = gr.Button("🎨 开始调色", variant="primary")
                        cg_result = gr.Textbox(label="结果", lines=10)
                    cg_btn.click(quick_color_grade, inputs=[cg_video, cg_style, cg_intensity, cg_preview], outputs=cg_result)

                with gr.TabItem("🎬 B-roll 插入"):
                    gr.Markdown("在场景切换处自动插入 B-roll 素材。")
                    with gr.Row():
                        with gr.Column():
                            br_video = gr.Textbox(label="主视频路径", placeholder="/path/to/main.mp4")
                            br_folder = gr.Textbox(label="B-roll 素材文件夹", placeholder="/path/to/broll/")
                            br_transition = gr.Dropdown(label="转场类型", choices=["fade", "dissolve", "none"], value="fade")
                            with gr.Row():
                                br_min = gr.Slider(1, 10, 2, step=1, label="最短时长（秒）")
                                br_max = gr.Slider(1, 15, 5, step=1, label="最长时长（秒）")
                            br_audio = gr.Dropdown(label="B-roll 音频", choices=[("静音", "mute"), ("混合", "mix"), ("替换", "replace")], value="mute")
                            br_btn = gr.Button("🎬 插入 B-roll", variant="primary")
                        br_result = gr.Textbox(label="结果", lines=10)
                    br_btn.click(insert_broll, inputs=[br_video, br_folder, br_transition, br_min, br_max, br_audio], outputs=br_result)

        # ═══ Tab 7: FCP 项目管理 ═══
        with gr.TabItem("🎬 FCP 管理"):
            gr.Markdown("### Final Cut Pro 项目管理（需要 FCP 运行中）")
            with gr.Tabs():

                with gr.TabItem("📊 状态 & 项目"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("**FCP 状态检查**")
                            fcp_check_btn = gr.Button("🔍 检查 FCP 状态", variant="secondary")
                            fcp_check_result = gr.Textbox(label="状态", lines=5)
                            fcp_check_btn.click(check_fcp, outputs=fcp_check_result)

                        with gr.Column():
                            gr.Markdown("**项目列表**")
                            fcp_list_btn = gr.Button("📁 列出项目", variant="secondary")
                            fcp_list_result = gr.Textbox(label="项目列表", lines=5)
                            fcp_list_btn.click(list_fcp_projects, outputs=fcp_list_result)

                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("**打开项目**")
                            fcp_open_name = gr.Textbox(label="项目名称")
                            fcp_open_btn = gr.Button("▶️ 打开项目", variant="primary")
                            fcp_open_result = gr.Textbox(label="结果", lines=3)
                            fcp_open_btn.click(open_fcp_project, inputs=[fcp_open_name], outputs=fcp_open_result)

                        with gr.Column():
                            gr.Markdown("**导入临时素材**")
                            fcp_import_btn = gr.Button("📥 导入素材", variant="primary")
                            fcp_import_result = gr.Textbox(label="结果", lines=3)
                            fcp_import_btn.click(import_temp_media, outputs=fcp_import_result)

                with gr.TabItem("⏱️ 时间追踪"):
                    gr.Markdown("追踪 FCP 项目的编辑时间。")
                    fcp_time_btn = gr.Button("⏱️ 查看时间追踪", variant="primary")
                    fcp_time_result = gr.Textbox(label="时间追踪", lines=15)
                    fcp_time_btn.click(project_time_tracking, outputs=fcp_time_result)

                with gr.TabItem("📝 文案管理"):
                    gr.Markdown("在 Apple 备忘录中管理视频文案。")
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("**查看文案**")
                            script_list_btn = gr.Button("📋 列出文案", variant="secondary")
                            script_list_result = gr.Textbox(label="文案列表", lines=10)
                            script_list_btn.click(list_scripts, outputs=script_list_result)
                        with gr.Column():
                            gr.Markdown("**新建文案**")
                            script_title = gr.Textbox(label="标题")
                            script_content = gr.Textbox(label="内容", lines=5)
                            script_create_btn = gr.Button("✏️ 创建文案", variant="primary")
                            script_create_result = gr.Textbox(label="结果", lines=3)
                            script_create_btn.click(create_script_note, inputs=[script_title, script_content], outputs=script_create_result)

        # ═══ Tab: 片头片尾 & 封面 ═══
        with gr.TabItem("🎬 片头 & 封面"):
            gr.Markdown("### 片头片尾动画 + 多平台封面图生成")
            with gr.Tabs():
                with gr.TabItem("🎬 片头片尾"):
                    gr.Markdown("预设动画模板，支持自定义标题、副标题。")
                    with gr.Row():
                        with gr.Column():
                            io_title = gr.Textbox(label="标题", placeholder="我的频道")
                            io_subtitle = gr.Textbox(label="副标题", placeholder="每周更新")
                            io_type = gr.Radio(label="类型", choices=["intro", "outro"], value="intro")
                            io_template = gr.Dropdown(label="模板", choices=[
                                ("淡入淡出", "fade"), ("缩放", "zoom"), ("滑入", "slide"),
                                ("极简", "minimal"), ("社交卡片", "social"), ("订阅提示", "subscribe")
                            ], value="fade")
                            io_duration = gr.Slider(3, 10, 5, step=1, label="时长 (秒)")
                            io_bg = gr.Dropdown(label="背景色", choices=["black", "white", "#1a1a2e", "#16213e"], value="black")
                            io_social = gr.Textbox(label="社交链接 (social/subscribe 模板用)", placeholder="B站: @mychannel")
                            io_btn = gr.Button("🎬 生成", variant="primary")
                        io_result = gr.Textbox(label="结果", lines=10)
                    def gen_io_ui(title, subtitle, type_val, template, duration, bg, social):
                        return generate_intro_outro(title, type_val, template, subtitle, duration, bg, social)
                    io_btn.click(gen_io_ui, inputs=[io_title, io_subtitle, io_type, io_template, io_duration, io_bg, io_social], outputs=io_result)

                with gr.TabItem("🖼️ 封面生成"):
                    gr.Markdown("从视频关键帧 + 标题文字生成各平台封面图。")
                    with gr.Row():
                        with gr.Column():
                            cv_video = gr.Textbox(label="视频文件", placeholder="/path/to/video.mp4")
                            cv_title = gr.Textbox(label="封面标题", placeholder="10个编程技巧")
                            cv_subtitle = gr.Textbox(label="副标题")
                            cv_style = gr.Dropdown(label="样式", choices=[
                                ("半透明暗层", "overlay"), ("底部渐变", "gradient"),
                                ("纯色底条", "solid"), ("模糊背景", "blur"), ("纯截图", "clean")
                            ], value="overlay")
                            cv_platforms = gr.CheckboxGroup(label="目标平台", choices=[
                                "bilibili", "youtube", "tiktok", "xiaohongshu", "xhs-square", "wechat"
                            ], value=["bilibili", "youtube"])
                            cv_btn = gr.Button("🖼️ 生成封面", variant="primary")
                        cv_result = gr.Textbox(label="结果", lines=10)
                    def gen_cover_ui(video, title, subtitle, style, platforms):
                        return generate_cover(video, title, subtitle, platforms, style)
                    cv_btn.click(gen_cover_ui, inputs=[cv_video, cv_title, cv_subtitle, cv_style, cv_platforms], outputs=cv_result)

        # ═══ Tab 8: 自动发布 ═══
        with gr.TabItem("🚀 发布"):
            gr.Markdown("### 将成品视频发布到各大平台")
            with gr.Row():
                with gr.Column():
                    pub_video = gr.Textbox(label="视频文件路径", placeholder="/path/to/final.mp4")
                    pub_platform = gr.Dropdown(
                        label="发布平台",
                        choices=[("B 站", "bilibili"), ("YouTube", "youtube"),
                                 ("抖音", "tiktok"), ("小红书", "xiaohongshu")],
                        value="bilibili"
                    )
                    pub_title = gr.Textbox(label="标题", placeholder="我的视频标题")
                    pub_tags = gr.Textbox(label="标签（逗号分隔）", placeholder="vlog，日常，教程")
                    pub_desc = gr.Textbox(label="简介", lines=3, placeholder="视频简介...")
                    pub_btn = gr.Button("🚀 发布", variant="primary", size="lg")
                with gr.Column():
                    pub_result = gr.Textbox(label="发布结果", lines=15)
            pub_btn.click(auto_publish, inputs=[pub_video, pub_platform, pub_title, pub_tags, pub_desc], outputs=pub_result)

        # ═══ Tab: 多平台导出 ═══
        with gr.TabItem("📱 多平台导出"):
            gr.Markdown("### 一个视频导出多种尺寸，适配各平台")
            with gr.Row():
                with gr.Column():
                    pe_video = gr.Textbox(label="视频文件路径", placeholder="/path/to/video.mp4")
                    pe_platforms = gr.CheckboxGroup(label="目标平台", choices=[
                        "youtube", "bilibili", "tiktok", "reels", "shorts",
                        "xiaohongshu", "xhs-square", "twitter", "wechat", "wechat-v"
                    ], value=["youtube", "tiktok", "bilibili"])
                    pe_mode = gr.Dropdown(label="适配模式", choices=[
                        ("加黑边", "pad"), ("智能裁切", "crop"), ("缩放适配", "fit")
                    ], value="pad")
                    pe_quality = gr.Dropdown(label="质量", choices=[
                        ("高", "high"), ("中", "medium"), ("低", "low")
                    ], value="high")
                    pe_btn = gr.Button("📱 开始导出", variant="primary", size="lg")
                pe_result = gr.Textbox(label="导出结果", lines=15)
            pe_btn.click(platform_export, inputs=[pe_video, pe_platforms, pe_mode, pe_quality], outputs=pe_result)

        # ═══ Tab: 项目历史 ═══
        with gr.TabItem("📂 项目历史"):
            gr.Markdown("### 查看历史项目")
            project_list_display = gr.Textbox(label="项目列表", lines=20)
            refresh_btn = gr.Button("🔄 刷新", variant="secondary")
            refresh_btn.click(list_projects, outputs=project_list_display)

    gr.Markdown("""
    ---
    **FCPX Assistant v3.0** | Powered by Gradio + edge-tts + Whisper | Made with ❤️ by Steve & Steven (≧∇≦)
    """)

if __name__ == "__main__":
    print("🚀 启动 FCPX Assistant WebUI...")
    print(f"📁 项目输出目录：{OUTPUT_DIR}")
    print(f"🎬 访问地址：http://localhost:7861")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        show_error=True,
        share=False,
        theme=gr.themes.Soft(),
        css=".gradio-container {max-width: 1200px !important}"
    )
