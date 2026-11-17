# 使用示例

## 示例 1：一句话生成周报（最常用）

用户说：**「生成这周的使用报告」**

技能自动执行：

```bash
# 采集最近 7 天数据
python scripts/collect_usage_data.py --period week --output data.json
# 生成 Markdown 报告
python scripts/generate_report.py data.json --output 使用情况报告.md
```

输出开头示意：

```markdown
# Workbuddy使用情况报告

> **报告周期**：2026-07-27 至 2026-08-02
> **报告类型**：周报 · 2026 年第31周（2026-07-27 至 2026-08-02）

## 一、概览统计
| 指标 | 数值 |
|------|------|
| 活跃天数 | 7 天 |
| 会话总数 | 18 个 |
| 总 Token 消耗 | 14.91M |
| 实际花费 | ¥10.26 |
```

## 示例 2：指定月份出月报

用户说：**「生成 7 月的使用报告」**

```bash
python scripts/generate_report.py --start 2026-07-01 --end 2026-07-31 --output 七月报告.md
```

采集器自动识别为「月报 · 2026年7月」。

## 示例 3：要 HTML 版 + JSON 版

```bash
python scripts/generate_report.py --period month --output report.html --format html
python scripts/generate_report.py --period month --output report.json --format json
```

HTML 版含交互图表、浅/深色自适应；JSON 版供程序处理。
