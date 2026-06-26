# stock-decision Skill - 使用说明

## 快速开始

### 1. 安装
```bash
clawhub install stock-decision
```

### 2. 运行
```bash
openclaw skill run stock-decision
```

### 3. 查看报告
```bash
cat ~/.openclaw/decisions/decision_*.md
```

## 配置

### 环境变量
```bash
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

### 参数配置
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

## 📈 持仓详情
| 代码 | 名称 | 现价 | 成本 | 盈亏% | 操作 |
|------|------|------|------|-------|------|
| 300570 | 太辰光 | 112.51 | 130.34 | -13.68% | 🔴 减仓/止损 |
```

## 常见问题

**Q: 持仓数据从哪里读取？**
A: 从 `~/.openclaw/workspace/SHARED_MEMORY.md` 动态读取

**Q: 如何更新持仓？**
A: 编辑 SHARED_MEMORY.md 中的持仓表格

**Q: 报告保存在哪里？**
A: `~/.openclaw/decisions/decision_YYYYMMDD_HHMMSS.md`

## 作者

- **作者**：富贵儿
- **版本**：1.0.0
- **日期**：2026-04-03
