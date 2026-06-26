---
name: douyin
description: "Douyin (TikTok China) video uploader & automation tool. Upload videos, manage login sessions, and automate publishing to Douyin Creator Platform. 抖音视频上传工具 | 自动化发布 | 创作者平台。Use when uploading video to Douyin, logging in to Douyin, or checking Douyin login status."
version: 2.2.0
allowed-tools: Bash(node *) Bash(npm *)
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
      anyBins:
        - chromium
        - google-chrome
        - chrome
    install:
      - kind: node
        package: puppeteer
        bins: []
    homepage: https://github.com/lancelin111/douyin-mcp-server
    emoji: "\U0001F3AC"
    os:
      - macos
      - linux
      - windows
---

# Douyin Video Uploader | 抖音视频上传工具

> **Douyin (TikTok China) video upload automation** — login, upload, and manage your Douyin Creator account from the command line or AI agents.
>
> 自动化上传视频到抖音创作者平台，支持登录、上传和账号管理。

**Keywords:** Douyin uploader, TikTok China, video upload, social media automation, 抖音上传, 抖音自动化, 短视频发布, creator platform

**This skill is self-contained — all code is bundled, no external repo cloning needed.**
此 skill 为自包含结构，所有代码已打包在内，无需克隆外部仓库。

## Important: First Upload Requires SMS Verification | 重要提示：首次上传需要短信验证

> **After logging in, your first video upload will require SMS verification.** Enter the verification code when prompted. After this one-time verification, all subsequent uploads will be fully automated.
>
> **登录成功后，第一次上传视频需要短信验证。** 按提示输入验证码即可。完成一次验证后，之后的上传将完全自动化，无需再次验证。

## Transparency Statement | 透明度声明

### Data Storage | 数据存储
- **Cookie file / Cookie 文件**: `{baseDir}/douyin-cookies.json` — Stores Douyin login credentials locally only (file permission: 0600) / 存储抖音登录凭证，仅在本地保存（文件权限：0600）
- **Browser data / 浏览器数据**: `{baseDir}/chrome-user-data/` — Puppeteer browser session data

### Network Access | 网络访问
This tool only accesses official Douyin domains / 本工具仅访问以下抖音官方域名：
- `https://creator.douyin.com` — Douyin Creator Platform (login & upload) / 抖音创作者平台（登录、上传）
- `https://www.douyin.com` — Douyin main site (permission verification) / 抖音主站（权限验证）

**No third-party servers are accessed. Your credentials are never uploaded or leaked.**
不会访问任何第三方服务器，不会上传或泄露您的登录凭证。

### Code Behavior | 代码行为
1. **login.js**: Opens browser → navigates to Douyin login → waits for manual login → saves Cookie locally / 打开浏览器 → 导航到抖音登录页 → 等待用户手动登录 → 保存 Cookie 到本地文件
2. **upload.js**: Loads Cookie → auto-login → uploads video → fills title/description/tags → publishes / 读取本地 Cookie → 自动登录 → 上传指定视频文件 → 填写标题/描述/标签 → 发布
3. **manage.js**: Read/validate/delete local Cookie files / 读取/验证/删除本地 Cookie 文件

### Dependencies | 依赖
- **puppeteer**: Browser automation (Chromium) / 浏览器自动化（Chromium）
- Full dependencies: see `package.json` in this directory / 完整依赖: 见本目录 `package.json`

## Installation | 安装

First-time setup — install dependencies / 首次使用需要安装依赖：

```bash
cd {baseDir} && npm install
```

> **Note / 说明**: Only installs puppeteer, no external repo cloning needed / 仅安装 puppeteer 依赖，无需克隆外部仓库。

## Feature 1: Login to Douyin | 功能一：登录抖音

Login to Douyin Creator Platform and save credentials (Cookie).
登录抖音创作者平台，保存登录凭证（Cookie）。

```bash
cd {baseDir} && node scripts/login.js
```

**Process / 流程：**
1. Auto-opens a browser window / 自动打开浏览器窗口
2. Waits for user to complete login (QR code or password) / 等待用户完成登录（扫码或账号密码）
3. Saves Cookie automatically after login / 登录成功后自动保存 Cookie

**Output example / 输出示例：**
```
✅ Login successful!
User: 用户昵称
Cookies saved: 25
```

## Feature 2: Upload Video | 功能二：上传视频

Upload video to Douyin with title, description and tags.
上传视频到抖音，支持设置标题、描述和标签。

```bash
cd {baseDir} && node scripts/upload.js --video "视频路径" --title "视频标题"
```

**Parameters / 参数：**

| Parameter 参数 | Required 必需 | Description 说明 |
|-----|-----|------|
| `--video` | Yes 是 | Absolute path to video file / 视频文件绝对路径 |
| `--title` | Yes 是 | Video title / 视频标题 |
| `--description` | No 否 | Video description / 视频描述 |
| `--tags` | No 否 | Tags, comma-separated / 标签，逗号分隔 |
| `--no-publish` | No 否 | Save as draft only / 仅保存草稿 |

**Full example / 完整示例：**
```bash
cd {baseDir} && node scripts/upload.js \
  --video "/Users/xxx/video.mp4" \
  --title "我的视频" \
  --description "视频描述" \
  --tags "日常,生活,记录"
```

**Output example / 输出示例：**
```
✅ Video upload and publish successful!
Title: 我的视频
Status: Published
```

## Feature 3: Manage Login Status | 功能三：管理登录状态

Check, view or clear login data / 检查、查看或清除登录数据。

### Check if login is valid | 检查登录是否有效
```bash
cd {baseDir} && node scripts/manage.js check
```

### View Cookie info | 查看 Cookie 信息
```bash
cd {baseDir} && node scripts/manage.js info
```

### Clear login data | 清除登录数据
```bash
cd {baseDir} && node scripts/manage.js clear
```

## FAQ | 常见问题

**Q: "Login expired" error?**
**Q: 提示 "Login expired"？**
```bash
cd {baseDir} && node scripts/manage.js clear
cd {baseDir} && node scripts/login.js
```

**Q: SMS verification during upload? / Q: 上传时遇到短信验证？**
The program will prompt you — enter the code as instructed.
程序会自动提示，按提示输入验证码即可。

**Q: How long does the Cookie last? / Q: Cookie 有效期多久？**
About 30 days. Check login status regularly.
约 30 天，建议定期检查登录状态。
