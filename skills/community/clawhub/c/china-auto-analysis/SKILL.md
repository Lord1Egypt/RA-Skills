# China Auto Market Analysis Skill

制作中国汽车市场产销分析可视化仪表盘。数据来源为 **akshare**（CPCA乘联会厂商排名接口）。

---

## 功能

- **YTD（累计至今）数据**：支持任意年月的累计数据，如 2026年1-2月
- **单月数据**：指定相同起止月份即可
- **三种数据维度**：产量 / 批发销量 / 零售销量
- **Top15 厂商排行**：水平条形图，当年 vs 上年同期对比
- **同比变化分析**：绝对值变化（万辆）+ 增速（%）
- **产销平衡对比**：产量 vs 批发 vs 零售三维分组条形图
- **KPI 概览卡**：总量、冠军、增速王、跌幅王
- **Dark Mode 专业风格**：深色背景、涨跌颜色编码

---

## 数据来源

| 接口 | 说明 |
|---|---|
| `akshare.car_market_man_rank_cpca` | CPCA乘联会·厂商排名（狭义/广义乘用车） |

支持 `产量`、`批发`、`零售` 三种口径，支持单月和累计模式。

---

## 快速使用

```bash
# 产量 YTD（1-2月累计）
python3 china_auto_dashboard.py --year 2026 --start-month 1 --end-month 2 --type 产量

# 单月批发销量（2月）
python3 china_auto_dashboard.py --year 2026 --start-month 2 --end-month 2 --type 批发销量

# 零售销量（Q1累计）
python3 china_auto_dashboard.py --year 2026 --start-month 1 --end-month 3 --type 零售销量

# 全年累计
python3 china_auto_dashboard.py --year 2025 --start-month 1 --end-month 12 --type 产量
```

**参数说明：**
| 参数 | 说明 |
|---|---|
| `--year` | 目标年份（默认 2026） |
| `--start-month` | 起始月份（默认 1） |
| `--end-month` | 结束月份（默认 2） |
| `--type` | `产量` / `批发销量` / `零售销量` |
| `--scope` | `狭义乘用车`（默认）/ `广义乘用车` |
| `--output` | 输出图片路径 |

---

## 安装依赖

```bash
pip install akshare pandas matplotlib numpy
# 中文字体（如需显示中文）
# Linux: apt install fonts-noto-cjk fonts-wqy-microhei
```

---

## 图表结构

```
┌─────────────────────────────────────────────────────────────┐
│  KPI卡1: 总量(YTD)  │ 基准去年 │ 冠军    │ 增速王 │ 跌幅王 │
├────────────────────────────┬────────────────────────────────┤
│  Top N 厂商排行条形图      │  同比变化（万辆 + %）           │
│  彩色=当年 灰色=去年       │  红=增长 绿=下降                │
├────────────────────────────┴────────────────────────────────┤
│  产量 vs 批发 vs 零售 三维对比（底部）                       │
└─────────────────────────────────────────────────────────────┘
```

## 追问示例

- "换成零售销量" → 重新调用，type=零售销量
- "看单月不要YTD" → start-month=2, end-month=2
- "只看前5名" → 修改 top_n 参数（TODO: CLI参数化）
- "换成广义乘用车" → --scope 广义乘用车
- "导出到 Excel" → TODO: 添加 Excel 导出功能

---

## 文件结构

```
china-auto-analysis/
├── SKILL.md                ← 本文件
└── china_auto_dashboard.py ← 核心可视化脚本
```
