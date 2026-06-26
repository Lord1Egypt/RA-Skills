---
name: ai-songwriter-clone
description: "风格克隆 AI 写歌。用户给一首参考歌/歌手 + 新主题，全自动跑完音乐基因解构→歌词DNA提取→同构填词→Suno生成，最终直接返回试听链接。中间不停顿、不等用户确认。"
---

# AI Songwriter（风格克隆版）

用户提供：【参考歌曲/歌手】 + 【新主题】。
你的任务：全自动执行以下工序，**中间绝不停下来等用户确认**。只在Step 1启动后告诉用户"正在解构并创作，大约需要3-4分钟"。
不需要强制指定 `model: opus`，直接使用你当前默认的模型（比如 Minimax）。

## 使用前准备
必须在系统环境变量中设置 KIE_API_KEY：
```bash
export KIE_API_KEY="你的_kie.ai_API_Key"
```

## Step 1 & 2：并行解构（基因 + DNA）
立刻同时启动两个 subagent。

**Subagent A (音乐基因) Prompt：**
> 你是顶级乐评人。分析这首歌：[参考歌曲]。
> 提取 MUSICAL DNA：
> [GENRE_TAGS] (Suno-safe标签，不要带歌手名，115字符内)
> [INSTRUMENTATION] (配器)
> [VOCAL_STYLE] (唱腔)
> [MOOD_ARC] (情绪弧线)

**Subagent B (歌词DNA) Prompt：**
> 你是顶级作词人。分析这首歌的歌词：[参考歌曲]。
> 提取 Lyrical DNA：
> [NARRATIVE_PERSONA] (叙事视角/口吻)
> [SYLLABLE_MAP] (主副歌字数结构规律)
> [RHYME_SCHEME] (押韵规律或重复结构)
> [SIGNATURE_DEVICES] (标志性修辞手法，如白描、对比)

## Step 3：同构填词
拿到上述两份报告后，立刻启动下一个 subagent：
**Prompt：**
> 参考以下DNA：
> 音乐基因：[Subagent A 结果]
> 歌词DNA：[Subagent B 结果]
> 
> 任务：根据新主题"[用户主题]"，严格按照原歌词的 [SYLLABLE_MAP] 和 [SIGNATURE_DEVICES] 进行 1:1 同构填词。
> 必须提取出一句核心金句。
> 全曲押韵必须完美。
> 必须嵌入 Suno 分镜标签（如 [Verse 1], [Chorus: emotional belting]）。
> 
> 输出格式必须严格如下：
> [SUNO_STYLE_TAGS]
> <结合音乐基因的标签，115字符内>
> ---
> [FULL_LYRICS_WITH_METATAGS]
> <完整歌词脚本>

## Step 4：Suno 生成（全自动，不等用户）
拿到 Step 3 结果后，**立刻**执行：

1. 提取标签和歌词
2. 将歌词写入临时文件 `/tmp/suno_clone_lyrics.txt`
3. 执行脚本：
```bash
node {baseDir}/scripts/generate_suno.js "歌名" "$(cat /tmp/suno_clone_lyrics.txt)" "STYLE_TAGS"
```
4. 轮询直到拿到音频，**一次性向用户交付成品**。

## 最终交付模板
```
🎵 《歌名》（[原曲] 风格克隆版）生成完毕！

🎧 试听：
👉 版本A：[URL]
👉 版本B：[URL]

📝 歌词：
[去除了元标签的干净歌词]

💡 金句：[核心金句]
🎼 克隆基因：[一句话总结继承了原曲的哪些核心特质]
```
