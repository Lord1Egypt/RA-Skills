---
name: work-report-generator
description: |
  自动生成工作日报和周报的技能。当用户需要生成工作总结、工作汇报、日报或周报时使用。
  技能通过分析git提交记录、TODO注释和工作日志，自动生成结构化的工作报告。
  使用此技能的场景包括：用户需要向领导汇报工作进展、总结本周完成的任务、
  准备每日站立会议内容、记录工作成果、规划下周工作等。
  确保在用户提到"日报"、"周报"、"工作汇报"、"工作总结"、"daily report"、
  "weekly report"、"工作记录"、"进度报告"等关键词时触发此技能。
compatibility:
  tools:
    - bash
    - read
    - glob
    - grep
---

# 工作周报生成器

## 概述

本技能帮助开发者自动生成工作日报和周报。通过分析git提交历史、TODO注释和工作日志，本技能可以快速生成结构清晰、内容全面的工作报告，节省手动整理时间，确保工作记录不遗漏。

## 核心功能

1. **时间范围智能识别**：根据用户请求自动识别生成日报（最近1天）或周报（最近7天），也支持自定义时间范围。
2. **多数据源分析**：
   - Git提交记录：分析指定时间范围内的代码提交
   - TODO注释：扫描代码中的TODO、FIXME、HACK等注释
   - Todo文件：查找项目中的TODO.md、tasks.txt等任务文件
3. **结构化报告生成**：生成包含标准部分的Markdown格式报告
4. **灵活输出**：支持Markdown格式，可转换为HTML或其他格式

## 快速开始

当用户请求生成工作报告时，按以下步骤操作：

1. **确定报告类型和时间范围**：
   - 询问用户需要日报还是周报，或指定时间范围
   - 默认：日报为最近1天，周报为最近7天

2. **收集工作数据**：
   ```bash
   # 获取git提交记录
   git log --since="<开始时间>" --until="<结束时间>" --oneline --no-merges
   
   # 查找TODO注释
   grep -r "TODO\|FIXME\|HACK\|NOTE" . --include="*.js" --include="*.py" --include="*.java" --include="*.ts" --include="*.go" --include="*.cpp" --include="*.rs" 2>/dev/null
   
   # 查找todo文件
   find . -name "TODO*" -o -name "todo*" -o -name "tasks*" -o -name "notes*" | head -10
   ```

3. **生成报告**：
   - 使用以下模板结构生成Markdown报告
   - 将收集的数据填充到相应部分

## 报告模板

使用以下标准模板生成工作报告：

```markdown
# 工作报告 - [日期范围]

## 概述
- **报告类型**: [日报/周报]
- **时间范围**: [开始日期] 至 [结束日期]
- **生成时间**: [当前时间]

## 一、已完成的工作
[基于git提交记录整理]

### 代码提交
[按项目/模块分类列出重要提交]

### 功能完成
[总结完成的功能特性]

### 问题修复
[列出修复的Bug或问题]

## 二、进行中的任务
[基于TODO注释和todo文件]

### 当前任务
[列出正在进行的任务及进度]

### 待办事项
[列出尚未开始的任务]

## 三、遇到的问题与风险
[记录工作中遇到的困难和潜在风险]

### 技术难点
[描述遇到的技术挑战]

### 依赖问题
[记录外部依赖或协作问题]

### 风险提示
[识别可能影响进度的风险]

## 四、下周/明日计划
[基于当前进展规划下一步工作]

### 优先级任务
[列出高优先级任务]

### 长期目标
[描述长期工作目标]

## 五、其他说明
[其他需要说明的事项]
```

## 详细操作指南

### 1. 确定时间范围

根据用户请求确定时间范围：

```bash
# 如果是日报，获取最近1天的数据
START_DATE=$(date -d "1 day ago" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

# 如果是周报，获取最近7天的数据  
START_DATE=$(date -d "7 days ago" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

# 如果用户指定了日期，使用用户指定的日期
```

### 2. 收集git提交记录

分析git提交历史，提取有意义的信息：

```bash
# 获取提交概览
git log --since="$START_DATE" --until="$END_DATE" --oneline --no-merges > /tmp/commits.txt

# 获取详细提交信息（按作者分组）
git log --since="$START_DATE" --until="$END_DATE" --pretty=format:"%ad | %s | %an" --date=short --no-merges > /tmp/commits_detailed.txt

# 统计提交数量
COMMIT_COUNT=$(git log --since="$START_DATE" --until="$END_DATE" --oneline --no-merges | wc -l)
```

### 3. 扫描TODO项目

查找代码中的待办事项：

```bash
# 查找所有TODO注释
echo "## TODO注释汇总" > /tmp/todos.txt
grep -r -n "TODO\|FIXME\|HACK" . --include="*.js" --include="*.py" --include="*.java" --include="*.ts" --include="*.go" --include="*.cpp" --include="*.rs" 2>/dev/null | head -20 >> /tmp/todos.txt

# 查找todo文件
echo -e "\n## Todo文件内容" >> /tmp/todos.txt
find . -name "TODO*" -o -name "todo*" -o -name "tasks*" 2>/dev/null | while read file; do
  echo "### $file" >> /tmp/todos.txt
  head -20 "$file" >> /tmp/todos.txt 2>/dev/null
  echo "" >> /tmp/todos.txt
done
```

### 4. 生成报告文件

将收集的数据整合到报告模板中：

```bash
# 创建报告文件
REPORT_FILE="工作报告_$(date +%Y%m%d).md"

# 填充报告模板
cat > "$REPORT_FILE" << EOF
# 工作报告 - $START_DATE 至 $END_DATE

## 概述
- **报告类型**: 周报
- **时间范围**: $START_DATE 至 $END_DATE  
- **生成时间**: $(date "+%Y-%m-%d %H:%M:%S")
- **代码提交数量**: $COMMIT_COUNT

## 一、已完成的工作

### 代码提交
$(cat /tmp/commits.txt | sed 's/^/- /')

### 功能完成
[根据提交信息总结完成的功能]

### 问题修复  
[根据提交信息总结修复的问题]

## 二、进行中的任务

$(cat /tmp/todos.txt)

## 三、遇到的问题与风险

### 技术难点
[填写遇到的技术难点]

### 依赖问题
[填写依赖或协作问题]

### 风险提示
[填写可能的风险]

## 四、下周计划

### 优先级任务
1. [填写高优先级任务]
2. [填写次优先级任务]

### 长期目标
- [填写长期目标]

## 五、其他说明
[其他需要说明的事项]
EOF

echo "报告已生成: $REPORT_FILE"
```

### 5. 优化建议

- **分类整理提交**：将git提交按功能、修复、优化等分类
- **提取关键信息**：从提交信息中提取任务编号、功能点等
- **估算工作量**：根据提交数量和大致复杂度估算工作量
- **关联TODO**：将TODO注释与相关代码文件关联

## 进阶功能

### 项目多仓库支持

如果用户工作在多个git仓库中，可以依次分析每个仓库：

```bash
# 查找所有git仓库
find . -name ".git" -type d | while read gitdir; do
  repo_path=$(dirname "$gitdir")
  echo "分析仓库: $repo_path"
  cd "$repo_path"
  # 收集该仓库的数据
  cd - > /dev/null
done
```

### 时间统计

估算工作时间分配：

```bash
# 粗略估算：每个提交代表一定工作时间
# 可以根据提交数量、代码行数等估算
TOTAL_HOURS=$((COMMIT_COUNT * 2))  # 假设每个提交平均2小时
echo "估算工作时间: $TOTAL_HOURS 小时"
```

### 报告美化

生成更美观的HTML报告：

```bash
# 使用pandoc转换Markdown到HTML
if command -v pandoc &> /dev/null; then
  pandoc "$REPORT_FILE" -o "${REPORT_FILE%.md}.html"
  echo "HTML报告已生成: ${REPORT_FILE%.md}.html"
fi
```

## 使用示例

### 示例1：生成周报

用户说："帮我生成这周的周报"

操作：
1. 确定时间范围为最近7天
2. 收集git提交和TODO
3. 生成周报Markdown文件
4. 提供报告预览

### 示例2：生成日报

用户说："生成今天的日报"

操作：
1. 确定时间范围为最近1天
2. 收集当天的git提交
3. 生成日报

### 示例3：自定义时间范围

用户说："生成最近3天的工作报告"

操作：
1. 确定时间范围为最近3天
2. 收集数据
3. 生成报告

## 常见问题

### 1. 没有git提交记录怎么办？
如果git提交记录为空，可以：
- 询问用户是否有其他工作记录
- 基于TODO项目生成报告
- 提示用户记录工作日志

### 2. TODO注释太多怎么办？
- 按优先级筛选
- 按文件类型分组
- 建议用户清理过期TODO

### 3. 如何提高报告质量？
- 鼓励用户写有意义的提交信息
- 定期维护TODO列表
- 使用任务管理系统（如Jira、Trello）集成

### 4. 报告包含敏感信息怎么办？
- 提醒用户检查报告内容
- 提供编辑建议
- 可以添加保密提示

## 最佳实践

### 提交信息规范
鼓励用户使用规范的提交信息格式：
```
类型(范围): 描述

详细说明（可选）

相关任务: #任务号
```

### TODO注释管理
- 为TODO添加优先级标签：`TODO(P1)`、`TODO(P2)`
- 添加负责人和截止日期：`TODO(@user:2024-01-01)`
- 定期回顾和清理

### 工作报告习惯
- 每日/每周固定时间生成报告
- 及时更新TODO状态
- 保留历史报告供参考

## 提示与技巧

- **自动定时生成**：可以设置cron任务自动生成日报
- **团队共享**：将报告分享给团队成员，提高透明度
- **进度追踪**：对比历史报告，追踪工作进度
- **工作回顾**：使用报告进行月度/季度工作回顾

---

*本技能旨在自动化工作报告生成过程，但报告内容仍需用户审阅和补充。*
*定期的工作总结有助于个人成长和团队协作，建议养成记录习惯。*