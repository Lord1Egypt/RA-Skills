# 音色与歌手风格 · `voice_clone` / `persona` / `upload_audio`

想让 AI **用你的声音**唱，或者让一系列歌**保持同一个人设**，就靠这三个接口。

三个都是**同步**接口。

---

## `voice_clone` · 声音克隆

```
POST https://api.a7w.cn/api/v1/apps/music_generation/voice_clone
模式：同步    计费：20 点（0.20 元）
```

基于清晰人声音频创建**私有的声音风格 ID**。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `audio_url` | string | **是** | 可公开访问的 **MP3 或 WAV** 人声音频 URL。**至少 10 秒**，建议单人清晰人声，尽量避免背景噪音或背景音乐 |
| `name` | string | 否 | 自定义声音风格名称 |
| `description` | string | 否 | 自定义声音风格描述 |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/voice_clone" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_url":"https://你的存储/我的清唱.mp3","name":"我的声音","description":"清亮男声"}'
```

### 参考音频的质量决定成败

| 要求 | 说明 | 做不到会怎样 |
|---|---|---|
| 格式 | MP3 或 WAV | 直接报错 |
| 时长 | **≥10 秒**，建议 30 秒以上 | 太短音色不稳 |
| 人声 | **单人清晰** | 多人会混出奇怪音色 |
| 环境 | **无背景噪音、无背景音乐** | 音色里带上噪音，唱出来很脏 |
| 访问 | **公网可访问 URL** | 不支持本地路径、不支持 Base64 |

> **录音建议**：找个安静房间，手机自带录音机就行，念一段或唱一段 30 秒，
> 中间别停太久。传到你自己的图床 / 对象存储拿公网链接。

### 拿到 ID 之后

`voice_clone` 返回的音色 ID 填进 `create` 的 `persona_id`，之后**所有歌都用这个音色**：

```json
{
  "type": "generate",
  "custom": true,
  "lyric": "...",
  "style": "...",
  "persona_id": "<voice_clone 返回的 ID>"
}
```

**克隆只需做一次**（0.20 元），之后反复使用不再收费 —— 这是做矩阵号最划算的一笔投入。

---

## `persona` · 创建歌手风格

```
POST https://api.a7w.cn/api/v1/apps/music_generation/persona
模式：同步    计费：12 点（0.12 元）
```

基于**已生成的歌曲**创建可复用的**歌手风格 ID**。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `audio_id` | string | **是** | 音频 ID，用于定位已生成或已上传的音频片段 |
| `name` | string | **是** | 歌手风格名称 |
| `vocal_start` | number | 否 | 人声片段**开始**时间，单位秒 |
| `vocal_end` | number | 否 | 人声片段**结束**时间，单位秒 |
| `description` | string | 否 | 歌手风格的文字描述 |
| `vox_audio_id` | string | 否 | 用于创建新歌手风格的人声参考音频 ID |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/persona" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_id":"<已生成歌曲的 audio_id>","name":"城市夜行者","vocal_start":30,"vocal_end":60,"description":"略带沙哑的温暖男声"}'
```

### 和 `voice_clone` 的区别

| | `voice_clone` | `persona` |
|---|---|---|
| 输入 | **你上传的**真实人声 URL | **已生成的**歌曲（audio_id） |
| 用途 | 让 AI 用**你的**音色唱 | 从已有作品里提取一个**可复用的人设** |
| 场景 | 个人 IP、想让 AI 复刻自己 | 一部剧 / 一个账号的**统一唱腔** |
| 计费 | 20 点 | 12 点 |

**`vocal_start` / `vocal_end` 很关键** —— 用它**只截取副歌那几秒**做人设，
比整首歌更干净、更聚焦。比如副歌是 30~60 秒，就传 `30` / `60`。

### 配合 `type` 使用

拿到 `persona_id` 后，`create` 里有两种用法：

| `type` | 效果 |
|---|---|
| `artist_consistency` | 按指定歌手风格生成 |
| `artist_consistency_vox` | **人声模式** + 指定歌手风格生成（更聚焦唱腔） |

---

## `upload_audio` · 上传参考音频

```
POST https://api.a7w.cn/api/v1/apps/music_generation/upload_audio
模式：同步    计费：13 点（0.13 元）
```

提交可访问的音频地址，返回**可用于后续创作的音频 ID**。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `audio_url` | string | **是** | 可公开访问的音频文件 URL，用于生成后续创作需要的音频 ID |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/upload_audio" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_url":"https://你的存储/一段旋律.mp3"}'
```

### 为什么需要它

很多操作（`extend`、`concat`、`stems`、`remaster`、`cover`…）都要 **`audio_id`**，
而不是 URL。你手上只有文件时，先用 `upload_audio` 换一个 `audio_id`：

```
你的本地/网盘音频
      ↓ 传到公网（对象存储 / 图床）
   audio_url
      ↓ upload_audio（0.13 元）
   audio_id
      ↓
extend / concat / stems / remaster / cover / vox / wav / mp4 / midi ...
```

> 已经在平台上生成过的歌，结果里**直接带 `audio_id`**，不需要再走这一步。

---

## 三个接口怎么选

| 我想… | 用 |
|---|---|
| 让 AI 用**我的**声音唱 | `upload_audio`（可选）→ `voice_clone` |
| 给一个账号 / 一部剧固定唱腔 | `persona`（从已有作品提取） |
| 把手上的音频变成能继续加工的素材 | `upload_audio` |
| 统一角色 + 更聚焦唱腔 | `persona` + `type: "artist_consistency_vox"` |
