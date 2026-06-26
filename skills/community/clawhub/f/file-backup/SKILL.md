---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 304502200aeae2a301f4803eddb248d5a31e8f539736d5b0e84643401248863a59f9eca1022100e7e82e85cab6b1ae66ca1a16448f3040078325c951f548293f5fa5db92d710b0
    ReservedCode2: 3046022100fc82f0e2c81471b88f6b6b7a00b32cf8d6a29f3967440c99e21ba69202a99f7c022100fc848215ff03569403cb6b70bbf52dde4cb45e739cb8cae35ea576a2129e7f53
description: |-
    修改文件前的自动备份工具。
    当需要修改重要文件时，先备份再修改，改完后让用户检查，确认无误后删除备份。
name: file-backup
---

# File Backup Skill

## 触发条件

修改重要文件前，特别是：
- 配置文件
- 核心机制文件
- 用户指定的敏感文件

## 工作流程

### 1. 备份
检测到要修改重要文件时，先创建备份：
```
cp 原文件 备份目录/原文件.日期.bak
```
例如：`cp config.json backups/config.json.2026-03-14.bak`

### 2. 执行修改
正常执行修改操作

### 3. 主动提醒检查 ⚠️
修改完成后，**必须主动让用户检查**：
```
备份已创建：backups/xxx.bak
请检查文件，确认无误后告诉我"可以删除备份"
```

### 4. 删除备份
收到用户确认后：
```
rm backups/xxx.bak
备份已删除
```

## 重要规则

1. **不备份不修改**：没有备份就不能改重要文件
2. **主动提醒**：改完后必须让用户检查，不能等用户忘
3. **确认才删**：必须等用户明确说"可以删除"才能删
4. **备份保留**：如果用户没确认，备份一直保留
5. **通用路径**：备份目录可自定义，默认为 `backups/`

## 配置（可选）

可以指定需要触发备份的文件类型：
- 配置文件：config.json, settings.yaml
- 核心文件：SOUL.md, MEMORY.md, AGENTS.md
- 自定义：用户指定的其他文件

## 示例

```
[检测到要修改 config.json]
→ 备份：cp config.json backups/config.json.2026-03-14.bak
→ 执行修改
→ 提醒："备份已创建 backups/config.json.2026-03-14.bak，请检查config.json，确认无误后告诉我'可以删除备份'"
[用户确认]
→ 删除备份
```
