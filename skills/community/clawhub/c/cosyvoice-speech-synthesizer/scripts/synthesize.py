#!/usr/bin/env python3
"""
CosyVoice 语音合成脚本
调用阿里云百炼 CosyVoice API 将文本转换为音频文件
支持从自然语言描述中自动提取 instruction 指令
"""

import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse

import requests


# API 端点
API_ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer"


# Instruction 提取规则
INSTRUCTION_PATTERNS = {
    # 方言模式
    "dialect": {
        "patterns": [
            (r"使用?([\u4e00-\u9fa5]{2,3})话?", "请用{0}表达"),
            (r"用([\u4e00-\u9fa5]{2,3})话?", "请用{0}表达"),
            (r"([\u4e00-\u9fa5]{2,3})话?版本?", "请用{0}表达"),
            (r"([\u4e00-\u9fa5]{2,3})口音", "请用{0}表达"),
        ],
        "keywords": {
            "广东": "广东话", "粤语": "广东话", "广州": "广东话",
            "四川": "四川话", "川普": "四川话",
            "东北": "东北话",
            "上海": "上海话", "沪语": "上海话",
            "北京": "北京话", "京腔": "北京话",
            "湖南": "湖南话", "长沙": "湖南话",
            "湖北": "湖北话", "武汉": "湖北话",
            "河南": "河南话",
            "山东": "山东话",
            "陕西": "陕西话", "西安": "陕西话",
            "台湾": "台湾话", "闽南": "台湾话",
        }
    },
    # 情感模式
    "emotion": {
        "patterns": [
            (r"([\u4e00-\u9fa5]{2,4})地(说|讲|表达|念)", "请用{0}的语气说"),
            (r"(非常|很|特别)?([\u4e00-\u9fa5]{2,4})地(说|讲|表达|念)", "请用{1}的语气说"),
            (r"([\u4e00-\u9fa5]{2,4})的(语气|口吻|感觉|情绪)", "请用{0}的语气说"),
            (r"(显得|表现|带着)([\u4e00-\u9fa5]{2,4}).*?(说|讲|表达)", "请用{1}的语气说"),
        ],
        "keywords": {
            "开心": "开心", "高兴": "开心", "快乐": "开心", "愉快": "开心", "欢乐": "开心",
            "生气": "生气", "愤怒": "生气", "气愤": "生气", "恼火": "生气",
            "温柔": "温柔", "柔和": "温柔", "轻柔": "温柔", "轻声": "温柔", "温婉": "温柔",
            "悲伤": "悲伤", "难过": "悲伤", "伤心": "悲伤", "哀伤": "悲伤",
            "严肃": "严肃", "认真": "严肃", "庄重": "严肃",
            "幽默": "幽默", "搞笑": "幽默", "诙谐": "幽默",
            "亲切": "亲切", "热情": "亲切", "友好": "亲切",
            "紧张": "紧张", "焦急": "紧张", "着急": "紧张",
            "兴奋": "兴奋", "激动": "兴奋", "亢奋": "兴奋",
            "平静": "平静", "冷静": "平静", "淡定": "平静",
            "撒娇": "撒娇", "可爱": "撒娇", "卖萌": "撒娇",
            "威严": "威严", "霸气": "威严", "庄重": "威严",
        }
    },
    # 角色模式
    "role": {
        "patterns": [
            (r"像([\u4e00-\u9fa5]{2,4})一样", "请像{0}一样讲解"),
            (r"([\u4e00-\u9fa5]{2,4})的(语气|口吻|风格|方式)", "请像{0}一样讲解"),
            (r"模仿([\u4e00-\u9fa5]{2,4})", "请像{0}一样讲解"),
            (r"扮演([\u4e00-\u9fa5]{2,4})", "请像{0}一样讲解"),
        ],
        "keywords": {
            "老师": "老师", "教师": "老师", "教授": "老师",
            "播音员": "播音员", "主持人": "播音员", "主播": "播音员", "主播": "播音员",
            "小孩": "小孩", "儿童": "小孩", "孩子": "小孩", "小朋友": "小孩",
            "老人": "老人", "老爷爷": "老人", "老奶奶": "老人",
            "客服": "客服", "服务员": "客服",
            "领导": "领导", "老板": "领导", "上司": "领导",
            "朋友": "朋友", "闺蜜": "朋友", "兄弟": "朋友",
            "医生": "医生", "护士": "医生",
            "律师": "律师",
            "销售": "销售", "推销员": "销售",
            "导游": "导游",
            "新闻": "新闻主播", "记者": "新闻主播",
            "诗朗诵": "诗人", "朗诵": "诗人", "诗人": "诗人",
            "讲故事": "讲故事的人", "故事": "讲故事的人",
        }
    },
    # 风格模式
    "style": {
        "patterns": [
            (r"([\u4e00-\u9fa5]{2,4})地(说|讲|表达|念)", "请{0}地表达"),
            (r"(用|以)?([\u4e00-\u9fa5]{2,4})的(方式|风格|语气)", "请{1}地表达"),
        ],
        "keywords": {
            "正式": "正式", "官方": "正式", "规范": "正式",
            "随意": "随意", "轻松": "随意", "休闲": "随意",
            "专业": "专业", "内行": "专业",
            "通俗": "通俗", "易懂": "通俗", "简单": "通俗",
            "文艺": "文艺", "诗意": "文艺",
            "商务": "商务", "职场": "商务",
            "日常": "日常", "生活化": "日常",
        }
    }
}


def extract_instruction(text: str) -> tuple:
    """
    从自然语言描述中提取 instruction 指令和纯文本内容
    
    Args:
        text: 用户输入的完整文本
        
    Returns:
        (instruction, clean_text): 提取的指令和清理后的文本
    """
    instruction = None
    clean_text = text
    
    # 按优先级检查各类模式
    for category, config in INSTRUCTION_PATTERNS.items():
        # 先检查关键词匹配
        for keyword, mapped_value in config["keywords"].items():
            if keyword in text:
                if category == "dialect":
                    instruction = f"请用{mapped_value}表达"
                elif category == "emotion":
                    instruction = f"请用{mapped_value}的语气说"
                elif category == "role":
                    instruction = f"请像{mapped_value}一样讲解"
                elif category == "style":
                    instruction = f"请{mapped_value}地表达"
                
                # 尝试移除描述性前缀
                clean_text = remove_instruction_prefix(text, keyword, category)
                return instruction, clean_text
        
        # 再检查正则模式
        for pattern, template in config["patterns"]:
            match = re.search(pattern, text)
            if match:
                # 提取匹配的内容
                groups = match.groups()
                if groups:
                    # 根据模板中的占位符索引决定使用哪些组
                    import re as re_module
                    # 找出模板中所有的占位符，如 {0}, {1}
                    placeholders = re_module.findall(r'\{(\d+)\}', template)
                    if placeholders:
                        # 根据占位符索引提取对应的组
                        values = []
                        for idx in placeholders:
                            idx = int(idx)
                            if idx < len(groups):
                                # 如果组为None或空字符串，尝试找下一个非空组
                                val = groups[idx]
                                if not val and idx + 1 < len(groups):
                                    val = groups[idx + 1]
                                values.append(val if val else "")
                            else:
                                values.append("")
                        instruction = template.format(*values)
                    else:
                        # 没有占位符，直接使用第一个组
                        extracted = groups[0] if groups[0] else (groups[1] if len(groups) > 1 else groups[-1])
                        instruction = template.format(extracted)
                    clean_text = remove_instruction_prefix(text, match.group(0), category)
                    return instruction, clean_text
    
    return instruction, clean_text


def remove_instruction_prefix(text: str, matched_text: str, category: str) -> str:
    """
    从文本中移除 instruction 描述部分，保留纯内容
    
    Args:
        text: 原始文本
        matched_text: 匹配到的 instruction 描述
        category: 类别
        
    Returns:
        清理后的文本
    """
    # 常见的指令前缀模式
    prefix_patterns = [
        rf"使用?{matched_text}[:：]?",
        rf"用{matched_text}[:：]?",
        rf"以{matched_text}[:：]?",
        rf"{matched_text}[:：]?",
        rf"请{matched_text}[:：]?",
        r"^(使用?|用|以)?[\u4e00-\u9fa5]{2,4}话?[:：]",
        r"^(像[\u4e00-\u9fa5]{2,4}一样)[:：]?",
        r"^[\u4e00-\u9fa5]{2,4}地(说|讲|表达|念)[:：]?",
    ]
    
    clean_text = text
    for pattern in prefix_patterns:
        clean_text = re.sub(pattern, "", clean_text, flags=re.IGNORECASE)
    
    # 清理多余的标点符号和空格
    clean_text = clean_text.strip(" ：:").strip()
    
    # 如果清理后为空，返回原始文本
    if not clean_text:
        clean_text = text
    
    return clean_text


def get_api_key():
    """从环境变量获取 API Key"""
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误: 未设置 DASHSCOPE_API_KEY 环境变量", file=sys.stderr)
        print("请设置: export DASHSCOPE_API_KEY='your-api-key'", file=sys.stderr)
        sys.exit(1)
    return api_key


def synthesize(
    text: str,
    voice: str = "longanhuan",
    model: str = "cosyvoice-v3-flash",
    format: str = "wav",
    sample_rate: int = 24000,
    volume: int = 50,
    rate: float = 1.0,
    pitch: float = 1.0,
    instruction: str = None,
    enable_ssml: bool = False,
    seed: int = None,
    word_timestamp_enabled: bool = False,
    hot_fix: str = None,
    enable_markdown_filter: bool = False,
    auto_extract_instruction: bool = True,
    stream: bool = False,
    api_key: str = None
) -> dict:
    """
    调用 CosyVoice API 进行语音合成

    Args:
        text: 待合成文本
        voice: 音色名称
        model: 模型名称
        format: 音频格式 (pcm/wav/mp3/opus)
        sample_rate: 采样率 (8000-48000 Hz)
        volume: 音量 (0-100)
        rate: 语速 (0.5-2.0)
        pitch: 音高 (0.5-2.0)
        instruction: 控制方言/情感/角色 (≤100字符，仅部分音色支持)
        enable_ssml: 是否开启 SSML
        seed: 随机种子 (0-65535)
        word_timestamp_enabled: 是否开启字级时间戳
        hot_fix: 文本热修复（仅复刻音色）
        enable_markdown_filter: Markdown 过滤（仅复刻音色）
        auto_extract_instruction: 是否自动从文本中提取 instruction
        stream: 是否使用流式输出
        api_key: API Key（如为 None 则从环境变量获取）

    Returns:
        API 响应字典
    """
    if api_key is None:
        api_key = get_api_key()

    # 自动提取 instruction
    extracted_instruction = None
    clean_text = text
    if auto_extract_instruction and not instruction:
        extracted_instruction, clean_text = extract_instruction(text)
        if extracted_instruction:
            instruction = extracted_instruction
            print(f"  自动提取指令: {instruction}")
            print(f"  合成文本: {clean_text}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    if stream:
        headers["X-DashScope-SSE"] = "enable"

    # 构建 payload
    payload = {
        "model": model,
        "input": {
            "text": clean_text,
            "voice": voice,
            "format": format,
            "sample_rate": sample_rate
        },
        "parameters": {}
    }

    # 添加可选参数
    params = payload["parameters"]
    
    if volume != 50:
        params["volume"] = volume
    if rate != 1.0:
        params["rate"] = rate
    if pitch != 1.0:
        params["pitch"] = pitch
    if instruction:
        params["instruction"] = instruction
    if enable_ssml:
        params["enable_ssml"] = enable_ssml
    if seed is not None:
        params["seed"] = seed
    if word_timestamp_enabled:
        params["word_timestamp_enabled"] = word_timestamp_enabled
    if hot_fix:
        params["hot_fix"] = hot_fix
    if enable_markdown_filter:
        params["enable_markdown_filter"] = enable_markdown_filter

    # 如果没有参数，删除 parameters 字段
    if not params:
        del payload["parameters"]

    try:
        response = requests.post(
            API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=300
        )
        response.raise_for_status()

        if stream:
            # 流式输出：解析 SSE 数据，获取最后一条消息
            lines = response.text.strip().split('\n')
            last_data = None
            for line in lines:
                if line.startswith('data:'):
                    data_str = line[5:].strip()
                    try:
                        data = json.loads(data_str)
                        if data.get("output", {}).get("finish_reason") == "stop":
                            last_data = data
                    except json.JSONDecodeError:
                        continue
            return last_data or {}
        else:
            return response.json()

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"解析响应失败: {e}", file=sys.stderr)
        sys.exit(1)


def download_audio(url: str, output_path: str) -> bool:
    """
    下载音频文件

    Args:
        url: 音频文件 URL
        output_path: 保存路径

    Returns:
        是否下载成功
    """
    try:
        response = requests.get(url, timeout=120, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return True
    except requests.exceptions.RequestException as e:
        print(f"下载音频失败: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="CosyVoice 语音合成工具 - 支持智能 instruction 提取",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
智能 Instruction 提取示例:
  # 自动识别方言
  python synthesize.py --text "使用广东话合成：我想吃干炒牛河" --output cantonese.wav
  
  # 自动识别情感
  python synthesize.py --text "开心地说：今天天气真好！" --output happy.wav
  
  # 自动识别角色
  python synthesize.py --text "像老师一样：同学们上课了" --output teacher.wav

常规用法示例:
  # 基本用法
  python synthesize.py --text "你好，世界！" --output hello.wav

  # 调整语速和音量
  python synthesize.py --text "你好！" --rate 1.2 --volume 80 --output hello.wav

  # 手动指定 instruction
  python synthesize.py --text "今天天气真不错！" --instruction "请用温柔的语气说" --output gentle.wav

  # 使用流式输出
  python synthesize.py --text "流式合成测试" --output stream.wav --stream
        """
    )

    parser.add_argument(
        "--text",
        required=True,
        help="待合成的文本内容（支持自然语言描述，如'使用广东话合成：...'）"
    )
    parser.add_argument(
        "--voice",
        default="longanhuan",
        help="音色名称 (默认: longanhuan)"
    )
    parser.add_argument(
        "--model",
        default="cosyvoice-v3-flash",
        help="模型名称 (默认: cosyvoice-v3-flash)"
    )
    parser.add_argument(
        "--format",
        default="wav",
        choices=["wav", "mp3", "pcm", "opus"],
        help="音频格式 (默认: wav)"
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=24000,
        help="采样率 Hz，范围 8000-48000 (默认: 24000)"
    )
    parser.add_argument(
        "--volume",
        type=int,
        default=50,
        help="音量，范围 0-100 (默认: 50)"
    )
    parser.add_argument(
        "--rate",
        type=float,
        default=1.0,
        help="语速，范围 0.5-2.0 (默认: 1.0)"
    )
    parser.add_argument(
        "--pitch",
        type=float,
        default=1.0,
        help="音高，范围 0.5-2.0 (默认: 1.0)"
    )
    parser.add_argument(
        "--instruction",
        help="手动指定控制方言/情感/角色的指令 (≤100字符，仅部分音色支持)"
    )
    parser.add_argument(
        "--no-auto-extract",
        action="store_true",
        help="禁用自动提取 instruction 功能"
    )
    parser.add_argument(
        "--enable-ssml",
        action="store_true",
        help="开启 SSML 支持"
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="随机种子，范围 0-65535"
    )
    parser.add_argument(
        "--word-timestamp",
        action="store_true",
        dest="word_timestamp_enabled",
        help="开启字级时间戳"
    )
    parser.add_argument(
        "--hot-fix",
        help="文本热修复（仅复刻音色）"
    )
    parser.add_argument(
        "--enable-markdown-filter",
        action="store_true",
        help="开启 Markdown 过滤（仅复刻音色）"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="输出文件路径"
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="使用流式输出模式"
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="只打印音频 URL，不下载文件"
    )

    args = parser.parse_args()

    # 调用 API
    print(f"正在合成语音...")
    print(f"  原始文本: {args.text}")
    
    # 预检查是否能提取 instruction
    auto_extract = not args.no_auto_extract and not args.instruction
    if auto_extract:
        extracted_instruction, clean_text = extract_instruction(args.text)
        if extracted_instruction:
            print(f"  自动提取指令: {extracted_instruction}")
            print(f"  合成文本: {clean_text}")
        else:
            print(f"  合成文本: {args.text}")
    else:
        print(f"  合成文本: {args.text}")
        if args.instruction:
            print(f"  手动指令: {args.instruction}")
    
    print(f"  音色: {args.voice}")
    print(f"  模型: {args.model}")
    print(f"  格式: {args.format}")
    print(f"  采样率: {args.sample_rate} Hz")
    print(f"  音量: {args.volume}")
    print(f"  语速: {args.rate}")
    print(f"  音高: {args.pitch}")
    if args.enable_ssml:
        print(f"  SSML: 开启")
    if args.seed is not None:
        print(f"  随机种子: {args.seed}")
    if args.word_timestamp_enabled:
        print(f"  字级时间戳: 开启")
    if args.hot_fix:
        print(f"  热修复: {args.hot_fix}")
    if args.enable_markdown_filter:
        print(f"  Markdown 过滤: 开启")
    if args.stream:
        print(f"  模式: 流式输出")
    print()

    result = synthesize(
        text=args.text,
        voice=args.voice,
        model=args.model,
        format=args.format,
        sample_rate=args.sample_rate,
        volume=args.volume,
        rate=args.rate,
        pitch=args.pitch,
        instruction=args.instruction,
        enable_ssml=args.enable_ssml,
        seed=args.seed,
        word_timestamp_enabled=args.word_timestamp_enabled,
        hot_fix=args.hot_fix,
        enable_markdown_filter=args.enable_markdown_filter,
        auto_extract_instruction=auto_extract,
        stream=args.stream
    )

    if not result:
        print("合成失败: 未获取到有效响应", file=sys.stderr)
        sys.exit(1)

    # 检查响应状态
    output = result.get("output", {})
    finish_reason = output.get("finish_reason")

    if finish_reason != "stop":
        print(f"合成未完成，状态: {finish_reason}", file=sys.stderr)
        print(f"完整响应: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    # 获取音频信息
    audio_info = output.get("audio", {})
    audio_url = audio_info.get("url")
    audio_id = audio_info.get("id")
    expires_at = audio_info.get("expires_at")
    request_id = result.get("request_id")
    usage = result.get("usage", {})
    characters = usage.get("characters", 0)

    print(f"合成成功!")
    print(f"  请求 ID: {request_id}")
    print(f"  音频 ID: {audio_id}")
    print(f"  字符数: {characters}")
    if expires_at:
        from datetime import datetime
        expire_time = datetime.fromtimestamp(expires_at)
        print(f"  URL 过期时间: {expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    if args.no_download:
        print(f"音频 URL: {audio_url}")
    else:
        print(f"正在下载音频到: {args.output}")
        if download_audio(audio_url, args.output):
            # 获取文件大小
            file_size = os.path.getsize(args.output)
            print(f"下载完成!")
            print(f"  文件路径: {os.path.abspath(args.output)}")
            print(f"  文件大小: {file_size / 1024:.2f} KB")
        else:
            print(f"下载失败，但音频 URL 仍然有效（24小时内）:")
            print(f"  {audio_url}")
            sys.exit(1)


if __name__ == "__main__":
    main()
