---
name: divination-oracle
description: "易经八卦起卦与解读技能。基于梅花易数算法进行起卦，结合AI大模型解读卦象辞与变爻含义。"
location: ~/clawd/skills/divination-oracle/SKILL.md
---

# Divination Oracle

易经起卦与解读助手。

## 使用方法

### 起卦
```bash
# 基于当前时间起卦
divination-oracle divine "我今天的工作运势如何？"
```

## 模块
- `engine/`: 梅花易数计算逻辑
- `data/`: 64卦数据库
- `docs/`: 占卜心法说明
