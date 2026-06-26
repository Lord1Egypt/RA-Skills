# 场景 1：公众号深度分析 → IMA 笔记 / 飞书文档

## 一句话定位
微信公众号文章 → NotebookLM 12 问深度分析 → 同步到 IMA 笔记或飞书文档。

## 触发词

- 「公众号深度分析」「这篇文章深度分析」
- 「分析这篇文章并写入飞书 / IMA」
- 「微信文章 转 IMA 笔记」

## 输入

| 字段 | 必填 | 说明 |
|---|---|---|
| 公众号 URL | ✅ | `https://mp.weixin.qq.com/s/xxx` |
| 输出目标 | ⬜ | `IMA` / `飞书文档` / `本地 md`，默认 IMA |
| IMA 知识库 | ⬜ | 用户首次使用时指定，默认询问 |
| 飞书目录 | ⬜ | 用户首次使用时提供 folder_token |

## 输出

- 结构化 JSON（12 个深度问答 + 3 轮递进）
- Markdown 报告（含原文摘要 + 12 问答 + 关键引用）
- 落地：IMA 笔记 / 飞书文档 / 本地 md 三选一

## 工作流（AI 内部执行）

> ✅ **2026-05-20 实测简化**：WorkBuddy 自带 WebFetch 已能直接抓微信公众号正文（标题/作者/全文/链接），**无需上游 wexin-read MCP**。Playwright 仅作为兜底。

### 生成路径决策树

```
公众号 URL
  ↓
[Step 1] WebFetch 抓取文章
  ↓
[Step 2] 检测 NotebookLM 可用性
  └─ `notebooklm status` → 可用 → 走 NotebookLM 路径（推荐）
  └─ 不可用 → 降级走 C 方案（本地 LLM）
```

> ⚠️ **2026-05-28 更新**：
> - CLI `notebooklm generate` 报 HTTP 400，**生成环节改用 Playwright 浏览器自动化**。
> - CLI `notebooklm source add-text` / `add-file` **完全不可用**（假成功或 HTTP 400），**上传环节改用 Playwright 浏览器自动化**。
> - Playwright 脚本使用 **notebook 标题**（而非 CLI ID），因 CLI ID 与 Web URL ID 格式不一致。
> - **9 种生成类型全部可用**（2026-05-28 实测验证）。

```
[Step A1] 将 article.md 上传到 NotebookLM（Playwright 浏览器上传）
  node scripts/notebooklm-playwright.js upload-text "<notebook标题>" "<source标题>" "<content>"
  # 脚本自动：打开笔记本 → 点击"添加来源" → "复制的文字" → 粘贴 → 插入
  # ⚠️ 注意：CLI source add-text/add-file 均不可用，必须用 Playwright 上传

[Step A2] 生成 Audio Overview（播客）
  node scripts/notebooklm-playwright.js generate "<notebook标题>" audio [outputDir]
  # 脚本自动：打开笔记本 → 点击"音频概览" → 等待生成完成

[Step A3] 生成深度报告
  node scripts/notebooklm-playwright.js generate "<notebook标题>" report [outputDir]
  # 点击"报告" → 等待完成

# 支持的 generateType：audio | video | report | mindmap | flashcards | quiz | presentation | infographic | datatable
```

### 路径 B：C 方案（降级 fallback）

```
[Step B1] 12 问深度分析（直接 LLM）
  → 直接喂 article.md 给 LLM 跑 12 问

[Step B2] 递进式提问结构
  Round 1（4 个）：核心论点、关键数据、作者立场、行业背景
  Round 2（4 个）：基于 R1 答案追问 → 对比、反例、隐藏假设、可证伪点
  Round 3（4 个）：基于 R2 答案追问 → 实操启示、可迁移框架、潜在风险、3 年趋势

[Step B3] 输出：analysis-report.md
```

---

### Step 3（通用）内容清洗

[Step 5] 落地输出
  if 目标 == IMA Notes（私人收藏）:
    → 调用 ima-skill:notes 写入笔记（不参与 AI Q&A）
    → 标题：[深度分析] <原文标题>
    → tags: 公众号分析, AI 深度阅读
  if 目标 == IMA KB（参与 AI 检索）:
    → 调用 ima-skill:knowledge-base 上传 .md
    → ⚠️ 这才会进 AI 问答数据源
  if 目标 == 飞书:
    → 调用 lark-master 创建 docx
    → 归档到用户指定的目录（首次使用通过 AskUserQuestion 询问）
  if 目标 == 本地:
    → 写到 ~/Downloads/neirong-gongfang/wechat-deep/<日期>/
```

## 抓取策略详细对比

| 路径 | 依赖 | 成功率 | 速度 | 适合 |
|---|---|---|---|---|
| **WebFetch 直抓** | ✅ 零依赖 | 🟢 高（实测通过） | 🟢 秒级 | 大多数公众号 |
| 上游 wexin-read MCP | Python + Playwright | 🟢 高 | 🟡 ~10s | WebFetch 失败时兜底 |
| 用户复制粘贴 | 0 依赖 | 🟢 100% | - | 终极兜底 |

## 提示词模板（递进式提问）

```
你是这篇文章的资深读者。已读 source，请基于内容回答下列问题。
要求：每个回答 200-300 字，引用原文时用「」包裹，不要编造。

Round 1 - 内容理解：
Q1. 这篇文章的核心论点是什么？用一句话概括。
Q2. 文章给出的关键数据 / 案例有哪些？分别支撑了哪个论点？
Q3. 作者的立场和潜在动机是什么？
Q4. 这篇文章在行业讨论中处于什么位置（突破 / 重复 / 反主流）？

[等待 R1 答案，将其作为上下文]

Round 2 - 批判分析：
Q5. R1 中提到的 [核心论点]，最主要的反例是什么？
Q6. 作者隐含了哪些未明说的前提假设？哪个最关键？
Q7. 哪些数据 / 案例的因果关系可能被高估？
Q8. 用什么实验或观察可以证伪这个论点？

[等待 R2 答案]

Round 3 - 行动启示：
Q9. 对我（一个 [用户角色]）的最直接启示是什么？
Q10. 文章中可迁移到其他领域的方法论是什么？
Q11. 如果照做这个方案，最大的潜在风险是什么？
Q12. 3 年后回看，文章哪部分最可能被证明错误 / 过时？
```

## 降级方案

| 失败点 | 降级 |
|---|---|
| 微信公众号抓不到（cookie 失效） | 让用户手动复制全文，跳到 Step 2 |
| NotebookLM 上传失败 | 改用 Gemini API 直接做 12 问分析（无引用追溯） |
| 飞书 / IMA 写入失败 | fallback 到本地 md，给用户文件路径 |

## 命令示例

用户对话只需说一句话，AI 自动调度：

```
把这篇文章深度分析写入 IMA：https://mp.weixin.qq.com/s/Hu3LHuxqD4xaKEjox4lXyg
```

```
深度分析这篇并发到飞书 <你的目录名>：https://mp.weixin.qq.com/s/xxx
```

## 输出物示例

```
~/Downloads/neirong-gongfang/wechat-deep/2026-05-20/
├── original.md              # 抓取的原文
├── analysis.json            # 12 问 12 答结构化数据
├── report.md                # 给人读的 Markdown 报告
└── meta.json                # 公众号、作者、发布时间、URL
```

IMA 笔记 / 飞书文档则直接以可读格式落地，附原文链接。

## 🛡️ 诚实度契约

> 详见 `references/honesty-rules.md`

### 完整度声明（必加在输出顶部）

```markdown
> **抓取完整度**: partial（WebFetch 抓到的正文，可能不是完整原文）
> **AI 演绎程度**: medium（12 问中 R2/R3 是 AI 推断和建议）
```

### 标注规则

- 12 问中的 **R1（内容理解）**：基于原文事实，标 *(基于原文)*
- 12 问中的 **R2（批判分析）** / **R3（行动启示）**：AI 推断/建议，标 *(AI 推断)* 或 *(AI 建议)*
- 引用原文时必须用「」包裹

### 输出 schema 必带

```json
{
  "source_completeness": "partial",
  "ai_inference_ratio": "medium",
  "warnings": ["R2/R3 为 AI 推断，请以原文为准"]
}
```
