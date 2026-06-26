---
name: cashback
description: 海外品牌官方商城返利（cashback）助手。通过多麦联盟渠道，为指定海外商家的购物订单提供返利查询与转链服务，三个能力：粘贴商品链接生成返利短链、查询商家返利比例、查看个人返利订单。当前仅支持 Adidas、Space NK NL（荷兰站）、designwebstore DE（德国站）三家，不在清单中的海外商家暂未开通。当用户发来这三家商家的商品链接，或提到"Adidas/阿迪达斯返利"、"Space NK 返利"、"designwebstore 返利"、"cashback"、"海淘返利"、"我的返利订单"时使用。不适用于：清单外的任何商家（包括 Amazon/Nike/iHerb/eBay/Shein 等）、快递查询、汇率换算。
version: 1.2.2
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

# 海外购物返利助手

3 个能力覆盖海外购物返利全流程：粘贴链接转链 → 搜商家问返利 → 查返利订单。

## 当前支持商家

| 商家名（`--store` 参数必须用此值）| 支持地区 | 域名匹配 | 用户可能的叫法 |
|---|---|---|---|
| `Adidas` | 全球/中国 | `*.adidas.com` / `*.adidas.cn` / `*.adidas.de` / `*.adidas.co.uk` 等所有 adidas 官方域名 | 阿迪达斯 / 阿迪 / adidas / Adidas |
| `Space NK NL` | 荷兰 | `*.spacenk.com`（通常含 `/nl/` 或 `/en_NL/` 路径）| space nk / spacenk / Space NK 荷兰站 |
| `designwebstore DE` | 德国 | `designwebstore.de` | designwebstore / design web store / designwebstore 德国站 |

> **重要**：商家清单由多麦联盟后端决定，**不在上表中的商家一律不支持**（包括 Amazon、Nike、iHerb、eBay、Shein 等）。用户问清单外商家时直接告知暂不支持，**不要调 API 硬查**。
>
> **商家名映射**：用户口头叫法（如"阿迪达斯"）必须先映射到左列的精确值（`Adidas`）再传给 `--store` 参数，否则 API 会返回 `store_not_found`。

## 前置条件

- 环境变量 `FX_AI_API_KEY`：从 [feima-lab 开放平台](https://platform.feima.ai/) 登录获取。未设置时脚本会返回 `missing_api_key` 错误
- **数据流向**：用户提供的链接和查询会被发送到 `https://api-ai-brain.fenxianglife.com` 处理，请确保信任该服务后再使用

## 快速开始

```bash
# 快捷命令（推荐，Claude 默认用这组）
node {baseDir}/scripts/run.mjs convert "https://www.adidas.com/us/ultraboost-5-shoes/ID8841.html"
node {baseDir}/scripts/run.mjs store "Adidas"
node {baseDir}/scripts/run.mjs orders

# 等价的标准调用（开发者调试用）
node {baseDir}/scripts/run.mjs call link-convert --url "<URL>"
node {baseDir}/scripts/run.mjs call store-rebate --store "Space NK NL"
node {baseDir}/scripts/run.mjs call order-query --days 30
```

## 路由决策

| 用户意图 | 命令 | 渲染模板 |
|---------|------|---------|
| 发商品链接、要返利链接 | `run.mjs convert "<URL>"` | Read `{baseDir}/references/link-convert-output.md` |
| 问某商家有没有返利、返利多少 | `run.mjs store "<精确商家名>"` | Read `{baseDir}/references/store-rebate-output.md` |
| 查我的返利、我的订单 | `run.mjs orders` 或 `run.mjs orders --days N` | Read `{baseDir}/references/order-query-output.md` |

## 链接归属判断

调用接口前，**必须**先用域名/商家名判断是否在服务范围，避免无效 API 调用：

| 输入类型 | 判断依据 | 动作 |
|---------|---------|------|
| 商品链接 | 域名匹配「支持商家表」的"域名匹配"列 | 调用 `convert` |
| 商品链接 | 域名**不匹配**表中任何商家 | **不调 API**，告知"该商家暂未开通返利，目前仅支持 Adidas、Space NK NL、designwebstore DE 三家" |
| 商家名 | 对照"用户可能的叫法"列，能映射到精确商家名 | 用映射后的值调用 `store` |
| 商家名 | 无法映射到上表任何商家 | **不调 API**，告知同上 |
| 查订单 | 直接调用，无需判断 | 调用 `orders` |

## 工作流

多接口 skill 必须**渐进式输出**——先告诉用户"正在查询"，不要等到 API 返回才出声：

```
Step 1 立即输出："正在查询 {商家名/订单/链接}..."（不等 API 返回）
  ↓
Step 2 判断链接/商家是否在服务范围（见"链接归属判断"）
  ↓  不在  → 告知不支持并结束
  ↓  在    → 继续
Step 3 调用对应接口（见"路由决策"）
  ↓
Step 4 拿到 JSON，Read 对应渲染模板，输出结果
  ↓
Step 5 用户继续追问 → 回到 Step 1
```

没有链接时先问用户要。

## 错误处理

| 现象 | 用户可见提示 | 兜底动作 |
|------|-------------|---------|
| 用户发清单外商家的链接或名字 | "该商家暂未开通返利，目前仅支持 Adidas、Space NK NL、designwebstore DE 三家" | **不调 API**，直接回复 |
| `store_not_found`（清单内商家名拼错）| "没找到该商家，商家名应为：Adidas / Space NK NL / designwebstore DE" | 用精确名称重试；若用户同时给了链接，改走 `convert` |
| `no_available_plan` | "该商家暂无可用返利计划" | 告知可能是临时下线，建议稍后重试 |
| `no_orders` | "近 {days} 天暂无返利订单" | 提示"通过返利链接购物后，订单通常需要 1-3 天才会出现" |
| `api_unavailable` / HTTP 错误 | "服务暂时不可用，请稍后重试" | 建议 1 分钟后重试 |
| `missing_api_key` | "请设置环境变量 `FX_AI_API_KEY`" | 给出 [feima-lab 开放平台](https://platform.feima.ai/) 链接 |
| `missing_parameter` | "请发一下商品链接 / 请告诉我要查哪个商家" | 引导用户补充参数 |

## 不适用场景

以下情况**不要**调用本 Skill：
- 清单外的任何海外商家（Amazon/Nike/iHerb/eBay/Shein 等）
- 国内电商（淘宝/京东/拼多多/抖音/唯品会/美团等）
- 快递物流查询
- 汇率换算、天气查询

## 兼容性

- Claude Code / Claude.ai / OpenClaw 本地节点
- Node.js 18+（内置 fetch，无额外依赖）
- 脚本路径解析基于 `import.meta.url`，支持 symlink 安装

## 环境依赖

- Node.js 18+
- 环境变量 `FX_AI_API_KEY`：从 [feima-lab 开放平台](https://platform.feima.ai/) 登录获取
