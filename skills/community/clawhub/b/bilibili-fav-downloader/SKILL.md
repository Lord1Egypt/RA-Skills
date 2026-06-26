---
name: bilibili-fav-downloader
description: >
  Bilibili 收藏夹自动下载工具。支持增量下载（每2小时自动检查新视频）、
  最高画质（视频+音频合并为MP4）、Telegram 通知。
  触发场景：
  (1) 用户想下载 Bilibili 收藏夹视频
  (2) 想设置收藏夹自动监控和新视频通知
  (3) 需要获取 Bilibili Cookie 或收藏夹 ID 的帮助
  (4) 想把现有 Bilibili 下载功能固化为可分享的 Skill
---

# Bilibili Favorite Downloader

全自动 Bilibili 收藏夹监控下载工具。用户只需提供 Cookie 和收藏夹 ID，即可自动下载。

## 环境要求

- Python 3.8+
- `yt-dlp`（Bilibili 下载核心）
- `ffmpeg`（音视频合并）
- Linux/macOS/WSL

## 环境安装

如果用户尚未安装环境，引导运行：
```bash
bash scripts/setup.sh
```

或手动安装：
```bash
# Ubuntu/Debian
sudo apt install ffmpeg
pip3 install yt-dlp

# macOS
brew install ffmpeg
pip3 install yt-dlp
```

## 使用方式

### 快速开始

1. 获取 Cookie（详见 `references/cookie-guide.md`）
2. 获取收藏夹 ID（详见 `references/favorite-guide.md`）
3. 运行下载：
```bash
python3 scripts/bilibili_fav_dl.py \
  --cookie /path/to/cookie.txt \
  --fav-id 你的收藏夹ID \
  --out-dir ./downloads
```

### 仅检查（不下载）

```bash
python3 scripts/bilibili_fav_dl.py \
  --cookie /path/to/cookie.txt \
  --fav-id 你的收藏夹ID \
  --check-only
```

### 自动化配置

设置每2小时自动运行（crontab）：
```bash
# 编辑 crontab
crontab -e

# 添加：
0 */2 * * * /usr/bin/python3 /path/to/bilibili_fav_dl.py --cookie /path/to/cookie.txt --fav-id 你的收藏夹ID --out-dir /path/to/downloads >> /var/log/bilibili_dl.log 2>&1
```

### Telegram 通知（可选）

设置环境变量：
```bash
export BILIBILI_TG_BOT_TOKEN="你的BotToken"
export BILIBILI_TG_CHAT_ID="你的ChatID"
```

然后在 crontab 中正常运行脚本即可。新视频下载完成后自动发送通知。

## 核心脚本说明

| 脚本 | 作用 |
|------|------|
| `scripts/setup.sh` | 自动安装 yt-dlp 和 ffmpeg |
| `scripts/bilibili_fav_dl.py` | 主下载脚本（分页获取、增量下载、TG通知）|

## Cookie 获取

详见 `references/cookie-guide.md`，核心步骤：
1. 登录 douyin.com
2. F12 → Network → 任意请求 → Request Headers → Cookie
3. 导出为 Netscape 格式文件

## 收藏夹 ID 获取

详见 `references/favorite-guide.md`，核心步骤：
1. 打开收藏夹页面
2. URL 中找 `fid=xxx` 或 `mlxxx`

## 文件命名格式

下载文件命名为：`视频标题___BV号.mp4`

例如：`【合集】2024年度盘点___BV1xx411x7h7.mp4`

## 已知限制

- 部分视频因地区版权限制无法下载
- Cookie 有效期约1-3个月，过期后需重新获取
- 需 Cookie 才能访问私人收藏夹
