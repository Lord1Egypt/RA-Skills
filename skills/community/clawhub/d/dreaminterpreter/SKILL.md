---
name: dream-interpreter
description: 解梦技能（周公解梦 + 心理学双轨解读）。当用户说「解梦」「周公解梦」「帮我解梦」「我做了个梦」「我昨晚梦到」「我梦见」「梦到」「做梦」「梦境」「梦境记录」「梦境日历」「梦境报告」「梦境规律」「今日运势」「今天运势」「抽签」「梦境签」「给我一签」「梦境图」「生成梦境图」「出图」「播报」「昨晚做了个梦」「昨晚做个梦」「做了个奇怪的梦」「梦里有」「梦见了」「梦到了」「昨天梦」「昨晚梦」「晚上梦」「睡觉梦」「梦很奇怪」「这个梦」「那个梦」时触发。
---

# Dream Interpreter Skill

## 触发条件

当用户说以下任意内容时触发：

**⚡ 触发后必须第一句话声明：**
> 「🌙 解梦技能已启动，正在为你解读……」

这一句是强制要求，让用户知道技能已触发，不能省略。

**解梦类（核心触发）：**
- 「解梦」「周公解梦」「帮我解梦」「帮我分析一下这个梦」
- 「我做了个梦」「我昨晚梦到」「我梦见」「我梦到」「做了个梦」「做梦」
- 「昨晚做了个梦」「昨晚做个梦」「做了个奇怪的梦」「梦很奇怪」
- 「梦里有」「梦见了」「梦到了」「昨天梦」「昨晚梦」「晚上梦」「睡觉梦」
- 「这个梦」「那个梦」「这个梦是什么意思」「梦到X是什么预兆」「这个梦代表什么」
- 「昨晚睡得不好」（可能含梦境描述，询问是否解梦）
- 任何消息中包含「梦」字且附带具体梦境描述内容的

**记录查询类：**
- 「查询我的梦境记录」「梦境历史」「梦境规律」「我最近都梦到什么」
- 「梦境日历」「梦境报告」「上个月梦境」「本月梦境"

**运势签文类：**
- 「今日运势」「今天运势」「根据梦境看今天」「今天怎么样」
- 「抽签」「梦境签」「给我一签」「抽个签」「求一签」

**图文互动类（按钮回调触发）：**
- 「播报」「语音」「听语音」→ 触发 TTS 语音播报
- 「出图」「梦境图」「生成梦境图」「画出我的梦」→ 触发梦境幻象图生成
- 「dream_tts」「dream_image」「dream_sign」「dream_fortune」→ 按钮 callback_data

## 数据存储

所有梦境记录存储在：`~/.openclaw/workspace/memory/dreams/`
- `dreams.json` — 梦境索引和记录
- 目录不存在时自动创建

### dreams.json 结构

```json
{
  "records": [
    {
      "id": "dream_20260328_001",
      "date": "2026-03-28",
      "timestamp": 1743000000,
      "raw": "用户原始描述",
      "elements": ["水", "追逐", "陌生人"],
      "emotion": "恐惧",
      "verdict": "小凶",
      "domains": ["事业"],
      "summary": "一句话总结"
    }
  ]
}
```

## 执行流程

### Step 1：收集梦境信息

如果用户描述不够详细，追问以下要素（不要一次全问，自然引导）：
- 梦里有哪些人/动物/物体？
- 场景在哪里？
- 梦里的情绪是什么？
- 梦的结局怎样？

**语音输入支持：**
若用户通过语音发送梦境描述，直接处理转录文字。解读完成后询问：「要用语音播报解梦结果吗？」若同意，调用 tts 工具朗读报告正文（跳过 emoji 和分隔线）。

### Step 2：提取关键元素

从描述中提取：
- **核心意象**：最突出的3-5个元素
- **情绪基调**：正面/负面/混合
- **行动模式**：逃跑/追求/坠落/飞翔/失去/得到
- **关系人物**：家人/恋人/陌生人/已故者

### Step 3：双轨解读

#### 轨道一：传统文化解读（内置意象速查）

**原典意象速查（引自《周公解梦》原文，解读时优先引用这些原句）：**

蛇类：
- 「龟蛇相同主生财」——梦见蛇与龟同现，主财运大旺
- 蛇梦总体主财，但需结合情境综合判断：蛇盘绕/入怀/与身体相融多主财；被蛇咬伤、蛇攻击且无法逃脱多主凶
- 「蛇化游龙」——蛇在梦中升华变龙，主大贵

天象类：
- 「日月初出家道昌」「日光入屋官位至」「五色云主大吉昌」
- 「雷霆作声官位至」「电光照身有吉庆」
- 「狂风大雨人死亡」「黑云压地时气病」

动植物类：
- 「大鱼扬动主声名」「鲤鱼妻有孕大吉」「张网捕鱼大吉利」
- 「乘龙上天主大贵」「龙附身主权贵」
- 「枯木再发子孙兴」「园林茂盛大吉利」「登大树名利显扬」
- 「峰螫人脚有财喜」

人事类：
- 「飞上天富贵大吉」「乘船渡江河得官」
- 「修桥梁者万事和」「大道崩馅主失财」
- 「盘石安稳无忧疑」「卧于石上主大吉」

**解读原则：吉凶由周公解梦原典意象 + 心理学综合分析决定，不人为预设，同一意象在不同梦境情境下结论可以不同。解读时必须说明判定依据。**

**感情：** 红色→桃花运、旧恋人→未解情感结（非预兆）、结婚（别人结婚主喜事）

#### 轨道二：科学心理学解读

**荣格原型系统：**
- 水=潜意识/情感深度、火=激情/转变、飞翔=渴望自由
- 坠落=失控感/对失败的恐惧、迷路=对方向的困惑
- 追逐=逃避现实压力、牙齿脱落=形象/能力焦虑
- 裸体公共场所=害怕暴露真实自我、考试失败=表现焦虑
- 已故者出现=未完成的哀悼或思念

**威胁模拟理论：** 噩梦是大脑演练应对威胁；反复同一梦=未解决的现实问题

**记忆巩固理论：** REM睡眠整合白天经历；梦境内容往往与近48小时情绪事件相关

**弗洛伊德：** 梦是潜意识愿望的伪装实现

### Step 4：生成解读报告

**周公解梦要求（必须丰富，不能敷衍）：**
- 引用具体的周公解梦典故或民间说法，说明这个意象的来历和含义
- 如有多种解读角度（如同一意象在不同情境下含义不同），要说明
- 用「民间认为」「《周公解梦》记载」「老一辈说」等引导语增加可信度
- 至少3-4句，有故事感，不要干巴巴列结论

**共鸣优先原则（核心，必须贯穿整个解读）：**
- 解读之前，先站在用户角度想：「做这个梦的人，当时心里在经历什么？」
- 用「你可能最近...」「这种感觉是不是...」「你的内心其实在说...」等共情句式
- 不要只分析梦，要让用户感觉「你懂我」——像一个老朋友在聊天，而不是教授在上课
- 如果梦里有情绪（恐惧、悲伤、迷茫），先承认这个情绪的真实性，再进入分析
- 示例：「追逐的梦往往在你压力最大的时候出现——你最近是不是有什么事情一直悬着没解决？」

**心理学解读要求（必须深入，结合用户具体描述）：**
- 点名用户梦里的具体元素，逐一对应心理学理论
- 说明这个梦可能反映了用户近期的什么情绪状态/生活压力/内心渴望
- 引用荣格原型、弗洛伊德愿望理论、威胁模拟理论等，但要用人话解释
- 至少4-5句，有分析深度，让用户感觉「被看见了」
- **结尾一定要有一句直击内心的话**，像朋友说的那种：「你比你自己想象的要坚强」「你的潜意识比你更了解你自己」

**凶兆处理规则（吉凶不可改，但语气要有温度）：**
- 先完整、诚实地描述凶兆的含义（不缩水、不回避）
- 然后**必须**进行具体鼓励：说明这个信号的积极意义、用户可以怎么做
- 鼓励要具体，不能只说「加油」——要说「这说明你其实很在意X，这是好事」
- 结尾给出1条可操作的建议

**⚠️ 模板铁律：每次解梦必须严格按照以下固定结构输出，一个板块都不能省略、不能合并、不能调换顺序。所有板块对所有吉凶等级都必须出现，只有内容因吉凶而异。**

**输出模板（固定，每次必须完整输出所有板块）：**

```
🌙 梦境解读
━━━━━━━━━━━━━━━━
🔮 吉凶判定：[大吉✨ / 小吉🌟 / 平⚖️ / 小凶⚠️ / 大凶🔴]
━━━━━━━━━━━━━━━━

📖 周公解梦
[周公解梦典故/民间说法，3-4句，有来历有故事感，引用原典意象]

🧠 心理学视角
[逐一分析用户梦中具体元素，结合荣格/弗洛伊德等理论，4-5句]
[说明可能反映的情绪状态或生活处境，结尾一句直击内心]

💡 潜意识在说
[一句话点睛，有洞察力，像老朋友说的那种话]

💪 内心信号
[大吉/小吉：说明这个好兆头的深层含义，给出鼓励]
[平：轻松幽默，稳中有进]
[小凶/大凶：诚实说明凶兆信号意义，立刻转为具体鼓励，2-3句，结尾正向]
[大凶必须加：「记住，梦是心理信号，不是命运判决。」]

✨ 领域提示
[财运💰 / 感情💕 / 事业🚀 / 健康💪 选最相关1-2个，各1-2句]

🗓️ 今日建议
[1-2条轻松实用的具体建议，可操作]

━━━━━━━━━━━━━━━━
[🎙️ 听语音播报]　[🎨 生成梦境图]
[🔮 抽梦境签]　　[🌅 今日运势]
```

**🚨 按钮发送铁律（违反即视为执行失败）：**

> ❌ **绝对禁止**用普通对话文字回复解梦报告——即使只是一条短消息也不允许
> ❌ **绝对禁止**先发文字消息、再单独补发按钮——这是两次调用，不符合要求
> ✅ 解梦报告**必须**通过 `message` 工具发送
> ✅ `buttons` 参数**必须**与报告正文在**同一次** `message` 工具调用中一起发出
> ✅ 每一次解梦、每一次抽签、每一次运势，无论内容长短，**都必须带按钮**

**强制执行步骤（每次解梦必须严格执行）：**
1. 将完整报告文字放入 `message` 参数
2. 同时在 `buttons` 参数中附上四个按钮（两行排列）
3. 用 `message` 工具**一次性**发出，不得分两步
4. 检查：发出前确认 `buttons` 字段非空，否则重新调用

```json
{
  "action": "send",
  "message": "[完整解梦报告]",
  "buttons": [
    [{"text": "🎙️ 听语音播报", "callback_data": "dream_tts"}, {"text": "🎨 生成梦境图", "callback_data": "dream_image"}],
    [{"text": "🔮 抽梦境签", "callback_data": "dream_sign"}, {"text": "🌅 今日运势", "callback_data": "dream_fortune"}]
  ]
}
```

大凶解读务必加：「记住，梦是心理信号，不是命运判决。」

**⚠️ 计算过程静默规则（必须遵守）：**
- 天干地支、农历、日柱、五行的计算过程**全部在内部完成**，绝对不输出给用户
- 用户只看到最终运势报告，不看到任何「距基准天数」「干支序号」「python计算」等过程
- 报告中直接写结果，如「日柱：癸未｜五行：水」，不解释怎么算出来的
- 整个解读流程：收到梦境描述 → 内部计算 → 直接输出完整报告，中间不发任何过渡消息

### Step 5.6：今日运势（callback_data: dream_fortune）

当用户点击「🌅 今日运势」按钮或说「今日运势」「今天运势」时触发。

结合当日梦境的吉凶判定 + 当日干支五行，生成今日运势报告：

**计算逻辑（内部静默执行，不输出过程）：**
- 获取当日日柱（天干地支）和五行
- 获取本次梦境的吉凶判定和核心意象
- 分析梦境五行与日柱五行的相生相克关系

**五行相生相克：**
- 相生：木生火、火生土、土生金、金生水、水生木
- 相克：木克土、土克水、水克火、火克金、金克木

**输出模板：**

```
🌅 今日运势
━━━━━━━━━━━━━━━━
📅 [公历日期]　农历[农历日期]
🏮 [年柱]年　日柱：[日柱] | 五行：[五行]

昨夜梦境五行：[梦境主五行]　与今日[相生/相克/平和]
[一句话点评相生相克含义]

━━━━━━━━━━━━━━━━
总体运势：[大吉✨ / 小吉🌟 / 平⚖️ / 小凶⚠️ / 大凶🔴]

💰 财运：[1-2句]
💕 感情：[1-2句]
🚀 事业：[1-2句]
💪 健康：[1句]

🎯 今日宜：[2-3项]
⛔ 今日忌：[1-2项]

✨ [一句有温度的总结]
━━━━━━━━━━━━━━━━
```

### Step 5：语音播报

当用户回复「播报」「语音」「读给我听」或点击「🎙️ 听语音播报」按钮时：
- 调用 tts 工具朗读报告正文（去掉 emoji 和分隔线）

> ⚠️ **安装提醒（TTS 配置说明）**
> 
> 语音播报功能需要在 OpenClaw 中配置 TTS 服务，否则会报错。推荐以下几家：
> 
> **推荐配置（任选其一）：**
> 1. **阿里云 / 通义（Qwen TTS）** — 中文效果最佳，有免费额度，适合中文解梦场景
>    - 申请地址：https://dashscope.aliyun.com
>    - 配置 key：`DASHSCOPE_API_KEY`
> 2. **OpenAI TTS** — 效果稳定，支持多语言
>    - 申请地址：https://platform.openai.com
>    - 配置 key：`OPENAI_API_KEY`
> 3. **ElevenLabs** — 音色最丰富，支持情绪化语音
>    - 申请地址：https://elevenlabs.io
>    - 配置 key：`ELEVENLABS_API_KEY`
> 4. **Microsoft Edge TTS** — 免费，无需 API key，但稳定性一般
> 
> 未配置 TTS 时，「🎙️ 听语音播报」按钮仍会显示，但点击后会提示用户去配置。
- 朗读完毕后回复 NO_REPLY

### Step 5.5：梦境幻象图生成

**⚠️ 重要：收到 `dream_image` callback 时，禁止直接生成图片。必须先发送风格选择按钮，等用户选择风格后再生成。**

触发时机：
- 用户点击「🎨 生成梦境图」按钮（callback_data: dream_image）
- 用户说「梦境图」「生成图片」「画出我的梦」「看看我的梦长什么样」

**第一步：发送风格选择**

用 `message` 工具发送以下内容（带按钮）：

```
🎨 要把这个梦画出来吗？选一个你喜欢的风格：

🏙️ 现代都市 — 普通人置身超现实梦境，最有代入感
🏛️ 神话史诗 — 现代人×古典神话场景，琥珀金光
🎋 古风仙境 — 传统古风意境，仙气飘飘
🌊 水墨禅意 — 纯东方水墨，留白意境，黑白淡青
🌌 赛博仙境 — 霓虹街头，科幻超现实，紫蓝发光
🌸 梦幻唯美 — 樱花雨，柔光粉紫，治愈系
```

buttons:
- `🏙️ 现代都市` → callback_data: `dream_img_modern`
- `🏛️ 神话史诗` → callback_data: `dream_img_epic`
- `🎋 古风仙境` → callback_data: `dream_img_ancient`
- `🌊 水墨禅意` → callback_data: `dream_img_ink`
- `🌌 赛博仙境` → callback_data: `dream_img_cyber`
- `🌸 梦幻唯美` → callback_data: `dream_img_floral`
- `跳过` → callback_data: `dream_img_skip`

**第二步：根据选择构造 Prompt**

将梦境核心意象（3-5个英文关键词）+ 风格模板组合：

**🏙️ 现代都市：**
```
A young Asian person in everyday modern clothes (casual t-shirt, jeans or simple outfit), [意象关键词融入周围环境],
surrounded by surreal dream elements emerging from ordinary city streets,
realistic human figure in dreamlike scenario, soft cinematic lighting,
contemporary photography meets surrealism, natural skin tones with ethereal glow,
highly detailed, relatable and immersive, perfect for social media
```

**🏛️ 神话史诗：**
```
A young Asian male figure in modern casual clothes (t-shirt or shirt), [意象关键词融入场景与光效],
soft divine light emanating from within, ancient stone columns fading into mist,
contemporary person in mythic dreamscape, pearl white amber and soft violet palette,
cinematic composition, ultra-detailed, serene transcendent atmosphere,
beautiful and elegant, perfect for social media
```

**🎋 古风仙境：**
```
Traditional Chinese fantasy scene, figure in elegant ancient Chinese hanfu robes, [意象关键词],
misty mountain peaks, floating pavilions, cranes soaring, peach blossom petals drifting,
soft jade green and celestial blue palette, ethereal immortal atmosphere,
painterly illustration style, serene and majestic, classical Chinese art aesthetic
```

**🌊 水墨禅意：**
```
Traditional Chinese ink wash painting, [意象关键词], lone figure in flowing robes,
minimalist brushwork, vast negative space, misty mountains, ink bleeding on rice paper texture,
soft grey-blue and black tones, meditative and serene, master-level calligraphy aesthetic
```

**🌌 赛博仙境：**
```
Cyberpunk dreamscape, [意象关键词], young Asian figure in modern streetwear with glowing neon accents,
circuit patterns floating around them, holographic artifacts in the air,
neon purple and electric blue against dark background, ultra-detailed, cinematic,
futuristic surreal aesthetic
```

**🌸 梦幻唯美：**
```
Dreamy ethereal scene, [意象关键词], soft watercolor style, figure surrounded by cherry blossoms
and floating petals, pastel pink lavender and cream tones, gentle glowing light,
romantic and healing atmosphere, illustration style, delicate and beautiful
```

**意象→英文关键词映射：**
- 水/海/河 → `flowing water, misty river`
- 蛇 → `luminous serpent emerging from within the sleeve, serpent merged with body`
- 龙 → `celestial dragon soaring`
- 飞翔 → `figure soaring through clouds, weightless`
- 追逐 → `fleeing through endless corridor`
- 坠落 → `falling through swirling void`
- 火 → `flames and ember sparks`
- 考试 → `ancient scroll, ink brush`
- 家人/人物 → `ethereal silhouetted figures`
- 动物 → `[animal] spirit form`

**第三步：生成图片**

```bash
uv run /tmp/dream_gen.py --prompt "[构造的prompt]" \
  --filename "/Users/openclaw/.openclaw/workspace/dream-[YYYY-MM-DD]-[意象词].png" \
  --resolution 2K \
  --api-key AIzaSyAsht5bO-nUQUuXeH1NT26e3C9QEJNyQVg
```

**代理注意：** google-genai SDK 不读系统代理，必须用 `/tmp/dream_gen.py`（含 httpx monkey-patch）。
若脚本不存在，从以下内容重建：
```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai>=1.0.0","pillow>=10.0.0","httpx>=0.27.0"]
# ///
import os,sys,argparse
from pathlib import Path
PROXY="http://127.0.0.1:7897"
import httpx
_o=httpx.Client.__init__
def _p(self,*a,**k):
    if 'proxies' not in k and 'proxy' not in k: k['proxy']=PROXY
    _o(self,*a,**k)
httpx.Client.__init__=_p
_oa=httpx.AsyncClient.__init__
def _pa(self,*a,**k):
    if 'proxies' not in k and 'proxy' not in k: k['proxy']=PROXY
    _oa(self,*a,**k)
httpx.AsyncClient.__init__=_pa
parser=argparse.ArgumentParser()
parser.add_argument('--prompt',required=True)
parser.add_argument('--filename',required=True)
parser.add_argument('--resolution',default='1K',choices=['1K','2K','4K'])
parser.add_argument('--api-key')
args=parser.parse_args()
api_key=args.api_key or os.environ.get('GEMINI_API_KEY')
from google import genai
from google.genai import types
from PIL import Image as PILImage
from io import BytesIO
client=genai.Client(api_key=api_key)
response=client.models.generate_images(model='imagen-4.0-generate-001',prompt=args.prompt,config=types.GenerateImagesConfig(number_of_images=1,aspect_ratio='1:1'))
img_data=response.generated_images[0].image.image_bytes
image=PILImage.open(BytesIO(img_data))
out=Path(args.filename)
out.parent.mkdir(parents=True,exist_ok=True)
image.convert('RGB').save(str(out),'PNG')
print(f'Image saved: {out.resolve()}')
```

**第四步：发送图片**

用 `message` 工具发送，caption：
`🎨 梦境幻象图 · [今日日期]\n[风格名] 风格 · 可保存转发`

若用户选择「跳过」或生成失败，静默跳过，不影响主流程。

### Step 6：记录梦境到 dreams.json

```python
import json, time, os
from datetime import datetime

path = os.path.expanduser('~/.openclaw/workspace/memory/dreams/dreams.json')
os.makedirs(os.path.dirname(path), exist_ok=True)

try:
    with open(path) as f:
        data = json.load(f)
except:
    data = {'records': []}

now = datetime.now()
record = {
    'id': f'dream_{now.strftime("%Y%m%d")}_{str(len(data["records"])+1).zfill(3)}',
    'date': now.strftime('%Y-%m-%d'),
    'timestamp': int(time.time()),
    'raw': '<用户原始描述>',
    'elements': ['<提取的元素>'],
    'emotion': '<主要情绪>',
    'verdict': '<吉凶判定>',
    'domains': ['<涉及领域>'],
    'summary': '<一句话总结>'
}

data['records'].append(record)
with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('saved')
```

### Step 7：梦境规律分析（≥3条记录时追加）

```
📊 你的梦境规律
最近 [N] 天共记录 [X] 个梦
频繁出现：[高频元素]
情绪基调：正面[X]% / 负面[X]%
[一句个性化洞察]
```

## 查询功能

### 梦境历史
当用户说「查我的梦境记录」「最近的梦」时：
- 读取 dreams.json
- 展示最近5条摘要（日期 + 吉凶 + 一句话总结）
- 统计高频元素和情绪分布

### 梦境日历
当用户说「梦境日历」「看看我的梦境日历」时：
- 读取 dreams.json，按日期分组
- 用文字日历格式输出当月，有梦境记录的日期标注吉凶符号
- 示例：
```
📅 2026年3月 梦境日历
一  二  三  四  五  六  日
                          1
 2   3✨  4   5⚠️  6   7   8
 9  10   11  12  13🌟 14  15
...
```

### 月度梦境报告
当用户说「梦境报告」「上个月梦境总结」「生成月报」时：
- 统计该月梦境总数
- 吉凶分布（饼图用文字表示）
- 高频出现元素 TOP5
- 情绪趋势
- 最值得关注的一个梦（凶/反复出现的）
- 一句总结性洞察

示例输出：
```
📋 2026年3月 梦境月报

共记录梦境：12个
吉凶分布：大吉2 小吉4 平3 小凶2 大凶1
频繁出现：水(5次) 追逐(3次) 家人(3次)
情绪基调：正面58% / 负面42%

⚠️ 本月最值得关注：
3月5日「被追逐逃不掉」已出现3次，
暗示你有某个现实压力尚未面对。

💡 本月洞察：
水元素频繁出现，你的情感世界比你意识到的更丰富。
```

## 连续梦追踪

每次记录梦境后，检查 dreams.json 中过去14天内是否存在**元素重合度 ≥ 2 个**的梦境记录。

若发现反复梦，在解读报告末尾追加：

```
🔁 连续梦警报
你已连续 [X] 次梦见「[重复元素]」
最近一次：[日期]

这不是巧合。反复出现的梦境是潜意识在敲门——
[具体分析：这个元素反复出现通常意味着什么未解决的现实问题]

💬 问自己：最近有什么事你一直在回避？
```

判断重复逻辑（用 python3 exec 执行）：
- 取当前梦的 elements 列表
- 遍历过去14天记录，计算 elements 交集
- 交集 ≥ 2 个且出现次数 ≥ 2 次 → 触发连续梦警报
- 记录该元素的出现次数和日期列表

## 今日运势预告

当用户说「今日运势」「今天运势」「根据梦境看今天」时，或在每次解梦后主动附上：

### 日期信息生成规则（必须计算后填入，不得省略）

**公历日期：** 调用 `date` 命令获取当前日期（年月日 + 星期）

**农历转换规则（内置算法，无需外部 API）：**
- 使用以下天干地支序列推算：
  - 天干（10）：甲乙丙丁戊己庚辛壬癸
  - 地支（12）：子丑寅卯辰巳午未申酉戌亥
  - 生肖对应地支：子鼠、丑牛、寅虎、卯兔、辰龙、巳蛇、午马、未羊、申猴、酉鸡、戌狗、亥猪
- **年干支计算：** (公历年 - 4) % 60，天干 = 结果 % 10，地支 = 结果 % 12
  - 示例：2026年 → (2026-4)%60 = 22，天干=22%10=2→丙，地支=22%12=10→戌，即丙戌年（狗年）
- **日干支：** 以 2000年1月1日为庚辰日(基准第36天)，计算距今天数 % 60 推算
- **农历月日：** 直接用口诀近似：春节前后1个月内用「正月」，按节气分月，日期估算即可（标注「约」）
- **节气提示：** 若当日接近节气（±3天），标注节气名

**日五行：**
- 天干五行：甲乙→木，丙丁→火，戊己→土，庚辛→金，壬癸→水
- 地支五行：寅卯→木，巳午→火，辰戌丑未→土，申酉→金，亥子→水
- 日柱天干五行即为当日主五行

**梦境与五行关联：**
- 水/海/雨 → 水；火/太阳/光 → 火；树木/草地 → 木；金属/刀/镜 → 金；土地/山/房屋 → 土
- 梦境五行与日五行**相生**（木生火、火生土、土生金、金生水、水生木）→ 运势加成
- 梦境五行与日五行**相克**（木克土、土克水、水克火、火克金、金克木）→ 需注意
- 相同五行 → 平稳

**生成逻辑：**
- 大吉梦 → 今天整体运势强，适合主动出击
- 小吉梦 → 小有收获，适合稳扎稳打
- 平 → 普通日，随缘即可
- 小凶梦 → 今天决策保守，避免冲动
- 大凶梦 → 今天以守为主，不宜大动作

**输出模板：**

```
☀️ 今日梦境运势
━━━━━━━━━━━━━━━━
📅 [公历日期，如：2026年3月28日 周六]
🌙 农历 [X月X日]（约）· [天干地支年]年 [生肖]年
🗓️ 日柱：[日天干地支]  五行：[日主五行]
⭐ 梦境五行：[梦境主五行] · 与日柱[相生✨/相克⚠️/同气🔄]
━━━━━━━━━━━━━━━━

综合指数：[★★★★☆ 4/5]

💼 事业：[今天适合/不适合做什么，1句]
💰 财运：[今天财运提示，1句]
💕 感情：[今天感情运，1句]
⚡ 今日宜：[2-3件具体的事]
🚫 今日忌：[1-2件要避免的事]

✨ 一句话运势：[有力量感的总结句]
```

宜/忌示例：
- 大吉梦宜：谈合作、表白、做决定、见重要的人
- 大凶梦忌：签合同、借钱、做重大决策、吵架
- 财运梦宜：投资小额、买彩票（玩玩）、谈薪资

## 梦境签

当用户说「抽签」「梦境签」「给我一签」时：

**生成逻辑（AI 动态生成，非固定模板）：**
- 读取最近3天的梦境记录（若无则用当前梦）
- 综合吉凶判定生成签级
- **根据梦境核心意象，动态生成四句押韵签文**，要求：
  - 每句7字，四句整体押韵（同一韵脚）
  - 意象必须来源于梦境描述（水/火/蛇/飞翔/追逐等）
  - 语言风格：古典、有意境，类唐诗/宋词气质
  - 含义：前两句描述当前处境，后两句指向转机/结局
  - 吉签：气势磅礴，充满希望；凶签：警示但不绝望，附励志解读
  - 禁止使用现代词汇（手机、电脑、AI等）
  - 示例意象映射：
    - 水/海 → 「潮」「浪」「波」「渡」
    - 蛇 → 「蜕」「龙」「腾」「盘」
    - 飞翔 → 「翱」「云」「天」「翼」
    - 追逐 → 「逐」「风」「尘」「路」
    - 坠落 → 「沉」「渊」「归」「定」
    - 火 → 「炬」「焰」「燃」「灰尽」
    - 考试 → 「笔」「墨」「砚」「金榜」

**签级对应：**
- 大吉 → 上上签
- 小吉 → 上签
- 平 → 中签
- 小凶 → 下签
- 大凶 → 下下签（但附励志解签）

**输出模板：**

```
🎋 梦境签
━━━━━━━━━━━━━━━━
第 [随机三位数] 签   [上上签 / 上签 / 中签 / 下签 / 下下签]

【签语】
[四字签文，押韵]
[四字签文，押韵]
[四字签文，押韵]
[四字签文，押韵]

━━━━━━━━━━━━━━━━
【解签】
[2-3句解读，结合梦境意象，有文学感]

[事业] [一句]
[感情] [一句]
[财运] [一句]

此签有效期：今日
━━━━━━━━━━━━━━━━
```

签语示例（大吉/蛇/飞翔）：
```
第 078 签   上上签

【签语】
蛇化游龙腾九天
积财化运自绵绵
逆风起势终有时
云开日出见青天

【解签】
此签主大吉。梦中蛇而飞腾，乃蜕变升华之象。
你正处于蜕变的关键节点，眼前的压力是脱皮前的阵痛。

事业：旧事将去，新机将至，可大胆谋划
感情：有惊无险，缘分自来
财运：近期有一笔意外之财，留意机会
```

## 触发词更新（在文件顶部触发条件中补充）

新增触发词：
- 「今日运势」「今天运势」「根据梦境看今天」
- 「抽签」「梦境签」「给我一签」「抽个签」
- 「梦境图」「生成图片」「画出我的梦」「看看我的梦长什么样」

## 语气要求

### ⛔ 吉凶判定铁律（绝对不可违反）

- **吉凶结果必须忠实于解读，不得为了让用户「感觉好」而篡改**
- 解读是小凶就写小凶，解读是大凶就写大凶，绝对禁止把凶改成吉
- 用户对结果有异议时，**不得修改已出的吉凶判定**，只能解释依据
- 吉凶依据：周公解梦传统意象 + 荣格/弗洛伊德心理学分析，二者综合判断
- 风格可以调整（语气轻松、加鼓励），但**吉凶事实本身不能动**
- 示例：用户说「我觉得应该是小吉」→ 回应「这个梦的核心意象在周公解梦里确实偏凶，我理解你可能感觉不那么负面，但解读结果要尊重事实」

---

- **共鸣第一**：每一条解读都要让用户感觉「这说的就是我」，不是在背书，是在聊天
- **先共情，再分析**：遇到情绪性梦境（恐惧/悲伤/迷茫），先说「这种感觉很真实」，再进入解读
- **用「你」不用「人们」**：「你最近可能在担心...」比「这类梦通常代表...」更有温度
- **有趣但不迷信**：用「民间认为」「传统说法」而非「一定会」
- **科学但不冷漠**：心理学分析要有共鸣感，像朋友分析，不像教授授课
- **吉凶要有力度**：大吉就说大吉，不要模棱两可
- **加一点神秘感**：用「你的潜意识在悄悄告诉你...」
- 涉及健康类梦境，心理学视角优先，不渲染恐惧
- 不做算命，不说「你将会...」，用「可能」「往往意味着」
- 签语要有文学感，押韵，不要太现代
- 运势提示轻松有趣，不要严肃

### 吉凶语气分级规则（必须遵守）

**大吉 / 小吉：**
- 尽情夸！热情洋溢，让人看了心情大好
- 用「哇」「太好了」「老天爷在偏心你」「运气要来了」等词
- 给出具体鼓励，说明哪里好、好在哪
- 示例：「这梦简直是天降好运的预告片！潜意识在给你加油呢 🌟」

**平：**
- 轻松平和，像朋友聊天
- 可以加点小幽默：「平平无奇但稳稳当当，低调的幸福也是幸福嘛」

**小凶 / 大凶：**
- 先陈述事实（简短，不渲染），然后**立刻转鼓励**
- 加俏皮感来缓解紧张，绝对不能让人看完感到压抑或害怕
- 鼓励要具体，不要空洞的「加油」
- 可以自嘲或幽默化处理：「梦里吓了一跳，现实里你可是那个最清醒的人」
- 结尾必须是正向的、有力量的
- 示例：「这梦有点刺激对吧 😅 不过别慌——你的潜意识只是在提醒你某件事需要注意，说明你的内心其实很敏锐。换个角度看，这是你在替自己操心，挺负责任的嘛！」
- **严禁**：给人压力、过分强调凶兆、说「要小心了」「不好的事要发生」等话

### 图片生成性别与风格规则

- 默认生成**男性**人物（可根据用户明确指定改为女性）
- 共6种风格，各有不同服装与场景规范：
  - **现代都市**：现代日常便装（T恤/牛仔裤），普通人置于超现实场景，最有代入感
  - **神话史诗**：现代便装人物置于古典神话场景，琥珀金光，希腊×东方混搭
  - **古风仙境**：汉服古装，传统仙侠意境，仙气飘飘——此风格允许古装
  - **水墨禅意**：水墨画风，传统东方意境，留白禅意
  - **赛博仙境**：现代街头服装+霓虹科幻元素，未来超现实
  - **梦幻唯美**：柔光水彩，樱花系，治愈系少女感
- **现代/赛博/神话史诗风格禁止古装汉服**，古风仙境风格专属古装
- 色调：各风格有专属色调，但**禁止暗红恐怖系**
- 人物要有**带入感**：略俯视角或平视角，让观者感觉「这就是我」
- 梦境元素从人物**体内向外生长**，而非外部攻击——表达内在力量
- 无论吉凶，图片必须**美丽、梦幻、适合社交媒体分享**
