---
name: byted-sol-douyin-creator-upload
description: 将本地视频文件上传到抖音创作者中心并发布，支持设置可见性（公开/好友可见/仅自己可见）、填写作品描述。适用于"把视频传到抖音""发布到创作者中心""上传并设为仅自己可见""上传抖音作品"这类任务。依赖已登录的抖音创作者账号，发布若触发短信验证码需人工提供。
author: byted-sol
version: 1.0.0
license: MIT
tags:
  - douyin
  - video-upload
  - creator-center
  - browser-automation
requirements:
  node: ">=18"
  commands:
    - node
  npm:
    - playwright-core
permissions:
  filesystem:
    - read local video file passed with --file
  network:
    - connect to local Chrome CDP endpoint
    - access creator.douyin.com through the user's logged-in browser session
---

# 抖音创作者中心视频上传与发布

给定本地视频绝对路径，连接已启动并开启 CDP 的 Chrome，会话复用当前已登录的抖音创作者账号，自动完成上传、填写作品描述、设置可见性，并按需点击发布。核心脚本为 `scripts/upload_to_creator.js`。

## 能力简介

该 Skill 用于把“本地视频 -> 上传到抖音创作者中心 -> 设置可见性 -> 发布”封装成单条命令执行，替代手动打开页面、点击上传、填写描述、切换可见性、点击发布的重复操作。

## 适用场景

在用户已经登录抖音创作者中心，并希望：

- 把本地视频上传到 `creator.douyin.com`
- 上传后直接发布到抖音作品
- 上传后填写作品描述
- 上传并设为“仅自己可见”
- 上传并设为“好友可见”或“公开”
- 只上传和填写信息，但暂不发布

时使用本 Skill。

## 前置条件

### 环境要求

- Node.js 可执行
- 宿主环境已安装 Chrome 或 Chromium，并已使用远程调试端口启动
- 运行脚本时需通过 `NODE_PATH=/usr/lib/node_modules/openclaw/node_modules` 复用 OpenClaw 自带的 `playwright-core`

### 账号要求

- Chrome 中已登录可用的抖音创作者账号
- 已存在一个 URL 包含 `creator.douyin.com` 的页面，供脚本通过 CDP 接管

### 启动参考

示例：

```bash
open -na "Google Chrome" --args --remote-debugging-port=9222
```

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--file` | 是 | 无 | 待上传视频的绝对路径 |
| `--visibility` | 否 | `self` | 可见性：`public` / `friend` / `self`，分别映射为“公开” / “好友可见” / “仅自己可见” |
| `--title` | 否 | 空 | 作品描述文字 |
| `--cdp` | 否 | `http://127.0.0.1:9222` | Chrome DevTools Protocol 连接地址 |
| `--publish` | 否 | `true` | 是否点击发布；`false` 表示只上传并填写信息，不执行发布 |

## 执行命令示例

### 示例 1：上传并发布，默认仅自己可见

```bash
NODE_PATH=/usr/lib/node_modules/openclaw/node_modules \
node skill-douyin-creator-upload/scripts/upload_to_creator.js \
  --file "/absolute/path/video.mp4"
```

### 示例 2：上传、填写描述、设为公开并发布

```bash
NODE_PATH=/usr/lib/node_modules/openclaw/node_modules \
node skill-douyin-creator-upload/scripts/upload_to_creator.js \
  --file "/absolute/path/video.mp4" \
  --title "今日作品发布测试" \
  --visibility public \
  --publish true
```

### 示例 3：只上传不发布

```bash
NODE_PATH=/usr/lib/node_modules/openclaw/node_modules \
node skill-douyin-creator-upload/scripts/upload_to_creator.js \
  --file "/absolute/path/video.mp4" \
  --title "先上传，稍后人工检查" \
  --visibility self \
  --publish false
```

## 执行逻辑步骤

按以下顺序执行：

1. 校验输入参数
   - `--file` 必填，且必须为本地绝对路径
   - `--visibility` 只允许 `public` / `friend` / `self`
   - `--publish` 解析为布尔值
2. 通过 `chromium.connectOverCDP({ endpointURL })` 连接已启动的 Chrome
3. 遍历所有 BrowserContext 和 Page，查找 URL 包含 `creator.douyin.com` 的页面
4. 若当前不在上传页，则跳转到 `https://creator.douyin.com/creator-micro/content/upload` 并等待约 6 秒
5. 在页面所有 `frame` 中查找动态加载的上传控件 `input[type="file"]`
   - 最多重试 3 次
   - 每次间隔 3 秒
6. 调用 `setInputFiles(...)` 上传本地视频文件
7. 等待页面 URL 跳转到 `/content/post/video`，最长等待 120 秒
8. 尝试关闭可能出现的提示弹窗，如“我知道了”“知道了”“完成”
9. 如传入 `--title`，向可编辑区域 `contenteditable` 填入作品描述
10. 根据 `--visibility` 勾选对应的可见性项
11. 若 `--publish=true`，点击“发布”按钮
12. 点击发布后检测是否出现“短信验证码”文案
   - 若出现，则明确提示需人工处理，不自动代填，并按约定退出

## 退出码约定

| 退出码 | 含义 |
|--------|------|
| `0` | 成功 |
| `1` | 未捕获异常 |
| `2` | 参数错误 |
| `3` | 未找到已登录的创作者中心页面 |
| `4` | 未找到上传控件 |
| `5` | 未找到发布按钮 |
| `10` | 发布触发短信验证码，需人工处理 |

## 异常处理

出现以下情况时，直接输出明确日志并按对应退出码停止：

- 视频路径为空、不是绝对路径、或文件不存在
- `--visibility` 取值非法
- CDP 连接失败
- 未找到 URL 包含 `creator.douyin.com` 的页面
- 页面结构变化，未找到 iframe 内上传控件
- 页面跳转超时，上传流程未进入发布页
- 未找到“发布”按钮
- 发布后触发短信验证码校验

日志统一使用以下前缀：

- `STEP:` 当前步骤
- `OK:` 步骤成功
- `WARN:` 可继续执行的异常或兼容性提示
- `ERROR:` 终止执行的错误

## 能力边界

- 不做视频剪辑、转码、封面生成
- 不代填短信验证码
- 不处理账号风控、平台拦截、登录失效
- 不保证兼容创作者中心所有灰度页面样式
- 仅支持抖音创作者中心 `creator.douyin.com`
