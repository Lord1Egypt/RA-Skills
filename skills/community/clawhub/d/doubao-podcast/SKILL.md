---
name: doubao-podcast
description: |
  Use when calling Doubao/ByteDance podcast TTS API to generate audio, parsing WebSocket binary frames, handling streaming audio chunks, extracting audio_url from PodcastEnd, troubleshooting podcast generation timeout or stuck issues, or designing podcast playback architecture (streaming vs non-streaming).
  Also use when: integrating podcast generation into a browser-based app (browser WebSocket cannot set custom headers), designing content caching to avoid redundant generation, or extracting article metadata for podcast titles.
  Trigger even without explicit mention of "Doubao" — any podcast TTS, ByteDance speech synthesis, or podcast generation task should use this skill.
---

# 豆包播客 TTS API 集成指南

基于 7 篇微信长文 POC + 线上生产环境的实战经验。覆盖从建连到拿到 mp3 的全流程，以及 11 条踩坑记录。

## 1. 接口概览

| 项 | 值 |
|----|-----|
| 协议 | WebSocket 二进制协议 v3 |
| 地址 | `wss://openspeech.bytedance.com/api/v3/sami/podcasttts` |
| 鉴权 | 4 个 Header：`X-Api-App-Id`、`X-Api-Access-Key`、`X-Api-Resource-Id`、`X-Api-App-Key` |
| Resource ID | `volc.service_type.10050` |
| 输出 | MP3, 96kbps, 24kHz mono（固定） |

## 2. 二进制协议

豆包使用自定义二进制帧，**不是**标准 JSON WebSocket。

### 帧头（固定 4 字节）

```
[0x11, 0x14, 0x10, 0x00]
```

- 第 2 字节高 4 位 = message_type（0xF = 错误帧）
- 第 2 字节低 4 位 = flags（0x04 = 含 session_id）
- 第 3 字节高 4 位 = serialization（1=JSON, 0=binary audio）

### 两种帧格式

```
Pre-connection:  header(4) + event_type(4, big-endian) + payload_size(4) + payload
Post-connection: header(4) + event_type(4) + sid_len(4) + session_id + payload_size(4) + payload
```

### 构造/解析代码

Python 版本见 `scripts/generate_podcast.py`。Node.js 版本：

```javascript
const HEADER = Buffer.from([0x11, 0x14, 0x10, 0x00]);

function preFrame(event, payload) {
  const p = Buffer.from(JSON.stringify(payload));
  const e = Buffer.alloc(4); e.writeUInt32BE(event);
  const l = Buffer.alloc(4); l.writeUInt32BE(p.length);
  return Buffer.concat([HEADER, e, l, p]);
}

function postFrame(event, sid, payload) {
  const sb = Buffer.from(sid);
  const p = Buffer.from(JSON.stringify(payload));
  const e = Buffer.alloc(4); e.writeUInt32BE(event);
  const sl = Buffer.alloc(4); sl.writeUInt32BE(sb.length);
  const pl = Buffer.alloc(4); pl.writeUInt32BE(p.length);
  return Buffer.concat([HEADER, e, sl, sb, pl, p]);
}

function parseEvent(data) {
  const buf = Buffer.from(data);
  if (buf.length < 8) return { eventType: null, payload: {} };
  const mt = (buf[1] >> 4) & 0xF;
  const fl = buf[1] & 0xF;
  const ser = (buf[2] >> 4) & 0xF;
  if (mt === 0xF) { /* 错误帧 */ return { eventType: -1, payload: {} }; }
  const evt = buf.readUInt32BE(4);
  let off = 8, payload = {};
  if (fl & 0x04) {
    const sl = buf.readUInt32BE(off); off += 4 + sl;  // 跳过 session_id
    const pl = buf.readUInt32BE(off); off += 4;
    if (pl > 0 && ser === 1) try { payload = JSON.parse(buf.slice(off, off + pl).toString()); } catch {}
  }
  return { eventType: evt, payload };
}
```

## 3. 握手流程与事件表

```
客户端                                豆包 API
  │── StartConnection(event=1) ────→│
  │←── ConnectionStarted(event=50) ─│  ← session_id 在二进制帧中
  │── StartSession(event=100) ─────→│  ← 携带播客参数
  │←── SessionStarted(event=150) ───│
  │  ┌── 流式循环 ──────────────────┐
  │←─┤ 360: RoundStart (JSON)      │  ← 文案文本（第1轮为空！见坑10）
  │←─┤ 361: RoundResp (binary)     │  ← 音频块 ~4.6KB/chunk
  │←─┤ 362: RoundEnd (JSON)        │
  │  └─────────────────────────────┘
  │←── 363: PodcastEnd (JSON) ─────│  ← audio_url（⚠️ duration_sec 可能为 0，见坑9）
  │←── 152: SessionFinished ───────│  ← ⚠️ 经常不来，见坑2
  │── FinishConnection(event=2) ──→│
```

### 事件速查

| event | 名称 | payload | 关键字段 |
|-------|------|---------|---------|
| 1/2 | Start/FinishConnection | `{}` | — |
| 50 | ConnectionStarted | 二进制 | session_id 在帧中提取 |
| 100 | StartSession | JSON | 播客参数 |
| 360 | RoundStart | JSON | `text`（第 1 轮为空） |
| 361 | RoundResp | binary | 音频块 |
| 363 | PodcastEnd | JSON | `meta_info.audio_url` |

### 提取 session_id（ConnectionStarted 帧）

```javascript
const buf = Buffer.from(data);
let off = 8;
const sidLen = buf.readUInt32BE(off); off += 4;
const sessionId = buf.slice(off, off + sidLen).toString();
```

## 4. 两种输入模式

### input_url（URL 文章）

```javascript
{
  input_info: { input_url: "https://...", return_audio_url: true },  // ⚠️ url 在 input_info 内
  use_head_music: true, use_tail_music: false,
  audio_config: { format: "mp3", sample_rate: 24000, speech_rate: 0 },
  speaker_info: { random_order: true, speakers: ["zh_male_dayixiansheng_v2_saturn_bigtts", "zh_female_mizaitongxue_v2_saturn_bigtts"] }
}
```

### input_text（短文本 < 200 字）

```javascript
{
  input_text: "文本内容...",  // ⚠️ text 在顶层，不是 input_info
  audio_config: { ... },
  speaker_info: { ... }
}
```

## 5. 实战踩坑记录（11 条）

### 坑 1：input_url vs input_text 参数位置

```
❌ {"input_url": "https://..."}                  → 顶层没这字段，静默失败
✅ {"input_info": {"input_url": "https://..."}}  → URL 模式正确用法
✅ {"input_text": "你好世界"}                     → 短文本模式正确用法
```

搞反了不会报错，只会得到空结果。

### 坑 2：PodcastEnd 之后不要等 SessionFinished

SessionFinished(152) **经常不来或等 10 分钟+**。PodcastEnd(363) 拿到 audio_url 后**立即 break**。

```javascript
if (eventType === 363) {
  const url = payload.meta_info?.audio_url || '';
  ws.close();  // 立即关闭！
  resolve({ audioUrl: url });
}
```

不加 break，5 分钟播客可能跑 15 分钟。这是最致命的坑。

### 坑 3：超时设 900s

| 文章长度 | 播客时长 | 生成耗时 |
|---------|---------|---------|
| ~2000字 | ~5 min | ~2.5 min |
| ~5000字 | ~10 min | ~4 min |
| ~25000字 | ~30 min | ~10 min |

统一设 `TIMEOUT = 900`（15 分钟）。

### 坑 4：WebSocket 连接参数

Python: `ping_timeout=120`，不设的话长文生成时会心跳超时断开。
Node.js: `ws` 库默认无 ping，不需要额外设置。

### 坑 5：连接断开但已有音频块

音频块是完整 MP3 片段，直接拼接就是可播放文件。断连时不要丢弃已收到的块。

### 坑 6：audio_url 24 小时过期

CDN URL 签名过期后返回 403。**生成完成后立即下载 mp3 到自己的存储**。

### 坑 7：Python nohup 输出缓冲

后台运行加 `python -u`（unbuffered）才能看到实时日志。

### 坑 8：浏览器 WebSocket 不支持自定义 Header ⭐

浏览器 `new WebSocket(url)` **无法设置 HTTP Header**。豆包需要 4 个鉴权 Header → **必须走服务端代理**。

推荐架构：

```
浏览器 ── POST /api/podcast ──→ 服务端 ── WSS + Header ──→ 豆包
       ← SSE 流式进度 ────────         ← 二进制帧 ──────
```

服务端用 Node.js `ws` 库（支持自定义 Header）连接豆包，通过 SSE（Server-Sent Events）把进度推给浏览器。凭证存在服务端，不暴露给前端。

### 坑 9：duration_sec 经常返回 0 ⭐

PodcastEnd 的 `meta_info.duration_sec` **实测经常为 0 或不返回**。

备用方案：根据音频大小估算（96kbps = 12KB/s）：

```javascript
const durationSec = meta.duration_sec || Math.round(totalAudioBytes / 12000);
```

### 坑 10：RoundStart 第一轮文案为空 ⭐

第 1 轮是片头音乐，`text` 字段为空字符串。**第 2 轮开始**才有实际文案内容。

如果需要从文案中提取标题/主题，从 Round 2+ 的文案中取。

### 坑 11：微信文章标题无法从服务端抓取 ⭐

从中国云服务器 `fetch` 微信文章会返回"环境异常"页面（反爬）。标题提取备用方案：

1. 优先：`fetch` 文章页面提取 `<title>` 或 `og:title`（非微信 URL 有效）
2. 备用：从 RoundStart 第 2 轮文案提取主题（去口语化前缀如"今天我们聊的是"）
3. 兜底：使用 fallback 文本

## 6. 内容存储与去重（生产架构）

豆包 token 昂贵，必须避免重复生成。推荐架构：

```
POST /generate {url}
  → 查 store：相同 url 已有？
    → YES：直接返回缓存（0 token）
    → NO：调豆包生成 → 下载 mp3 到本地 → 写入 store → 返回
```

Store 数据模型：
```json
{ "id": "gen_xxx", "source_url": "https://...", "title": "...", "audio_file": "gen_xxx.mp3", "duration_sec": 682 }
```

音频下载到本地后不再依赖豆包 CDN（24h 过期）。

## 7. 性能基线

| 指标 | 值 |
|------|-----|
| 生成速度 | 2.7× 实时（1 分钟播客 ≈ 22s 生成） |
| 首 token | avg 6s |
| Token 消耗 | ~800 字/分钟播客，~3000 token/分钟 |
| 音频块 | ~4.6KB/chunk |
| 总测试量 | 7 篇 + 线上多篇，全部成功 |

## 8. 错误处理

| 场景 | 表现 | 处理 |
|------|------|------|
| 建连失败 | event=-1 | 检查凭证，重试 |
| 内容过滤 | 错误码 `50302102` | 提示不支持，不重试 |
| 心跳超时 | 静默断开 | Python: `ping_timeout=120` |
| audio_url 过期 | CDN 403 | 用本地存储的 mp3 |

## 9. 参考实现

| 文件 | 语言 | 说明 |
|------|------|------|
| `scripts/generate_podcast.py` | Python | 批量生成 + CLI，POC 验证用 |
| 项目 `server/podcast-api.js` | Node.js | 生产环境：HTTP API + SSE + 内容存储 |
