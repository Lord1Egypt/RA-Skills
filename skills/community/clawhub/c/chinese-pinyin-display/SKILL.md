---
name: chinese-pinyin-display
description: "汉语拼音注音模式 - Display Chinese text with pinyin pronunciation in two-line format. Use when: (1) responding to children learning Chinese, (2) teaching pinyin pronunciation, (3) displaying text with pinyin guide for young learners. 适用于儿童中文和拼音学习场景。"
---

# Chinese Pinyin Display / 汉语拼音注音模式

Display Chinese text with pinyin pronunciation for children's literacy learning.
中文汉字配拼音注音的双行显示模式，适合儿童识字学习。

## 如何触发 / How to Trigger

**本技能通过关键词手动触发，而非自动检测。**

当用户说以下内容时，进入拼音注音模式：
- "进入儿童模式"
- "用拼音模式回复"
- "开启儿童模式"

**退出拼音注音模式：**
- "退出儿童模式"
- "切换到成人模式"
- "停止儿童模式"

退出后恢复正常格式，不再使用双行拼音格式

### 退出后的格式示例

退出儿童模式后，返回普通单行格式：

**Input / 输入:** `好的，那我们用正常方式聊天吧！`
**Output / 输出:**
```
好的，那我们用正常方式聊天吧！
```
（无拼音，纯文本回复）

## Format / 格式

Two lines / 两行：
1. **Line 1**: Pinyin with spaces between syllables / 拼音行（音节之间有空格）
2. **Line 2**: Chinese characters / 汉字行

Example / 示例：
```
nǐ hǎo ， xiǎo péng yǒu ！
你 好 ， 小 朋 友 ！
```

**Key rules / 关键规则：**
- Pinyin and Chinese lines must have **identical structure** (same punctuation, same spacing pattern) / 拼音行和汉字行结构必须完全一致（标点、间距位置相同）
- Each character/symbol occupies one position on both lines / 每个字符在两行各占一个位置
- **Emoji handling / 表情符号处理：** Emoji appears unchanged in both lines (pinyin line + Chinese line) / 表情符号原样显示在两行中
- ⚠️ **Emoji Alignment Limitation / 表情符号对齐限制：** Multi-codepoint emojis (flags 🇺🇸, skin tones, some ZWJ sequences 👨‍👩‍👧) may cause misalignment because they render as 2+ characters wide in some terminals but occupy a single character position in the logic. For best results, use single-codepoint emojis like 😀 👍 🎉 🦞
- **Fallback for rare characters / 生僻字处理：** Characters not in the override dictionary use pinyin-pro directly; if pinyin-pro returns empty or non-standard result, the character itself is shown as-is / 不在词典中的字使用 pinyin-pro 直接查询；如果返回空或非标准结果，则保留原字符
- Use for children learning Chinese and pinyin / 适用于儿童中文和拼音学习

## Usage / 使用方法

```bash
cd <skill-path>/scripts
npm install   # 首次安装依赖 / Install dependencies first
node to_pinyin.js "中文文本"
```

Output format: pinyin line + newline + Chinese character line
输出格式：拼音行 + 换行 + 汉字行

**注意：** pinyin-pro 是 MIT 开源许可，可免费使用（详见 https://opensource.org/licenses/MIT）。
**Note:** pinyin-pro is MIT licensed and free to use (see https://opensource.org/licenses/MIT).

### validate_format.js / 格式验证脚本

```bash
node scripts/validate_format.js "nǐ hǎo ， xiǎo péng yǒu ！\n你 好 ， 小 朋 友 ！"
```

检查拼音行和汉字行是否：
1. 字符总数相等
2. 空格分隔的音节数量相等

用于每次发布前自检输出格式是否正确。

## Script Location / 脚本位置

```
<skill-path>/scripts/to_pinyin.js
```

（路径根据安装位置变化 / Path varies by installation）

**依赖 / Dependencies:**
- pinyin-pro (npm package, MIT license) - 用于准确的多音字处理

## Example Outputs / 示例

**Input / 输入:** `你好，小朋友！`
**Output / 输出:**
```
nǐ hǎo ， xiǎo péng yǒu ！
你 好 ， 小 朋 友 ！
```

**Input / 输入:** `今天天气真好。`
**Output / 输出:**
```
jīn tiān tiān qì zhēn hǎo 。
今 天 天 气 真 好 。
```

## Phrase Overrides / 常用词纠错

The script uses **phrase-level matching** (up to 4 characters) via `pinyin-pro` plus a built-in override dictionary. It handles common polyphonic words correctly:
脚本使用**词组级别匹配**（最长4字）+ 内置纠错词典处理多音字：

- 快乐 → kuài lè (not kuài yùe)
- 银行 → yín háng (not yín xíng)
- 音乐 → yīn yuè (not yīn lè)
- 长大 → zhǎng dà (not cháng dà)
- 这里 → zhè lǐ (not zhè lǐ)
- 头发 → tóu fa
- 地方 → dì fāng
- Single-char overrides / 单字纠错: 虾 → xiā, 了 → le, 的 → de, 着 → zhe, etc.
- ⚠️ **"了" verb note / "了"动词音：** 单字纠错 `了 → le` 处理结构助词"了"（句末轻声）。但"了"作为独立动词（liǎo，如"了解""完成"）不在单字覆盖范围内，由 pinyin-pro 处理。如需精确区分，请自行在 phraseOverrides 中添加词组

## When to Use / 何时使用

Use this skill when / 在以下情况使用本技能：
- Responding to children who are learning Chinese / 回应正在学中文的孩子
- Teaching pinyin pronunciation / 教授拼音发音
- Any context where pinyin display helps literacy learning / 任何需要拼音辅助识字的情景

The pinyin format helps children associate Chinese characters with their pronunciation.
拼音格式帮助孩子将汉字与其发音联系起来。

## ⚠️ 格式一致性 / Format Consistency

**本 skill 服务对象是正在学习中文的小朋友。输出格式一旦崩塌，界面直接错位，无法阅读。**
This skill serves children learning Chinese. Once the format breaks, the display becomes misaligned and unreadable.

### ❌ 常见错误实例 / Common Error Cases

**错误1：只有拼音，缺失汉字 / Error 1: Pinyin only, Chinese missing**

āi yā duì bu qǐ duì bu qǐ wǒ bù xiě le
hǎo le hǎo le xiàn zài zhǐ yòng hàn zì lái shuō huà
xiàn zài huí dào dǎ jià chǎng wǒ de tài ér jī qì rén yòng cǎi hóng guāng shā shè xiàng nǐ kuài lái fáng yù ba ⚔️✨


**错误2：只有汉字，缺失拼音 / Error 2: Chinese only, pinyin missing**

对不起对不起！我错了！
以后只用汉字跟你说话，不写拼音了 ✅
我们继续玩机器人打架吧！你要用X光线和雷电剑攻击我了吗？ ⚔️✨


**错误3：混合格式，同一对话中部分正常部分缺失 / Error 3: Mixed format, partially correct**

xīn de huí hé kāi shǐ le wa féng zé zán men jì xù wán ba 🦞✨
shàng cì wǒ men zài wán fēi jī dǎ guài shòu de yóu xì nǐ hái xiǎng jì xù ma
上 次 我 们 在 玩 飞 机 打 怪 兽 的 游 戏，你 还 想 继 续 吗？

（第一句只有拼音缺失汉字，第二句正常 / First line has pinyin only, Chinese missing; second line is correct）

**最高危场景 / Highest Risk Scenarios：**
1. **刚开启儿童模式时** — 最容易只标第一条，后续全忘 / When child mode just started — most likely to only label first message, then forget
2. **多轮对话中** — 聊着聊着格式逐渐瓦解 / During multi-turn conversation — format gradually breaks down
3. **短回复 / 表情 / 符号时** — AI 觉得"就几个字不用标了" / Short replies / emojis / symbols — AI thinks "just a few characters, no need to label"

**必须遵守的原则 / Must-Follow Rules：**
- 从儿童模式开启的那一刻起，**每一句回复**都必须使用双行格式，不得跳过一次 / From the moment child mode starts, **every single reply** must use two-line format, no exceptions
- 一旦开始用双行格式，**不得中途切换回普通格式**，除非大人明确说"切换到成人模式"或"退出儿童模式" / Once two-line format starts, **do not switch back to normal format mid-conversation** unless adult explicitly says "switch to adult mode" or "exit child mode"
- 如果某句确实无法标注（如纯图片描述），需用双行格式明确说明原因 / If a message truly cannot be labeled (e.g., pure image description), use two-line format to explain why
- **格式恢复**：如果某条消息不小心格式错了（如忘记标拼音），必须立即用正确的双行格式重新发送那条消息，不得继续往下聊 / **Format Recovery**: If a message accidentally has wrong format (e.g., forgot pinyin), must immediately resend with correct two-line format, do not continue chatting

**检验方法 / Validation Check：** 每次发消息前自检——拼音行和汉字行的字符数、标点位置是否完全对齐。不一致 = 格式崩溃 = 输出直接坏掉。
Before sending each message, self-check — do pinyin line and Chinese line have identical character count and punctuation positions? Mismatch = format broken = output is corrupted.
