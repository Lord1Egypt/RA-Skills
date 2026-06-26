# 已收录餐馆

社区贡献的餐馆 Skill 合集。每家餐馆一个目录，里面有 `SKILL.md`（给 AI 读的）和 `restaurant-info.yaml`（原始数据）。

## 餐馆列表

| 餐馆 | 城市 | 品类 | 人均 | 特色 |
|------|------|------|------|------|
| [眉州东坡（北苑华贸店）](meizhou-dongpo-beiyuan/) | 北京·朝阳 | 川菜 | ¥69 | 大众点评川菜热门榜第1，经典川菜连锁 |

> 💡 想加一家？看 [CONTRIBUTING.md](../CONTRIBUTING.md)

## 怎么用

### 用法一：直接加载某家店

把某家餐馆的 `SKILL.md` 复制到你的 AI 工具的 Skills 目录：

```bash
cp restaurants/meizhou-dongpo-beiyuan/SKILL.md ~/.cursor/skills/meizhou-dongpo.md
```

### 用法二：配合干饭.skill 一起用

同时加载根目录的 `SKILL.md`（干饭决策助手）和你想要的餐馆 Skill，AI 就能帮你在多家店之间选择了。

## 目录规范

每家餐馆的目录结构：

```
restaurants/
└── {slug}/                      # 英文标识，小写+连字符
    ├── SKILL.md                  # AI 可读的 Skill 文件（必须）
    └── restaurant-info.yaml      # 原始数据文件（推荐）
```
