---
name: cocktail-boy
description: 你的私人调酒师 - 提供鸡尾酒推荐、配方查询和调制指南。支持搜索特定鸡尾酒、按原料查找、随机推荐和场景化推荐。数据库中包含 1635+ 款鸡尾酒配方！
---

# cocktail-boy - 你的私人调酒师 🍸

## 功能描述
根据用户需求提供鸡尾酒推荐、配方查询和调制指南。用户可以：
- 搜索特定鸡尾酒名称
- 按原料查找鸡尾酒
- 获取详细的调制步骤
- 推荐适合场景的鸡尾酒

## 使用方法

### 1. **查询特定鸡尾酒**
```
/cocktail [酒名]
例如：/cocktail mojito, /cocktail margarita
```

### 2. **搜索含某原料的鸡尾酒**
```
/search-ingredients [原料名]
例如：/search-ingredients vodka, /search-ingredients gin
```

### 3. **推荐鸡尾酒（随机）**
```
/recommend
```

### 4. **按场景推荐**
```
/scene [场景描述]
例如：/scene 约会晚上，/scene 聚会喝酒
```

## 技能脚本位置
`~/.openclaw/workspace/skills/cocktail-boy/`

## 配置文件路径
- 数据库：`cocktail-db/rohan_cocktails.csv` (1635 个配方)
- 主脚本：`scripts/query.sh`
- 快捷命令：`~/.bashrc` (可选)

---

_Ready to mix! 🍹_
