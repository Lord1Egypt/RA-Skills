---
name: stock-decision
description: 从共享记忆读取持仓，生成 A 股投资决策报告（止损/止盈/仓位管理）
version: 1.0.0
author: 富贵儿
tags: ["stock", "investment", "A 股", "量化", "决策"]
---

# stock-decision Skill - A 股投资决策助手

## 功能说明

本 Skill 提供以下功能：

1. **持仓读取** - 从 SHARED_MEMORY.md 动态读取持仓配置
2. **实时价格** - 获取 A 股实时行情数据
3. **买卖信号** - 生成止损/止盈/仓位调整建议
4. **风险预警** - 触及阈值自动预警
5. **报告生成** - 生成 Markdown 格式投资决策报告

## 使用方式

### 命令行调用
```bash
openclaw skill run stock-decision
```

### 配置参数
```bash
openclaw skill config stock-decision --maxPosition 20 --stopLoss -8 --stopProfit 15
```

## 输出示例

```markdown
# 📊 A 股投资决策报告

## 🚨 紧急操作
### 太辰光 (300570) strong_sell
- 操作：减仓/止损
- 理由：触及止损线 (-8.0%)
- 止损价：119.91 元
- 止盈价：149.89 元
```

## 配置说明

### 环境变量
```bash
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

### 参数说明
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `maxPosition` | 20.0 | 单票最大仓位% |
| `stopLoss` | -8.0 | 止损线% |
| `stopProfit` | 15.0 | 止盈线% |

## 依赖

```bash
pip3 install requests
```

## 更新日志

### v1.0.0 (2026-04-03)
- ✅ 初始版本发布
- ✅ 从 SHARED_MEMORY 动态读取持仓
- ✅ 实时价格获取
- ✅ 买卖信号生成

## 支持

- **作者**：富贵儿
- **文档**：https://docs.openclaw.ai
- **社区**：https://discord.com/invite/clawd
