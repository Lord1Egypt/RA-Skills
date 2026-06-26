# Git 提交记录检索命令参考

## 基本命令

### 查看提交历史

```bash
# 查看所有提交
git log

# 查看最近 N 条提交
git log -n 10

# 查看简洁版提交历史
git log --oneline

# 查看图形化分支历史
git log --graph --oneline --all
```

### 按作者过滤

```bash
# 查看指定作者的提交
git log --author="张三"

# 查看包含特定邮箱的提交
git log --author="zhangsan@example.com"

# 查看多个作者的提交（正则匹配）
git log --author="张三|李四"
```

### 按时间过滤

```bash
# 查看指定日期之后的提交
git log --since="2024-01-01"

# 查看指定日期之前的提交
git log --until="2024-12-31"

# 查看最近一周的提交
git log --since="1 week ago"

# 查看最近一个月的提交
git log --since="1 month ago"

# 查看指定日期范围的提交
git log --since="2024-01-01" --until="2024-12-31"
```

### 查看修改文件

```bash
# 查看每次提交修改的文件
git log --name-status

# 查看每次提交修改的文件（简洁版）
git log --name-only

# 查看文件修改统计
git log --stat
```

### 自定义输出格式

```bash
# 自定义格式输出
git log --pretty=format:"%H - %an, %ad : %s"

# 常用格式选项：
# %H  - 完整提交哈希
# %h  - 简短提交哈希
# %an - 作者名字
# %ae - 作者邮箱
# %ad - 作者日期
# %s  - 提交信息
# %d  - 分支名称
```

## 详细查看单个提交

```bash
# 查看指定提交的详细信息
git show <commit-id>

# 查看指定提交的修改文件列表
git show --name-status <commit-id>

# 查看指定提交的代码变更
git show --stat <commit-id>
```

## 导出提交记录

### 导出为文本文件

```bash
# 导出所有提交记录
git log > commits.txt

# 导出指定作者的提交记录
git log --author="张三" > zhangsan_commits.txt

# 导出指定时间范围的提交记录
git log --since="2024-01-01" --until="2024-12-31" > 2024_commits.txt
```

### 导出为 CSV 格式

```bash
# 使用自定义格式导出为 CSV
git log --pretty=format:"%h,%an,%ae,%ad,%s" --date=short > commits.csv
```

### 导出为 JSON 格式（需要 jq）

```bash
# 使用 jq 工具导出为 JSON
git log --pretty=format:'{"commit":"%H","author":"%an","email":"%ae","date":"%ad","message":"%s"},' --date=iso | \
  sed '$ s/,$//' | \
  jq -s . > commits.json
```

## 实用组合命令

### 查看某作者在某段时间的提交

```bash
git log --author="张三" --since="2024-01-01" --until="2024-12-31" --name-status
```

### 统计某作者的提交数量

```bash
# 统计总数
git log --author="张三" --oneline | wc -l

# 统计每个作者的提交数量
git shortlog -sn
```

### 查看某个文件的历史修改

```bash
# 查看文件的所有修改历史
git log --follow path/to/file

# 查看文件的所有修改者和修改次数
git log --follow --format="%an" path/to/file | sort | uniq -c
```

### 查看代码行数统计

```bash
# 查看每个作者的代码行数贡献
git log --author="张三" --pretty=tformat: --numstat | \
  awk '{ add += $1; subs += $2 } END { printf "新增: %s, 删除: %s\n", add, subs }'
```

## 高级查询

### 按提交信息内容过滤

```bash
# 查看包含特定关键词的提交
git log --grep="修复"

# 查看包含多个关键词的提交
git log --grep="修复" --grep="bug" --all-match
```

### 按文件路径过滤

```bash
# 查看特定目录的提交历史
git log path/to/directory/

# 查看特定文件的提交历史
git log path/to/file
```

### 查看分支差异

```bash
# 查看某分支相对于另一分支的差异提交
git log branchA..branchB

# 查看两个分支的共同提交
git log branchA...branchB
```