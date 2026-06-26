# ai-dev-guardrails v3.0 — Five-Layer Defense Architecture

## v3.0 新增 (2026-05-19)

| 新增 | 来源 | 内容 |
|------|------|------|
| M8: Quality Gate | production-code-audit + Industry BP | 五维代码审计(架构/安全/性能/质量/测试) + 严重等级 + 量化对比 + 报告模板 |
| M9: Scope Fidelity Gate | moyu | SF-L1~L4范围忠实度检测 + 15条Anti-Grinding表 + 文件变更审计 + 级联修复检测 |
| Anti-Hallucination扩展 | moyu | 7条→15条，合并moyu冲动对照表 |
| 审计日志 | Industry Layer 5 | 跨层Guardrail Activity Log（记录每次拦截/检查/变更） |
| Related Skills更新 | — | 新增Industry frameworks引用 |

## 五层防御架构

```
Layer 1: 指令层  L0-L5 决策流    — 拦截不合理/模糊/错误需求
Layer 2: 项目层  M1-M7           — 契约/仪表盘/关口/审计/偏离/L5防御
Layer 3: 交付层  M6 Reliability  — 回归安全 + 迭代健康
Layer 4: 审计层  M8 Quality      — 五维代码质量 + 量化度量 [NEW v3.0]
Layer 5: 范围层  M9 Fidelity     — 文件变更审计 + 过度工程检测 [NEW v3.0]
```

## 文件状态

| 文件 | 行数 |
|------|:----:|
| SKILL.md | 968 |
| scenarios.md | 574 |
| test-report.md | 946 |
| l5-defense-test.md | 563 |
| boundaries.md | (unchanged) |
| **总计** | **~3,050** |
