# 歌词与风格 · `lyrics` / `style` / `mashup_lyrics` / `timing`

四个**同步**接口，都是"给输入、直接拿结果"，不用轮询。

---

## `lyrics` · 生成歌词

```
POST https://api.a7w.cn/api/v1/apps/music_generation/lyrics
模式：同步    计费：12 点（0.12 元）
```

根据主题或风格描述生成**结构化歌词**。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `prompt` | string | **是** | 歌词生成提示词，用于描述歌词的**主题、情绪或风格** |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/lyrics" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"写一首关于凌晨加班后骑车回家的城市民谣，主歌写疲惫，副歌写希望，两段主歌一段副歌"}'
```

### prompt 怎么写

**给结构，不要只给主题。**

| | 写法 | 结果 |
|---|---|---|
| ❌ | `写一首关于青春的歌` | 泛泛而谈，结构可能不完整 |
| ✅ | `写一首关于毕业那天最后一次走出校门的歌。主歌写具体场景（教室、操场、自行车棚），副歌要明亮有希望。两段主歌一段副歌，加一段桥段` | 结构完整，可直接进 `create` |

**好用的要素**：主题 + 情绪走向 + 结构要求 + 具体意象。

### ★ 一个重要发现：`lyrics` 顺带把 `style` 也给你了

**实测**：`lyrics` 的返回里，`data.tags` 直接是一段**专业英文编曲描述**——
配器、律动、混音质感、人声处理都写好了：

```json
{
  "title": "夜归单车",
  "text": "[Verse 1]\n楼下的风有点冷\n...",
  "tags": [
    "City folk with gentle fingerpicked acoustic guitar, brushed percussion,
     and a steady walking bass; verse feels weary and close-mic with sparse
     room tone, pre-chorus lifts on layered harmonies and rising strings,
     chorus opens warm and singable with gang-vocal echoes on the anchor
     phrase. Add a soft tape hiss, passing-bus ambience between lines..."
  ]
}
```

**这意味着：`lyrics` 一次调用（0.12 元）同时拿到了歌词和专业风格描述。**

- 走 `lyrics` → 歌词 + `tags` 直接当 `style` 用 → **省掉 `style` 那一趟 0.14 元**
- 只有当你想**单独精修风格**、或者自己已经写好词时才需要单独调 `style`

> 实测数据：输入 `写一首关于凌晨加班后骑车回家的城市民谣，主歌写疲惫，副歌写希望`，
> 8.5 秒返回，`title` = 「夜归单车」，歌词含 Verse 1 / Pre-Chorus / Chorus /
> Verse 2 / Bridge 完整结构。计费 `usage.points_cost = 12`，与价目表一致。

### 返回结构

```json
{
  "code": 1,                    // ⚠️ 1 = 成功（不是 0）
  "msg": "success",
  "data": {
    "result": {
      "task_id": "...",
      "title": "夜归单车",
      "data": { "status": "complete", "title": "...", "text": "...", "tags": ["..."] },
      "status": "completed",
      "elapsed": 8.518
    },
    "usage": { "points_cost": 12, "actual_points": 12 }
  }
}
```

- **`code: 1` 才是成功** —— 这个平台的成功码是 `1`，不是 `0`，别写错判断
- `data.usage.points_cost` / `actual_points` 是**本次真实扣费**，可以用来对账
- 歌词在 `data.result.data.text`，风格描述在 `data.result.data.tags[0]`

生成结果直接填进 `create` 的 `lyric` 字段（`custom: true`）。

---

## `style` · 优化音乐风格

```
POST https://api.a7w.cn/api/v1/apps/music_generation/style
模式：同步    计费：14 点（0.14 元）
```

根据提示词生成**更完整的音乐风格描述**。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `prompt` | string | **是** | 需要优化的风格提示词 |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/style" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"城市民谣，木吉他，温暖男声，慢速"}'
```

### 为什么这 0.14 元值得花

你写的是大白话（"城市民谣，木吉他"），它返回的是一段**专业编曲语言**
（配器、律动、混音质感、人声处理）。把这段填回 `create` 的 `style`，
出片质量通常明显好于自己写。

> **先看 `lyrics` 那一节。** 如果你本来就要用 AI 写词，`lyrics` 返回的 `tags`
> 里**已经带了一段专业风格描述**，可以直接当 `style` 用，省掉这 0.14 元。
> 单独调 `style` 的适用场景是：**词已自己写好**，或**想在已有风格上再精修一版**。

> 上限提醒：`style` 在**常规模型**下最多 200 字符、**高质量模型** 1000 字符。
> 优化后的描述可能变长（实测英文编曲描述常有 400+ 字符），超了要自己精简。

---

## `mashup_lyrics` · 歌词混合

```
POST https://api.a7w.cn/api/v1/apps/music_generation/mashup_lyrics
模式：同步    计费：12 点（0.12 元）
```

将**两段歌词融合**为新的混合版本。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `lyrics_a` | string | **是** | 第一段歌词 |
| `lyrics_b` | string | **是** | 第二段歌词 |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/mashup_lyrics" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"lyrics_a":"<歌词A>","lyrics_b":"<歌词B>"}'
```

**用处**：两版歌词各有所长时，让模型合成一版，比人肉拼凑自然。
产出的歌词同样可以喂给 `create`（配合 `type: "mashup"` 做真正的混音曲）。

---

## `timing` · 歌词时间轴

```
POST https://api.a7w.cn/api/v1/apps/music_generation/timing
模式：同步    计费：免费
```

基于音频 ID 获取**歌词与音频的时间轴信息**。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `audio_id` | string | **是** | 音频 ID，用于定位已生成或已上传的音频 |
| `callback_url` | string | 否 | 任务完成/失败时平台主动通知的 HTTPS 地址；同步接口可不传 |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/timing" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_id":"<audio_id>"}'
```

**免费**，是"歌词卡点字幕"和"逐句 MV 剪辑"的关键输入 ——
有了每句歌词的起止时间，就能自动生成 SRT 或做逐句转场。

---

## 四个接口怎么串起来

```
lyrics ──→ 歌词 ──┐
                  ├──→ create（type: generate, custom: true）
style  ──→ 风格 ──┘
                        │
                        ↓
                   生成结果 audio_id
                        │
              ┌─────────┴─────────┐
              ↓                   ↓
       timing（免费拿时间轴）   mashup_lyrics（想再合词时）
```
