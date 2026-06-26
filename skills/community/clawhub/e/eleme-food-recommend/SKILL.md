---
name: eleme-food-recommend
version: 1.0.0
description: 饿了么外卖推荐技能，根据用户饭点和口味偏好推荐附近外卖
author: your-name
homepage: https://github.com/your-name/eleme-food-recommend
---

# 饿了么外卖推荐 Skill

根据用户的饭点设置和口味偏好，在饭点前推荐附近外卖店铺的菜品。

## 功能

- 设置用户饭点（早餐、午餐、晚餐时间）
- 设置口味偏好（清淡、重口、微辣、中辣等）
- 设置每日推荐菜品数量
- 根据定位获取附近外卖店
- 智能推荐符合口味的菜品

## 使用

```bash
# 设置用户信息（cookie、饭点、口味、数量）
python main.py set-config --cookie "your_eleme_cookie" --breakfast "07:30" --lunch "11:30" --dinner "18:30" --flavor "清淡" --count 3

# 获取今日推荐
python main.py recommend

# 查看当前配置
python main.py show-config
```
