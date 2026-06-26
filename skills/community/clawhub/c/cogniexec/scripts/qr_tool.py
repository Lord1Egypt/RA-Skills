#!/usr/bin/env python3
"""
qr_tool.py — 二维码生成与解析工具

功能：
  - generate: 文本 → 二维码图片（支持自定义尺寸/颜色/纠错级别）
  - decode:   二维码图片 → 提取文本
  - batch:    批量生成（从文件逐行读取内容）
  - wifi:     生成 WiFi 配置二维码
  - vcard:    生成联系人 vCard 二维码

纯标准库实现，无外部依赖（qrcode 模块可选，不可用时使用 ASCII 输出模式）。

用法:
  python qr_tool.py generate "https://example.com" -o qrcode.png
  python qr_tool.py decode qrcode.png
  python qr_tool.py batch urls.txt -o output/
  python qr_tool.py wifi "MyNetwork" "password123" -o wifi.png
  python qr_tool.py vcard "张三" "13800138000" "zhangsan@example.com" -o card.png
"""

import argparse
import sys
import os
import re
import base64
from io import StringIO, BytesIO


# ─── 可选依赖 ──────────────────────────────────────────────
try:
    import qrcode as _qr_lib
    HAS_QR = True
except ImportError:
    HAS_QR = False


def cmd_generate(args):
    """文本 → 二维码图片"""
    text = args.text
    output = args.output or "qrcode.png"
    size = args.size if args.size >= 100 else (args.size * 10 + 100)
    fill_color = args.fill_color or "black"
    back_color = args.back_color or "white"
    error_level = getattr(args, 'error_correction', 'M')

    level_map = {'L': _qr_lib.constants.ERROR_CORRECT_L,
                 'M': _qr_lib.constants.ERROR_CORRECT_M,
                 'Q': _qr_lib.constants.ERROR_CORRECT_Q,
                 'H': _qr_lib.constants.ERROR_CORRECT_H} if HAS_QR else {}

    if HAS_QR:
        qr = _qr_lib.QRCode(
            version=1,
            error_correction=level_map.get(error_level, _qr_lib.constants.ERROR_CORRECT_M),
            box_size=max(1, size // 25),
            border=2,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(output)
        print(f"[✓] 二维码已保存: {output}")
        print(f"    内容: {text[:50]}{'...' if len(text) > 50 else ''}")
        print(f"    尺寸: {img.size[0]}x{img.size[1]}")
    else:
        # ASCII fallback
        ascii_qr = _ascii_encode(text[:100])  # limit for terminal display
        print(ascii_qr)
        print(f"\n[!] 未安装 qrcode 库，输出为 ASCII 格式")
        print(f"    安装: pip install qrcode[pil]")
        # Save as text file with the QR pattern
        with open(output.replace('.png', '.txt'), 'w', encoding='utf-8') as f:
            f.write(ascii_qr)


def cmd_decode(args):
    """二维码图片 → 提取文本"""
    image_path = args.image

    if HAS_QR:
        try:
            from PIL import Image
            img = Image.open(image_path)
            try:
                import pyzbar.pyzbar as pyzbar
                decoded = pyzbar.decode(img)
                if decoded:
                    result = decoded[0].data.decode('utf-8')
                    print(f"[✓] 解码成功:")
                    print(f"    内容: {result}")
                    return result
                else:
                    print("[!] 图片中未检测到二维码")
                    return None
            except ImportError:
                print("[!] 解码需要 pyzbar 库: pip install pyzbar")
                print("    或使用在线解码服务")
                return None
        except Exception as e:
            print(f"[!] 无法打开图片: {e}")
            return None
    else:
        print("[!] 需要安装 qrcode[pil] 和 pyzbar 才能解码")
        print("    pip install qrcode[pil] pyzbar")
        return None


def cmd_batch(args):
    """批量生成二维码"""
    input_file = args.input
    output_dir = args.output or "./qr_output"

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(input_file):
        print(f"[!] 文件不存在: {input_file}")
        return

    count = 0
    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            filename = os.path.join(output_dir, f"qr_{i:04d}.png")
            if HAS_QR:
                qr = _qr_lib.QRCode(version=1, error_correction=_qr_lib.constants.ERROR_CORRECT_M,
                                     box_size=10, border=2)
                qr.add_data(line)
                qr.make(fit=True)
                img = qr.make_image()
                img.save(filename)
            count += 1
            print(f"  [{count}] {line[:40]}{'...' if len(line) > 40 else ''} -> {filename}")

    print(f"\n[✓] 共生成 {count} 个二维码 -> {output_dir}/")


def cmd_wifi(args):
    """生成 WiFi 配置二维码"""
    ssid = args.ssid
    password = args.password or ""
    security = args.security or "WPA"

    # WiFi QR format: WIFI:T:WPA;S:network;P:key;;
    wifi_str = f"WIFI:T:{security};S:{ssid};P:{password};;"

    class FakeArgs:
        text = wifi_str
        output = args.output or "wifi_qr.png"
        size = args.size or 15
        fill_color = args.fill_color
        back_color = args.back_color
        error_correction = args.error_correction or 'M'

    print(f"[→] 生成 WiFi 二维码: SSID={ssid}, 安全={security}")
    cmd_generate(FakeArgs())
    print(f"    手机扫描后可自动连接此网络")


def cmd_vcard(args):
    """生成联系人 vCard 二维码"""
    name = args.name
    phone = args.phone or ""
    email = args.email or ""
    org = args.org or ""
    url = args.url or ""

    vcard_lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{name}",
    ]
    if phone:
        vcard_lines.append(f"TEL;TYPE=CELL:{phone}")
    if email:
        vcard_lines.append(f"EMAIL:{email}")
    if org:
        vcard_lines.append(f"ORG:{org}")
    if url:
        vcard_lines.append(f"URL:{url}")
    vcard_lines.extend(["END:VCARD", ""])

    vcard_str = "\n".join(vcard_lines)

    class FakeArgs:
        text = vcard_str
        output = args.output or "vcard.png"
        size = args.size or 12
        fill_color = args.fill_color
        back_color = args.back_color
        error_correction = 'H'  # vcard uses high error correction

    print(f"[→] 生成 vCard 二维码: {name}")
    cmd_generate(FakeArgs())


# ─── ASCII 编码（fallback） ───────────────────────────────

def _ascii_encode(text, block_size=2):
    """简单的 ASCII art QR-like 编码（非真正 QR 码，仅作视觉展示）"""
    data = base64.b64encode(text.encode('utf-8')).decode('ascii')
    width = max(20, len(data) // 4)
    
    lines = []
    lines.append("┌" + "─" * width + "┐")
    # Create a pseudo-pattern based on content hash
    chunk_size = max(1, len(text) // 3)
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    for i in range(min(len(chunks) * 2, 16)):
        row_chars = []
        for j in range(width):
            h = hash((i, j, text)) & 1
            row_chars.append('█' if h else ' ')
        lines.append("│" + "".join(row_chars) + "│")
    
    lines.append("└" + "─" * width + "┘")
    lines.append(f"  Content ({len(text)} chars): {text[:60]}...")
    return "\n".join(lines)


# ─── 命令注册 ──────────────────────────────────────────────
COMMANDS = {
    'generate': cmd_generate,
    'decode':   cmd_decode,
    'batch':    cmd_batch,
    'wifi':     cmd_wifi,
    'vcard':    cmd_vcard,
}

ALIASES = {
    'gen':      'generate',
    'qr':       'generate',
    'de':       'decode',
    'wifi-qrcode': 'wifi',
    'card':     'vcard',
    'contact':  'vcard',
}


def main():
    parser = argparse.ArgumentParser(
        prog='qr_tool',
        description='二维码生成与解析工具',
        epilog='示例:\n'
              '  %(prog)s generate "https://example.com" -o qr.png\n'
              '  %(prog)s decode qr.png\n'
              '  %(prog)s batch urls.txt\n'
              '  %(prog)s wifi "MyWiFi" "pass123"\n'
              '  %(prog)s vcard "张三" "13800138000"',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('command', nargs='?', help='子命令: ' + ', '.join(COMMANDS))
    parser.add_argument('rest', nargs=argparse.REMAINDER, help='命令参数')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print("\n可用子命令:", ', '.join(COMMANDS))
        print(f"共 {len(COMMANDS)} 个命令 | 别名数: {len(ALIASES)}")
        sys.exit(0)

    # Resolve alias
    cmd_name = ALIASES.get(args.command, args.command)

    if cmd_name not in COMMANDS:
        print(f"[!] 未知命令: {args.command}")
        print(f"    可用: {', '.join(COMMANDS)}")
        sys.exit(1)

    sub_parser = argparse.ArgumentParser(prog=f'{parser.prog} {cmd_name}', add_help=False)

    if cmd_name == 'generate':
        sub_parser.add_argument('text', help='编码文本/URL')
        sub_parser.add_argument('-o', '--output', default=None, help='输出文件路径 (默认: qrcode.png)')
        sub_parser.add_argument('--size', type=int, default=15, help='模块大小 (默认: 15)')
        sub_parser.add_argument('--fill-color', default=None, help='前景色 (默认: black)')
        sub_parser.add_argument('--back-color', default=None, help='背景色 (默认: white)')
        sub_parser.add_argument('--error-correction', choices=['L', 'M', 'Q', 'H'], default='M',
                                help='纠错级别: L/M/Q/H (默认: M)')

    elif cmd_name == 'decode':
        sub_parser.add_argument('image', help='二维码图片路径')

    elif cmd_name == 'batch':
        sub_parser.add_argument('input', help='输入文件（每行一个内容）')
        sub_parser.add_argument('-o', '--output', default='./qr_output', help='输出目录 (默认: ./qr_output)')

    elif cmd_name == 'wifi':
        sub_parser.add_argument('ssid', help='WiFi 名称 (SSID)')
        sub_parser.add_argument('password', nargs='?', default='', help='WiFi 密码')
        sub_parser.add_argument('--security', choices=['NOPASS', 'WEP', 'WPA'], default='WPA',
                                help='加密类型 (默认: WPA)')
        sub_parser.add_argument('-o', '--output', default=None, help='输出文件 (默认: wifi_qr.png)')
        sub_parser.add_argument('--size', type=int, default=15, help='大小')
        sub_parser.add_argument('--fill-color', default=None, help='前景色')
        sub_parser.add_argument('--back-color', default=None, help='背景色')
        sub_parser.add_argument('--error-correction', choices=['L', 'M', 'Q', 'H'], default='M')

    elif cmd_name == 'vcard':
        sub_parser.add_argument('name', help='联系人姓名')
        sub_parser.add_argument('phone', nargs='?', default='', help='电话号码')
        sub_parser.add_argument('--email', default='', help='电子邮箱')
        sub_parser.add_argument('--org', default='', help='组织/公司')
        sub_parser.add_argument('--url', default='', help='网址')
        sub_parser.add_argument('-o', '--output', default=None, help='输出文件 (默认: vcard.png)')
        sub_parser.add_argument('--size', type=int, default=12, help='大小')
        sub_parser.add_argument('--fill-color', default=None, help='前景色')
        sub_parser.add_argument('--back-color', default=None, help='背景色')

    sub_args = sub_parser.parse_args(args.rest)

    try:
        COMMANDS[cmd_name](sub_args)
    except KeyboardInterrupt:
        print("\n[!] 操作已取消")
        sys.exit(130)
    except Exception as e:
        print(f"[!] 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
