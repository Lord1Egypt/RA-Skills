---
name: bilibili-video-summarizer
description: B站（bilibili）视频字幕下载与总结工具。当用户说"帮我总结这个B站视频"、"B站视频总结"、"总结b站视频"、"这个视频说了什么"、"视频内容是什么"时触发此技能。自动从B站下载字幕（支持官方字幕和AI字幕），解析为纯文本后对视频内容进行总结，支持中英文双语字幕。
---

# bilibili-video-summarizer

B站视频字幕下载与智能总结。

## 首次使用：配置 Cookie

B站字幕下载需要登录认证。首次使用时：

1. 读取 [references/cookie-setup.md](references/cookie-setup.md) 查看获取 SESSDATA 的方法
2. **引导用户打开 B站 并登录**，按 `F12` → Console → 运行 `console.log(document.cookie.match(/SESSDATA=([^;]+)/)?.[1])`
3. 用户粘贴 SESSDATA 后，保存为 Netscape 格式 cookie 文件到 `~/.config/bilibili-cookies.txt`
4. 如果用户已有 cookie 文件，直接使用

## 使用流程

### Step 1：下载字幕

从用户提供的 B站 URL 中提取 BV 号或完整 URL，调用 `scripts/download.sh`：

```bash
bash <skill>/scripts/download.sh "https://www.bilibili.com/video/BV1X4wAzEEMe"
```

**成功输出示例：**
```
VIDEO_TITLE: 视频标题
AVAILABLE_SUBS: zh-CN srt en-US srt ai-zh srt
SUBTITLE_FILE: /tmp/bili-subtitles/视频标题.zh-CN.srt
SUCCESS
```

**失败处理：**
- `ERROR: Cookie file not found` → 引导用户配置 cookie（见上方首次使用）
- `ERROR: No subtitles could be downloaded` → 说明该视频无字幕，告知用户无法总结
- `ERROR: Could not fetch video title` → URL 无效，请用户确认链接

### Step 2：解析字幕为纯文本

调用 `scripts/parse.py`：

```bash
python3 <skill>/scripts/parse.py "/tmp/bili-subtitles/视频标题.zh-CN.srt"
```

输出纯文本内容（约数千字）。

### Step 3：总结内容

将字幕文本整理为结构化总结，格式：

```
## 视频标题
**字幕字数：** X,XXX 字符

### 🎯 内容主题
[一句话概括视频核心主题]

### 📝 主要内容
[按视频结构分段总结，每段2-4句话]

### 💡 关键要点
- [要点1]
- [要点2]
- [要点3]

### 📌 结论/彩蛋
[视频结尾信息，如有]
```

**总结原则：**
- 忠实于字幕原文，不添加视频未提及的内容
- 保留关键术语和数据
- 中文视频用中文总结，英文视频可用中英文混排
- 语气自然，像人工撰写

## 技术说明

- **字幕优先级**：zh-CN → zh-Hans → zh-Hant → ai-zh → en-US
- **工具**：`yt-dlp`（pip3 install yt-dlp --break-system-packages）
- **Cookie 格式**：Netscape HTTP Cookie File（`~/.config/bilibili-cookies.txt`）
- **Cookie 有效期**：约30天，过期后需重新配置
- **不适用场景**：无字幕的纯音乐/舞蹈/游戏实况视频

## 文件结构

```
bilibili-video-summarizer/
├── SKILL.md                          # 本文件
├── references/
│   └── cookie-setup.md               # Cookie 配置指南
└── scripts/
    ├── download.sh                    # 字幕下载脚本
    └── parse.py                      # SRT→纯文本解析脚本
```
