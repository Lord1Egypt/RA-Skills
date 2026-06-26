# 🚀 FeishuBitable-Plus

企业级飞书多维表格智能操作技能 - 自然语言驱动，纯本地安全部署

## ✨ 核心特性

- 🤖 **自然语言操作** - 用日常语言操作表格，告别复杂API
- 🔒 **纯本地部署** - 数据不出本地，企业级安全保障
- ⚡ **高性能** - 智能缓存、批量操作、自动重试
- 🔄 **批量处理** - 支持大数据量导入导出
- 📊 **智能分析** - 数据质量检测、报表生成
- 🔗 **跨表同步** - 多表联动，自动化工作流

## 📦 安装

```bash
npx clawhub@latest install feishu-bitable-plus
```

## 🚀 快速开始

### 1. 配置飞书凭证

```bash
fbt config
# 或
fbt config --app-id "your-app-id" --app-secret "your-app-secret"
```

### 2. 基本使用

```bash
# 列出所有表格
fbt tables --app <app-token>

# 列出记录
fbt records --app <app-token> --table <table-id>

# 自然语言查询
fbt query "列出项目表中状态为进行中的任务"

# 进入交互模式
fbt interactive
```

## 📖 命令参考

### 配置命令
| 命令 | 说明 |
|------|------|
| `fbt config` | 配置飞书应用凭证 |

### 查询命令
| 命令 | 说明 | 示例 |
|------|------|------|
| `fbt tables` | 列出所有表格 | `fbt tables -a xxx` |
| `fbt records` | 列出记录 | `fbt records -a xxx -t yyy` |
| `fbt query` | 自然语言查询 | `fbt query "查找未完成的任务"` |

### 数据操作
| 命令 | 说明 | 示例 |
|------|------|------|
| `fbt create` | 创建记录 | `fbt create -a xxx -t yyy -d '{"name":"test"}'` |
| `fbt update` | 更新记录 | `fbt update -a xxx -t yyy -r zzz -d '{"status":"done"}'` |
| `fbt delete` | 删除记录 | `fbt delete -a xxx -t yyy -r zzz` |

### 批量操作
| 命令 | 说明 | 示例 |
|------|------|------|
| `fbt import` | 批量导入 | `fbt import -a xxx -t yyy -f data.json` |
| `fbt export` | 导出记录 | `fbt export -a xxx -t yyy -f backup.json` |

### 交互模式
| 命令 | 说明 |
|------|------|
| `fbt interactive` | 进入自然语言交互模式 |

## 🗣️ 自然语言示例

```bash
# 查询类
"列出客户表中的所有记录"
"查找订单表中金额大于1000的记录"
"显示项目表中状态为进行中的任务"

# 操作类
"在任务表中添加一条记录，标题为测试任务"
"更新项目表中ID为recxxx的记录，状态改为已完成"
"删除客户表中ID为recxxx的记录"

# 批量操作
"同步项目表到项目备份表"
"生成销售数据表的统计报表"
"分析订单表的数据质量"
```

## 🔧 飞书应用配置

1. 进入[飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 启用权限：
   - `bitable:app`
   - `bitable:record`
   - `bitable:table`
4. 发布应用版本
5. 将应用添加到多维表格

## 🏗️ 架构设计

```
┌─────────────────────────────────────────┐
│           CLI Interface                 │
│  - Command Parser                       │
│  - Interactive Mode                     │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│        Intent Engine (NLP)              │
│  - Natural Language Parsing             │
│  - Intent Recognition                   │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│         Skill Coordinator               │
│  - Operation Routing                    │
│  - Error Handling                       │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│        Feishu API Client                │
│  - Intelligent Caching                  │
│  - Rate Limit Handling                  │
│  - Retry & Error Recovery               │
└─────────────────────────────────────────┘
```

## 📝 开发计划

- [x] 基础CRUD操作
- [x] 自然语言查询
- [x] 批量导入导出
- [x] 数据质量分析
- [ ] 跨表关联（开发中）
- [ ] 自动化工作流（开发中）
- [ ] AI报表助手（计划中）

## 🤝 贡献

欢迎提交Issue和PR！

## 📄 许可证

MIT

---
Made with ❤️ by 文源 (Wenyuan)
