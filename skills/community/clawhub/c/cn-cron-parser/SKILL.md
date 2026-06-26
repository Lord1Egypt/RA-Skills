slug: cn-cron-parser
name: Cron表达式解析
version: "1.0.0"
author: 千策

# Cron表达式解析


解析Cron表达式，生成人类可读的时间描述，计算下次执行时间。

## 功能

- Cron表达式解析
- 生成人类可读描述
- 计算下次执行时间
- 常用模板生成

## 使用方法

```bash
# 解析Cron表达式
python3 cn_cron_parser.py "0 9 * * *"
python3 cn_cron_parser.py "*/15 * * * *"

# 计算下次执行时间
python3 cn_cron_parser.py "0 9 * * *" --next

# 生成常用模板
python3 cn_cron_parser.py --templates
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `cron` | Cron表达式 | 必填 |
| `--next` | 显示下次执行时间 | False |
| `--templates` | 显示常用模板 | False |

## Cron格式

```
┌───────────── 分钟 (0 - 59)
│ ┌─────────── 小时 (0 - 23)
│ │ ┌───────── 日期 (1 - 31)
│ │ │ ┌────── 月份 (1 - 12)
│ │ │ │ ┌──── 星期 (0 - 6, 0=周日)
│ │ │ │ │
* * * * *
```

## 示例

```bash
# 每天早上9点
python3 cn_cron_parser.py "0 9 * * *"

# 每15分钟
python3 cn_cron_parser.py "*/15 * * * *"

# 每周一早上9点
python3 cn_cron_parser.py "0 9 * * 1"

# 每月1号凌晨
python3 cn_cron_parser.py "0 0 1 * *"
```

## 依赖

- Python 3.x
- croniter (pip install croniter)

## 注意事项

- Cron格式：分 时 日 月 周
- 星期：0=周日，1=周一，以此类推

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
