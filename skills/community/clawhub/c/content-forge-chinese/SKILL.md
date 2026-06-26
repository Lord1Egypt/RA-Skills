---
name: neirong-gongfang
description: 把公众号/小宇宙播客/知识星球/财新/视频号/B站等中文内容一键丢进，生成播客、PPT、思维导图、深度报告。中文用户深度定制，预置 5 大杀手场景模板，与 IMA 笔记、飞书文档无缝联动。本地 LLM 兜底，保证可用性。Use when 用户说「丢进 NotebookLM」「转成播客」「公众号转播客」「PDF 做思维导图」「文章生成 PPT」等。
license: MIT
---

# 内容工坊

把任何中文内容丢进，生成播客 / PPT / 思维导图 / 深度分析。

## 本地化适配

- 🗣 中文优先：生成结果默认中文，适合中文内容创作者
- 📱 飞书联动：输出直接同步至飞书文档、多维表格、云盘
- 🗄 IMA 知识库：内容自动存入 IMA 笔记/知识库，支持 AI 问答检索
- 💻 本地 LLM 兜底：NotebookLM 不可用时，自动降级调用本地大模型

## 触发词

「丢进 NotebookLM」「生成 NotebookLM」「转成播客」「做成 PPT」「做成思维导图」「深度分析这篇」「转 IMA 笔记 / 飞书」

## 5 大场景路由（命中后读对应文档）

| 场景 | 输入 | 文档 |
|---|---|---|
| 公众号深度分析 → IMA / 飞书 | 公众号 URL | `scenarios/01-wechat-to-ima.md` |
| 小宇宙播客 → 飞书 / IMA 摘要 | 小宇宙 URL | `scenarios/02-xiaoyuzhou-to-feishu.md` |
| 知识星球精华 → 思维导图 | 帖子文本 | `scenarios/03-zsxq-to-mindmap.md` |
| 财新文章 → 通勤播客 | 财新 URL | `scenarios/04-caixin-to-podcast.md` |
| 视频号 / B站 → 团队 PPT | 视频链接 | `scenarios/05-shipinhao-to-ppt.md` |

## 工作流（所有场景统一）

```
1. 抓取 → 2. 清洗 → 3. 【优先】NotebookLM 生成
                      ↘【降级】本地 LLM（C 方案）→ 4. 落地（IMA / 飞书 / 本地）
```

**NotebookLM 可用性检测**：每次执行 Step 3 前先运行 `notebooklm status`，可用则走 NotebookLM路径；失败则自动降级到 C 方案（本地 LLM 直接生成），不影响产出。

> ⚠️ **2026-05-28 重要更新**：CLI `notebooklm` 全功能不可用（`generate` HTTP 400、`source add-text` 假成功），**上传+生成全部改用 Playwright 浏览器自动化**：
> - CLI 仅用于：`login`（获取 cookies）/ `list` / `create`
> - 上传改用：`scripts/notebooklm-playwright.js upload-text "<notebook标题>" "<source标题>" "<content>"`
> - 生成改用：`scripts/notebooklm-playwright.js generate "<notebook标题>" <audio\|video\|report\|mindmap\|flashcards\|quiz\|presentation\|infographic\|datatable>`
> - 脚本通过 Playwright 操控浏览器完成全流程
> 
> 📋 **配额规则（2026-05-28 实测）**：
> | 维度 | 类型 | 重置条件 |
> |---|---|---|
> | 🔴 账号级每日上限 | 音频、视频、报告 | 新 notebook 也无法重置（但 24h 滚动窗口后可用） |
> | 🟢 notebook 级每日 1 次 | 思维导图、闪卡、测验、演示文稿、信息图、数据表格 | 新建 notebook 即重置 |

匹配场景 → 读 `scenarios/0X-xxx.md` → 按 SOP 执行 → 失败走 `references/troubleshooting.md` 降级。

## 🛡️ 诚实度规范（所有场景必守）

⚠️ **本 skill 的核心差异化：不只追求"做出来"，更追求"如实标注信息来源"**。

### 三类内容必须区分

| 类型 | 标记方式 | 例子 |
|---|---|---|
| **事实** | 直陈 | 节目时长 78 分钟 |
| **引用** | 用「」 | 「我们真是最后一代古代人」 |
| **AI 推断** | *(推断)* 或 *(基于章节标题推测)* | "本期高潮是 AI 与时代位置的讨论 *(推断)*" |
| **AI 建议** | 标注「推荐讲法」「AI 建议」 | "可以这样开场：…… *(AI 建议)*" |

### 输出底部必带 confidence 字段

```json
{
  "source_completeness": "full | partial | metadata-only",
  "ai_inference_ratio": "low | medium | high",
  "warnings": ["未听原音频", "正文仅有节选"]
}
```

### 抓取不完整时显著警告

当只拿到 metadata 而非全文时，**输出顶部** 必加一行警告：

```
⚠️ 本分析基于 [节目页 shownotes / 章节标题 / 元数据]，未读全文/未听原音频。
```

### NotebookLM 生成内容标注

调用 NotebookLM Audio Overview / Mind Map 时，输出注明：

```
🤖 以下内容由 NotebookLM 基于 source 演绎生成，可能包含：
   - 未在原文出现的过渡和判断
   - AI 推测的因果关系
   原始 source: <link>
```

📖 详细规范 → `references/honesty-rules.md`

## 按需查阅

| 何时 | 读什么 |
|---|---|
| **调用任何工具前** | `references/tool-map.md` 🔴 必读 |
| **写输出前** | `references/honesty-rules.md` 🔴 必读 |
| **首次安装** | `references/installation-cn.md` |
| **网络不通** | `references/china-network.md` |
| **抓不到内容** | `references/paywall-strategies-cn.md` |
| **任意环节报错** | `references/troubleshooting.md` |
| **PPT 生成问题** | `references/troubleshooting.md` →「PPT 生成工具链」章节 |

## 协同

`WebFetch`（内置抓取）/ `lark-master`（飞书）/ `ima-skill:notes` 或 `:knowledge-base`（IMA，注意区别！）/ `feishu-md-cleaner`（格式清理）/ `agent-browser`（兜底浏览器）

⚠️ **每个工具的能力/触发/坑请查 `references/tool-map.md`**，不要凭名字猜用法。

## License & Credits

MIT · 原创：[SirKayZh/ContentForge](https://github.com/SirKayZh/ContentForge) · 致谢上游：[joeseesun/qiaomu-anything-to-notebooklm](https://github.com/joeseesun/qiaomu-anything-to-notebooklm)
