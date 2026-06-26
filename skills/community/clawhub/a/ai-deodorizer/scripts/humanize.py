#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ai-Deodorizer 核心脚本 - 两轮改写去味工具

作者: xx235300
功能: 调用 LLM API 对 AI 生成的文本进行两轮改写，去除"AI味"

环境变量配置:
    API_KEY      - 你的 API Key（必填）
    API_BASE     - API 基础地址（可选，默认 https://api.minimaxi.chat）
    MODEL        - 模型名称（可选，默认 MiniMax-M2.7）

使用方法:
    # 设置环境变量
    export MINIMAX_API_KEY="your_api_key_here"

    # 基本用法
    python humanize.py --input "你的AI文本..."

    # 从文件读取
    python humanize.py --file input.txt

    # 指定输出文件
    python humanize.py --input "文本" --output result.txt

    # 指定去味强度
    python humanize.py --input "文本" --mode strong
"""

import argparse
import os
import sys

import requests

# =============================================================================
# 常量配置（可通过环境变量覆盖）
# =============================================================================

API_KEY = os.environ.get("MINIMAX_API_KEY", "")
API_BASE = os.environ.get("API_BASE", "https://api.minimaxi.chat")
MODEL = os.environ.get("MODEL", "MiniMax-M2.7")

# 第一轮改写 Prompt（模式修复）
PROMPT_ROUND1 = """你是一个文字编辑，负责将AI生成的文本改写得更自然、更像人类书写。

你的任务：
1. 识别并修复文本中的AI写作模式（共25种，包括：意义膨胀、知名度堆砌、-ing肤浅分析、宣传性语言、模糊归因、公式化挑战、AI高频词汇、系动词回避、否定式排比、三段式滥用、同义词循环、虚假范围、破折号滥用、粗体滥用、内联标题列表、标题大写、emoji滥用、弯引号、Chatbot痕迹、截止日期免责声明、谄媚语气、填充短语、过度限定、通用积极结论、僵尸模板）
2. 用自然表达替换AI模式
3. 保留原文的核心信息和基本结构
4. 保持原有语气（正式/口语/技术性）

禁止：
- 不要添加任何你自己的观点
- 不要改变原文的事实内容
- 不要简化内容让文章变短
- 不要在结尾添加总结性废话

请直接输出去味后的文本，不需要解释你做了什么修改。"""

# 第二轮改写 Prompt（Anti-AI Audit）
PROMPT_ROUND2 = """请完成以下两步：

第一步：快速浏览以下文本，列出它最明显的一到两个"AI味"特征（是什么让它看起来像AI写的？）。回答要简短。

第二步：根据第一步的答案，将文本改写，让它明显不再是AI写的。

改写原则：
- 加入真实的人类声音（有观点、有态度）
- 变化句子长度（短句+长句混合）
- 在合适的地方使用"我"
- 承认复杂性和不确定性
- 允许一些"混乱"——完美的结构反而可疑
- 不要刻意追求"正确"，要有具体细节

直接输出去味后的文本。"""

# 去味强度对应的 API 参数
MODE_PARAMS = {
    "light": {
        "temperature": 0.3,
        "top_p": 0.5,
    },
    "medium": {
        "temperature": 0.5,
        "top_p": 0.7,
    },
    "strong": {
        "temperature": 0.7,
        "top_p": 0.9,
    },
}


# =============================================================================
# LLM API 调用
# =============================================================================

def call_llm_api(prompt: str, text: str, mode: str = "medium") -> str:
    """
    调用 LLM API 进行文本改写。

    Args:
        prompt: 改写提示词
        text: 待改写的文本
        mode: 去味强度 (light/medium/strong)

    Returns:
        改写后的文本

    Raises:
        ValueError: 输入为空或 API Key 未设置
        RuntimeError: API 调用失败
    """
    if not API_KEY:
        raise ValueError("未设置 API Key 环境变量，请设置 MINIMAX_API_KEY 或其他兼容 API。")

    if not text or not text.strip():
        raise ValueError("输入文本为空，请提供有效内容。")

    # 获取强度参数
    params = MODE_PARAMS.get(mode, MODE_PARAMS["medium"])

    # 构建消息内容
    messages = [
        {"role": "user", "content": f"{prompt}\n\n待改写文本：\n{text}"}
    ]

    # 构造 API 请求
    url = f"{API_BASE}/v1/text/chatcompletion_v2"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": params["temperature"],
        "top_p": params["top_p"],
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
    except requests.exceptions.Timeout:
        raise RuntimeError("API 请求超时（超过120秒），请检查网络连接后重试。")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("网络连接失败，请检查网络状态后重试。")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"网络请求异常: {e}")

    # 检查 HTTP 状态码
    if response.status_code != 200:
        try:
            error_detail = response.json()
            error_msg = error_detail.get("base_resp", {}).get("status_msg", response.text)
        except Exception:
            error_msg = response.text
        raise RuntimeError(f"API 返回错误 (HTTP {response.status_code}): {error_msg}")

    # 解析响应
    try:
        result = response.json()
    except Exception:
        raise RuntimeError(f"API 响应格式异常，无法解析 JSON: {response.text}")

    # 提取生成的文本
    try:
        choices = result.get("choices", [])
        if not choices:
            raise RuntimeError(f"API 返回空 choices，原始响应: {result}")
        generated_text = choices[0].get("message", {}).get("content", "")
        if not generated_text:
            raise RuntimeError(f"API 返回空内容，原始响应: {result}")
        return generated_text.strip()
    except (IndexError, KeyError) as e:
        raise RuntimeError(f"解析 API 响应失败: {e}，原始响应: {result}")


def humanize_text_round1(text: str, mode: str = "medium") -> str:
    """第一轮改写：模式修复"""
    return call_llm_api(PROMPT_ROUND1, text, mode)


def humanize_text_round2(text: str, mode: str = "medium") -> str:
    """第二轮改写：Anti-AI Audit"""
    return call_llm_api(PROMPT_ROUND2, text, mode)


def humanize(text: str, mode: str = "medium") -> str:
    """
    对文本进行两轮去味改写。

    Args:
        text: 原始 AI 生成文本
        mode: 去味强度 (light/medium/strong)

    Returns:
        去味后的文本
    """
    # 第一轮：修复 AI 写作模式
    round1_result = humanize_text_round1(text, mode)
    # 第二轮：Anti-AI Audit，消除残留 AI 特征
    round2_result = humanize_text_round2(round1_result, mode)
    return round2_result


# =============================================================================
# 命令行界面
# =============================================================================

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        prog="humanize",
        description="Ai-Deodorizer: 对 AI 文本进行两轮去味改写",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
去味强度说明:
  light   - 轻度改写，保留更多原文风格
  medium  - 中度改写，平衡自然度与信息保留（默认）
  strong  - 深度改写，最大程度消除 AI 特征

示例:
  python humanize.py --input "这是一个AI生成的段落..."
  python humanize.py --file input.txt --output result.txt
  python humanize.py --file input.txt --mode strong
  cat input.txt | python humanize.py --file /dev/stdin
        """,
    )

    # 输入来源（互斥）
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--input", "-i",
        metavar="TEXT",
        help="直接传入待去味的文本内容",
    )
    input_group.add_argument(
        "--file", "-f",
        metavar="PATH",
        help="从指定文件读取文本内容（支持 - 读取标准输入）",
    )

    # 可选参数
    parser.add_argument(
        "--output", "-o",
        metavar="PATH",
        help="输出结果到指定文件（不指定则打印到 stdout）",
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["light", "medium", "strong"],
        default="medium",
        help="去味强度（默认: medium）",
    )

    return parser.parse_args()


def read_input(args):
    """
    根据命令行参数读取输入文本。
    """
    if args.input is not None:
        return args.input

    path = args.file
    try:
        if path == "-":
            text = sys.stdin.read()
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

        if not text.strip():
            raise ValueError(f"文件内容为空: {path}")
        return text

    except FileNotFoundError:
        raise ValueError(f"文件不存在: {path}")
    except UnicodeDecodeError:
        raise ValueError(f"文件编码错误，请确保文件为 UTF-8 编码: {path}")
    except OSError as e:
        raise ValueError(f"读取文件失败: {e}")


def write_output(text: str, output_path: str = None):
    """输出结果。"""
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"去味结果已保存到: {output_path}", file=sys.stderr)
        except OSError as e:
            raise ValueError(f"写入文件失败: {e}")
    else:
        print(text)


# =============================================================================
# 主入口
# =============================================================================

def main():
    """主函数"""
    args = parse_args()

    # 读取输入
    try:
        input_text = read_input(args)
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    # 执行两轮去味
    try:
        result = humanize(input_text, args.mode)
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: 未知异常 ({type(e).__name__}): {e}", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    try:
        write_output(result, args.output)
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
