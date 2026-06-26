---
name: binance-earning-assistant
description: 币安撸毛助手 - 展示币安最新撸毛活动信息，包括理财产品、活动奖励、空投预告等。Use when user asks for "今日撸毛", "币安活动", "赚钱活动", "撸毛信息", "Binance earning", "airdrop info", or any query about Binance promotional events, rewards, or earning opportunities.
metadata:
  version: 2.0.1
  author: 0x_WanG
  license: MIT
  openclaw:
    emoji: "💰"
    always: false
dependencies:
  - requests
environment:
  - HTTP_PROXY (可选) - HTTP 代理地址，例如 http://127.0.0.1:26001
  - OPENCLAW_WORKSPACE (可选) - OpenClaw 工作区路径，默认 ~/.openclaw/workspace
triggers:
  - "今日撸毛"
  - "今日撸毛信息"
  - "币安活动"
  - "币安撸毛"
  - "赚钱活动"
  - "撸毛信息"
  - "Binance earning"
  - "airdrop info"
  - "binance rewards"
  - "币安理财"
  - "币安空投"
persistence:
  - 创建 ~/.openclaw/workspace/.binance_earning 目录
  - 存储导出文件 (exports/*.md)
---

# 币安撸毛助手

展示币安最新撸毛活动信息，包括理财产品、活动奖励、空投预告等。

## 功能特性

- ✅ **实时获取** - 从币安 API 实时获取最新活动
- ✅ **智能过滤** - 自动过滤非华语区活动
- ✅ **分类展示** - 理财、活动奖励、广场任务
- ✅ **详细信息** - 代币、奖池、截止日期、发布时间
- ✅ **Alpha 空投** - 实时获取 alpha123.uk 空投数据

## 使用方法

### 查看活动信息

```bash
python3 summary_table.py
```

## 输出格式

活动列表包含以下信息：

- **序号** - 活动编号
- **代币** - 活动相关代币
- **奖池/APR** - 奖励金额或年化收益率
- **活动名称** - 活动中文名称
- **发布** - 发布日期
- **截止** - 截止日期

## 活动分类

| 分类 | 说明 |
|------|------|
| 💰 理财产品 | 币安理财产品，包括活期、定期 |
| 🎁 活动奖励 | 交易竞赛、奖励活动 |
| 📢 其他活动 | 知识问答等其他活动 |
| 🚀 ALPHA 空投预告 | Alpha 板块空投预告 |

## 依赖说明

**必需依赖：**
- `requests` - 用于 HTTP 请求

## 持久化说明

**技能会创建以下目录和文件：**
- `$OPENCLAW_WORKSPACE/.binance_earning/` - 数据目录（默认 `~/.openclaw/workspace/.binance_earning/`）
  - `exports/` - 导出的 Markdown 文件

**环境变量说明：**
- `OPENCLAW_WORKSPACE` - 指定工作区路径（可选，默认 `~/.openclaw/workspace`）
- `HTTP_PROXY` - 指定 HTTP 代理（可选，某些网络环境需要）

## 示例输出

```
════════════════════════════════════════
🚀 币安撸毛助手 - 当前可参与活动总览
════════════════════════════════════════
更新时间：2026-03-14 20:42
活动总数：18 个

════════════════════════════════════════
💰 理财产品（8 个）
════════════════════════════════════════

【1】Enjoy Up to 8% APR with RLUSD Flexib...
 🔗 链接：https://www.binance.com/zh-CN/support/announcement/65317d61d1c445f99f73a04c05233dd2
 💰 奖池：8%
 📅 截止时间：2026-03-31
 🎯 门槛：无特殊要求
 📝 参与方式：1.打开理财 2.选择产品 3.申购确认
 ⚠️ 风险：理财非存款，产品有风险
```

## 注意事项

1. 活动信息可能随时变更，请以官方页面为准
2. 空投有风险，参与需谨慎
3. 理财非存款，产品有风险

## 更新日志

### v2.0.1 (2026-03-24) - Clawhub 安全审查修复

- ✅ 移除：未声明的 LLM fallback（bailian 客户端调用）
- ✅ 修复：硬编码用户路径 `/Users/pigbaby/...` → 使用环境变量 `OPENCLAW_WORKSPACE`
- ✅ 修复：硬编码代理设置 → 改为从环境变量 `HTTP_PROXY` 读取（可选）
- ✅ 新增：SKILL.md 中声明环境变量（HTTP_PROXY, OPENCLAW_WORKSPACE）
- ✅ 优化：所有脚本统一使用环境变量配置，兼容不同运行环境

### v1.0.7 (2026-03-16)

- ✅ 新增：实时 API 获取活动列表（币安官方 API）
- ✅ 新增：活动名称中文化映射
- ✅ 新增：表格形式首次回复（简洁展示）
- ✅ 新增：详情查询功能（回复序号查看）
- ✅ 新增：自动计算剩余天数
- ✅ 新增：紧急提醒（今天/明天截止高亮）
- ✅ 新增：触发词自动响应（"今日撸毛"等）
- ✅ 优化：过期活动自动过滤
- ✅ 优化：按剩余天数排序
- ✅ 修复：截止日期核实问题

### v1.0.6 (2026-03-15)

- ✅ 新增：触发词支持
- ✅ 新增：OpenClaw 自动响应配置

### v1.0.5 (2026-03-14)

- ✅ 修复：文档与实际功能保持一致
- ✅ 修复：删除未实现的 API 获取描述
- ✅ 简化：只保留实际实现的功能

### v1.0.4 (2026-03-14)

- ✅ 删除：Telegram/钉钉通知功能描述
- ✅ 删除：OCR 功能描述

### v1.0.3 (2026-03-14)

- ✅ 添加：环境变量声明
- ✅ 添加：依赖声明
- ✅ 添加：持久化说明

### v1.0.2 (2026-03-14)

- ✅ 初始版本发布
- ✅ 支持分类展示
- ✅ 支持详细信息展示
- ✅ 支持导出 Markdown
