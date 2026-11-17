#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器 Cookie 管理器
从主流浏览器读取指定域名的 Cookie
"""

import sys
import json
import argparse
from typing import Optional, Dict, Any

# 检查依赖
try:
    from rookiepy import chrome, edge, firefox, brave, opera, opera_gx, vivaldi, librewolf, arc, chromium
except ImportError as e:
    print(f"错误: 缺少必要的依赖库")
    print(f"请安装: pip install rookiepy")
    sys.exit(1)


# 浏览器映射
BROWSER_MAP = {
    "chrome": chrome,
    "edge": edge,
    "firefox": firefox,
    "brave": brave,
    "opera": opera,
    "opera-gx": opera_gx,
    "vivaldi": vivaldi,
    "librewolf": librewolf,
    "arc": arc,
    "chromium": chromium,
}


def format_cookie_header(cookies: list) -> str:
    """将 Cookie 转换为 HTTP Header 格式"""
    cookie_pairs = []
    for cookie in cookies:
        if cookie.get('name') and cookie.get('value'):
            cookie_pairs.append(f"{cookie['name']}={cookie['value']}")
    return "; ".join(cookie_pairs)


def format_curl(cookies: list, url: str) -> str:
    """将 Cookie 转换为 cURL 格式"""
    cookie_header = format_cookie_header(cookies)
    return f'curl "{url}" -H "Cookie: {cookie_header}"'


def get_cookies(browser_name: str, domain: str) -> Optional[list]:
    """
    从指定浏览器获取指定域名的 Cookie

    Args:
        browser_name: 浏览器名称
        domain: 目标域名

    Returns:
        Cookie 列表，失败返回 None
    """
    browser_module = BROWSER_MAP.get(browser_name.lower())
    if not browser_module:
        print(f"错误: 不支持的浏览器 '{browser_name}'")
        print(f"支持的浏览器: {', '.join(BROWSER_MAP.keys())}")
        return None

    try:
        # 读取 Cookie
        cookies = browser_module.cookie(domain=domain)
        if not cookies:
            print(f"警告: 未找到 '{domain}' 的 Cookie")
            print("可能原因:")
            print("  1. 浏览器未访问过该域名")
            print("  2. Cookie 已被清除")
            print("  3. Linux 环境需要特殊权限")
            return []

        # 过滤有效的 Cookie
        valid_cookies = []
        for cookie in cookies:
            if cookie.get('name') and cookie.get('value'):
                valid_cookies.append({
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': cookie.get('domain', ''),
                    'path': cookie.get('path', ''),
                    'expirationDate': cookie.get('expirationDate', None)
                })

        print(f"✓ 成功读取 {len(valid_cookies)} 个 Cookie")
        return valid_cookies

    except PermissionError:
        print("错误: 权限不足")
        print("Windows 系统: 请以管理员身份运行程序")
        print("Linux/macOS 系统: 检查文件权限")
        return None
    except Exception as e:
        print(f"错误: 读取 Cookie 失败: {e}")
        return None


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='浏览器 Cookie 管理器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --browser chrome --domain douyin.com
  %(prog)s --browser edge --domain tiktok.com --output-format cookie-header
  %(prog)s --browser firefox --domain xiaohongshu.com --output-file cookies.json
        """
    )
    parser.add_argument('--browser', required=True,
                       help='浏览器名称')
    parser.add_argument('--domain', required=True,
                       help='目标域名（如 douyin.com）')
    parser.add_argument('--output-format', default='json',
                       choices=['json', 'cookie-header', 'curl'],
                       help='输出格式（默认: json）')
    parser.add_argument('--output-file', '-o',
                       help='输出文件路径（可选）')

    args = parser.parse_args()

    # 获取 Cookie
    cookies = get_cookies(args.browser, args.domain)
    if cookies is None:
        sys.exit(1)

    if not cookies:
        print("没有找到 Cookie")
        sys.exit(0)

    # 格式化输出
    if args.output_format == 'json':
        output = json.dumps(cookies, ensure_ascii=False, indent=2)
        print("\n=== Cookie (JSON) ===")
    elif args.output_format == 'cookie-header':
        output = format_cookie_header(cookies)
        print("\n=== Cookie Header ===")
    elif args.output_format == 'curl':
        url = f"https://{args.domain}"
        output = format_curl(cookies, url)
        print("\n=== cURL Command ===")
    else:
        print(f"错误: 不支持的格式 '{args.output_format}'")
        sys.exit(1)

    print(output)

    # 写入文件
    if args.output_file:
        try:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n✓ Cookie 已保存到: {args.output_file}")
        except Exception as e:
            print(f"错误: 写入文件失败: {e}")


if __name__ == '__main__':
    main()
