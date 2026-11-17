# 导出与查询 · `wav` / `mp4` / `midi` / `vox` / `query`

歌生成出来了，这几个接口负责**把它变成能交付的文件**。

---

## `query` · 查询音乐任务

```
POST https://api.a7w.cn/api/v1/apps/music_generation/query
模式：同步    计费：免费
```

按平台任务 ID 查询任务状态与结果。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `task_id` | string | **是** | 提交任务时返回的平台任务 ID |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/query" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_id":"<task_id>"}'
```

**免费，放心轮询。** 结果里的 `audio_id` 是后续几乎所有操作的入场券
（导出、分轨、续写、做人设都要它）。

> `a7w.py call` 默认会**自动轮询到结束**，一般不用手写轮询；
> 只有加 `--no-wait` 时才需要自己 `query`。

---

## `wav` · 导出高质量 WAV

```
POST https://api.a7w.cn/api/v1/apps/music_generation/wav
模式：异步    计费：14 点（0.14 元）
```

基于音频 ID 导出**高质量 WAV 文件**。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `audio_id` | string | **是** | 音频 ID |
| `callback_url` | string | 否 | 任务完成/失败时平台主动通知的 HTTPS 地址 |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/wav" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_id":"<audio_id>"}'
```

**要交付成品就用它。** 0.14 元换一份无损，比省这点钱交个有损音频划算得多。

---

## `mp4` · 导出 MP4

```
POST https://api.a7w.cn/api/v1/apps/music_generation/mp4
模式：同步    计费：20 点（0.20 元）
```

基于音频 ID 获取**视频文件链接**。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `audio_id` | string | **是** | 音频 ID |
| `callback_url` | string | 否 | 任务完成/失败时平台主动通知的 HTTPS 地址 |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/mp4" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_id":"<audio_id>"}'
```

**同步返回**，直接拿视频链接。适合要直接发视频平台、不想自己配画面的场景。

---

## `midi` · 导出 MIDI

```
POST https://api.a7w.cn/api/v1/apps/music_generation/midi
模式：异步    计费：14 点（0.14 元）
```

基于音频 ID **提取 MIDI 文件**。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `audio_id` | string | **是** | 音频 ID |
| `callback_url` | string | 否 | 任务完成/失败时平台主动通知的 HTTPS 地址 |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/midi" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_id":"<audio_id>"}'
```

**这是给"还想继续编"的人准备的。** MIDI 可以导进任意宿主软件（DAW）里
换音源、改和声、调节奏 —— AI 出个骨架，人来精修。

---

## `vox` · 人声处理

```
POST https://api.a7w.cn/api/v1/apps/music_generation/vox
模式：异步    计费：14 点（0.14 元）
```

基于音频 ID 提取**指定片段的人声或伴奏**处理结果。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `audio_id` | string | **是** | 音频 ID |
| `vocal_start` | number | 否 | 人声提取**开始**时间，单位秒 |
| `vocal_end` | number | 否 | 人声提取**结束**时间，单位秒 |
| `callback_url` | string | 否 | 任务完成/失败时平台主动通知的 HTTPS 地址 |

### 请求

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/vox" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_id":"<audio_id>","vocal_start":30,"vocal_end":75}'
```

**和 `create` 的 `stems` 怎么选？**

| 你要 | 用哪个 | 费用 |
|---|---|---|
| 只要**某一段**的人声/伴奏 | `vox` + `vocal_start/_end` | **0.14 元** |
| 要**整首**分离人声与伴奏两轨 | `create` 的 `type: "stems"` | 0.65 元 |
| 要**整首**分人声/鼓/贝斯/其他四轨 | `create` 的 `type: "all_stems"` | 0.65 元 |

只想拿副歌那段清唱做人设（`persona`）→ 用 `vox`，便宜又精准。

---

## 费用速查

| 接口 | 模式 | 点数 | 折合 |
|---|---|---|---|
| `query` | 同步 | **免费** | — |
| `vox` | 异步 | 14 | 0.14 元 |
| `midi` | 异步 | 14 | 0.14 元 |
| `wav` | 异步 | 14 | 0.14 元 |
| `mp4` | 同步 | 20 | 0.20 元 |

> 1 元 = 100 点。上表是**租户实际结算价**，平台另有标准价，**以你账号实际扣费为准**。

---

## 一条完整的交付链路

```bash
API=https://api.a7w.cn/api/v1/apps/music_generation
KEY=sk-你的key

# 1) 生成
TASK=$(curl -sS -X POST "$API/create" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"generate","custom":false,"prompt":"温暖的城市民谣，木吉他"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['data']['task_id'])")

# 2) 查结果拿 audio_id（免费）
AID=$(curl -sS -X POST "$API/query" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" -d "{\"task_id\":\"$TASK\"}" \
  | python -c "import sys,json;print(json.load(sys.stdin)['data']['audio_id'])")

# 3) 导无损（0.14 元）+ 拿时间轴做字幕（免费）
curl -sS -X POST "$API/wav"    -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" -d "{\"audio_id\":\"$AID\"}"
curl -sS -X POST "$API/timing" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" -d "{\"audio_id\":\"$AID\"}"
```

> 上面用 `python -c` 只是为了演示取字段；实际用 `scripts/a7w.py call` 会自动轮询，
> 一行命令就能拿到最终结果。
