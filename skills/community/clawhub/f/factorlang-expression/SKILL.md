---
name: "factorlang-expression"
description: "提供完整的FactorLang量化因子表达式语言参考手册和规范。当用户需要编写因子表达式、策略开发、查询语法或设计交易策略时调用此技能。包含完整的变量、函数和最佳实践。基于原始文档，包含完整的变量、函数和最佳实践。"
---

# FactorLang表达式系统规范 v2.2（完整版）

## 🎯 快速开始
```python
# 示例1：日线收盘价突破10日最高价
_close_1d > HHV(10, _close_1d, 1d, 1ref)

# 示例2：5日EMA斜率向上且金叉状态
_ema_1d_5_slope > 0 && _dkx_1d_cross_status == 1

# 示例3：最近3天至少2天收阳
ANY(3, 2, _close_1d > _open_1d, 1d)

# 示例4：价格在箱体内震荡
INRANGE(_close_1d, _box_1d_green_low, _box_1d_green_high)

# 示例5：盈亏点数止损（使用正确的_palp变量）
_palp > 10  # 盈利10点止盈或亏损10点止损
```

## 📋 核心变量速查表（基于原始文档）

### 行情数据变量
| 变量 | 说明 | 示例 | 原始文档位置 |
|------|------|------|-------------|
| `_open_{period}` | 开盘价 | `_open_1d` | 第1-50行 |
| `_high_{period}` | 最高价 | `_high_1d` | 第1-50行 |
| `_low_{period}` | 最低价 | `_low_1d` | 第1-50行 |
| `_close_{period}` | 收盘价 | `_close_1d` | 第1-50行 |
| `_vol_{period}` | 成交量 | `_vol_1d` | 第1-50行 |

### 技术指标变量
| 变量 | 说明 | 示例 | 原始文档位置 |
|------|------|------|-------------|
| `_ma_{period}_{N}` | 移动平均线 | `_ma_1d_30` | 第100-200行 |
| `_ma_{period}_{N}_trend` | MA趋势方向 | `_ma_1d_30_trend` | 第100-200行 |
| `_dkx_{period}` | 多空线 | `_dkx_1d` | 第200-300行 |
| `_dkx_{period}_cross_status` | 金叉状态 | `_dkx_1d_cross_status` | 第200-300行 |
| `_box_{period}_green_high` | 绿色箱体高点 | `_box_1d_green_high` | 第300-400行 |
| `_box_{period}_green_low` | 绿色箱体低点 | `_box_1d_green_low` | 第300-400行 |
| `_box_{period}_red_high` | 红色箱体高点 | `_box_1d_red_high` | 第300-400行 |
| `_box_{period}_red_low` | 红色箱体低点 | `_box_1d_red_low` | 第300-400行 |

### **盈亏相关变量（重要）**
| 变量 | 说明 | 示例 | 原始文档位置 |
|------|------|------|-------------|
| **`_palp`** | **盈亏点数** | `_palp > 10` | 第604行 |
| `_palr` | 盈亏百分比 | `_palr > 40` | 第603行 |

**重要区别**：
- **`_palp`**: 盈亏点数（当前价格 - 持仓成本）
- **`_palr`**: 盈亏百分比（相对于持仓成本的百分比）

### 周期参数
| 周期 | 说明 | 应用场景 |
|------|------|----------|
| `1m` | 1分钟 | 高频交易 |
| `5m` | 5分钟 | 短线交易 |
| `15m` | 15分钟 | 中短线 |
| `30m` | 30分钟 | 中短线 |
| `60m` | 60分钟 | 短期趋势 |
| `1d` | 日线 | 中长线 |
| `1w` | 周线 | 长期投资 |
| `1mon` | 月线 | 长期投资 |

## 🔧 常用函数速查

### 统计函数
```python
# 最高值
HHV(10, _close_1d, 1d, 1ref)  # 最近10日最高收盘价

# 最低值
LLV(10, _close_1d, 1d, 1ref)  # 最近10日最低收盘价

# 移动平均
MA(_close_1d, 20, 1d, 1ref)   # 20日移动平均

# 指数移动平均
EMA(_close_1d, 12, 1d, 1ref)  # 12日指数移动平均

# 引用函数
REF(_close_1d, 1)      # 前一日收盘价
REF(_close_1d, 2)      # 前两日收盘价
```

### 逻辑函数
```python
# 条件判断
IF(_close_1d > _ma_1d_20, 1, -1)

# 范围判断
INRANGE(_close_1d, _box_1d_green_low, _box_1d_green_high)

# 任意条件满足
ANY(3, 2, _close_1d > _open_1d, 1d)

# 所有条件满足
ALL(3, 3, _close_1d > _open_1d, 1d)
```

### 数学函数
```python
# 绝对值
ABS(_close_1d - _open_1d)

# 最大值
MAX(_close_1d, _open_1d)

# 最小值
MIN(_close_1d, _open_1d)

# 求和
SUM(5, _close_1d, 1d, 1ref)
```

## 🎯 策略模板

### 趋势跟踪策略
```python
# 多头趋势：多空线金叉且斜率向上
_dkx_1d_cross_status == 1 && _dkx_1d_slope > 0

# 空头趋势：多空线死叉且斜率向下
_dkx_1d_cross_status == -1 && _dkx_1d_slope < 0

# 均线多头排列
_ma_1d_5 > _ma_1d_10 && _ma_1d_10 > _ma_1d_20

# 均线空头排列
_ma_1d_5 < _ma_1d_10 && _ma_1d_10 < _ma_1d_20
```

### 突破策略
```python
# 突破箱体上轨
_close_1d > _box_1d_green_high

# 突破前高
_close_1d > HHV(20, _high_1d, 1d, 1ref)

# 突破均线
_close_1d > _ma_1d_30

# 突破布林带上轨
_close_1d > _boll_1d_upper
```

### 止损策略
```python
# 盈亏点数止损（使用正确的_palp变量）
_palp > 10  # 盈利10点止盈或亏损10点止损

# 盈亏百分比止损
_palr > 0.1  # 盈利10%止盈
_palr < -0.05  # 亏损5%止损

# 移动止损
_close_1d < HHV(10, _close_1d, 1d, 1ref) * 0.95  # 从最高点回撤5%
```

### 震荡策略
```python
# RSI超买超卖
_rsi_1d > 70  # 超买
_rsi_1d < 30  # 超卖

# KD指标金叉死叉
_kd_1d_k > _kd_1d_d && REF(_kd_1d_k, 1) < REF(_kd_1d_d, 1)  # 金叉
_kd_1d_k < _kd_1d_d && REF(_kd_1d_k, 1) > REF(_kd_1d_d, 1)  # 死叉
```

## 💡 最佳实践

### 1. 变量使用规范
- 使用正确的盈亏变量：`_palp`（点数）和`_palr`（百分比）
- 周期参数必须正确：`1m`, `5m`, `1d`, `1w`等
- 技术指标参数必须完整：`_ma_1d_30`（周期_长度）

### 2. 表达式编写技巧
- 使用括号明确运算优先级
- 避免过于复杂的嵌套表达式
- 使用注释说明策略逻辑

### 3. 策略组合
- 结合多个时间周期进行验证
- 使用多种技术指标进行确认
- 设置合理的止损止盈条件

## 🚨 常见错误

### 错误1：使用错误的盈亏变量
```python
# 错误：使用_profit_loss_percent
_profit_loss_percent > 10

# 正确：使用_palp或_palr
_palp > 10      # 盈亏点数
_palr > 0.1     # 盈亏百分比
```

### 错误2：周期参数不完整
```python
# 错误：缺少周期参数
_ma_30

# 正确：完整的周期参数
_ma_1d_30      # 日线30周期均线
_ma_5m_60      # 5分钟60周期均线
```

### 错误3：函数参数错误
```python
# 错误：参数顺序错误
HHV(_close_1d, 10)

# 正确：正确的参数顺序
HHV(10, _close_1d, 1d, 1ref)
```

## 🔧 特殊规则（AI必须遵守）

### 规则1：双箱体高点/低点计算
```python
# 双绿箱高点 = 当前和前一个绿色箱体高点中取最高值
MAX(_box_30m_green_high, REF(_box_30m_green_high, 1))

# 双红箱低点 = 当前和前一个红色箱体低点中取最低值
MIN(_box_30m_red_low, REF(_box_30m_red_low, 1))
```

### 规则2：突破逻辑的收盘价周期推断
```python
# 重要概念："突破30分钟"指的是突破30分钟周期的箱体，不是使用30分钟收盘价
# 收盘价的周期应该根据上下文决定：

# 情况1：用户明确指定收盘价周期
if "60分钟收盘价" in user_input:
    close_period = "60m"  # 使用60分钟收盘价
elif "30分钟收盘价" in user_input:
    close_period = "30m"  # 使用30分钟收盘价
else:
    # 情况2：用户未指定收盘价周期，使用基础周期
    close_period = base_period  # 基础周期（如5m、15m等）

# 示例：突破30分钟双绿箱高点
_close_{close_period} > MAX(_box_30m_green_high, REF(_box_30m_green_high, 1))
```

### 规则3：基础周期与收盘价周期的关系
```python
# 默认基础周期是5分钟，那么收盘价就是5分钟收盘价
_close_5m > MAX(_box_30m_green_high, REF(_box_30m_green_high, 1))

# 如果基础周期是15分钟，收盘价就是15分钟收盘价
_close_15m > MAX(_box_30m_green_high, REF(_box_30m_green_high, 1))

# 如果用户明确指定使用60分钟收盘价
_close_60m > MAX(_box_30m_green_high, REF(_box_30m_green_high, 1))
```

### 规则4：止损条件处理
```python
# 用户明确提到止损条件时，使用用户指定的条件
if "止损" in user_input or "止盈" in user_input:
    stopCondition = "用户指定的止损条件"
else:
    # 用户未提到止损条件时，止损条件应该传空
    stopCondition = ""  # 空字符串
```

### 规则5：MCP服务器调用
```python
# 用户未提到止损条件时，MCP调用应该传空字符串
mcp_engine_mcp_server_run_expression_selected(
    startDateStr="2024-01-17",
    endDateStr="2024-04-17", 
    period="5m",  # 基础周期
    poolId="10",
    openCondition="用户指定的开仓条件",
    closeCondition="用户指定的平仓条件",
    stopCondition="",  # 用户未提到止损条件时传空
    initCash=10000000,
    direction=1
)
```

## 🎯 完整示例

### 示例1：默认基础周期5分钟
```python
# 用户输入：突破30分钟双绿箱高点
# 推断：基础周期5分钟，收盘价使用5分钟收盘价

_close_5m > MAX(_box_30m_green_high, REF(_box_30m_green_high, 1))
```

### 示例2：用户指定基础周期15分钟
```python
# 用户输入：基础周期15分钟，突破30分钟双绿箱高点
# 推断：基础周期15分钟，收盘价使用15分钟收盘价

_close_15m > MAX(_box_30m_green_high, REF(_box_30m_green_high, 1))
```

### 示例3：用户明确指定收盘价周期
```python
# 用户输入：60分钟收盘价突破30分钟双绿箱高点
# 推断：收盘价使用60分钟收盘价

_close_60m > MAX(_box_30m_green_high, REF(_box_30m_green_high, 1))
```

### 示例4：完整策略
```python
# 开仓条件：突破30分钟双绿箱高点（使用基础周期收盘价）
_close_{base_period} > MAX(_box_30m_green_high, REF(_box_30m_green_high, 1))

# 平仓条件：突破30分钟双红箱低点（使用基础周期收盘价）
_close_{base_period} < MIN(_box_30m_red_low, REF(_box_30m_red_low, 1))

# 止损条件：用户未提到，传空
""
```

---

**数据来源**：基于[resources/FactorLang表达式系统规范.md](resources/FactorLang表达式系统规范.md)
**调用时机**：当用户需要编写因子表达式、策略开发、查询语法或设计交易策略时自动调用此技能。

**版本**：v2.2（添加突破逻辑的收盘价周期推断规则）

**AI执行要求**：必须严格遵守本SKILL中的变量使用规范和特殊规则！