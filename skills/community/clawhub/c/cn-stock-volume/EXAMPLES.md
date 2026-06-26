# cn-stock-volume - 完整使用示例

## 🎯 快速开始（3 步完成）

### 步骤 1：生成报告（自动获取指数 + 涨跌家数）

```bash
cd ~/.jvs/.openclaw/workspace/skills/stock-data-monorepo/cn-stock-volume

python3 scripts/generate_report.py
```

**输出示例：**
```
[INFO] 生成报告：2026-03-22
[INFO] 重新获取数据：2026-03-22
[INFO] 获取 上证指数 数据...
[INFO] 获取 深证成指 数据...
[INFO] 获取 创业板指 数据...
[INFO] 获取 up 数据...
[INFO] 获取 down 数据...
[INFO] 缓存已保存：.../cache/2026-03-22.json

✅ 报告生成完成！

📁 Workspace 输出:
   Markdown: .../output/stock-report-2026-03-22.md
   JSON: .../output/data-2026-03-22.json

📁 Desktop 输出:
   Markdown: /Users/shinelp100/Desktop/A 股每日复盘/stock-report-2026-03-22.md
   JSON: /Users/shinelp100/Desktop/A 股每日复盘/data-2026-03-22.json
```

### 步骤 2：查看报告

```bash
cat ~/Desktop/A\ 股每日复盘/stock-report-2026-03-22.md
```

**报告内容示例：**
```markdown
# 📊 A 股市场日报 | 2026-03-22

## 三大指数

| 指数 | 点位 | 涨跌幅 |
|------|------|--------|
| 上证指数 | 3957.05 | 📉 -1.24% |
| 深证成指 | 13866.20 | 📉 -0.25% |
| 创业板指 | 3352.10 | 📈 +1.30% |

## 成交量

- **今日量能**：待补充
- **量能变化**：待补充

## 涨跌家数

- **上涨**：662 家
- **下跌**：4786 家
- **涨跌比**：≈ 1:7.2（下跌显著多于上涨）
```

### 步骤 3：补充成交量数据（可选）

```bash
# 补充今日和昨日成交量（单位：万亿）
python3 scripts/补数据.py 2026-03-22 --today 1.23 --previous 1.30

# 重新生成报告
python3 scripts/generate_report.py 2026-03-22
```

**重新生成后的报告：**
```markdown
## 成交量

- **今日量能**：1.23 万亿
- **量能变化**：缩量 0.07 万亿 (-5.38%)
- **市场情绪**：🟢 缩量调整
```

---

## 📚 常用命令速查

### 查询操作

```bash
# 查询今日
python3 scripts/generate_report.py

# 查询指定日期
python3 scripts/generate_report.py 2026-03-22

# 强制刷新（忽略缓存）
python3 scripts/generate_report.py --force

# 仅输出 JSON（不保存文件）
python3 scripts/generate_report.py --json

# 仅输出 Markdown（不保存文件）
python3 scripts/generate_report.py --markdown
```

### 数据补充

```bash
# 补充成交量数据
python3 scripts/补数据.py 2026-03-22 --today 1.23 --previous 1.30

# 查看已补充的数据
python3 scripts/补数据.py 2026-03-22 --show

# 清除已补充的数据
python3 scripts/补数据.py 2026-03-22 --clear
```

### 简写参数

```bash
# 使用简写参数
python3 scripts/补数据.py 2026-03-22 -t 1.23 -p 1.30
```

---

## 📁 文件位置

| 文件类型 | 路径 | 说明 |
|----------|------|------|
| **报告（Markdown）** | `~/Desktop/A 股每日复盘/stock-report-YYYY-MM-DD.md` | 人类阅读 |
| **数据（JSON）** | `~/Desktop/A 股每日复盘/data-YYYY-MM-DD.json` | 程序调用 |
| **缓存** | `.../cn-stock-volume/cache/YYYY-MM-DD.json` | 自动缓存，TTL=24h |
| **手动数据** | `.../cn-stock-volume/manual/YYYY-MM-DD.json` | 用户补充的成交量 |
| **脚本** | `.../cn-stock-volume/scripts/` | 所有可执行脚本 |

---

## 🔧 高级用法

### 1. 批量生成多日报告

```bash
# 生成最近 5 天的报告
for date in 2026-03-18 2026-03-19 2026-03-20 2026-03-21 2026-03-22; do
    python3 scripts/generate_report.py $date
done
```

### 2. 批量补充成交量数据

```bash
# 连续补充 5 天数据
python3 scripts/补数据.py 2026-03-18 -t 1.20 -p 1.25
python3 scripts/补数据.py 2026-03-19 -t 1.25 -p 1.20
python3 scripts/补数据.py 2026-03-20 -t 1.18 -p 1.25
python3 scripts/补数据.py 2026-03-21 -t 1.22 -p 1.18
python3 scripts/补数据.py 2026-03-22 -t 1.23 -p 1.22
```

### 3. 在其他脚本中使用 JSON 数据

```python
import json
from pathlib import Path

# 读取 JSON 数据
data_path = Path("~/Desktop/A 股每日复盘/data-2026-03-22.json").expanduser()
data = json.loads(data_path.read_text(encoding='utf-8'))

# 访问数据
print(f"上证指数：{data['indices']['shanghai']['point']}")
print(f"涨跌幅：{data['indices']['shanghai']['change']}%")
print(f"上涨家数：{data['sentiment']['up']}")
print(f"下跌家数：{data['sentiment']['down']}")
print(f"涨跌比：{data['sentiment']['ratio']}")
```

### 4. 查看缓存状态

```bash
# 查看缓存文件
ls -lh cache/

# 查看特定日期的缓存
cat cache/2026-03-22.json | jq .
```

### 5. 清理缓存

```bash
# 清理所有缓存
rm -rf cache/*

# 清理特定日期的缓存
rm cache/2026-03-22.json
```

---

## ⚠️ 常见问题

### Q1: 为什么成交量显示"待补充"？
**A**: 成交量数据目前不支持自动获取，需要手动补充。这是设计决策，因为同花顺问财的成交量数据格式不统一。

### Q2: 如何补充成交量数据？
**A**: 使用 `补数据.py` 脚本：
```bash
python3 scripts/补数据.py 2026-03-22 --today 1.23 --previous 1.30
```

### Q3: 缓存多久过期？
**A**: 24 小时。过期后会自动重新获取数据。

### Q4: 周末查询会怎样？
**A**: 自动往前推到最近交易日（通常是周五）。

### Q5: 如何强制刷新数据？
**A**: 使用 `--force` 参数：
```bash
python3 scripts/generate_report.py --force
```

### Q6: JSON 数据在哪里？
**A**: `~/Desktop/A 股每日复盘/data-YYYY-MM-DD.json`

### Q7: 如何修改已补充的数据？
**A**: 两种方式：
1. 重新运行 `补数据.py` 覆盖：
   ```bash
   python3 scripts/补数据.py 2026-03-22 -t 1.25 -p 1.30
   ```
2. 直接编辑 JSON 文件：
   ```bash
   vim ~/Desktop/A\ 股每日复盘/data-2026-03-22.json
   ```

---

## 📊 输出格式示例

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

- **今日量能**：1.23 万亿
- **量能变化**：缩量 0.07 万亿 (-5.38%)
- **市场情绪**：🟢 缩量调整

## 涨跌家数

- **上涨**：662 家
- **下跌**：4786 家
- **涨跌比**：≈ 1:7.2（下跌显著多于上涨）
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
    "today": 1.23,
    "previous": 1.30,
    "change": -0.07,
    "changePercent": -5.38,
    "type": "缩量"
  },
  "sentiment": {
    "up": 662,
    "down": 4786,
    "ratio": "1:7.2",
    "description": "下跌显著多于上涨"
  }
}
```

---

## 🎯 最佳实践

1. **每日定时生成**：建议每个交易日收盘后（15:30 后）生成报告
2. **补充成交量**：从东方财富或同花顺查看当日成交量后补充
3. **批量处理**：如需补全历史数据，使用循环批量生成
4. **缓存利用**：同一交易日无需重复获取，使用缓存即可
5. **数据备份**：定期备份 `~/Desktop/A 股每日复盘/` 目录

---

## 📖 相关文档

- [SKILL.md](SKILL.md) - 技能完整说明
- [DESIGN.md](DESIGN.md) - 详细设计文档
- [README.md](README.md) - 快速入门
