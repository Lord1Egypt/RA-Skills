# AI 音乐工坊

**一句话，一首歌。** AI 写词、作曲、编曲、演唱，一首 0.65 元。

---

## 内容

```
ai-music-studio/
├── SKILL.md                        主入口：计费、两种模式、17 种操作、常见坑
├── README.md                       本文件
├── LICENSE.md                      MIT
├── references/
│   ├── 做歌指南.md                  从一句话到成品：流程图、prompt 模板、省钱技巧
│   ├── api-create.md               create 的 17 种操作类型与全部参数
│   ├── api-lyrics.md               lyrics / style / mashup_lyrics / timing
│   ├── api-voice.md                voice_clone / persona / upload_audio
│   ├── api-export.md               wav / mp4 / midi / vox / query
│   ├── getting-started.md          注册、充值、获取与配置 API Key
│   └── 通用说明.md                  权限表、异步机制、错误码、计费口径
└── scripts/
    └── a7w.py                      零依赖客户端（库 + 命令行，只用 Python 标准库）
```

---

## 这个插件能做什么

`api.a7w.cn` 插件 **`music_generation`**，共 **13 个接口**。

**从零创作**

| 能力 | 怎么做 |
|---|---|
| 一句话生成一首歌 | `create` + `type: "generate"` |
| 按主题自动写词 | `lyrics` 或 `lyric_prompt` |
| 把大白话风格变专业 | `style` |
| 给参考音频生成 | `create` + `type: "inspo"`（1~4 段） |
| 纯伴奏 / 无人声 BGM | `create` + `instrumental: true` |
| 指定歌手风格 | `create` + `type: "artist_consistency"` |

**用你的声音唱**

| 能力 | 怎么做 |
|---|---|
| 克隆你的音色 | `voice_clone`（一次 0.20 元，可反复用） |
| 从已有作品提取人设 | `persona` |
| 把手上的音频变成素材 | `upload_audio` |

**改造已有歌曲**

| 能力 | 怎么做 |
|---|---|
| AI 翻唱 | `type: "cover"` / `"upload_cover"` |
| 续写 | `type: "extend"` + `continue_at` |
| 拼接 | `type: "concat"` |
| 混音 | `type: "mashup"` |
| 局部替换 | `type: "replace_section"` |
| 加人声 / 加伴奏 | `type: "overpainting"` / `"underpainting"` |
| 母带重制 | `type: "remaster"` |
| 分轨（2 轨 / 4 轨） | `type: "stems"` / `"all_stems"` |

**导出交付**

| 能力 | 怎么做 |
|---|---|
| 无损音频 | `wav` |
| 带画面视频 | `mp4` |
| 可再编曲的 MIDI | `midi` |
| 歌词时间轴（做字幕） | `timing`（**免费**） |

---

## 快速开始

```bash
# 1. 配置你自己的 API Key（只需一次）
export A7W_API_KEY=sk-你的key
# 或者：python3 scripts/a7w.py login --key sk-你的key

# 2. 看这个插件的接口与参数
python3 scripts/a7w.py schema music_generation

# 3. 生成一首歌（异步任务自动轮询到结束）
python3 scripts/a7w.py call music_generation create \
  --body '{"type":"generate","custom":false,"prompt":"一首轻快的城市清晨民谣，木吉他，温暖男声"}'
```

或者直接用 curl：

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/music_generation/create" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"generate","custom":false,"prompt":"一首轻快的城市清晨民谣，木吉他，温暖男声"}'
```

---

## 用之前先拿 Key

**本包不内嵌任何密钥，也不代付费用。**

1. 打开 **[算力集市 api.a7w.cn](https://api.a7w.cn/)** 注册（新用户有赠送点数）
2. 控制台创建一个 API Key，形如 `sk-xxxxxxxx...`
3. 填进环境变量 `A7W_API_KEY`，或在平台的凭证管理里配置

**读取顺序**：`--key` 参数 → `A7W_API_KEY` → `~/.a7w/config.json`

---

## 计费

按**点数**计费，**1 元 = 100 点**。租户实际结算价：

| 典型做法 | 走了哪些接口 | 总价 |
|---|---|---|
| 最快出一首 | `create` | **0.65 元** |
| 词 + 曲 + 无损全包 | `lyrics` + `create` + `wav` | **0.91 元** |
| 用自己音色唱 | 上面 + `voice_clone`（一次，可复用） | **1.11 元** |

> `lyrics` 返回的 `tags` 里**自带专业编曲描述**，可以直接当 `style` 用，省掉单独调 `style` 的 0.14 元。

- 异步任务**提交时预冻结点数**，完成后按实际用量结算
- **`query` 和 `timing` 免费**，可以放心轮询
- 平台同时给出标准价与租户实际结算价，**以实际扣费为准**
  （返回里的 `data.usage.points_cost` 就是本次真实扣费）
- **不要重复提交**同一个任务 —— 每次提交都会扣 65 点

---

## 这个包不包含什么

- **不提供 API Key** —— 必须由使用者自己在 api.a7w.cn 获取
- **不代付费用** —— 消耗的是使用者自己账号的点数
- **不保证可用性** —— 接口由平台弹性调度，可用性、限流与计费以站内为准
- **不替代版权审查** —— 生成内容的使用与合规责任由使用者承担；
  做 AI 翻唱、续写、分轨时请确认你对原始音频有相应权利
- **不做声音仿冒** —— 克隆他人音色用于冒充、诈骗或误导属于违法用途

---

## 联系我们

- **技术微信：9872659** —— 加好友时说一下是从哪个 Skill 找过来的，直接给你配套的 API Key 与能跑的示例。
- **要算力 / 要 API Key**：[算力集市 · 注册领 API Key](https://api.a7w.cn/)

---

## 相关链接

| 链接 | 地址 | 说明 |
|---|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn | 一个 Key 调用全部 AI 算力 |
| [AI 插件市场](https://aigc.a7w.cn/) | aigc.a7w.cn | 浏览全部 AI 插件与接口说明 |
