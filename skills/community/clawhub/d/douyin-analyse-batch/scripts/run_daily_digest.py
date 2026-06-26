#!/usr/bin/env python3
"""
run_daily_digest.py — 抖音每日日报流水线
获取热榜TOP15 → OpenClaw LLM分析 → MD+DOCX → 邮件发送
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path

_HOME = Path.home()

# 当前脚本所在目录
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_BASE = SCRIPT_DIR.parent

ANALYSIS_DIR = SKILL_BASE          # douyin-daily-report 根目录
OUTPUT_DIR   = Path(os.environ.get('DOUYIN_OUTPUT_DIR', str(_HOME / 'Documents' / 'douyin_analysis')))
VENV_PY     = os.environ.get('DOUYIN_VENV_PY', '/tmp/douyin_transcribe/venv/bin/python3')
TIKHUB_API_BASE = 'https://api.tikhub.dev'

TMP_DIR = Path("/tmp/douyin_transcribe")
TMP_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_LIMIT = int(os.environ.get('DOUYIN_DIGEST_LIMIT', '15'))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ── OpenClaw LLM 分析 ────────────────────────────────────────────────────────

def call_openclaw_llm(title: str, transcript: str, video_url: str = "") -> str:
    """通过 openclaw agent 命令调用内置模型生成分析笔记"""
    session_key = "agent:main:lightclawbot:direct:100012167891"

    prompt = f"""你是一个专业的抖音视频内容分析师。请分析以下抖音视频并生成分析笔记。

【视频标题】{title}
【视频链接】{video_url or "无"}
【口播转写内容】
{transcript if transcript else "（无转写内容，仅根据标题和标签分析）"}

请生成以下格式的分析笔记，用中文回复，严格只输出分析笔记本身：

#### 1. 核心内容
- 

#### 2. 内容摘要
- 钩子：
- 核心主张：
- 论据支撑：

#### 3. 批判性分析
- 情绪钩子：
- 夸大之处：
- 幸存者偏差：
- 真正有价值的部分："""

    result = subprocess.run(
        ["openclaw", "agent",
         "--session-id", session_key,
         "--message", prompt,
         "--timeout", "90"],
        capture_output=True,
        text=True,
        timeout=120,
        env={**os.environ, "PATH": os.environ.get("PATH", "") + ":/root/.local/share/pnpm"}
    )

    answer_lines = []
    for line in result.stdout.splitlines():
        if line.strip() and not line.startswith("["):
            answer_lines.append(line)

    if answer_lines:
        return "\n".join(answer_lines).strip()
    return None


# ── TikHub API ────────────────────────────────────────────────────────────────

def get_tikhub_token():
    config_path = _HOME / ".openclaw" / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            cfg = json.load(f)
            token = cfg.get("tikhub_api_token", "")
            if token:
                return token
    raise RuntimeError("未配置 TikHub API Token，请先在 ~/.openclaw/config.json 中添加 tikhub_api_token")


def get_hot_videos_tikhub(limit: int = 15) -> list[dict]:
    """通过 TikHub 热榜 API 获取 TOP 视频"""
    import requests
    token = get_tikhub_token()
    url = f"{TIKHUB_API_BASE}/api/v1/douyin/billboard/fetch_hot_total_video_list"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"page": 1, "page_size": limit, "sub_type": 1001}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 200:
        raise RuntimeError(f"fetch_hot_total_video_list 失败: {data.get('message')}")
    inner = data.get("data", {})
    objs = inner.get("data", {}).get("objs", []) if isinstance(inner, dict) else []
    return objs


# ── 单视频处理 ────────────────────────────────────────────────────────────────

def analyze_one_video(video: dict, rank: int, skip_transcribe: bool) -> str:
    """处理单个视频：LLM分析 → 构造分析块"""
    item_id  = video.get('item_id', '')
    title    = video.get('item_title', '') or video.get('item_id', f'视频{item_id}')
    item_url = video.get('item_url', '')
    play_cnt = video.get('play_cnt', 0)
    like_cnt = video.get('like_cnt', 0)
    author   = video.get('nick_name', '未知作者')

    # 原生可打开的分享链接（稳定，不带时效token）
    share_url = f"https://www.douyin.com/video/{item_id}" if item_id else item_url

    header = (
        f"## 第 {rank} 条｜{title}\n\n"
        f"- 播放量：{play_cnt:,}\n"
        f"- 点赞量：{like_cnt:,}\n"
        f"- 作者：{author}\n"
    )
    if share_url:
        header += f"- 视频链接：{share_url}\n"
    header += "\n"

    transcript_text = ''
    transcript_note = '（已跳过转写，使用标题和标签分析）'

    body = "- 视频标题：" + title + "\n\n"
    body += "### 口播转写\n\n"
    body += transcript_note + "\n\n"

    # 调用 OpenClaw LLM 生成分析笔记
    llm_analysis = ""
    if title:
        try:
            llm_result = call_openclaw_llm(title, transcript_text, share_url)
            if llm_result:
                llm_analysis = "\n### 分析笔记\n\n" + llm_result + "\n\n---\n"
            else:
                llm_analysis = (
                    "\n### 分析笔记\n\n"
                    "#### 1. 核心内容\n- （LLM 分析生成失败）\n\n"
                    "---\n"
                )
        except Exception as e:
            llm_analysis = (
                f"\n### 分析笔记\n\n"
                f"#### 1. 核心内容\n- （LLM 调用异常：{str(e)[:100]}）\n\n"
                "---\n"
            )

    body += llm_analysis
    return header + body


# ── 日报汇总 ─────────────────────────────────────────────────────────────────

def build_toc(videos: list[dict]) -> str:
    rows = []
    for i, v in enumerate(videos, 1):
        title = v.get('item_title', v.get('item_id', f'视频{i}'))
        play  = v.get('play_cnt', 0)
        like  = v.get('like_cnt', 0)
        item_id = v.get('item_id', '')
        share_url = f"https://www.douyin.com/video/{item_id}" if item_id else v.get('item_url', '')
        rows.append(f"| {i} | {title} | {play:,} | {like:,} | {share_url} |")
    header = "| 排名 | 标题 | 播放量 | 点赞量 | 链接 |\n|------|------|--------|--------|------|\n"
    return header + '\n'.join(rows)


def write_daily_report(today: str, videos: list[dict], sections: list[str],
                       success_count: int) -> tuple[Path, Path]:
    now_str = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    file_path = OUTPUT_DIR / f"{today} 抖音热门视频日报.md"
    toc    = build_toc(videos)
    detail = '\n'.join(sections)

    content = f"""# 抖音热门视频日报 {today}

> 自动生成时间：{now_str}
> 热榜来源：TikHub 视频热榜（每日更新）
> 视频条目数：{len(videos)}，成功分析：{success_count}

---

## 热榜总览

{toc}

---

## 视频分析详情

{detail}
"""
    file_path.write_text(content, encoding='utf-8')

    # MD → DOCX
    docx_path = None
    try:
        # 用 venv Python 运行 md_to_docx（依赖 python-docx）
        p = subprocess.run(
            [VENV_PY, str(SCRIPT_DIR / 'helpers' / 'md_to_docx.py'), str(file_path)],
            capture_output=True, text=True, timeout=60
        )
        if p.returncode == 0:
            docx_path = file_path.with_suffix('.docx')
            print(f"[OK] Word 文档已生成: {docx_path}")
        else:
            print(f"[WARN] Word 文档生成失败: {p.stderr.strip()[:100]}", file=sys.stderr)
    except Exception as e:
        print(f"[WARN] Word 文档生成失败: {e}", file=sys.stderr)

    return file_path, docx_path


# ── 发邮件 ────────────────────────────────────────────────────────────────────

def send_email(note_path: Path, docx_path: Path, today: str, success_count: int):
    topic = f"{today}（共 {success_count} 条分析）"
    try:
        p = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / 'helpers' / 'send_email.py'),
             '--note-path', str(note_path),
             '--docx-path', str(docx_path) if docx_path else '',
             '--topic', topic],
            capture_output=True, text=True, timeout=60
        )
        if p.returncode == 0:
            print(f"[OK] 邮件已发送 → {os.environ.get('DOUYIN_EMAIL_RECIPIENTS', '')}")
        else:
            print(f"[WARN] 邮件发送失败: {p.stderr.strip()[:200]}", file=sys.stderr)
    except Exception as e:
        print(f"[WARN] 邮件发送异常: {e}", file=sys.stderr)


# ── 主入口 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='抖音每日日报生成')
    parser.add_argument('--limit', type=int, default=DEFAULT_LIMIT)
    parser.add_argument('--no-email', action='store_true')
    parser.add_argument('--skip-transcribe', action='store_true')
    args = parser.parse_args()

    today = dt.date.today().strftime('%Y-%m-%d')
    print(f"[START] 抖音热门视频日报 {today}，获取 TOP {args.limit}")

    # 步骤1：获取热榜
    try:
        videos = get_hot_videos_tikhub(args.limit)
        print(f"[OK] TikHub 热榜获取成功，共 {len(videos)} 条")
    except Exception as e:
        print(f"[ERROR] 热榜获取失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 步骤2：逐一分析
    sections = []
    success_count = 0
    for i, video in enumerate(videos):
        rank  = i + 1
        title = video.get('item_title', video.get('item_id', f'视频{rank}'))
        print(f'[{rank}/{len(videos)}] 分析：{title[:40]}')
        try:
            section = analyze_one_video(video, rank, skip_transcribe=args.skip_transcribe)
            sections.append(section)
            if 'LLM 分析生成失败' not in section and 'LLM 调用异常' not in section:
                success_count += 1
        except Exception as e:
            print(f'[WARN] 分析失败: {e}', file=sys.stderr)
            err_section = f"## 第 {rank} 条｜{title}\n\n### 获取失败\n\n```\n{str(e)[:200]}\n```\n\n---\n"
            sections.append(err_section)

    # 步骤3：写入日报（MD + DOCX）
    report_path, docx_path = write_daily_report(today, videos, sections, success_count)
    print(f'[OK] 日报已写入: {report_path}')

    # 步骤4：发送邮件
    if not args.no_email:
        send_email(report_path, docx_path, today, success_count)

    result = {
        'date': today,
        'report_path': str(report_path),
        'total': len(videos),
        'success': success_count,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
