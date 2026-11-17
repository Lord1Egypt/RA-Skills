---
name: ai-music-studio
slug: ai-music-studio
displayName: AI音乐生成歌曲写词作曲编曲演唱人声克隆翻唱伴奏分轨混音一键出歌
description: "输入一句话，AI 帮你写词、作曲、编曲、演唱，一首完整的歌只要 0.65 元。支持人声克隆与专属歌手风格，让 AI 用你的音色唱；支持 AI 翻唱、续写、混音、采样、母带重制、伴奏分离与分轨导出。含 17 种生成操作、13 个接口的完整参数表与真实计费口径。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
version: 1.0.1
summary: "一句话生成一首完整的歌——AI 写词、AI 作曲、AI 编曲、AI 演唱，从灵感到成品一首只要 0.65 元。支持歌词生成、风格优化、人声性别偏好、创意实验强度与风格影响强度调节；也能上传自己的声音做音色克隆、创建专属歌手风格，让 AI 用你的音色唱歌。还能对既有歌曲做 AI 翻唱、续写、拼接、混音、采样、局部替换、母带重制与分轨（人声 / 伴奏 / MIDI），覆盖文生音乐、参考曲风、灵感模式、自定义歌词等 17 种生成操作，以及歌词、风格、MIDI、WAV、MP4 导出与任务查询等 13 个接口。含完整参数表、真实计费口径（按点数计费，1 元 = 100 点）与零依赖客户端。适用于短视频配乐、短剧主题曲与片尾曲、电商带货 BGM、口播背景音乐、播客片头、游戏音效、个人音乐创作与 AI 翻唱玩梗。一个 Key 调用全部 AI 音乐算力，不用自己部署 GPU，也不用同时管几家的账单。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 三剪客
  - 设计多媒体
  - AI音乐
  - 音乐生成
  - AI写歌
  - 人声克隆
  - AI翻唱
  - 分轨
---

# AI 音乐工坊 · 一句话出一首歌

给一句话，拿走一首完整的歌——**有人声、有伴奏、有歌词、能下载**。

不用懂乐理，不用买音源，不用装宿主软件，也不用自己部署 GPU。
一台能跑 `curl` 的机器 + 一个 `api.a7w.cn` 的 Key，就够了。

| 你最关心 | 答案 |
|---|---|
| 一首歌多少钱 | **65 点 = 0.65 元**（1 元 = 100 点） |
| 要多久 | 异步任务，提交后轮询；`query` 免费 |
| 能商用吗 | 生成内容的使用与合规责任由使用者承担，推广前请自行核对平台与版权要求 |
| 要装什么 | **什么都不用装**。零依赖 Python 客户端只用标准库，或者直接用 `curl` |

---

## 一、一首歌，到底花多少钱

平台按**点数**计费，**1 元 = 100 点**。这个插件 13 个接口的**租户实际结算价**：

| 接口 | 做什么 | 模式 | 点数 | 折合 |
|---|---|---|---|---|
| **`create`** | **生成一首歌** | 异步 | **65** | **0.65 元** |
| `lyrics` | 生成歌词 | 同步 | 12 | 0.12 元 |
| `style` | 把你的风格描述优化得更专业 | 同步 | 14 | 0.14 元 |
| `mashup_lyrics` | 两段歌词融合成新版本 | 同步 | 12 | 0.12 元 |
| `voice_clone` | 克隆你的音色 | 同步 | 20 | 0.20 元 |
| `persona` | 创建可复用的歌手风格 | 同步 | 12 | 0.12 元 |
| `upload_audio` | 上传参考音频拿音频 ID | 同步 | 13 | 0.13 元 |
| `wav` | 导出高质量 WAV | 异步 | 14 | 0.14 元 |
| `mp4` | 导出带画面的 MP4 | 同步 | 20 | 0.20 元 |
| `midi` | 导出 MIDI（可再编曲） | 异步 | 14 | 0.14 元 |
| `vox` | 提取人声或伴奏 | 异步 | 14 | 0.14 元 |
| `timing` | 歌词时间轴（做字幕用） | 同步 | **免费** | — |
| `query` | 查任务状态与结果 | 同步 | **免费** | — |

**三种典型花法：**

| 做法 | 走了哪些接口 | 总价 |
|---|---|---|
| 最快出一首 | 只要 `create` | **0.65 元** |
| 词 + 曲 + 无损全包 | `lyrics` + `create` + `wav` | **0.91 元** |
| 用自己音色唱 | 上面这些 + `voice_clone`（克隆只需一次，可反复用） | **1.11 元** |

> **`lyrics` 一趟拿两样**：它返回的 `tags` 里**直接带一段专业编曲描述**，
> 可以当 `style` 用 —— 所以走 `lyrics` 就不用再单独调 `style`，省 0.14 元。
> 详见 [`references/api-lyrics.md`](references/api-lyrics.md)。

> ⚠️ 平台同时给出**标准价**和**租户实际结算价**，两者可能差很多。
> 上表是租户实际结算价；**以你账号里实际扣费为准**
> （每次返回的 `data.usage.points_cost` 就是本次真实扣费，可以直接对账）。
> 查询类接口（`query` / `timing`）免费，可以放心轮询。

---

## 一·五、先看一个真实输出

下面全部是**实际调用**的结果，不是示例编的。输入就一句话：

> `写一首关于凌晨加班后骑车回家的城市民谣，主歌写疲惫，副歌写希望`

**8.5 秒**后返回，AI 自己起了标题 **《夜归单车》**，歌词是完整的
Verse / Pre-Chorus / Chorus / Verse 2 / Bridge 结构：

```
[Verse 1]
楼下的风有点冷
我把领子竖了又竖
工牌还挂在胸口
像一天没卸下的负重

[Chorus]
我骑回家
天就快亮了
心里那点火
还没有熄呢
```

**同一次返回里，还附了一段可以直接用的专业编曲描述：**

```
City folk with gentle fingerpicked acoustic guitar, brushed percussion, and a
steady walking bass; verse feels weary and close-mic with sparse room tone,
pre-chorus lifts on layered harmonies and rising strings, chorus opens warm
and singable with gang-vocal echoes on the anchor phrase. Add a soft tape hiss,
passing-bus ambience between lines...
```

这段填进 `create` 的 `style`，就是上一节说的"省掉 0.14 元"。
**扣费 `usage.points_cost = 12`，与价目表完全一致。**

> 完整请求与返回结构见 [`references/api-lyrics.md`](references/api-lyrics.md)。

---

## 二、两种创作模式，别用错

`create` 的核心开关是 `custom`：

| | **灵感模式**（`custom: false`） | **自定义模式**（`custom: true`） |
|---|---|---|
| 你给什么 | 一句 `prompt`（≤500 字符） | `lyric` + `style`（+ `title`） |
| 谁写词 | AI 写 | **你给词**，或给 `lyric_prompt` 让 AI 按你的主题写 |
| 适合 | 快速试方向、批量铺 BGM | 要指定歌词、要精确控制风格 |
| 额外能调 | — | `weirdness`（创意强度）、`style_influence`（风格贴合度）、`style_negative`（**不想要**什么） |

**歌词与风格的字符上限随模型变**：

| 字段 | 常规模型 | 高质量模型 |
|---|---|---|
| `lyric` | ≤3000 字符 | ≤5000 字符 |
| `style` | ≤200 字符 | ≤1000 字符 |
| `title` | ≤80 字符 | ≤100 字符 |

> `custom: true` 且 `lyric` 为空时，才轮到 `lyric_prompt` 生效（AI 按你的主题自动写词）。

---

## 三、17 种生成操作，一张表看懂

`create` 的 `type` 参数决定干什么。**同一个接口，17 种玩法**：

**从零创作**

| `type` | 做什么 |
|---|---|
| `generate` | 根据提示词生成音乐（最常用） |
| `inspo` | 基于 **1~4 段参考音频**生成灵感作品（走 `audio_urls`） |
| `cover` | 参考既有曲风重新演绎 |
| `upload_cover` | 对**你上传的**音频做风格翻唱 |
| `artist_consistency` | 按指定歌手风格生成（走 `persona_id`） |
| `artist_consistency_vox` | 人声模式 + 指定歌手风格生成 |

**续写与拼接**

| `type` | 做什么 |
|---|---|
| `extend` | 基于已有音频续写（配合 `continue_at` 指定从第几秒接） |
| `upload_extend` | 续写你上传的音频 |
| `concat` | 拼接音频片段 |

**编辑与增强**

| `type` | 做什么 |
|---|---|
| `remaster` | 增强音质（母带重制） |
| `mashup` | 混合多首歌曲（走 `mashup_audio_ids`） |
| `replace_section` | 替换指定时间段（`replace_section_start` / `_end`） |
| `underpainting` | 为**人声**添加伴奏 |
| `overpainting` | 为**伴奏**添加人声 |
| `samples` | 在指定时间段添加采样 |

**分轨**

| `type` | 做什么 |
|---|---|
| `stems` | 分离**人声和伴奏**两轨 |
| `all_stems` | 分离**人声、鼓、贝斯、其他乐器**四轨 |

---

## 四、13 个接口一览

| 接口 | 名称 | 模式 |
|---|---|---|
| `create` | 创建音乐任务 | 异步 |
| `query` | 查询音乐任务 | 同步 |
| `lyrics` | 生成歌词 | 同步 |
| `style` | 优化音乐风格 | 同步 |
| `mashup_lyrics` | 歌词混合 | 同步 |
| `voice_clone` | 声音克隆 | 同步 |
| `persona` | 创建歌手风格 | 同步 |
| `upload_audio` | 上传参考音频 | 同步 |
| `wav` | 导出 WAV | 异步 |
| `mp4` | 导出 MP4 | 同步 |
| `midi` | 导出 MIDI | 异步 |
| `vox` | 人声处理 | 异步 |
| `timing` | 歌词时间轴 | 同步 |

逐接口的完整参数表见 [`references/`](references/)。

---

## 五、⚠️ 用之前：先拿一个 Key，否则跑不起来

**本 Skill 不内嵌任何密钥，也不代付费用。** 必须有一个 `api.a7w.cn` 的 API Key。

### 第一步：注册并创建 Key

1. 打开 **[算力集市 api.a7w.cn](https://api.a7w.cn/)** 注册（新用户有赠送点数，可以先白跑几条试试）
2. 在控制台创建一个 API Key，形如 `sk-xxxxxxxx...`
3. **完整复制保存** —— 多数平台只在创建时显示一次

### 第二步：把 Key 填进你正在用的地方

| 你在哪用 | 怎么填 |
|---|---|
| **AI 工具 / Agent 平台**（Kimi、扣子、SkillHub 客户端等） | 平台的**环境变量 / 凭证管理 / 插件配置**里加：`A7W_API_KEY` = `sk-你的key` |
| **本机命令行** | `export A7W_API_KEY=sk-你的key`（Windows 用 `$env:A7W_API_KEY="..."`） |
| **只想跑一次** | 命令里直接带 `--key sk-你的key` |
| **长期本机使用** | `python3 scripts/a7w.py login --key sk-你的key` |

**读取顺序**：`--key` 参数 → 环境变量 `A7W_API_KEY` → `~/.a7w/config.json`

不用这个 Key 也完全没关系——**换任何一家的音乐 API，成本都不会是 0.65 元一首。**

---

## 六、怎么调用

### 零安装用法（推荐先看这个）

本 Skill 自带一个只用 Python 标准库的客户端，**不需要装任何第三方包**：

```bash
# 1. 配置你自己的 API Key（只需一次）
export A7W_API_KEY=sk-你的key

# 2. 看这个插件的接口与参数
python3 scripts/a7w.py schema music_generation

# 3. 生成一首歌（异步任务，客户端会自动轮询到结束）
python3 scripts/a7w.py call music_generation create \
  --body '{"type":"generate","prompt":"一首轻快的城市清晨民谣，木吉他，男声","custom":false}'
```

### 直接 curl

```bash
# 提交生成任务
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/create" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"generate","prompt":"一首轻快的城市清晨民谣，木吉他，男声","custom":false}'

# 拿返回的 task_id 查结果
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/query" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_id":"<上一步返回的 task_id>"}'
```

### 同步 vs 异步

| 模式 | 接口 | 怎么处理 |
|---|---|---|
| **同步** | `lyrics` `style` `voice_clone` `persona` `upload_audio` `mp4` `timing` `query` | 直接返回结果 |
| **异步** | `create` `wav` `midi` `vox` | 返回 `task_id`，轮询 `query` 到完成 |

`a7w.py call` **默认自动轮询到结束**；加 `--no-wait` 只提交不等。

---

## 七、从想法到成品：完整一条流水线

**目标：一首有词、有曲、无损、带字幕时间轴的歌。**

```bash
KEY=sk-你的key
API=https://api.a7w.cn/api/v1/apps/music_generation

# ① 写词（0.12 元）—— 也可以自己写，跳过这步
curl -sS -X POST "$API/lyrics" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"写一首关于凌晨加班后骑车回家的城市民谣，副歌要有希望感"}'

# ② 把风格描述优化得更专业（0.14 元）—— 可选，但对效果提升明显
curl -sS -X POST "$API/style" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"城市民谣，木吉他，温暖男声，慢速"}'

# ③ 生成（0.65 元）—— custom=true 时用你给的词和风格
curl -sS -X POST "$API/create" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type":"generate",
    "custom":true,
    "title":"凌晨两点的环路",
    "lyric":"<第①步的歌词>",
    "style":"<第②步优化后的风格>",
    "vocal_gender":"m",
    "weirdness":0.3,
    "style_influence":0.7,
    "style_negative":"电子, 说唱"
  }'
# → 记下返回的 task_id

# ④ 查结果（免费）
curl -sS -X POST "$API/query" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" -d '{"task_id":"<task_id>"}'

# ⑤ 导出无损 WAV（0.14 元）
curl -sS -X POST "$API/wav" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" -d '{"audio_id":"<结果里的 audio_id>"}'

# ⑥ 拿歌词时间轴做字幕（免费）
curl -sS -X POST "$API/timing" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" -d '{"audio_id":"<audio_id>"}'
```

**想让 AI 用你自己的音色唱：**

```bash
# 克隆音色（0.20 元，只需做一次，之后可复用）
# audio_url 要公网可访问的 MP3/WAV，至少 10 秒、单人清晰人声、尽量无背景噪音
curl -sS -X POST "$API/voice_clone" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_url":"https://你的存储/我的清唱.mp3","name":"我的声音"}'
# → 拿到 persona_id / 声音风格 ID，之后在 create 里带上 persona_id
```

**想拿现成伴奏练唱 / 二次创作：**

```bash
# 分离人声与伴奏（0.65 元）
curl -sS -X POST "$API/create" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"stems","audio_id":"<已有音频的 audio_id>"}'

# 四轨全分（人声 / 鼓 / 贝斯 / 其他）
curl -sS -X POST "$API/create" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"all_stems","audio_id":"<audio_id>"}'
```

---

## 八、常见坑

| 坑 | 表现 | 怎么避 |
|---|---|---|
| **拿 `code == 0` 判断成功** | 明明成功了却判成失败 | **这个平台的成功码是 `1`**，不是 `0`。返回形如 `{"code":1,"msg":"success","data":{...}}` |
| **`custom` 传了字符串 `"true"`** | 行为不可预期 | 平台**兼容** `true/false`、`1/0`、`yes/no`、`on/off` 字符串；但**优先传 JSON boolean**，最稳 |
| **入参给了本地路径** | 报参数错误 | `audio_url` / `audio_urls` 必须是**公网可访问的 URL**，不支持本地路径，也不支持 Base64 |
| **歌词/风格超长被截断** | 结果不对 | 常规模型 `lyric` ≤3000、`style` ≤200；高质量模型才算 5000 / 1000。**先确认你用的是哪个档** |
| **`custom:true` 却没给 `lyric`** | 以为会报错，其实会走 `lyric_prompt` | 想完全自己控制就同时给 `lyric`；只给主题就交给 `lyric_prompt` |
| **`extend` 忘了 `continue_at`** | 从头又生成一遍 | 续写要指定从第几秒接，例如 `213.5` = 3 分 33.5 秒 |
| **`inspo` 参考音频数量不对** | 报错 | `audio_urls` 要求 **1~4 个**公网地址 |
| **`mashup` 忘了 `mashup_audio_ids`** | 报错 | 混音类型必须填这个 |
| **重复提交异步任务** | 扣两次钱 | 提交后先记下 `task_id`，用 `query`（免费）确认状态 |
| **以为单价统一** | 预算算不准 | 13 个接口**每个价格都不同**，还有租户价与标准价的差别 |
| **长任务先超时** | 客户端超时，服务端其实已完成 | 加长超时，或 `--no-wait` 只提交、之后手动 `query` |
| **克隆音色用了带 BGM 的音频** | 音色不干净 | 至少 10 秒、单人、清晰、无背景噪音/音乐 |

---

## 九、权限与用途说明

| 能力 | 是否申请 | 用途 |
|---|---|---|
| 网络访问 | **申请** | 调用 `api.a7w.cn` 的音乐接口（本 Skill 唯一的联网行为） |
| 读取文件 | 仅读取用户指定的输入文件 | 少数支持上传的接口用作入参 |
| 写入文件 | 仅在传入 `--out` 时 | 保存接口返回的 JSON 或下载成片 |
| 子进程 / 后台常驻 | 不申请 | 只有 curl / python 一次性调用 |
| 凭证 | 读取**使用者自己**提供的 API Key | 从 `~/.a7w/config.json` 或环境变量读取 |

**不内嵌任何密钥。** 请求只发往 `api.a7w.cn`，不发送到其他任何地址。

## 十、能力边界

- **不提供 API Key**：Key 必须由使用者自己获取
- **不代付费用**：调用消耗的是使用者自己账号的点数
- **不保证可用性**：接口由平台弹性调度，可用性、限流与计费以站内为准
- **不替代版权审查**：生成内容的使用与合规责任由使用者承担。**做 AI 翻唱、续写、分轨时，请确认你对原始音频有相应权利**
- **不做声音仿冒**：克隆他人音色用于冒充、诈骗或误导，属于违法用途

## 参考文件

| 文件 | 用途 |
|---|---|
| `references/做歌指南.md` | 从零到一首成品歌的完整流程、两种模式怎么选、prompt 怎么写 |
| `references/api-create.md` | `create` 的 **17 种操作类型**与全部参数详解 |
| `references/api-lyrics.md` | `lyrics` / `style` / `mashup_lyrics` / `timing` |
| `references/api-voice.md` | `voice_clone` / `persona` / `upload_audio` |
| `references/api-export.md` | `wav` / `mp4` / `midi` / `vox` / `query` |
| `references/getting-started.md` | 注册、充值、获取与配置 API Key |
| `references/通用说明.md` | 权限表、异步任务机制、常见错误码、计费口径 |
| `scripts/a7w.py` | 通用零依赖客户端（库 + 命令行，只用 Python 标准库） |

---

## 联系我们

- **技术微信：9872659** —— 加好友时说一下是从哪个 Skill 找过来的，直接给你配套的 API Key 与能跑的示例。
- **要算力 / 要 API Key**：[算力集市 · 注册领 API Key](https://api.a7w.cn/) —— 一个 Key 调用全部 AI 算力，注册、充值、创建 Key 都在这里。
- **更多 AI 插件与接口**：[AI 插件市场](https://aigc.a7w.cn/)。

---

## 相关链接

| 链接 | 地址 | 说明 |
|---|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn | 一个 Key 调用全部 AI 算力；注册、充值、创建 Key 都在这 |
| [AI 插件市场](https://aigc.a7w.cn/) | aigc.a7w.cn | 浏览全部 AI 插件与接口说明 |
| [视频超清 · 在线批量超分](https://vr.a7w.cn/) | vr.a7w.cn | 网页版视频超分，批量处理，最高 4K |
| [三剪客 · 一句话批量出片](https://ks.a7w.cn/) | ks.a7w.cn | 短剧二创 / 影视解说 / 矩阵号批量混剪桌面客户端 |
| [0人公司 · AI Agent 平台](https://a7w.cn/) | a7w.cn | 主站，了解整套 AI Agent 生态 |
