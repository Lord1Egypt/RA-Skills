#!/usr/bin/env python3
"""
中文简繁转换工具
使用 opencc-python-reimplemented 进行本地转换
"""

import argparse
import sys
import json

# 延迟导入，避免未安装时报错
def get_converter():
    try:
        from opencc import OpenCC
        return OpenCC
    except ImportError:
        print("错误：未安装 opencc 库")
        print("请运行：pip install opencc-python-reimplemented")
        sys.exit(1)

def convert_text(text: str, direction: str = "t2s") -> str:
    """
    转换中文文本
    
    Args:
        text: 要转换的文本
        direction: 转换方向
            - t2s: 繁体转简体 (默认)
            - s2t: 简体转繁体
            - t2tw: 繁体转台湾正体
            - t2hk: 繁体转香港繁体
    
    Returns:
        转换后的文本
    """
    OpenCC = get_converter()
    cc = OpenCC(direction)
    return cc.convert(text)

def main():
    parser = argparse.ArgumentParser(description="中文简繁转换工具")
    parser.add_argument("text", nargs="?", help="要转换的文本")
    parser.add_argument("-d", "--direction", default="t2s", 
                        choices=["t2s", "s2t", "t2tw", "t2hk"],
                        help="转换方向: t2s繁转简, s2t简转繁, t2tw繁转台湾, t2hk繁转香港")
    parser.add_argument("-j", "--json", action="store_true", help="JSON输出")
    
    args = parser.parse_args()
    
    if not args.text:
        if not sys.stdin.isatty():
            args.text = sys.stdin.read().strip()
        else:
            print("错误：请提供要转换的文本")
            sys.exit(1)
    
    result = convert_text(args.text, args.direction)
    
    if args.json:
        output = {
            "success": True,
            "direction": args.direction,
            "original": args.text,
            "converted": result
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(result)

if __name__ == "__main__":
    main()
