# cashback

[![ClawHub](https://img.shields.io/badge/ClawHub-cashback-blue)](https://clawhub.ai/fangshan101-coder/cashback)

> 海外品牌官方商城返利助手。粘贴链接生成返利短链、查商家返利比例、看自己的返利订单。

## 安装

```bash
# 先安装公共基础
npx skills install fangshan101-coder/fx-base

# 再安装 cashback
npx skills install fangshan101-coder/cashback
```

> `cashback` 依赖 `fx-base`，两个必须装在同一个 `.claude/skills/` 目录下。

## 配置

使用前需设置 API Key 环境变量：

```bash
export FX_AI_API_KEY="your-api-key"
```

从 [feima-lab 开放平台](https://platform.feima.ai/) 登录获取 API Key。

建议将 `export` 加入 `~/.zshrc` 或 `~/.bashrc` 使其永久生效。

## 核心能力

- **链接转返利短链** — 粘贴支持商家的商品链接，生成带返利追踪的短链和佣金信息
- **商家返利查询** — 问"某商家有没有返利"，返回返利比例和返利入口链接
- **个人订单查询** — 查看近 N 天的返利订单列表、状态和预估返利汇总

## 当前支持商家

| 商家 | 支持地区 | 域名匹配 |
|------|---------|---------|
| **Adidas** | 全球/中国 | `*.adidas.com` / `*.adidas.cn` / `*.adidas.de` / `*.adidas.co.uk` 等 |
| **Space NK NL** | 荷兰 | `*.spacenk.com`（通常含 `/nl/` 路径）|
| **designwebstore DE** | 德国 | `designwebstore.de` |

> 商家清单由多麦联盟后端决定。清单外商家（如 Amazon/Nike/iHerb/eBay/Shein 等）暂未开通返利。

## 使用方式

直接发商品链接或问商家名，无需任何指令：

```
https://www.adidas.com/us/ultraboost-5-shoes/ID8841.html
Adidas 有返利吗
我的返利订单
```

也可以明确意图：

```
帮我生成这个链接的返利短链
Space NK 荷兰站返利多少
查近 7 天的返利订单
```

## 输出示例

### 链接转链

```
### 🌍 Adidas

| 项目 | 详情 |
|------|------|
| 商品 | Ultraboost 5 Shoes |
| 返利 | **最高6%** |
| 商家 | Adidas |

👉 返利链接：https://s.duomai.com/xxx
```

### 商家返利查询

```
### 🏪 Space NK NL

| 项目 | 详情 |
|------|------|
| 返利比例 | **最高8%** |
| 所属地区 | 荷兰 |
| 返利链接 | https://s.duomai.com/xxx |
```

### 订单查询

```
### 📋 近 30 天返利订单

**汇总**：共 3 笔订单，预估返利 **¥82.50**

| 商家 | 订单金额 | 预估返利 | 状态 | 下单时间 |
|------|---------|---------|------|---------|
| Adidas | ¥899.00 | ¥53.94 | 已确认 | 2026-03-25 |
| Space NK NL | €65.00 | €5.20 | 待确认 | 2026-04-01 |
```

## 环境依赖

- Node.js 18+
- 环境变量 `FX_AI_API_KEY`（见上方配置说明）
- 依赖 skill：`fx-base`（提供公共请求层）
