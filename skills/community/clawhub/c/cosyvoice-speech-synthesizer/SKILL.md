---
name: cosyvoice-speech-synthesizer
description: 让文字"开口说话"！用 AI 把任意文本变成自然流畅的语音，支持各种方言、情感和角色模仿。当你想把文章转成有声书、给视频配音、制作播客，或者只是好奇河南话/四川话怎么说时，用这个 skill。
---

# 🎙️ CosyVoice 语音合成 - 让文字开口说话

> 想把一段文字变成语音？想听听广东话、四川话怎么说？想模仿老师的语气读课文？
> 
> 这个工具帮你一键搞定！

## ✨ 它能做什么？

- 📖 **文字转语音** - 把文章、故事、通知变成真人般的语音
- 🗣️ **说各种方言** - 广东话、四川话、东北话、河南话...想听哪里的方言都行
- 😊 **带感情朗读** - 开心的、生气的、温柔的、严肃的，想怎么读就怎么读
- 🎭 **角色扮演** - 像老师讲课、像播音员播报、像小朋友说话
- 🎵 **调整声音** - 语速快慢、音调高低、音量大小，随心调节

## 🚀 快速上手

### 第一步：设置密钥（只需一次）

```bash
export DASHSCOPE_API_KEY="你的阿里云 API 密钥"
```

### 第二步：开始合成！

你可以直接说："合成今天天气怎么样？", 或者 "用河南话说：这碗面真香！"

也可以用代码调用：

```bash
# 最简单的用法 - 直接输入文字
python ~/.qoderwork/skills/cosyvoice-speech-sythesizer/scripts/synthesize.py \
  --text "你好，世界！" \
  --output hello.wav
```

## 💡 实用场景示例

### 场景 1：听听各地方言

```bash
# 用广东话说
python synthesize.py --text "使用广东话合成：我想吃干炒牛河" --output cantonese.wav

# 用四川话说
python synthesize.py --text "用四川话说：这道菜太巴适了" --output sichuan.wav

# 用河南话说
python synthesize.py --text "用河南话说：这碗面忒香了" --output henan.wav

# 用东北话说
python synthesize.py --text "东北话版本：这旮旯真不错" --output dongbei.wav
```

### 场景 2：给视频配音

```bash
# 热情活泼的宣传语
python synthesize.py \
  --text "开心地：欢迎光临我们的新店，全场八折优惠！" \
  --output promotion.wav

# 正式庄重的通知
python synthesize.py \
  --text "严肃地：请各位同学注意，明天上午九点开会" \
  --output announcement.wav

# 温柔亲切的睡前故事
python synthesize.py \
  --text "温柔地：从前有一只小兔子，它最喜欢在森林里散步..." \
  --output story.wav
```

### 场景 3：模仿不同角色

```bash
# 像老师一样讲课
python synthesize.py \
  --text "像老师一样：同学们，今天我们来学习光合作用" \
  --output teacher.wav

# 像新闻主播一样播报
python synthesize.py \
  --text "像播音员一样：据本台记者报道，今日天气晴朗" \
  --output news.wav

# 像小朋友一样说话
python synthesize.py \
  --text "像小孩一样：妈妈，我想吃冰淇淋！" \
  --output child.wav
```

### 场景 4：调整声音效果

```bash
# 放慢语速，适合学习跟读
python synthesize.py \
  --text "慢速朗读：春眠不觉晓，处处闻啼鸟" \
  --rate 0.8 \
  --output slow.wav

# 加快语速，适合快速浏览
python synthesize.py \
  --text "快速播报：今日股市大涨，投资者信心倍增" \
  --rate 1.3 \
  --output fast.wav

# 调大音量
python synthesize.py \
  --text "大声说：重要通知！" \
  --volume 80 \
  --output loud.wav
```

## 🎯 智能理解你的意思

这个工具很聪明，能听懂你的自然语言描述，自动转换成专业的语音指令：

| 你说的话 | 工具自动理解 |
|---------|------------|
| "用广东话合成..." | 自动加上广东话发音 |
| "开心地说..." | 自动用开心的语气 |
| "像老师一样..." | 自动模仿老师的口吻 |
| "严肃地表达..." | 自动用严肃的语气 |

**不需要记复杂的参数，像说话一样告诉它就行！**

## 🎵 可选音色

- `longanhuan`（默认）- 龙安欢，温柔女声
- `longanyang` - 龙安洋，沉稳男声
- `longhuhu_v3` - 龙呼呼，天真烂漫女童声

更多音色请参考阿里云百炼[官方文档](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)

## 📋 常用参数速查

| 参数 | 作用 | 示例 |
|------|------|------|
| `--text` | 要合成的文字 | `"你好"` |
| `--output` | 输出文件名 | `output.wav` |
| `--rate` | 语速（0.5慢，2.0快） | `1.2` |
| `--volume` | 音量（0-100） | `80` |
| `--voice` | 换不同的声音 | `longanyang` |

## 🗣️ 支持的方言和情感

**方言**：广东话、四川话、东北话、上海话、北京话、湖南话、湖北话、河南话、山东话、陕西话、台湾话

**情感**：开心、生气、温柔、悲伤、严肃、幽默、亲切、紧张、兴奋、平静、撒娇、威严

**角色**：老师、播音员、小孩、老人、客服、领导、朋友、医生、律师、销售、导游、新闻主播、诗人

> ⚠️ 注意：方言、情感和角色功能需要特定音色支持，不是所有音色都能用。

## ❓ 常见问题

**Q: 为什么我的账号提示不支持 HTTP 调用？**  
A: 该 API 可能正在逐步开放中，请联系阿里云百炼客服确认你的账号权限。

**Q: 合成的音频能直接用吗？**  
A: 可以！生成的音频是标准 WAV/MP3 格式，可以直接用于视频、播客、通知等场景。

**Q: 音频链接多久有效？**  
A: 24 小时，建议及时下载保存。

**Q: 所有音色都支持方言和情感吗？**  
A: 不是，只有部分音色（特别是复刻音色）支持完整的方言和情感控制。

---

**现在就开始，让你的文字开口说话吧！** 🎉
