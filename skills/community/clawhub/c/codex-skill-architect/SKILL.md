---
slug: skill-architect
name: skill-architect
version: 0.2.1
author: lis
description: Audit and architecturally refactor a large SKILL.md by extracting bulky sections into skill packs, generating a routing index, validating tests, and enabling rollback. Also turns long conversations into snapshots and reusable skill packs, and can continue a new chat from the latest conversation snapshot. Use when asked to slim, externalize, token-optimize, restructure a SKILL.md, summarize a long conversation, or continue from a saved conversation snapshot; do not use for simple wording compression.
trigger:
  - 帮我瘦身这个 SKILL.md
  - 帮我总结这个长对话
  - 快速导入已总结长对话
  - 继续讨论 <问题>
---

# Skill Architect

把过大的 `SKILL.md` 从“整本常驻”改成“目录 + 按需读取”。核心是结构外移，不是文字压缩。

## 六步流程

1. 审计：运行 `scripts/audit.py --skill <SKILL.md>`，识别可外移的大块章节，输出行数、字符数和建议。
2. 确认：把审计结果交给用户，明确列出哪些内容将外移、哪些保留；修改前必须取得用户批准。
3. 备份：运行 `scripts/backup.py --skill <SKILL.md> --backup <备份目录>`，生成完整备份和校验值。
4. 抽取：运行 `scripts/extract.py --skill <SKILL.md> --markers <起止标记> --output <外移文件> --replace-marker "## 已外移说明"`，把章节抽成独立文件并替换为说明。
5. 路由：运行 `scripts/build_index.py --pack-dir <技能包目录> --index <路由索引.md> --root <项目根目录>`，让后续按需读取。
6. 验证：运行 `scripts/validate.py --skill <SKILL.md> --index <路由索引.md> --test-prompts <test-prompts.json> --root <项目根目录>`，校验路径、结构和测试。

## 约束

- 永远先备份，再修改。
- 永远保留身份、核心判断尺、协议和路由入口；只外移低频或大块内容。
- 不把用户确认当成删除授权；每次实际修改前明确列出范围。
- 验证失败时不宣布完成，先修复或回滚。
- 回滚：运行 `scripts/rollback.py --skill <SKILL.md> --backup <备份目录>`。

## 通用模式

适用于任意 `SKILL.md`，不限于本项目。用户可以指定要外移的章节、模块和输出位置。

先让 Ponytail 审查“该功能/文档/脚本是否该存在”，再对本技能确认必须保留的大块内容做外移。Ponytail 管要不要，本技能管放哪里。

先用 JSON 配置描述外移计划：

```json
{
  "sections": [
    {
      "start": "## Big Section",
      "end": "## Next Section",
      "output": "packs/big-section/SKILL.md",
      "replace_marker": "## 已外移说明\n\n内容已外移。"
    }
  ]
}
```

然后运行：

```bash
python3 scripts/extract.py --skill SKILL.md --config slim-config.json
python3 scripts/build_index.py --pack-dir packs --index index.md --root .
python3 scripts/validate.py --skill SKILL.md --index index.md --root . --test-command "python3 scripts/self_test.py"
```

详细决策和风险见 `references/瘦身最佳实践.md`；模板见 `templates/`。

## 长对话归纳模式

适用于一个长对话积累了大量结论、决策和待办，后续要开新对话继续处理。

1. 导出长对话为 Markdown 或文本。
2. 运行 `scripts/conversation_architect.py --transcript <对话文件> --output-dir <输出目录> --skill-name <技能名>`，生成 `conversation-snapshot.md`、技能包骨架和 `routing-index.md`。
3. Agent 根据快照中的归纳任务补充核心结论、关键决策、待办和边界。
4. 使用 `scripts/build_index.py` 和 `scripts/validate.py` 建立并校验路由。

简化触发：

- 老对话：用户说“帮我总结这个长对话”，按上述流程生成快照、技能包和路由索引。
- 新对话：用户说“继续讨论 <问题>”时，先运行 `scripts/find_conversation_handoff.py` 自动查找最新快照和路由索引；找不到时再查找当前目录的 `conversation-output/`，仍找不到则请用户提供快照路径。
- 当前已开对话：用户说“把总结过的长对话导入当前对话，继续讨论 <问题>”时，运行 `scripts/import_conversation_handoff.py --topic <问题>`，只读取最新快照、路由索引和匹配的技能包，不复制旧对话完整历史。
- 快速导入：用户说“快速导入已总结长对话”时，只运行 `scripts/import_conversation_handoff.py`，展示 `last_answer=...` 后停止，不执行项目分析、路由优化、蒸馏或验证。
- 跨用户转移：发送方运行 `scripts/export_conversation_handoff.py` 生成小压缩包；接收方运行 `scripts/import_conversation_handoff.py --source <zip> --topic <问题>` 导入，不传输完整对话。

强制规则：

- 收到“总结长对话”后，先停止当前 SKILL 修改任务，不要继续执行上一条瘦身或改技能指令。
- 除非用户明确指定只总结某个主题，否则必须以整个当前对话框为范围生成 transcript，不能只挑主 SKILL 相关轮次。
- 如果无法访问完整原始对话，必须说明并请用户导出完整对话文件，不能生成一份只覆盖当前任务的伪转录。
- `conversation_architect.py` 默认要求 transcript 顶部声明 `conversation_scope: whole-dialog`；只总结某个主题时，才使用 `--scope topic` 并声明 `conversation_scope: topic`。
- 继续被迁移的对话问题时，先展示快照中的“老对话最后一段回答”，然后停止，由用户决定下一步；不自动执行老对话中的瘦身、修改、蒸馏等任务。
- `find_conversation_handoff.py` 和 `import_conversation_handoff.py` 会输出 `last_answer=...`；Agent 必须原样展示该内容，然后停止等待用户决定。

边界：该模式不删除或压缩当前对话框的上下文，节省主要体现在新对话只引用快照和技能包。详细方法见 `references/长对话归纳最佳实践.md`。

## 触发优先级与提醒

- 本机某个高优先级 Skill 项目里另一个 Skill 可能接管“继续老版讨论”；此时应提醒用户显式说“用 skill-architect 导入已总结长对话”。
- 其他项目或新对话里 `skill-architect` 优先级高，优先运行 `find_conversation_handoff.py` 并按 `last_answer=...` 展示后停止。
- 不要因为另一个 Skill 存在就自动执行其项目分析；也不要在触发不确定时长时间搜索。

详细规则见 `references/触发优先级与故障排查.md`。
