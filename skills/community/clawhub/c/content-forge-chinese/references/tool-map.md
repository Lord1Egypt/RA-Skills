# 工具能力地图（Tool Map）

> AI 调用其他工具前必读。每条记录回答四个问题：**用来做什么 / 何时触发 / 怎么调 / 有什么坑**。
>
> 工具新增/变更后，**必须立即更新此文件**，否则 SOP 会跑偏。

---

## 1. WebFetch（WorkBuddy 内置）

| 项 | 内容 |
|---|---|
| **能力** | 抓取任意 URL 内容，转 Markdown，按 prompt 提取信息 |
| **触发** | 抓微信公众号 / 普通网页 / 简单 HTML 页面 |
| **调用** | `WebFetch(url, prompt)` —— prompt 描述要提取什么 |
| **国内可用性** | 🟢 高（不依赖代理也能抓国内站点） |
| **优势** | 零依赖、秒级返回、自动 HTML→MD |
| **不适用** | 需要登录态的内容（财新订阅、星球）、JS 重渲染的 SPA、视频站点 |

### 实测（2026-05-20）

抓 https://mp.weixin.qq.com/s/KnRRCarUpn54HbE-Um2yJg：
- ✅ 标题、作者、公众号、正文、内嵌链接、图片 URL、表格数据全部抓到
- ✅ 不需要 wexin-read MCP

抓 https://www.xiaoyuzhoufm.com/podcast/<id>：
- ✅ 节目名、嘉宾、时长、**完整章节时间戳**、shownotes、推荐链接
- ❌ 拿不到音频文件 URL（小宇宙防盗链）—— 但通常不需要

抓 https://www.bilibili.com/video/BV<id>：
- ✅ 标题、UP主、时长、简介、播放量等元数据
- ❌ 视频本身需要 yt-dlp，但元数据 WebFetch 已够用

### 坑

- 输出会被 LLM 总结，**不一定是逐字原文**。要原文请在 prompt 明确「保留全文不要摘要」
- 对超长文章（>5w 字）会自动截断
- 同一 URL 15 分钟内会走缓存

---

## 2. ima-skill 系列（IMA 笔记 / 知识库）

IMA 有两个独立子能力，**功能完全不同，必须分清**：

### 2a. ima-skill:notes（个人笔记）

| 项 | 内容 |
|---|---|
| **能力** | 创建/搜索/编辑/删除 IMA 个人笔记 |
| **触发** | 用户说"写入 IMA 笔记""保存到 IMA""帮我记一下" |
| **是否参与 AI Q&A** | ❌ **不参与**！Notes 仅是笔记本，不进检索 |
| **格式限制** | 纯 Markdown 文本 + **网络图片链接**（不接受本地图片） |
| **单笔记上限** | 约 50KB |

### 2b. ima-skill:knowledge-base（知识库）

| 项 | 内容 |
|---|---|
| **能力** | 上传文件/网页到 IMA 知识库，搜索知识库内容 |
| **触发** | 用户说"上传到知识库""加到资料库""搜知识库" |
| **是否参与 AI Q&A** | ✅ **参与**！这才是问答检索的数据源 |
| **支持格式** | Markdown / PDF / Word / 网页 URL |
| **本 Skill 的意义** | 想让产物可被 AI 问答检索 → 必须走 KB，不能走 Notes |

### 调用决策

| 场景 | 用哪个 |
|---|---|
| 公众号深度分析报告（私人阅读） | `ima-skill:notes` |
| 公众号深度分析（要 AI 问答） | `ima-skill:knowledge-base` |
| 小宇宙摘要（个人收藏） | `ima-skill:notes` |
| 知识库文档（团队/AI 用） | `ima-skill:knowledge-base` |

### 坑

- Notes 的 Markdown 不支持本地图片 `![](./xxx.png)`，必须先上传图床转 https URL（用 `feishu-md-cleaner` 处理）
- KB 上传 PDF 要等待索引完成才能搜（约 30s-2min）
- 写入前问用户："要进 AI 问答检索？" → 是 → KB；否 → Notes

---

## 3. lark-master（飞书全能技能）

| 项 | 内容 |
|---|---|
| **能力** | 飞书文档 / 表格 / 多维表格 / 云盘 / Wiki / 消息 / 日历 / 任务 / 视频会议 / 妙记 |
| **触发** | 用户说"写到飞书""创建飞书文档""归档到飞书""发飞书消息" |
| **认证** | 用户需先按 `lark-master` Skill 指引完成飞书 App 授权 |
| **本 Skill 用到的能力** | 创建 docx 文档、写入云盘指定目录 |

### 常用调用模式

```bash
# 创建 docx
lark-cli drive +create --as user --doc-type docx --title "<标题>" --folder-token "<目录>"

# 写入内容（上面命令返回 obj_token）
lark-cli docx +update --as user --token "<obj_token>" --content-file "report.md"

# 上传到云盘指定目录
lark-cli drive +upload --as user --folder-token "<目录token>" --file "<本地路径>"
```

### 默认目录

由用户在首次使用时配置，推荐建立分类目录：

- AI 文章深度分析存档目录
- 播客笔记目录
- 临时产物目录

> 用户的具体目录命名/结构属于个人偏好，请通过 AskUserQuestion 询问，**不要硬编码**。

### 坑

- Wiki 下的资源**不能**直接用 node_token 调 docx/bitable API，必须先 `wiki/v2/spaces/get_node` 取 obj_token
- 飞书目录结构因人而异，**不要假设**用户的层级命名，首次使用时让用户提供 folder_token

---

## 4. feishu-md-cleaner（飞书 MD 清理）

| 项 | 内容 |
|---|---|
| **能力** | 飞书导出的 .md → 清洗 HTML 表格、转义字符、提取 docx 内图片 → 上传图床 → 替换为 https URL |
| **触发** | 飞书 → IMA / 其他 Markdown 平台前的中间清洗 |
| **本 Skill 调用时机** | 把飞书文档作为内容源时（场景 5 视频号 PPT 的飞书归档前置） |

### 链路

```
飞书 docx → lark-cli export → 原始 .md（含 HTML 表格、escaped chars、本地图片）
   ↓
feishu-md-cleaner → 清洗后的 .md（纯 Markdown + https 图片）
   ↓
ima-skill:notes / ima-skill:knowledge-base
```

---

## 5. wexin-read MCP（可选上游组件）

| 项 | 内容 |
|---|---|
| **能力** | Playwright 模拟浏览器抓微信公众号 |
| **触发** | WebFetch 抓不全时兜底（实测大多数场景 WebFetch 已够） |
| **依赖** | Python + Playwright + Chromium |
| **需要安装上游** | 是（如不使用可跳过，不影响本 Skill 基本功能） |

> ⚠️ 本 Skill 主流程**不需要** wexin-read MCP，WebFetch 内置抓取已覆盖场景 1/2/4/5 的抓取需求。安装上游仅在高级用户需要粉丝内容抓取时才有必要。

### 何时必须用

- WebFetch 返回内容明显被截断（< 30% 原文）
- 公众号开启了"不允许第三方抓取"严格模式
- 用户提供了登录态 cookie 想抓只对粉丝可见的内容

---

## 6. agent-browser / playwright-cli（终极兜底）

| 项 | 内容 |
|---|---|
| **能力** | 完整浏览器自动化 —— 点击、填表、滚动、截图 |
| **触发** | 上面所有抓取方案都失败 + 内容必须拿到 |
| **本 Skill 主要用途** | 视频号录屏、知识星球登录后抓取、复杂 SPA |

### 决策树

```
抓 URL：
  WebFetch
    ├─ 成功 → done
    └─ 失败/不全 → wexin-read MCP（仅微信）
                      ├─ 成功 → done
                      └─ 失败 → agent-browser
                                  └─ 让 AI 模拟浏览器交互
```

---

## 7. notebooklm CLI（上游官方工具）

| 项 | 内容 |
|---|---|
| **能力** | 创建 notebook、添加 source、生成 Audio Overview / Mind Map / Briefing Doc / Quiz / Video 等 |
| **安装** | `pip install notebooklm-cli` 或 `npm install -g @notebooklm/cli`（需确认官方包名） |
| **认证** | `notebooklm login` → 浏览器授权 → 一次性完成 |
| **国内可用性** | 🔴 需代理（notebooklm.google.com 在大陆封锁） |
| **首选场景** | 场景 3（Mind Map）、场景 4（播客/Audio Overview）、场景 5（PPT/Slide Deck） |
| **不适用场景** | 国内特供内容（公众号/小宇宙/知识星球）—— 先抓取再上传 |

### 调用流程（3步）

```bash
# Step 1：创建 notebook（返回 notebook ID）
notebooklm create "<标题>"

# Step 2：添加 source（本地文件或 URL）
notebooklm source add /path/to/file.txt --title "<源标题>"
# 或直接传 URL（YouTube、网页等）
notebooklm source add https://example.com/article

# Step 3：生成内容并下载
notebooklm generate <type>    # audio | mind-map | slide-deck | quiz | report | ...
notebooklm artifact wait <task_id>   # 等待生成完成
notebooklm download <type> <output_path>   # 下载到本地
```

### 生成类型对照

| 类型 | 命令 | 输出格式 |
|---|---|---|
| 播客（Audio Overview） | `notebooklm generate audio` | `.mp3` |
| 思维导图 | `notebooklm generate mind-map` | `.json` |
| PPT | `notebooklm generate slide-deck` | `.pdf` |
| 测验 | `notebooklm generate quiz` | `.md` |
| 报告 | `notebooklm generate report` | `.md` |
| 闪卡 | `notebooklm generate flashcards` | `.md` |

### 检测可用性

```bash
notebooklm status 2>/dev/null && echo "✅ 可用" || echo "❌ 不可用"
```

### 降级触发条件

- `notebooklm status` 失败（未安装 / 未登录 / 网络不可达）
- 代理未配置 / 配置失败
- 生成超时（Audio Overview 通常 3-5 分钟）

### 降级路径

```
notebooklm 不可用
  → 检测环境变量 PROXY / notebooklm_proxy
  → 尝试设置代理重试
  → 仍失败 → 降级到 C 方案（本地 LLM 直接生成）
```

---

## 8. Get笔记 API（语音/视频转写）

| 项 | 内容 |
|---|---|
| **能力** | 接收音视频 URL → 异步回调返回逐字稿 + 时间戳 + 说话人分离 |
| **触发** | 场景 2（小宇宙）、场景 5（视频号/B站） |
| **配置** | `GETNOTE_API_KEY` + `GETNOTE_CLIENT_ID` 环境变量 |
| **替代** | 没配 API → fallback 到 Whisper.cpp 本地（large-v3 模型） |

---

## 9. 标准库（ffmpeg / yt-dlp / Whisper.cpp）

| 工具 | 用途 | 调用 |
|---|---|---|
| `ffmpeg` | 提取音轨、抽关键帧、合并音视频 | `ffmpeg -i video.mp4 -vn audio.m4a` |
| `yt-dlp` | B站/YouTube/抖音/小红书视频下载 | `python3 -m yt_dlp <URL>` |
| `whisper.cpp` | 本地音频转写（无 API 时兜底） | `./main -m models/ggml-large-v3.bin -f audio.wav` |

### yt-dlp 实战技巧（2026-05-20 实测）

教程类系列视频**优先做元数据探查**，**不要**直接下载：

```bash
# 仅获取分 P 清单（秒级，不下载视频）
python3 -m yt_dlp --skip-download \
  --print "p%(playlist_index)s | %(title)s | %(duration_string)s" \
  <URL>

# 优先尝试拿字幕（B站部分视频有内嵌字幕）
python3 -m yt_dlp --write-sub --sub-lang zh --skip-download <URL>
```

安装方式：
```bash
pip3 install --user yt-dlp
# 用 `python3 -m yt_dlp` 调用，避免 PATH 问题
```

---

## 工具调用决策矩阵

| 任务 | 首选 | 次选 | 兜底 |
|---|---|---|---|
| 抓微信公众号 | WebFetch | wexin-read MCP | agent-browser |
| 抓飞书文档 | feishu-read MCP | lark-cli +export | 用户上传 |
| 抓海外付费墙 | jina-proxy | bot-ua | agent-browser |
| 抓财新等国内付费 | 用户 cookie | 公众号镜像 | 用户复制粘贴 |
| 写 IMA 私人 | `ima-skill:notes` | - | 本地 .md |
| 写 IMA AI 检索 | `ima-skill:knowledge-base` | - | - |
| 写飞书 | `lark-master` | - | 本地 .md |
| 文章深度分析 | LLM 12 问（C 方案） | NotebookLM | - |
| 视频转写 | Get笔记 API | Whisper.cpp 本地 | - |
| 视频下载 | yt-dlp | 用户屏幕录制 | - |
| 思维导图渲染 | 直接出 Mermaid | NotebookLM Mind Map | - |
| 图床上传 | feishu-md-cleaner 集成 | 用户手动 | - |

---

## 维护规范

✅ **新增工具**：在本文件加一节，含触发/调用/坑
✅ **删除工具**：标注 `~~deprecated~~` 说明替代方案
✅ **能力变化**：实测发现新边界 → 立即更新对应章节
✅ **示例命令**：尽量给可复制的最小调用样例
