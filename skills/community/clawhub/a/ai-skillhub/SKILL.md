---
name: ai-skillhub
description: OpenClaw AI SkillHub 核心。支持两种触发方式：①「!skill URL」自动模式，AI 自动归纳关键词和分类；②「!skill 关键词 URL」手动模式，用户指定关键词。提取内容 → 生成原始内容.md + SKILL.md → 推送 GitHub。
---

# AI SkillHub — 全自动知识策展系统

## 命令格式

```
!skill <URL>              ← 自动模式，AI 自动归纳关键词和分类
!skill <关键词> <URL>     ← 手动模式，用户指定关键词
```

---

## ⚡ 第零步：立即回复用户（不得跳过）

收到命令的**第一件事**是回复：

```
✅ 收到！正在处理「{URL}」，请稍等...
```

然后才开始执行下面的步骤。

---

## 🗺️ 平台识别 → 执行卡速查表

**先看 URL，匹配平台，直接跳到对应执行卡，不要阅读其他部分。**

| URL 特征 | 平台 | 执行卡 |
|---------|------|--------|
| `youtube.com` 或 `youtu.be` | YouTube | → [执行卡 A] |
| `bilibili.com` | B站 | → [执行卡 B] |
| `mp.weixin.qq.com` | 微信公众号 | → [执行卡 C] |
| `douyin.com` 或 `v.douyin.com` | 抖音 | → [执行卡 D] |
| 其他所有网址 | 通用网页 | → [执行卡 E] |

---

## [执行卡 A] YouTube

### A1. 先跑字幕脚本（必须第一步，不得绕过）

```bash
python3 ~/.openclaw/scripts/yt_transcript.py "{url}"
```

**结果判断：**

✅ **输出包含 `"transcript"` 字段** → 提取成功，将 `transcript` 内容作为正文，进入 [Step 4 归类]

❌ **输出包含 `"error"` 字段** → 字幕不可用，进入 A2

---

### A2. 字幕失败 → 通知用户运行本地流水线

告知用户：

```
⚠️ 该视频没有字幕，需要在你的 Windows 本地下载音频后转写。

请在你的电脑上打开 PowerShell，运行：

powershell -ExecutionPolicy Bypass -File "C:\Users\admin\Documents\trae_projects\vps skill\yt_local_pipeline.ps1" "{url}" tiny

运行完成后，会在当前目录生成 yt_transcript_XXXXXX.txt 文件。
请把文件内容粘贴回来，我继续处理。
```

收到用户粘贴的内容后，将其作为正文，进入 [Step 4 归类]。

---

## [执行卡 B] B站

### B1. 检查 cookies 并下载音频

```bash
BILI_COOKIES="$HOME/.openclaw/cookies/bilibili.txt"
if [ -f "$BILI_COOKIES" ]; then
  COOKIES_ARG="--cookies $BILI_COOKIES"
else
  COOKIES_ARG=""
fi

python3 -m yt_dlp -x --audio-format mp3 --audio-quality 5 \
  $COOKIES_ARG \
  -o /tmp/content_audio.mp3 \
  "{url}" 2>&1
```

**结果判断：**

✅ **下载成功** → 进入 B2

❌ **下载失败且 cookies 不存在** → 告知用户：
```
❌ B站下载失败：需要登录 cookies。
cookies 文件应在：~/.openclaw/cookies/bilibili.txt
请联系管理员重新导出 cookies 后重试。
```

---

### B2. Whisper 转写

```bash
python3 -c "
import whisper
model = whisper.load_model('tiny')
result = model.transcribe('/tmp/content_audio.mp3', language='zh')
with open('/tmp/原始内容.txt', 'w', encoding='utf-8') as f:
    f.write(result['text'])
print('转写完成，字数:', len(result['text']))
"
```

> **模型选择**：默认 `tiny`。用户明确说「用 small」「用 medium」时才替换。

转写完成后，将 `/tmp/原始内容.txt` 内容作为正文，进入 [Step 4 归类]。

---

## [执行卡 C] 微信公众号

### C1. 第一步：必须先跑 wx_extract.py（不得跳过，不得用其他工具替代）

```bash
python3 ~/.openclaw/scripts/wx_extract.py "{url}"
```

**结果判断：**

✅ **输出 JSON 包含 `"content"` 字段且无 `"error"` 字段** → 提取成功，将 `content` 内容作为正文，进入 [Step 4 归类]

❌ **输出包含 `"error": "blocked"` 字段** → 进入 C2

---

### C2. 第二步：extract_content_from_websites 浏览器模式

```
extract_content_from_websites(
  url="{url}",
  mode="browser_only",
  prompt="提取微信公众号文章完整正文，包括标题和所有段落"
)
```

✅ 成功 → 将结果作为正文，进入 [Step 4 归类]

❌ 失败 → 进入 C3

---

### C3. 第三步：搜索引擎缓存

使用 `batch_web_search` 搜索：
1. `"{文章标题}" 全文`
2. `"{url中的短ID}" site:weixin.sogou.com`

✅ 找到完整内容 → 使用，注明「内容来自搜索缓存」，进入 [Step 4 归类]

❌ 未找到 → 进入 C4

---

### C4. 最终兜底：请用户提供

```
⚠️ 该微信文章受谷歌云 IP 限制，自动抓取失败。
请在微信中打开文章，复制全文后粘贴给我，我继续处理。
```

---

## [执行卡 D] 抖音

**直接告知用户，不要尝试任何下载：**

```
❌ 抖音视频无法处理。
原因：当前服务器（美国 Google Cloud IP）被抖音 API 封锁，无论是否有 cookies 均无效。
建议：若该内容同时发布在 B站或 YouTube，请提供对应链接。
```

---

## [执行卡 E] 通用网页（知乎 / 小红书 / 其他）

### E1. extract_content_from_websites

```
extract_content_from_websites(
  url="{url}",
  mode="browser_only",
  prompt="提取这个页面的完整正文内容，包括标题、所有段落，不要省略任何内容"
)
```

✅ 成功 → 进入 [Step 4 归类]

❌ 失败 → 进入 E2

---

### E2. 搜索引擎兜底

```
batch_web_search("{页面标题} 全文")
```

✅ 找到 → 进入 [Step 4 归类]

❌ 找不到 → 告知用户无法提取，请求直接粘贴内容

---

## [Step 4] 自动归类（仅自动模式）

> 手动模式（用户提供了关键词）跳过此步。

用 `llm-task` 分析内容，确定 `keyword` 和 `category`：

```json
{
  "prompt": "你是一个知识分类专家。请根据以下内容，输出：\n1. keyword（关键词）：2-6个字，概括内容主题，中文或英文均可，作为文件夹名使用（不含特殊字符）\n2. category（分类）：从以下分类中选一个最合适的：编程开发 / 法律金融 / 内容创作 / 商业运营 / 效率工具 / 健康生活 / 教育学习 / 其他\n3. reason（理由）：一句话说明分类依据\n\n【内容标题】：{title}\n【内容摘要（前500字）】：{content[:500]}\n\n严格按 JSON 格式输出：{\"keyword\": \"...\", \"category\": \"...\", \"reason\": \"...\"}",
  "model": "minimax/auto"
}
```

---

## [Step 5] 保存原始内容

写入 `/tmp/原始内容.md`：

```markdown
# 原始内容记录

## 来源信息
- URL：{url}
- 平台：{platform}
- 关键词：{keyword}
- 分类：{category}
- 归类方式：{自动归类 / 用户指定}
- 提取时间：{datetime}
- 提取方式：{方式，例：YouTube字幕API / B站yt-dlp+Whisper(tiny) / wx_extract.py / 本地流水线+Whisper(tiny)}

## 内容正文
{完整内容，一字不删}
```

---

## [Step 6] 事实抽取

用 `llm-task` 扫描全文，重点检测财务/结果类关键词：

```json
{
  "prompt": "你是一个事实抽取专家。从以下内容中抽取所有关键事件，特别关注【结果、状态、金额、是否成功】。\n\n必须扫描：追回、退款、退回、赔付、胜诉、执行成功、失败、已追回、已退款、钱、款、金额、赔偿\n\n输出格式：\n## 关键事件\n| 事件 | 结果状态 | 证据句子 | 时间/金额 |\n\n## financial_outcome\n- has_financial_outcome: true/false\n- outcome_summary:\n- evidence_sentence:\n\n注意：必须逐句扫描，不得跳段",
  "input": "{原始内容全文}"
}
```

---

## [Step 7] 生成 SKILL.md

写入 `/tmp/SKILL.md`：

```markdown
# {关键词} Skill

## ⚠️ 关键结果
{如果 has_financial_outcome=true，用粗体标注结果}

## 核心事件
{从 Step 6 events 转化}

## 详细内容
{结构化总结}

## 重要事实清单
{其他关键事实}
```

---

## [Step 8] 推送 GitHub

```bash
export GITHUB_TOKEN=$(grep GITHUB_TOKEN ~/.openclaw/.env | cut -d= -f2)
export GITHUB_REPO=$(grep GITHUB_REPO ~/.openclaw/.env | cut -d= -f2)
export GITHUB_BRANCH=$(grep GITHUB_BRANCH ~/.openclaw/.env | cut -d= -f2-)

rm -rf /tmp/skillhub_repo
git clone "https://${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git" /tmp/skillhub_repo

mkdir -p "/tmp/skillhub_repo/skills/{category}/{keyword}"
cp /tmp/原始内容.md "/tmp/skillhub_repo/skills/{category}/{keyword}/原始内容.md"
cp /tmp/SKILL.md "/tmp/skillhub_repo/skills/{category}/{keyword}/SKILL.md"

cd /tmp/skillhub_repo
git config user.email "openclaw@bot"
git config user.name "OpenClaw Bot"
git add .
git commit -m "Add skill [{category}/{keyword}] - $(date '+%Y-%m-%d')"
git push origin ${GITHUB_BRANCH:-main}

rm -rf /tmp/skillhub_repo
```

---

## 完成通知

```
✅ Skill 已保存：【{keyword}】
🏷️ 分类：{category}
📄 原始内容：skills/{category}/{keyword}/原始内容.md
🧠 分析摘要：skills/{category}/{keyword}/SKILL.md
📦 来源：{url}
🔗 GitHub：https://github.com/{GITHUB_REPO}/tree/main/skills/{category}/{keyword}
📌 提取方式：{方式}
```

---

## 🚫 禁止事项（违反即为错误）

1. **禁止对 YouTube 直接用 yt-dlp 下载**——VPS 是谷歌云 IP，必然 403，不要尝试
2. **禁止对微信公众号跳过 wx_extract.py**——必须先跑脚本，不能直接用浏览器工具或 llm-task
3. **禁止用 `llm-task` 访问任何 URL**——llm-task 只做文本推理，没有联网能力
4. **禁止对抖音尝试任何下载**——直接告知用户不可用
5. **禁止只推送一个文件**——必须同时推送 `原始内容.md` + `SKILL.md`
6. **禁止省略或截断原始内容**——原始内容必须一字不删全量保存

---

## 工具与环境

| 工具/路径 | 用途 |
|-----------|------|
| `python3 ~/.openclaw/scripts/yt_transcript.py` | YouTube 字幕提取 |
| `python3 ~/.openclaw/scripts/wx_extract.py` | 微信公众号提取 |
| `python3 -m yt_dlp` | B站/西瓜视频音频下载 |
| `whisper`（Python 库） | 音频转写 |
| `~/.openclaw/cookies/bilibili.txt` | B站登录 cookies |
| `~/.openclaw/.env` | GitHub Token / Repo 配置 |
| `C:\...\yt_local_pipeline.ps1` | YouTube 无字幕时本地下载流水线（用户在 Windows 本地运行） |
| `exec` | 在 VPS 执行 shell 命令 |
| `extract_content_from_websites` | 网页/浏览器内容提取 |
| `batch_web_search` | 搜索引擎兜底 |
| `llm-task` | 纯文本推理（不能联网） |
