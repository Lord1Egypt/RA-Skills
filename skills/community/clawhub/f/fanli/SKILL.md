---
name: fanli
description: 将商品链接或淘口令转为带优惠券的推广链接，跨平台比价（淘宝/天猫/京东/拼多多/抖音/唯品会/美团）， 查询历史价格走势并给出购买建议。当用户发来商品链接、淘口令、美团链接，或提到"转链"、"比价"、"历史价"、 "全网最低价"、"有没有优惠券"、"值不值得买"、"价格走势"、"优惠"、"便宜"、"划算"、"打折"、 "降价"、"满减"、"省钱"、"买不买"、"该不该入手"、"美团"、"外卖"、"团购"、"到店"、"美团红包"时使用。 不适用于：快递查询、汇率换算、天气查询、闲鱼二手交易等非购物比价场景。
version: 4.2.2
allowed-tools: Bash(node {baseDir}/scripts/run.mjs:*),Read({baseDir}/**),Read({baseDir}/../fx-base/**)
metadata:
  openclaw:
    requires:
      env:
        - FX_AI_API_KEY
    primaryEnv: FX_AI_API_KEY
---

> **CRITICAL** — 开始前 **必须**用 Read 工具读取 [`../fx-base/SKILL.md`](../fx-base/SKILL.md)，其中包含 feima-lab API 认证和请求规范。
>
> fx-base 未安装？执行 `npx skills install fangshan101-coder/fx-base` 安装到同目录下。

# 省钱购物助手

一次 `convert` 调用 → 同时拿到商品信息 + 比价 + 历史价 → 直接按模板渲染输出。

## 前置条件

- 环境变量 `FX_AI_API_KEY`：从 [feima-lab 开放平台](https://platform.feima.ai/) 登录获取。未设置时脚本会返回 `missing_api_key` 错误
- **数据流向**：用户提供的商品链接会被发送到 `https://api-ai-brain.fenxianglife.com` 进行解析，请确保信任该服务后再使用

## 快速开始

```bash
# 快捷命令（推荐）
node {baseDir}/scripts/run.mjs convert "<链接或口令>"

# 美团链接转链
node {baseDir}/scripts/run.mjs convert "https://click.meituan.com/t?t=1&c=2&p=xxx"

# 等价的标准调用
node {baseDir}/scripts/run.mjs call convert --tpwd "<链接或口令>"

# 查看接口帮助
node {baseDir}/scripts/run.mjs call convert --help
```

返回 JSON 包含：商品详情 + `comparePriceData`（比价） + `historyPriceData`（历史价）。
服务端 `includeComparePrice` 和 `includeHistoryPrice` 默认 `true`，无需额外传参。

## 路由决策

| 用户意图 | 快捷命令 | 标准调用 | 渲染模板 |
|---------|---------|---------|---------|
| 发链接、问值不值得买、问优惠券、没说意图 | `convert "<链接>"` | `call convert --tpwd "<链接>"` | Read `{baseDir}/references/convert-output.md` |
| 明确说"比价"、"哪家便宜" | `compare-price "<链接>"` | `call compare-price --productIdentifier "<链接>"` | Read `{baseDir}/references/compare-price-output.md` |
| 明确说"历史价"、"价格走势" | — | `call convert --tpwd "<链接>" --includeComparePrice false` | Read `{baseDir}/references/convert-output.md` |

所有命令前缀：`node {baseDir}/scripts/run.mjs`

**默认用 `convert`**，它一次返回商品信息 + 比价 + 历史价全部数据。美团链接（`click.meituan.com`、`dpurl.cn`、`meituan.com`、`imeituan://` 等）同样走 `convert` 路径，数据结构与电商一致。`convert` 支持两个可选参数控制返回内容：
- `--includeComparePrice true/false`（默认 true）
- `--includeHistoryPrice true/false`（默认 true）

历史价路径走 `convert` 而非独立接口，是因为购买建议需要到手价（`finalPrice`）与历史价比较，而独立的历史价接口不返回到手价。

**输出格式**：所有接口支持 `--format json`（默认）或 `--format table`。如果下游 Agent 需要结构化数据而非 Markdown 渲染，直接用 `--format json` 跳过模板渲染。

## 工作流

```
收到链接/口令
  → 输出"正在查询商品信息..."
  → 根据上方路由表调用对应接口
  → 拿到 JSON
  → Read 路由表中对应的渲染模板，按模板输出
```

没有链接时先问用户要。

## 错误处理

接口返回错误时，告知用户具体原因并给建议，不要返回原始 JSON：

| 现象 | 用户可见提示 |
|------|-------------|
| `missing_parameter` | 请发一下商品链接或淘口令 |
| `errorMessage: "未找到相关商品"` | 没找到商品信息，请检查链接是否正确 |
| `topLowestItems` 为空 | 暂无比价数据 |
| `historyPriceData` 不存在 | 暂无历史价格数据 |
| `missing_api_key` | 请设置环境变量 `FX_AI_API_KEY`，从 [feima-lab 开放平台](https://platform.feima.ai/) 登录获取 |
| `api_unavailable` / HTTP 错误 | 服务暂时不可用，请稍后再试 |

## 不适用场景

以下情况**不要**调用本 Skill：
- 快递物流查询
- 汇率换算、天气查询
- 闲鱼/二手交易（无标准价格体系）
- 没有具体商品链接的购物讨论

## 环境依赖

- Node.js 18+（内置 fetch，无需额外依赖）
- 环境变量 `FX_AI_API_KEY`：从 [feima-lab 开放平台](https://platform.feima.ai/) 登录获取
