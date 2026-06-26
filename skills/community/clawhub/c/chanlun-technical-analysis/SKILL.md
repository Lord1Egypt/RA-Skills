# ChanLun Technical Analysis Skill

基于缠中说禅技术理论，实现 A 股股票的技术面分析，包括分型、笔、线段、中枢、背驰等核心概念的自动识别与可视化。

## 核心功能

| 功能 | 说明 |
|------|------|
| **分型识别** | 顶分型(Top Fractal)、底分型(Bottom Fractal)自动检测 |
| **笔识别** | 顶底交替连接，K 线包含处理 |
| **线段识别** | 至少 3 笔，有重叠区域 |
| **中枢识别** | 至少 3 笔重叠区域 |
| **背驰检测** | MACD 柱面积比较 |
| **图表绘制** | K 线 + 分型 + 笔 + 线段 + 中枢 + MACD + 成交量 |
| **报告生成** | Markdown 格式技术分析报告 |
| **PNG 图片** | 直观的技术图形展示（主图 + 副图），英文标签 |

---

## 缠论核心概念

### 1. 分型 (Fractal)

**顶分型**: 第二 K 线高点是相邻三 K 线高点中最高的，低点也是相邻三 K 线低点中最高的
- 顶分型的最高点叫该分型的顶

**底分型**: 第二 K 线低点是相邻三 K 线低点中最低的，高点也是相邻三 K 线高点中最低的
- 底分型的最低点叫该分型的底

### 2. K 线包含处理

**向上处理**: 两 K 线高点取高者，低点取较高者
**向下处理**: 两 K 线低点取低者，高点取较低者

### 3. 笔 (Stroke)

- 两个相邻的顶和底构成一笔
- 顶和底之间至少有 1 根 K 线相隔
- 笔分为向上笔和向下笔

### 4. 线段 (Line Segment)

- 由奇数笔组成（至少 3 笔）
- 前三笔必须有重叠部分
- 分为向上线段和向下线段

### 5. 中枢 (Pivot)

- 某级别走势中，被至少三个连续次级别走势所重叠的部分
- 对笔来说：至少三笔重叠
- 对线段来说：至少三段重叠

### 6. 背驰 (Divergence)

- 没有趋势就没有背驰
- 比较相邻两段的 MACD 柱面积
- c 段面积 < b 段面积 = 背驰

---

## 使用方法

```bash
# 分析单只股票（自动生成图表和报告）
python3 scripts/chanlun_analysis.py 601688

# 指定时间周期
python3 scripts/chanlun_analysis.py 601688 --period 60

# 输出 JSON 数据
python3 scripts/chanlun_analysis.py 601688 --json

# 指定输出目录
python3 scripts/chanlun_analysis.py 601688 --output ./reports
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `stock_code` | 股票代码（如 601688） | 必填 |
| `--period` | 周期：daily/60/30 等 | daily |
| `--output` | 输出目录 | ./outputs |
| `--json` | 额外输出 JSON 格式 | 否 |
| `--verbose` | 详细输出 | 否 |

> **注意**: 图表 PNG 是必需输出，无需额外参数，每次分析自动生成。

---

## 输出内容

每次分析**自动生成**以下文件：

### 1. 技术分析报告 (Markdown)

报告结构（**核心结论优先**）：

| 章节 | 内容 |
|------|------|
| **🎯 核心结论** | 走势判断、背驰信号、操作建议、关键价位 |
| **📊 缠论分析图表** | PNG 图表展示 |
| **📋 分项统计** | 行情概况、分型统计、笔分析、中枢分析、背驰检测 |
| **⚠️ 风险提示** | 免责声明 |

### 2. 缠论可视化图表 (PNG) - 必需输出

图表内容：
- **主图**: K 线图 + 分型标记 (T=顶分型, B=底分型) + 笔连接 + 线段区域 + 中枢区域
- **副图 1**: MACD 指标 (柱状图 + DIF 线 + DEA 线)
- **副图 2**: 成交量柱状图

**图表元素说明**:

| 元素 | 颜色/样式 | 说明 |
|------|----------|------|
| Bullish Candle | 🔴 红色 | 收盘价≥开盘价（阳线） |
| Bearish Candle | 🟢 绿色 | 收盘价<开盘价（阴线） |
| Top Fractal (T) | 🟢 绿色圆圈 | 顶分型，局部高点 |
| Bottom Fractal (B) | 🔴 红色圆圈 | 底分型，局部低点 |
| Up Stroke | 🔵 蓝色实线 | 向上笔，从底到顶 |
| Down Stroke | 🟣 紫色虚线 | 向下笔，从顶到底 |
| Pivot Zone | 🟡 黄色区域 | 中枢，至少3笔重叠区间 |
| Segment | 浅色背景 | 线段区域 |

### 3. 输出文件

| 文件 | 说明 |
|------|------|
| `{stock_code}_chanlun_chart.png` | 缠论分析图表 |
| `{stock_code}_chanlun_report.md` | 技术分析报告 |

### 3. JSON 数据结构

```json
{
  "stock_code": "601688",
  "trend": "uptrend",
  "fractals": {
    "tops_count": 8,
    "bottoms_count": 7
  },
  "strokes_count": 12,
  "segments_count": 3,
  "pivots_count": 2,
  "divergence": {
    "detected": true,
    "type": "bullish",
    "confidence": 0.75
  }
}
```

---

## 买卖点定义

### 第一类买卖点
- 趋势背驰后形成的转折点
- 下跌趋势底背驰 → 第一类买点
- 上涨趋势顶背驰 → 第一类卖点

### 第二类买卖点
- 第一类买卖点后的第一次回抽
- 不回前低/前高形成

### 第三类买卖点
- 突破中枢后的回抽
- 回抽不进入中枢区间

---

## 环境要求

### 🔑 Tushare 数据源配置

本技能依赖 **Tushare Pro** 作为数据源，需要预先配置 API Token。

#### Tushare 注册要求

| 项目 | 说明 |
|------|------|
| **注册地址** | https://tushare.pro/register |
| **注册流程** | 手机号注册 → 实名认证 → 获取 Token |
| **免费额度** | 新用户赠送 500 积分，基础日线数据免费 |
| **积分说明** | 积分越高，接口权限越多，详细权限见官网 |

#### 环境变量配置

**方式一：临时配置（当前终端有效）**
```bash
export TUSHARE_TOKEN=your_token_here
```

**方式二：永久配置（写入 ~/.bashrc）**
```bash
echo 'export TUSHARE_TOKEN=your_token_here' >> ~/.bashrc
source ~/.bashrc
```

**验证配置**
```bash
python3 -c "import os; print('TUSHARE_TOKEN:', os.getenv('TUSHARE_TOKEN', 'NOT SET'))"
```

#### 常见问题

| 问题 | 解决方案 |
|------|---------|
| Token 未设置 | 报错 `TUSHARE_TOKEN environment variable is required` |
| Token 无效 | 检查 Token 是否正确复制，无多余空格 |
| 接口权限不足 | 登录 Tushare 官网查看积分权限 |

### 必需环境变量

| 变量名 | 说明 | 必需 | 获取方式 |
|--------|------|:----:|---------|
| `TUSHARE_TOKEN` | Tushare Pro API Token | ✅ | https://tushare.pro |

### Python 依赖

```bash
pip install pandas numpy matplotlib tushare
```

| 包名 | 版本要求 | 说明 |
|------|---------|------|
| pandas | >=1.5.0 | 数据处理 |
| numpy | >=1.20.0 | 数值计算 |
| matplotlib | >=3.5.0 | 图表绘制 |
| tushare | >=1.2.0 | A股数据源（需注册获取 Token） |

---

## 文件结构

```
chanlun-technical-analysis/
├── SKILL.md                    # 技能文档
├── skill.json                  # 技能元数据
└── scripts/
    ├── chanlun_analysis.py     # 主入口脚本
    ├── chanlun_core.py         # 核心算法（分型/笔/线段）
    ├── chanlun_divergence.py   # 背驰检测
    └── chanlun_chart.py        # 图表绘制
```

---

## 注意事项

1. **数据质量**: 使用前复权数据，避免除权缺口影响
2. **周期选择**: 建议使用日线或以上周期，分钟线噪音较多
3. **主观性**: 缠论部分判断存在主观性，算法仅为辅助
4. **结合其他指标**: 建议配合成交量、基本面等综合分析
5. **图表标签**: 所有图表使用英文标签，避免中文字体依赖问题

---

## 免责声明

本技能仅供学习和研究使用，不构成任何投资建议。股市有风险，投资需谨慎。