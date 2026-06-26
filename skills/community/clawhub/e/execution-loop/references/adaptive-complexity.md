# Pattern 1.3: Adaptive Complexity Scoring（任务复杂度自适应）

## 问题

所有任务使用相同的 harness 配置——简单的拼写修复和复杂的架构重构都走同样的 Ralph + Handoff + Verification 全流程。简单任务 overhead 太高，复杂任务可能保障不足。

来源：`rubenzarroca/sdd-autopilot` — 8 阶段 pipeline 的复杂度分类

## 原理

在执行前做 triage——评估任务复杂度，自动选择执行模式。

### 复杂度分级

| 等级 | 判断标准 | 执行模式 |
|------|---------|---------|
| Trivial | 单文件、< 10 行改动、无依赖 | Express（跳过 plan/verify） |
| Low | 单文件、可能需要测试更新 | Light（plan + implement） |
| Medium | 2-5 文件、涉及跨模块修改 | Standard（plan + implement + verify） |
| High | 5+ 文件、架构变更、新 API | Full（plan + implement + verify + review） |
| Critical | 安全修复、数据迁移、生产变更 | Full + Agent-type 验证门禁（Pattern 1.1 模式 C） |

### 执行模式映射

| 模式 | 启用的 Pattern |
|------|---------------|
| Express | 仅 Pattern 6.5（原子写入） |
| Light | + Pattern 2.1（工具错误升级） |
| Standard | + Pattern 1.1（Ralph）+ Pattern 3.5（Context 估算） |
| Full | + Pattern 3.1（Handoff）+ Pattern 6.3（Hook Bracket）+ Pattern 6.1（Post-Edit 诊断） |
| Full+Gate | + Pattern 1.1 模式 C（Agent-type 验证） + Pattern 2.5（Scoped Hooks） |

## 实现

在 session 启动时（UserPromptSubmit hook + `once: true`）做 triage：

```bash
# 分析 prompt 中的文件数、改动范围、关键词
FILES_MENTIONED=$(echo "$PROMPT" | grep -oE '[a-zA-Z_/]+\.(py|ts|rs|go|cpp|java)' | wc -l)
HAS_SECURITY=$(echo "$PROMPT" | grep -qiE 'security|vulnerability|CVE|auth|密钥|安全' && echo 1 || echo 0)
HAS_MIGRATION=$(echo "$PROMPT" | grep -qiE 'migration|migrate|数据迁移' && echo 1 || echo 0)

if [ "$HAS_SECURITY" = "1" ] || [ "$HAS_MIGRATION" = "1" ]; then
  LEVEL="critical"
elif [ "$FILES_MENTIONED" -gt 5 ]; then
  LEVEL="high"
elif [ "$FILES_MENTIONED" -gt 1 ]; then
  LEVEL="medium"
elif [ "$FILES_MENTIONED" -eq 1 ]; then
  LEVEL="low"
else
  LEVEL="trivial"
fi
```

## 安全规则

**MUST：当 triage 不确定时，默认 Standard，NEVER 默认 Express。** Express 跳过验证——如果一个安全修复被误判为 Trivial，agent 会不经验证直接提交。

**MUST：Express 模式不应用于任何写入生产代码的操作。** Express 适合只读分析、文档更新、配置微调。

## 已知局限

文件计数 triage 是极简启发式。已知失败场景：
- "Fix the auth bug" 提到 0 个文件但可能涉及 10+ 文件
- 带连字符/数字的文件名（`my-component.ts`, `v2.config.js`）匹配不到
- 上下文信息（是否涉及安全、数据库、支付）比文件数更重要

**生产建议**：用 LLM triage（一次 Haiku 调用评估复杂度）替代 regex 启发式。

## Tradeoff

- Triage 本身会消耗一些 token（但远少于在简单任务上运行全流程的 overhead）
- 误判复杂度会导致过度/不足保障——文件计数只是起点，需要持续优化
- 历史数据可以提升 triage 准确度（追踪实际 vs 预估复杂度）
