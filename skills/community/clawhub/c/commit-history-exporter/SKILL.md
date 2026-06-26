---
name: commit-history-exporter
version: 1.0.0
description: 检索并导出 SVN 和 Git 仓库中指定人员的提交记录及修改点信息。支持按作者、时间范围、项目路径过滤，可导出为 Markdown、CSV、JSON、Detailed 等格式。Detailed 格式包含完整提交日志。当用户说"导出某人的提交记录"、"查看提交历史"、"生成提交日志"、"导出代码提交记录"、"查看 SVN 提交"、"导出 Git 历史"、"查看提交备注"等类似请求时触发此 Skill。
---

# Commit History Exporter

检索并导出 SVN/Git 仓库中指定人员的提交记录和修改详情，支持获取提交日志（commit message）。

## 工作流程

### 1. 确认需求

根据用户请求，识别以下参数：

- **版本控制系统**: Git 还是 SVN
- **作者**: 指定人员（可选，默认所有）
- **时间范围**: 起始和结束日期/修订号（可选）
- **项目路径**: 仓库路径（可选，默认当前目录）
- **输出格式**: Markdown、CSV、JSON、Detailed（默认 Markdown）
- **认证信息**: SVN 用户名/密码（获取提交日志需要）

### 2. 检查仓库类型

执行前检查目标目录：

- **Git**: 存在 `.git` 目录
- **SVN**: 存在 `.svn` 目录

### 3. 执行导出

根据版本控制系统和认证状态选择导出方式：

#### Git 仓库（无需认证）
使用 [scripts/export_git_commits.sh](scripts/export_git_commits.sh)

#### SVN 仓库（可能需要认证）

**有认证**: 使用服务器获取完整提交日志
**无认证**: 使用本地工作副本数据库获取基本信息

使用 [scripts/export_svn_commits.sh](scripts/export_svn_commits.sh)

## 输出格式说明

### Markdown 格式

适合人工阅读和文档记录，包含：
- 提交基本信息（哈希/修订号、作者、日期）
- 修改文件列表（新增、修改、删除）
- 统计信息

### Detailed 格式（推荐）

**完整报告**，包含：
- 提交基本信息
- **提交日志（commit message）**
- 修改文件列表
- 统计分析

**注意**: SVN 仓库获取提交日志需要认证。

### CSV 格式

适合数据分析和导入其他系统：
- 表格格式，每行一个提交
- 包含：commit_id, author, email, date, message, files_changed

### JSON 格式

适合程序处理和 API 调用：
- 结构化数据
- 包含元数据和提交数组
- 每个提交包含详细的修改文件信息

## 使用示例

### Git 仓库导出

```bash
# 导出指定作者的所有提交记录（Markdown 格式）
./scripts/export_git_commits.sh "张三"

# 导出指定作者和时间范围的提交记录
./scripts/export_git_commits.sh "张三" "2024-01-01" "2024-12-31"

# 导出完整报告（包含提交日志）- Detailed 格式
./scripts/export_git_commits.sh "张三" "" "" "detailed"

# 指定项目路径
./scripts/export_git_commits.sh "张三" "" "" "detailed" "/path/to/project"
```

### SVN 仓库导出

```bash
# 导出指定作者的提交记录（无认证，基本信息）
./scripts/export_svn_commits.sh "liangyixiong"

# 导出完整报告（包含提交日志）- 需要认证
./scripts/export_svn_commits.sh "liangyixiong" "" "" "detailed" "/path/to/svn" "用户名" "密码"

# 导出指定修订号范围
./scripts/export_svn_commits.sh "" "100" "500" "detailed" "/path/to/svn"

# Windows 路径示例（WSL 环境）
./scripts/export_svn_commits.sh "liangyixiong" "" "" "detailed" "/mnt/d/SVN/L1_Card/Module_PCD"
```

## SVN 认证说明

### 为什么需要认证？

SVN 是集中式版本控制系统，提交日志存储在服务器端。要从服务器获取完整的提交日志，需要认证。

### 无认证时的处理

当无法连接 SVN 服务器时，脚本会：
1. 使用本地工作副本数据库 (`wc.db`) 获取基本信息
2. 输出报告中标注需要认证获取的内容
3. 提供认证指南

### 如何提供认证？

**方法 1**: 在命令中提供
```bash
./scripts/export_svn_commits.sh "作者" "" "" "detailed" "/path/to/svn" "用户名" "密码"
```

**方法 2**: 安装 SVN 命令行工具后配置认证缓存
- **SlikSVN**: https://sliksvn.com/download/
- **VisualSVN**: https://www.visualsvn.com/downloads/

**方法 3**: 使用 Windows TortoiseSVN
- TortoiseSVN 已保存的认证可用于 WSL 环境（需配置）

### 认证缓存位置

- **Linux**: `~/.subversion/auth/`
- **Windows**: `C:\Users\<用户名>\AppData\Roaming\Subversion\auth\`

## 使用 Python 直接查询 SVN 数据库

当无法获取 SVN 认证时，可使用 Python 直接从本地数据库获取基本信息：

```python
import sqlite3
from datetime import datetime

db_path = '/path/to/project/.svn/wc.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询指定作者的修改记录
cursor.execute("""
    SELECT 
        changed_revision,
        changed_date,
        changed_author,
        local_relpath,
        kind
    FROM NODES
    WHERE wc_id = 1 AND op_depth = 0
        AND changed_author LIKE '%作者名%'
    ORDER BY changed_revision DESC
""")

for rev, date_ts, author, path, kind in cursor.fetchall():
    date = datetime.utcfromtimestamp(date_ts / 1000000)
    print(f"r{rev} | {date} | {author} | {path}")
```

详见 [references/svn_database_query.md](references/svn_database_query.md)

## 常见场景

### 场景 1: 导出某员工一年的提交记录（含日志）

用户: "导出张三 2024 年的所有 Git 提交记录，包含提交备注"

执行:
```bash
./scripts/export_git_commits.sh "张三" "2024-01-01" "2024-12-31" "detailed"
```

### 场景 2: 查看最近一个月的团队提交情况

用户: "查看最近一个月所有人的提交记录"

执行:
```bash
./scripts/export_git_commits.sh "" "1 month ago" "" "detailed"
```

### 场景 3: 导出 SVN 项目提交历史（含日志）

用户: "导出 liangyixiong 在 Module_PCD 项目的 SVN 提交记录，包含提交日志"

执行:
```bash
./scripts/export_svn_commits.sh "liangyixiong" "" "" "detailed" "/mnt/d/SVN/L1_Card/Module_PCD"
```

如果需要认证:
```bash
./scripts/export_svn_commits.sh "liangyixiong" "" "" "detailed" "/mnt/d/SVN/L1_Card/Module_PCD" "用户名" "密码"
```

### 场景 4: 统计团队成员代码贡献

用户: "统计李四的代码提交数量"

方法 1（直接使用命令）:
```bash
git log --author="李四" --oneline | wc -l
```

方法 2（导出后统计）:
```bash
./scripts/export_git_commits.sh "李四" "" "" "csv"
```

## 命令参考

### Git 命令详解

查看 [references/git_commands.md](references/git_commands.md) 了解：
- 基本查看命令
- 按作者、时间、路径过滤
- 自定义输出格式
- 代码统计技巧
- 高级查询方法

### SVN 命令详解

查看 [references/svn_commands.md](references/svn_commands.md) 了解：
- SVN 基本命令
- XML 输出处理
- 作者和时间过滤技巧
- SVN 与 Git 对照表
- 注意事项

### SVN 数据库查询

查看 [references/svn_database_query.md](references/svn_database_query.md) 了解：
- wc.db 数据库结构
- 直接查询本地数据库
- 无认证获取基本信息
- Python 查询脚本示例

## 注意事项

1. **Git**: 支持本地查询，不需要网络连接
2. **SVN**: 获取完整提交日志需要服务器认证
3. **SVN 无认证**: 可使用本地数据库获取基本信息
4. **大仓库**: 查询大量历史记录时，建议限制时间或修订号范围
5. **权限**: 确保有读取仓库的权限
6. **路径**: 如果未指定项目路径，默认使用当前工作目录