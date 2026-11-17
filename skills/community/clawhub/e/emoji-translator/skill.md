# 🎭 emoji-translator

**400+ emoji，中英文双向翻译 + 智能内嵌，还能玩梗。**
**400+ emoji with CN↔EN bidirectional translation + smart inline embedding. Memes included.**

不只是「猫 → 🐱」，是完整的文字↔emoji互译系统。日常聊天、吐槽造梗、找emoji的终极工具。
Not just "cat → 🐱" — a full text↔emoji translation engine. Your ultimate toolkit for daily chat, meme crafting, and emoji discovery.

## 三种模式 · Three Modes

### ✨ 智能内嵌 · Smart Inline（推荐 Recommended）
emoji 直接插到原文关键词后面，保留原文，自然增强：
Emoji inserted directly after matching keywords — preserves the original text, enhances naturally:

```
输入 Input:  "今天开会加班写代码好累好饿"
输出 Output: 今天开会🤡加班💀写代码🤖好👍累😴好饿

输入 Input:  "I love pizza and coffee"  
输出 Output: I love😍 pizza🍕 and coffee☕
```

### 🔤 提取模式 · Extract
纯 emoji 列表，适合做签名 / 标题：
Bare emoji list, perfect for signatures or headlines:

```
输入 Input:  "我今天好开心啊"
输出 Output: 😀 👍 ❤️
```

### 🔡 反向翻译 · Reverse
emoji → 文字解释 / text explanation：

```
输入 Input:  "🤯 🔥 💯"
输出 Output: 爆炸头 火 满分
```

### 😏 自动玩梗 · Meme Mode

| 你说 You say | 它加 Adds | 你说 You say | 它加 Adds |
|--------------|-----------|--------------|-----------|
| 开会 meeting | 🤡 | 加班 overtime | 💀 |
| 摸鱼 slacking | 🐟 | 摆烂 giving up | 🛌 |
| 内卷 rat race | 🏃 | 崩溃 meltdown | 😭 |
| 累/困 tired | 😴 | 饿 hungry | 🤤 |

## 技术亮点 · Tech Highlights
- **400+ emoji 词库**：手写中英文关键词标注 · *400+ hand-annotated CN+EN keywords*
- **位置感知内嵌**：emoji 精准插在关键词后，不破坏句子结构 · *Position-aware insertion, never garbles your sentence*
- **最长匹配优先**：「写代码🤖」不会被拆成「写」+「代码」 · *Longest-match-first prevents "写"+"代码" from splitting "写代码"*
- **零依赖**：纯 Python，标准库 only · *Zero deps, stdlib only*

## 触发词 · Triggers

「翻译成emoji」「emojify」「解读emoji」「用emoji表达」「emoji翻译」「这段话加上emoji」「把emoji插进去」
