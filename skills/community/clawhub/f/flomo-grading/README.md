# flomo笔记打分技能

随机推送flomo笔记让用户打分，持续学习用户的打分偏好，动态更新"好笔记"评判标准。

## 文件说明

### 📂 可公开文件（可上传到ClawHub）

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能说明文档 |
| `skill.json` | 技能元信息 |
| `grading-principles.md` | 打分原则总结（需确认无隐私顾虑） |
| `scoring-history-public.json` | 打分历史（隐私处理版，笔记内容已屏蔽） |

### 🔒 隐私文件（仅本地保存）

| 文件 | 说明 |
|------|------|
| `scoring-history.json` | 完整打分历史（含笔记原文） |
| `all_notes_index.json` | 全量笔记索引（8336篇的ID和元信息） |
| `.scored_ids.txt` | 已打分笔记ID列表 |
| `.current_note.json` | 当前正在打分的笔记 |
| `.missing_notes.json` | 丢失的笔记记录 |

## 使用方式

1. 启动技能：从全量索引中随机选择未打分笔记
2. 展示笔记：获取完整内容并展示
3. 用户打分：S/A/B/C/D/E
4. 记录学习：保存到 scoring-history.json，更新打分原则
5. 循环继续

## 当前进度

- 总笔记数：8336 篇
- 已打分：154 篇（1.8%）
- 分数分布：S:5, A:37, B:65, C:33, D:10, E:4

## API依赖

- Flomo MCP API
- Token: 已配置在 SECRET.md
