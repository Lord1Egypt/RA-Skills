# 功能三 · Echo Map（真实经历 → DND 冒险映射）

> 子技能 `dnd-dm-skill:echo-map`
> 把用户的真实世界经历（人物 / 冲突 / 地点 / 目标 / 情绪 / 时间）确定性地映射为
> DND 5e 的种族 / 职业 / 阵营 / 怪物 / 地点 / 神器，并强制 **anon 化** 防隐私泄露。

## 何时调用

- 用户想把一段真实经历（职场、生活、旅行、冲突）改写成 DND 冒险
- 需要把现实人物 / 机构 / 地名脱敏为幻想名后，再生成模组 JSON

## 核心红线（隐私优先）

1. **绝不回写真实身份**：真实姓名 / 机构名 / 地名不进入 `world_cards` 知识库、不出现在最终交付物。
2. **强制脱敏**：所有真实名必须先经 `echo_map.py anonymize` 替换为幻想名（`mapping_dict.anonymize` 池），再进入模组。
3. **语义映射由 LLM 完成，结构由脚本兜底**：脚本只做脱敏 + 输出契约规范化，不替代你的叙事判断。

## 运行方式（脚本）

```bash
# 1) 脱敏：真实名 → 幻想名（并改写经历文本）
python "echo-map/scripts/echo_map.py" \
       anonymize --names "张三 李四" --places "上海 甲公司" \
       --story experience.txt --out experience_anon.txt

# 2) 规范化 LLM 草稿（脱敏 + 补全 chronicle_note + 校验契约）
python "echo-map/scripts/echo_map.py" \
       normalize --draft draft_module.json --names "张三 李四" --places "上海 甲公司" --out final.json
```

> 数据字典：`data/mapping_dict.json`（8 个槽位 + anonymize 池 + 输出契约）。

## 标准循环

1. 收取用户经历文本。
2. 让用户确认需脱敏的真实名（人名 / 地名 / 机构名）——或你先抽取疑似实名，请用户确认后再脱敏。
3. 运行 `anonymize` 得到脱敏文本与映射字典。
4. 按 `references/echo-map-workflow.md` 的提示词骨架，**由你（LLM）** 完成语义映射，产出模组 JSON 草稿。
5. 运行 `normalize` 脱敏 + 补全契约，输出最终 `final.json`。
6. 可把 `final.json` 喂给 `module-forge` 进一步 CR 平衡，或喂给 `world-lore` 检索设定锚点。
