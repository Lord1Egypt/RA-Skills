#!/usr/bin/env python3
"""
Content Producer v1.0 - 多平台内容分发器
标准付费版 ¥29.9

一次输入，自动适配小红书/知乎/公众号/抖音四种平台格式

用法:
  python3 content_producer.py --topic "你的主题" --platform xiaohongshu
  python3 content_producer.py --topic "AI工具" --platform all --output ./output

依赖:
  pip install requests pyyaml
  OpenAI API Key (或兼容API)
"""

import os
import sys
import json
import time
import argparse
import hashlib
from pathlib import Path
from datetime import datetime

VERSION = "1.0.0"

# ========== 配置 ==========

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE = os.environ.get("OPENAI_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")  # 便宜且够用

OUTPUT_DIR = Path(os.environ.get("CONTENT_OUTPUT_DIR", "./content_output"))

# ========== 平台配置 ==========

PLATFORMS = {
    "xiaohongshu": {
        "name": "小红书",
        "word_count": "300-800字",
        "style": "口语化、有温度、emoji点缀",
        "features": "标题要吸引、正文短段落、结尾引导互动、加标签",
        "price_guide": "种草文/测评/攻略"
    },
    "zhihu": {
        "name": "知乎",
        "word_count": "1000-2000字",
        "style": "专业、逻辑清晰、有数据支撑",
        "features": "直接回答问题、分点论述、引用案例/数据、结尾呼吁关注",
        "price_guide": "干货回答/行业分析"
    },
    "gongzhonghao": {
        "name": "公众号",
        "word_count": "1500-3000字",
        "style": "深度、有故事感、结构清晰",
        "features": "开头讲故事或痛点、分章节、金句收尾、引导转发",
        "price_guide": "深度文章/行业洞察"
    },
    "douyin": {
        "name": "抖音",
        "word_count": "200-500字 (口播脚本)",
        "style": "口语化、节奏快、钩子强",
        "features": "前3秒抓人、分段口播、视觉建议、结尾引导互动",
        "price_guide": "口播脚本/带货文案"
    }
}

# ========== Prompt 模板 ==========

PROMPT_TEMPLATES = {
    "xiaohongshu": """你是一个资深小红书内容运营专家。请根据以下信息生成一篇小红书笔记。

【主题】{topic}
【要点】{points_text}
【风格】{style}
【字数】{word_count}

要求：
1. 标题要吸引眼球，带数字或关键词
2. 正文用短段落，2-3句一段
3. 适当使用emoji增强可读性
4. 结尾要有互动引导
5. 最后附5-10个相关标签

直接输出完整笔记内容，不要额外解释。""",

    "zhihu": """你是一个知乎高赞回答作者。请根据以下信息写一篇知乎回答。

【问题/主题】{topic}
【核心观点】{points_text}
【风格】{style}
【字数】{word_count}

要求：
1. 开头直接亮出核心观点，建立专业感
2. 逻辑结构清晰，分点论述
3. 引用数据或案例支撑（可以合理推断）
4. 语言专业但不晦涩
5. 结尾简短呼吁关注/点赞

直接输出完整回答，不要额外解释。""",

    "gongzhonghao": """你是一个公众号资深撰稿人。请根据以下信息写一篇公众号文章。

【主题】{topic}
【核心内容】{points_text}
【风格】{style}
【字数】{word_count}

要求：
1. 开头用故事或痛点引入，建立共鸣
2. 主体分3-4个章节，每章有小标题
3. 内容有深度，有洞察
4. 语言流畅，金句点缀
5. 结尾有升华和引导转发

直接输出完整文章（Markdown格式），不要额外解释。""",

    "douyin": """你是一个抖音短视频脚本作者。请根据以下信息写一条短视频脚本。

【主题】{topic}
【核心卖点】{points_text}
【风格】{style}
【字数】{word_count}

要求：
1. 前3秒必须抓人（痛点/悬念/反差）
2. 口播节奏紧凑，不建议长句
3. 标注视觉建议 [画面: xxx]
4. 结尾引导互动（点赞/评论/关注）

输出格式：
---
【标题】xxx
【时长】xx秒
【脚本】
[画面] xxx
[口播] xxx
...
【文案】xxx
【标签】#xxx #xxx
---

直接输出脚本，不要额外解释。"""
}

# ========== 工具函数 ==========

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def ensure_dir(d):
    Path(d).mkdir(parents=True, exist_ok=True)

# ========== 核心功能 ==========

def generate_content(topic, points, platform, style="casual"):
    """调用LLM生成指定平台内容"""
    import requests

    if not OPENAI_API_KEY:
        log("❌ 未设置 OPENAI_API_KEY")
        return None

    # 构建要点文本
    if points:
        points_text = "\n".join([f"- {p}" for p in points])
    else:
        points_text = "请根据主题自行展开"

    cfg = PLATFORMS.get(platform)
    if not cfg:
        log(f"❌ 未知平台: {platform}")
        return None

    prompt = PROMPT_TEMPLATES[platform].format(
        topic=topic,
        points_text=points_text,
        style=style,
        word_count=cfg["word_count"]
    )

    log(f"  调用 {OPENAI_MODEL} 生成 {cfg['name']} 内容...")

    try:
        resp = requests.post(
            f"{OPENAI_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": "你是顶尖的中文自媒体内容创作者，精通各平台写作风格。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            },
            timeout=120
        )
        data = resp.json()
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
            log(f"  ✅ 生成完成 ({len(content)}字符)")
            return content
        else:
            err = data.get("error", {}).get("message", "未知错误")
            log(f"  ❌ API错误: {err}")
            return None
    except Exception as e:
        log(f"  ❌ 请求失败: {e}")
        return None


def save_content(topic, platform, content, output_dir):
    """保存生成的内容到文件"""
    if not content:
        return None

    plat_name = PLATFORMS[platform]["name"]
    safe_topic = topic.replace("/", "_").replace(" ", "_")[:30]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"[{plat_name}]_{safe_topic}_{timestamp}.md"
    filepath = output_dir / filename

    # 添加元数据头
    header = f"""---
title: {topic}
platform: {platform}
generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
model: {OPENAI_MODEL}
---

"""
    filepath.write_text(header + content, encoding="utf-8")
    log(f"  💾 已保存: {filepath}")
    return filepath


def generate_all_platforms(topic, points, style, output_dir):
    """一键生成所有平台"""
    results = {}
    for platform in PLATFORMS:
        log(f"\n--- {PLATFORMS[platform]['name']} ---")
        content = generate_content(topic, points, platform, style)
        if content:
            save_content(topic, platform, content, output_dir)
            results[platform] = content
        time.sleep(2)  # API限流保护
    return results


def list_history(output_dir):
    """列出所有已生成的内容"""
    files = sorted(output_dir.glob("*.md"))
    if not files:
        log("暂无历史记录")
        return

    log(f"\n📚 历史内容 ({len(files)}篇)")
    log("-" * 60)
    for f in files:
        size = f.stat().st_size
        modified = datetime.fromtimestamp(f.stat().st_mtime).strftime("%m-%d %H:%M")
        name = f.stem
        log(f"  {modified}  {size:>6}B  {name}")


# ========== 主流程 ==========

def main():
    parser = argparse.ArgumentParser(description=f"多平台内容分发器 v{VERSION}")
    parser.add_argument("--topic", required=True, help="内容主题")
    parser.add_argument("--points", help="要点列表，逗号分隔", default="")
    parser.add_argument("--platform", default="all",
                       choices=["all", "xiaohongshu", "zhihu", "gongzhonghao", "douyin"],
                       help="目标平台 (默认: all)")
    parser.add_argument("--style", default="casual",
                       choices=["professional", "casual", "educational", "promotional"],
                       help="写作风格")
    parser.add_argument("--output", default=None, help="输出目录")
    parser.add_argument("--history", action="store_true", help="查看历史记录")
    args = parser.parse_args()

    global OUTPUT_DIR
    if args.output:
        OUTPUT_DIR = Path(args.output)
    else:
        OUTPUT_DIR = OUTPUT_DIR / datetime.now().strftime("%Y%m%d")

    ensure_dir(OUTPUT_DIR)

    # 历史记录模式
    if args.history:
        list_history(OUTPUT_DIR)
        return

    log(f"{'='*50}")
    log(f"📝 多平台内容分发器 v{VERSION}")
    log(f"主题: {args.topic}")
    log(f"平台: {'全部' if args.platform == 'all' else PLATFORMS[args.platform]['name']}")
    log(f"风格: {args.style}")
    log(f"{'='*50}")

    points = [p.strip() for p in args.points.split(",") if p.strip()]

    if args.platform == "all":
        log(f"\n🎯 生成全部4个平台内容...")
        results = generate_all_platforms(args.topic, points, args.style, OUTPUT_DIR)
        success = sum(1 for v in results.values() if v)
        log(f"\n{'='*50}")
        log(f"✅ 完成！{success}/{len(PLATFORMS)} 个平台生成成功")
        log(f"📂 输出目录: {OUTPUT_DIR}")
    else:
        log(f"\n🎯 生成 {PLATFORMS[args.platform]['name']} 内容...")
        content = generate_content(args.topic, points, args.platform, args.style)
        if content:
            save_content(args.topic, args.platform, content, OUTPUT_DIR)
            log(f"\n{'='*50}")
            log(f"✅ 完成！")
            log(f"📂 输出目录: {OUTPUT_DIR}")
            print("\n" + content)

    log(f"\n💡 提示: 使用 --history 查看历史内容")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\n⚠️ 用户中断")
        sys.exit(1)
    except Exception as e:
        log(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
