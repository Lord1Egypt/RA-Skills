---
name: "quant-trading"
version: "2.2.0"
description: "AI量化交易系统，8因子信号系统、多数据源容错、实时行情分析"
author: "AI Skills Team"
tags: ["量化", "股票", "交易", "投资", "回测"]
requires: []
---

# AI量化交易技能 v2.2

完整的量化交易系统，提供股票分析、信号生成、回测和实时行情监控。

## 技能描述

V2.2完整版量化交易系统，提供8因子信号系统、多数据源容错（AKShare+Efinance）、实时行情分析（量比/换手率）、筹码分布分析、大盘环境判断和邮件推送通知。

## 使用场景

- 用户："分析贵州茅台" → 返回完整的技术分析报告
- 用户："今天有哪些买入信号？" → 扫描市场返回符合条件的股票
- 用户："回测这个策略" → 运行回测系统返回收益报告
- 用户："大盘环境如何？" → 分析市场环境判断强势/震荡/弱势

## 工具和依赖

### 工具列表

位于 `core/` 和 `modules/` 目录：
- `core/分析流水线.py`：完整分析流程
- `modules/01-多数据源管理器.py`：AKShare+Efinance容错
- `modules/02-大盘环境分析器.py`：市场环境判断
- `modules/03-市场增强分析器.py`：恐慌贪婪指数
- `modules/04-实时行情分析器.py`：量比/换手率/量价关系
- `modules/05-筹码分布分析器.py`：集中度/获利盘/形态识别
- `modules/06-邮件通知器.py`：SMTP邮件推送
- `modules/07-通知中心.py`：多渠道统一接口

### API密钥

**可选**（邮件通知）：
- SMTP邮箱配置

### 外部依赖

- Python 3.7+
- akshare
- efinance
- pandas
- numpy
- smtplib（邮件通知，可选）

## 配置说明

### 安装方法

```bash
cd 12-量化交易V2.2完整版
bash 一键部署脚本.sh
```

### 配置文件

编辑 `config/V2.2配置文件.yaml`：
```yaml
# 数据源配置
data_source:
  primary: akshare
  fallback: efinance

# 信号阈值
thresholds:
  strong_market: 8.5
  normal_market: 9.0
  weak_market: 9.5

# 邮件通知
email:
  enabled: true
  smtp_server: "smtp.qq.com"
  smtp_port: 587
  sender: "your@email.com"
  password: "your-password"
```

## 使用示例

### 场景1：分析单只股票

用户："分析贵州茅台"

AI：
```python
from core.分析流水线 import analyze_stock

result = analyze_stock("600519")
# 返回：
# - 8因子信号评分 (0-10分)
# - 技术指标分析
# - 实时行情分析
# - 筹码分布分析
# - 买入/卖出建议
```

### 场景2：市场扫描

用户："今天有哪些买入信号？"

AI：
```python
from modules.市场扫描器 import scan_market

signals = scan_market(market="A股", threshold=9.0)
# 返回：信号评分 >= 9.0 的股票列表
# 包含股票代码、名称、信号评分、建议
```

### 场景3：大盘环境判断

用户："大盘环境如何？"

AI：
```python
from modules.大盘环境分析器 import MarketAnalyzer

analyzer = MarketAnalyzer()
env = analyzer.analyze_market()
# 返回：
# - 市场环境：强势/震荡/弱势
# - 涨跌家数统计
# - 指数分析
# - 动态阈值建议
```

### 场景4：运行回测

用户："回测这个策略"

AI：
```python
from tests.完整回测系统 import run_backtest

results = run_backtest(
    start_date="2023-01-01",
    end_date="2024-12-31",
    initial_capital=100000
)
# 返回：
# - 总收益率
# - 年化收益率
# - 最大回撤
# - 夏普比率
# - 交易明细
```

### 场景5：实时监控

用户："监控我的自选股"

AI：
```python
from modules.实时监控器 import monitor_stocks

stocks = ["600519", "000858", "002475"]
monitor_stocks(stocks, interval=300)
# 每5分钟检查一次
# 有信号时发送邮件通知
```

## 8因子信号系统

```python
因子权重分配:
• 动量指标 (Momentum)     - 25%
• 均线偏离 (MA Deviation) - 20%
• 成交量 (Volume)         - 15%
• 波动率 (Volatility)     - 10%
• MACD                     - 10%
• 布林带 (Bollinger)       - 10%
• 实时量比 (Volume Ratio) - 5%  [V2.2新增]
• 筹码集中度 (Chip)       - 5%  [V2.2新增]
```

## 动态买入阈值

```python
强势市场: 信号 ≥ 8.5分
震荡市场: 信号 ≥ 9.0分
弱势市场: 信号 ≥ 9.5分
```

## 系统特色

### 1. 多数据源容错

- 主数据源：AKShare
- 备用源：Efinance
- 自动故障切换
- 熔断机制（3次失败=5分钟冷却）

### 2. 实时行情分析

- 量比5级分析（极度缩量~巨量）
- 换手率5级分析（死寂~高换手）
- 量价关系分析
- 信号评分（0-10分）

### 3. 筹码分布分析

- 价格分布计算
- 90%/70%集中度
- 获利盘比例
- 形态识别（单峰/双峰/多峰/吸筹/派发）
- 支撑压力位

### 4. 大盘环境判断

- 市场环境分类（强势/震荡/弱势）
- 动态阈值调整
- 涨跌家数统计
- 指数分析

### 5. 邮件推送通知

- 买入信号推送
- 卖出信号推送
- 风险警报推送
- 每日汇总报告

### 6. 通知中心

- 多渠道整合（邮件/微信/飞书/Telegram/钉钉）
- 优先级管理（低/普通/高/紧急）
- 失败重试机制
- 消息队列
- 频率控制

## 故障排除

### 问题1：数据获取失败

**解决**：
1. 检查网络连接
2. 系统会自动切换到备用数据源
3. 如仍失败，等待5分钟后重试（熔断机制）

### 问题2：邮件通知失败

**解决**：
1. 检查SMTP配置
2. 确认邮箱授权码正确
3. 检查网络连接
4. 查看日志获取详细错误

### 问题3：回测结果异常

**解决**：
1. 检查数据完整性
2. 确认日期范围正确
3. 验证初始资金设置
4. 查看交易明细定位问题

## 文档阅读顺序

### 新手入门

1. `docs/V2.2完整部署与使用指南.md` - 了解如何部署和使用
2. `docs/V2.2快速实施指南.md` - 了解分阶段实施方案
3. `tests/系统测试脚本.py` - 运行测试验证系统
4. `tests/完整回测系统.py` - 运行回测查看效果

### 进阶使用

5. `docs/V2.2集成架构设计.md` - 深入了解系统架构
6. `core/分析流水线.py` - 学习如何使用分析流水线
7. `modules/` - 各个模块的源代码

## 注意事项

1. **投资风险**：本系统仅供参考，不构成投资建议
2. **数据延迟**：可能有15-20分钟延迟
3. **零成本运行**：使用免费数据源，无需API费用
4. **邮件配置**：邮件通知为可选功能
5. **合规使用**：遵守相关法律法规，不得用于非法用途
