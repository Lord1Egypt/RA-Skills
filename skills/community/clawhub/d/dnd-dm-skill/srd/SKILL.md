# SRD 5.2.1 — D&D 2024 系统参考文档

> 本目录是 `dnd5e-srd` OpenClaw skill 的引用副本，用于工作目录内本地检索。
> 官方维护版本位于 `~/AppData/Roaming/LobsterAI/SKILLs/dnd5e-srd/`。

## 内容

20 个参考文件 + 2 个 Python 搜索脚本，覆盖 **SRD 5.2.1**（2024版 D&D 5e，CC-BY-4.0 许可）。

## 使用方式

通过 Python 脚本搜索+展开：

```bash
# 搜索——返回精确字符位置
python srd/scripts/search_with_positions.py "fireball" --all

# 展开上下文
python srd/scripts/expand_context.py "fireball" --result 1 --mode section --all
```

引用格式：`[DND5eSRD_XXX-YYY.md, chars N-M]`

## 文件索引

`references/DND5eSRD_001-018.md` — 介绍/角色创建
`references/DND5eSRD_019-035.md` — 野蛮人/吟游诗人/牧师
`references/DND5eSRD_036-046.md` — 牧师/德鲁伊/战士/武僧
`references/DND5eSRD_047-063.md` — 武僧/圣武士/游侠/游荡者
`references/DND5eSRD_064-076.md` — 术士/邪术师/法师
`references/DND5eSRD_077-086.md` — 法师/起源/专长
`references/DND5eSRD_087-103.md` — 装备/武器/护甲/工具
`references/DND5eSRD_104-120.md` — 法术（规则+法术列表·A-C）
`references/DND5eSRD_121-137.md` — 法术（D-M）
`references/DND5eSRD_138-154.md` — 法术（M-P）
`references/DND5eSRD_155-175.md` — 法术（P-Z）
`references/DND5eSRD_176-191.md` — 规则术语表（含全部15种状态）
`references/DND5eSRD_192-203.md` — 玩法工具箱/魔法物品(1)
`references/DND5eSRD_204-229.md` — 玩法工具箱/魔法物品(2)
`references/DND5eSRD_230-252.md` — 魔法物品(3)
`references/DND5eSRD_253-272.md` — 怪物(1)
`references/DND5eSRD_273-292.md` — 怪物(2)
`references/DND5eSRD_293-312.md` — 怪物(3)
`references/DND5eSRD_313-332.md` — 怪物(4)
`references/DND5eSRD_333-364.md` — 怪物(5)/动物

---

*基于 dnd5e-srd skill v1.0 · SRD 5.2.1 · CC-BY-4.0*
