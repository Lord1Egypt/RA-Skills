---
name: gemini-image-gen-watermark-removal
description: "Google Gemini 网页端生图并去水印。通过 OpenClaw Browser Tool 控制浏览器生成、下载图片，再用 GeminiWatermarkTool 去除水印。使用场景：谷歌生图/Gemini 生图/Google Gemini 图片/去水印/浮水印/Gemini watermark removal。"
---

# Google Gemini 生图

通过 OpenClaw Browser Tool 操控已登录 Google 账号的浏览器，在 Gemini 网页端生成并下载图片。

## 前置条件

- 浏览器已登录 Google 账号
- OpenClaw Browser Tool 可用（确保 `openclaw browser status` 正常）
- profile 使用 `user` 连接已打开的 Chrome

## 执行流程

### 1. 打开 Gemini 页面

```
browser(action="open", profile="user", url="https://gemini.google.com")
```

也可以直接打开已有对话链接复用图片：
```
browser(action="open", profile="user", url="https://gemini.google.com/app/<对话ID>")
```

### 2. 点击「制作图片」

snapshot 找到按钮 ref，然后 click：
```
browser(action="snapshot", profile="user", compact=true)
// 找到「制作图片」按钮的 ref，然后 click
browser(action="act", profile="user", request={"kind": "click", "ref": "<ref>"})
```

新对话会先展示风格选择界面（单色/色块/跑跑等），可以直接忽略，在输入框输入 prompt 即可。

### 3. 输入 Prompt 并发送

```
browser(action="act", profile="user", request={"kind": "type", "ref": "<textarea ref>", "text": "你的Prompt"})
browser(action="act", profile="user", request={"kind": "press", "key": "Enter"})
```

**⚠️ Prompt 规则**：
- 避免使用"唱""弹奏"等动词关键词，否则 Gemini 会误触发音乐生成而非图片生成
- 改为纯视觉描述，如"wearing a microphone headset"而非"singing with a microphone"
- 需要文字时直接在 prompt 中写明，如 `The text "畢士傾訴" appears on a banner`

### 4. 等待图片生成

**⚠️ 关键：不要用 `act(kind="wait")`！**

`act(kind="wait")` 在 CDP 层面没有真正的"等待页面变化"机制，它只是在等 WebSocket 响应，8 秒无响应就会超时并导致整个 browser tool session 不可用。

**正确做法：用 `exec sleep` 等待后再 snapshot**

```
exec: sleep 20 && echo "done"
// 等待 exec 完成后
browser(action="snapshot", profile="user", compact=true)
```

生成完成标志：页面出现「下载完整尺寸的图片」「复制图片」「分享图片」等按钮。

如果 snapshot 显示还在生成中（有 "Creating your image..." 按钮），再 sleep 一轮。

### 5. 下载图片

点击「下载完整尺寸的图片」按钮：
```
browser(action="act", profile="user", request={"kind": "click", "ref": "<下载按钮ref>"})
```

等待下载完成后检查下载目录：
```bash
sleep 5 && ls -lt ~/Downloads/Gemini_Generated_Image* | head -3
```

### 6. 去水印

Gemini 生成的图片带有水印，使用 [GeminiWatermarkTool](https://github.com/allenk/GeminiWatermarkTool) 去除。

**安装**（macOS / Linux）：
```bash
brew install allenk/tap/gwt
```
或从 [GitHub Releases](https://github.com/allenk/GeminiWatermarkTool/releases) 下载二进制文件。

**已知可用路径**（若 brew 不可用）：
```
~/.claude/skills/gwt/bin/GeminiWatermarkTool
```

**使用**：
```bash
gwt --force -i <输入图片> -o <输出图片>
```

### 7. 发送到飞书（可选）

使用 send-feishu-image 技能：
```python
import sys
sys.path.insert(0, "~/.openclaw/workspace/skills/send-feishu-image")
from send_feishu_image import send_image
result = send_image(
    image_path="/path/to/output.png",
    user_id="ou_7abe0c2af8a0f7b5b1c1171bcd8707d8",
    caption="图片说明"
)
```

## 已知问题

| 问题 | 解决方案 |
|------|----------|
| `act(kind="wait")` 超时导致 browser tool 不可用 | **永远不要用 `act(kind="wait")`**，改用 `exec sleep` + `snapshot` 轮询 |
| snapshot 超时 | 重启 Gateway（菜单栏 OpenClaw → Restart） |
| 标签页未找到 | `browser(action="snapshot")` 查看当前页面状态 |
| 触发了音乐生成 | prompt 去掉"唱""弹"等词，改为纯视觉描述 |
| 图片长时间未生成 | Gemini 模型较慢，sleep 20-25 秒再 snapshot |
| gwt 安装失败（GitHub 不可达） | 检查 `~/.claude/skills/gwt/bin/GeminiWatermarkTool` 是否已存在 |
| 下载后找不到新文件 | 注意文件名变化，用 `ls -lt` 按时间排序查看最新的 |

## 完成后

- 关闭不用的标签页：`browser(action="close", targetId="<ID>")`
