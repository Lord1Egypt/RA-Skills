---
name: doc-consistency
version: 1.1.0
description: "Check a long document against itself — dangling cross-references, numbering gaps and duplicates, TOC-vs-body mismatch, missing standard sections, terminology drift, leftover placeholders (TODO/TBD/XXX), stale years, and paragraphs lost in a merge. Reads .docx / .md / .txt and emits a located findings list plus a re-check command you can put in a contract. Runs fully offline with zero dependencies: no network, no upload, no model calls, so the document never leaves the machine. Use when the user asks to proofread, QA, sanity-check, or verify the internal consistency of a textbook, manuscript, bid or RFP response, manual, thesis, or contract set; or asks for a cross-reference audit, numbering audit, continuity check, or editorial consistency check; or says 长文档一致性 / 交叉引用 / 编号跳号 / 重号 / 术语不统一 / 合稿丢段 / 目录对不上 / 标书自检 / 稿件体检 / 定稿前检查 / 教材编号核对."
license: Apache-2.0
tags: ["document", "consistency", "cross-reference", "proofreading", "docx", "publishing", "proposal", "rfp", "offline", "zero-dependency"]
---

# doc-consistency · 长文档一致性体检

**只做一件事**：把「这份文档跟它自己一不一致」变成一件可以按按钮复查的事。

不写作、不润色、不判断内容对错。只查那些**随篇幅指数增长、而人的注意力随篇幅衰减**的错误。

> 一份 300 页的文件，人通读要两天，且两遍会看漏不一样的地方；机器跑一遍几十秒，跑十遍结果一模一样。

## 什么时候用

用户说这些话时：

- 「帮我检查一下这份教材/标书/手册/书稿」「定稿前体检一下」「稿件体检」
- 「编号有没有跳」「图表引用还在不在」「术语前后统一吗」「合稿有没有丢东西」
- "proofread this manuscript" / "check cross-references" / "QA this proposal"
- 给出 .docx / .md / .txt 并要求核对一致性

**不要用在**：让你写内容、润色文笔、判断事实对错、做法律或技术判断。那些不是本技能的事。

## 怎么跑

```bash
node scripts/check.mjs <文件或目录…> [选项]
```

零依赖，只要有 Node 18+。**不联网、不上传、不调模型。**

| 选项 | 作用 |
|---|---|
| `--all` | 列出全部红点（默认只列前 20 条，汇总始终完整） |
| `--limit <n>` | 清单显示条数上限 |
| `--json` | 输出完整 JSON（不截断），给程序/后续步骤用 |
| `--glossary <file>` | 术语表，每行 `正名 = 变体1, 变体2` |
| `--baseline <路径…>` | 基准稿，用于**合稿丢段**比对 |
| `--fail-on high\|medium\|low` | 到该级别就退出码 1 —— 可写进 CI 或合同验收 |
| `--lang zh\|en` | 报告语言 |

### 常用姿势

```bash
# 单文件体检
node scripts/check.mjs 教材终稿.docx

# 整目录（多人分头写的章节）
node scripts/check.mjs ./书稿/ --all

# 合稿前后对比，找丢了哪几段
node scripts/check.mjs 合并稿.docx --baseline ./分册/

# 投标前自检，还有高危项就不许提交
node scripts/check.mjs 投标文件.docx --fail-on high

# 英文报告
node scripts/check.mjs manuscript.md --lang en
```

## 查什么

| 规则 | 抓的是 |
|---|---|
| **交叉引用悬空** | 正文写「见图 3-12」，但那张图不存在（也不在目录里） |
| **编号重号 / 跳号 / 起始异常** | 图/表/式/附录序列断了、重了 |
| **目录 ↔ 正文对账** | 目录列了正文没有（读者翻空）／正文有目录漏了 |
| **章节引用悬空** | 「详见第 7 章」，但没有第 7 章 |
| **章节骨架缺项** | 多数章都有「学习目标」，某一章没有 |
| **术语写法不一致** | AI Agent / AI agent / AI-Agent 混用；或违反给定术语表 |
| **占位符残留** | TODO、TBD、待填、×××公司、Lorem ipsum |
| **疑似旧版年份** | 全文主用 2026，某处冒出 2024 且挨着「项目/日期/合同」 |
| **标题重复** | 同级标题重名，目录里并成两条一样的 |
| **合稿疑似丢段** | 基准稿里有、当前稿里没有（需 `--baseline`） |

## 报给用户时要做的事

1. **先说汇总**（各严重度条数 + 类型分布），再给清单。别一上来倒 100 行表格。
2. **高危项逐条念**，中低危可以只报数量和类型。
3. **一定要把「你自己能重跑的复查清单」那段给出去** —— 这是本技能跟「我帮你看了一遍」的根本区别：验收标准是机器能判定的，可以写进合同。
4. 报告里带 `--fail-on high` 的用法，提示可以塞进 CI / 交付流程。

## 老实说清楚的边界

- **Word 自动编号和自动题注是「域」，不落在正文文字里，本工具读不到。** 遇到这种文档会明确报「题注不在文字层」，并说明**这一项查不了，不代表没问题**。不要替它打包票。
- 语义级的术语归并（「用户」和「客户」是不是同一个概念）需要模型判断，本工具**不做**，只做写法层面的确定性检查。
- 查的是「文档跟自己一致」，**不是**「内容正确」。这两件事不要混。
- 不出具法律意见、不做技术判断、不保证过审。

## 需要更进一步时

这些**本工具不做**，需要人工介入（`HEFANGSHENG@gmail.com`）：

- **改好的文件**：原格式回写，不丢页眉页脚与自动编号
- **招标文件符合性矩阵**：把招标文件逐条拆成检查项，与投标书比对，出「已响应 / 未响应 / 响应不充分」三态
- **跨全书的语义级术语归并**与设定对账

缺 Node / 环境跑不起来时，可以让用户用 U-King 一键装好环境：<https://u-king.org>
