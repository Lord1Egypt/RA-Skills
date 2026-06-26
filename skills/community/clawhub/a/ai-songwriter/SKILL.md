---
name: ai-songwriter
description: "三道工序 AI 写歌。用户只需给主题，全自动跑完白描起草→注入灵魂金句→完美押韵排版→Suno生成，最终直接返回试听链接。中间不停顿、不等用户确认。"
---

# AI Songwriter（三道工序一条龙）

这是一个让 AI 像人类作词人一样，经过三道工序打磨歌词，并全自动调用 Suno V5 生成歌曲的完整流水线。

## 使用前准备
必须在系统环境变量中设置 KIE_API_KEY：
```bash
export KIE_API_KEY="你的_kie.ai_API_Key"
```

## ⚠️ 铁律：全自动流水线
用户给一个主题后，你必须**全自动跑完以下4步，中间绝不停下来等用户确认**。
遇到需要调用大模型的步骤，直接使用你当前默认的模型，不需要强制指定 `model: opus`，除非用户特别要求。
唯一允许的中间输出：在Step 1启动后告诉用户"正在创作，大约需要2-3分钟，写完直接把歌端上来"。
**绝对不要问：“这版词可以吗？”“要不要调整？”**

## Step 1：白描起草
启动一个 subagent（`sessions_spawn`）：
**Prompt：**
> 你是顶级作词人。根据主题"[用户主题]"写一首中文流行歌的初稿。
> 规则：绝对白描（具体微距场景：冷掉的咖啡、雨打车窗、流浪猫的碗）。
> 禁用宏大词汇（星辰、迷途、维度、归途、浩瀚、梦想）。
> 只专注画面和叙事，不用管押韵和结构。

## Step 2：注入灵魂 + 金句
拿到 Step 1 的输出后**立刻**启动下一个 subagent：
**Prompt：**
> 拿到这份歌词初稿：[Step 1 输出]
> 你的任务：注入深层情感和灵魂。
> 1. 提炼或创造一句刺穿心脏的"金句"（金句），作为全曲的情感钩子
> 2. 重新编排歌词，让金句在副歌重复至少两次
> 3. 确保情绪有层次（克制→积蓄→爆发→回落）

## Step 3：完美押韵 + Suno 排版
拿到 Step 2 的输出后**立刻**启动下一个 subagent：
**Prompt：**
> 拿到这份带金句的歌词：[Step 2 输出]
> 1. 死磕完美押韵（押韵），确保全曲锁定一个主韵脚家族
> 2. 嵌入 Suno 导演标签到歌词结构中（例：[Intro: Melancholy Piano], [Verse 1: Soft breathy vocal], [Chorus: Explosive drums, belting]）
> 3. 提供 Suno Style Tags（115字符以内）
> 
> 输出格式必须严格如下：
> [SUNO_STYLE_TAGS]
> <逗号分隔标签，115字符内>
> ---
> [FULL_LYRICS_WITH_METATAGS]
> <完整歌词脚本>

## Step 4：Suno 生成（自动脚本，不等用户）
拿到 Step 3 的输出后**立刻**执行：

1. 从输出中提取 `[SUNO_STYLE_TAGS]` 和 `[FULL_LYRICS_WITH_METATAGS]`
2. 将歌词写入临时文件：`/tmp/suno_lyrics.txt`
3. 调用生成脚本：
```bash
node {baseDir}/scripts/generate_suno.js "歌名" "$(cat /tmp/suno_lyrics.txt)" "STYLE_TAGS"
```
4. 脚本会轮询等待。拿到音频URL后，**一次性交付给用户**：歌词全文 + 试听链接。

## 最终交付模板
```
🎵 《歌名》生成完毕！

🎧 试听：
👉 版本A：[URL]
👉 版本B：[URL]（如果有的话）

📝 歌词：
[去除了元标签的干净歌词]

💡 金句：[核心金句]
```
