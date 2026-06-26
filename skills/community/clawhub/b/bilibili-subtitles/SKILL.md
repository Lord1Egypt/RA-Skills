---
name: bilibili-subtitles
description: 使用 yt-dlp 从哔哩哔哩公开视频提取已有字幕或自动字幕（不下载整段视频）。当用户提到 B 站、bilibili、BV 号、视频字幕、拉字幕、做摘要、根据视频内容回答问题时使用。v1 仅支持平台已提供字幕轨道的视频；无字幕视频需换源或后续用 Whisper 等方案。
---

# B 站字幕提取（yt-dlp）

## 依赖

- 已安装 **yt-dlp**（推荐）：`brew install yt-dlp`
- 保持较新版本：`brew upgrade yt-dlp`（B 站接口常变）

## 何时用本 Skill

| 场景 | 是否适合 v1 |
|------|----------------|
| 视频有 UP 上传字幕或 B 站自动字幕 | ✅ |
| 无任何字幕轨 | ❌（需换有字幕视频，或另做音频转写） |

## 标准流程

### 1. 查看有哪些字幕

```bash
yt-dlp --list-subs "https://www.bilibili.com/video/BVxxxxxxxxxx/"
```

记下语言代码（如 `zh-Hans`、`zh-CN`）。

### 2. 只下载字幕（不下载视频）

```bash
yt-dlp --write-subs --write-auto-subs --skip-download \
  --sub-langs "zh-Hans,zh-CN,zh,zh-Hant,en" \
  -o "bilibili_%(id)s.%(ext)s" \
  "https://www.bilibili.com/video/BVxxxxxxxxxx/"
```

- `--write-auto-subs`：含 B 站自动生成的字幕（若有）。
- 输出多为 `.vtt` 或 `.srt`，与视频同目录或当前目录。

### 3. 把 VTT 收成纯文本（便于喂给模型）

```bash
# 简单去时间轴与标记（按需调整路径）
sed -e '/^WEBVTT/d' -e '/^NOTE/d' -e '/^[0-9][0-9]:/d' -e '/^$/d' -e 's/<[^>]*>//g' \
  "某文件.zh-Hans.vtt" | sed '/^$/d' > bilibili_subtitles_plain.txt
```

## 若出现 HTTP 412 / 无法下载网页

B 站可能对匿名请求限流。按顺序尝试：

1. **用浏览器 Cookie（推荐）**  
   ```bash
   yt-dlp --cookies-from-browser chrome --list-subs "URL"
   ```
   可将 `chrome` 换成 `safari`、`firefox`（本机需已登录 bilibili.com）。

2. **导出 Netscape 格式 cookies.txt**，再：  
   `yt-dlp --cookies /path/to/cookies.txt ...`

3. **升级 yt-dlp** 后重试。

详见 [reference.md](reference.md)。

## 对 Agent 的提示

- 先 `--list-subs`，无可用语言则明确告知用户「该 BV 无字幕轨」，不要假装已提取。
- 提取成功后，优先读 `.srt`/`.vtt` 再总结；长文本可先落盘再分段阅读。
- 勿在回复中粘贴完整 Cookie 或账号秘密。

## ClawHub / OpenClaw 发布说明

本 Skill 为 **纯文档 + 系统命令**，无额外二进制。发布时在描述中写明：依赖 `yt-dlp`、可能需 Cookie、v1 不做无字幕转写。
