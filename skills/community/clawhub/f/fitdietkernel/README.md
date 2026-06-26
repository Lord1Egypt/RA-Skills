# FitDietKernel 🏋️

> **健身饮食的个人知识库**  
> 无论你用什么饮食方法，AI 都能精准帮你算

[![Stars](https://img.shields.io/github/stars/yibinpro/FitDietKernel?style=flat&color=2ecc71)](https://github.com/yibinpro/FitDietKernel)
[![License](https://img.shields.io/github/license/yibinpro/FitDietKernel)](https://github.com/yibinpro/FitDietKernel)

---

## ⚡ 快速安装 (OpenClaw / Claude Code)

```bash
# 方法1: 通过 ClawHub 安装 (推荐)
npx clawhub@latest install fitdietkernel

# 方法2: 手动安装
git clone https://github.com/yibinpro/FitDietKernel.git ~/fitdietkernel
```

### 配置 AI 助手

安装后告诉 AI：

```
你是一个精准饮食教练，接入了 FitDietKernel 个人知识库。

规则：
1. 优先读取 profile.json 获取我的体重、目标、饮食法
2. 查 knowledge_base/food_registry.json 计算食物数据
3. 查 knowledge_base/rules.md 执行凯圣王算法
4. 每天结束后生成 logs/YYYY-MM-DD.md 打卡记录
5. 碳水误差超过10g要警告我

数据路径：~/fitdietkernel/
```

---

## 🎯 解决什么问题

健身最痛的点：

| 痛点 | 传统 AI | FitDietKernel |
|------|---------|---------------|
| "这个能吃吗" | "馒头碳水高，少吃" | "1个=18.5g碳水，今天MC日能吃2个" |
| "今天吃超了吗" | "大概没超吧" | "实际52g，目标147g，-95g安全" |
| "上次那个食物呢" | "抱歉我忘了" | **永远记得** |

---

## 🏗️ 项目结构

```
FitDietKernel
├── profile.json              # 你是谁：体重、目标、饮食法
├── knowledge_base/
│   ├── food_registry.json    # 你的食物数据库（精准数据）
│   ├── recipes.json         # 验证过的食谱
│   └── rules.md              # 核心规则
└── logs/
    ├── 2026-04-06.md         # 每日打卡
    └── weekly_report/        # AI 周报
```

---

## 🥋 支持的饮食方法

| 饮食法 | 配置示例 |
|--------|----------|
| **碳循环** | 低95g / 中147g / 高315g |
| **生酮** | 碳水<30g，脂肪>70% |
| **增肌** | 碳水400g+，蛋白200g+ |
| **减脂** | 碳水150g，蛋白180g |
| **16:8间歇断食** | 进食窗口 12:00-20:00 |

---

## 🚀 快速开始

### 1. Fork 项目

点击右上角 Fork，修改成你的数据

### 2. 配置你的档案

```json
// profile.json
{
  "name": "你的名字",
  "currentWeight": 80,
  "targetWeight": 75,
  "height": 175,
  "age": 30,
  "activityLevel": "moderate",
  "dietType": "carbon_cycling"
}
```

**碳循环计算公式**（AI 自动帮你算）：

```
基础代谢 (BMR) = 体重(kg) × 23
运动消耗 (TDEE) = BMR × 1.4 ~ 1.6

// 碳水：按体重倍数
低碳日碳水 = 体重 × 1.0g
中碳日碳水 = 体重 × 1.5g  
高碳日碳水 = 体重 × 3.0g

// 蛋白：固定值，增肌/保持 1.5~2g/kg，减脂 2~2.5g/kg
蛋白 = 体重 × 1.5~2.0g

// 脂肪：剩余热量
脂肪 = (TDEE - 碳水×4 - 蛋白×4) / 9
```

比如 80kg 体重：
- **碳水**：低80g / 中120g / 高240g
- **蛋白**：120~160g (固定)
- **脂肪**：低碳日多点，高碳日少点

### 3. 接入 AI（OpenClaw 示例）

```
你是一个精准饮食教练。

规则：
1. 读 profile.json 获取我的饮食目标和预算
2. 查 food_registry.json 计算食物数据
3. 告诉我今天还能吃多少
```

---

## 💡 核心功能

### 🔢 精准计算

```
问：今天能吃几个馒头？
答：
- 你的馒头：1个 = 18.5g 碳水
- 今天是 MC 日，预算 147g
- 已吃：65g燕麦 + 50g蓝莓 = 40g
- 剩余：107g
- 可以吃：5.7个
```

### 📊 误差追踪

| 周 | 平均误差 | 状态 |
|----|----------|------|
| 第1周 | +8g | 🟢 |
| 第2周 | -5g | 🟢 |
| 第3周 | +22g | 🟡 需注意 |

### 🔄 新食物注册

```
"把这个贝果存入，1个=25g碳水，早餐用"
```

AI 自动更新数据库，下次直接查。

---

## 📖 谁适合用

- 🏋️ 任何健身饮食法的人
- 🥗 碳循环 / 生酮 / 增肌 / 减脂 / 间歇断食
- 🤖 用 AI 辅助健身的人

---

## 🔧 技术细节

- 数据存本地/GitHub，隐私安全
- 纯 JSON + Markdown，无数据库
- 配合任意 AI（ChatGPT/OpenClaw/Claude）

---

## 🤝 欢迎贡献

Fork 项目，添加你的饮食法配置，分享给更多人！

---

## 📄 License

MIT - 你自己的数据，存在你自己的仓库。

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=yibinpro-FitDietKernel&label=Views&color=2ecc71" alt="Views">
</p>