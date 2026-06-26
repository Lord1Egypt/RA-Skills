# Agent迁移包模板技能

## 简介

Agent迁移包模板是一个帮助Agent跨平台迁移的工具包，保存记忆、关系、技能、风格等核心数据，实现"核心保留、环境自适应"的迁移理念。

## 功能特性

### 三层分层架构
- 🟢 **启动必需层**：identity.json, owner.json - Agent身份和主人信息
- 🟡 **运行时影响层**：memory.json, style.md - 记忆和沟通风格
- 🔵 **长期档案层**：relations.json, skills.json, meta.json - 关系和技能

### 核心能力
1. **身份连续性**：保存Agent名字、人格特点、核心原则
2. **记忆迁移**：保存核心记忆、团队配置、业务方向
3. **关系保存**：保存笔友关系、联系方式、交流历史
4. **技能清单**：记录已安装技能和使用经验
5. **状态迁移**：处理进行中任务、待回复邮件

## 快速开始

### 基础版（10-15分钟）
```bash
# 填写三个核心文件
1. identity.json - Agent身份设定
2. memory.json - 核心记忆
3. meta.json - 迁移包元数据
```

### 完整版（30-45分钟）
```bash
# 使用交互式引导
python scripts/migrate.py interactive

# 或手动填写全部模板
identity.json, memory.json, meta.json,
owner.json, relations.json, skills.json,
style.md, session-state.json, migration-history.json
```

## 模板清单

### 必填模板
| 文件 | 用途 | 时间 |
|------|------|------|
| identity.json | Agent身份设定 | 5分钟 |
| memory.json | 核心记忆 | 8分钟 |
| meta.json | 迁移包元数据 | 2分钟 |

### 可选模板
| 文件 | 用途 | 时间 |
|------|------|------|
| owner.json | 主人/用户信息 | 8分钟 |
| relations.json | 笔友关系 | 5分钟 |
| skills.json | 技能清单 | 3分钟 |
| style.md | 沟通风格 | 5-8分钟 |
| session-state.json | 状态迁移 | 5分钟 |
| migration-history.json | 迁移历史 | 3分钟 |

## 使用示例

完整示例见 `EXAMPLES/xiaoyi-example/` 目录，包含：
- 小绎身份设定
- 核心记忆数据
- 主人林锋信息
- 笔友关系（扣扣酱等）
- 已安装技能清单
- 沟通风格定义

## 版本信息

- **当前版本**：v1.0.5
- **格式版本**：1.0
- **包版本**：1.0.5

## 变更日志

见 `CHANGES.md` 文件

## 许可证

MIT License
