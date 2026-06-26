---
slug: cn-countdown
name: 倒计时工具
version: "1.0.0"
author: 千策
---

# 📅 CN Countdown — 中文倒数日/纪念日计算器

记录重要日子，计算距离今天还有多少天，或已经过去了多少天。

## 核心功能

| 功能 | 说明 |
|------|------|
| 添加日子 | 添加任意重要日期，支持名称、标签 |
| 倒计时 | 显示距离目标日期还有多少天 |
| 已过天数 | 显示从某天起已经过去了多久 |
| 农历支持 | 自动识别农历生日并计算 |
| 列表展示 | 彩色表格，一目了然 |
| 编辑/删除 | 管理已记录的日子 |

## 使用方式

```bash
# 查看所有记录的日子（默认按倒计时排序）
python3 scripts/countdown.py --list

# 添加一个日子（默认算倒计时）
python3 scripts/countdown.py --add "春节" --date "2026-02-17" --tag "节日"

# 添加生日（自动标注年龄）
python3 scripts/countdown.py --add "妈妈的生日" --date "1965-05-20" --tag "生日"

# 添加纪念日（从那天起过了多久）
python3 scripts/countdown.py --add "在一起纪念日" --date "2020-09-01" --tag "纪念日"

# 添加考试倒计时
python3 scripts/countdown.py --add "高考" --date "2026-06-07" --tag "考试"

# 查看已过天数（从某天到现在）
python3 scripts/countdown.py --since "2020-01-01"

# 查看距离某天（从今天到目标）
python3 scripts/countdown.py --to "2026-07-01"

# 删除一条记录
python3 scripts/countdown.py --delete "春节"

# 编辑日子
python3 scripts/countdown.py --edit "春节" --new-date "2026-02-16"
```

## 数据存储

数据保存在 `~/.qclaw/workspace/countdown.json`，纯本地，无账户，无云端。

## 标签说明

- `生日` — 显示年龄和今年生日倒计时
- `纪念日` — 显示在一起/结婚等已过天数
- `考试` — 突出显示紧迫感
- `节日` — 农历/传统节日
- `目标` — 个人目标达成日
- `其他` — 自定义

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
