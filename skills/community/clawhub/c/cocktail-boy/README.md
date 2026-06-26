# 🍹 Cocktail-Boy - 私人调酒师

## 🎯 功能

帮你查询和推荐鸡尾酒配方！数据库包含 **1635** 款鸡尾酒，中英文均可。

## 📋 常用命令

### 查询特定鸡尾酒
```
 mojito, margarita, old fashioned, tequila sunrise, daiquiri...
```

### 按原料查找
```
/vodka /gin /rum /whiskey /tequila /brandy
/lemon /lime /orange /mint ...
```

### 随机推荐
```
/recommend
```

## 💡 使用示例

**主人**: "我想喝 mojito"  
**Jarvis**: 🍸 正在搜索 Mojito...
  - Mint Leaf - 8 (Muddle)
  - Banks 5 Island Rum - 2oz (Build)
  - Club Soda - 1oz (Top)
  - Simple Syrup - 1oz (Build)
  - Lime Juice - 0.75oz (Build)
  
  **🧊 调制方法**: Shake with ice and fine-strain into a chilled Collins glass filled with ice

---

**主人**: "有什么含威士忌的酒推荐吗？"  
**Jarvis**: 🔍 正在查找含 whiskey 的鸡尾酒...
  ✅ 找到了 47 款包含 whiskey 的鸡尾酒！
  
  🍸 Whiskey Sour
     原料：1.5oz Bourbon, 0.75oz Lemon Juice, 0.5oz Simple Syrup
  
  🍸 Old Fashioned
     原料：2oz Bourbon, 1 cube Sugar Cube, 2 dashes Angostura Bitters
  
  ... 还有 45 款未显示

---

**主人**: "帮我随机推荐一款鸡尾酒"  
**Jarvis**: 🎲 今日推荐酒单：
🍸 Manhattan
  
  **原料**: 
  - Rye Whiskey, Sweet Vermouth, Angostura Bitters
  
  **酒杯**: Martini glass

---

## 📚 数据库信息

- **来源**: GitHub 公开数据集 (Rohan)
- **大小**: 1635+ 款鸡尾酒配方
- **格式**: CSV (可导出到 Excel/Numbers)
- **语言**: 英文（酒名和原料均为国际通用名称）

## 🔗 文件位置

```
/root/.openclaw/workspace/cocktail-db/
└── rohan_cocktails.csv    # 主数据库 (1635 个配方)
    
/root/.openclaw/workspace/skills/cocktail-boy/
├── SKILL.md               # 技能说明文档
└── scripts/
    ├── query.sh           # 核心查询脚本
    └── cocktail-boy       # 快捷调用命令
```

---

_Ready to mix your favorite cocktail! 🍹_
