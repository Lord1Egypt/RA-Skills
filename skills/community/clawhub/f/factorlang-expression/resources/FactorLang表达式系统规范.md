# FactorLang表达式系统规范 v1.0
## 量化因子表达式语言参考手册
### —— 策略开发、因子计算、信号生成

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
```

## 1. 语法规范
### 1.1 运算符
| 类别 | 运算符 | 说明 | 示例 |
|------|--------|------|------|
| **逻辑运算** | `&&` | 逻辑AND | `a > b && c < d` |
|  | `\|\|` | 逻辑OR | `a > b \|\| c < d` |
| **比较运算** | `>` | 大于 | `_close_1d > _open_1d` |
|  | `>=` | 大于等于 | `_close_1d >= 10` |
|  | `<` | 小于 | `_close_1d < _ma_1d_20` |
|  | `<=` | 小于等于 | `_volume_1d <= 1000000` |
|  | `==` | 等于 | `_dkx_1d_cross_status == 1` |
|  | `!=` | 不等于 | `_close_1d != REF(_close_1d, 1)` |
| **算术运算** | `+` | 加 | `_close_1d + 1.5` |
|  | `-` | 减 | `_close_1d - _open_1d` |
|  | `*` | 乘 | `_volume_1d * 1.5` |
|  | `/` | 除 | `(_close_1d - _open_1d) / _open_1d` |
|  | `%` | 取余 | `_barpos_1d % 5 == 0` |

### 1.2 运算符优先级
| 优先级 | 运算符 | 说明 | 结合性 |
|--------|--------|------|--------|
| 1 | `()` | 括号 | 从左到右 |
| 2 | `!` | 逻辑非 | 从右到左 |
| 3 | `*` `/` `%` | 乘、除、取余 | 从左到右 |
| 4 | `+` `-` | 加、减 | 从左到右 |
| 5 | `<` `<=` `>` `>=` | 比较运算符 | 从左到右 |
| 6 | `==` `!=` | 相等性比较 | 从左到右 |
| 7 | `&&` | 逻辑与 | 从左到右 |
| 8 | `\|\|` | 逻辑或 | 从左到右 |

### 1.3 数据类型

**数据类型说明**：
- 当前所有的类型都转为float类型参与计算和返回

## 2. 核心概念
### 2.1 周期参数
| 参数 | 含义 | 应用场景 | 示例 |
|------|------|----------|------|
| `1m` | 1分钟周期 | 高频交易、日内策略 | `_close_1m`, `High(5m)` |
| `5m` | 5分钟周期 | 短线交易 | `_volume_5m`, `_ma_5m_20` |
| `10m` | 10分钟周期 | 日内波段 | `_close_10m` |
| `15m` | 15分钟周期 | 日内趋势 | `_ema_15m_12` |
| `30m` | 30分钟周期 | 中短线交易 | `_close_30m`, `_dkx_30m` |
| `60m` | 60分钟周期 | 短期趋势 | `_ma_60m_20` |
| `1d` | 日线周期 | 中长线策略 | `_close_1d`, `_box_1d_green_high` |
| `1w` | 周线周期 | 长期投资 | `_close_1w`, `_ma_1w_20` |
| `1mon` | 月线周期 | 超长期分析 | `Open(1mon)` |

**格式说明**：
- `{period}` ：此格式代表周期变量，实际使用请用以上参数代替,比如，1m代表说明是1分钟周期。

### 2.2 引用
```python
# 方式1：REF函数引用
REF(_close_1d, 1)      # 前一日收盘价
REF(_ma_1d_20, 2)      # 前两日的20日均线
REF(_dkx_1d_cross_status, 1)  # 前一日的金叉状态

# 方式2：后缀引用参数
_close_1d_1ref         # 同 REF(_close_1d, 1) - 前一日收盘价
_ma_1d_20_2ref         # 同 REF(_ma_1d_20, 2) - 前两日20日均线
_dkx_1d_0ref           # 当前值，同 _dkx_1d

# 方式3：函数参数引用
Close(1d, 1ref)        # 前一日收盘价
High(5m, 2ref)         # 前两根5分钟K线的最高价
LLV(10, _close_1d, 1d, 1ref)  # 昨日计算的最近10日最低收盘价
```

**引用参数说明**：
- `0ref` 或 不写：当前值
- `1ref`：前一个值
- `2ref`：前两个值
- 以此类推

**格式说明**：
- `{ref}` ：此格式代表引用变量，实际使用请用具体参数代替，比如，1ref代替说明是前一个。

### 2.3 斜率
**斜率计算说明**：
- 使用**线性回归**计算最近N个周期的斜率
- 默认**N=3**，即使用最近3个数据点计算斜率
- 线性回归公式：**y=a+bx**，其中**b**为斜率

**标准化斜率**：
- 默认使用（相对于ATR)：**斜率*10/atr**

#### 2.3.1 方向定义
- 斜率 > 0：指标向上
- 斜率 = 0：指标水平
- 斜率 < 0：指标向下

#### 2.3.2 趋势判断
- 标准化斜率 > 0.05：趋势向上
- 标准化斜率 < -0.05：趋势向下
- 其他：趋势水平

**默认区间边界值**： **-0.05 ~ 0.05**

#### 2.3.2 其他概念定义
- **趋势（Trend）**：价格或指标在一段时间内持续朝某个方向运动的**倾向**。
- **拐点（Turning Point）**：趋势方向发生改变的转折点，即从上涨转为下跌或从下跌转为上涨的**临界位置**。
- **叉点（Crossover Point）**：两条指标线**相交的点**，代表技术信号可能发生变化的位置。
- **多空线金叉（DKX Golden Cross）**：多空线**上穿**其均线，为买入信号。
- **多空线死叉（DKX Death Cross）**：多空线**下穿**其均线，为卖出信号。
- **均线快线（Fast Moving Average）**：**较短周期**的移动平均线，对价格变化反应更敏感。
- **均线慢线（Slow Moving Average）**：**较长周期**的移动平均线，反映更长期的价格趋势。

### 2.4 命名规范
- 内置变量命名， 以 `_`开头， 并且以`_`连接字母或数字， 建议：全小写
- 函数命名，建议：全大写。注意：**当前函数不区分大小写**
- 因子命名，建议：以 `factor_`开头，全小写
- 周期变量命名参考 `2.1 周期参数`；引用变量命名参考 `2.2 引用`
- 其他变量命名：斜率命名 `slope`；趋势命名`trend`；拐点命名`turn`；叉点命名`cross`；金叉命名`cross_golden`；死叉命名`cross_dead`；点命名`point`；位置命名`pos`

## 3. 内置变量
### 3.1 行情数据
| 变量 |  说明 | 等效函数 | 示例 |
|------|------|----------|------|
| `_open_{period}` | 开盘价 | `Open({period})` | `_open_1d`, `Open(1d)` |
| `_open_{period}_{ref}` | 开盘价 | `Open({period}, {ref})` | `_open_1d_1ref`, `Open(1d, 1ref)`, `REF(_high_1d, 1)` |
| `_high_{period}` | 最高价 | `High({period})` | `_high_1w`, `High(1w)` |
| `_high_{period}_{ref}` | 最高价 | `High({period}, {ref})` | `_high_1w_1ref`, `High(1w, 1ref)`, `REF(_high_1w, 1)`|
| `_low_{period}` | 最低价 | `Low({period})` | `_low_30m`, `Low(30m)` |
| `_low_{period}_{ref}` | 最低价 | `Low({period},{ref})` | `_low_30m_1ref`, `Low(30m, 1ref)`, `REF(_low_30m, 1)` |
| `_close_{period}` | 收盘价 | `Close({period})` | `_close_1mon`, `Close(1mon)` |
| `_close_{period}_{ref}` | 收盘价 | `Close({period},{ref})` | `_close_1mon_1ref`, `Close(1mon, 1ref)`, `REF(_close_1mon, 1)` |
| `_vol_{period}` | 交易量 | `Vol({period})` | `_vol_1mon`, `Vol(1mon)` |
| `_vol_{period}_{ref}` | 交易量 | `Vol({period},{ref})` | `_vol_1mon_1ref`, `Vol(1mon, 1ref)`, `REF(_vol_1mon, 1)` |
| `_barpos_{period}` | K线位置（从1开始） | `BarPos({period})` | `_barpos_5m`, `BarPos(5m)` |
| `_barpos_{period}_{ref}` | K线位置（从1开始） | `BarPos({period},{ref})` | `_barpos_5m_1ref`, `BarPos(5m, 1ref)`, `REF(_barpos_5m, 1)` |

### 3.2 技术指标变量
#### 3.2.1 平均真实波幅（ATR，Average True Range）
##### 定义
**ATR**（Average True Range）用于衡量价格波动性，计算最近N期的平均真实波幅。

**计算公式**：
```
TR = MAX(
    HIGH - LOW,
    ABS(HIGH - REF(CLOSE, 1)),
    ABS(LOW - REF(CLOSE, 1))
)
ATR = MA(TR, N)  # N周期TR的移动平均
```

**默认参数**：N = 30

**变量格式**：
```
# 基础值
# ATR
# _atr_{period}      默认30周期
# _atr_{period}_{N}  指定N周期
_atr_1d       # 日线ATR30值
_atr_1d_15    # 日线ATR15值
```

#### 3.2.2 多空线（DKX）
##### 定义
**多空线**是一种结合价格、成交量、趋势的综合指标，用于判断多空力量对比。

**计算公式**：
```
# 多空线基本公式
MID = (3*CLOSE + LOW + HIGH + OPEN) / 6
DKX = (20*MID + 19*REF(MID,1) + 18*REF(MID,2) + ... + 1*REF(MID,19)) / 210
MADKX = MA(DKX, 10)  # DKX的10日移动平均
```

**变量格式**：
```python
# 基础值
# 多空线
# _dkx_{period}
# _dkx_{period}_{ref}
_dkx_1d           # 日线多空线
_dkx_1d_1ref      # 前一个日线多空线
# MA多空线
# _madkx_{period}      默认10周期
# _madkx_{period}_{ref}
_madkx_1d         # 日线MA多空线
_madkx_1d_1ref    # 前一个日线MA多空线

# 斜率属性
# 多空线斜率
# _dkx_{period}_slope
# _dkx_{period}_slope_{ref}
_dkx_1d_slope      # 日线多空线斜率（>0向上，<0向下）
_dkx_1d_slope_1ref # 前一个日线多空线斜率（>0向上，<0向下）
# MA多空线斜率
# _madkx_{period}_slope
# _madkx_{period}_slope_{ref}
_madkx_1d_slope   # 日线MA多空线斜率
_madkx_1d_slope_1ref  # 前一个日线MA多空线斜率

# 趋势（trend）属性
# 多空线趋势（1:趋势向上，-1:趋势向下，0：趋势水平）
# _dkx_{period}_trend
# _dkx_{period}_trend_{ref}
_dkx_1d_trend     # 多空线方向
_madkx_1d_trend   # MA多空线方向

# 拐点属性
# 拐点值
# _dkx_{period}_turn_point
# _dkx_{period}_turn_point_{ref}
_dkx_1d_turn_point     # 日线拐点值
_dkx_1d_turn_point_1ref # 前一个日线拐点值
# 拐点位置（拐点所在的BarPos）
# _dkx_{period}_turn_pos
# _dkx_{period}_turn_pos_{ref}
_dkx_1d_turn_pos       # 日线拐点位置
_dkx_1d_turn_pos_1ref  # 前一个日线拐点位置
# 拐点斜率
# _dkx_{period}_turn_slope
# _dkx_{period}_turn_slope_{ref}
_dkx_1d_turn_slope     # 日线拐点斜率
_dkx_1d_turn_slope_1ref # 前一个日线拐点斜率
# 拐点方向（或趋势） 1：向上拐 -1：向下拐
# _dkx_{period}_turn_trend
# _dkx_{period}_turn_trend_{ref}
_dkx_1d_turn_trend     # 日线拐点方向
_dkx_1d_turn_trend_1ref # 前一个日线拐点方向

# 向下拐点
# 多空线向下拐点值
# _dkx_{period}_turn_down_point
# _dkx_{period}_turn_down_point_{ref}
_dkx_1d_turn_down_point   # 日线多空线向下拐点值
_dkx_1d_turn_down_point_1ref  # 前一个日线多空线向下拐点值
# MA多空线向下拐点值
# _madkx_{period}_turn_down_point
# _madkx_{period}_turn_down_point_{ref}
_madkx_1d_turn_down_point   # 日线MA多空线向下拐点值
_madkx_1d_turn_down_point_1ref  # 前一个日线MA多空线向下拐点值
# 多空线向下拐点位置（拐点所在的BarPos）
# _dkx_{period}_turn_down_pos
# _dkx_{period}_turn_down_pos_{ref}
_dkx_1d_turn_down_pos     # 日线多空线向下拐点位置
_dkx_1d_turn_down_pos_1ref     # 前一个日线多空线向下拐点位置
# MA多空线向下拐点位置（拐点所在的BarPos）
# _madkx_{period}_turn_down_pos
# _madkx_{period}_turn_down_pos_{ref}
_madkx_1d_turn_down_pos     # 日线MA多空线向下拐点位置
_madkx_1d_turn_down_pos_1ref     # 前一个日线MA多空线向下拐点位置
# 多空线向下拐点斜率
# _dkx_{period}_turn_down_slope
# _dkx_{period}_turn_down_slope_{ref}
_dkx_1d_turn_down_slope   # 日线多空线向下拐点斜率
_dkx_1d_turn_down_slope_1ref   # 前一个日线多空线向下拐点斜率
# MA多空线向下拐点斜率
# _madkx_{period}_turn_down_slope
# _madkx_{period}_turn_down_slope_{ref}
_madkx_1d_turn_down_slope   # 日线MA多空线向下拐点斜率
_madkx_1d_turn_down_slope_1ref   # 前一个日线MA多空线向下拐点斜率

# 向上拐点
# 多空线向下拐点值
# _dkx_{period}_turn_up_point
# _dkx_{period}_turn_up_point_{ref}
_dkx_1d_turn_up_point     # 日线多空线向上拐点值
_dkx_1d_turn_up_point_1ref     # 前一个日线多空线向上拐点值
# MA多空线向下拐点值
# _madkx_{period}_turn_up_point
# _madkx_{period}_turn_up_point_{ref}
_madkx_1d_turn_up_point     # 日线MA多空线向上拐点值
_madkx_1d_turn_up_point_1ref     # 前一个日线MA多空线向上拐点值
# 多空线向上拐点位置（拐点所在的BarPos）
# _dkx_{period}_turn_up_pos
# _dkx_{period}_turn_up_pos_{ref}
_dkx_1d_turn_up_pos       # 日线多空线向上拐点位置
_dkx_1d_turn_up_pos_1ref       # 前一个日线多空线向上拐点位置
# MA多空线向上拐点位置（拐点所在的BarPos）
# _madkx_{period}_turn_up_pos
# _madkx_{period}_turn_up_pos_{ref}
_madkx_1d_turn_up_pos       # 日线MA多空线向上拐点位置
_madkx_1d_turn_up_pos_1ref       # 前一个日线MA多空线向上拐点位置
# 多空线向上拐点斜率
# _dkx_{period}_turn_up_slope
# _dkx_{period}_turn_up_slope_{ref}
_dkx_1d_turn_up_slope     # 日线多空线向上拐点斜率
_dkx_1d_turn_up_slope_1ref     # 前一个日线多空线向上拐点斜率
# MA多空线向上拐点斜率
# _madkx_{period}_turn_up_slope
# _madkx_{period}_turn_up_slope_{ref}
_madkx_1d_turn_up_slope     # 日线MA多空线向上拐点斜率
_madkx_1d_turn_up_slope_1ref     # 前一个日线MA多空线向上拐点斜率

# 叉点属性
# 交叉点状态
# 叉点状态（1:金叉，-1:死叉）
# 多空线与MA多空线交叉后， 当多空线在MA多空线上方时状态为1，即金叉；反之为-1，即死叉。
# _dkx_{period}_cross_status
_dkx_1d_cross_status      # 当前日线叉点状态

# 死叉值，即出现死叉状态时叉点的值
# _dkx_{period}_cross_dead_point
# _dkx_{period}_cross_dead_point_{ref}
_dkx_1d_cross_dead_point  # 日线死叉点值
_dkx_1d_cross_dead_point_1ref  # 前一个日线死叉点值
# 死叉位置，即出现死叉状态时叉点所在的BarPos
# _dkx_{period}_cross_dead_point
# _dkx_{period}_cross_dead_point_{ref}
_dkx_1d_cross_dead_pos    # 日线死叉点位置
_dkx_1d_cross_dead_pos_1ref    # 前一个日线死叉点位置

# 金叉值，即出现金叉状态时叉点的值
# _dkx_{period}_cross_golden_point
# _dkx_{period}_cross_golden_point_{ref}
_dkx_1d_cross_golden_point # 日线金叉点值
_dkx_1d_cross_golden_point_1ref # 前一个日线金叉点值
# 金叉位置，即出现金叉状态时叉点所在的BarPos
# _dkx_{period}_cross_golden_pos
# _dkx_{period}_cross_golden_pos_{ref}
_dkx_1d_cross_golden_pos  # 日线金叉点位置
_dkx_1d_cross_golden_pos_1ref  # 前一个日线金叉点位置
```

#### 3.2.3 箱体（BOX）
##### 定义
**箱体**是将连续的K线实体按照涨跌方向进行分组形成的价格区间。

**箱体属性计算**：
```
红色箱体：
  _box_{period}_red_high = MAX(箱体内所有K线的最高价)
  _box_{period}_red_low = MIN(箱体内所有K线的最低价)
  _box_{period}_red_high_pos = 箱体最高价所在的BarPos
  _box_{period}_red_low_pos = 箱体最低价所在的BarPos

绿色箱体：
  _box_{period}_green_high = MAX(箱体内所有K线的最高价)
  _box_{period}_green_low = MIN(箱体内所有K线的最低价)
  _box_{period}_green_high_pos = 箱体最高价所在的BarPos
  _box_{period}_green_low_pos = 箱体最低价所在的BarPos
```

**变量格式**：
```python
# 绿色箱体
# 绿色箱体值
# 绿色箱体高点值
# _box_{period}_green_high
# _box_{period}_green_high_{ref}
_box_1d_green_high      # 日线单绿箱高点
_box_1d_green_high_1ref # 前一个日线单绿箱高点
# 绿色箱体低点值
# _box_{period}_green_low
# _box_{period}_green_low_{ref}
_box_1d_green_low       # 日线单绿箱低点
_box_1d_green_low_1ref  # 前一个日线单绿箱低点
# 绿色箱体开盘价值
# _box_{period}_green_open
# _box_{period}_green_open_{ref}
_box_1d_green_open      # 日线单绿箱开盘价
_box_1d_green_open_1ref # 前一个日线单绿箱开盘价
# 绿色箱体收盘价值
# _box_{period}_green_close
# _box_{period}_green_close_{ref}
_box_1d_green_close      # 日线单绿箱收盘价
_box_1d_green_close_1ref # 前一个日线单绿箱收盘价

# 绿色箱体位置
# 绿色箱体高点位置
# _box_{period}_green_high_pos
# _box_{period}_green_high_pos_{ref}
_box_1d_green_high_pos      # 日线单绿箱体高点位置
_box_1d_green_high_pos_1ref # 前一个日线单绿箱体高点位置
# 绿色箱体低点位置
# _box_{period}_green_low_pos
# _box_{period}_green_low_pos_{ref}
_box_1d_green_low_pos      # 日线单绿箱体低点位置
_box_1d_green_low_pos_1ref # 前一个日线单绿箱体低点位置
# 绿色箱体开盘位置
# _box_{period}_green_open_pos
# _box_{period}_green_open_pos_{ref}
_box_1d_green_open_pos      # 日线单绿箱体开盘价位置
_box_1d_green_open_pos_1ref # 前一个日线单绿箱体开盘价位置
# 绿色箱体收盘位置
# _box_{period}_green_close_pos
# _box_{period}_green_close_pos_{ref}
_box_1d_green_close_pos        # 日线单绿箱体收盘价位置
_box_1d_green_close_pos_1ref   # 前一个日线单绿箱体收盘价位置

# 红色箱体
# 红色箱体值
# 红色箱体高点值
# _box_{period}_red_high
# _box_{period}_red_high_{ref}
_box_1d_red_high        # 日线单红箱高点
_box_1d_red_high_1ref   # 前一个日线单红箱高点
# 红色箱体低点值
# _box_{period}_red_low
# _box_{period}_red_low_{ref}
_box_1d_red_low         # 日线单红箱低点
_box_1d_red_low_1ref    # 前一个日线单红箱低点
# 红色箱体开盘价值
# _box_{period}_red_open
# _box_{period}_red_open_{ref}
_box_1d_red_open        # 日线单红箱开盘价
_box_1d_red_open_1ref   # 前一个日线单红箱开盘价
# 红色箱体收盘价值
# _box_{period}_red_close
# _box_{period}_red_close_{ref}
_box_1d_red_close       # 日线单红箱收盘价
_box_1d_red_close_1ref  # 前一个日线单红箱盘价

# 红色箱体位置
# 红色箱体高点位置
# _box_{period}_red_high_pos
# _box_{period}_red_high_pos_{ref}
_box_1d_red_high_pos      # 日线单红箱高点位置
_box_1d_red_high_pos_1ref # 前一个日线单红箱体高点位置
# 红色箱体低点位置
# _box_{period}_red_low_pos
# _box_{period}_red_low_pos_{ref}
_box_1d_red_low_pos      # 日线单红箱低点位置
_box_1d_red_low_pos_1ref # 前一个日线单红箱体低点位置
# 红色箱体开盘位置
# _box_{period}_red_open_pos
# _box_{period}_red_open_pos_{ref}
_box_1d_red_open_pos      # 日线单红箱开盘价位置
_box_1d_red_open_pos_1ref # 前一个日线单红箱体开盘价位置
# 红色箱体收盘位置
# _box_{period}_red_close_pos
# _box_{period}_red_close_pos_{ref}
_box_1d_red_close_pos        # 日线单红箱收盘价位置
_box_1d_red_close_pos_1ref   # 前一个日线单红箱体收盘价位置

# 组合使用
# 双绿色箱体
MAX(_box_1d_green_high, _box_1d_green_high_1ref) # 双绿箱高点
MIN(_box_1d_green_low, _box_1d_green_low_1ref)   # 双绿箱低点
# 三绿色箱体
MAX(_box_1d_green_high, _box_1d_green_high_1ref， _box_1d_green_high_2ref)  # 三绿箱高点
MIN(_box_1d_green_low, _box_1d_green_low_1ref, _box_1d_green_low_2ref)      # 三绿箱低点
# 双红色箱体
MAX(_box_1d_red_high, _box_1d_red_high_1ref) # 双红箱高点
MIN(_box_1d_red_low, _box_1d_red_low_1ref)   # 双红箱低点
# 三红色箱体
MAX(_box_1d_red_high, _box_1d_red_high_1ref， _box_1d_red_high_2ref)  # 三红箱高点
MIN(_box_1d_red_low, _box_1d_red_low_1ref， _box_1d_red_high_2ref)    # 三红箱低点
```

#### 3.2.4 移动平均线（MA， Moving Average）
#### 定义
**MA**（Moving Average）是简单移动平均线，计算最近N个周期价格的平均值。

**计算公式**：
```
MA(N) = SUM(CLOSE, N) / N
```

**变量格式**：
```python
# 基础值
# _ma_{period}_{num}
# _ma_{period}_{num}_{ref}
_ma_1d_30         # 日线30周期简单移动平均
_ma_1d_30_1ref    # 前一个日线30周期简单移动平均

# 斜率属性
# _ma_{period}_{num}_slope
# _ma_{period}_{num}_slope_{ref}
_ma_1d_30_slope   # 30日MA斜率
_ma_1d_30_slope_1ref   # 前一个30日MA斜率

# 方向属性（1:向上，-1:向下）
# _ma_{period}_{num}_trend
# _ma_{period}_{num}_trend_{ref}
_ma_1d_30_trend        # 30日MA方向
_ma_1d_30_trend_1ref   # 前一个30日MA方向

# 拐点属性
# 向下拐点值
# _ma_{period}_{num}_turn_down_point
# _ma_{period}_{num}_turn_down_point_{ref}
_ma_1d_20_turn_down_point        # 20日MA向下拐点值
_ma_1d_20_turn_down_point_1ref   # 20日MA向下拐点值
# 向下拐点斜率
# _ma_{period}_{num}_turn_down_slope
# _ma_{period}_{num}_turn_down_slope_{ref}
_ma_1d_20_turn_down_slope        # 20日MA向下拐点斜率
_ma_1d_20_turn_down_slope_1ref   # 前一个20日MA向下拐点斜率
# 向下拐点位置
# _ma_{period}_{num}_turn_down_pos
# _ma_{period}_{num}_turn_down_pos_{ref}
_ma_1d_20_turn_down_pos          # 20日MA向下拐点位置
_ma_1d_20_turn_down_pos_1ref     # 前一个20日MA向下拐点位置
# 向上拐点值
# _ma_{period}_{num}_turn_up_point
# _ma_{period}_{num}_turn_up_point_{ref}
_ma_1d_20_turn_up_point          # 20日MA向上拐点值
_ma_1d_20_turn_up_point_1ref     # 前一个20日MA向上拐点值
# 向上拐点斜率
# _ma_{period}_{num}_turn_up_slope
# _ma_{period}_{num}_turn_up_slope_{ref}
_ma_1d_20_turn_up_slope          # 20日MA向上拐点斜率
_ma_1d_20_turn_up_slope_1ref     # 前一个20日MA向上拐点斜率
# 向上拐点位置
# _ma_{period}_{num}_turn_up_pos
# _ma_{period}_{num}_turn_up_pos_{ref}
_ma_1d_20_turn_up_pos            # 20日MA向上拐点位置
_ma_1d_20_turn_up_pos_1ref       # 前一个20日MA向上拐点位置
```

#### 3.2.5 指数移动平均线（EMA, Exponential Moving Average）
##### 定义
**EMA**（Exponential Moving Average）是指数移动平均线，赋予近期价格更高的权重。

**计算公式**：
```
EMA(N) = α * CLOSE + (1-α) * REF(EMA, 1)
其中：α = 2/(N+1)
```

**变量格式**：
```python
# 基础值
# _ema_{period}_{num}
# _ema_{period}_{num}_{ref}
_ema_1d_30        # 日线30周期指数移动平均
_ema_1d_30_1ref   # 前一个日线30周期指数移动平均

# 斜率属性
# _ema_{period}_{num}_slope
# _ema_{period}_{num}_slope_{ref}
_ema_1d_30_slope       # 30日EMA斜率
_ema_1d_30_slope_1ref  # 前一个30日EMA斜率

# 方向属性（1:向上，-1:向下）
# _ema_{period}_{num}_trend
# _ema_{period}_{num}_trend_{ref}
_ema_1d_30_trend       # 30日EMA方向
_ema_1d_30_trend_1ref  # 前一个30日EMA方向

# 拐点属性
# 向下拐点值
# _ema_{period}_{num}_turn_down_point
# _ema_{period}_{num}_turn_down_point_{ref}
_ema_1d_30_turn_down_point       # 30日EMA向下拐点值
_ema_1d_30_turn_down_point_1ref  # 前一个30日EMA向下拐点值
# 向下拐点斜率
# _ema_{period}_{num}_turn_down_slope
# _ema_{period}_{num}_turn_down_slope_{ref}
_ema_1d_30_turn_down_slope       # 30日EMA向下拐点斜率
_ema_1d_30_turn_down_slope_1ref  # 前一个30日EMA向下拐点斜率
# 向下拐点位置
# _ema_{period}_{num}_turn_down_pos
# _ema_{period}_{num}_turn_down_pos_{ref}
_ema_1d_30_turn_down_pos       # 30日EMA向下拐点位置
_ema_1d_30_turn_down_pos_1ref  # 前一个30日EMA向下拐点位置
# 向上拐点值
# _ema_{period}_{num}_turn_up_point
# _ema_{period}_{num}_turn_up_point_{ref}
_ema_1d_30_turn_up_point       # 30日EMA向上拐点值
_ema_1d_30_turn_up_point_1ref  # 前一个30日EMA向上拐点值
# 向上拐点斜率
# _ema_{period}_{num}_turn_up_slope
# _ema_{period}_{num}_turn_up_slope_{ref}
_ema_1d_30_turn_up_slope       # 30日EMA向上拐点斜率
_ema_1d_30_turn_up_slope_1ref  # 前一个30日EMA向上拐点斜率
# 向上拐点位置
# _ema_{period}_{num}_turn_up_pos
# _ema_{period}_{num}_turn_up_pos_{ref}
_ema_1d_30_turn_up_pos         # 30日EMA向上拐点位置
_ema_1d_30_turn_up_pos _1ref  # 前一个30日EMA向上拐点位置
```

#### 3.2.6 Zigzag指标（Zig）
##### 定义
**Zigzag指标**用于识别价格走势中的显著转折点，过滤掉小幅波动，突出主要趋势变化。

**计算公式**：
```
# Zigzag指标基于N个ATR或价格百分比变化识别转折点
# 当价格从上一个转折点变化超过指定ATR倍数或百分比时，形成新的转折点
```

**默认参数**：百分比阈值 = 5%

**变量格式**：
```python
# 基础值
# Zigzag低点值指标
# _zig_{period}_low_point_{k}_{t}_{n}_{m}
# k: 0--收盘价,1--开盘价,2--最高价,3--最低价,,4--low,high,5--ema,6--ma,7--dkx,8--madkx 默认：3
# t: 0--ATR,1--百分比 默认：0
# n: 变化值，比如 5，即0.5，系统会除以10，该值取决于t的类型。 默认：15
# m: 均线数，即 当k为5或6时，才需要设置大于0的值 默认：0
# _zig_{period}_low_point_{k}_{t}_{n}_{ref}
_zig_1d_low_point_3_0_15   # 日线收盘价计算Zigzag指标，当1.5个ATR时形成转折点，低点值
_zig_1d_low_point_3_0_15_1ref     # 前一个日线收盘价计算Zigzag指标，当1.5个ATR时形成转折点，前低点值
_zig_1d_low_point_5_0_15_30     # 日线30周期EMA计算Zigzag指标，当1.5个ATR时形成转折点，低点值
_zig_1d_low_point_5_0_15_30_1ref     # 前一个日线30周期EMA计算Zigzag指标，当1.5个ATR时形成转折点，前低点值

# Zigzag高点值指标
# _zig_{period}_high_point_{k}_{t}_{n}_{m}
# k: 0--收盘价,1--开盘价,2--最高价,3--最低价,,4--low,high,5--ema,6--ma,7--dkx,8--madkx 默认：3 默认：3
# t: 0--ATR,1--百分比 默认：0
# n: 变化值，比如 5，即0.5，系统会除以10，该值取决于t的类型。 默认：15
# m: 均线数，即 当k为5或6时，才需要设置大于0的值 默认：0
# _zig_{period}_high_point_{k}_{t}_{n}_{m}_{ref}
_zig_1d_high_point_3_0_15   # 日线收盘价计算Zigzag指标，当1.5个ATR时形成转折点，高点值
_zig_1d_high_point_3_0_15_1ref     # 前一个日线收盘价计算Zigzag指标，当1.5个ATR时形成转折点，前高点值
_zig_1d_high_point_5_0_15_30     # 日线30周期EMA计算Zigzag指标，当1.5个ATR时形成转折点，高点值
_zig_1d_high_point_5_0_15_30_1ref     # 前一个日线30周期EMA计算Zigzag指标，当1.5个ATR时形成转折点，前高点值

# Zigzag低点位置指标
# _zig_{period}_low_pos_{k}_{t}_{n}_{m} 
# k: 0--收盘价,1--开盘价,2--最高价,3--最低价,,4--low,high,5--ema,6--ma,7--dkx,8--madkx 默认：3 默认：3
# t: 0--ATR,1--百分比 默认：0
# n: 变化值，比如 5，即0.5，系统会除以10，该值取决于t的类型。 默认：15
# m: 均线数，即 当k为5或6时，才需要设置大于0的值 默认：0
# _zig_{period}_low_pos_{k}_{t}_{n}_{m}_{ref}
_zig_1d_low_pos_3_0_15   # 日线收盘价计算Zigzag指标，当1.5个ATR时形成转折点，低点位置
_zig_1d_low_pos_3_0_15_1ref     # 前一个日线收盘价计算Zigzag指标，当1.5个ATR时形成转折点，前低点位置
_zig_1d_low_pos_5_0_15_30     # 日线30周期EMA计算Zigzag指标，当1.5个ATR时形成转折点，低点位置
_zig_1d_low_pos_5_0_15_30_1ref     # 前一个日线30周期EMA计算Zigzag指标，当1.5个ATR时形成转折点，前低点位置

# Zigzag高点位置指标
# _zig_{period}_high_pos_{k}_{t}_{n}_{m} 
# k: 0--收盘价,1--开盘价,2--最高价,3--最低价,,4--low,high,5--ema,6--ma,7--dkx,8--madkx 默认：3 默认：3
# t: 0--ATR,1--百分比 默认：0
# n: 变化值，比如 5，即0.5，系统会除以10，该值取决于t的类型。 默认：15
# m: 均线数，即 当k为5或6时，才需要设置大于0的值 默认：0
# _zig_{period}_high_pos_{k}_{t}_{n}_{m}_{ref}
_zig_1d_high_pos_3_0_15   # 日线收盘价计算Zigzag指标，当1.5个ATR时形成转折点，高点位置
_zig_1d_high_pos_3_0_15_1ref     # 前一个日线收盘价计算Zigzag指标，当1.5个ATR时形成转折点，前高点位置
_zig_1d_high_pos_5_0_15_30     # 日线30周期EMA计算Zigzag指标，当1.5个ATR时形成转折点，高点位置
_zig_1d_high_pos_5_0_15_30_1ref     # 前一个日线30周期EMA计算Zigzag指标，当1.5个ATR时形成转折点，前高点位置
```

#### 3.2.7 相对强弱指数（RSI，Relative Strength Index）
##### 定义
**RSI**（Relative Strength Index）用于衡量价格变动的速度和幅度，判断市场的超买超卖状态。

**计算公式**：
```
# RSI计算公式
RS = 平均上涨幅度 / 平均下跌幅度
RSI = 100 - (100 / (1 + RS))
```

**默认参数**：N = 10

**变量格式**：
```python
# 基础值
# RSI指标
# _rsi_{period}      默认10周期
# _rsi_{period}_{N}  指定N周期
_rsi_1d         # 日线RSI10值 
_rsi_1d_6       # 日线RSI6值
_rsi_1d_1ref    # 前一个日线RSI值
```

### 3.3 仓位指标变量
| 变量 | 说明 | 示例值 | 计算公式 |
|------|------|--------|----------|
| `_holding_cost` | 持仓（平均）成本 | 50.25 | `∑(买入数量×买入价格)/总持仓数量` |
| `_holding_qty` | 持仓数量（都为正数） | 1000.0 | >0 有仓位 |
| `_holding_days` | 持仓天数 | 15 | `当前日期 - 开仓日期` |
| `_entry_price` | 最近一次开仓价格 | 48.50 | 最近开仓成交价 |
| `_exit_price` | 最近一次平仓价格 | 52.30 | 最近平仓成交价 |
| `_entry_barpos` | 最近开仓K线位置 | 120 | 开仓时的barpos值 |
| `_exit_barpos` | 最近平仓K线位置 | 135 | 平仓时的barpos值 |
| `_market_value` | 持仓市值 | 55250.0 | `持仓数量 × 当前价格` |
| `_palr` | 盈亏百分比，盈亏% | 4.2 | `(市值-成本)/成本 × 100%`， 如果是空头，则为相反数 |
| `_palp` | 盈亏点数 | 1.75 | `当前价格 - 持仓成本`，如果是空头，则为相反数 |

**方向说明**：
- 当前持仓只考虑一个方向， 要么是**多头方向**，要么是**空头方向**

## 4. 系统函数
### 4.1 基本数学函数
```python
# 最大值函数
# MAX(value1, value2, ...)
MAX(_close_1d, _open_1d)               # 当日最高价
MAX(_ma_1d_5, _ma_1d_10, _ma_1d_20)    # 多条均线的最大值

# 最小值函数
# MIN(value1, value2, ...)
MIN(_close_1d, _open_1d)                # 当日最低价
MIN(_box_1d_green_low, _box_1d_red_low) # 箱体下沿，双绿箱体低点

# 绝对值函数
# ABS(value)
ABS(_dkx_1d_slope)                      # 多空线斜率的绝对值
ABS(_palr)                              # 盈亏率的绝对值
```

### 4.2 系统函数
#### 4.2.1 引用函数
```python
# REF(value, n)
# 参数：value - 要引用的变量，n - 引用周期数
REF(_close_1d, 1)             # 前一日收盘价
REF(_ma_1d_20, 2)             # 前两日的20日均线
```

#### 4.2.2 最大值函数
```python
# HHV(window, expression, period, [ref])
# 参数：window - 滑动窗口大小，expression - 表达式，period - 周期，ref - 引用参数
HHV(10, _close_1d, 1d)           # 最近10日最高收盘价
HHV(20, _high_1d, 1d)            # 最近20日最高价
HHV(10, _close_1d, 1d, 1ref)     # 昨日计算的最近10日最高收盘价
HHV(5, _dkx_1d, 1d)              # 最近5日多空线最大值
```

#### 4.2.3 最小值函数
```python
# LLV(window, expression, period, [ref])
# 参数：window - 滑动窗口大小，expression - 表达式，period - 周期，ref - 引用参数
LLV(10, _close_1d, 1d)           # 最近10日最低收盘价
LLV(20, _low_1d, 1d)             # 最近20日最低价
LLV(10, _close_1d, 1d, 1ref)     # 昨日计算的最近10日最低收盘价
LLV(5, _dkx_1d, 1d)              # 最近5日多空线最小值
```

#### 4.2.4 均值函数
```python
# MEAN(window, expression, period, [ref])
# 参数：window - 滑动窗口大小，expression - 表达式，period - 周期，ref - 引用参数
MEAN(10, _close_1d, 1d)          # 10日收盘价均线
MEAN(20, _volume_1d, 1d)         # 20日成交量均线
MEAN(10, _close_1d, 1d, 1ref)    # 昨日计算的10日均线
MEAN(5, _dkx_1d, 1d)             # 5日多空线均值
```

#### 4.2.5 任意满足函数
```python
# ANY(window, required_count, condition, period, [ref])
# 参数：window - 滑动窗口大小，required_count - 需要满足的个数，condition - 条件表达式，period - 周期，ref - 引用参数
ANY(5, 3, _close_1d > _open_1d, 1d)           # 最近5天至少3天收阳
ANY(10, 4, _close_1d > _ma_1d_20, 1d)         # 最近10天至少4天收盘在20日线上
ANY(20, 10, _dkx_1d_slope > 0, 1d)            # 最近20天至少10天多空线斜率向上
ANY(5, 2, _close_1d > _open_1d, 1d, 1ref)     # 昨日判断的最近5天至少2天收阳
```

#### 4.2.6 计数函数
```python
# COUNT(window, condition, period, [ref])
# 参数：window - 滑动窗口大小，condition - 条件表达式，period - 周期，ref - 引用参数
COUNT(20, _close_1d > _open_1d, 1d)           # 最近20天收阳的天数
COUNT(10, _close_1d > _ma_1d_20, 1d)          # 最近10天收盘在20日线上的天数
COUNT(5, _dkx_1d_cross_status == 1, 1d)       # 最近5天金叉的天数
COUNT(10, _close_1d > _open_1d, 1d, 1ref)     # 昨日计算的最近10天收阳天数
```

#### 4.2.7 范围判断函数
```python
# INRANGE(value, min_value, max_value)
# 参数：value - 要判断的值，min_value - 最小值，max_value - 最大值
INRANGE(_close_1d, 10, 20)                                                  # 收盘价在10-20之间
INRANGE(_palr, -5, 5)                                                       # 盈亏率在-5%到5%之间
INRANGE(_close_1d, _box_1d_green_low, _box_1d_green_high)                   # 收盘价在绿箱体内
INRANGE(_vol_1d, 0.8 * MEAN(20, _vol_1d, 1d), 1.2 * MEAN(20, _vol_1d, 1d))  # 成交量在均量80%-120%之间
```

#### 4.2.8 IF判断函数
```python
# IF(condition, thenValue, elseValue)
# 参数：condition - 要判断的条件，满足：thenValue，不满足：elseValue
IF(_close_1d > _open_1d, _high_1d, _low_1d)              # 阳线时用高点，阴线时用低点
```

## 5. 表达式示例
### 5.1 趋势判断类
```python
# 多头趋势：价格在20日线上，20日线向上
_close_1d > _ma_1d_20 && _ma_1d_20_slope > 0

# 金叉确认：快线上穿慢线
_ema_1d_12 > _ema_1d_26 && REF(_ema_1d_12, 1) <= REF(_ema_1d_26, 1)

# 多空线向上且金叉状态
_dkx_1d_slope > 0 && _dkx_1d_cross_status == 1

# 价格突破箱体
_close_1d > _box_1d_green_high

# 均线多头排列
_ma_1d_5 > _ma_1d_10 && _ma_1d_10 > _ma_1d_20 && _ma_1d_20 > _ma_1d_60
```

### 5.2 风险控制类
```python
# 止损条件：亏损超过8%
_palr < -8.0

# 动态止盈：盈利超过20% 或 价格跌破10日线
_palr > 20.0 || _close_1d < _ma_1d_10

# 最大持仓天数限制
_holding_days > 30

# 回撤控制：从最高点回撤超过5%
(_close_1d / HHV(20, _close_1d, 1d) - 1) * 100 < -5.0
```

### 5.3 量价关系类
```python
# 放量上涨
_close_1d > _open_1d && _vol_1d > 1.5 * MEAN(20, _vol_1d, 1d)

# 缩量回调
_close_1d < REF(_close_1d, 1) && _vol_1d < 0.8 * MEAN(20, _vol_1d, 1d)

# 量价齐升
_close_1d > REF(_close_1d, 1) && _vol_1d > REF(_vol_1d, 1) && _vol_1d > MEAN(20, _vol_1d, 1d)
```

### 5.4 组合条件类
```python
# 买入信号：金叉 + 放量 + 突破箱体
_dkx_1d_cross_status == 1 && 
_vol_1d > 1.5 * REF(_vol_1d, 1) &&
_close_1d > _box_1d_green_high

# 卖出信号：死叉 或 盈利回撤超过5%
_dkx_1d_cross_status == -1 ||
(_palr > 10 && (_close_1d / HHV(5, _close_1d, 1d) - 1) * 100 < -5.0)

# 加仓条件：趋势向上 + 缩量回调到支撑
_ma_1d_20_slope > 0 &&
_close_1d < _ma_1d_20 && _close_1d > _ma_1d_60 &&
_vol_1d < 0.7 * MEAN(20, _vol_1d, 1d)
```

### 5.5 复杂策略类
```python
# 多周期共振：日线金叉 + 60分钟多头
_dkx_1d_cross_status == 1 && _dkx_60m_slope > 0

# 突破回踩确认
_close_1d > HHV(20, _close_1d, 1d) &&  # 突破20日高点
REF(_close_1d, 1) < REF(_close_1d, 2) &&  # 昨日回调
_close_1d > REF(_close_1d, 1)  # 今日上涨

# 均线粘合后发散
ABS(_ma_1d_5 - _ma_1d_10) / _ma_1d_5 < 0.01 &&  # 5日和10日线距离小于1%
_ma_1d_5_slope > 0 &&  # 5日线向上
_close_1d > MAX(_ma_1d_5, _ma_1d_10, _ma_1d_20)  # 价格站上所有均线
```

## 6. 最佳实践
### 6.1 边界处理
```python
# 检查前引用时数据是否足够
_barpos_1d > 20 && _close_1d > REF(_close_1d, 20)

# 窗口函数初始阶段处理
IF(_barpos_1d > 10, HHV(10, _close_1d, 1d) > _close_1d, 0)

# 避免除零错误
IF(_open_1d != 0, (_close_1d - _open_1d) / _open_1d, 0) > 0.05
```

### 6.2 可读性建议
```python
# 使用括号明确优先级
(_close_1d > _open_1d) && (_vol_1d > REF(_vol_1d, 1))

# 复杂表达式分行书写
(
  _dkx_1d_cross_status == 1 && 
  _vol_1d > 1.2 * MEAN(20, _vol_1d, 1d) &&
  _close_1d > _box_1d_green_high
) || 
(
  _ma_1d_5 > _ma_1d_20 && 
  _ma_1d_20_slope > 0 &&
  ANY(3, 2, _close_1d > _open_1d, 1d)
)
```

## 7. 常见问题解答
### 7.1 引用参数相关问题
**Q: `_close_1d_1ref` 和 `REF(_close_1d, 1)` 有什么区别？**
A: 两者功能相同，`_close_1d_1ref`是语法糖，`REF()`是函数形式。建议复杂表达式使用`REF()`函数，简单引用使用后缀形式。

**Q: 如果引用的周期不存在怎么办？**
A: 返回`NaN`（非数字），表达式计算时会自动处理为`false`。

### 7.2 函数使用问题
**Q: HHV/LLV/MEAN函数中的ref参数有什么用？**
A: 用于计算历史时点的指标值。比如在回测中，计算昨天看到的"最近10日最高价"，需要使用`HHV(10, _close_1d, 1d, 1ref)`。

**Q: ANY函数和COUNT函数有什么区别？**
A: ANY返回布尔值（是否达到阈值），COUNT返回具体个数。ANY适合判断条件，COUNT适合统计数量。

### 7.3 表达式编写问题
**Q: 如何表达"连续3天上涨"？**
A: 使用引用和逻辑与：`_close_1d > REF(_close_1d, 1) && REF(_close_1d, 1) > REF(_close_1d, 2) && REF(_close_1d, 2) > REF(_close_1d, 3)`

**Q: 如何表达"价格在均线附近"？**
A: 使用INRANGE函数：`INRANGE(_close_1d, _ma_1d_20 * 0.99, _ma_1d_20 * 1.01)` 或在1%范围内。

---

## 📋 测试题
检查你对表达式的理解程度：

1. **5日EMA在20日EMA之上，且5日EMA斜率向上**
   ```python
   _ema_1d_5 > _ema_1d_20 && _ema_1d_5_slope > 0
   ```

2. **最近10日收盘价在20日线上的天数超过7天**
   ```python
   COUNT(10, _close_1d > _ma_1d_20, 1d) > 7
   ```

3. **价格突破最近20日最高价，且成交量是平均的1.5倍**
   ```python
   _close_1d > HHV(20, _close_1d, 1d) && 
   _volume_1d > 1.5 * MEAN(20, _volume_1d, 1d)
   ```

4. **持仓盈利超过10%，但价格跌破5日线**
   ```python
   _palr > 10.0 && _close_1d < _ma_1d_5
   ```

5. **多空线金叉，且最近5天有3天以上是多头趋势**
   ```python
   _dkx_1d_cross_status == 1 && 
   ANY(5, 3, _dkx_1d_slope > 0, 1d)
   ```
   
---