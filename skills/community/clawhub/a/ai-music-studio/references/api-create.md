# `create` · 创建音乐任务

```
POST https://api.a7w.cn/api/v1/apps/music_generation/create
模式：异步（返回 task_id，用 query 查结果）
计费：65 点 / 次（租户实际结算价，1 元 = 100 点）
```

**这是整个插件的核心接口。** 17 种操作类型都走它，靠 `type` 区分。

> ⚠️ `create` 的 `required` 是**空的** —— 没有任何字段在所有情况下都必填。
> 必填什么**取决于你选的 `type`**。所以要按下面的表对号入座。

---

## 一、`type` 的 17 种取值

### 从零创作

| `type` | 做什么 | 关键参数 |
|---|---|---|
| `generate` | 根据提示词生成音乐（最常用） | `prompt` 或 `lyric`+`style` |
| `inspo` | 基于参考音频生成灵感作品 | `audio_urls`（**1~4 个**公网地址） |
| `cover` | 参考既有曲风重新演绎 | `audio_id` + `style` |
| `upload_cover` | 对你上传的音频做风格翻唱 | `audio_id` + `style` |
| `artist_consistency` | 按指定歌手风格生成 | `persona_id` |
| `artist_consistency_vox` | 人声模式 + 指定歌手风格生成 | `persona_id` + `vox_audio_id` |

### 续写与拼接

| `type` | 做什么 | 关键参数 |
|---|---|---|
| `extend` | 基于已有音频续写 | `audio_id` + `continue_at` |
| `upload_extend` | 续写你上传的音频 | `audio_id` + `continue_at` |
| `concat` | 拼接音频片段 | `audio_id` |

### 编辑与增强

| `type` | 做什么 | 关键参数 |
|---|---|---|
| `remaster` | 增强音质（母带重制） | `audio_id` |
| `mashup` | 混合多首歌曲 | `mashup_audio_ids` |
| `replace_section` | 替换指定时间段 | `replace_section_start` / `_end` |
| `underpainting` | 为**人声**添加伴奏 | `audio_id` + `underpainting_start` / `_end` |
| `overpainting` | 为**伴奏**添加人声 | `audio_id` + `overpainting_start` / `_end` |
| `samples` | 在指定时间段添加采样 | `samples_start` / `samples_end` |

### 分轨

| `type` | 做什么 | 关键参数 |
|---|---|---|
| `stems` | 分离**人声和伴奏**两轨 | `audio_id` |
| `all_stems` | 分离**人声、鼓、贝斯、其他乐器**四轨 | `audio_id` |

---

## 二、全部参数

### 决定"生成什么"

| 参数 | 类型 | 说明 |
|---|---|---|
| `type` | string | 操作类型，见上表。**17 选 1** |
| `custom` | boolean | `true` = 自定义模式（按 `lyric`+`style`）；`false` = 灵感模式（按 `prompt`）。**优先传 JSON boolean**，平台也兼容 `true/false`、`1/0`、`yes/no`、`on/off` 字符串 |
| `prompt` | string | 灵感模式的提示词，**≤500 字符**。自定义歌词模式请优先用 `lyric` + `style` |
| `lyric` | string | 自定义模式的歌词。常规模型 **≤3000**，高质量模型 **≤5000** 字符 |
| `lyric_prompt` | string | 自动写词的提示词。**仅在 `custom: true` 且 `lyric` 为空时生效** |
| `style` | string | 音乐风格描述。常规模型 **≤200**，高质量模型 **≤1000** 字符 |
| `style_negative` | string | **不想要**出现的风格描述（负面提示词） |
| `title` | string | 自定义模式的歌曲标题。常规模型 ≤80，高质量模型 ≤100 字符 |
| `instrumental` | boolean | **纯伴奏模式**，开启后**忽略歌词内容**。优先传 JSON boolean |

### 控制"像不像"

| 参数 | 类型 | 范围 / 取值 | 说明 |
|---|---|---|---|
| `weirdness` | number | `0` ~ `1` | 创意实验强度，越高结果越开放。**仅自定义模式生效** |
| `style_influence` | number | `0` ~ `1` | 风格影响强度，越高越贴近你填的风格。**仅自定义模式生效** |
| `audio_weight` | number | `0` ~ `1` | 参考音频权重，越高越依赖参考音频。**主要用于翻唱类操作** |
| `vocal_gender` | string | `m` / `f` | 人声性别偏好。**只提高概率，不保证严格符合** |
| `variation_category` | string | `high` / `normal` / `subtle` | 变化强度 |
| `persona_id` | string | — | 歌手或声音风格 ID（来自 `persona` 或 `voice_clone`） |
| `vox_audio_id` | string | — | 用于创建新歌手风格的人声参考音频 ID |

### 基于"已有音频"

| 参数 | 类型 | 说明 |
|---|---|---|
| `audio_id` | string | 已有音频 ID。**`extend` / `concat` 等基于已有音频的操作需要填** |
| `audio_urls` | array | 参考音频 URL 列表。**`inspo` 要求 1~4 个**公网可访问地址 |
| `mashup_audio_ids` | array | 用于混合的音频 ID 列表。**`mashup` 需要填** |
| `continue_at` | number | 从已有音频第几秒继续。例：`213.5` = 3 分 33.5 秒 |
| `replace_section_start` | number | `replace_section` 要替换片段的**开始**秒数 |
| `replace_section_end` | number | `replace_section` 要替换片段的**结束**秒数 |
| `samples_start` | number | 添加采样的开始秒数，默认 `0` |
| `samples_end` | number | 添加采样的结束秒数，**需小于歌曲总时长** |
| `underpainting_start` | number | 添加伴奏的开始秒数，默认 `0` |
| `underpainting_end` | number | 添加伴奏的结束秒数，需小于歌曲总时长 |
| `overpainting_start` | number | 添加人声的开始秒数，默认 `0` |
| `overpainting_end` | number | 添加人声的结束秒数，需小于歌曲总时长 |

### 任务通知

| 参数 | 类型 | 说明 |
|---|---|---|
| `callback_url` | string | 任务完成或失败时由平台主动通知的 **HTTPS** 地址。同步接口可不传 |

---

## 三、可直接抄的请求体

**① 灵感模式（最快出一首，0.65 元）**

```json
{
  "type": "generate",
  "custom": false,
  "prompt": "一首轻快的城市清晨民谣，木吉他扫弦，温暖男声，中速"
}
```

**② 自定义模式（自己给词和风格）**

```json
{
  "type": "generate",
  "custom": true,
  "title": "凌晨两点的环路",
  "lyric": "[Verse 1]\n路灯把影子拉长\n...",
  "style": "城市民谣, 木吉他, 温暖男声, 慢速, 略带疲惫",
  "style_negative": "电子, 说唱, 高亢",
  "vocal_gender": "m",
  "weirdness": 0.3,
  "style_influence": 0.7
}
```

**③ 让 AI 按主题自动写词**

```json
{
  "type": "generate",
  "custom": true,
  "lyric_prompt": "写一首关于毕业那天最后一次走出校门的歌，副歌要明亮",
  "style": "青春流行, 钢琴, 合唱感"
}
```
> `custom: true` + `lyric` 留空 → 才轮到 `lyric_prompt` 生效。

**④ 纯伴奏（做 BGM / 练唱底带）**

```json
{
  "type": "generate",
  "custom": false,
  "prompt": "lofi 学习背景音乐，钢琴，无人声，循环感",
  "instrumental": true
}
```

**⑤ 灵感模式（给几段参考音频）**

```json
{
  "type": "inspo",
  "audio_urls": [
    "https://你的存储/ref1.mp3",
    "https://你的存储/ref2.mp3"
  ],
  "prompt": "参考这两段的氛围，做一首更明亮的版本"
}
```

**⑥ 续写（从 3 分 33.5 秒处接着写）**

```json
{
  "type": "extend",
  "audio_id": "<audio_id>",
  "continue_at": 213.5
}
```

**⑦ 分离人声与伴奏**

```json
{ "type": "stems", "audio_id": "<audio_id>" }
```

**⑧ 四轨全分**

```json
{ "type": "all_stems", "audio_id": "<audio_id>" }
```

**⑨ 母带重制**

```json
{ "type": "remaster", "audio_id": "<audio_id>" }
```

**⑩ 混音（多首混合）**

```json
{ "type": "mashup", "mashup_audio_ids": ["<id1>", "<id2>"] }
```

---

## 四、拿到 task_id 之后

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/query" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_id":"<上一步返回的 task_id>"}'
```

`query` **免费**，可以放心轮询。结果里会带后续操作要用的 `audio_id`
（导出 WAV/MP4/MIDI、分轨、续写、做歌手风格都要它）。
