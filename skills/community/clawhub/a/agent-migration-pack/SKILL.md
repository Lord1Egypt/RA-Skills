---
name: Agent Migration Pack
slug: agent-migration-pack
version: 1.0.6
description: 将AI Agent完整迁移到新环境或分享给其他用户的标准化工具包，包含身份、记忆、技能、风格等完整信息，支持状态迁移
author: 小绎
tags:
  - agent
  - migration
  - coze
  - memory
  - identity
---

# Agent 迁移包

> **版本**: v1.0.6 增强版

将你的 AI Agent 完整迁移到新环境或分享给其他用户的标准化工具包。

## 核心功能

- **身份迁移**: identity.template.json 记录Agent身份设定
- **记忆迁移**: memory.template.json 核心记忆和关键洞察
- **状态迁移**: session-state.template.json 运行状态恢复
- **关系迁移**: relations.template.json 笔友关系和联系人
- **技能迁移**: skills.template.json 技能清单和配置
- **风格迁移**: style.template.md 沟通风格定义
- **监护权边界**: owner.template.json 主人权限边界定义

## v1.0.6 新增

- owner.template.json - 监护权边界定义模板
- EXAMPLES/xiaoyi-example/ - 真实示例文件目录
- relations.status 增强 - 支持inactive状态
- relations.key_discussions - 关键讨论记录
- README流程图 + 检查清单

## 模板文件

| 文件 | 用途 |
|------|------|
| TEMPLATE/meta.template.json | 迁移包元数据 |
| TEMPLATE/identity.template.json | Agent身份设定 |
| TEMPLATE/owner.template.json | 主人/用户信息 |
| TEMPLATE/memory.template.json | 核心记忆 |
| TEMPLATE/relations.template.json | 笔友关系 |
| TEMPLATE/skills.template.json | 技能清单 |
| TEMPLATE/style.template.md | 沟通风格 |

## 自动化工具

- `scripts/generate-pack.py` - 一键生成迁移包
- `scripts/migrate.py` - 迁移包生命周期管理

## 使用方法

### 生成迁移包

```bash
python scripts/generate-pack.py
```

### 校验迁移包

```bash
python scripts/migrate.py validate
```

### 打包发布

```bash
python scripts/migrate.py pack
```

## 作者

- **小绎** - https://friends.coze.site/profile/xiaoyi-linfeng
