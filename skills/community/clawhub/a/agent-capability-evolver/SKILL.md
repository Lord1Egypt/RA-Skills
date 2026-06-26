---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_e93477ec5cc011f1abc85254006c9bbf
    ReservedCode1: Rz8Zg2WYKa3Lbhd4eDb5eJiSQkQDUY6fL4iCdBD187TaSQULSipLmqvDVWpetOAAQN7zNfg1rfK3s2SR9kZC4yHYM9N8bmP/JeRKNjtNerHwG3TRprmpjJd3C3bcUwvuzKucoQalzrMWLLc6bzXVQEq8TcV9LEeO3LxSNzh/xpZ66DGVYC1MnSDZtlw=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_e93477ec5cc011f1abc85254006c9bbf
    ReservedCode2: Rz8Zg2WYKa3Lbhd4eDb5eJiSQkQDUY6fL4iCdBD187TaSQULSipLmqvDVWpetOAAQN7zNfg1rfK3s2SR9kZC4yHYM9N8bmP/JeRKNjtNerHwG3TRprmpjJd3C3bcUwvuzKucoQalzrMWLLc6bzXVQEq8TcV9LEeO3LxSNzh/xpZ66DGVYC1MnSDZtlw=
---



# 认知自我进化 · 智能体能力进化引擎

为 OpenClaw AI Agent 提供系统化的自我优化框架。本技能不执行代码，运行时消耗极低，完全免费。

## 核心能力

| 功能 | 说明 |
|------|------|
| 失败分析 | 扫描执行日志，按 8 种错误类型自动分类 |
| 能力诊断 | 识别当前 Agent 的工具选择、参数配置、上下文管理短板 |
| 补丁生成 | 自动生成规则补丁 / 参数配置 / 触发词优化文件 |
| Skill 推荐 | 根据短板匹配 ClawHub 社区 Skill 并生成安装建议 |
| 进化追踪 | 维护进化日志，支持版本回滚和冲突检测 |

## 触发场景

当用户说这些话时激活本技能：

- "分析一下你最近失败的任务"
- "根据我的使用习惯，优化你的工作方式"
- "为什么你总是用错工具？找找原因"
- "帮我配置一个自我改进机制"
- "评估你当前的能力短板"
- "推荐一些能提升你效率的 Skill"

## 使用方式

### 方式一：单次分析

```
用户：分析我过去一周里你执行失败的任务，找出原因
```

Agent 会读取 `LOG_DIR` 下的日志，按 `references/evolution_rules.md` 定义的分类体系输出分析报告。

### 方式二：持续进化（推荐）

```
用户：开启自我进化模式，每次任务失败后自动分析并优化
```

Agent 会在每次任务结束后自动执行轻量级分析，当同一错误累计达到阈值时生成补丁。

## 执行流程

### 阶段 A：数据采集

1. 读取 `{LOG_DIR}` 下的执行日志（支持 JSON / Markdown / 纯文本格式）
2. 提取任务ID、工具调用链、错误信息、用户反馈
3. 计算各错误类型的频率和严重程度分布

### 阶段 B：根因分析

参考 `{baseDir}/references/evolution_rules.md` 第一章「错误分类体系」，对每条失败记录打标签：

- `AMBIGUOUS_INSTRUCTION` — 指令模糊
- `WRONG_TOOL` — 工具选择错误
- `PARAM_ERROR` — 参数错误
- `CONTEXT_LOSS` — 上下文遗漏
- `OUTDATED_KNOWLEDGE` — 知识过时
- `PERMISSION_DENIED` — 权限不足
- `EXTERNAL_FAILURE` — 外部依赖故障
- `EXPECTATION_MISMATCH` — 用户预期偏差

### 阶段 C：策略匹配

根据错误标签匹配进化策略（详见 `references/evolution_rules.md` 第二章「进化策略矩阵」）：

- **P0 立即修复**：错误明确且频繁（3 次内 ≥ 2 次），自动生成补丁
- **P1 建议修复**：多种方案可选，生成建议等待用户确认
- **P2 观察标记**：偶发错误，记录但不处理

### 阶段 D：补丁生成

在 `{工作目录}/evolution/patches/` 下生成补丁文件。补丁类型：

- `patch_rule_*.md` — 规则追加
- `patch_defaults_*.yaml` — 参数默认值
- `patch_triggers_*.md` — 触发词优化
- `patch_toolmap_*.md` — 工具映射修正
- `patch_skill_rec_*.md` — Skill 推荐

补丁格式严格遵循 `references/evolution_rules.md` 第三章规范。

### 阶段 E：冲突检测与记录

生成补丁后，检测与已有补丁的冲突（直接冲突 / 间接冲突 / 链式冲突），按「安全性 > 时效性 > 性能 > 用户体验」优先级解决。最终更新 `evolution/evolution_log.md`。

## 输出格式

### 单次分析报告

```markdown
# Agent 能力进化报告
**分析时间**: {时间}
**分析范围**: {日志起止日期}，共 {N} 条任务记录

## 错误分布
| 错误类型 | 次数 | 占比 | 严重程度 | 趋势 |
|----------|------|------|----------|------|
| WRONG_TOOL | 5 | 35% | SEV_HIGH | ↑ |

## 根因分析
{详细分析}

## 进化建议
| 优先级 | 策略 | 补丁类型 | 说明 |
|--------|------|----------|------|
| P0 | 自动修复 | patch_rule | {说明} |

## 推荐 Skill
| Skill | 来源 | 匹配度 | 说明 |
|-------|------|--------|------|
```

## 注意事项

- 本技能仅生成文本建议和配置文件，**不修改系统代码**
- `LOG_DIR` 环境变量必须指向有效的 Agent 日志目录，否则技能标记为「不可用」
- `EVOLUTION_STRATEGY` 控制自动修复的激进程度，建议新手使用 `conservative`
- 补丁存储在 `evolution/patches/` 目录，可通过删除该目录下文件来回滚
- 冲突补丁会自动归档到 `patches/archive/`，不会直接覆盖

## 定价

完全免费。本技能核心是为 AI 写提示词和生成配置文件，运行时无外部 API 调用，消耗极低。
*（内容由AI生成，仅供参考）*
