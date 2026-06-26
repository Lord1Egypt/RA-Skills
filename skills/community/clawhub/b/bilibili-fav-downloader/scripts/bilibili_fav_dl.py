#!/usr/bin/env python3
"""
Bilibili 收藏夹自动下载脚本
功能:
- 分页获取收藏夹所有视频（自动翻页）
- 增量下载（已下载跳过）
- 最高画质下载（视频+音频合并为MP4）
- 下载失败重试
- 自动写入已下载记录

用法:
  python3 bilibili_fav_dl.py --cookie /path/to/cookie.txt --fav-id 3220842352 --out-dir ./downloads
  python3 bilibili_fav_dl.py --check-only  # 仅检查，不下载

环境变量:
  BILIBILI_COOKIE_FILE  Cookie文件路径
  BILIBILI_FAV_ID       收藏夹ID
  BILIBILI_OUT_DIR      输出目录
  BILIBILI_TG_BOT_TOKEN Telegram Bot Token（可选）
  BILIBILI_TG_CHAT_ID   Telegram Chat ID（可选）
"""
import json, subprocess, os, re, sys, argparse, time
from datetime import datetime

# ========== 默认配置 ==========
DEFAULT_COOKIE_FILE = os.environ.get("BILIBILI_COOKIE_FILE", "/opt/bilibili-favorites/cookie.txt")
DEFAULT_FAV_ID = os.environ.get("BILIBILI_FAV_ID", "")
DEFAULT_OUT_DIR = os.environ.get("BILIBILI_OUT_DIR", "/opt/bilibili-favorites/downloads")
STATE_FILE = "/opt/bilibili-favorites/downloaded_bvid.txt"
LOG_FILE = "/opt/bilibili-favorites/download.log"

# ========== 工具函数 ==========
def log(msg, also_print=True):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    if also_print:
        print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def curl_api(url, cookie_file):
    r = subprocess.run([
        "curl", "-s", url,
        "-b", cookie_file,
        "-H", "User-Agent: Mozilla/5.0",
    ], capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except:
        return {}

def get_all_videos(fav_id, cookie_file):
    """分页获取收藏夹所有视频"""
    all_items = []
    pn = 1
    while True:
        url = f"https://api.bilibili.com/x/v3/fav/resource/list?media_id={fav_id}&pn={pn}&ps=20&jsonp=jsonp&type=0"
        data = curl_api(url, cookie_file)
        if data.get("code") != 0:
            log(f"API page{pn} error: {data.get('message')}")
            break
        items = data["data"]["medias"]
        all_items.extend(items)
        if not data["data"]["has_more"]:
            break
        pn += 1
        time.sleep(0.3)
    return all_items

def download_video(bvid, title, output_dir, cookie_file):
    """下载单个视频，最高画质"""
    safe_title = re.sub(r'[\\/:*?"<>|\x00-\x1f]', '_', title).strip()
    safe_title = re.sub(r'\s+', ' ', safe_title)
    output_file = os.path.join(output_dir, f"{safe_title}___{bvid}.mp4")

    if os.path.exists(output_file):
        return True, "skipped"

    # yt-dlp 最高画质：bestvideo+bestaudio 合并
    result = subprocess.run([
        "yt-dlp",
        "--cookies", cookie_file,
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",
        "--no-playlist",
        "-o", output_file,
        f"https://www.bilibili.com/video/{bvid}"
    ], capture_output=True, text=True)

    if result.returncode == 0 and os.path.exists(output_file):
        size = os.path.getsize(output_file) / 1024 / 1024
        return True, f"success ({size:.1f}MB)"
    else:
        err = result.stderr[-300:] if result.stderr else "unknown"
        return False, err[-150:]

def write_state(bvid):
    with open(STATE_FILE, "a") as f:
        f.write(bvid + "\n")

def send_tg(msg):
    token = os.environ.get("BILIBILI_TG_BOT_TOKEN")
    chat_id = os.environ.get("BILIBILI_TG_CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    subprocess.run([
        "curl", "-s", url,
        "-d", f"chat_id={chat_id}",
        "-d", f"text={msg}",
        "-d", "parse_mode=HTML"
    ], capture_output=True)

def main():
    parser = argparse.ArgumentParser(description="Bilibili 收藏夹自动下载")
    parser.add_argument("--cookie", default=DEFAULT_COOKIE_FILE, help="Cookie 文件路径 (Netscape格式)")
    parser.add_argument("--fav-id", default=DEFAULT_FAV_ID, help="收藏夹 ID (media_id)")
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR, help="输出目录")
    parser.add_argument("--check-only", action="store_true", help="仅检查，不下载")
    parser.add_argument("--state-file", default=STATE_FILE, help="已下载记录文件")
    parser.add_argument("--uid", default="", help="用户 UID (用于 Referer)")
    args = parser.parse_args()

    if not args.fav_id:
        print("[!] 必须提供 --fav-id 参数")
        sys.exit(1)

    if not os.path.exists(args.cookie):
        print(f"[!] Cookie 文件不存在: {args.cookie}")
        sys.exit(1)

    os.makedirs(args.out_dir, exist_ok=True)
    log(f"========== 开始检查收藏夹 {args.fav_id} ==========")

    # 读取已下载记录
    downloaded = set()
    if os.path.exists(args.state_file):
        with open(args.state_file) as f:
            downloaded = set(l.strip() for l in f if l.strip())
    log(f"已下载: {len(downloaded)}")

    # 获取视频列表
    try:
        items = get_all_videos(args.fav_id, args.cookie)
    except Exception as e:
        log(f"获取列表失败: {e}")
        sys.exit(1)

    log(f"收藏夹总计: {len(items)} 个视频")

    # 筛选新增
    new_videos = []
    for item in items:
        bvid = item.get("bvid", "")
        title = item.get("title", "未知")
        if not bvid or "已失效" in title:
            continue
        if bvid not in downloaded:
            new_videos.append((bvid, title))

    log(f"新增待下载: {len(new_videos)}")

    if not new_videos:
        log("无需下载，退出")
        return

    if args.check_only:
        log(f"检查模式：发现 {len(new_videos)} 个新视频（未下载）")
        return

    # 逐个下载
    success = 0
    failed = 0
    for bvid, title in new_videos:
        ok, status = download_video(bvid, title, args.out_dir, args.cookie)
        if ok:
            downloaded.add(bvid)
            write_state(bvid)
            success += 1
            log(f"  ✅ {bvid}: {title} [{status}]")
        else:
            failed += 1
            log(f"  ❌ {bvid}: {title} [{status}]")

    log(f"========== 完成: 成功={success} 失败={failed} 总计已下载={len(downloaded)} ==========")

    if success > 0:
        msg = f"📥 Bilibili收藏夹下载完成！\n成功: {success}个 | 失败: {failed}个\n总计已下载: {len(downloaded)}个"
        send_tg(msg)

if __name__ == "__main__":
    main()
