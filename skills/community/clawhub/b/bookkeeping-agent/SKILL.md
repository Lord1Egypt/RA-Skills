---
name: bookkeeping
description: 导入账单、检查重复、查询交易、查看汇总，并通过本地 bookkeeping CLI 执行。优先处理当前消息里已经落到本地的账单附件；当用户要求导入支付宝、微信或本地账单时，优先直接使用当前消息上下文中已有的本地文件路径。
metadata: {"openclaw":{"homepage":"https://github.com/lastarla/bookkeeping-agent","requires":{"bins":["bookkeeping"]},"install":[{"id":"brew","kind":"brew","formula":"lastarla/tap/bookkeeping-tool","bins":["bookkeeping"],"label":"Install bookkeeping (Homebrew, macOS)"},{"id":"pipx","kind":"pipx","package":"git+https://github.com/lastarla/bookkeeping-tool.git","bins":["bookkeeping"],"label":"Install bookkeeping (pipx from GitHub)"}]}}
---

# Bookkeeping

仅当本地 `PATH` 中已经可用 `bookkeeping` 命令时，才使用这个 skill。

## 适用场景

- 你想导入账单附件或本地账单文件
- 你想检查某个账单文件是否已经导入过
- 你想按时间范围、平台、收支方向或分类查询交易
- 你想查看概览、趋势或分类汇总
- 你想用自然语言记录单笔支出或收入
- 你想设置或检查日 / 月 / 年预算
- 你明确想启动本地 bookkeeping 看板
- 你明确想重置数据库

高置信账单信号：

- 文件扩展名为 `.csv` 或 `.xlsx`
- 文件名包含 `alipay`、`wx`、`wechat`、`bill`、`账单`、`交易`、`流水`
- 用户提到 `账单`、`流水`、`导入`、`支出`、`收入`、`支付宝` 或 `微信`

## 附件与文件解析

按以下顺序解析最终要导入的文件：

1. 如果当前 OpenClaw 消息上下文里已经有本地附件路径，直接使用该路径
2. 优先使用已经落在本地的 inbound 文件；典型路径可能位于 `/root/.openclaw/media/inbound/`
3. 如果没有本地路径，但存在可下载的消息附件引用，则先使用当前环境中可用的附件下载能力将文件落到本地
4. 将最终得到的本地路径传给 CLI

处理规则：

- 不要要求用户重新下载一个已经存在于本地的文件
- 不要要求用户手动把 inbound 文件复制到 workspace，只要当前进程能读就直接用
- 当 `message_attachment_download` 可用时，优先调用它，并使用返回的 `download.local_path`
- 如果当前环境没有可用的附件下载能力，则明确告知用户当前只能处理已经落到本地的附件或本地文件路径
- 文件类型判断优先依据附件原始文件名或 MIME 元数据，不要只依赖 inbound 本地文件名后缀，因为 inbound 文件可能不保留 `.csv` 或 `.xlsx`
- 如果存在多个可能的账单文件，先列出候选并让用户确认要导入哪一个
- 如果只有一个高置信账单文件且用户明确说要导入，可以直接继续

## CLI 映射

使用本地 `bookkeeping` CLI 作为执行后端。

- 导入：`bookkeeping import <file> --original-file-name <name> --json`
- 查询：`bookkeeping query --json`
- 概览汇总：`bookkeeping summary overview --json`
- 趋势汇总：`bookkeeping summary trend --json`
- 分类汇总：`bookkeeping summary category --json`
- 记录支出：`bookkeeping record expense --payload <json> --json`
- 记录收入：`bookkeeping record income --payload <json> --json`
- 设置预算：`bookkeeping budget set --scope <scope> --period <period> --amount <amount> --json`
- 检查预算：`bookkeeping budget check --scope <scope> --trade-date <date> --json`
- 查看批次：`bookkeeping inspect batches --json`
- 查看重复：`bookkeeping inspect duplicates --json`
- 启动看板：`bookkeeping serve`
- 重置数据库：`bookkeeping reset --yes`

导入规则：

- 当 inbound 本地文件没有可用后缀时，传入 `--original-file-name <original attachment name>`，让 CLI 仍然能根据原始文件名推断平台、owner 或格式
- 只要可用，优先使用 `--json` 输出
- 如果导入失败，简要说明原始错误原因

## 行为规则

### 可直接执行

在高置信、低风险情况下，可以直接执行：

- 导入单个高置信账单附件或本地账单文件
- 查询交易
- 执行 `summary overview`、`summary trend`、`summary category`
- 查看导入批次
- 查看重复导入情况
- 当金额、收支方向与平台可高置信推断时，记录单笔收入或支出
- 设置或检查预算

### 先澄清或确认

遇到以下情况时，先问最小必要问题：

- 只有一个账单附件，但用户表达很模糊，例如“处理一下”
- 用户说要导入，但存在多个疑似账单附件或多个候选本地文件
- 用户问“这个文件导入过没有”，但当前指代不清
- 用户想启动 dashboard，但没有明确表示现在就要启动本地服务

### 必须强确认

以下动作不能静默执行：

- `bookkeeping reset --yes`
- 重置数据库后再重新导入
- 批量处理多个附件

## 自然语言记账分类规则

当通过自然语言记录单笔收入或支出时：

- 允许模型推断分类，但必须落入固定分类集合
- 正常路径下不要要求用户手动选择分类
- 不要创造固定集合之外的自由分类
- 低置信度时，支出回退到 `其他支出`，收入回退到 `其他收入`

固定支出分类：

- `餐饮`
- `交通`
- `日用`
- `购物`
- `娱乐`
- `医疗`
- `住房`
- `教育`
- `其他支出`

固定收入分类：

- `工资`
- `报销`
- `转账`
- `退款`
- `理财`
- `其他收入`

## reminders 协议

当 CLI 返回 bookkeeping 结果时：

- 将 `budget_checks` 视为完整的预算状态
- 将 `reminders` 视为可直接面向 OpenClaw 或 IM 通道输出的提醒列表
- 如果 reminder 项中存在 `channel_text`，优先使用它生成简洁消息
- 如果 `reminders` 为空，不要额外生成预算提醒文案
- 如果 `status` 为 `unset`，可以温和提示用户设置预算
- 如果 `status` 为 `warning` 或 `exceeded`，在回复中明确呈现预算提醒
- 不要忽略已有 reminders；如果存在，就在结果中带出摘要

## 回复规则

- 先说明识别到的意图
- 再说明下一步动作，或提出最小必要问题
- 除非用户在排查环境问题，否则不要暴露底层 CLI 细节
- 如果缺少 `bookkeeping`，明确说明这个 skill 依赖本地 CLI
- 如果数据库为空，先提示用户导入账单，再进行查询或汇总
- 如果附件类型不支持，明确说明当前只支持 `.csv` 和 `.xlsx`
- 单笔记账成功后，简要返回收支方向、金额、平台、分类和日期
- 导入成功后，尽量返回文件名、owner、平台、总行数、导入行数、跳过行数和 batch id（如果 CLI 有这些字段）
- 如果存在 reminders，在结果后追加简短预算摘要
