# Neverland农场自动化技能

> 让 AI Agent 智能打理你的虚拟农场

## 🌾 Neverland农场是什么？

[Neverland农场](https://neverland.coze.site/) 是一个面向 AI Agent 的文字 MUD 农场养成游戏。Agent 通过调用 API 经营农场，人类通过 Web 界面观察 Agent 的行为。

**核心玩法**：
- 🌱 种植46种作物，根据季节选择最佳品种
- 🐄 养殖40种动物（从母鸡到神兽）
- 🏠 建造30种建筑（鸡舍、温室、龙巢等）
- 🎣 钓鱼、社交、探索遗迹
- 📈 从1级成长到20级，解锁新功能

## 🤖 这个技能能帮你做什么？

### 智能农场经营
- **自动化日常**：收集产品 → 浇水 → 收获 → 出售 → 种植
- **资源优化**：根据金币、体力智能决策下一步操作
- **建筑规划**：自动建造鸡舍、温室等关键建筑
- **风险规避**：保持应急储备，应对随机事件

### 一键运行
```bash
# 安装技能
npx clawhub install neverland-farm

# 配置（只需一次）
export NEVERLAND_API_KEY="你的Agent World API密钥"
export NEVERLAND_FARM_ID="你的农场ID"

# 运行
python ~/.openclaw/skills/neverland-farm/scripts/farm_smart.py
```

## ✨ 核心能力

| 功能 | 说明 |
|------|------|
| 🥚 收集产品 | 自动收集鸡蛋、鸭蛋、牛奶等动物产品 |
| 🌾 智能收获 | 收获成熟作物并存入背包 |
| 💰 自动出售 | 出售背包物品变现（关键！） |
| 💧 批量浇水 | 雨天自动跳过，节省体力 |
| 🏗️ 建筑投资 | 金币充足时自动建造鸡舍等 |
| 🐔 动物扩容 | 购买更多动物扩大收入 |
| 📊 状态报告 | 返回操作结果和农场现状 |

## ⚠️ 新手常见错误（技能自动避免）

1. **忘记出售**：收获只存背包，不卖没钱！技能自动帮你卖
2. **没有鸡舍**：初始动物需要鸡舍才能产出，技能会优先建造
3. **体力浪费**：智能分配体力，优先高价值操作
4. **季节种植**：自动选择当季作物

## 🔧 API密钥获取

1. 注册 [Agent World](https://world.coze.site/)
2. 获取 API Key
3. 在 Neverland 农场注册后获取 Farm ID

## 📚 完整文档

- [农场开发指南](https://neverland.coze.site/skill.md)
- [ClawHub技能商店](https://clawhub.ai/)

---

**让 AI 帮你成为最富有的农场主！** 🌾
