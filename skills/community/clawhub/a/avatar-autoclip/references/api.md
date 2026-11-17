# 接口参考（逐字段）

上游开放 API 的**唯一正确路径形式**：

```
https://<域名>/api/v1/apps/<应用代号>/<接口代号>
```

> ⚠️ 平台 `GET /api/v1/apps/<app>` 返回的 `endpoint_path` 字段**不可信**。
> 实测 `smart_clip` 给的是 `/v1/clip/template`、`voice_tts` 给的是 `/v1/tts`，
> 这些都不是能通的地址。两个代号都取接口返回里的 `code` 字段。

本包涉及的三个应用：

| 应用 | 应用代号 | 干什么 |
|---|---|---|
| 图片数字人 | `pic_lipsync` | 一张人物图片 + 音频 → 口播视频 |
| 智能剪辑 | `smart_clip` | 模板 + 口播视频/素材/音频 → 成片 |
| 语音 TTS | `voice_tts` | 文案 → 音频（数字人的前置） |

---

## 一、鉴权与公共约定

```http
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

响应统一是 `{"code":1|0,"msg":"…","data":…}`。**但中转网关会再套一层**，
详见下面「响应信封」一节。

### 公共可选字段（与业务 JSON 同级）

| 字段 | 说明 |
|---|---|
| `callbackUrl` | 异步终态时向该地址 POST JSON。**注意是驼峰 `callbackUrl`**，不是下划线的 `callback_url` |
| `smart_route` | `on` / `auto` / `off`，智能路由开关；仅标记支持的接口生效 |
| `storage` | 结果转存到自己的对象存储（AK/SK 不落库） |

---

## 二、图片数字人 `pic_lipsync`

### 2.1 提交任务

```
POST /api/v1/apps/pic_lipsync/submit
```

| 参数 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `model` | 否 | `super-lipsync-pro` | **只有这一个可选值** |
| `mode` | 否 | `audio` | `audio` 音频驱动；`text` 文案驱动 |
| `image_url` | **是** | — | 人物图片 URL |
| `audio_url` | **是** | — | audio 模式=驱动音频；**text 模式=参考音色**（也必须给） |
| `content` | text 模式**是** | — | 要朗读的口播文案 |
| `prompt` | 否 | — | 人物动作、表情、画面风格提示词 |
| `quality` | 否 | `standard` | `fast` / `standard` / `max` |

**两个容易踩的点：**

1. **text 模式也必须传 `audio_url`** —— 它是"参考音色"，不是可选。想纯文案驱动，
   得先有一个音色样本音频。
2. **计费按输入音频的实际时长结算**。音频地址探测不到时长时接口**直接拒绝创建**，
   不会用默认时长兜底（这是为了避免不明确扣费）。所以音频 URL 必须公网可达。

响应：

```json
{"code":1,"msg":"success","data":{
  "task_id":"task_xxxxxxxxxxxx","status":"pending",
  "app":"pic_lipsync","api":"submit","frozen_points":19.44}}
```

> 提交即**冻结**点数（`frozen_points`），完成后按实际时长结算。

### 2.2 查询任务

```
POST /api/v1/apps/pic_lipsync/query      body: {"task_id":"task_xxx"}
```

**也可以走通用路由** `GET /api/v1/tasks/{task_id}`（推荐，模型与应用任务共用）。

完成时的实测响应（走应用级 query）：

```json
{"code":1,"msg":"success","data":{
  "result":"任务完成","status":"completed","progress":100,
  "duration":4.875,"resolution":"480x832",
  "output_url":"https://cdn2.example.com/xxx.mp4",
  "cover_url":"https://cdn2.example.com/xxx.mp4",
  "unique_id":"5c6a2f039fdb26384caef26a7a935bea",
  "created_at":"2026-10-08 12:10:59","updated_at":"2026-10-08 12:11:35"}}
```

> ⚠️ **视频地址在 `output_url`，不是 `video_url`。**
> 而且实测 `cover_url` 有时和 `output_url` 是同一个视频地址（上游把视频塞进了封面字段）。
> 所以取结果必须按优先级多字段兜：`video_url` → `video_uri` → `output_url` → `result_url`。
> 本包的 `find_deep()` 就是干这个的。

> ⚠️ 返回的 URL 文件名可能带 `_4k` / `vr_` 之类的前缀，那是对象存储的命名，
> **不代表分辨率**。实测拿到 `vr_xxx_4k.mp4`，ffprobe 出来是 480x832。

---

## 三、智能剪辑 `smart_clip`

三个提交接口对应三种模板场景，**模板不能跨场景使用**。

| 场景 `scene` | 提交接口 | 输入 |
|---|---|---|
| `realMan` | `realman_broadcast` | **口播视频** + 素材 |
| `oralMixCutting` | `broadcast_mixcut` | **音频** + 素材 |
| `newsMixCutting` | `news_mixcut` | **标题** + 素材（无人声驱动） |

### 3.1 模板列表（同步免费）

```
GET /api/v1/apps/smart_clip/template?scene=realMan&pageSize=10&sortBy=desc
```

| 参数 | 位置 | 必填 | 说明 |
|---|---|---|---|
| `scene` | query | **是** | `realMan` / `oralMixCutting` / `newsMixCutting` |
| `pageSize` | query | 否 | 默认 10 |
| `sid` | query | 否 | **分页游标**：返回里有 `sid` 就代表还有下一页，翻页时原样回传 |
| `searchKey` | query | 否 | `name` / `id` |
| `searchValue` | query | 否 | 搜索值 |
| `sortBy` | query | 否 | `desc`（默认，按上架时间倒序）/ `asc` |

响应 `data.results[]`：`id`、`name`、`coverUrl`、`scene`、`demoUrl`（样片）、`ratio`。
`data.sid` 有值 = 还有下一页。

> 分页是**游标式**（`sid`），不是页码式。传 `page=2` 没用。

### 3.2 模板详情（同步免费）

```
GET /api/v1/apps/smart_clip/template_detail?id=<模板ID>
```

| 字段 | 说明 |
|---|---|
| `videoStructInfo.editInfo.canvas` | `{width, height}`，模板画布尺寸 |
| `...editInfo.headerLayer` | 标题图层，`{}` = 模板没有这个图层 |
| `...editInfo.subtitleLayer` | 字幕图层 |
| `...editInfo.ipLayer` | 身份栏图层 |
| `...editInfo.figureLayer` | 数字人图层 |
| `...editInfo.backgroundLayer` | 背景图层 |

图层结构：`width`、`height`、`transform.{anchor,scalar,position}`、`uri`（仅背景图层）。
`anchor` / `scalar` **不支持修改**。

### 3.3 真人口播混剪

```
POST /api/v1/apps/smart_clip/realman_broadcast
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `styleId` | **是** | 模板 ID（必须是 `realMan` 场景的） |
| `videoUrl` | **是** | 口播视频 URL，mp4/mov。平台会**优先探测该媒体时长用于计费** |
| `language` | 否 | 视频中语音的语种，参考 ASR 支持的语种 |
| `title` | 否 | 标题。**不想显示标题就不要传这个字段** |
| `subtitle` | 否 | 字幕数组（兼容 `subtitles`），每项 `startMs`/`endMs`/`text` |
| `materials` | 否 | 素材数组，每项 `type`(image/video) + `fileUrl` |
| `materialSoundSwitch` | 否 | 素材是视频时的原声开关，默认 `false` |
| `introduceCard` | 否 | 身份栏：`{name, description}` |
| `packRules` | 否 | 包装开关，见下 |
| `processRules` | 否 | 处理规则，见下 |
| `structLayers` | 否 | 要改的图层 |
| `callbackUrl` | 否 | 结果回调地址 |

`processRules`：

| 字段 | 默认 | 说明 |
|---|---|---|
| `watermarkShow` | `false` | 加"AI生成"字样水印 |
| `resourcePreprocessMethod` | 不设置=保持原时长 | `roughCut` 粗剪（自动去无声片段）/ `sliceMerge` 按 subtitle 时间轴去不连续片段 |
| `materialMatchWay` | `preciseMatch` | `fuzzyMatch` / `preciseMatch` |
| `metadata` | — | 元水印，**只支持一组，且 value 必须是字符串** |
| `firstFrameCover` | — | 首帧封面：`coverSwitch`/`templateId`/`imageUrl`/`resultImageUrl`（后两者二选一，`resultImageUrl` 优先且直接当首帧） |

### 3.4 素材混剪

```
POST /api/v1/apps/smart_clip/broadcast_mixcut
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `styleId` | **是** | `oralMixCutting` 场景的模板 ID |
| `materials` | **是** | 素材数组 |
| `audioUrl` | 否 | 音频 URL（mp3/wav/m4a，<5min，≤100MB）。**与 `content` 二选一** |
| `content` | 否 | 文案，3~1800 字符 —— **当前平台不支持这个分支** |
| `speakerId` / `speakerExtra` | 否 | 音色 —— **当前平台不支持这个分支** |

> 🚫 **关键限制**：`broadcast_mixcut` 目前**只支持 `audioUrl` 或素材链路**。
> 传 `content` 或 `speakerId` 会返回 `unsupported_speaker_branch`。
> 要文案驱动就走 `pic_lipsync` 的 text 模式。
> 本包在本地就把这个分支拦掉，不浪费一次调用（退出码 4）。

### 3.5 新闻体视频

```
POST /api/v1/apps/smart_clip/news_mixcut
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `styleId` | **是** | `newsMixCutting` 场景的模板 ID |
| `title` | **是** | 3~1800 字符 |
| `materials` | **是** | 素材数组。平台探测素材时长用于计费 |
| `processRules.videoDuration` | 否 | 5~300 秒，默认跟随素材时长 |
| `processRules.materialComposition` | 否 | `random`（默认）/ `order` |
| `processRules.watermarkShow` | 否 | 默认 `false` |
| `processRules.metadata` | 否 | 元水印，一组，value 字符串 |
| `processRules.firstFrameCover` | 否 | 首帧封面 |

> ⚠️ `news_mixcut` **没有 `videoUrl`** —— 它不靠人声驱动，靠标题 + 素材。
> 其中 `voice_tts` 的 TTS 可以先生成旁白音频，但 `news_mixcut` 本身不吃 `audioUrl`；
> 要"配音 + 新闻体"请自己把音频合进素材，或改用 `pic_lipsync` + `realman_broadcast`。

### 3.6 三个提交接口共用的对象

`subtitle[]`：

| 字段 | 必填 | 说明 |
|---|---|---|
| `startMs` | 是 | 开始时间，ms |
| `endMs` | 是 | 结束时间，ms，**最大 310000** |
| `text` | 是 | 文本，**只支持单字符级别** |

> `text` 是**单字符级**的！上游 ASR 返回的就是逐字时间轴，直接回填这里。
> 自己按整句填不算错，但和 ASR 结果对齐时要注意这个粒度。

`materials[]`：

| 字段 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `type` | 是 | — | `image` / `video` |
| `fileUrl` | 是 | — | 素材 URL |
| `soundSwitch` | 否 | `false` | 素材为视频时的原声开关（素材混剪与新闻体支持） |

`introduceCard`：`{name, description}`，身份栏。

`packRules`：

| 字段 | 说明 |
|---|---|
| `headerSwitch` | 标题包装开关 |
| `materialSwitch` | 素材包装开关 |
| `subtitleSwitch` | 字幕包装开关 |
| `keywordSwitch` | 关键词包装开关 |
| `backgroundMusic.audioSwitch` / `.audioUrl` / `.volume` | 背景音乐。传了 `audioUrl` 优先于模板内置；`volume` 默认 `0.3`，范围 0~1，**保留一位小数** |

> `packRules` 只控制"是否参与效果包装"，**不能控制图层的显示/隐藏** —— 那是 `structLayers` 的活。

`structLayers[]`：

| 字段 | 必填 | 说明 |
|---|---|---|
| `markCode` | 是 | `headerLayer` / `subtitleLayer` / `ipLayer` / `backgroundLayer` / `figureLayer` |
| `show` | 否 | 不设置则跟随模板。**`backgroundLayer` / `figureLayer` 不支持设置** |
| `showMode` | 否 | `always` / `customize`，仅 `headerLayer` 生效 |
| `showTime` | 条件必填 | `headerLayer` + `showMode=customize` 时**必填且 >0**，保留 3 位小数 |
| `layer.transform.position` | 否 | 锚点定位 |
| `layer.uri` | 否 | 背景图，**仅 `backgroundLayer` 生效** |

---

## 四、语音 TTS `voice_tts`

`voice_tts` 下有 6 个接口：

| API 编码 | 方法 | 模式 | 实测状态 |
|---|---|---|---|
| `tts_async` | POST | 异步 | ✅ **可用**（本包默认走这条） |
| `tts_live` | POST | 异步 | ✅ 可用（WebSocket 流式上游） |
| `tts` | POST | 同步 | ❌ **实测坏**：任何参数都返回 `{"code":0,"msg":"任务处理失败，请稍后重试"}` |
| `list_voices` | GET | 同步 | ✅ 免费 |
| `stt` | POST | 同步 | 语音转文字 |
| `clone_voice` | POST | — | 本包不涉及 |

### 4.1 文案转音频（异步，推荐）

```
POST /api/v1/apps/voice_tts/tts_async      # 或 tts_live
```

提交后返回 `task_id`，用 `GET /api/v1/tasks/{task_id}` 取 `result.audio_url`。

| 参数 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `text` | **是** | — | `tts_async` 适合长文本（最大约 10000 字符） |
| `reference_id` | 否 | — | **音色模型 ID**。不传就用平台默认音色（实测可用）。单说话人传 string；多说话人（仅 `s2-pro`）可传 string[] |
| `model` | 否 | `s2-pro` | `s1` / `s2-pro` |
| `format` | 否 | `mp3` | `wav` / `pcm` / `mp3` / `opus` |
| `prosody` | 否 | — | `{speed, volume, normalize_loudness}` |
| `callback_url` | 否 | — | 回调地址；不传就轮询 |

响应：

```json
{"code":1,"msg":"success","data":{
  "task_id":"task_xxx","status":"pending","app":"voice_tts","api":"tts_async",
  "frozen_points":150,"actual_points":0}}
```

完成后：

```json
{"code":1,"msg":"success","data":{
  "task_id":"task_xxx","model":"voice_tts/tts_async","type":"app",
  "status":"completed",
  "result":{"format":"mp3","audio_url":"https://cdn2.example.com/aigc/awaud_xxx.mp3"},
  "usage":{"points_cost":0.7}}}
```

**实测数据**（2.1 秒中文短句）：

| 路由 | 冻结 | 实扣 | 耗时 |
|---|---|---|---|
| `tts_async` | 150 点 | **0.7 点** | ~3 秒（+结果落全延迟） |
| `tts_live` | 180 点 | 0.84 点 | ~6 秒 |

> 冻结点数（150/180）远大于实扣（0.7/0.84）—— **预算要按冻结值留余量**，
> 结算以 `usage.points_cost` 为准。

> ⚠️ **音频地址也吃"completed 后结果为空"那个竞态。**
> 实测第一次查到 `completed` 时 `audio_url` 是 `""`，**再等 ~30 秒才落全**。
> 轮询必须带结果字段兜底（本包 `require_keys=("audio_url",…)`）。

### 4.2 文案转音频（同步，实测不可用）

```
POST /api/v1/apps/voice_tts/tts
```

参数与上面基本一致（外加 `latency` / `top_p` / `temperature` / `chunk_length`
/ `min_chunk_length` / `max_new_tokens` / `repetition_penalty` /
`condition_on_previous_chunks` / `mp3_bitrate` / `opus_bitrate` / `normalize` /
`sample_rate`，同步接口建议 ≤500 字符）。

**但实测在 `api.a7w.cn` 上这条路由一律返回
`{"code":0,"msg":"任务处理失败，请稍后重试"}`** —— 换了音色、换了模型、换了中英文都一样，
是**上游服务侧**的问题，不是参数问题。**要音频请走 `tts_async`。**
（保留本节是因为自建域名下可能正常，且上游修好后可以直接切回来。）

### 4.3 语音转文字（ASR）—— 做卡拉OK字幕的关键

```
POST /api/v1/apps/voice_tts/stt
```

| 参数 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `audio_url` | 否 | — | 音频 URL（与文件上传二选一） |
| `language` | 否 | 自动检测 | 识别语言 |
| `ignore_timestamps` | 否 | **`true`** | **要字级时间轴必须显式传 `false`** |

> ⚠️ 默认 `ignore_timestamps=true` 会**丢掉时间戳**，拿回来的分段是空的。
> 想用来填 `subtitle[]` 就必须传 `false`。

实测返回（`ignore_timestamps=false`）：

```json
{"code":1,"msg":"success","data":{
  "result":{
    "duration":2.0636875,"language":"Chinese","language_code":"zh",
    "segments":[
      {"end":0.16,"start":0,   "text":"大"},
      {"end":0.32,"start":0.16,"text":"家"},
      {"end":0.56,"start":0.32,"text":"好"},
      {"end":0.72,"start":0.56,"text":"欢"},
      {"end":0.80,"start":0.80,"text":"迎"},
      {"end":0.96,"start":0.80,"text":"来"}
    ],
    "text":"大家好，欢迎来到今天的分享。"},
  "usage":{"points_cost":40,"actual_points":40}}}
```

**三个关键点**（本包 `subtitles_from_asr()` 全部处理了）：

1. **单位是秒**，要 ×1000 换成 `startMs`/`endMs`
2. **粒度是单字符** —— 正好匹配上游 `subtitle[].text` 的"只支持单字符级别"要求
3. **`segments[].text` 不含标点，但 `text` 字段里有完整标点**。
   要复现"卡拉OK逐字高亮 + 标点正确"的效果，得把标点按字符顺序**对齐补回**到对应的字上

另外实测有 **`{"start":0.80,"end":0.80}` 这种零时长段**，
而上游要求 `endMs > startMs`，所以必须做修正（本包补到下一个字的起点，或 +40ms）。

费用：**40 点/次**（按次，不按时长）。

### 4.4 音色列表（免费）

```
GET /api/v1/apps/voice_tts/list_voices?page_size=20&page_number=1
```

可传 `tag` / `title` / `sort_by`(score/task_count/created_at) / `language` / `title_language`。
返回 `data.total` + `data.items[]`，每项有 `id`（= `reference_id`）、`title`、`state`。

### 4.3 语音转文字

```
POST /api/v1/apps/voice_tts/stt
```

`audio_url`（或文件上传）、`language`、`ignore_timestamps`（默认 `true`）。
**要拿字级时间轴去填 `subtitle[]` 就必须传 `ignore_timestamps=false`。**

---

## 五、参考生图 `nano_banana`（1 张参考图 → N 张同风格人物图）

这是「只提供一张参考图，生成多张同风格人物图」的那一步。

```
POST /api/v1/apps/nano_banana/submit
GET  /api/v1/apps/nano_banana/query?task_id=<id>
```

### 请求参数

| 参数 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `prompt` | **是** | — | 图片内容、风格、主体和细节描述 |
| `action` | 否 | `generate` | **`generate` = 文生图；`edit` = 基于参考图编辑（参考生图）** |
| `image_urls` | `action=edit` 时**是** | — | 参考图 URL 列表 |
| `resolution` | 否 | `1K` | `1K` / `2K` / `4K`（官方高清模型按档位计费） |
| `aspect_ratio` | 否 | — | 宽高比，竖版用 `9:16` |
| `model` | 否 | `nano-banana` | 普通模型 / 官方模型（官方模型一致性更高、支持高清档） |
| `callback_url` | 否 | — | 完成回调 |

### 参考生图怎么用

**保住人物身份的关键是 prompt 里的一句话**，不能省：

```
保持参考图里同一个人的面部特征、五官比例、发型与整体气质完全一致，
只改变场景、服装与姿态；<新的场景描述>。真实照片质感，竖版构图，光线自然。
```

`action=edit` + `image_urls=[参考图]` + 上面这句，就能得到**同一个人换场景/服装/姿态**的新图。
同一张参考图配不同的后半句，就得到一组「同一身份、可直接拿去做口播」的竖版人物图。

### 响应

```json
{"code":1,"msg":"success","data":{
  "task_id":"task_xxx","status":"pending",
  "app":"nano_banana","api":"submit","frozen_points":72}}
```

完成后：

```json
{"code":1,"msg":"success","data":{
  "task_id":"task_xxx","model":"nano_banana/submit","status":"completed",
  "result":{
    "success":true,"prompt":"…","trace_id":"…",
    "image_url":"https://cdn2.example.com/aigc/awimg_xxx.png",
    "data":[{"prompt":"…","image_url":"https://cdn2.example.com/aigc/awimg_xxx.png"}],
    "results":[{"prompt":"…","image_url":"https://cdn2.example.com/aigc/awimg_xxx.png",
                "transfer_status":"success"}],
    "upstream_task_id":"…"},
  "usage":{"points_cost":24}}}
```

> ⚠️ **图片地址同时在三个层级出现**：`result.image_url`、`result.data[].image_url`、
> `result.results[].image_url`。别只认一个字段，**三层都收一遍再去重**
> （本包 `collect_image_urls()`）。

**实测数据**：1K / 9:16，约 **35 秒**出图，**24 点/张**（冻结 72 点，按实际结算）。
输出尺寸实测 **768x1344**（9:16）。

---

## 六、公共接口

| 接口 | 说明 |
|---|---|
| `GET /api/v1/tasks/{task_id}` | 通用任务查询（模型与应用任务共用）。返回 `task_id`/`model`/`type`/`call_type`/`status`/`result`/`usage`/`error` |
| `GET /api/v1/user/balance` | 当前 Key 的可用点数 |
| `GET /api/v1/user/usage?start_date=&end_date=` | 使用量统计（`Y-m-d`） |
| `GET /api/v1/pricing?type=app_api&app_code=&api_code=` | 单个接口的有效价格 |
| `POST /api/v1/pricing/batch` | 批量查价，`items` 最多 100 条 |
| `POST /api/v1/upload` | 临时文件上传，`multipart/form-data` 单字段 `file`，默认单文件 ≤512MB |

`GET /api/v1/tasks/{task_id}` 的 `status`：
`pending` / `processing` / `completed` / `failed` / `cancelled`。

> 任务**只能由创建它的 Key 所属租户和用户查询**。

`POST /api/v1/upload` 返回的 `url` **最长有效 24 小时**，平台可能提前回收。
不要把它当持久地址写进数据库或素材库。

---

## 七、响应信封（四个形态）

这是接这个平台最容易翻车的地方。同一个接口在不同网关下信封不同：

```jsonc
// 形态 1：直连租户域名
{"code":1,"msg":"success","data":{"results":[...]}}

// 形态 2：api.a7w.cn 中转，把上游响应体整个塞进 data.result
//   注意：中转层会在 data 里**同时**放 result 和 usage
{"code":1,"msg":"success","data":{
   "result":{"code":"Succeed","data":{"results":[...],"sid":"..."},"requestId":"..."},
   "usage":{"points_cost":0,"actual_points":0}}}

// 形态 3：个别接口不经二次包装（如音色列表）
{"code":1,"msg":"success","data":{"total":38,"items":[...]}}

// 形态 4：网关错误对象
{"error":{"message":"点数余额不足","type":"insufficient_points","code":"insufficient_points"}}
```

### 💥 坑一：`result` 是双重身份字段

任务查询**完成后**，`data` 里**也有一个 `result`**
（`{"status":"completed","result":{"video_url":"..."}}`），
它和形态 2 的包装字段**同名**。

无脑"看到 `result` 就往下钻"会把 `status` 丢掉 —— 结果是**轮询永远等不到终态**。

**正确判据**（按顺序）：

| 情况 | `data.result` 长什么样 | 怎么处理 |
|---|---|---|
| **A** | 是个**带 `code` 的信封**（`{"code":"Succeed","data":{…}}`） | **一定是中转包装层 → 剥掉** |
| **B** | 是数组 | `data` 没有别的字段 → 归一成 `{"results":[…]}`；否则原样返回 |
| **C** | 是普通对象（没有 `code`） | `data` 还有 `status`/`task_id` → **原样返回，保留 status** |
| **D** | 是标量（如 `"任务完成"`） | 整个 `data` 才有意义 |

### 💥 坑二：判据 A 必须排在"看兄弟字段"之前

中转层会给 `data.result` 配一个 `usage` 兄弟字段：

```json
{"data":{"result":{"code":"Succeed","data":{"results":[…]}},"usage":{"points_cost":0}}}
```

如果判据写成「**只有当 `data` 里除了 `result` 没有别的字段时才剥**」，
那么带 `usage` 的这种就**不会被剥**，`results` 永远取不到 ——
**表现是"模板列表永远是空的"**，而且接口返回是 `code:1 success`，
看起来一切正常，极难排查。

所以**判据 A（result 自己是信封）优先于兄弟字段判断**。

> 本包 `unwrap()` 已按 A→B→C→D 实现，`scripts/selftest.py` 对这四种形态
> 各有回归用例（含带 `usage` 兄弟字段的两个）。

---

## 八、退出码（本包约定）

| 码 | 含义 |
|---|---|
| 0 | 成功 |
| 2 | 用法错误（参数缺失、格式不对、找不到 Key） |
| 3 | 上游接口错误（`code=0`、HTTP 4xx/5xx） |
| 4 | **本地预检不通过** —— 没有任何请求发出，不产生费用 |
| 5 | 超出 `--budget` 预算 |
| 6 | 等待任务超时（任务可能仍在跑，用 `task <id>` 继续查） |
| 7 | **缺少授权声明** —— 涉及真实人像/声音但没传 `--authorized` |
