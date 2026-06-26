#!/usr/bin/env python3
"""
Base64 编解码工具
纯 Python 标准库实现
"""

import base64
import argparse
import sys
import os


def encode_string(text: str) -> str:
    """将字符串编码为 Base64"""
    return base64.b64encode(text.encode('utf-8')).decode('ascii')


def decode_string(b64_text: str) -> str:
    """将 Base64 字符串解码为原始字符串"""
    try:
        return base64.b64decode(b64_text.encode('ascii')).decode('utf-8')
    except Exception as e:
        raise ValueError(f"解码失败: {e}")


def encode_file(input_path: str) -> str:
    """将文件内容编码为 Base64"""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"文件不存在: {input_path}")
    with open(input_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode('ascii')


def decode_file(b64_text: str, output_path: str) -> None:
    """将 Base64 内容解码写入文件"""
    data = base64.b64decode(b64_text.encode('ascii'))
    with open(output_path, 'wb') as f:
        f.write(data)


def main():
    parser = argparse.ArgumentParser(
        description='Base64 编解码工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s encode "Hello World"           编码字符串
  %(prog)s decode "SGVsbG8gV29ybGQ="       解码字符串
  %(prog)s encode_file image.png           编码文件
  %(prog)s decode_file output.b64 out.png  解码到文件
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # encode
    p_encode = subparsers.add_parser('encode', help='编码字符串为 Base64')
    p_encode.add_argument('text', help='要编码的字符串')

    # decode
    p_decode = subparsers.add_parser('decode', help='解码 Base64 字符串')
    p_decode.add_argument('text', help='要解码的 Base64 字符串')

    # encode_file
    p_encode_file = subparsers.add_parser('encode_file', help='将文件编码为 Base64')
    p_encode_file.add_argument('input', help='输入文件路径')
    p_encode_file.add_argument('-o', '--output', default='-', help='输出文件路径（默认 stdout）')

    # decode_file
    p_decode_file = subparsers.add_parser('decode_file', help='将 Base64 解码为文件')
    p_decode_file.add_argument('b64', help='Base64 字符串或文件')
    p_decode_file.add_argument('output', help='输出文件路径')

    args = parser.parse_args()

    if args.command == 'encode':
        print(encode_string(args.text))

    elif args.command == 'decode':
        print(decode_string(args.text))

    elif args.command == 'encode_file':
        result = encode_file(args.input)
        if args.output == '-':
            print(result)
        else:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"已保存到: {args.output}")

    elif args.command == 'decode_file':
        decode_file(args.b64, args.output)
        print(f"已保存到: {args.output}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
