# SVN 提交记录检索命令参考

## 基本命令

### 查看提交历史

```bash
# 查看最近提交
svn log

# 查看最近 N 条提交
svn log -l 10

# 查看详细提交信息（包含修改文件）
svn log -v

# 查看指定修订号范围的提交
svn log -r 100:200
```

### 按作者过滤

```bash
# SVN 不直接支持 --author 参数，需要结合其他工具
# 方法 1: 使用 grep 过滤
svn log | grep "| 张三 |"

# 方法 2: 使用 XML 输出 + grep
svn log --xml | grep -A 5 "<author>张三</author>"
```

### 按时间过滤

```bash
# 查看指定日期之后的提交（需要先查找起始修订号）
svn log -r {2024-01-01}:HEAD

# 查看指定日期范围的提交
svn log -r {2024-01-01}:{2024-12-31}

# 注意: SVN 使用 {日期} 格式指定日期
```

### 查看修改文件

```bash
# 查看每次提交修改的文件
svn log -v

# 输出格式示例:
# Added: path/to/new/file
# Modified: path/to/modified/file
# Deleted: path/to/deleted/file
```

## 详细查看单个提交

```bash
# 查看指定修订号的详细信息
svn log -r 1234 -v

# 查看指定修订号的代码变更
svn diff -c 1234

# 查看两个修订号之间的差异
svn diff -r 100:200

# 查看指定修订号修改的文件列表
svn log -r 1234 -v --xml
```

## 导出提交记录

### 导出为文本文件

```bash
# 导出所有提交记录
svn log > svn_commits.txt

# 导出详细提交记录（包含修改文件）
svn log -v > svn_commits_detailed.txt

# 导出指定修订号范围的提交记录
svn log -r 100:200 > svn_commits_range.txt
```

### 导出为 XML 格式

```bash
# 导出为 XML（便于程序处理）
svn log --xml > svn_commits.xml

# 导出详细信息为 XML
svn log -v --xml > svn_commits_detailed.xml

# XML 格式示例:
# <log>
#   <logentry revision="1234">
#     <author>张三</author>
#     <date>2024-01-01T10:00:00.000000Z</date>
#     <msg>提交信息</msg>
#     <paths>
#       <path action="M">path/to/file</path>
#     </paths>
#   </logentry>
# </log>
```

### 使用 Python 处理 SVN XML

```python
import xml.etree.ElementTree as ET

# 解析 SVN XML 输出
tree = ET.parse('svn_commits.xml')
root = tree.getroot()

for logentry in root.findall('logentry'):
    revision = logentry.get('revision')
    author = logentry.find('author').text
    date = logentry.find('date').text
    message = logentry.find('msg').text
    
    print(f"r{revision} | {author} | {date} | {message}")
    
    # 获取修改文件列表
    for path in logentry.findall('.//path'):
        action = path.get('action')
        file_path = path.text
        print(f"  {action}: {file_path}")
```

## 实用组合命令

### 查看某作者在某段时间的提交

```bash
# 先找到时间范围对应的修订号
start_rev=$(svn log -r {2024-01-01}:HEAD -l 1 | grep "^r" | cut -d'|' -f1 | tr -d 'r')
end_rev=$(svn log -r HEAD:{2024-12-31} -l 1 | grep "^r" | cut -d'|' -f1 | tr -d 'r')

# 查看该范围的提交并过滤作者
svn log -r ${start_rev}:${end_rev} -v | grep -B 5 -A 20 "| 张三 |"
```

### 统计某作者的提交数量

```bash
# 统计总数
svn log | grep "| 张三 |" | wc -l

# 统计每个作者的提交数量
svn log | cut -d'|' -f2 | sort | uniq -c
```

### 查看某个文件的历史修改

```bash
# 查看文件的所有修改历史
svn log path/to/file

# 查看文件的详细修改历史
svn log -v path/to/file

# 查看文件的所有修改者和修改次数
svn log path/to/file | cut -d'|' -f2 | sort | uniq -c
```

### 查看代码行数统计

```bash
# SVN 不直接提供代码统计，需要使用 svn diff 配合工具
# 统计指定修订号的代码变更
svn diff -c 1234 --summarize

# 统计代码行数变化
svn diff -c 1234 | grep -E "^[\+\-]" | grep -v "^[\+\-][\+\-][\+\-]" | wc -l
```

## 高级查询

### 按提交信息内容过滤

```bash
# 查看包含特定关键词的提交
svn log | grep -B 5 "关键词"

# 使用 XML 输出 + grep
svn log --xml | grep -B 5 -A 10 "关键词"
```

### 按文件路径过滤

```bash
# 查看特定目录的提交历史
svn log path/to/directory

# 查看特定文件的提交历史
svn log path/to/file
```

### 查看分支差异

```bash
# 查看分支创建信息
svn log --stop-on-copy path/to/branch

# 查看分支与主线的差异
svn diff -r HEAD:base path/to/branch
```

## SVN vs Git 对照

| 功能 | Git | SVN |
|------|-----|-----|
| 查看提交历史 | `git log` | `svn log` |
| 按作者过滤 | `git log --author="张三"` | `svn log | grep "| 张三 |"` |
| 按时间过滤 | `git log --since="2024-01-01"` | `svn log -r {2024-01-01}:HEAD` |
| 查看修改文件 | `git log --name-status` | `svn log -v` |
| 查看单个提交 | `git show <commit-id>` | `svn log -r <revision>` |
| 查看代码变更 | `git show <commit-id>` | `svn diff -c <revision>` |
| 导出 XML | 需要第三方工具 | `svn log --xml` |
| 本地仓库 | 支持 | 不支持（需要连接服务器） |

## 注意事项

1. **SVN 需要网络连接**: SVN 是集中式版本控制，大多数操作需要连接服务器
2. **修订号**: SVN 使用数字修订号，而 Git 使用哈希值
3. **作者过滤**: SVN 不直接支持作者过滤，需要结合 grep 等工具
4. **日期格式**: SVN 使用 `{YYYY-MM-DD}` 格式指定日期
5. **性能考虑**: 查询大量提交记录可能较慢，建议限制范围