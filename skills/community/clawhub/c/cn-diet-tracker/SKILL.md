---
slug: cn-diet-tracker
name: 饮食记录追踪
version: "1.0.0"
author: 千策
---

# 🥗 CN Diet Tracker — 中文饮食记录

记录饮食，关注健康。

## 核心功能

| 功能 | 说明 |
|------|------|
| 记录饮食 | 一句话记录：食物名+估算热量 |
| 热量统计 | 今日/本周摄入 |
| 营养分析 | 碳水/蛋白/脂肪占比 |
| 目标管理 | 设定每日热量目标 |

## 使用方式

```bash
# 记录一餐
python3 scripts/diet.py --add "白米饭一碗" 230 --category 主食
python3 scripts/diet.py --add "番茄炒蛋" 180 --category 菜品
python3 scripts/diet.py --add "苹果" 80 --category 水果

# 今日统计
python3 scripts/diet.py --today

# 设定目标
python3 scripts/diet.py --target 2000

# 周报
python3 scripts/diet.py --week
```

## 数据存储

本地 JSON：~/.qclaw/workspace/diet.json

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
