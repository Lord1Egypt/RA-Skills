#!/usr/bin/env python3
"""
从浏览器提取 cookie 保存为 Netscape 格式文件.
由 bili_review.py 用 yt-dlp 自带 python 环境调用(内含 yt_dlp.cookies, 可解密各浏览器 cookie).
只保留 B 站相关域名的 cookie, 不导出其他网站.
用法: python3 extract_cookies.py <browser> <output_path>
"""
import sys

from yt_dlp.cookies import extract_cookies_from_browser

BILI_DOMAINS = ("bilibili.com", "b23.tv", "biligame.com", "bilibili.tv",
                "bstar.app", "biligame.net")


def main() -> None:
    if len(sys.argv) != 3:
        print("用法: extract_cookies.py <browser> <output_path>", file=sys.stderr)
        sys.exit(2)
    browser, output = sys.argv[1], sys.argv[2]
    jar = extract_cookies_from_browser(browser)

    filtered = type(jar)()
    for cookie in jar:
        domain = cookie.domain.lstrip(".")
        if any(domain == d or domain.endswith("." + d) for d in BILI_DOMAINS):
            filtered.set_cookie(cookie)

    filtered.save(output, ignore_discard=True, ignore_expires=True)
    print(f"已提取 {browser} cookie({len(filtered)}条, 仅B站) -> {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
