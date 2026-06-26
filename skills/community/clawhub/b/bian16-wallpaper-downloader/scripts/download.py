#!/usr/bin/env python3
"""
彼岸图网 4K 壁纸批量下载脚本

功能：
1. 从手机壁纸分类页抓取详情页列表
2. 通过登录 cookie 调用下载 API 获取 4K 原图
3. 验证分辨率，自动跳过非 4K
4. 支持自定义间隔避免触发限制
5. 自动补齐到目标数量

用法：
  python3 download.py --cookie "COOKIE_STRING" --count 20 --interval 180 --outdir /data/wallpapers/anime/bian16

参数：
  --cookie    彼岸图网登录 cookie（必填）
  --count     下载数量（默认 20）
  --interval  每张间隔秒数（默认 180，即 3 分钟）
  --outdir    保存目录（默认 /data/wallpapers/anime/bian16）
  --category  分类路径（默认 shoujibizhi，即手机壁纸）
  --min-width 最小宽度阈值（默认 2000，低于此视为非 4K）
  --pages     最大扫描页数（默认 20）
"""

import argparse
import json
import os
import re
import time
import urllib.request


def parse_args():
    p = argparse.ArgumentParser(description="彼岸图网 4K 壁纸批量下载")
    p.add_argument("--cookie", required=True, help="彼岸图网登录 cookie 字符串")
    p.add_argument("--count", type=int, default=20, help="下载数量（默认 20）")
    p.add_argument("--interval", type=int, default=180, help="每张间隔秒数（默认 180）")
    p.add_argument("--outdir", default="/data/wallpapers/anime/bian16", help="保存目录")
    p.add_argument("--category", default="shoujibizhi", help="分类路径（默认 shoujibizhi）")
    p.add_argument("--min-width", type=int, default=2000, help="最小宽度阈值（默认 2000）")
    p.add_argument("--pages", type=int, default=20, help="最大扫描页数（默认 20）")
    return p.parse_args()


def make_headers(cookie, referer="https://pic.netbian.com/"):
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": referer,
        "Cookie": cookie,
    }


def fetch(url, headers, timeout=30):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def get_jpeg_real_size(data):
    """获取 JPEG 图片的实际分辨率（取最后一个 SOF 标记）"""
    last_w, last_h = None, None
    i = 0
    while i < len(data) - 1:
        if data[i] == 0xFF and data[i + 1] in (0xC0, 0xC1, 0xC2):
            h = (data[i + 5] << 8) | data[i + 6]
            w = (data[i + 7] << 8) | data[i + 8]
            last_w, last_h = w, h
        i += 1
    return last_w, last_h


def collect_detail_ids(base_headers, category, max_pages, existing_ids):
    """从分类页面收集详情页 ID"""
    detail_ids = []
    for page in range(1, max_pages + 1):
        if len(detail_ids) >= 200:
            break

        if page == 1:
            url = f"https://pic.netbian.com/{category}/"
        else:
            url = f"https://pic.netbian.com/{category}/index_{page}.html"

        try:
            html = fetch(url, base_headers, timeout=15).decode("gbk", errors="ignore")
        except Exception as e:
            print(f"  页面 {page} 获取失败: {e}")
            continue

        links = re.findall(r'href="(/tupian/(\d+)\.html)"', html)
        for _, tid in links:
            if tid not in existing_ids and tid not in detail_ids:
                detail_ids.append(tid)

        print(f"  页面 {page}: 累计 {len(detail_ids)} 个新 ID")

    return detail_ids


def download_4k_image(tid, base_headers, outdir, min_width):
    """下载单张 4K 原图，返回 (success, width, height, size_bytes)"""
    detail_url = f"https://pic.netbian.com/tupian/{tid}.html"

    # Step 1: 获取下载 token
    token_url = f"https://pic.netbian.com/e/extend/netbiandownload.php?id={tid}&t={time.time()}"
    try:
        token_data = fetch(token_url, {**base_headers, "Referer": detail_url})
        token_json = json.loads(token_data)
    except Exception as e:
        return False, None, None, 0, f"token 获取失败: {e}"

    if "pic" not in token_json or not token_json["pic"]:
        return False, None, None, 0, f"无 token: {token_json.get('msg', 'unknown')}"

    # Step 2: 用 token 下载 4K 原图
    pic_url = f"https://pic.netbian.com{token_json['pic']}"
    try:
        img_data = fetch(pic_url, {**base_headers, "Referer": detail_url})
    except Exception as e:
        return False, None, None, 0, f"下载失败: {e}"

    # Step 3: 验证分辨率
    w, h = get_jpeg_real_size(img_data)
    if not w or w < min_width:
        return False, w, h, len(img_data), f"分辨率不足: {w}x{h}"

    # Step 4: 保存文件
    filepath = os.path.join(outdir, f"{tid}_4k.jpg")
    with open(filepath, "wb") as f:
        f.write(img_data)

    return True, w, h, len(img_data), "OK"


def main():
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    base_headers = make_headers(args.cookie)

    # 扫描已有文件
    existing_ids = set()
    for f in os.listdir(args.outdir):
        if f.endswith(".jpg"):
            tid = f.replace("_4k.jpg", "")
            existing_ids.add(tid)

    need = args.count - len(existing_ids)
    if need <= 0:
        print(f"已有 {len(existing_ids)} 张，目标 {args.count} 张，无需下载")
        return

    print(f"已有: {len(existing_ids)} 张, 还需: {need} 张")
    print(f"分类: {args.category}, 间隔: {args.interval}s, 最小宽度: {args.min_width}px")
    print()

    # 收集 ID
    print("扫描分类页...")
    detail_ids = collect_detail_ids(base_headers, args.category, args.pages, existing_ids)
    print(f"共找到 {len(detail_ids)} 个新 ID\n")

    if not detail_ids:
        print("未找到新的壁纸 ID")
        return

    # 逐张下载
    downloaded = 0
    skipped = 0
    errors = 0

    print(f"开始下载 {need} 张 4K 壁纸 (间隔 {args.interval}s)...")
    eta_min = need * args.interval // 60
    print(f"预计耗时: ~{eta_min} 分钟\n")

    for tid in detail_ids:
        if downloaded >= need:
            break

        success, w, h, size, msg = download_4k_image(
            tid, base_headers, args.outdir, args.min_width
        )

        if success:
            downloaded += 1
            size_mb = size / 1024 / 1024
            print(f"[{downloaded}/{need}] {tid}: {w}x{h} ({size_mb:.1f}MB) - {time.strftime('%H:%M:%S')}")

            if downloaded < need:
                next_t = time.strftime("%H:%M", time.localtime(time.time() + args.interval))
                print(f"  下一张 ~{next_t}...")
                time.sleep(args.interval)
        else:
            if "分辨率不足" in msg:
                skipped += 1
            else:
                errors += 1
                print(f"  跳过 {tid}: {msg}")
            time.sleep(5)  # 失败后短暂等待

    total = len(existing_ids) + downloaded
    print(f"\n完成！本次下载: {downloaded} 张, 跳过: {skipped}, 错误: {errors}")
    print(f"总计: {total} 张 -> {args.outdir}")


if __name__ == "__main__":
    main()
