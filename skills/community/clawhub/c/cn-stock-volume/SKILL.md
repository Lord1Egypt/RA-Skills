# cn-stock-volume v3.0

获取中国 A 股市场核心数据：**三大指数点位及涨跌幅**、**成交量变化**、**涨跌家数比**。

## 📊 数据指标

| 指标 | 获取方式 | 说明 | 示例 |
|------|----------|------|------|
| **上证指数** | 🤖 自动 | 点位 + 涨跌幅 | 3957.05 点，-1.24% |
| **深证成指** | 🤖 自动 | 点位 + 涨跌幅 | 13866.20 点，-0.25% |
| **创业板指** | 🤖 自动 | 点位 + 涨跌幅 | 3352.10 点，+1.30% |
| **上涨家数** | 🤖 自动 | A 股上涨数量 | 1234 家 |
| **下跌家数** | 🤖 自动 | A 股下跌数量 | 3456 家 |
| **今日量能** | ✍️ 手动 | 四市总成交金额 | `待补充` |
| **昨日量能** | ✍️ 手动 | 前一交易日成交金额 | `待补充` |

## 🚀 快速开始

### 步骤 1：获取自动数据

```bash
# 查询今日（自动获取指数 + 涨跌家数）
python3 scripts/generate_report.py

# 查询指定日期
python3 scripts/generate_report.py 2026-03-22

# 强制刷新（忽略缓存）
python3 scripts/generate_report.py --force
```

### 步骤 2：补充成交量数据

```bash
# 补充今日和昨日成交量（单位：万亿）
python3 scripts/补数据.py 2026-03-22 --today 1.23 --previous 1.30

# 查看当前手动数据
python3 scripts/补数据.py 2026-03-22 --show

# 清除手动数据
python3 scripts/补数据.py 2026-03-22 --clear
```

### 步骤 3：重新生成报告

```bash
# 重新生成（使用补充的成交量数据）
python3 scripts/generate_report.py 2026-03-22
```

## 📁 输出文件

### Markdown 报告（人类阅读）
- **位置**: `~/Desktop/A 股每日复盘/stock-report-YYYY-MM-DD.md`
- **用途**: 直接阅读、分享到群聊

### JSON 数据（程序调用）
- **位置**: `~/Desktop/A 股每日复盘/data-YYYY-MM-DD.json`
- **用途**: 其他程序/脚本调用

## 🏗️ 目录结构

```
cn-stock-volume/
├── SKILL.md              # 本文件
├── DESIGN.md             # 详细设计文档
├── scripts/
│   ├── fetch_data.py     # 数据获取核心
│   ├── generate_report.py # 报告生成
│   └── 补数据.py          # 手动补充数据
├── cache/                # 缓存（TTL=24h）
│   └── YYYY-MM-DD.json
├── manual/               # 手动补充数据
│   └── YYYY-MM-DD.json
└── output/               # 输出文件
    ├── report.md
    └── data.json
```

## 📋 数据源

**同花顺问财**（浏览器自动化）

| 数据 | 查询语句 | URL |
|------|----------|-----|
| 上证指数 | `上证指数` | [问财](https://www.iwencai.com/unifiedwap/result?w=上证指数&querytype=zhishu) |
| 深证成指 | `深证成指` | [问财](https://www.iwencai.com/unifiedwap/result?w=深证成指&querytype=zhishu) |
| 创业板指 | `创业板指` | [问财](https://www.iwencai.com/unifiedwap/result?w=创业板指&querytype=zhishu) |
| 上涨家数 | `A 股上涨数量` | [问财](https://www.iwencai.com/unifiedwap/result?w=A 股上涨数量&querytype=zhishu) |
| 下跌家数 | `A 股下跌数量` | [问财](https://www.iwencai.com/unifiedwap/result?w=A 股下跌数量&querytype=zhishu) |

## 🔧 特性

### 缓存机制
- **TTL**: 24 小时
- **位置**: `cache/YYYY-MM-DD.json`
- **作用**: 避免重复调用浏览器，提升速度

### 非交易日处理
- 自动检测周末
- 往前推移直到找到最近交易日
- 最多往前推 7 天

### 手动补充
- 成交量数据需手动补充
- 支持命令行补充（`补数据.py`）
- 支持直接编辑 JSON 文件
- 补充后重新生成报告即可更新

### 错误处理
- 单个数据失败 → 使用占位符 `待补充`
- 不影响其他数据获取
- 清晰的错误提示

## 📝 输出示例

### Markdown

```markdown
# 📊 A 股市场日报 | 2026-03-22

## 三大指数

| 指数 | 点位 | 涨跌幅 |
|------|------|--------|
| 上证指数 | 3957.05 | 📉 -1.24% |
| 深证成指 | 13866.20 | 📉 -0.25% |
| 创业板指 | 3352.10 | 📈 +1.30% |

## 成交量

- **今日量能**：1.23 万亿
- **量能变化**：缩量 0.07 万亿 (-5.69%)
- **市场情绪**：🟢 缩量调整

## 涨跌家数

- **上涨**：1234 家
- **下跌**：3456 家
- **涨跌比**：≈ 1:2.8（下跌显著多于上涨）
```

### JSON

```json
{
  "date": "2026-03-22",
  "indices": {
    "shanghai": { "point": 3957.05, "change": -1.24 },
    "shenzhen": { "point": 13866.20, "change": -0.25 },
    "chinext": { "point": 3352.10, "change": 1.30 }
  },
  "volume": {
    "today": 1.23,
    "previous": 1.30,
    "change": -0.07,
    "changePercent": -5.38,
    "type": "缩量"
  },
  "sentiment": {
    "up": 1234,
    "down": 3456,
    "ratio": "1:2.8",
    "description": "下跌显著多于上涨"
  }
}
```

## ⚠️ 注意事项

1. **浏览器依赖**: 需要 OpenClaw browser 工具可用（自动获取数据时）
2. **网络要求**: 需要能访问同花顺问财网站
3. **成交量手动补充**: 目前不支持自动获取，需手动补充
4. **缓存清理**: 手动删除 `cache/` 目录可清空缓存
5. **非交易日**: 周末自动往前推，可能不是用户期望的日期

## 🛠️ 开发状态

- [x] 目录结构创建
- [x] 数据获取框架（fetch_data.py）
- [x] 报告生成脚本（generate_report.py）
- [x] 手动补充脚本（补数据.py）
- [x] 缓存逻辑
- [x] 非交易日处理
- [x] 浏览器工具集成（调用 OpenClaw browser.snapshot）
- [x] 数据解析逻辑（解析 snapshot 文本）
- [x] 完整流程测试（2026-03-22 测试通过）

## 📖 相关文档

- [DESIGN.md](DESIGN.md) - 详细设计文档

## 💡 使用技巧

### 批量补充多日数据

```bash
# 连续补充 3 天数据
python3 scripts/补数据.py 2026-03-20 -t 1.20 -p 1.25
python3 scripts/补数据.py 2026-03-21 -t 1.25 -p 1.20
python3 scripts/补数据.py 2026-03-22 -t 1.23 -p 1.25
```

### 查看缓存状态

```bash
ls -lh cache/
```

### 查看手动数据

```bash
cat manual/2026-03-22.json
```
