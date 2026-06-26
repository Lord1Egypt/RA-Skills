# cn-stock-volume v3.0 - 设计文档

## 📊 数据需求

### 自动获取数据（浏览器）

| 指标 | 数据源 | 查询语句 | 示例 |
|------|--------|----------|------|
| **上证指数** | 同花顺问财 | `上证指数` | 3957.05 点，-1.24% |
| **深证成指** | 同花顺问财 | `深证成指` | 13866.20 点，-0.25% |
| **创业板指** | 同花顺问财 | `创业板指` | 3352.10 点，+1.30% |
| **上涨家数** | 同花顺问财 | `A 股上涨数量` | 1234 家 |
| **下跌家数** | 同花顺问财 | `A 股下跌数量` | 3456 家 |

### 手动补充数据（占位符）

| 指标 | 说明 | 默认值 |
|------|------|--------|
| **今日量能** | 四市总成交金额 | `待补充` |
| **昨日量能** | 前一交易日成交金额 | `待补充` |
| **量能变化** | 自动计算（如补充了数据） | `待补充` |

---

## 🏗️ 架构设计

```
cn-stock-volume/
├── SKILL.md              # 技能说明文档
├── DESIGN.md             # 设计文档（本文件）
├── scripts/
│   ├── fetch_data.py     # 核心数据获取脚本
│   ├── generate_report.py # 报告生成脚本
│   └──补数据.py          # 手动补充数据脚本
├── cache/                # 缓存目录
│   └── YYYY-MM-DD.json   # 按日期缓存
├── manual/               # 手动补充数据
│   └── YYYY-MM-DD.json   # 用户补充的数据
└── output/
    ├── report.md         # Markdown 报告
    └── data.json         # JSON 数据
```

---

## 📝 输出格式

### Markdown 报告

```markdown
# 📊 A 股市场日报 | 2026-03-22

## 三大指数

| 指数 | 点位 | 涨跌幅 |
|------|------|--------|
| 上证指数 | 3957.05 | 📉 -1.24% |
| 深证成指 | 13866.20 | 📉 -0.25% |
| 创业板指 | 3352.10 | 📈 +1.30% |

## 成交量

- **今日量能**：`待补充`
- **量能变化**：`待补充`

## 涨跌家数

- **上涨**：1234 家
- **下跌**：3456 家
- **涨跌比**：≈ 1 : 2.8（下跌显著多于上涨）
```

### JSON 数据

```json
{
  "date": "2026-03-22",
  "indices": {
    "shanghai": { "point": 3957.05, "change": -1.24 },
    "shenzhen": { "point": 13866.20, "change": -0.25 },
    "chinext": { "point": 3352.10, "change": 1.30 }
  },
  "volume": {
    "today": null,
    "previous": null,
    "change": null,
    "changePercent": null,
    "type": "待补充"
  },
  "sentiment": {
    "up": 1234,
    "down": 3456,
    "ratio": "1:2.8",
    "description": "下跌显著多于上涨"
  },
  "meta": {
    "cached": false,
    "dataSource": "iwencai",
    "manualDataRequired": ["volume.today", "volume.previous"]
  }
}
```

---

## 🔧 技术实现

### 浏览器调用流程

1. 使用 OpenClaw `browser` 工具访问问财 URL
2. 调用 `browser.snapshot` 获取页面内容
3. 解析 snapshot 文本，提取数据
4. 保存到缓存

### 问财 URL 格式

```
https://www.iwencai.com/unifiedwap/result?w={查询语句}&querytype=zhishu
```

| 数据 | 查询语句 (w=) | 完整 URL |
|------|--------------|----------|
| 上证指数 | `上证指数` | `https://www.iwencai.com/unifiedwap/result?w=上证指数&querytype=zhishu` |
| 深证成指 | `深证成指` | `https://www.iwencai.com/unifiedwap/result?w=深证成指&querytype=zhishu` |
| 创业板指 | `创业板指` | `https://www.iwencai.com/unifiedwap/result?w=创业板指&querytype=zhishu` |
| 上涨家数 | `A 股上涨数量` | `https://www.iwencai.com/unifiedwap/result?w=A 股上涨数量&querytype=zhishu` |
| 下跌家数 | `A 股下跌数量` | `https://www.iwencai.com/unifiedwap/result?w=A 股下跌数量&querytype=zhishu` |

### 数据解析规则

**指数数据格式**：
```
上证指数 (000001) 3957.05-49.50/-1.24%
                    ↑点位  ↑涨跌额  ↑涨跌幅
```

解析目标：
- 点位：`3957.05`
- 涨跌幅：`-1.24`

**涨跌家数格式**：
```
下跌家数为 4785 家
```

解析目标：
- 下跌家数：`4785`

### 手动补充数据

**补充方式 1**：编辑 JSON 文件
```bash
# 创建/编辑手动数据文件
vim manual/2026-03-22.json
```

内容：
```json
{
  "volume": {
    "today": 1.23,
    "previous": 1.30
  }
}
```

**补充方式 2**：使用补数据.py 脚本
```bash
python3 scripts/补数据.py 2026-03-22 --today 1.23 --previous 1.30
```

**补充方式 3**：在生成的 JSON 中直接修改
```bash
vim ~/Desktop/A 股每日复盘/data-2026-03-22.json
```

### 缓存策略

- **缓存位置**：`cache/YYYY-MM-DD.json`
- **TTL**：24 小时
- **缓存键**：日期
- **检查逻辑**：启动时先检查缓存，有有效缓存则直接使用

### 非交易日处理

- 检测目标日期是否为交易日（排除周末）
- 如为非交易日，自动往前推一天
- 递归检查，直到找到最近的交易日
- 最多往前推 7 天，超过则报错

### 错误处理

| 场景 | 处理方式 |
|------|----------|
| 单个数据获取失败 | 使用占位符 `待补充`，继续获取其他数据 |
| 全部数据获取失败 | 返回错误，提示检查网络 |
| 缓存读取失败 | 忽略缓存，重新获取 |
| 解析失败 | 使用占位符 `待补充`，记录日志 |

---

## 🚀 使用方式

### 命令行

```bash
# 查询今日（自动获取 + 占位符）
python3 scripts/generate_report.py

# 查询指定日期
python3 scripts/generate_report.py 2026-03-22

# 强制刷新（忽略缓存）
python3 scripts/generate_report.py --force

# 仅输出 JSON
python3 scripts/generate_report.py --json

# 补充手动数据
python3 scripts/补数据.py 2026-03-22 --today 1.23 --previous 1.30

# 重新生成报告（使用补充的数据）
python3 scripts/generate_report.py 2026-03-22
```

### 其他 Skill 调用

```python
import json
from pathlib import Path

# 读取 JSON 数据
data_path = Path("~/Desktop/A 股每日复盘/data-2026-03-22.json").expanduser()
data = json.loads(data_path.read_text())

# 访问数据
print(f"上证指数：{data['indices']['shanghai']['point']}")
print(f"上涨家数：{data['sentiment']['up']}")
```

---

## 📅 开发计划

- [x] 创建目录结构
- [x] 实现数据获取框架（fetch_data.py）
- [x] 实现缓存逻辑
- [x] 实现报告生成脚本（generate_report.py）
- [ ] 实现浏览器工具集成
- [ ] 实现数据解析逻辑
- [ ] 实现手动补充脚本（补数据.py）
- [ ] 测试非交易日处理
- [ ] 测试错误处理
- [ ] 编写使用文档
