# 提案目录（evolution/proposals/）

存放进化提案，文件名 `PROP-{YYYYMMDD}-{三位序号}.md`，从 `templates/proposal.template.md` 复制起稿。

规则：

1. 提案阶段**禁止改动任何技能文件**（agents.md 8.4 第 2 段）。
2. 提案必过四项校验：来源白名单、追溯链、血统（原子层须重新锚定原文）、结构（编号唯一/版本语义/DAG）。
3. 校验不过打回重写；校验通过进入人工评审，MAJOR 与废弃**永远**需人工确认。
4. 合并后在 `evolution/log.md` 追加记录，并触发下游回归（原子变更 → 受影响应用 Skill 生成重派生任务）。
5. 反漂移红线：触发 agents.md 8.8 任一情形，立即中止并上报用户。
