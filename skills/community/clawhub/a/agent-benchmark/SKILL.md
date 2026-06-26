# agent-benchmark - AI Agent 能力评估基准

**版本**: 0.1.0  
**作者**: 小蒲萄 (Clawd)  
**创建日期**: 2026-03-18  
**类型**: SWE-bench Lite (PowerShell Edition)

---

## 📖 简介

评估 AI Agent 任务完成能力的基准测试系统，灵感来源于 SWE-bench。

**核心功能**：
- ✅ 12 个标准化测试任务
- ✅ 5 大能力维度评估
- ✅ 自动化评分和报告生成
- ✅ 分类别能力分析
- ✅ 可自定义扩展任务

---

## 🎯 评估维度

| 维度 | 权重 | 测试内容 |
|------|------|---------|
| **文件操作** | 15% | 文件读写、目录管理、路径处理 |
| **数据处理** | 35% | JSON/CSV、数组、字符串、正则 |
| **系统操作** | 15% | 环境变量、日期时间、系统信息 |
| **健壮性** | 15% | 错误处理、异常捕获、边界条件 |
| **代码质量** | 20% | 函数定义、代码复用、最佳实践 |

---

## 🚀 快速开始

### 运行完整基准测试

```powershell
# 进入技能目录
cd C:\Users\99236\.openclaw\workspace\skills\agent-benchmark

# 运行基准测试
.\src\benchmark-runner.ps1
```

### 自定义任务文件

```powershell
# 使用自定义任务集
.\src\benchmark-runner.ps1 -TaskFile ".\tasks\custom-tasks.json"

# 指定输出目录
.\src\benchmark-runner.ps1 -OutputDir ".\reports\my-benchmark"

# 详细输出模式
.\src\benchmark-runner.ps1 -Verbose
```

---

## 📋 测试任务清单

### Easy (基础能力)

| ID | 任务 | 类别 | 分值 | 测试点 |
|----|------|------|------|--------|
| task-001 | 文件创建与内容写入 | 文件操作 | 10 | 基础文件 I/O |
| task-002 | JSON 数据处理 | 数据处理 | 10 | JSON 解析/序列化 |
| task-003 | 数组操作 | 数据处理 | 10 | 过滤/聚合 |
| task-011 | 环境变量访问 | 系统操作 | 10 | 系统信息读取 |

### Medium (中级能力)

| ID | 任务 | 类别 | 分值 | 测试点 |
|----|------|------|------|--------|
| task-004 | 目录列表与过滤 | 文件操作 | 15 | 文件搜索/统计 |
| task-005 | 字符串操作 | 数据处理 | 15 | 多步骤转换 |
| task-006 | 日期时间计算 | 系统操作 | 15 | 时间差计算 |
| task-007 | CSV 数据生成 | 数据处理 | 20 | 结构化数据导出 |
| task-012 | 正则表达式匹配 | 数据处理 | 20 | 模式提取 |

### Hard (高级能力)

| ID | 任务 | 类别 | 分值 | 测试点 |
|----|------|------|------|--------|
| task-008 | 错误处理测试 | 健壮性 | 20 | try-catch 异常处理 |
| task-009 | 多步骤数据管道 | 数据处理 | 25 | 复杂数据流 |
| task-010 | 函数定义与调用 | 代码质量 | 25 | 代码复用/算法 |

**总分**: 195 分  
**及格线**: 60% (117 分)  
**优秀线**: 80% (156 分)

---

## 📊 评分标准

### 单任务评分

```
单任务得分 = 基础分 + 验证分 + 效率分

基础分:
- 成功完成：50%
- 部分完成：30%
- 失败：0%

验证分 (50%):
- 输出匹配预期：50%
- 输出部分匹配：25%
- 输出不匹配：0%

效率分 (10%):
- 在预期时间内完成：+10%
- 超时：0%
```

### 总体评级

| 平均分 | 评级 | 说明 |
|--------|------|------|
| ≥ 0.9 | 🏆 S 级 | 生产就绪，超越预期 |
| ≥ 0.8 | ✅ A 级 | 生产就绪，表现优秀 |
| ≥ 0.7 | 👍 B 级 | 良好，少量改进空间 |
| ≥ 0.6 | ⚠️ C 级 | 及格，需要改进 |
| < 0.6 | ❌ D 级 | 不及格，需大幅提升 |

---

## 📁 文件结构

```
skills/agent-benchmark/
├── SKILL.md                      # 技能文档（本文件）
├── src/
│   ├── benchmark-runner.ps1      # 基准测试执行器
│   └── scoring-engine.ps1        # 评分引擎（可选扩展）
├── tasks/
│   ├── default-tasks.json        # 默认任务集（12 题）
│   ├── custom-tasks.json         # 自定义任务（用户添加）
│   └── advanced-tasks.json       # 高级任务集（未来扩展）
├── reports/
│   ├── benchmark-report-*.md     # 测试报告（自动生成）
│   └── summary.json              # 汇总数据（可选）
└── README.md                     # 使用说明
```

---

## 🧪 示例任务

### 任务示例：JSON 数据处理

```json
{
  "id": "task-002",
  "name": "JSON Data Processing",
  "category": "Data Processing",
  "difficulty": "Easy",
  "description": "Parse JSON and extract specific field",
  "script": "$data = @{Name='Clawd'; Type='AI'; Version='1.0'} | ConvertTo-Json; $parsed = $data | ConvertFrom-Json; Write-Host \"Name: $($parsed.Name)\"",
  "expectedOutput": "Name: Clawd",
  "expectedTimeSeconds": 5,
  "points": 10
}
```

### 任务示例：错误处理测试

```json
{
  "id": "task-008",
  "name": "Error Handling Test",
  "category": "Robustness",
  "difficulty": "Hard",
  "description": "Handle errors gracefully with try-catch",
  "script": "try { \n  $content = Get-Content -Path 'nonexistent-file.txt' -ErrorAction Stop\n  Write-Host 'File found'\n} catch {\n  Write-Host 'Error handled: File not found'\n}",
  "expectedOutput": "Error handled: File not found",
  "expectedTimeSeconds": 5,
  "points": 20
}
```

---

## 📈 报告示例

运行基准测试后生成 Markdown 报告：

```markdown
# Agent Benchmark Report

**Generated**: 2026-03-18 09:30:00  
**Total Tasks**: 12  
**Average Score**: 0.85 / 1.0  
**Average Time**: 8.5s

## 📊 Summary

| Metric | Value |
|--------|-------|
| **Success Rate** | 83.3% |
| **Partial Completion** | 8.3% |
| **Failure Rate** | 8.3% |
| **Average Score** | 0.85 |
| **Avg Execution Time** | 8.5s |

## 📈 Detailed Results

| Task | Category | Difficulty | Status | Score | Time (s) |
|------|----------|------------|--------|-------|----------|
| File Creation | File Ops | Easy | ✅ Success | 1.0 | 2.3 |
| JSON Processing | Data | Easy | ✅ Success | 1.0 | 3.1 |
| ... | ... | ... | ... | ... | ... |
```

---

## 🔧 自定义任务

### 创建自定义任务集

创建 `tasks/custom-tasks.json`:

```json
{
  "metadata": {
    "version": "1.0.0",
    "name": "My Custom Tasks",
    "description": "Custom benchmark for specific use case"
  },
  "tasks": [
    {
      "id": "custom-001",
      "name": "My Custom Task",
      "category": "Custom Category",
      "difficulty": "Medium",
      "description": "Description of what to do",
      "script": "Write-Host 'Hello World'",
      "expectedOutput": "Hello World",
      "expectedTimeSeconds": 5,
      "points": 15
    }
  ]
}
```

### 运行自定义任务

```powershell
.\src\benchmark-runner.ps1 -TaskFile ".\tasks\custom-tasks.json"
```

---

## 🎯 使用场景

### ✅ 适合的场景

- **Agent 能力评估** - 新版本发布前测试
- **回归测试** - 确保更新未破坏功能
- **对比测试** - 不同配置/模型对比
- **能力诊断** - 识别薄弱环节
- **持续集成** - 自动化质量门禁

### ❌ 不适合的场景

- **性能基准测试** - 非性能导向
- **安全测试** - 无安全相关任务
- **大规模负载测试** - 设计为轻量级

---

## 📊 指标解释

### Task Completion Rate (任务完成率)
成功完成的任务数 / 总任务数

### Average Execution Time (平均执行时间)
所有任务执行时间的算术平均值

### Success Rate (成功率)
达到 80% 以上分数的任务比例

### Error Rate (错误率)
执行中出错的任务比例

### Code Quality (代码质量)
基于代码结构、复用性、最佳实践的综合评分

---

## 🔍 故障排查

### 常见问题

**Q: 任务执行超时**
```
原因：脚本复杂度过高或死循环
解决：检查任务脚本，增加 expectedTimeSeconds
```

**Q: 输出验证失败**
```
原因：实际输出与 expectedOutput 不匹配
解决：调整 expectedOutput 正则表达式或检查脚本逻辑
```

**Q: 报告生成失败**
```
原因：输出目录不存在或权限问题
解决：确保 OutputDir 存在且有写权限
```

---

## 📝 更新日志

### v0.1.0 (2026-03-18)
- ✅ 初始版本发布
- ✅ 12 个标准化测试任务
- ✅ 5 大评估维度
- ✅ 自动化评分系统
- ✅ Markdown 报告生成
- ✅ 自定义任务支持

---

## 🤝 贡献

欢迎提交新的测试任务！请遵循以下格式：

1. 任务难度分级明确（Easy/Medium/Hard）
2. 预期输出可自动化验证
3. 执行时间在 30 秒以内
4. 不依赖外部网络/API
5. 不修改系统配置

---

## 📄 许可证

MIT License

---

*最后更新：2026-03-18*
