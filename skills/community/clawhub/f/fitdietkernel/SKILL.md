---
name: fitdietkernel
description: 健身饮食的个人知识库 - 让AI精准帮你算饮食（碳循环/生酮/增肌/减脂）
metadata:
  openclaw:
    emoji: "🏋️"
    category: "productivity"
    tags: ["diet", "fitness", "carbon-cycling", "macro", "health"]
---

# FitDietKernel 🏋️

> 健身饮食的个人知识库，让 AI 成为你的精准饮食教练

## 功能

- 🔢 精准碳水计算（按体重动态计算）
- 🍚 食物注册（10g 碳水等值换算）
- 📊 误差追踪（±10g 安全线）
- 📋 自动打卡记录
- 📈 周报生成

## 计算公式

### 碳循环

```
低碳日 = 体重 × 1.0g
中碳日 = 体重 × 1.5g
高碳日 = 体重 × 3.0g

蛋白 = 体重 × 1.5~2.0g
脂肪 = 剩余热量
```

### 食物换算 (10g 碳水)

| 食材 | 分量 |
|------|------|
| 燕麦 | 16g (干) |
| 意面 | 13g (干) |
| 杂粮馒头 | 0.5个 |
| 蓝莓 | 72g |
| 红薯 | 50g |

## 使用方法

1. 克隆仓库到本地
2. 修改 `profile.json` 配置你的体重、目标
3. 告诉 AI 知识库路径，让它读取数据

```
你是一个精准饮食教练，接入了 FitDietKernel。
数据路径：~/fitdietkernel/
```