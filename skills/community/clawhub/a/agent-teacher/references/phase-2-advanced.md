# 进阶课程详解

## 搜索与信息获取

### mmx-cli（MiniMax CLI 工具箱）

**用途**：中文友好的搜索、图片生成、语音合成、视频生成、音乐生成

**安装**：已安装在 PATH（`which mmx` 验证），API key 已配置在 `~/.mmx/config.json`

**优势**：比 `mcporter call` 更稳定，不易超时

**所有子命令**：
```
mmx --help
mmx search     # 搜索
mmx image      # 图片生成
mmx speech     # 语音合成
mmx video      # 视频生成
mmx music      # 音乐生成
mmx vision     # 图片理解
mmx quota      # 额度查询
```

**搜索（search）**：
```bash
mmx search query "搜索内容"
```

**图片生成（image）**：
```bash
mmx image generate "一只穿宇航服的猫站在火星上"
# 查看任务状态（慢任务）
mmx video task get <task_id>
```

**语音合成（speech）**：
```bash
mmx speech synthesize "要转成语音的文字"
# 查看可用音色
mmx speech voices
```

**图片理解（vision）**：
```bash
mmx vision describe "https://example.com/image.jpg"
```

**视频生成（video）**：
```bash
mmx video generate "日落海浪，慢镜头"
# 视频生成慢，可后台运行
mmx video generate "描述" &
# 查看任务状态
mmx video task get <task_id>
```

**音乐生成（music）**：
```bash
mmx music generate "生成一首欢快的夏天流行歌"
```

**额度查询**：
```bash
mmx quota show
```

**验证**：
- `mmx search query "今天上海天气"` 能返回准确结果
- `mmx image generate "一只红猫"` 能生成图片

### mini-max-web-search（MiniMax 网络搜索 via MCP）

**用途**：中文友好的网络搜索，质量高于 Brave Search

**说明**：备选方案，`mmx search` 优先于本方式

**核心用法**：
```bash
mcporter call --stdio "uvx minimax-coding-plan-mcp -y" \
  --env MINIMAX_API_KEY=你的key \
  --env MINIMAX_API_HOST=https://api.minimaxi.com \
  web_search query:"搜索内容"
```

**注意**：mcporter 方式容易卡死/超时，优先用 `mmx search`

### multi-search-engine（多引擎搜索）

**用途**：搜索中文/英文网络资源，支持 17 种搜索引擎

**安装**：`clawhub install multi-search-engine --dir skills`

**核心用法**：
- 支持百度、Bing、Google、搜狗等
- 支持 `site:` 搜索特定网站
- 支持时间过滤（day/week/month/year）
- 支持 `intitle:` 标题搜索

**验证**：能搜索"上海今天天气"并给出准确结果

---

## 浏览器控制

### browser（浏览器控制）

**用途**：控制 Chrome 浏览器，打开网页、截图、分析页面

**安装**：OpenClaw 内置（需启用）

**核心用法**：
```javascript
browser({ action: "open", url: "https://example.com" })
browser({ action: "snapshot" })
browser({ action: "screenshot" })
browser({ action: "act", kind: "click", ref: "..." })
```

**两种模式**：
- `profile="openclaw"`：OpenClaw 自己管理的隔离浏览器
- `profile="chrome"`：控制你已有的 Chrome 标签页（需安装 Chrome 扩展）

**验证**：能用 browser 打开一个网页并截图

---

## 外部服务调用

### mcporter（MCP 工具调用）

**用途**：备选方案，用于 mmx-cli 不覆盖的场景

**安装**：需单独配置 MiniMax API key

**注意**：mcporter 方式容易卡死/超时，搜索和图片生成优先用 `mmx-cli`

**常用工具**：
| 工具 | 用途 |
|------|------|
| `text_to_image` | 图片生成（用 `mmx image` 优先）|
| `text_to_video` | 视频生成（用 `mmx video` 优先）|
| `text_to_audio` | TTS 语音 |
| `voice_clone` | 声音克隆 |

**验证**：能生成一张图片

---

## 视觉输出

### canvas（画布控制）

**用途**：生成图片、PPT 等视觉内容

**安装**：OpenClaw 内置

**⚠️ 注意**：`action` 字段必须是特定枚举值，不接受 `open`。用 `browser` 工具打开 URL 而非 canvas。

**核心用法**：
```javascript
canvas({ action: "present", url: "data:image/png;base64,..." })
canvas({ action: "snapshot" })
```

**验证**：能用 canvas 生成一张图片

### mmx-cli（MiniMax 图片/视频生成）

**用途**：云端图片/视频生成，稳定可靠

**安装**：已安装在 PATH，API key 已配置

**图片生成**：
```bash
mmx image generate "一只穿宇航服的猫站在火星上"
```

**视频生成**：
```bash
mmx video generate "日落海浪，慢镜头"
```

**特点**：比 mcporter 方式更稳定，不易超时

### image（OpenClaw 内置图片理解）

**用途**：分析/理解图片内容

**安装**：OpenClaw 内置，视觉模型权限自动激活

**注意**：OpenClaw 有时误用 `read` 工具来识图，导致结果不准确。遇到识图任务时，应明确使用 `image` 工具。

---

## 技能开发

### skill-creator（创建新技能）

**用途**：创建、编辑、改进技能

**安装**：OpenClaw 内置

**核心用法**：按照 AgentSkills 规范创建 SKILL.md + 资源文件

**参考**：`skills/skill-creator/SKILL.md`

### clawhub（技能管理）

**用途**：查找、安装、发布技能

**安装**：`npm install -g clawhub`

**核心用法**：
```bash
clawhub search [关键词]          # 搜索技能
clawhub install [名称] --dir skills   # 安装技能
clawhub publish [路径]          # 发布技能
```

**验证**：能用 clawhub 搜索到一个技能

---

## 进阶课程毕业标准

1. 能用 `mmx search` 搜索中文内容
2. 能用内置 `image` 工具正确理解图片（不用 `read` 工具）
3. 能用 `mmx image generate` 生成图片
4. 能用 browser 打开网页并获取内容
5. 能用 clawhub 找到并安装一个新技能
