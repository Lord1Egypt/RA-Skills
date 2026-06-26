# Verify 操作指南

Verify 阶段的完整操作步骤、报告格式和错误摘要生成规则。

## 验证操作步骤

1. 读取 `plan-{round}.md`，提取验收标准和文件清单
2. 检查项目是否有测试：`scripts/run_tests.sh`、`pytest.ini`、`pyproject.toml`、`package.json`、`Makefile` 等
3. 如有测试，运行测试并捕获完整输出到 `verify_test_log-{round:03d}.txt`；优先使用项目约定命令（如 项目源码测试用 `scripts/run_tests.sh`）
4. 执行 `git -C {cwd} diff --stat` 和 `git -C {cwd} diff > verify_diff-{round:03d}.patch`；非 git repo 时记录无法生成 diff，用文件 mtime 做弱检查
5. 逐条比对验收标准，给出 ✅/❌/⚠️ 和证据
6. 生成 `verify_report-{round:03d}.md`（格式见下方），结论必须是 `PASSED` 或 `FAILED`
7. 如果失败，生成错误摘要（≤500字）用于下一轮 spec_plan.md

## verify_report.md 格式

```markdown
# Verify Report - Round {round_number}
> Task: {task_id} | Status: PASSED/FAILED

## 总结
{一句话描述验证结果}

## 验证详情

### 测试运行
- **命令**: {执行的测试命令}
- **退出码**: {code}
- **结果**: PASSED/FAILED
- **关键错误**:
  ```
  {前5个最关键的错误，去重去噪}
  ```

### 文件变更检查
- **预期修改**: {plan中的文件清单}
- **实际修改**: {git diff结果}
- **差异**: {不在plan中但被修改的文件}

### 验收标准核对
| 标准 | 状态 | 备注 |
|------|------|------|
| {标准1} | ✅/❌/⚠️ | {说明} |

## 问题汇总
1. **P0**: {关键问题}
2. **P1**: {重要问题}

## 建议修复方向
1. {针对P0的修复建议}

## 附件路径
- 完整测试日志: verify_test_log-{round}.txt
- Git diff: verify_diff-{round}.patch
```

### 格式设计要点

- **分层信息**：总结→详情→附件，OMC 可以按需深入
- **P0/P1 优先级标记**：帮助 OMC 聚焦关键问题而非被噪声淹没
- **建议修复方向**：不只是报告问题，还给出方向，让下一轮 plan 更有针对性
- **关键错误限制 5 个**：避免数千行测试日志直接灌给 OMC

## 错误摘要生成规则

从 verify_report 提取下一轮 OMC 需要的错误摘要：

- 只保留 P0 和 P1 问题，忽略噪声、风格建议和重复堆栈
- 每个问题一句话描述 + 定位（`文件:行号`）；无法定位时写模块或命令名
- 附上测试失败的关键 assert、异常类型或退出码
- 总长度不超过 500 字；超过时按 P0 优先截断
- 连续两轮 P0 问题文本或根因相同 → 触发 `consecutive_same_error` 退出
- `no_progress` 判断：最近两轮 `问题汇总 + 建议修复方向` 相似度 >80% 且无新增通过项

### 为什么限制 500 字？

OMC 的 spec_plan.md 需要包含完整上下文（项目结构、需求、前序轮次报告）。如果错误摘要太长，会挤占其他关键上下文的空间。500 字足够描述 3-5 个关键问题及其定位，OMC 据此做出的 plan 质量和拿 5000 字日志差不多。
