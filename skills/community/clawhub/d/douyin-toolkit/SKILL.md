---
name: douyin-toolkit
description: 自动发布视频到抖音（支持短信验证）。上传视频、填写标题、处理验证码，一条龙完成。
tags: [douyin, video, publish, automation, 抖音, 视频发布]
---

# douyin-publisher

自动将视频发布到抖音创作者平台。

## 前置要求

```bash
pip install playwright
python -m playwright install chromium
```

## 首次使用（登录）

```bash
python3 publish.py --start-browser
```

浏览器启动后，在 VNC 或浏览器窗口中打开抖音创作者中心，扫码登录。
登录态会自动保存在 `chrome_profile/`，下次无需再登录。

## 发布视频

基本用法：
```bash
python3 publish.py --video /path/to/video.mp4 --title "视频标题"
```

## 连续发布多条（保持浏览器不关）

```bash
python3 publish.py --video video1.mp4 --title "第一条" --keep-alive
python3 publish.py --video video2.mp4 --title "第二条" --keep-alive
```

`--keep-alive` 让发布完不关浏览器，后续发布无需重新打开。

## 输入验证码（如需）

脚本发验证码后，在另一个终端执行：
```bash
python3 publish.py --code 验证码
```

默认等待 120 秒，超时可调：
```bash
python3 publish.py --video xxx.mp4 --title "标题" --code-timeout 300
```

## 参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--video` | 视频文件路径（必填） | - |
| `--title` | 视频标题 | 空 |
| `--description` | 视频描述 | 空 |
| `--start-browser` | 启动Chrome（首次登录用） | - |
| `--code` | 短信验证码 | - |
| `--keep-alive` | 发布后保留Chrome不关 | off |
| `--code-timeout` | 验证码等待超时（秒） | 120 |

## 常见问题

### 登录态过期怎么办？
运行 `python3 publish.py --start-browser` 重新扫码登录。

### 提示"找不到文件上传入口"？
可能原因：
1. 登录态过期 → 重新登录
2. 页面加载异常 → 稍后重试

### 想发布多条但不想每次都扫码？
用 `--keep-alive` 参数，发布完浏览器不关，下一条直接跑。

## 说明

- 登录态保存在本地 `chrome_profile/`，不会上传到别处
- 不是每次发布都需要短信验证
- 首次登录用 `--start-browser`，日常发布不用
- 脚本自动截图保存到 `screenshots/` 目录，方便排查
