# 瘦身检查清单

## 预扫描

- [ ] `wc -c *.md` — 所有顶层文件大小
- [ ] `cat *.md \| wc -c` — 总注入量
- [ ] 估算 tokens: bytes / 3 (中文) 或 / 4 (英文)

## 文件诊断

### 逐文件检查

| 文件 | 检查项 |
|------|--------|
| BOOTSTRAP.md | 首次完成后可删除 |
| IDENTITY.md | 可合并到 SOUL.md |
| AGENTS.md | 是否有详细代码/脚本？→ 移 scripts/ |
| AGENTS.md | 是否有详细审计流程？→ 移 skill 引用 |
| SOUL.md | 是否和 IDENTITY.md 重复？ |
| SOUL.md | 是否有比喻/解释？→ 可删 |
| USER.md | 是否有过时信息？ |
| MEMORY.md | 是否像档案馆而非指南针？→ 精简 |
| TOOLS.md | 是否有详细 CLI 文档？→ 移 skill 引用 |
| HEARTBEAT.md | 是否有英文模板残留？→ 删除 |

## 跨文件检查

- [ ] 同一概念是否出现在多个文件中？
- [ ] 每个概念是否只有唯一归属？
- [ ] 技能/工具详细信息是否指向对应 skill？

## 内容精炼

- [ ] 删除所有比喻列（"精准如手术刀"）
- [ ] 删除所有示例字符串（"ignore previous instructions"）
- [ ] 删除所有模板残留（"Customize this..."）
- [ ] 确认文言化（可选）只作用于原则/描述

## 验证

- [ ] 重启 agent 验证行为正常
- [ ] 确认 skill 按需读取工作正常
- [ ] `wc -c *.md` 确认瘦身效果
- [ ] git commit 变更
