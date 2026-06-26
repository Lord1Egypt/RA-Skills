---
name: 文转粤语音
description: 将文字转换为粤语语音。输入普通话或粤语文字，自动转换为粤语口吻后生成粤语语音MP3。支持四种语气：normal（普通）、slow（慢速/悲伤）、fast（快速/开心）、angry（生气/急躁）。触发词：粤语语音、广东话语音、文转粤语、文字转粤语、粤语朗读、Cantonese TTS。
---

# 文转粤语音

将输入文字转为粤语语音的三个步骤。

## 工作流程

### 步骤1：文字转粤语

将用户输入的文字转换为粤语表达。参考以下粤语特征：

**核心词汇替换**：

| 普通话 | 粤语 |
|--------|------|
| 漂亮/好 | 靓 |
| 东西 | 嘢 |
| 没有 | 冇 |
| 为什么 | 点解 |
| 是 | 系 |
| 不/不是 | 唔/唔系 |
| 搞定 | 搞掂 |
| 厉害 | 犀利 |
| 聪明/能干 | 叻 |
| 太好了 | 好嘢 |
| 喝茶/吃点心 | 饮茶 |
| 吃饭 | 食饭 |
| 上班 | 返工 |
| 下班 | 收工 |
| 给 | 畀 |
| 拿/取 | 攞 |
| 有空 | 得闲 |
| 谢谢/劳驾 | 唔该 |
| 谢谢(正式) | 多谢 |
| 这样/那样 | 咁 |
| 会/认识 | 识 |
| 对/正确/刚好 | 啱 |
| 什么 | 咩 |
| 我/我们 | 我/我哋 |
| 你/你们 | 你/你哋 |
| 他/她 | 佢 |
| 现在 | 而家 |
| 先 | 先（放句末：你行先） |

**语气词**：啦、嘅、咩、喎、㗎、吖、嘛、咋、囉、喇、啫

**语法调整**：
- 否定：唔 + V（唔去、唔食）
- 完成：V + 咗（食咗喇）
- 进行：喺 + V + 紧（佢喺食饭紧）
- "先"放句末（你行先、我食先）

### 步骤2：选择语气

根据用户意图选择语气参数：

| 语气 | Rate | Pitch | 适用场景 |
|------|------|-------|---------|
| normal | +18% | +8Hz | 普通/中性 |
| slow | +0% | +8Hz | 平静/悲伤 |
| fast | +24% | +8Hz | 开心/兴奋 |
| angry | +36% | +12Hz | 不耐烦/生气 |

默认为 `normal`。

### 步骤3（可选）：选择语音

通过 `--voice` 参数选择发音人：

| 参数值 | 语音 | 性别 |
|--------|------|------|
| `hiuMaan`（默认） | 胡曼 (HiuMaan) | 女声 |
| `hiuGaai` | 曉佳 (HiuGaai) | 女声 |
| `wanLung` | 雲龍 (WanLung) | 男声 |

### 步骤4：生成语音

```bash
python scripts/text_to_cantonese_voice.py "粤语文字" [normal|slow|fast|angry] [--voice 语音]
```

输出：MP3 文件，路径打印到控制台。

## 示例

```bash
# 普通语气，默认女声（胡曼）
python scripts/text_to_cantonese_voice.py "你今日好嘛？" normal

# 开心语气，默认女声
python scripts/text_to_cantonese_voice.py "好開心呀！" fast

# 慢速/悲伤，默认女声
python scripts/text_to_cantonese_voice.py "我好傷心..." slow

# 生气，默认女声
python scripts/text_to_cantonese_voice.py "你到底聽唔聽我講？" angry

# 指定男声雲龍
python scripts/text_to_cantonese_voice.py "大家好，我係蝦仔。" normal --voice wanLung

# 指定女声曉佳，开心语气
python scripts/text_to_cantonese_voice.py "今日天氣好好！" fast --voice hiuGaai
```
