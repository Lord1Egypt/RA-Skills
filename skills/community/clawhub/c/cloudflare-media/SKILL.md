---
name: cloudflare-media
version: 2.2.0
description: |
  使用 Cloudflare Workers AI 生成图片或语音。触发条件：
  - 文生图："生成图片"、"文生图"、"text-to-image"、"AI 作图"、"帮我画"
  - TTS："文字转语音"、"TTS"、"读出来"、"语音合成"、"text-to-speech"
allowed-tools:
  - Read
  - Write
  - Edit
  - Exec
  - Image
  - Message
---

# Cloudflare Workers AI — 图片 & 语音生成

## 凭证配置

优先从 `skills/cloudflare-media/config.json` 或 MEMORY.md 读取 Account ID 和 API Token，缺失则询问用户。

---

# 第一部分：文生图（Text-to-Image）

## 可选模型一览（共10个）

| # | 模型 | 模型 ID | 简介 | 价格 | 传输方式 |
|---|------|---------|------|------|---------|
| 1 | FLUX.2 klein 4B | `@cf/black-forest-labs/flux-2-klein-4b` | 高速蒸馏版，4B参数，实时预览 | $0.000059/tile | multipart |
| 2 | FLUX.2 klein 9B | `@cf/black-forest-labs/flux-2-klein-9b` | 增强质量版，9B参数 | $0.015/first MP | multipart |
| 3 | FLUX.2 dev | `@cf/black-forest-labs/flux-2-dev` | 最高质量，开放权重 | $0.00021/tile/step | multipart |
| 4 | FLUX.1 schnell | `@cf/black-forest-labs/flux-1-schnell` | 12B参数，最快4步生成，适合批量 | $0.000053/tile | JSON body |
| 5 | SDXL-Lightning | `@cf/bytedance/stable-diffusion-xl-lightning` | 极快文生图，几步完成，Beta | $0.00/step | JSON body |
| 6 | DreamShaper 8 LCM | `@cf/lykon/dreamshaper-8-lcm` | 强逼真写实风格，不牺牲创意范围 | 免费 | JSON body |
| 7 | Leonardo Lucid Origin | `@cf/leonardo/lucid-origin` | 强提示跟随，支持文字渲染 | $0.007/tile | JSON body |
| 8 | Leonardo Phoenix 1.0 | `@cf/leonardo/phoenix-1.0` | 最佳文字生成，提示 adherence 最强 | $0.0058/tile | JSON body |

---

### 1. FLUX.2 klein 4B / 9B / dev（Black Forest Labs）

**特点：** 高速/高质量/最高质量三档，multipart/form-data 传输

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| prompt | ✅ | — | 图片描述文本 |
| width | ❌ | 1024 | 宽度 256~1024（64倍数）|
| height | ❌ | 1024 | 高度 256~1024（64倍数）|
| steps | ❌ | — | 步数（参考值25）|

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/@cf/black-forest-labs/flux-2-klein-4b" \
  -H "Authorization: Bearer {TOKEN}" \
  -F "prompt=a sunset over the ocean" \
  -F "width=1024" -F "height=1024"
```

**返回：** `{"result":{"image":"base64..."}}` → 保存为 `.png`

---

### 2. FLUX.1 schnell（Black Forest Labs）

**特点：** 12B 参数，极快（默认4步），适合批量生成，JSON body

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| prompt | ✅ | — | 图片描述（最长2048字符）|
| steps | ❌ | 4 | 步数（1~8，越高越慢）|

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/@cf/black-forest-labs/flux-1-schnell" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"a cyberpunk cat","steps":4}'
```

**返回：** `{"image":"base64..."}` → 保存为 `.jpg`

---

### 3. SDXL-Lightning（ByteDance）Beta

**特点：** 极快几步生成，支持 img2img，输出为原始 JPEG 二进制流

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| prompt | ✅ | — | 图片描述 |
| negative_prompt | ❌ | — | 反向提示词 |
| width | ❌ | 1024 | 宽度 256~2048 |
| height | ❌ | 1024 | 高度 256~2048 |
| num_steps | ❌ | 20 | 步数（1~20）|
| guidance | ❌ | 7.5 | 提示跟随度 |
| strength | ❌ | 1 | img2img 强度（0~1）|
| seed | ❌ | — | 随机种子 |
| image / image_b64 | ❌ | — | img2img 输入图（数组或base64）|
| mask / mask_b64 | ❌ | — | inpainting mask |

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/@cf/bytedance/stable-diffusion-xl-lightning" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"a cyberpunk cat","num_steps":10}'
```

**返回：** 原始 JPEG 二进制流 → 保存为 `.jpg`

---

### 4. DreamShaper 8 LCM（lykon）

**特点：** 强逼真写实风格，LCM 加速，支持 img2img + inpainting，参数同 SDXL-Lightning

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| prompt | ✅ | — | 图片描述 |
| negative_prompt | ❌ | — | 反向提示词 |
| width | ❌ | 1024 | 宽度 256~2048 |
| height | ❌ | 1024 | 高度 256~2048 |
| num_steps | ❌ | 20 | 步数（1~20）|
| guidance | ❌ | 7.5 | 提示跟随度 |
| strength | ❌ | 1 | img2img 强度（0~1）|
| seed | ❌ | — | 随机种子 |
| image / image_b64 | ❌ | — | img2img 输入图 |
| mask / mask_b64 | ❌ | — | inpainting mask |

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/@cf/lykon/dreamshaper-8-lcm" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"a realistic photo of a cat","num_steps":8}'
```

**返回：** 原始 JPEG 二进制流 → 保存为 `.jpg`

---

### 5. Leonardo Lucid Origin

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| prompt | ✅ | — | 图片描述 |
| width | ❌ | 1120 | 宽度 0~2500 |
| height | ❌ | 1120 | 高度 0~2500 |
| guidance | ❌ | 4.5 | 提示跟随度（0~10）|
| num_steps | ❌ | — | 步数（1~40）|
| seed | ❌ | — | 随机种子 |

**返回：** `{"result":{"image":"base64..."}}` → 保存为 `.png`

---

### 6. Leonardo Phoenix 1.0

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| prompt | ✅ | — | 图片描述 |
| width | ❌ | 1024 | 宽度 0~2048 |
| height | ❌ | 1024 | 高度 0~2048 |
| guidance | ❌ | 2 | 提示跟随度（2~10）|
| num_steps | ❌ | 25 | 步数（1~50）|
| negative_prompt | ❌ | — | 反向提示词 |
| seed | ❌ | — | 随机种子 |

**返回：** 原始 JPEG 二进制流 → 保存为 `.jpg`

---

# 第二部分：TTS（Text-to-Speech）

## 可选模型一览（共4个）

| # | 模型 | 模型 ID | 简介 | 价格 |
|---|------|---------|------|------|
| 1 | Deepgram Aura-2 英语 | `@cf/deepgram/aura-2-en` | 40个声音，上下文感知，自然停顿表达 | $0.03/1k字符 |
| 2 | Deepgram Aura-2 西班牙语 | `@cf/deepgram/aura-2-es` | 同上，专为西班牙语优化 | $0.03/1k字符 |
| 3 | Deepgram Aura-1 | `@cf/deepgram/aura-1` | 12个声音，Aura-2 低配版，半价 | $0.015/1k字符 |
| 4 | MyShell MeloTTS | `@cf/myshell-ai/melotts` | 多语言（en/es/fr/zh/ja/ko），费用最低 | $0.0002/分钟 |

### Deepgram Aura 声音列表

**Aura-2（40个）：**
amalthea, andromeda, apollo, arcas, aries, asteria, athena, atlas, aurora, callista, cora, cordelia, delia, draco, electra, harmonia, helena, hera, hermes, hyperion, iris, janus, juno, jupiter, luna, mars, minerva, neptune, odysseus, ophelia, orion, orpheus, pandora, phoebe, pluto, saturn, thalia, theia, vesta, zeus

> 默认声音：`luna`（女声，温暖）

**Aura-1（12个）：**
angus, asteria, arcas, orion, orpheus, athena, luna, zeus, perseus, helios, hera, stella

> 默认声音：`angus`（男声）

### Deepgram Aura 参数

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| text | ✅ | — | 要转语音的文本 |
| speaker | ❌ | luna/angus | 声音名称 |
| encoding | ❌ | mp3 | 编码：linear16/flac/mulaw/alaw/mp3/opus/aac |
| sample_rate | ❌ | — | 采样率（Hz）|
| bit_rate | ❌ | — | 比特率（bps）|

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/@cf/deepgram/aura-2-en" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","speaker":"luna"}'
```

**返回：** 原始 MP3 二进制流 → 保存为 `.mp3`

### MyShell MeloTTS 参数

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| prompt | ✅ | — | 要转语音的文本 |
| lang | ❌ | en | 语言：en/es/fr/zh/ja/ko |

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/@cf/myshell-ai/melotts" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello world","lang":"en"}'
```

**返回：** `{"result":{"audio":"base64..."}}`（实测为 WAV 16bit 44100Hz PCM）→ 保存为 `.wav`

---

# 第三部分：交互流程

## 步骤一：检查凭证

读取 `skills/cloudflare-media/config.json` 或 MEMORY.md，缺失则询问用户。

## 步骤二：展示模型选项

用户提出请求后立即展示所有可选模型：

**文生图（8个模型）：**
```
🎨 文生图 — 可选模型（共8个）

1️⃣ FLUX.2 klein 4B（推荐快速预览）
   高速蒸馏版，4B参数，实时交互

2️⃣ FLUX.2 klein 9B
   增强质量版，9B参数，更细腻

3️⃣ FLUX.2 dev
   最高输出质量，开放权重

4️⃣ FLUX.1 schnell
   12B参数，极快（4步），适合批量

5️⃣ SDXL-Lightning（Beta）
   极快几步生成，ByteDance出品

6️⃣ DreamShaper 8 LCM
   强逼真写实风格

7️⃣ Leonardo Lucid Origin
   强提示跟随，支持文字渲染

8️⃣ Leonardo Phoenix 1.0
   最佳文字生成

请提供：模型编号（默认1）+ 图片描述 + 尺寸（可选）
```

**TTS（4个模型）：**
```
🔊 TTS — 可选模型（共4个）

1️⃣ Deepgram Aura-2 英语（推荐）
   40个声音，上下文感知，自然表达
   默认声音：luna

2️⃣ Deepgram Aura-2 西班牙语
   同上，专为西班牙语优化

3️⃣ Deepgram Aura-1
   12个声音，半价

4️⃣ MyShell MeloTTS
   多语言（en/es/fr/zh/ja/ko），最便宜

请提供：模型编号（默认1）+ 要朗读的文本 + 声音（可选）
```

## 步骤三：生成并发送

- **webchat**：图片用 `image` 展示，音频用 `tts` 工具发送
- **其他 channel**：走对应平台接口

---

# 第四部分：注意事项

1. **免费额度**：SDXL-Lightning / DreamShaper 均为 $0.00（免费），FLUX/Leonardo 按 tile 计费
2. **输出格式实测**：
   - Deepgram Aura → 原始 MP3 二进制
   - MeloTTS → base64 WAV（不是 MP3！）
   - Phoenix 1.0 / SDXL-Lightning / DreamShaper → 原始 JPEG 二进制流
3. **img2img/inpainting**：SDXL-Lightning 和 DreamShaper 支持图生图，需要额外提供 image/mask 数据，skill 当前版本暂不支持图片输入作为参数传递
