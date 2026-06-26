---
name: "doubao-web"
description: "Use Playwright to host a browser and call Doubao Web's image generation function. Call this skill when the user requests to draw or generate an image using Doubao. (使用 Playwright 托管浏览器的方式，调用豆包 Web 端生图功能。当用户要求使用豆包画图、生成图片时调用此技能。)"
instructions: |
  1. Call this skill when the user requests to draw or generate an image, specifically mentioning Doubao or not specifying a particular tool. (当用户请求画图、生成图片，并指明使用豆包或未指定特定工具时，请调用此技能。)
  2. Extract the core subject, style, and scene from the user's description to use as the prompt. (提取用户描述中的核心主体、风格和场景作为 prompt。)
  3. If the user specifies an image aspect ratio (e.g., avatar, wallpaper, 16:9, etc.), automatically match and add the `--ratio=<value>` parameter. (如果用户指定了图片比例，如头像、壁纸、16:9等，请自动匹配并添加 `--ratio=<value>` 参数。)
  4. If the user specifies an image save path, use the `--output=<path>` parameter. (如果用户指定了图片保存路径，请使用 `--output=<path>` 参数。)
  5. By default, execute the command in headless mode in the background: `npx ts-node /Users/pengjianfang/skills/doubao-web-image/scripts/main.ts "user's prompt" [optional parameters]`. (默认使用后台无头模式执行命令：`npx ts-node /Users/pengjianfang/skills/doubao-web-image/scripts/main.ts "用户的prompt" [可选参数]`。)
  6. After execution, show the user the path of the generated image or confirm successful generation. (执行完毕后，向用户展示生成的图片路径或确认生成成功。)
---

# Doubao Web Image Generator

This project/skill uses Playwright to automate browser control, directly utilizing the real environment of Doubao Web for image generation, perfectly bypassing the `a_bogus` signature risk control issue. (这个项目/技能通过 Playwright 自动化控制浏览器的方式，直接利用豆包 Web 端的真实环境进行图片生成，从而完美避开 `a_bogus` 签名风控问题。)

## Features (功能)

- Auto-save login status to `~/.doubao-web-session` (自动保存登录状态在 `~/.doubao-web-session`)
- Send image generation Prompts in a real browser environment (在真实浏览器环境中发送生图 Prompt)
- Intercept and parse SSE stream responses to get the watermark-free original image URL (拦截并解析 SSE 流式响应，获取无水印原图 URL)

## How to Run (如何运行)

```bash
# Default headless mode (silent background run) and original image quality, saving to generated.png
# 默认使用无头模式 (后台静默运行) 和 获取原图画质，并默认保存为 generated.png
npx ts-node scripts/main.ts "A cyberpunk style cat (一只赛博朋克风格的猫咪)"

# Specify image save path (--output or --image)
# 指定图片保存路径 (--output 或 --image)
npx ts-node scripts/main.ts "A cyberpunk style cat" --output="./my_cyber_cat.png"

# Specify image quality (--quality=preview or --quality=original)
# preview fetches faster, original attempts to get high-res quality (default)
# 指定图片画质 (--quality=preview 或 --quality=original)
# preview 抓取速度更快，original 尝试获取大图画质 (默认)
npx ts-node scripts/main.ts "A cyberpunk style cat" --quality=preview --output="./preview_cat.png"

# For the first run or when login is required, you must use the --ui parameter to show the browser window
# 首次运行或需要登录时，必须使用 --ui 参数显示浏览器窗口
npx ts-node scripts/main.ts "Test" --ui
```

### Command Line Arguments (命令行参数说明)

| Parameter (参数) | Description (说明) | Default (默认值) |
|------|------|--------|
| `prompt` | (Required) Prompt for generating the image / (必填) 生成图片的提示词 | `A cute golden retriever (一只可爱的金毛犬)` |
| `--output=<path>` / `--image=<path>` | Local path to save the downloaded image / 图片下载保存的本地路径 | `./generated.png` |
| `--quality=<value>` | Image quality requirement: `preview` or `original` (High-res) / 图片画质要求，可选 `preview` (预览图) 或 `original` (高清原图) | `original` |
| `--ratio=<value>` | Image aspect ratio selection. Supported: `1:1` (Square avatar), `2:3` (Social media selfie), `3:4` (Classic photo), `4:3` (Article illustration), `9:16` (Mobile wallpaper portrait), `16:9` (Desktop wallpaper landscape) / 图片比例选择，支持：`1:1` (正方形头像), `2:3` (社交媒体自拍), `3:4` (经典比例拍照), `4:3` (文章配图插画), `9:16` (手机壁纸人像), `16:9` (桌面壁纸风景) | |
| `--ui` | Show browser interface (must be used for first login) / 显示浏览器界面（首次登录时必须使用） | Background silent run (后台静默运行) |
| `--help`, `-h` | Show help menu / 显示帮助菜单 | |

## Technical Principle (技术原理)

1. **Browser Hosting (浏览器托管)**: Use Playwright to launch a real Chromium browser, loading the user data directory. (利用 Playwright 启动一个真实的 Chromium 浏览器，加载用户数据目录。)
2. **UI Automation (UI 自动化)**: Locate the input box, auto-fill `Help me generate an image: {prompt}` and simulate pressing Enter. (定位输入框，自动填入 `帮我生成图片：{prompt}` 并模拟回车。)
3. **Network Interception (网络拦截)**: Listen to the POST request response of `/samantha/chat/completion` to get the complete SSE data stream. (监听 `/samantha/chat/completion` 的 POST 请求响应，获取完整的 SSE 数据流。)
4. **Data Parsing (数据解析)**: Use regex to match the `image_ori` URL in the response stream. (使用正则匹配响应流中的 `image_ori` 的 URL。)

## Directory Structure (目录结构)

- `scripts/doubao-webapi/client.ts` - Core Playwright client logic (核心 Playwright 客户端逻辑)
- `scripts/main.ts` - Command line entry file (命令行入口文件)
- `package.json` - Project dependencies (项目依赖)