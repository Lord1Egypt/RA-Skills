"""
提取字幕.py
对音频库中的 .m4a 文件用 Whisper 模型做语音识别，按视频标题命名为 Markdown，存放到 字幕文本/{博主}/{标题}.md。
并汇总每个博主的全部视频脚本到 字幕文本/{博主}.md。
已存在同名文件视为已处理并跳过。
"""

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd
import whisper
from dotenv import load_dotenv

from run_state import resolve_cleaned_files
from storage import AUDIO_DIR, MODEL_DIR, SUBTITLE_DIR
from utils import video_id_from_url

load_dotenv(Path(__file__).parent.parent / ".env")

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "medium")

_whisper_model = None


def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        MODEL_DIR.mkdir(exist_ok=True)
        model_file = MODEL_DIR / f"{WHISPER_MODEL}.pt"
        if not model_file.exists():
            print(f"  首次使用，下载 Whisper {WHISPER_MODEL} 模型到 models/ ...")
        else:
            print(f"  加载 Whisper 模型（{WHISPER_MODEL}，来自 models/）...")
        try:
            _whisper_model = whisper.load_model(WHISPER_MODEL, download_root=str(MODEL_DIR))
        except Exception as e:
            print(f"  Whisper 加载失败：{e}")
            if model_file.exists():
                print(f"  模型文件可能损坏，尝试删除后重新下载：")
                print(f"    del \"{model_file}\"")
            raise
    return _whisper_model


def load_title_map() -> dict:
    """从最新的 cleaned CSV 中构建 video_id -> (title, blogger) 映射（向量化）"""
    mapping = {}
    for csv_path in resolve_cleaned_files():
        try:
            df = pd.read_csv(csv_path, encoding="utf-8-sig")
        except Exception:
            continue
        if "链接" not in df.columns:
            continue
        df = df.copy()
        df["_vid"] = (
            df["链接"].astype(str).str.strip()
            .str.rstrip("/").str.split("/").str[-1]
            .str.split("?").str[0]
        )
        df = df[df["_vid"].str.len() > 0].drop_duplicates("_vid", keep="last")
        title_col   = next((c for c in ["标题", "视频标题"]  if c in df.columns), None)
        blogger_col = next((c for c in ["博主", "博主昵称"] if c in df.columns), None)
        titles   = df[title_col].astype(str).str.strip()   if title_col   else pd.Series("", index=df.index)
        bloggers = df[blogger_col].astype(str).str.strip() if blogger_col else pd.Series("", index=df.index)
        mapping.update(zip(df["_vid"], zip(titles, bloggers)))
    return mapping


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|]", "_", name).strip()
    name = re.sub(r"\s+", " ", name)
    return name[:150]


def process_video(audio_path: Path, title_map: dict, summary_index: dict):
    video_id = audio_path.stem
    blogger = audio_path.parent.name
    title, mapped_blogger = title_map.get(video_id, ("", ""))
    if mapped_blogger:
        blogger = mapped_blogger

    safe_title = sanitize_filename(title) if title else video_id
    blogger_dir = SUBTITLE_DIR / sanitize_filename(blogger or "未知博主")
    blogger_dir.mkdir(parents=True, exist_ok=True)
    out_path = blogger_dir / f"{video_id}.md"  # 文件名用 video_id，方便后续脚本稳定匹配

    if out_path.exists():
        print(f"  已存在，跳过：{blogger}/{video_id}")
        summary_index[blogger].append((safe_title, out_path))
        return

    print(f"识别：{audio_path.name} -> {blogger}/{video_id}.md")
    model = get_whisper_model()
    result = model.transcribe(str(audio_path), language="zh", fp16=False)
    lines = [seg["text"].strip() for seg in result["segments"] if seg["text"].strip()]

    # 首行写标题，方便人工阅读；正文为逐句识别结果
    content = (f"# {safe_title}\n\n" if safe_title != video_id else "") + "\n".join(lines)
    out_path.write_text(content, encoding="utf-8")
    print(f"  已保存：{out_path.name}，共 {len(lines)} 句")

    summary_index[blogger].append((safe_title, out_path))


def write_blogger_summaries(summary_index: dict):
    for blogger, items in summary_index.items():
        safe_blogger = sanitize_filename(blogger or "未知博主")
        summary_path = SUBTITLE_DIR / f"{safe_blogger}.md"
        parts = []
        for title, path in sorted(items, key=lambda x: x[0]):
            parts.append(f"## {title}\n")
            try:
                parts.append(Path(path).read_text(encoding="utf-8"))
            except Exception:
                parts.append("(读取字幕失败)\n")
            parts.append("\n\n")
        summary_path.write_text("".join(parts), encoding="utf-8")
        print(f"汇总：{summary_path}")


def run():
    SUBTITLE_DIR.mkdir(parents=True, exist_ok=True)
    audio_files = list(AUDIO_DIR.rglob("*.m4a"))

    if not audio_files:
        print("音频库/ 目录下没有找到音频文件")
        return

    title_map = load_title_map()
    summary_index: dict[str, list] = defaultdict(list)

    print(f"共找到 {len(audio_files)} 个音频")
    for af in audio_files:
        process_video(af, title_map, summary_index)

    write_blogger_summaries(summary_index)
    print("\n语音识别完成")


if __name__ == "__main__":
    run()
