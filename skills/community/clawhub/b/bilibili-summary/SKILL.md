---
name: bilibili-subtitle
description: 处理 B 站（哔哩哔哩）视频字幕的完整工作流。能力包括：（1）引导用户扫码登录获取 Cookie；（2）自动获取视频字幕（优先 AI 字幕，自动回退 CC 字幕）；（3）生成视频内容摘要；（4）当用户询问"某内容在哪个时间段"时，从字幕文件中精准定位时间戳。当用户提供 B 站视频链接、BVID，或提到"b站字幕""帮我看视频""视频摘要""视频哪里讲到了""字幕提取"等任何与 B 站视频内容理解相关的场景时，务必使用此 skill。即使用户只是随口提到一个 bilibili 链接，也应该触发此 skill。
---

# B 站视频字幕 Skill

> 此 skill 完全自包含，所有脚本均在 `scripts/` 目录内，无需额外项目依赖。

## 依赖安装

脚本只需要一个第三方库，在运行前确保已安装：

```bash
pip install requests
```

可选安装（用于终端显示扫码二维码）：

```bash
pip install qrcode
```

---

## 核心能力

| 场景 | 你需要做什么 |
|------|------------|
| 用户给链接/BVID，想要字幕或摘要 | 检查登录 → 获取字幕 → 生成摘要 |
| 用户问"某内容在几分几秒" | 获取字幕（如已有则跳过）→ 搜索 SRT 时间戳 |
| 用户 Cookie 失效或首次使用 | 引导扫码登录 → 重新获取字幕 |

---

## 工作流

### 第一步：解析 BVID

从用户输入中提取 BVID（格式：`BVxxxxxxxxxx`）。

- 支持纯 BVID：`BV1ZL411o7LZ`
- 支持完整链接：`https://www.bilibili.com/video/BV1ZL411o7LZ`
- 短链（`https://b23.tv/xxx`）需先让用户提供完整链接或 BVID

### 第二步：检查字幕缓存

检查 `subtitles_output/<BVID>/<BVID>.txt` 是否已存在：

- **存在**：直接使用，跳过第三步。告知"已找到本地缓存字幕"。
- **不存在**：进入第三步获取字幕。

### 第三步：获取字幕

运行获取脚本（路径相对于 skill 目录）：

```bash
python <skill-dir>/scripts/fetch_subtitle.py <BVID> --cookie cookie.txt --output-dir subtitles_output
```

`<skill-dir>` 是此 SKILL.md 所在的目录路径。脚本会自动：
1. 按优先级查找 Cookie（指定路径 → 当前目录 → 脚本目录）
2. 优先获取 AI 字幕，无 AI 字幕时自动回退到 CC 字幕
3. 同时输出 `.txt`、`.srt`、`.vtt` 三种格式

**常见错误处理：**

| 错误 | 处理方式 |
|------|---------|
| Cookie 不存在/无效 | 引导用户登录（见下方"扫码登录"） |
| 该视频没有字幕 | 告知用户（硬字幕需 OCR，超出 skill 能力） |
| 网络超时 | 建议用户检查网络并重试 |

### 扫码登录（仅在需要时执行）

当 `cookie.txt` 不存在或已失效时，引导用户登录。

根据当前环境选择合适方式：

**方式 A：AI 可运行终端命令（如 Antigravity/Claude Code）**

1. 告知用户需要登录 B 站以获取 AI 字幕
2. 运行登录脚本：
   ```bash
   python <skill-dir>/scripts/cookie_login.py --output cookie.txt
   ```
3. 脚本会在终端打印 ASCII 二维码和登录链接
4. 如果 ASCII 二维码显示不清晰，可以用以下方式生成图片二维码给用户：
   ```python
   import qrcode
   img = qrcode.make("<扫码链接URL>")
   img.save("qr_login.png")
   ```
5. 用户在手机 B 站 App 扫码并确认后，Cookie 自动保存
6. 继续执行第三步

**方式 B：AI 无法运行命令（如 OpenClaw/Claude.ai）**

1. 引导用户自己在终端执行：
   ```bash
   pip install requests qrcode
   python <path-to-installed-skill>/scripts/cookie_login.py
   ```
2. 或者让用户手动获取 Cookie：
   - 登录 B 站 → F12 → Application → Cookies
   - 复制 `SESSDATA` 和 `bili_jct` 的值
   - 写入 `cookie.txt`，格式：`SESSDATA=xxx; bili_jct=xxx`

### 第四步：生成摘要

读取 `subtitles_output/<BVID>/<BVID>.txt` 的纯文本字幕，生成结构化摘要：

```
## 视频摘要：[BVID]

### 核心主题
（一句话概括视频主要讲了什么）

### 主要内容
1. [要点一]
2. [要点二]
3. [要点三]
...

### 关键结论
（视频最后强调或总结的观点）
```

字幕文本很长时：
- 按内容逻辑分段，不要平均切割
- 识别明显的"话题切换"作为章节分隔点
- 摘要长度以覆盖主要观点为准

### 第五步：时间戳查询

当用户问"xxx 在哪个时间段"或"视频里什么时候讲到了 xxx"时：

1. 确认已有 SRT 文件（`subtitles_output/<BVID>/<BVID>.srt`）
2. 运行时间戳搜索脚本：
   ```bash
   python <skill-dir>/scripts/search_timestamp.py \
     subtitles_output/<BVID>/<BVID>.srt "<关键词>" --context 2
   ```
3. 将结果整理成友好格式：
   - "视频在 **01:23** 左右提到了这个内容"
   - 多处匹配时列出所有时间点
   - 关键词找不到时，尝试近义词或分拆词搜索

> SRT 时间格式为 `HH:MM:SS,mmm`，向用户展示时简化为 `MM:SS`。

---

## 目录结构

```
bilibili-subtitle/             ← skill 根目录（本目录）
├── SKILL.md                   ← 本文件
└── scripts/
    ├── fetch_subtitle.py      ← 字幕获取（自包含，无外部依赖）
    ├── search_timestamp.py    ← 时间戳搜索
    └── cookie_login.py        ← 扫码登录获取 Cookie

用户工作目录下生成：
├── cookie.txt                 ← 登录 Cookie（自动生成）
└── subtitles_output/
    └── <BVID>/
        ├── <BVID>.txt         ← 纯文本字幕（用于摘要）
        ├── <BVID>.srt         ← 带时间戳字幕（用于时间定位）
        └── <BVID>.vtt         ← VTT 格式字幕
```

---

## 注意事项

- **AI 字幕需要登录**：未登录只能获取 UP 主手动上传的 CC 字幕，大多数视频的 AI 字幕必须登录。
- **Cookie 有效期**：通常有效数月，但账号异常登出会导致失效。
- **字幕条数少**：如果获取到的字幕极少（< 10 条），可能是 CC 字幕而非完整 AI 字幕，提示用户。
- **硬字幕**：烧录在画面中的字幕（如综艺、电影）无法获取，需 OCR 工具处理。
