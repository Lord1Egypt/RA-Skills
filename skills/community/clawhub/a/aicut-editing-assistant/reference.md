# 地鼠AI剪辑 智能剪辑参考文档

本文件包含实战经验沉淀、防卡顿规则和给官方的建议。SKILL.md 只保留核心操作规则，详细参考内容在此展开。

## 1. PY022 官方桥接实战总结

### 1.1 验证结论

```text
window.aicutAI / window.openCutAI 可用
getProjectSnapshot() 可读真实项目状态
importMedia() 可导入本地音频
applyTimeline() 可真实创建 63s 时间线
importSrt() 可导入字幕/标题轨
player.seek/play/pause 可做网页内预览
validateProject() 可做导出前校验
```

结论：以后 地鼠AI剪辑 自动剪辑优先走官方桥接，不再把 UI 拖拽或 IndexedDB 写入当主链路。

### 1.2 PY022 成片结果

```text
1. 读取已上传素材并复用浏览器媒体库 mediaId
2. 导入用户确认可用的 v4 口播音频
3. 用 applyTimeline 铺出 63 秒主时间线
4. 关闭视频原声
5. 导入字幕/标题轨
6. 网页预览并截图检查
7. 成功导出 mp4
```

导出文件验证：

```text
文件时长约 63.09 秒
画面尺寸 1440x1080
音频轨为 AAC stereo 44100Hz
```

### 1.3 字幕实战经验

PY022 初次实战发现：

```text
地鼠AI剪辑 旧版 importSrt 的 style/字号单位不稳定
fontSize 30/42 容易过大遮挡画面
fontSize 10 勉强可用，但仍更像标题轨而不是正式字幕
```

官方已按反馈补强 douyinSafe 预设，后续直接用 `{ preset: "douyinSafe" }`。

douyinSafe 预设完整参数（源码 `getCapabilities()`）：

```text
fontSize: 4.2, color: "#ffffff", strokeColor: "#000000", strokeWidth: 0.55
fontWeight: "bold", textAlign: "center", lineHeight: 1.18
maxCharsPerLine: 18, maxLines: 2
placement: verticalAlign "bottom", marginLeftRatio 0.08, marginRightRatio 0.08, marginVerticalRatio 0.085
```

### 1.3.1 成片字幕返工与 8-35 秒错位处理

触发条件：

```text
用户反馈“字幕 8-35 秒对不上”
用户反馈“某一段字幕不跟口播”
用户反馈“字幕越往后越偏”
用户反馈“审片版前面还行，后面字幕慢了/快了”
```

处理原则：

```text
不要手调旧字幕。
不要沿用旧 SRT/旧 captions 的 start/end。
不要用素材原始时间轴替代最终成片时间轴。
最终导出成片的音频，才是字幕返工的唯一时间基准。
```

标准流程：

```text
1. 导出当前审片版/最终版视频。
2. 从导出视频抽取最终成片音频。
3. 用本地 Whisper 对这条最终成片音频重新转写，生成 JSON/SRT/VTT。
4. 把确认过的字幕文本整理成 captions；旧字幕只可作为文本草稿，不可复用时间码。
5. 调用 local_subtitle_align / aicut local subtitle-align，输出 aligned.srt 和 aligned.ass。
6. AICut 项目内重新导入 aligned.srt；本地 ffmpeg 兜底导出时烧录 aligned.ass。
7. 重新导出成片并抽查 8、12、16、20、24、28、32、35 秒字幕是否贴住口播。
```

CLI 示例：

```bash
aicut local subtitle-align @/absolute/path/to/subtitle-align-plan.json \
  --transcript /absolute/path/to/final-audio-whisper.json \
  --srt-output /absolute/path/to/aligned.srt \
  --ass-output /absolute/path/to/aligned.ass \
  --report /absolute/path/to/subtitle-align-report.md \
  --check-times 8,12,16,20,24,28,32,35
```

计划模板：

```text
apps/aicut-cli/examples/local-subtitle-align-plan.json
```

计划字段要点：

```json
{
  "title": "地鼠AI剪辑字幕返工",
  "transcript": "/absolute/path/to/final-audio-whisper.json",
  "srtOutput": "/absolute/path/to/aligned.srt",
  "assOutput": "/absolute/path/to/aligned.ass",
  "reportPath": "/absolute/path/to/subtitle-align-report.md",
  "checkTimes": [8, 12, 16, 20, 24, 28, 32, 35],
  "captions": [
    { "text": "确认后的字幕文本", "transcriptIndex": 0 },
    { "text": "合并多段转写时这样写", "transcriptStartIndex": 1, "transcriptEndIndex": 2 }
  ]
}
```

MCP 工具：

```text
tool: local_subtitle_align
input: { "plan": { "transcript": "...final-audio-whisper.json", "captions": [{ "text": "...", "transcriptIndex": 0 }] } }
```

验收口径：

```text
aligned.srt 用于 AICut 字幕轨导入。
aligned.ass 用于本地 ffmpeg 兜底流程烧录字幕。
subtitle-align-report.md 必须记录抽查秒点和附近字幕。
返工后必须重新导出；只生成新字幕文件不算完成。
```

### 1.4 官方补强后的新能力

```text
importMedia 支持 File / Blob / base64 / url / localPath / tauriPath
importMedia 返回 imported[] / failed[] / idMap，支持 onProgress/signal
importMedia 两种调用：数组简写 或 {media, options} 对象
player 支持 currentTime / isPlaying / timeupdate / ended / seek / statechange
player.on({event, listener}) 统一事件注册
validateProject 可校验主轨、音频轨、字幕、缺失媒体、视频原声关闭状态
音量语义明确为 dB：volumeDb: 0 = 正常，muted: true = 静音，BGM 建议 -18
createProject / listProjects / getCurrentProject / openProject 项目生命周期
localMedia 桌面端本地文件桥接（地鼠AI剪辑桌面端）
bridge.on({event, listener}) 项目事件：ready / projectChanged / projectLoaded
getCapabilities() 返回运行时能力（桌面端信息、音量范围、导入建议、字幕预设）
applyProject 支持 captions 直接输入 + srtText + subtitleStyle 统一样式
exportProject 支持 format: mp4|webm, quality: low|medium|high|very_high, fps?, includeAudio?
```

### 1.5 DJI 原素材与 H.264 代理素材规则

```text
DJI 原素材 HEVC 10-bit 在 Chromium 里可能不能预览。
真实工作流建议使用 H.264 代理素材做网页预览。

如果素材为 DJI / HEVC / 10-bit / Chromium 预览异常：
先生成 H.264 代理素材用于网页预览和 地鼠AI剪辑 时间线。
正式导出如 地鼠AI剪辑 支持原素材可再替换；否则使用高质量 H.264 代理。
代理素材要关闭原声或确保 muteAllVideoSourceAudio 生效。
```

---

## 2. OpenClaw Jobs 体系详解

### 2.1 启用条件

```text
NEXT_PUBLIC_AICUT_AI_JOBS_ENABLED=true
```

### 2.2 连接方式

WebSocket 连接 `/api/ai-editing/ws?clientId=xxx`，连接成功收到 `{type: "ready", clientId}`。

### 2.3 Job 状态流转

```text
pending → claimed → planning → applied → completed
                                    ↘ failed（任一步失败）
```

### 2.4 服务端 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/ai-editing/jobs` | GET | 列出 Jobs（?clientId=） |
| `/api/ai-editing/jobs` | POST | 创建 Job |
| `/api/ai-editing/jobs/{id}` | GET | 获取 Job |
| `/api/ai-editing/jobs/{id}` | PATCH | 更新 Job 状态 |
| `/api/ai-editing/jobs/{id}/summaries` | POST | 提交素材摘要，返回计划 |
| `/api/ai-editing/ws` | GET (WS) | WebSocket 连接 |

### 2.5 Job 类型定义

```ts
AiEditingJobCreateInput: {clientId, title, goal, script?, skill?, assetHints?}
AiEditingJobUpdateInput: {status, message?, projectId?, plan?, error?}
AiEditingJob: {id, clientId, title, goal, script, skill, assetHints, assetSummaries, status, message?, projectId?, plan?, error?, createdAt, updatedAt}
```

### 2.6 素材摘要

```ts
AiEditingAssetSummary: {id, name, type: "image"|"video"|"audio", durationSeconds?, transcript?, tags?, notes?}
```

浏览器端自动从 `editor.media.getAssets()` 构建（过滤 ephemeral 素材，自动添加 type/has-audio/分辨率标签）。

### 2.7 计划结构

```ts
AiEditingPlan: {summary, timeline: AiEditingPlanSegment[], missingAssets, riskReview, manualReview}
AiEditingPlanSegment: {startSeconds, endSeconds, assetId?, assetName?, caption?, visualIntent, audioIntent?, notes?}
```

内置 `buildInitialEditingPlan`：取前 8 个非音频素材，首段 3s、后续 5s 封顶，自动添加 riskReview 和 manualReview。

### 2.8 计划应用

`applyAiEditingPlanToTimeline`：匹配 assetId 或 assetName，插入视频/图片到主轨，插入字幕到文字轨，跳过无效段落。

---

## 3. ClientEditingSkill 框架详解

### 3.1 数据模型（Rust editing_skills crate）

```text
ClientEditingSkill
├── id, clientName, displayName, status(Draft/Active/Archived)
├── version: {major, minor, patch}  (默认 0.1.0)
├── outputTargets: OpenClawTool | DishuAiCutTimeline | RenderedVideo[]
├── narrative: NarrativeStyle
│   ├── summary: 叙事定位
│   ├── openingHooks: 开头钩子[]
│   ├── storyBeats: 故事节点[]
│   └── bannedMoves: 禁止剪法[]
├── pacingRules: PacingRule[]
│   └── {name, description, minSeconds, maxSeconds}
├── subtitle: SubtitleStyle
│   └── {fontFamily, primaryColor, strokeColor, maxCharsPerLine, emphasisStyle}
├── visual: VisualStyle
│   └── {aspectRatio, colorMood, cameraLanguage, preferredShots[], avoidedShots[]}
├── audio: AudioStyle
│   └── {voiceVolume, musicVolume, musicMood, bannedEffects[]}
├── riskRules: RiskRule[]
│   └── {name, description, severity(0-3)}
└── knowledge: EditingKnowledgeBlock[]
    └── {title, content, tags[]}
```

### 3.2 内置模板：documentary_talking_head_template

```text
叙事：真实纪实口播，强调现场感、商业信任和清晰判断
开头钩子：前 2 秒给出冲突/结果/反常识判断
故事节点：现场问题 → 关键判断 → 解决动作 → 结果或复盘
禁止剪法：夸张转场、无根据的成功承诺、纯情绪鸡血包装
节奏规则：
  opening: 0-2s，开头必须快速建立看点
  expectation: 2-5s，补充为什么值得看下去
  first-proof: 5-12s，尽早给出画面证据
字幕：serif-heavy, #FFFFFF/#000000, 18字/行, 关键词加粗
画面：4:3, 暗调纪实, 真实现场+人物口播+项目细节穿插
声音：口播优先, 低音量铺底, 克制纪录片感
风险：隐私(P3), 无法证明的承诺(P3)
知识：风格目标是真实、克制、有现场感
```

### 3.3 Skill 校验与评分

`validate_skill` 校验：
- id/clientName/displayName/narrative.summary/subtitle.fontFamily/visual.aspectRatio 必填
- outputTargets 不能为空（severity 2 = blocking）
- pacingRules 中 maxSeconds > minSeconds（severity 2 = blocking）
- riskRules severity 不超过 3
- pacingRules 为空时 severity 1 警告

`skill_completeness` 评分（满分 17 分）：
- identity: 3 分（id + clientName + displayName）
- narrative: 3 分（summary + openingHooks + storyBeats）
- pacing: 1 分（至少一条规则）
- subtitle: 3 分（fontFamily + primaryColor + maxCharsPerLine > 0）
- visual: 3 分（aspectRatio + cameraLanguage + preferredShots）
- audio: 2 分（voiceVolume + musicMood）
- risk: 1 分（至少一条规则）
- knowledge: 1 分（至少一条知识块）

### 3.4 上下文生成

`build_editing_skill_context` 生成 `EditingSkillContext`：
- title: `{clientName} / {displayName}`
- systemBrief: `你是 {clientName} 的 AI 剪辑助理。输出目标：{target}。必须优先遵守该客户剪辑 Skill，不套用通用模板，不编造素材，不跳过人工终审。`
- styleRules: 叙事定位、画幅、画面语言、色彩、字幕、声音、优先/避免镜头、禁止剪法/声音效果
- timelineRules: 开头钩子、故事节点、节奏规则（含秒数范围）
- riskRules: `[P{severity}] {name}：{description}`
- knowledgeNotes: `{title} [{tags}]：{content}`

### 3.5 计划提示生成

`build_editing_plan_prompt` 生成 `EditingPlanPrompt`：
- context: EditingSkillContext
- userBrief: 项目名 + 目标 + 口播脚本 + 素材清单
- requiredOutputSchema: summary / timeline / missingAssets / riskReview / manualReview
- reviewChecklist: 是否遵守 Skill / 是否编造素材 / 前 2 秒看点 / 字幕规则 / 风险人工终审

---

## 4. 防卡顿与资源保护规则

来源：PY022 实战事故，com.apple.WebKit.WebContent 曾出现 CPU 接近 100%、内存约 3.4GB。

### 4.1 使用守则

```text
1. 不长时间无监控挂着 地鼠AI剪辑 编辑器页面。
2. 优先用官方 Bridge 接口一次性 applyProject/applyTimeline，减少 UI 拖拽和页面重渲染。
3. 大视频素材优先复用浏览器媒体库已有 mediaId，不默认把多个大视频转 base64/Blob 注入页面。
4. 如必须导入本地大文件，分批、小步验证，不一次性塞入大量素材。
5. 网页预览完成或阶段任务结束后，主动关闭/释放 地鼠AI剪辑 标签页，避免后台持续占用。
6. 每次 地鼠AI剪辑 操作前后，如用户反馈电脑卡，立即暂停剪辑操作，先查资源占用。
7. 不再反复 IndexedDB patch + 刷新页面；这会增加 UI 状态异常和 WebKit 卡死风险。
```

### 4.2 资源检查命令

```bash
ps -Ao pid,ppid,%cpu,%mem,rss,comm,args | sort -k3 -nr | head -20
ps -Ao pid,%cpu,%mem,rss,comm,args | egrep 'WebKit|Chrome|opencli|node|ffmpeg|地鼠AI剪辑' | sort -k2 -nr | head -40
```

### 4.3 判断规则

```text
com.apple.WebKit.WebContent 长时间 CPU > 80% 或内存 > 2GB -> 卡死风险高
ffmpeg 高占用 -> 可能在转码/导出，确认是否主动任务
Chrome Helper 高占用 -> 优先确认是否 地鼠AI剪辑 标签页
QwenPaw/OpenClaw WebKit 高占用 -> 可能内嵌浏览器卡死
```

### 4.4 处理规则

```text
1. 先停止继续剪辑/导入/预览
2. 优先关闭 地鼠AI剪辑 标签页或释放 session
3. 如仍卡，向用户说明 PID、CPU、内存，征得明确同意后 kill
4. 禁止未经用户授权直接杀进程
5. 杀掉后复查 top 进程，确认 CPU/内存回落
```

原则：剪辑自动化不能以拖垮用户电脑为代价。宁可慢一点，也不要一次性把网页剪辑器打爆。

---

## 5. 本地媒体路由详解

### 5.1 Web 端 localPath

浏览器端 `localPath` 走 `/api/ai-editing/local-media?path=xxx` 服务端路由：

- 需配置环境变量 `AICUT_LOCAL_MEDIA_ROOTS`（逗号分隔的允许根目录）
- 可选配置 `AICUT_LOCAL_MEDIA_TOKEN`（启用后请求需带 `x-aicut-local-media-token` 头或 `?token=` 参数）
- 支持 Range 请求（206 Partial Content）
- 路径安全：realpath 解析 + 必须在 allowed roots 内
- 不支持 `file://` URL

### 5.2 桌面端 tauriPath

地鼠AI剪辑桌面端 通过 Tauri invoke 调用：

| Tauri 命令 | 说明 |
|------------|------|
| `desktop_info` | 获取桌面端信息（platform, version） |
| `authorize_media_folder` | 授权文件夹访问 |
| `list_media_folder` | 列出文件夹素材 |
| `get_authorized_media_roots` | 获取已授权根目录 |
| `revoke_media_roots` | 撤销所有授权 |
| `read_media_file_base64` | 读取文件为 base64 |

---

## 6. 素材上传过渡期策略

当前稳定入口：用户手动上传，AI 接手后续剪辑。

```text
1. 不能默认 AI 能直接从用户电脑静默读取任意本地文件
2. 不能默认自动上传接口一定稳定可用
3. 当自动化上传不稳定时，优先接受用户手动上传，再由 AI 读取媒体库并继续剪辑
```

推荐工作流：

```text
用户手动上传素材 -> AI 调用 getProjectSnapshot 读取媒体库
-> AI 复用已上传 mediaId -> AI 排时间线 -> AI 导入音频/字幕 -> 预览 -> 导出
```

何时升级自动上传：稳定的本地桥接助手 / MCP/HTTP/WebSocket 通道 / File/Blob 直接注入 / 进度与失败回调 / 不增加卡顿风险。

---

## 7. 给官方的建议优先级

### P0

```text
1. createProject() ✅ 已实现
2. listProjects() / getCurrentProject() / openProject() ✅ 已实现
3. 明确 localPath 适用宿主环境 ✅ 已实现（服务端路由 + 桌面端桥接）
```

### P1

```text
4. ready / projectChanged / projectLoaded 状态事件 ✅ 已实现（bridge.on）
5. 媒体元信息增强（fingerprint 已实现，便于去重与复用）
6. failed[] code 标准化 ✅ 已实现（AicutAiImportErrorCode 枚举）
```

### P2

```text
7. exportProject() 完整文档与状态事件 ✅ 已实现（format/quality/fps/includeAudio）
8. codec / preview 兼容性能力进一步明确（HEVC 10-bit 代理建议已记录）
9. validateProject() schema 继续稳定化 ✅ 已实现（missingMedia + warnings）
```

### P3（新建议）

```text
10. ClientEditingSkill 与 Bridge API 更深层集成（Skill 驱动自动排时间线参数）
11. OpenClaw Jobs 与 ClientEditingSkill 的 Plan 生成链路打通
12. exportProject 进度事件（当前仅 editor.project.getExportState()）
```

### P4（CLI/MCP 相关）— 已实现

```text
13. ✅ CLI 和 MCP 已实现（HTTP API :4891 + MCP WebSocket :4890）
14. ✅ 内嵌 MCP Server 直接操控 Bridge（不再需要 Playwright/Puppeteer 注入）
15. ✅ MCP 已有 project_apply / subtitle_import_srt / project_export 等时间线操控 tool
16. ⬜ MCP 支持资源订阅（resources）：实时项目状态、Job 状态推送（待实现）
```

只在以下情况才整理给官方：

```text
1. 明确影响自动剪辑主链路的接口缺失
2. 需要标准化的 schema / 类型定义
3. 需要导出前校验或性能保护接口
4. DJI/HEVC 代理素材、导出兼容性等真实工作流问题
```

---

## 8. CLI 详细参考

### 8.1 安装

```bash
cd apps/aicut-cli && npm install
# 直接使用
node src/index.js --help
# 或全局链接
npm link
aicut --help
```

### 8.2 命令详解

| 命令 | 说明 |
|------|------|
| `aicut health` | 检查 地鼠AI剪辑 服务是否在线 |
| `aicut jobs list [--clientId <id>]` | 列出所有/指定客户端的 Job |
| `aicut jobs create '<json>'` | 创建 Job，支持 @file.json |
| `aicut jobs get <jobId>` | 查看 Job 详情 |
| `aicut jobs summaries <jobId> '<json>'` | 提交素材摘要，服务端生成计划 |
| `aicut jobs update <jobId> '<json>'` | 更新 Job 状态 |
| `aicut jobs watch [--clientId <id>]` | WebSocket 实时监听 Job |
| `aicut media url <localPath>` | 获取本地媒体 HTTP URL |
| `aicut media fetch <localPath> [out]` | 下载本地媒体文件 |
| `aicut skill validate '<json>'` | 校验 Skill JSON |
| `aicut skill completeness '<json>'` | 计算 Skill 完整度评分 |
| `aicut skill template` | 输出纪实口播 Skill 模板 |

### 8.3 JSON 参数

`jobs create` 的 JSON 格式：

```json
{
  "clientId": "my-project",
  "title": "剪一条获客视频",
  "goal": "建立信任",
  "script": "口播稿内容...",
  "assetHints": [
    { "name": "现场口播.mp4", "type": "video", "description": "主口播" }
  ]
}
```

`jobs summaries` 的 JSON 格式：

```json
[
  { "id": "asset-1", "name": "现场口播.mp4", "type": "video", "durationSeconds": 42, "tags": ["video", "has-audio"] }
]
```

`jobs update` 的 JSON 格式：

```json
{ "status": "completed", "projectId": "my-project", "message": "用户已完成审片" }
```

### 8.4 典型工作流

```bash
# 1. 检查服务
aicut health

# 2. 创建剪辑任务
aicut jobs create '{"clientId":"demo","title":"测试剪辑","goal":"自动粗剪"}'

# 3. 提交素材摘要（假设 jobId = job_xxx）
aicut jobs summaries job_xxx '[{"id":"a1","name":"clip.mp4","type":"video","durationSeconds":30}]'

# 4. 查看生成的计划
aicut jobs get job_xxx

# 5. 实时监听
aicut jobs watch --clientId demo
```

---

## 9. MCP Server 详细参考

### 9.1 安装

```bash
cd apps/aicut-mcp && npm install
```

### 9.2 配置

地鼠AI剪辑桌面端 内嵌了 MCP WebSocket Server（端口 4890），AI 代理可直接连接。

CatPaw / Claude Desktop / Cursor 等 MCP 客户端配置：

```json
{
  "mcpServers": {
    "aicut": {
      "url": "ws://127.0.0.1:4890/mcp",
      "transport": "websocket"
    }
  }
}
```

或通过 HTTP API 间接调用：

```json
{
  "mcpServers": {
    "aicut": {
      "command": "node",
      "args": ["/path/to/地鼠AI剪辑-main/apps/aicut-mcp/src/index.js"],
      "env": {
        "AICUT_URL": "http://localhost:4891",
        "AICUT_LOCAL_MEDIA_TOKEN": ""
      }
    }
  }
}
```

### 9.3 Tools 一览

地鼠AI剪辑桌面端 内嵌 MCP Server 提供 18 个 tools：

| Tool | 参数 | 说明 |
|------|------|------|
| `health` | 无 | 检查 地鼠AI剪辑 服务连接 |
| `bridge_call` | `method, args?` | 通用 Bridge 调用（可调任意 Bridge 方法） |
| `project_create` | `name` | 创建项目 |
| `project_list` | 无 | 列出项目 |
| `project_current` | 无 | 获取当前项目 |
| `project_open` | `id` | 打开项目 |
| `project_snapshot` | 无 | 项目快照（媒体库+时间线） |
| `project_validate` | 无 | 校验项目 |
| `media_import` | `media[]` | 导入素材 |
| `timeline_apply` | `canvasSize?, timeline, clearTimeline?, muteAll?` | 排时间线 |
| `project_apply` | `canvasSize?, media?, timeline?, captions?, ...` | 一步完成 |
| `subtitle_import_srt` | `srtText, fileName?, style?` | 导入 SRT 字幕 |
| `mute_all_video_source_audio` | 无 | 关闭所有视频原声 |
| `project_export` | `format?, quality?, download?` | 导出视频 |
| `player_play` | 无 | 播放 |
| `player_pause` | 无 | 暂停 |
| `player_seek` | `seconds` | 跳转 |
| `player_state` | 无 | 播放器状态 |

### 9.4 典型 AI 代理工作流

```text
1. AI 代理连接 ws://127.0.0.1:4890/mcp → initialize
2. AI 代理调用 project_snapshot → 读取当前项目状态
3. AI 代理调用 bridge_call(localMedia.authorizeFolder) → 授权文件夹
4. AI 代理调用 project_apply → 导入素材+排时间线+字幕+关原声
5. AI 代理调用 project_validate → 校验
6. AI 代理调用 project_export → 导出视频
```

### 9.5 已实现验证结果

```text
✅ 内嵌 MCP WebSocket Server（端口 4890）已稳定运行
✅ 18 个 tools 全部验证通过
✅ project_apply 一键完成：导入+排时间线+字幕+关原声（~1s）
✅ project_export 导出 mp4/webm（5s 视频约 3s 出片）
✅ 全链路计时：从授权到导出约 3-8 秒
```
