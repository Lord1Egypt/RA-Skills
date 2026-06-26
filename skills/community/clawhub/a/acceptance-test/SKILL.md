---
name: acceptance-test
description: |
  验收测试助手 - 验证系统是否满足业务需求，确保交付质量。
  当用户需要以下功能时触发此skill：
  (1) 业务需求验证
  (2) 用户场景测试
  (3) 验收标准检查
  (4) 客户验收支持
  (5) 验收报告生成
---

# Acceptance Test

验收测试助手 — 确保交付符合预期

## 核心能力

### 1. 需求验证
- **功能验证** - 功能点检查
- **验收标准** - AC验证
- **边界条件** - 边界测试
- **异常场景** - 错误处理
- **性能指标** - 性能验证

### 2. 用户场景
- **BDD测试** - 行为驱动
- **Gherkin** - Given-When-Then
- **场景覆盖** - 用户故事
- **角色测试** - 不同角色
- **权限验证** - 权限检查

### 3. 验收流程
- **准入条件** - 准入检查
- **验收执行** - 测试执行
- **缺陷记录** - 问题跟踪
- **签字确认** - 验收签字
- **交付物** - 交付清单

### 4. 报告生成
- **通过率** - 验收结果
- **风险清单** - 遗留风险
- **质量评估** - 质量评分
- **发布建议** - 发布决策
- **改进建议** - 改进点

## 使用工作流

```bash
# 执行验收测试
python scripts/acceptance_runner.py --stories stories.json --env staging

# BDD测试
python scripts/bdd_runner.py --features features/ --steps steps/

# 验收报告
python scripts/acceptance_report.py --results results.json --signoff required
```

---

*验收测试是交付前的最后一道关卡，确保价值交付。*
