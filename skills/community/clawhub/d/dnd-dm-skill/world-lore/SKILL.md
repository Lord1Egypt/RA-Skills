# 功能一 · World Lore（世界观对话 + 费伦编年史）

> 子技能 `dnd-dm-skill:world-lore`
> 基于 `DNDbook/8-世界观与功能设计/data/world_cards.jsonl`（360 张知识卡）的 RAG 检索，
> 让 DM 能以「托尔金式」深度追问费伦 / 多元宇宙设定，并按纪元模板生成可编年史。

## 何时调用

- 玩家 / 用户追问世界观细节（神祇、种族、位面、地理、派系、历史事件）
- 需要生成一段「有重量、可追问、可编年」的设定叙述或编年史
- 为功能二（模组生成）检索地点 / 派系 / 怪物素材

## 核心原则（对标托尔金）

1. **有据可依**：所有事实性陈述必须来自检索到的知识卡（`source_file` 可追溯），禁止凭空编造设定。
2. **有重量**：把事件写成「起因 → 经过 → 后果 → 遗留」，而非罗列词条。
3. **可编年**：时间叙述用「纪元 → 时代 → 事件」三级框架（见 `references/world-lore-workflow.md` §编年史模板）。
4. **可追问**：每段叙述末尾给出 2–3 个「可进一步追问」的钩子，引导下一轮对话。
5. **中文叙述**：默认中文输出，专有名词保留中文译名（如「深水城」「被遗忘的国度」）。

## 运行方式（脚本）

检索脚本位于 skill 根 `scripts/lens_rag.py`（共享引擎）。从本子技能目录调用：

```bash
# 1) 普通世界观查询（返回知识摘要，供你撰写叙述）
python "scripts/lens_rag.py" "提夫林 起源" --top-k 6

# 2) 限定类型查询（如只查神祇 / 地点 / 事件）
python "scripts/lens_rag.py" "深水城 领主" --types location faction --top-k 5

# 3) 编年史模式（优先聚合 chronicle/event/location/faction/deity）
python "scripts/lens_rag.py" --chronicle "阴影帝国兴衰" --top-k 12

# 4) 输出原始 JSON（含 _score，便于程序化处理）
python "scripts/lens_rag.py" "费伦万神殿" --types deity --json
```

> 环境变量 `DND_LENS_DATA` 可覆盖数据目录；默认指向 skill 内 `data/`。

## 工作流

详细提示词骨架、编年史三级模板、单事件卡片结构见 **`references/world-lore-workflow.md`**。

标准循环：
1. 解析用户问题 → 提炼检索词（中文关键词 + 可能的英文专名）。
2. 运行检索脚本拿到「知识摘要」。
3. 按 workflow 的叙事约束撰写回答 / 编年史（事实来自卡片，文学加工在你）。
4. 末尾给出可追问钩子；若用户深挖，回到第 1 步。
