"""
重生爽文全自动流水线
用法见 SKILL.md
"""

import os
import re
import time
import random
import argparse
import subprocess

import requests
from openai import OpenAI

# ─────────────────────────────────────────────────────────────
#  默认 Prompt
# ─────────────────────────────────────────────────────────────

DEFAULT_PREMISE_PROMPT = """你是一个深谙人性和流量密码的网文脑洞大师。
请生成【一句】极具爆点和情绪张力的"重生复仇、放下助人情结"的短篇小说核心设定。

公式必须严格遵守：
[极端爆款场景] + [白莲花/绿茶/作精反派]非要进行[某种作死行为]。上一世我拼命阻止，却被[反派煽动群众]合伙[害死]。这一世我重生，决定[冷眼旁观/主动帮他们把路走绝]。

例如：
- 公司团建去野山，绿茶女同事非要带大家和藏马熊合影，上一世我拦着被全公司网暴推下山崖，这一世我笑着给他们当摄影师。

要求：脑洞要大，反派要气人，群众要降智，主角要冷血。直接输出这句话，不要多余废话。日常题材（职场、校园、家庭），末日、玄幻不要。"""

DEFAULT_STORY_PROMPT = """你是一位白金级网文作家，擅长"重生打脸"情绪流爽文。请根据提供的【8步大纲】写一篇充满张力的短篇小说。
写作要领：
1. 第一人称视角。文字冷酷、清醒，主角绝不内耗。
2. 极度压抑：第4步和第5步，要把群众的丑恶嘴脸、忘恩负义写得令人发指，让读者看懂拳头变硬。
3. 极度释放：第7步和第8步的报应必须非常惨烈（断手断脚、家破人亡、或者惨死），主角绝对不救，只在最后出面无情嘲讽。
4. 对话极具画面感，少用旁白，多用动作和冲突推动剧情。
5. 输出内容会直接转化成语音，所以不要有标题或者章节分割，直接连贯输出正文内容。"""

OUTLINE_PROMPT = """你是一个顶级的网文大纲策划师。请根据提供的核心冲突，严格按照以下【8步公式】扩充出逻辑严密的爽文大纲：
1. 上一世：我因善良阻止反派作死，反被反派污蔑，煽动乌合之众害死。
2. 重生：回到命运转折点，决定冷眼旁观/主动帮他们把路走绝。
3. 逼迫：我不阻拦，但反派非要我同流合污/怕我告密/变本加厉抢夺财物。
4. 网暴（重点）：反派煽动群众攻击我，大幅描写群众的愚蠢、贪婪和对我的霸凌。
5. 夺走：反派和群众逼我就范。
6. 转折：我留有后手，有惊无险，反派根据原计划开始作死行为。
7. 崩塌：反派的作死行为导致严重后果，写得非常惨烈。
8. 结局：反派和群众开始忏悔，我在高处冷笑俯视。"""

# ─────────────────────────────────────────────────────────────
#  路径常量
# ─────────────────────────────────────────────────────────────

INPUT_FILE   = "output.txt"
AUDIO_DIR    = "audio"
VIDEO_DIR    = "video"
MERGED_AUDIO = "merged_audio.mp3"
VIDEO_LIST   = "video_list.txt"
AUDIO_LIST   = "audio_list.txt"

TTS_API_URL  = "https://zero-libre-tts.vercel.app/api/tts"
VOICE_CONFIG = {"voice": "zh-CN-XiaoxiaoMultilingualNeural", "rate": 50, "pitch": 0, "preview": False}

# ─────────────────────────────────────────────────────────────
#  素材检查
# ─────────────────────────────────────────────────────────────

def check_assets_for_video():
    """
    执行视频合成前检查所有必要素材，缺失时打印清晰指引并抛出异常。
    """
    errors = []

    # 1. audio/ 目录
    if not os.path.exists(AUDIO_DIR):
        errors.append(
            f"  ✗ 缺少 audio/ 目录\n"
            f"    → 请先执行步骤2（生成语音），会自动创建此目录并填入 .mp3 文件"
        )
    else:
        mp3s = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]
        if not mp3s:
            errors.append(
                f"  ✗ audio/ 目录存在但没有 .mp3 文件\n"
                f"    → 请先执行步骤2（生成语音）"
            )

    # 2. video/ 目录
    if not os.path.exists(VIDEO_DIR):
        errors.append(
            f"  ✗ 缺少 video/ 目录\n"
            f"    → 请在脚本同级目录下新建 video/ 文件夹，\n"
            f"      并放入至少一个竖屏 .mp4 视频素材（建议无版权背景视频）"
        )
    else:
        mp4s = [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")]
        if not mp4s:
            errors.append(
                f"  ✗ video/ 目录存在但没有 .mp4 文件\n"
                f"    → 请向 video/ 文件夹中放入至少一个 .mp4 视频素材\n"
                f"      推荐使用竖屏（9:16）无版权素材，横屏也可自动裁剪"
            )

    # 3. bgm.mp3
    if not os.path.exists("bgm.mp3"):
        errors.append(
            f"  ✗ 缺少 bgm.mp3\n"
            f"    → 请将背景音乐文件命名为 bgm.mp3，放在脚本同级目录下\n"
            f"      推荐使用无版权轻音乐（时长 > 3分钟 以免循环卡顿）"
        )

    # 4. ffmpeg / ffprobe
    for tool in ("ffmpeg", "ffprobe"):
        try:
            subprocess.run([tool, "-version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            errors.append(
                f"  ✗ 系统未找到 {tool}\n"
                f"    → 请安装 FFmpeg：https://ffmpeg.org/download.html\n"
                f"      macOS:   brew install ffmpeg\n"
                f"      Ubuntu:  sudo apt install ffmpeg\n"
                f"      Windows: 下载后将 bin/ 目录加入 PATH"
            )

    if errors:
        border = "─" * 54
        msg = (
            f"\n{border}\n"
            f"  ⚠️  视频合成素材检查未通过，请按以下提示操作：\n"
            f"{border}\n"
            + "\n\n".join(errors)
            + f"\n{border}\n"
            f"  修复后重新执行：python pipeline.py --video\n"
            f"{border}\n"
        )
        raise RuntimeError(msg)

    log("✓ 素材检查通过")


def check_assets_for_audio():
    """执行语音合成前检查 output.txt 是否存在。"""
    if not os.path.exists(INPUT_FILE):
        border = "─" * 54
        raise RuntimeError(
            f"\n{border}\n"
            f"  ⚠️  找不到 {INPUT_FILE}\n"
            f"    → 请先执行步骤1（生成小说）：\n"
            f"      python pipeline.py --novel --theme 末日\n"
            f"{border}\n"
        )


# ─────────────────────────────────────────────────────────────
#  工具函数
# ─────────────────────────────────────────────────────────────

def log(msg):
    print(msg, flush=True)


def _make_client(cfg: dict) -> OpenAI:
    api_key  = cfg.get("api_key")  or os.environ.get("OPENAI_API_KEY",  "")
    base_url = cfg.get("base_url") or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    if not api_key:
        raise ValueError("缺少 API Key：请在 cfg['api_key'] 或环境变量 OPENAI_API_KEY 中提供")
    return OpenAI(api_key=api_key, base_url=base_url)


def _model(cfg: dict) -> str:
    return cfg.get("model") or os.environ.get("OPENAI_MODEL", "gpt-4o")


def _run_cmd(cmd: str):
    log(f"  $ {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def _get_duration(file: str) -> float:
    cmd = f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{file}"'
    return float(subprocess.check_output(cmd, shell=True).decode().strip())


# ─────────────────────────────────────────────────────────────
#  步骤 1：生成小说
# ─────────────────────────────────────────────────────────────

def _generate_premise(client, model, theme, premise_prompt):
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": premise_prompt},
            {"role": "user",   "content": f"请生成一个题材为【{theme}】的脑洞。"},
        ],
        temperature=0.9,
    )
    return resp.choices[0].message.content.strip()


def _generate_outline(client, model, premise):
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": OUTLINE_PROMPT},
            {"role": "user",   "content": f"核心设定：{premise}"},
        ],
        temperature=0.7,
    )
    return resp.choices[0].message.content


def _generate_story(client, model, outline, story_prompt):
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": story_prompt},
            {"role": "user",   "content": f"大纲如下，请直接输出正文小说：\n\n{outline}"},
        ],
        temperature=0.8,
    )
    return resp.choices[0].message.content


def run_novel(theme: str = "随机猎奇", cfg: dict = None):
    """生成小说，保存到 output.txt"""
    cfg = cfg or {}
    client = _make_client(cfg)
    model  = _model(cfg)
    premise_prompt = cfg.get("premise_prompt", DEFAULT_PREMISE_PROMPT)
    story_prompt   = cfg.get("story_prompt",   DEFAULT_STORY_PROMPT)

    log(f"\n[1/3] 生成【{theme}】题材脑洞...")
    premise = _generate_premise(client, model, theme, premise_prompt)
    log(f"🎯 脑洞：{premise}\n")

    log("[2/3] 生成8步大纲...")
    outline = _generate_outline(client, model, premise)
    log(outline)

    log("\n[3/3] 撰写正文小说...")
    story = _generate_story(client, model, outline, story_prompt)
    log(story)

    with open(INPUT_FILE, "w", encoding="utf-8") as f:
        f.write("【AI生成的绝妙脑洞】\n" + premise + "\n\n")
        f.write("【爽文正文】\n" + story + "\n")

    log(f"\n✅ 小说已保存至 {INPUT_FILE}")
    return INPUT_FILE


# ─────────────────────────────────────────────────────────────
#  步骤 2：生成语音
# ─────────────────────────────────────────────────────────────

def _extract_story(text: str) -> str:
    marker = "【爽文正文】"
    if marker in text:
        text = text.split(marker, 1)[1]
    return text.strip()


def _split_paragraphs(text: str):
    parts = re.split(r"\n\s*\n", text)
    return [p.strip() for p in parts if len(p.strip()) > 5]


def _call_tts(text: str, index: int):
    payload = {"text": text, **VOICE_CONFIG}
    r = requests.post(TTS_API_URL, json=payload, timeout=60)
    if r.status_code == 200:
        path = os.path.join(AUDIO_DIR, f"{index:03d}.mp3")
        with open(path, "wb") as f:
            f.write(r.content)
        log(f"  ✓ {path}")
    else:
        log(f"  ✗ TTS 失败 (段落 {index}): {r.text[:120]}")


def run_audio(cfg: dict = None):
    """将 output.txt 转为语音，输出到 audio/"""
    cfg = cfg or {}
    delay = int(cfg.get("tts_delay", 10))

    check_assets_for_audio()

    # 清空旧文件
    if os.path.exists(AUDIO_DIR):
        old = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]
        for f in old:
            os.remove(os.path.join(AUDIO_DIR, f))
        if old:
            log(f"🗑 已清空 audio/ 下 {len(old)} 个旧文件")
    os.makedirs(AUDIO_DIR, exist_ok=True)

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"找不到 {INPUT_FILE}，请先执行 run_novel()")

    text = open(INPUT_FILE, encoding="utf-8").read()
    text = _extract_story(text)
    paragraphs = _split_paragraphs(text)
    log(f"\n共 {len(paragraphs)} 段，开始 TTS 转换...")

    for i, p in enumerate(paragraphs):
        log(f"[{i+1}/{len(paragraphs)}] {p[:50]}...")
        _call_tts(p, i)
        if i < len(paragraphs) - 1:
            log(f"  等待 {delay}s...")
            time.sleep(delay)

    log(f"\n✅ 所有音频已生成到 {AUDIO_DIR}/")
    return AUDIO_DIR


# ─────────────────────────────────────────────────────────────
#  步骤 3：生成视频
# ─────────────────────────────────────────────────────────────

def _merge_audio_files():
    files = sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")])
    if not files:
        raise FileNotFoundError(f"{AUDIO_DIR}/ 下没有 .mp3 文件，请先执行 run_audio()")
    with open(AUDIO_LIST, "w", encoding="utf-8") as f:
        for fn in files:
            f.write(f"file '{AUDIO_DIR}/{fn}'\n")
    _run_cmd(f'ffmpeg -y -f concat -safe 0 -i {AUDIO_LIST} -c copy {MERGED_AUDIO}')
    return _get_duration(MERGED_AUDIO)


def _build_video_list(target_duration: float):
    videos = [v for v in os.listdir(VIDEO_DIR) if v.endswith(".mp4")]
    if not videos:
        raise FileNotFoundError(f"{VIDEO_DIR}/ 下没有 .mp4 文件")
    total = 0.0
    with open(VIDEO_LIST, "w", encoding="utf-8") as f:
        while total < target_duration:
            v = random.choice(videos)
            path = os.path.join(VIDEO_DIR, v)
            dur = _get_duration(path)
            total += dur
            f.write(f"file '{path}'\n")
    log(f"  视频素材拼接时长: {total:.1f}s（目标 {target_duration:.1f}s）")


def _merge_video_files():
    _run_cmd(f'ffmpeg -y -f concat -safe 0 -i {VIDEO_LIST} -c copy temp_video.mp4')


def _build_final_video(bgm_vol: float = 0.08, voice_vol: float = 1.8):
    # 竖屏 9:16 → 1080x1920，居中裁剪
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    cmd = (
        'ffmpeg -y -stream_loop -1 -i bgm.mp3 '
        f'-i {MERGED_AUDIO} '
        '-i temp_video.mp4 '
        f'-filter_complex '
        f'"[0:a]volume={bgm_vol}[bgm];'
        f'[1:a]volume={voice_vol}[voice];'
        f'[voice][bgm]amix=inputs=2:duration=first[a];'
        f'[2:v]{vf}[v]" '
        '-map "[v]" -map "[a]" '
        '-shortest -c:v libx264 -preset fast -crf 23 output.mp4'
    )
    _run_cmd(cmd)


def run_video(cfg: dict = None):
    """合并音频 + 视频素材，输出 output.mp4（竖屏 9:16）"""
    cfg = cfg or {}
    bgm_vol   = float(cfg.get("bgm_vol",   0.08))
    voice_vol = float(cfg.get("voice_vol", 1.8))

    check_assets_for_video()

    log("\n🎵 合并配音文件...")
    duration = _merge_audio_files()
    log(f"  音频总时长: {duration:.1f}s")

    log("\n🎞 生成随机视频列表...")
    _build_video_list(duration)

    log("\n🔗 拼接视频素材...")
    _merge_video_files()

    log("\n🎬 合成最终视频（竖屏 9:16）...")
    _build_final_video(bgm_vol, voice_vol)

    log("\n✅ 完成！输出文件：output.mp4")
    return "output.mp4"


# ─────────────────────────────────────────────────────────────
#  CLI 入口
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="重生爽文全自动流水线")
    parser.add_argument("--all",   action="store_true", help="执行全部三步")
    parser.add_argument("--novel", action="store_true", help="仅步骤1：生成小说")
    parser.add_argument("--audio", action="store_true", help="仅步骤2：生成语音")
    parser.add_argument("--video", action="store_true", help="仅步骤3：生成视频")
    parser.add_argument("--theme", default="随机猎奇",  help="小说题材（默认随机）")
    parser.add_argument("--bgm-vol",   type=float, default=0.08, help="背景音乐音量（默认0.08）")
    parser.add_argument("--voice-vol", type=float, default=1.8,  help="人声音量（默认1.8）")
    parser.add_argument("--tts-delay", type=int,   default=10,   help="TTS请求间隔秒数（默认10）")
    args = parser.parse_args()

    cfg = {
        "bgm_vol":   args.bgm_vol,
        "voice_vol": args.voice_vol,
        "tts_delay": args.tts_delay,
        # API 信息从环境变量读取
        "api_key":  os.environ.get("OPENAI_API_KEY",  ""),
        "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "model":    os.environ.get("OPENAI_MODEL",    "gpt-4o"),
    }

    do_novel = args.all or args.novel
    do_audio = args.all or args.audio
    do_video = args.all or args.video

    if not any([do_novel, do_audio, do_video]):
        parser.print_help()
        return

    if do_novel:
        run_novel(args.theme, cfg)
    if do_audio:
        run_audio(cfg)
    if do_video:
        run_video(cfg)


if __name__ == "__main__":
    main()
