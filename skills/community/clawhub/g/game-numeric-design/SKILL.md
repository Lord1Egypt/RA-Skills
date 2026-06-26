---
name: game-numeric-design
description: 游戏数值策划技能 - 基于《游戏数值设定入门》方法论，提供数值设计公式、经济系统、成长曲线等工具
metadata:
  openclaw:
    emoji: "📊"
author: 太子
dependencies: []
---

# 游戏数值策划技能

基于《游戏数值设定入门》的方法论，提供游戏数值设计工具。

## 核心方法论

### 五特性模型

任何数值模块都具备五个特性：

| 特性 | 说明 | 示例 |
|------|------|------|
| 生成 | 模块产生的原因和过程 | 怪物生成、装备掉落 |
| 成长 | 从起始到成型的轨迹 | 等级提升、属性成长 |
| 消亡 | 消失和灭亡 | 装备淘汰、技能失效 |
| 变化 | 不单向成长，受环境影响 | 属性波动、爆率变化 |
| 联系 | 模块之间的关系 | 装备影响战斗力 |

### 数值设定流程

```
1. 基本功能假设
2. 建立数据模型
3. 设定数值方向
4. 调整数值实现方向
5. 验证并输出
```

## 公式工具库

### 1. 加减乘除

适用于：线性变化、直观数值

```javascript
// 力量影响攻击：每点力量+1攻击
attack = baseAttack + strength * 1

// 升级经验：等差数列
expToLevel = baseExp + level * 1000

// 伤害公式：减法
damage = attack - defense
```

### 2. 幂函数

适用于：成长曲线、边际效应

```javascript
// 升级经验：先易后难 (i < 1)
exp = 1000 * Math.pow(level, 0.667)

// COMBO得分：指数爆炸 (i > 1)
comboScore = base * Math.pow(2, comboCount)

// 经验衰减 (i < 0)
attr = baseMax / (max - current)
```

### 3. 数组/数列

适用于：固定数值表、阶段成长

```javascript
// 等差数列：每5级多获得1点
pointPerLevel = 3 + Math.floor(level / 5)

// 等比数列：金币产出
gold = baseGold * Math.pow(1.1, level)

// 斐波那契：资源消耗
cost = fibonacci(level)
```

### 4. 正态分布

适用于：随机几率、波动数值

```javascript
// 骰子模型：xdy
function roll(x, y) {
  let sum = 0;
  for (let i = 0; i < x; i++) {
    sum += Math.floor(Math.random() * y) + 1;
  }
  return sum;
}

// 爆率计算
function getDropRate(baseRate, luck) {
  return baseRate * (1 + luck / 1000);
}
```

## 模块设计模板

### 属性模块

```javascript
// 属性设计原则
const ATTR_GROWTH = {
  // 分段函数：1-10级每级3点，11-20级每级4点
  pointPerLevel: (level) => 3 + Math.floor((level - 1) / 10),
  
  // 公式：敏捷影响闪避
  dodge: (agility) => agility / 30,
  
  // 临界值：属性达到某值后效果递减
  criticalEffect: (value, threshold) => {
    if (value <= threshold) return value;
    return threshold + (value - threshold) * 0.5;
  }
};
```

### 怪物模块

```javascript
// 怪物数值模板
const MONSTER_TEMPLATE = {
  // 生命值：等比增长
  hp: (level) => Math.floor(100 * Math.pow(1.15, level - 1)),
  
  // 攻击力：等比增长
  attack: (level) => Math.floor(10 * Math.pow(1.12, level - 1)),
  
  // 掉落：品质概率
  dropTable: {
    white: 0.50,
    green: 0.30,
    blue: 0.15,
    purple: 0.04,
    gold: 0.01
  }
};
```

### 装备模块

```javascript
// 装备属性价值
const EQUIPMENT_VALUE = {
  // 属性换算比例
  valuePerPoint: {
    damage: 10,
    defense: 8,
    hp: 1,
    speed: 5
  },
  
  // 品质加成
  qualityMultiplier: {
    white: 1.0,
    green: 1.5,
    blue: 2.0,
    purple: 3.0,
    gold: 5.0
  }
};
```

### 经济系统

```javascript
// 经济系统设计
const ECONOMY = {
  // 产出
  income: {
    monster: (level) => level * 10,
    quest: (questId) => QUEST_REWARDS[questId],
    daily: 100
  },
  
  // 支出
  expense: {
    upgrade: (currentLevel) => 50 * Math.pow(1.5, currentLevel),
    repair: (maxDurability) => Math.ceil(maxDurability * 0.1),
    shop: (item) => item.basePrice * 1.2
  },
  
  // 平衡检查
  balanceCheck: (income, expense, targetRatio = 1.2) => {
    return income / expense >= targetRatio;
  }
};
```

## 数值方向确定

### 方法

1. **确定目标**：玩家在X级时能完成Y
2. **反推数值**：根据目标计算所需数值
3. **验证调整**：通过公式验证可行性

### 示例：战斗平衡

```javascript
// 目标：玩家5级时，使用技能可险胜同级怪物
const TARGET = {
  playerLevel: 5,
  monsterLevel: 5,
  winCondition: '险胜(需吃药1次)'
};

// 计算：玩家攻击 * 攻击次数 = 怪物HP
// 怪物攻击 * 攻击次数 = 玩家HP
function calculateBalance(target) {
  const playerAtk = 16 * target.playerLevel;
  const playerHp = 100 + target.playerLevel * 20;
  const monsterAtk = 10 * target.monsterLevel;
  const monsterHp = 300 * Math.pow(1.1, target.monsterLevel - 1);
  
  const playerKillTime = monsterHp / playerAtk;
  const monsterKillTime = playerHp / monsterAtk;
  
  return {
    playerKillTime,
    monsterKillTime,
    balanced: Math.abs(playerKillTime - monsterKillTime) < 2
  };
}
```

## 快速参考

| 场景 | 推荐公式 |
|------|----------|
| 升级经验 | 幂函数 (i<1 先易后难) |
| 装备属性 | 品质倍率 |
| 怪物强度 | 等比数列 |
| 技能伤害 | 基础 + 系数 * 等级 |
| 爆率 | 正态分布/数组 |
| 经济产出 | 等差 + 浮动 |

## 使用示例

当需要设计游戏数值时：

1. 确定模块类型（属性/装备/怪物/经济）
2. 选择合适公式
3. 用模板生成数值
4. 验证平衡性
5. 调整参数
