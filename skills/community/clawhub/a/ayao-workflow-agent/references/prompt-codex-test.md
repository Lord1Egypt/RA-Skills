# Codex Test Prompt Template

用于里程碑完成后派发给 `codex-test` agent。
目标：针对里程碑涉及的模块写单元测试 + 跑验收脚本，**不写业务代码**。

## 调用命令格式

```bash
codex exec --dangerously-bypass-approvals-and-sandbox 'PROMPT'
```

## 单元测试边界（铁律）

### ✅ 要测的
| 类型 | 举例 | 原因 |
|------|------|------|
| 算法 / 计算逻辑 | 策略引擎信号、风控规则、仓位计算、止盈止损判断 | 数据驱动，边界条件多，最容易出 bug |
| 数据转换 | 订单参数构建、价格格式化、EIP712 签名构造 | 错一个字段就下错单 |
| 状态机 / 业务规则 | 订单生命周期状态流转、风控审批逻辑 | 规则组合复杂，必须穷举关键路径 |

### ❌ 不测的
| 类型 | 原因 |
|------|------|
| 前端组件 / 页面 | 视觉验收靠人眼，单测没意义 |
| API 路由 / CRUD | 由验收脚本（verify-phaseX.ts）端到端覆盖 |
| 网络连接 / WS | 连通性在开发阶段已验证，不重复测 |
| 持久化层 CRUD | 验收脚本已覆盖，无需单独单测 |

### Mock 策略
- **只 mock 外部 IO**（CLOB API、DB、WebSocket）
- **不 mock 内部逻辑** — 策略引擎、风控模块用真实实现跑，不绕过
- 目标：测试快（秒级），但覆盖真实计算路径

### 通过标准
- 验收脚本：所有 checks PASSED
- 单元测试：0 failed，覆盖被测模块的所有主要分支（正常路径 + 关键边界）

## 模板

```
## Project
[Project name] — [one-line description]
Working directory: [absolute path]

## Milestone
[M1]: [里程碑名称]
包含任务：[T001, T002, T003]
测试说明：[验证什么功能]

## 你的任务
这是一个测试任务，不要写业务代码。请按以下步骤执行：

### Step 1: 跑验收脚本（如有）
cd [project_dir]/[subdirectory]
npx tsx scripts/[verify-script].ts
记录输出结果。

### Step 2: 针对以下文件写单元测试
- `[src/providers/clob-ws.ts]` — [测试重点：连接、心跳、快照格式]
- `[src/engine/risk-control.ts]` — [测试重点：风控规则、边界条件]

测试文件放在对应的 `__tests__/` 或 `*.test.ts` 位置，参考项目现有测试风格。
如果项目没有测试框架，使用 vitest（已在 devDependencies 中，否则先检查 package.json）。

### Step 3: 跑单元测试
npx vitest run [test-file-pattern]
（或项目已有的测试命令，查看 package.json scripts）

### Step 4: 汇报结果
输出格式：
✅ verify-phase2.ts: PASSED (12/12 checks)
✅ clob-ws.test.ts: 8 passed, 0 failed
❌ risk-control.test.ts: 2 failed
  - runRiskCheck: size limit not enforced when position is short
  - runRiskCheck: returns null when riskControl undefined (expected false)

如果有失败，请说明失败的具体原因和行号。

### Step 5: Commit 测试代码
git add -A && git commit -m "test([milestone-id]): add unit tests for [module names]" && git push

## Reference Code
请先阅读以下文件了解项目模式：
- `[src/providers/clob-ws.ts]` — 被测模块
- `[package.json]` — 确认测试框架和可用脚本

## Do NOT
- 修改业务代码（只改 *.test.ts 和 scripts/verify-*.ts）
- 添加 npm 依赖（除非测试框架缺失，且先确认）
- 跳过失败的测试（用 skip 掩盖问题）
- 修改 tsconfig.json 或其他配置文件

## Done When
- 验收脚本输出明确（PASSED 或具体失败项）
- 单元测试覆盖 scope 内所有主要模块的核心路径
- 测试代码已 commit & push
- 最终汇报结果（每个文件的 pass/fail 统计）
```

## 常见错误与预防

| 错误 | 原因 | 预防 |
|------|------|------|
| 测试无法运行（import 失败） | 项目路径或模块解析问题 | 先 cd 进对应子项目目录，确认 tsconfig 路径 |
| Mock 不真实导致测试没意义 | 过度 mock 掩盖真实问题 | 优先用真实依赖，DB 用测试数据库或 in-memory |
| 测试文件不 commit | 忘了或认为测试是临时的 | commit 命令写死在 prompt 里 |
| 测试全过但验收脚本失败 | 单元粒度太细没覆盖集成问题 | Step 1 先跑验收脚本，失败直接汇报 |
