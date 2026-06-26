---
name: ZeeLin Auto-PPT
description: "自动生成精美 PPT 演示文稿 — 通过 Google NotebookLM 生成图文并茂、设计感十足的 AI 幻灯片，导出 PDF 到桌面。用户需自行登录 NotebookLM 网页版。标题微软雅黑 40 号加粗，排版震撼，逻辑图清晰，内容有深度有创新，引用权威数据。配合 desearch skill 使用效果更好。Keywords: PPT, presentation, slides, NotebookLM, PDF, design, infographic, AI generated."
user-invocable: true
metadata: {"openclaw":{"emoji":"📊","skillKey":"auto-ppt"}}
---

# ZeeLin Auto-PPT — AI 精美演示文稿生成器 📊

通过 Google NotebookLM 一键生成**图文并茂、排版精美、设计震撼**的演示文稿，导出 **PDF** 到桌面。

> ⚠️ **使用前请自行登录 NotebookLM 网页版**（https://notebooklm.google.com/）。登录由用户完成，Agent 只负责在已登录状态下完成创建笔记本、补充来源、粘贴内容、生成幻灯片和下载 PDF。

> 💡 **配合 desearch / deep-research 风格工作流使用效果更好**。若用户要求“深度研究报告大纲、分章节 PDF、最后合并、统一白板手绘风格、先补 YouTube 信息源”，请读取：`/Users/youke/.openclaw/workspace/skills/auto-ppt/references/deep-research-multipart-workflow.md`。

## 触发与模式选择

### 模式 A：普通 Auto-PPT
适用于：
- 给一个主题，直接生成一份 PDF
- 用 NotebookLM 做一份成品幻灯片
- 用户只要单份 PDF/PPT 收口

### 模式 B：多部分深度研究 Auto-PPT
适用于用户提到这些要求时：
- 先做成**具有传播力的深度研究报告大纲**
- 拆成 **6–10 个专业研究部分**
- **每个部分先单独做一份 PDF**
- **最后再合并**
- 先去 **YouTube 检索相关视频链接** 作为信息源
- 要 **白板手绘风格 / 布局多样 / 视觉惊艳 / 风格统一**
- 参考 `desearch-ppt-1.0.0 2` 的 PPT 风格

如果是模式 B，**只额外读取一个 reference**：
- `/Users/youke/.openclaw/workspace/skills/auto-ppt/references/deep-research-multipart-workflow.md`

---

## 🚨 最重要的规则：一次性连贯完成，不要中断

**你必须在一个回合内连续调用所有工具，一次性完成全部步骤。**

❌ 禁止的行为：
- 每做一步就停下来向用户汇报，等用户说"继续"
- 把每个步骤拆成独立回复
- 用长篇解释代替脚本执行

✅ 正确的行为：
- 生成内容后，**立即**调用 exec 执行脚本
- 所有 tool call 在同一个回合内连续发出
- 最后只给用户**一条简洁汇报**

**节省 tokens 规则：**
- 不复述显而易见的步骤
- 不把整段内容再次贴回聊天
- 复杂收尾优先走脚本
- 多部分模式下，先定大纲，再分 part 执行，不要一次塞一个超长 prompt

---

## 新默认流程：先补 YouTube 信息源，再生成演示文稿

当用户明确提到以下任一要求时，优先使用这个流程：
- “先打开 YouTube 搜关键词，再把视频链接加到 NotebookLM 来源里”
- “先加 YouTube 信息源，再做 PPT”
- “龙虾管理 / OpenClaw manage 这种主题先搜视频再生成”
- “把这个流程封装到自动做 PPT 的 skill 里”

### 标准执行顺序
1. 打开 YouTube
2. 以用户给的主题关键词检索（如 `龙虾管理`、`OpenClaw manage`）
3. 选 2–5 个相关视频链接
4. 打开 NotebookLM，新建 notebook
5. 点击 **添加来源 → 网站**
6. 将 YouTube 视频 URL 逐条插入为网站来源
7. 再把正文内容作为 **Copied text / 复制的文字** 插入
8. 点击 **自定义演示文稿 / Customize presentation**
9. 输入统一风格要求（如白板手绘、布局多样、标题强、信息图感强）
10. 点击生成
11. 下载 PDF 到桌面
12. 如用户要求，继续合并 PDF、清理重复页、导出 PPTX

### 参数约定（给脚本）
优先通过环境变量把这些信息传给脚本，而不是把所有流程写死在聊天里：
- `AUTO_PPT_YOUTUBE_QUERY`：YouTube 搜索关键词
- `AUTO_PPT_MAX_YOUTUBE`：最多采集多少个视频链接，默认 3
- `AUTO_PPT_CUSTOM_PROMPT`：NotebookLM 的“自定义演示文稿”风格提示词；未提供时默认使用 whiteboard sketch/doodle 英文风格模板

### 推荐风格提示词
如果用户没给具体风格，可默认：
- `STYLE: Whiteboard sketch/doodle style
- Background: light gray paper texture with wooden frame border
- Hand-drawn/sketch illustrations in black ink lines
- Blue and red accent colors
- All Chinese text must be perfectly rendered, clear and readable
- Layout should be clean and professional like a real presentation slide

Design a beautiful presentation slide with the following content. Arrange text and illustrations naturally for the best visual effect.`

如果用户只说“按默认白板手绘风格做”，优先使用上面这段英文风格提示，不要自行改写弱化。

---

## ⚡ 主生成脚本

普通模式：

```json
{"tool": "exec", "args": {"command": "cat > /tmp/ppt_content.txt << 'CONTENT_EOF'\n你的完整内容文本...\nCONTENT_EOF"}}
```

然后：

```json
{"tool": "exec", "args": {"command": "bash /Users/youke/.openclaw/workspace/skills/auto-ppt/scripts/create_ppt.sh \"$(cat /tmp/ppt_content.txt)\" \"文件名.pdf\""}}
```

带 YouTube 来源和自定义演示文稿模式：

```json
{"tool": "exec", "args": {"command": "AUTO_PPT_YOUTUBE_QUERY='OpenClaw manage' AUTO_PPT_MAX_YOUTUBE=3 AUTO_PPT_CUSTOM_PROMPT='请做成白板手绘风格、强信息图表达、标题有冲击力、布局多样、避免重复版式。' bash /Users/youke/.openclaw/workspace/skills/auto-ppt/scripts/create_ppt.sh \"$(cat /tmp/ppt_content.txt)\" \"OpenClaw龙虾管理学-01-问题定义与总框架.pdf\"", "timeout": 1800}}
```

---

## 收尾后处理（推荐，最省 token）

当用户提到这些需求时：
- 把下载到桌面的 PDF 合并成 1 个
- 再导出成 PPT / PPTX
- 把语义重复的页面删除、合并
- 让再次打开的 PPT 逻辑更通顺

优先执行：

```json
{"tool": "exec", "args": {"command": "python3 /Users/youke/.openclaw/workspace/skills/auto-ppt/scripts/postprocess_ppt_outputs.py --all-desktop --output-name final_deck", "timeout": 600}}
```

输出到桌面：
- `final_deck.merged.pdf`
- `final_deck.cleaned.pdf`
- `final_deck.cleaned.pptx`

如需指定顺序：

```json
{"tool": "exec", "args": {"command": "python3 /Users/youke/.openclaw/workspace/skills/auto-ppt/scripts/postprocess_ppt_outputs.py --output-name final_deck 第一部分.pdf 第二部分.pdf 第三部分.pdf", "timeout": 600}}
```

---

## Agent 规则

1. **用 `exec` 执行脚本**，不要直接用 `browser` 工具拼流程
2. 默认主生成阶段先产出 PDF
3. 若用户明确要求“后续收尾 / 合并 / 删重 / 导出 PPT”，优先调用后处理脚本
4. 若用户明确要求“先分 6–10 部分、每部分 PDF、先补 YouTube 信息源”，切到**多部分深度研究模式**并读取对应 reference
5. 对“删语义重复页”，优先低成本脚本启发式处理，不默认调用大模型逐页判断
6. 整体风格要统一，但单页布局要尽量多样
7. 涉及 YouTube 来源时，优先用脚本自动搜索并插入 2–5 个高相关视频 URL，不要只把搜索词写进正文冒充来源

---

## 设计标准

| 项目 | 要求 |
|------|------|
| 标题字体 | 微软雅黑，40 号，加粗 |
| 整体风格 | 图文并茂、精美震撼、配图精良 |
| 逻辑图 | 专业清晰（流程图/对比图/数据图表） |
| 内容 | 有创新、有深度、权威数据标注来源 |
| 初始输出 | PDF，保存到 `~/Desktop/` |
| 收尾输出 | 合并 PDF + cleaned PDF + cleaned PPTX |
| 高级模式 | 6–10 部分深度研究 + YouTube 信息源 + 分 part PDF + 最终合并 |

---

## TL;DR

- 普通需求：主题 → 长文 → NotebookLM → PDF
- 加强版：YouTube 检索 → 视频 URL 加到 NotebookLM 网站来源 → 长文 → 自定义演示文稿 → PDF
- 收尾需求：PDF → 合并/删重 → cleaned PDF + PPTX
- 深度研究需求：先出 6–10 部分大纲 → 每部分先补 YouTube 信息源 → 分 part 生成 PDF → 最后合并 → 必要时再后处理

