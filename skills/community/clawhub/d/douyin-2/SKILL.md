---
name: douyin
description: 抖音视频上传工具。支持登录抖音账号、上传视频、管理登录状态。当用户需要上传视频到抖音、登录抖音、检查抖音登录状态时使用。
version: 2.1.0
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

# 抖音视频上传工具

自动化上传视频到抖音创作者平台，支持登录、上传和账号管理。

**此 skill 为自包含结构，所有代码已打包在内，无需克隆外部仓库。**

## 透明度声明

### 数据存储
- **Cookie 文件**: `{baseDir}/douyin-cookies.json` - 存储抖音登录凭证，仅在本地保存
- **浏览器数据**: `{baseDir}/chrome-user-data/` - Puppeteer 浏览器会话数据

### 网络访问
本工具仅访问以下抖音官方域名：
- `https://creator.douyin.com` - 抖音创作者平台（登录、上传）
- `https://www.douyin.com` - 抖音主站（权限验证）

**不会访问任何第三方服务器，不会上传或泄露您的登录凭证。**

### 代码行为
1. **login.js**: 打开浏览器 → 导航到抖音登录页 → 等待用户手动登录 → 保存 Cookie 到本地文件
2. **upload.js**: 读取本地 Cookie → 自动登录 → 上传指定视频文件 → 填写标题/描述/标签 → 发布
3. **manage.js**: 读取/验证/删除本地 Cookie 文件

### 依赖
- **puppeteer**: 浏览器自动化（Chromium）
- 完整依赖: 见本目录 `package.json`

## 安装

首次使用需要安装依赖：

```bash
cd {baseDir} && npm install
```

> **说明**: 仅安装 puppeteer 依赖，无需克隆外部仓库。

## 功能一：登录抖音

登录抖音创作者平台，保存登录凭证（Cookie）。

```bash
cd {baseDir} && node scripts/login.js
```

**流程：**
1. 自动打开浏览器窗口
2. 等待用户完成登录（扫码或账号密码）
3. 登录成功后自动保存 Cookie

**输出示例：**
```
✅ Login successful!
User: 用户昵称
Cookies saved: 25
```

## 功能二：上传视频

上传视频到抖音，支持设置标题、描述和标签。

```bash
cd {baseDir} && node scripts/upload.js --video "视频路径" --title "视频标题"
```

**参数：**

| 参数 | 必需 | 说明 |
|-----|-----|------|
| `--video` | 是 | 视频文件绝对路径 |
| `--title` | 是 | 视频标题 |
| `--description` | 否 | 视频描述 |
| `--tags` | 否 | 标签，逗号分隔 |
| `--no-publish` | 否 | 仅保存草稿 |

**完整示例：**
```bash
cd {baseDir} && node scripts/upload.js \
  --video "/Users/xxx/video.mp4" \
  --title "我的视频" \
  --description "视频描述" \
  --tags "日常,生活,记录"
```

**输出示例：**
```
✅ Video upload and publish successful!
Title: 我的视频
Status: Published
```

## 功能三：管理登录状态

检查、查看或清除登录数据。

### 检查登录是否有效
```bash
cd {baseDir} && node scripts/manage.js check
```

### 查看 Cookie 信息
```bash
cd {baseDir} && node scripts/manage.js info
```

### 清除登录数据
```bash
cd {baseDir} && node scripts/manage.js clear
```

## 常见问题

**Q: 提示 "Login expired"？**
```bash
cd {baseDir} && node scripts/manage.js clear
cd {baseDir} && node scripts/login.js
```

**Q: 上传时遇到短信验证？**
程序会自动提示，按提示输入验证码即可。

**Q: Cookie 有效期多久？**
约 30 天，建议定期检查登录状态。
