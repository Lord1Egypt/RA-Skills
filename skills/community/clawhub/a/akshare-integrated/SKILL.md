# AKShare集成选股技能

基于AKShare实时数据的智能选股技能，集成动态权重调整和行业差异化评分。

## 🎯 技能特性

- **实时数据**：集成AKShare获取实时股价
- **智能评分**：三层九维评分系统
- **动态权重**：根据市场趋势调整权重
- **行业差异化**：不同行业不同评分标准
- **风险控制**：完善的风控与失效体系
- **证据分层**：A/B/C/D四级证据体系

## 📦 安装要求

```bash
# 安装AKShare
pip install akshare --upgrade

# 安装依赖
pip install pandas numpy
```


## 🚀 使用方法

### 基本选股

```bash
# 运行选股分析
stock-selector-akshare run

# 使用特定市场
stock-selector-akshare run --market hk

# 指定股票代码
stock-selector-akshare run --symbols 00700,00998,01810
```

### 获取实时数据

```bash
# 获取港股实时数据
stock-selector-akshare data hk 00700

# 获取A股实时数据
stock-selector-akshare data a 000001

# 获取美股实时数据
stock-selector-akshare data us AAPL
```

### 批量查询

```bash
# 批量查询港股
stock-selector-akshare batch hk 00700,00998,01810

# 多市场查询
stock-selector-akshare multi "00700,000001,AAPL"
```

## 🔧 系统架构

### 1. 数据层
- **AKShare接口**：获取实时股票数据
- **数据缓存**：5分钟本地缓存
- **错误处理**：多数据源备选机制

### 2. 评分层
- **价值层** (40%)：基本面、行业位势、估值赔率
- **交易层** (35%)：资金结构、价格形态、量价配合
- **风险层** (25%)：波动风险、事件风险、流动性风险

### 3. 决策层
- **动作决策**：BUY/HOLD/REDUCE/SELL/WATCH
- **仓位建议**：基于评分和风险评估
- **触发条件**：量化的买入/卖出触发点

### 4. 风控层
- **风险边界**：明确的止损/止盈点
- **失效条件**：系统失效的识别标准
- **证据分级**：A/B/C/D四级证据可靠性

## 📊 评分系统

### 价值层 (40分)
1. **基本面质量** (15分)
   - 财务健康度
   - 盈利能力
   - 成长前景

2. **行业位势** (15分)
   - 行业地位
   - 竞争格局
   - 政策支持

3. **估值赔率** (10分)
   - PE/PB/PS估值
   - 历史估值分位数
   - 相对估值优势

### 交易层 (35分)
1. **资金结构** (10分)
   - 主力资金流向
   - 外资持股比例
   - 机构调研热度

2. **裸K形态** (10分)
   - 关键价位突破
   - 技术形态形成
   - 趋势强度

3. **量价配合** (15分)
   - 成交量放大
   - 价格有效性
   - 突破确认

### 风险层 (25分)
1. **波动风险** (10分)
   - 历史波动率
   - 日内波动幅度
   - Beta系数

2. **事件风险** (10分)
   - 重要事件临近
   - 政策风险
   - 行业风险

3. **流动性风险** (5分)
   - 成交量稳定性
   - 买卖价差
   - 市场深度

## 🎯 决策规则

### 动作决策

| 条件 | 动作 |
|------|------|
| 总分 ≥ 85，价值层均衡，形态分 ≥ 8 | **BUY** |
| 总分 ≥ 70，交易层均衡 | **HOLD** |
| 总分 < 70，风险层亮红灯 | **REDUCE** |
| 总分 < 60，且发生风险事件 | **SELL** |
| 其他情况 | **WATCH** |

### 仓位建议

| 评分区间 | 建议仓位 | 理由 |
|----------|----------|------|
| ≥ 90 | 15% | 优秀标的，确定性高 |
| 85-89 | 10% | 良好标的，机会明确 |
| 80-84 | 8% | 机会标的，适度配置 |
| 70-79 | 5% | 观察标的，谨慎配置 |

## ⚠️ 风险控制

### 风险边界
- **止损线**：-8% ~ -12%
- **止盈线**：+20% ~ +30%
- **最大仓位**：单只股票 ≤ 15%
- **总仓位**：激进市场 ≤ 80%，保守市场 ≤ 50%

### 失效条件
1. **系统失效**：连续3次数据获取失败
2. **策略失效**：连续5次推荐亏损
3. **市场失效**：大盘单日跌幅 > 5%
4. **流动性失效**：成交量萎缩 > 50%

## 🔍 使用示例

### 示例1：分析腾讯控股

```bash
stock-selector-akshare run --symbols 00700 --format json
```

**输出:**
```json
{
  "success": true,
  "timestamp": "2026-03-11T04:15:30Z",
  "results": [
    {
      "symbol": "00700",
      "name": "腾讯控股",
      "action": "BUY",
      "total_score": 94,
      "position_suggestion": "7%",
      "real_time_price": 562.500,
      "change_percent": "+0.45%",
      "recommendation": "强烈推荐买入",
      "evidence_level": "A"
    }
  ]
}
```

### 示例2：批量分析港股

```bash
stock-selector-akshare batch hk 00700,00998,01810
```

### 示例3：多市场分析

```bash
stock-selector-akshare multi "00700,000001,AAPL"
```

## 🔄 集成方式

### Python集成

```python
from stock_selector_akshare import AKShareStockSelector

# 创建选择器
selector = AKShareStockSelector()

# 分析单只股票
result = selector.analyze_stock("00700", market="hk")

# 批量分析
results = selector.analyze_batch(["00700", "00998"], market="hk")

# 获取实时数据
real_time_data = selector.get_real_time_data("00700", "hk")
```

### API集成

```bash
# 获取实时数据API
curl "http://localhost:8080/api/stock/00700?market=hk"

# 批量分析API
curl -X POST "http://localhost:8080/api/analyze/batch" \
  -H "Content-Type: application/json" \
  -d '{"symbols":["00700","00998"],"market":"hk"}'
```

## 🚨 注意事项

1. **数据延迟**：免费接口可能有15-30秒延迟
2. **交易时间**：非交易时间返回的数据可能是0
3. **频率限制**：避免频繁调用，建议1秒以上间隔
4. **缓存策略**：默认5分钟缓存，减少API调用
5. **错误处理**：添加重试机制和备用数据源

## 📈 性能优化建议

1. **批量获取**：使用全市场数据API，避免单只股票多次调用
2. **缓存策略**：本地缓存 + 内存缓存组合
3. **异步处理**：使用异步请求提高并发性能
4. **连接复用**：保持HTTP连接复用
5. **数据压缩**：启用数据压缩减少传输量

## 🔧 维护说明

### 日常维护
- 检查AKShare库更新
- 测试数据获取接口
- 验证评分算法有效性

### 故障排查
1. 检查网络连接
2. 验证AKShare安装
3. 查看错误日志
4. 测试备用数据源

### 性能监控
- API响应时间
- 数据获取成功率
- 评分计算耗时
- 内存使用情况

---

**技能状态**：🚀 已集成AKShare  
**版本**：v2.0  
**最后更新**：2026-03-11  
**维护者**：OpenClaw技能库