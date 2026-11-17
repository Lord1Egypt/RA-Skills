# Skill Architect 使用说明

## 第一步：安装

Codex / Claude Code / Cursor 通用：

```bash
cp -r skill-architect <Codex 技能目录>/
cp -r skill-architect <Claude Code 技能目录>/
# 或放入通用技能目录 <你的技能目录>/
```

安装后，在对话中输入触发语即可调用。

## 第二步：为臃肿的 Skill 瘦身

触发语：

```text
帮我瘦身这个 SKILL.md
```

执行流程：

```text
审计 → 确认 → 备份 → 抽取 → 生成路由 → 验证 → 完成
```

每步说明：

| 步骤 | 说明 | 用户操作 |
| --- | --- | --- |
| 审计 | 统计行数、章节，标出适合外移的内容 | 查看审计报告 |
| 确认 | 列出可外移章节，等待用户确认 | 回复“确认执行” |
| 备份 | 生成完整备份和 SHA-256 校验值 | 无需操作 |
| 抽取 | 按配置将章节抽成独立技能包 | 无需操作 |
| 生成路由 | 扫描技能包，自动生成路由索引 | 无需操作 |
| 验证 | 校验路径、测试集和路由准确率 | 查看验证结果 |

实际命令：

```bash
python3 scripts/audit.py --skill SKILL.md
python3 scripts/backup.py --skill SKILL.md --backup backup/
python3 scripts/extract.py --skill SKILL.md --config slim-config.json
python3 scripts/build_index.py --pack-dir packs --index index.md --root .
python3 scripts/validate.py --skill SKILL.md --index index.md --root .
```

## 第三步：把长对话沉淀为快照

触发语：

```text
生成这个对话的快照
```

或：

```text
帮我总结这个长对话
```

实际命令：

```bash
python3 scripts/conversation_architect.py --transcript 对话文件.md --output-dir conversation-output --skill-name project-notes
```

输出内容：

- `conversation-snapshot.md`：核心结论、决策、待办和边界。
- `skills/*/SKILL.md`：按话题生成的技能包。
- `routing-index.md`：话题路由索引。

注意：生成快照不会退还当前对话已消耗的 Token。快照的价值是在新对话中只加载精简内容。

## 第四步：导出 Skill 包

触发语：

```text
导出为 Skill 包
```

实际命令：

```bash
python3 scripts/export_conversation_handoff.py --snapshot-dir conversation-output --output skill-package.zip
```

输出 zip 包含：

- 快照
- 路由索引
- 按话题拆分的 Skill
- 导入说明

## 第五步：在新对话或当前对话导入

触发语：

```text
导入 Skill 包
```

或使用低消耗快速导入：

```text
快速导入已总结长对话
```

实际命令：

```bash
python3 scripts/import_conversation_handoff.py --source skill-package.zip --dest imported-conversation-output --topic <问题>
```

导入后，继续讨论：

```text
读取 imported-conversation-output/conversation-snapshot.md 和 routing-index.md，继续讨论 <问题>。
```

## 注意事项

- 建议定期生成快照，而不是等到对话已经非常庞大时才处理。
- 导出前检查快照和 Skill 是否包含敏感信息。
- 快照适合保留结论和可复用方法；需要精确还原完整聊天记录时，保留原始对话日志。
- 如果存在其他高优先级 Skill，优先提醒用户显式调用 Skill Architect。

## 遇到问题时

```bash
# 运行自测
python3 scripts/self_test.py

# 回滚到修改前状态
python3 scripts/rollback.py --skill SKILL.md --backup backup/SKILL.md

# 运行隐私检查
python3 scripts/check_privacy.py --root .
```

## 版本信息

- 当前版本：0.2.1。
- 许可证：CC BY-NC-SA 4.0。
