#!/usr/bin/env python3
"""
cn-ascii-art - ASCII艺术生成器
"""
import argparse
import sys

def try_import_pyfiglet():
    """尝试导入pyfiglet"""
    try:
        import pyfiglet
        return pyfiglet
    except ImportError:
        return None

def generate_ascii(text, font='standard'):
    """生成ASCII艺术"""
    pyfiglet = try_import_pyfiglet()
    
    if pyfiglet is None:
        # 降级方案：简单ASCII
        result = []
        for char in text.upper():
            result.append(char * 3)
        return '\n'.join(result)
    
    try:
        fig = pyfiglet.Figlet(font=font, direction='left-to-right')
        return fig.renderText(text)
    except:
        return text.upper()

def list_fonts():
    """列出可用字体"""
    pyfiglet = try_import_pyfiglet()
    
    if pyfiglet:
        fonts = pyfiglet.Figlet().getFonts()
        print("可用字体:")
        for i, font in enumerate(fonts[:20]):
            print(f"  {font}")
        if len(fonts) > 20:
            print(f"  ... 共{len(fonts)}个字体")
    else:
        print("pyfiglet未安装，使用简单模式")

def main():
    parser = argparse.ArgumentParser(description='ASCII艺术生成器')
    parser.add_argument('text', nargs='?', help='要转换的文本')
    parser.add_argument('--font', default='standard', help='字体样式')
    parser.add_argument('--list', action='store_true', help='列出可用字体')
    
    args = parser.parse_args()
    
    if args.list:
        list_fonts()
        return
    
    if not args.text:
        print("用法:")
        print("  python3 cn_ascii_art.py 'Hello'")
        print("  python3 cn_ascii_art.py '你好' --font banner")
        print("  python3 cn_ascii_art.py --list")
        return
    
    result = generate_ascii(args.text, args.font)
    print(result)

if __name__ == '__main__':
    main()