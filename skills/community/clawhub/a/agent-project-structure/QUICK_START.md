# Agent Project Structure 规范

## 快速开始

### 检查现有结构

```bash
python scripts/check_structure.py <项目路径>
```

### 创建新项目结构

```bash
python scripts/create_structure.py <项目路径>
```

## 标准目录结构

```
agent-project/
├── projects/          # 项目文件目录
├── log/               # 日志文件目录
├── temp/              # 临时文件目录（截图、缓存等）
│   ├── screenshots/   # 截图文件
│   └── cache/         # 缓存文件
├── config/            # 配置文件目录
├── data/              # 数据文件目录
│   ├── input/         # 输入数据
│   └── output/        # 输出数据
├── scripts/           # 脚本文件目录
└── docs/              # 文档目录
```

## 文件分类原则

| 类型 | 目录 | 说明 |
|------|------|------|
| 项目文件 | `projects/` | 项目代码、资源 |
| 日志文件 | `log/` | 应用日志 |
| 临时文件 | `temp/` | 截图、缓存 |
| 配置文件 | `config/` | 环境配置 |
| 数据文件 | `data/` | 输入/输出数据 |

## 使用场景

1. **检查现有结构** - 检查现有项目结构是否符合规范
2. **创建新项目** - 生成标准目录结构
3. **重构项目结构** - 指导现有项目重构

## 相关资源

- [SKILL.md](SKILL.md) - Skill 主文件
- [references/PROJECT_STRUCTURE.md](references/PROJECT_STRUCTURE.md) - 详细规范说明
- [references/GITIGNORE.md](references/GITIGNORE.md) - .gitignore 模板
