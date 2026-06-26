# 场景 5：视频号 → 团队 PPT

## 一句话定位
微信视频号（或 B 站 / 抖音）链接 → 提取音视频 → Whisper 转写 → NotebookLM 生成 PPT。

## 触发词

- 「视频号生成 PPT」「这个视频做 PPT」
- 「B站视频做团队分享 PPT」
- 「短视频转 PPT」

## 为什么单独做？

视频号是国内**最难抓**的内容源之一：
- ❌ 没有公开播放 URL（仅限微信内打开）
- ❌ 反爬严格，不能像 YouTube 那样直接 yt-dlp
- ✅ 唯一可靠路径：屏幕录制 → 提取音轨 → 转写

B 站 / 抖音 / 小红书视频则可以走标准 yt-dlp 路径。

## 输入

| 字段 | 必填 | 说明 |
|---|---|---|
| 视频号链接 / B站 BV 号 / 视频文件 | ✅ | 三选一 |
| PPT 风格 | ⬜ | `团队分享` / `客户汇报` / `极简风`，默认团队分享 |
| 页数偏好 | ⬜ | `15-20` / `25-30` / `40+`，默认 25 |
| 输出格式 | ⬜ | `PDF` / `PPTX` / `Marp md`，默认 PDF |

## 输出

- PPT 文件（PDF / PPTX / Marp）
- 演讲者备注（speaker notes）
- 视频转写文字稿（含时间戳）
- 关键截图（每页配图来源于视频帧）

## 工作流

> ✅ **2026-05-20 实测发现**：教程类系列视频（每集都有清晰章节标题）**不需要转写音频**。`yt-dlp --skip-download --print` 秒级拿到所有分 P 标题 + 时长，直接基于章节出大纲质量已足够。22 集教程从输入到出 PPT 大纲全程 < 5 分钟。

### 视频类型 → 处理路径决策

```
视频是哪种？
├─ 教程系列（章节明确，如 BV1Dx411z7gb）
│   → yt-dlp 元数据 + 章节标题 → 直接出 PPT 大纲（推荐 ✅）
├─ 单集长视频（演讲、分享、访谈）
│   → 下载 + 字幕/转写 → 内容摘要 → PPT 大纲
└─ 短视频 / 视频号
    → 下载 / 录屏 → Whisper 转写 → PPT 大纲
```

### 详细步骤

```
[Step 1] 元数据探查（**任何视频都先做这步**）
  ├─ python3 -m yt_dlp --skip-download --print "<format>" <URL>
  ├─ 提取：标题、UP主、时长、分 P 列表（如有）、字幕可用性
  └─ 输出：playlist.txt + meta.json

[Step 2] 路径分支

  PATH A（教程系列，章节明确）：
    ├─ 跳过下载和转写
    ├─ 章节标题 + 时长 → LLM 直接出大纲
    └─ 输出：outline.md

  PATH B（长视频，需详细内容）：
    ├─ yt-dlp 下载视频/字幕
    ├─ 有内嵌字幕 → 直接用字幕
    ├─ 无字幕 → ffmpeg 抽音轨 → Whisper / Get笔记 转写
    └─ 输出：transcript.txt

  PATH C（视频号 / 抖音 / 小红书）：
    ├─ 视频号：用户录屏后给本地文件
    ├─ 抖音/小红书：yt-dlp 试试，失败让用户提供
    └─ 输出：video.mp4 → 进入 Step 3

[Step 3] 检测 NotebookLM 可用性
  └─ `notebooklm status` → 可用 → 走路径 A（生成 Slide Deck）
  └─ 不可用 → 降级走路径 B（本地 LLM 直接出大纲）

### 路径 A：NotebookLM 路径（推荐）

```
[Step A1] 长视频下载 + 转写（如 Step 2 选了 PATH B/C）
  ├─ yt-dlp 下载 / 字幕提取
  ├─ ffmpeg 抽音轨
  └─ Whisper / Get笔记 转写 → transcript.txt

[Step A2] 上传 NotebookLM（Playwright 浏览器上传）
  node scripts/notebooklm-playwright.js upload-text "<视频标题>" "transcript" "<content>"

[Step A3] 生成演示文稿（Slide Deck）
  node scripts/notebooklm-playwright.js generate "<视频标题>" presentation [outputDir]
  # 脚本自动：打开笔记本 → 点击"演示文稿" → 等待生成完成

[Step A4] 选配封面图（关键帧匹配）
  ├─ 每页根据时间戳从 frames/ 取最接近的关键帧
  ├─ 对截图做轻度增强
  └─ 输出：每页配图
```

### 路径 B：C 方案（降级 fallback）

```
[Step B1] LLM 直接渲染 PPT 大纲
  ├─ 用 LLM 把内容整理成 25 ± 3 页大纲（JSON）
  ├─ 每页：标题 / 要点 / 演讲者备注 / ts 时间戳
  └─ 输出：outline.json

[Step B2] 生成 PPT
  ├─ Markdown 大纲 → Marp / Slidev 渲染 → PDF/PPTX
  ├─ 或 python-pptx 模板填充
  └─ 输出：deck.pdf / deck.pptx
```

[Step 4] 输出
  └─ ~/Downloads/neirong-gongfang/video-to-ppt/<日期>/
```

## PPT 大纲生成 Prompt

```
你是一位专业的内容设计师，把视频转写整理成一份给团队分享用的 PPT。

输入：视频转写（含时间戳）
输出：JSON 数组，每个对象 = 1 页 PPT

要求：
- 总页数 25 ± 3
- 第 1 页：封面（标题、副标题、原视频出处）
- 第 2 页：本次分享的 3 个目标
- 第 3 - N-2 页：核心内容
  - 每页 1 个核心论点 + 3-5 条要点
  - 标题用动词开头，避免名词堆叠
  - 要点不超过 15 字 / 条
- 倒数第 2 页：行动建议
- 最后一页：Q&A / 谢谢

每页 schema：
{
  "page": 1,
  "title": "...",
  "bullets": ["...", "..."],
  "notes": "讲者备注 200 字",
  "ts": "00:12:34"   // 对应视频时间戳，用于截图
}
```

## 渲染选择

### Skill 方案对比（2026-05-21 实测）

| 方案 | Skill | 设计质量 | 易用性 | 适用场景 |
|---|---|---|---|---|
| **方案1（推荐）** | `anthropics/skills@pptx` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 需要专业设计感、自定义布局 |
| **方案2（快速）** | `aktsmm/powerpoint-automation` | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 标准格式、快速出稿、批量生成 |
| **方案3（极简）** | Marp / Slidev | ⭐⭐ | ⭐⭐⭐⭐ | 程序员、版本化需求 |

> 实测详情 → `~/Downloads/neirong-gongfang/pptx-skill-comparison/2026-05-21/comparison-report.md`
>
> 其他候选：`supercent-io/pptx-builder`（私有仓库，安装失败）、`googleworkspace/cli@presentation`（仅创建Google Slides，不适用本场景）

### 方案1：anthropics/skills@pptx（html2pptx）

**技术路径**：HTML slides → html2pptx.js（Playwright渲染 + PptxGenJS生成）

```bash
# 1. 生成HTML slides（每页一个HTML文件）
# 2. 运行转换脚本
node gen.js  # 内部调用 html2pptx(slide.html, pptx)
```

**优点**：设计质量最高，完全自定义布局，支持图表/图片/图标
**缺点**：需手写HTML+JS，调试周期较长
**依赖**：Node.js + Playwright + Sharp（全局已安装）

### 方案2：aktsmm/powerpoint-automation（content.json + 模板）

**技术路径**：content.json → template.pptx → create_from_template.py

```bash
python scripts/create_from_template.py template.pptx content.json output.pptx
```

**优点**：最易用（只需JSON），自动布局匹配，有验证脚本
**缺点**：设计质量依赖模板，可定制性有限
**依赖**：Python + python-pptx

### 输出格式

| 格式 | 优点 | 适合 |
|---|---|---|
| **PDF** | 跨平台，立即可用 | 临时分享 |
| **PPTX** | 可二次编辑 | 正式汇报、需要美化 |
| **Marp md** | 版本化，纯文本 | 程序员、需要长期维护 |

## 降级方案

| 失败点 | 降级 |
|---|---|
| 视频号无法录屏（手机用户） | 让用户上传视频文件 |
| Whisper 转写不准（方言/口音） | 询问是否切到 Get笔记 API（更鲁棒） |
| NotebookLM 生成大纲超长 | 拆 source（每 30 分钟一段），分页生成 |
| html2pptx 渲染失败 | fallback 到 aktsmm/powerpoint-automation（content.json + 模板） |
| 模板渲染失败 | fallback 到 Marp md |

## 输出物示例

```
~/Downloads/neirong-gongfang/video-to-ppt/2026-05-20/
├── video.mp4               # 原视频缓存
├── audio.m4a
├── transcript.txt
├── frames/                 # 关键帧
├── outline.json            # PPT JSON
├── deck.pdf                # 25 页 PDF
├── deck.pptx               # 可编辑版
└── speaker-notes.md        # 讲稿
```

## 进阶：批量处理

```
把这 5 个 B 站 BV 号都做成 PPT，并合并成一份"AI Agent 入门"系列分享
```

AI 内部：每个视频独立 pipeline → 最后用 LLM 做章节合并 → 输出一份完整 deck。

## 🛡️ 诚实度契约

> 详见 `references/honesty-rules.md`

### ⚠️ 本场景最大风险

**教程系列视频走"元数据路径"时，AI 没看视频内容**，PPT 里的：
- 各页要点：基于章节标题的推断
- Speaker Notes：AI 编的"建议讲法"，不是原视频内容

绝不能让用户以为 PPT 是从视频"提炼"出来的。

### 完整度声明（按路径分）

| 路径 | source_completeness | ai_inference_ratio |
|---|---|---|
| A 教程系列只看元数据 | metadata-only | high |
| B 长视频走转写 | full | medium |
| C 视频号录屏后转写 | full | medium |

### 标注规则（PATH A）

- 章节标题 + 时长：直陈，标 *(来自视频元数据)*
- 各页"要点"：标 *(基于章节标题推测，未观看视频)*
- "Speaker Notes" 重命名为 **"推荐讲法（AI 建议）"**，避免假装是从视频抄的
- 模块划分：标 *(AI 建议的逻辑分组)*

### 标注规则（PATH B/C）

- 转写文字段落：直陈
- PPT 要点：基于转写做的提炼，标 *(基于转写)*
- Speaker Notes：可以更接近原讲者表述，但仍标 *(AI 整理)*

### 输出 schema 必带

```json
{
  "source_completeness": "metadata-only | full",
  "ai_inference_ratio": "high | medium",
  "method": "yt-dlp 元数据 / Whisper 转写 / Get笔记 转写",
  "warnings": [
    "PATH A：未观看视频，PPT 内容基于章节标题",
    "Speaker Notes 为 AI 推荐讲法，不是原作者表达"
  ]
}
```

### 升级路径

如果 PATH A 输出质量不够，升级到 PATH B：
1. 让用户确认是否要下载和转写（耗时 30-60 min）
2. 走完整 yt-dlp + Whisper pipeline
3. ai_inference_ratio 降到 medium
