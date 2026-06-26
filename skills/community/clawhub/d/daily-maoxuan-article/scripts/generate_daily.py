#!/usr/bin/env python3
"""
每日毛选语录配图生成脚本 v1.1
使用 Doubao-Seedream 模型生成配图
"""

import os
import sys
import json
import random
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# 基础路径
BASE_DIR = Path(__file__).parent.parent
QUOTES_FILE = BASE_DIR / "references" / "mao-quotes.md"


def load_quotes() -> List[str]:
    """加载语录列表"""
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    return [line.strip() for line in content.split('\n') if line.strip()]


def find_seedream_script() -> Optional[Path]:
    """查找 di-seedream-gen 的 generate_image.py"""
    candidates = [
        Path(os.environ.get("SEEDREAM_SCRIPT", "")),
        Path.home() / ".openclaw" / "skills" / "di-seedream-gen" / "scripts" / "generate_image.py",
        Path.home() / ".openclaw" / "workspace-imagor" / "skills" / "di-seedream-gen" / "scripts" / "generate_image.py",
        Path.home() / ".openclaw" / "workspace" / "skills" / "di-seedream-gen" / "scripts" / "generate_image.py",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def generate_prompt(quote: str) -> str:
    """根据语录生成图片提示词"""
    style_prompts = {
        "没有调查，就没有发言权。": "人文纪实摄影，乡村田埂上，干部和农民群众坐在一起亲切交谈，大家表情自然生动，真实自然不刻板，细节丰富，8k分辨率，人文纪实摄影",
        "实践是检验真理的唯一标准。": "历史纪实摄影，1978年农村打谷场，农民们围坐在一起讨论生产问题，光线柔和自然，真实还原时代氛围，细节丰富，8k分辨率",
        "星星之火，可以燎原。": "井冈山写实风光，夜晚山村油灯下，毛泽东坐在木板床上写文章，窗外是井冈山的松涛竹海，油灯灯光柔和，人物神情专注，真实自然，细节丰富，8k分辨率",
        "一切反动派都是纸老虎。": "延安窑洞内，毛泽东坐在土炕上和美国记者斯特朗谈话，窑洞光线从窗户照进来，光影斑驳，真实自然，细节丰富，8k分辨率",
        "自己动手，丰衣足食。": "延安南泥湾，八路军战士开垦荒地，战士们光着膀子流汗，脸上带着劳动的汗水，笑容真诚，真实劳动场景，细节丰富，8k分辨率",
        "好好学习，天天向上。": "明亮写实摄影，新中国乡村小学教室里，孩子们坐在木课桌前认真看书，阳光从窗户照进来，氛围积极阳光，真实自然，细节丰富，8k分辨率",
        "世上无难事，只要肯登攀。": "写实风光摄影，井冈山主峰，登山者沿着石阶攀登顶峰，云海在脚下翻腾，风光壮丽，细节丰富，8k分辨率",
        "独立自主，自力更生，艰苦奋斗，勤俭建国。": "新中国成立初期工业纪实，工厂车间里工人们忙碌工作，穿着工装神情专注认真，真实还原创业初期的奋斗场景，细节丰富，8k分辨率",
        "下定决心，不怕牺牲，排除万难，去争取胜利。": "抗日战争敌后战场，八路军战士深夜爬山行军，夜色朦胧，战士们神情坚毅，月光洒在脸上，氛围紧张真实，细节丰富，8k分辨率",
    }
    style = style_prompts.get(
        quote,
        "真实自然的纪实摄影，符合语录内容意境，人物表情生动自然不刻板，细节丰富，纹理清晰，自然柔和光影，8k分辨率，高质量专业摄影，无水印"
    )
    return f"根据语录'{quote}'生成意境相符的高质量写实摄影图片，{style}"


def main():
    parser = argparse.ArgumentParser(description="每日毛选语录配图生成")
    parser.add_argument("--output-dir", "-o", default=str(BASE_DIR / "temp" / "images"), help="输出目录")
    parser.add_argument("--size", "-s", default="2K", help="图片尺寸")
    parser.add_argument("--quote", "-q", help="指定语录，默认随机")
    parser.add_argument("--model", "-m", default="doubao-seedream-4-5-251128", help="模型 ID")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 加载语录
    quotes = load_quotes()
    if not quotes:
        print("❌ 语录文件为空")
        sys.exit(1)

    print(f"📚 语录数: {len(quotes)} 条")

    # 选择语录
    selected = args.quote if args.quote else random.choice(quotes)
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n📝 今日语录：{selected}")

    # 获取 API Key
    api_key = os.environ.get("SEEDREAM_API_KEY", "")
    if not api_key:
        print("❌ 未设置 SEEDREAM_API_KEY 环境变量")
        sys.exit(1)

    # 查找 Seedream 脚本
    script = find_seedream_script()
    if not script:
        print("❌ 找不到 di-seedream-gen 的 generate_image.py")
        print("   请设置 SEEDREAM_SCRIPT 环境变量指向该脚本")
        sys.exit(1)

    # 生成图片
    prompt = generate_prompt(selected)
    print(f"🎨 提示词: {prompt[:80]}...")

    output_file = output_dir / f"{today}.png"
    env = os.environ.copy()
    env["SEEDREAM_API_KEY"] = api_key

    cmd = [
        sys.executable, str(script),
        "--prompt", prompt,
        "--filename", str(output_file),
        "--size", args.size,
        "--model", args.model
    ]

    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=120)
        if result.returncode == 0 and output_file.exists():
            print(f"\n✅ 图片已保存: {output_file}")
        else:
            print(f"❌ 生成失败: {result.stderr[:300]}")
            sys.exit(1)
    except subprocess.TimeoutExpired:
        print("❌ 生成超时")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
