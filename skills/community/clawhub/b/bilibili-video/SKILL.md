---
name: bilibili-video
description: >
  B站(Bilibili)视频字幕提取与音频转写工具。基于 bilibili-api-python，自带 WBI 签名反爬。
  三级降级策略：CC字幕 → AI字幕(9种语言) → 音频下载+ASR转写。
  当以下情况时使用：
  (1) 用户提供 B 站视频链接或 BV/AV/EP/SS 号，要求获取字幕或文字内容
  (2) 用户要求下载 B 站视频的音频
  (3) 用户要求总结、分析 B 站视频内容（需先提取字幕）
  (4) 用户提到"B站"、"bilibili"、"视频字幕"、"视频转写"、"BV号"
  触发词：B站、bilibili、哔哩哔哩、视频字幕、视频转写、BV号、看这个视频、视频内容
---

# B站视频字幕与音频提取

## 快速使用

```bash
# 提取字幕（三级降级自动选择最佳来源）
python3 skills/bilibili-video/scripts/bilibili_extract.py BV1GqZUBvENu

# 完整 URL 也行
python3 skills/bilibili-video/scripts/bilibili_extract.py "https://www.bilibili.com/video/BV1GqZUBvENu/"

# 仅查看视频信息
python3 skills/bilibili-video/scripts/bilibili_extract.py --info BV1GqZUBvENu

# 仅下载音频（不转写）
python3 skills/bilibili-video/scripts/bilibili_extract.py --audio-only BV1GqZUBvENu

# 禁用 ASR 兜底（字幕不可用时仅下载音频）
python3 skills/bilibili-video/scripts/bilibili_extract.py --no-asr BV1GqZUBvENu
```

## 三级降级策略

1. **CC 字幕**：UP 主上传的字幕，准确度最高，优先中文
2. **AI 字幕**：B 站 AI 生成字幕，支持 ai-zh/ai-en 等 9 种语言
3. **音频转写**：下载音频，调用 `speech-to-text.sh`（飞书STT → Gemini → MiMo → Qwen 四级降级）

大部分视频前两级即可覆盖。第三级需要更多时间但可处理任何有声视频。

## 输出

- 目录：`/tmp/openclaw/bilibili/`
- 文件：`{BV_ID}_transcript.txt`
- 格式：视频元信息 + 正文（自动繁转简）

## 登录（提升成功率）

无 cookie 可用但功能受限。遇到 412 风控时需要登录：

```bash
# 终端扫码登录
python3 skills/bilibili-video/scripts/bilibili_login.py

# 检查 cookie 是否有效
python3 skills/bilibili-video/scripts/bilibili_login.py --check
```

也可以从浏览器手动提取 cookie（SESSDATA、bili_jct、buvid3、DedeUserID），保存为 JSON 到 `~/.openclaw/workspace/.bilibili_cookies.json`。

## 依赖

- bilibili-api-python（已安装，每日自动更新）
- aiohttp（已安装）
- ffmpeg（已安装，音频转写时使用）
- opencc-python-reimplemented（可选，繁转简）

## 踩坑记录

详见 `references/api-notes.md`：WBI 签名、Cookie 管理、常见错误码、AI 字幕语言代码。
