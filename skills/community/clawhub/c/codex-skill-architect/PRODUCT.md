# Skill Architect

## 你还在为 Skill 越来越庞大、对话越来越长而烦恼吗？

`SKILL.md` 越写越大，几百上千行被整份加载，大部分内容当前问题根本用不上。同一个对话框里聊得越久，Token 消耗得越快，因为每次提问都要背着整个历史记录。更麻烦的是，当你发现时，这个长对话已经很难关闭，因为里面有大量整理好的结论、上下文和方法论。

Skill Architect 用架构重构解决 Skill 臃肿：脱敏案例中主 `SKILL.md` 从 2034 行降到 586 行，行数减少约 71%，Token 估算节省约 60%（约 25,700-34,300 tokens）。再用长对话快照解决对话膨胀：把积累迁移为可复用、可传输的 Skill 包。

这不是你的问题，是架构的问题。

## 三个痛点，一个解法

| 痛点 | 表现 | 解法 |
| --- | --- | --- |
| Skill 越来越臃肿 | `SKILL.md` 从几十行涨到上千行，每次对话都被完整加载 | 架构重构为入口 + 路由 + 按需读取 |
| 对话越来越长 | 同一个对话框聊了几十轮，每次新问题都背着整段历史 | 生成对话快照和精简 Skill，迁移到新对话 |
| 积累被锁死 | 方法、决策、上下文被锁在对话框里 | 导出为可传输、可复用的 Skill 包 |

## Skill Architect 的解法

> 把“每次全量加载”改为“入口 + 路由 + 按需读取”。把“被锁在对话框里的积累”迁移为“可传输、可复用的技能包”。

## 三大能力

### 能力一：Skill 架构重构

把臃肿的 `SKILL.md` 拆解为“总目录 + 路由索引 + 技能包”：

- 脱敏案例：2034 行 → 586 行，行数减少约 71%。
- 每次只加载当前问题需要的技能包。
- 修改一处不影响全局，每个技能包独立维护。

### 能力二：长对话快照 + 迁移

在当前对话框内生成快照和精简 Skill，把积累迁移到新对话继续使用：

- 快照保留事实、决策、待办，不丢上下文。
- 精简 Skill 提炼可复用方法，后续按需加载。
- 当前对话可以安全关闭，积累不会丢失。

### 能力三：跨 Agent / 跨用户传输

将沉淀的方法论导出为 Skill 包：

- 同一用户在 Codex、Claude Code、Cursor 之间迁移。
- 团队内部分享已验证的方法论。
- 导入后即可在新对话中按需加载。

## 本机实际验证案例（脱敏）

### 案例一：Skill 架构重构

本机真实执行过两轮架构重构：

- 主 `SKILL.md`：2034 行 → 586 行。
- 累计减少：1448 行，约 71%。
- 活动技能包：215 个。
- 路由路径：355 条。
- 测试提示词：303 条。
- 预期簇全部命中：193/281；零命中：0。

### 案例二：长对话快照与迁移

本机真实执行过长对话快照生成：

- 对话轮次：30 轮。
- 生成 `conversation-snapshot.md`。
- 生成 `routing-index.md`。
- 生成 5 个主题技能包。
- 快照保留“老对话最后一段回答”。
- 新对话可自动查找快照和路由索引，只加载当前话题技能包。

### 案例三：跨用户 Skill 包导出导入

本机真实执行过 Skill 包传输：

```bash
python3 scripts/export_conversation_handoff.py --snapshot-dir conversation-output --output skill-package.zip
python3 scripts/import_conversation_handoff.py --source skill-package.zip --dest imported-conversation-output --topic <问题>
```

导出包包含：

- 快照
- 路由索引
- 5 个主题技能包
- `README.md` 导入说明

接收端导入成功，并能匹配当前话题技能包。

### 案例四：触发优先级与快速导入

本机曾出现另一个高优先级 Skill 接管续接请求，导致长时间项目分析。修复后的规则：

- 存在高优先级 Skill 时，优先提醒用户显式调用 Skill Architect。
- 用户说“快速导入已总结长对话”时，只运行导入脚本并展示最后一段回答，不执行项目分析。
- 导入成功后由用户决定下一步，不自动继续旧任务。

## 工作流程

1. 审计：`scripts/audit.py --skill SKILL.md`
2. 确认：用户确认要外移的章节。
3. 备份：`scripts/backup.py --skill SKILL.md --backup backup/`
4. 抽取：`scripts/extract.py --skill SKILL.md --config slim-config.json`
5. 路由：`scripts/build_index.py --pack-dir packs --index index.md --root .`
6. 验证：`scripts/validate.py --skill SKILL.md --index index.md --root .`
7. 回滚：`scripts/rollback.py --skill SKILL.md --backup backup/SKILL.md`

长对话处理：

```bash
python3 scripts/conversation_architect.py --transcript 对话文件.md --output-dir conversation-output --skill-name project-notes
```

跨用户传输：

```bash
python3 scripts/export_conversation_handoff.py --snapshot-dir conversation-output --output skill-package.zip
python3 scripts/import_conversation_handoff.py --source skill-package.zip --topic <问题>
```

## 适用对象

- 维护超过 500 行 `SKILL.md` 的 Codex / Claude Code / Cursor 用户。
- 长期在同一个对话框里处理多类问题，希望降低 Token 消耗的用户。
- 需要把方法论迁移到新对话或分享给团队的用户。

## 边界说明

- 当前对话内生成快照不会退还已消耗的 Token，节省在后续新对话中生效。
- 快照会丢失细节，适合保留结论和可复用方法，不适合精确还原完整聊天记录。
- 传输功能默认只迁移结构化的快照和 Skill 内容，不含用户私有数据。
- 存在其他高优先级 Skill 时，优先提醒用户显式调用 Skill Architect，不做长时间项目分析。

## 版本信息

- 当前版本：0.2.1。
- 许可证：CC BY-NC-SA 4.0。
- 使用说明见 `USAGE.md`。

Token 是硬成本，架构重构是长期收益。迁移和分享让积累不再被锁死。Skill Architect 帮你把三者都解决。
