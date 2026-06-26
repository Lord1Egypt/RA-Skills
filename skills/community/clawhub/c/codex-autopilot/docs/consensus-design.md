# Autopilot 两项核心改进 — 共识方案

*整合 AgentTeam 外部分析 + Codex 内部设计的共识*

---

## 改进一：Test Agent 自动测试覆盖率提升

### 共识结论

| 决策点 | 共识 | 理由 |
|--------|------|------|
| 独立 vs 复用 Codex | **默认复用（shared），可选隔离** | Token 成本控制；串行避免冲突 |
| 触发时机 | **Review CLEAN 后 + idle 时** | commit 后太频繁；review 后是自然的"收尾"节点 |
| 测试写在哪 | **走 branch（与改进二联动）** | 隔离风险，失败可删 |
| 覆盖率策略 | **底线不下降 + 增量治理** | 先守住底线，再逐步提升 |
| 框架适配 | **适配器模式，统一 coverage JSON** | Jest/JUnit/bats 各写 adapter |
| 质量门禁 | **断言密度 + 覆盖增益 + 重跑验证** | 防空测试，确保有意义 |

### 架构图

```
Review CLEAN
    │
    ▼
test-agent.sh evaluate
    │ 收集 coverage → 归一化 JSON
    ▼
test-task-generator.sh
    │ 找低覆盖文件 → 生成任务（每轮 ≤3 条）
    ▼
task-queue.sh add <project> "补测试: src/foo.ts" --type test
    │
    ▼
watchdog idle 检测 → 消费队列
    │
    ▼
branch-manager.sh ensure → 创建 ap/<project>/test/<timestamp>
    │
    ▼
Codex 在 branch 上写测试 + commit
    │
    ▼
test-quality-gate.sh 校验
    ├─ 通过 → branch ready_merge → auto-merge → ✅
    └─ 失败 → 重新入队（最多 2 次）→ 标记 test_issues
```

### config.yaml

```yaml
test_agent:
  enabled: true
  mode: "shared"                    # shared | isolated
  trigger:
    on_review_clean: true           # 主触发
    on_commit_evaluate: true        # 轻量评估（不生成任务）
    nightly: "02:30"                # 兜底补偿
  queue:
    max_tasks_per_round: 3          # 防队列被测试淹没
    priority: "normal"
  coverage:
    changed_files_min: 80           # 本轮变更文件最低覆盖率
    global_no_regression: true      # 全局覆盖率不得下降
    ratchet_weekly: 1               # 每周自动上调 1%
    ratchet_cap: 90                 # 封顶
    critical_paths: ["src/core", "scripts"]
    critical_min: 90
  quality_gate:
    min_assertions: 1               # 每个测试文件至少 1 个有效断言
    disallow_empty: true
    require_coverage_delta: true    # 覆盖率必须不下降
    rerun_times: 2                  # 重跑验证稳定性
  frameworks:
    jest:
      test_cmd: "npm test -- --coverage --ci"
      coverage_file: "coverage/coverage-summary.json"
    junit:
      test_cmd: "./gradlew test jacocoTestReport"
      coverage_file: "build/reports/jacoco/test/jacocoTestReport.xml"
    bats:
      test_cmd: "bats test/"
      coverage_file: null           # 降级为 test pass rate
```

### 新增脚本

| 脚本 | 职责 | 行数估计 |
|------|------|----------|
| `test-agent.sh` | 主编排：evaluate/enqueue | ~200 |
| `coverage-collect.sh` | 框架探测 + coverage 归一化 | ~150 |
| `test-task-generator.sh` | 根据覆盖缺口生成任务文本 | ~100 |
| `test-quality-gate.sh` | 断言/覆盖/稳定性门禁 | ~120 |

### 分阶段实施

**Phase 1（3 天）**：Jest only + shared 模式 + review clean 触发 + 基础门禁
**Phase 2（2 天）**：JUnit/bats adapter + 完整质量门禁 + nightly 补偿
**Phase 3（2 天）**：isolated 模式 + 覆盖率 ratchet + status-sync 集成

---

## 改进二：Branch 隔离模式

### 共识结论

| 决策点 | 共识 | 理由 |
|--------|------|------|
| 什么走 branch | **自动任务（queue 派发）走 branch；Wesley 手动开发留 main** | 核心开发效率不受影响 |
| 命名规范 | **`ap/<window>/<type>/<yyyymmdd-hhmmss>`** | 清晰可追溯 |
| auto-merge 条件 | **auto-check 通过 + 测试通过 + 无冲突** | 最小安全条件 |
| merge 策略 | **squash merge** | 保持 main 历史干净 |
| 冲突处理 | **自动 rebase 1 次 → 失败则通知人工** | 避免复杂自动解决 |
| 清理策略 | **merged 立删；failed 保留 7 天；abandoned TTL 72h** | 防垃圾堆积 |
| Layer 2 review | **branch 上 review（可选）** | 默认 auto-check 通过即可 merge |

### 架构图

```
task-queue.sh 消费任务
    │
    ▼
tmux-send.sh --branch-mode auto
    │
    ▼
branch-manager.sh ensure
    │ git checkout -b ap/<window>/<type>/<ts>
    ▼
Codex 在 branch 上开发 + commit
    │
    ▼
watchdog 检测到 branch commit + idle
    │
    ▼
auto-check.sh → 通过？
    ├─ 否 → nudge 修复（在 branch 上）
    └─ 是 ↓
         ▼
    branch-manager.sh auto-merge
         │ rebase → squash merge → push
         ├─ 成功 → 清理分支 → ✅ Discord 通知
         └─ 冲突 → 标记 conflict → 生成冲突修复任务
```

### config.yaml

```yaml
branch_isolation:
  enabled: true
  default_mode: "auto"              # auto | on | off
  base_branch: "main"
  naming:
    prefix: "ap"
    include_timestamp: true
  policy:
    force_branch_types:             # 这些任务强制走 branch
      - feature
      - refactor
      - test
      - review_fix
    allow_main_types:               # 这些可留 main
      - ops
      - report
    file_count_threshold: 5         # 超过 5 文件强制 branch
  auto_merge:
    enabled: true
    strategy: "squash"
    require_auto_check: true
    require_tests: true
    require_review: false           # 默认不要求 Layer 2
    max_rebase_attempts: 1
  cleanup:
    ttl_hours: 72
    keep_failed_hours: 168
    prefix_whitelist: ["ap/"]       # 只清理 ap/ 前缀
```

### 新增/修改脚本

| 脚本 | 变更 | 行数估计 |
|------|------|----------|
| `branch-manager.sh`（新增） | ensure/mark-ready/auto-merge/cleanup | ~300 |
| `tmux-send.sh`（修改） | 加 --branch-mode/--task-type 参数 | +50 |
| `watchdog.sh`（修改） | branch 维度 HEAD 追踪 + auto-merge 调用 | +80 |
| `task-queue.sh`（修改） | branch metadata 字段 | +30 |

### 分阶段实施

**Phase 1（2 天）**：branch-manager.sh ensure + tmux-send.sh 支持 → 任务可在 branch 执行
**Phase 2（2 天）**：auto-merge 闭环 + watchdog 集成 → 自动合并通过的 branch
**Phase 3（1 天）**：cleanup + 熔断 + 全链路状态观测

---

## 两项改进的联动关系

```
                    ┌─────────────────────┐
                    │  task-queue.sh      │
                    │  (统一任务入口)      │
                    └──────┬──────────────┘
                           │
                    ┌──────▼──────────────┐
                    │ branch-manager.sh   │
                    │ (分支隔离)           │
                    └──────┬──────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         dev 任务      test 任务    review_fix
         (feature)    (test-agent)  (Layer 2)
              │            │            │
              ▼            ▼            ▼
         Codex 开发    Codex 写测试  Codex 修复
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────▼──────────────┐
                    │ auto-check + test   │
                    │ + quality gate      │
                    └──────┬──────────────┘
                           │
                    ┌──────▼──────────────┐
                    │ auto-merge          │
                    │ (squash → main)     │
                    └─────────────────────┘
```

Test Agent 的测试任务 **天然走 branch 模式**，两项改进互相增强：
- Branch 隔离让测试任务安全执行（写坏了删分支就行）
- Test Agent 提供了 auto-merge 的"测试通过"门禁条件

### 建议实施顺序

1. **先做 Branch 隔离 Phase 1**（2 天）— 基础设施
2. **再做 Test Agent Phase 1**（3 天）— 利用 branch 隔离
3. **两者 Phase 2 并行推进**（2 天）— auto-merge + 质量门禁
4. **最后 Phase 3 治理层**（2 天）— cleanup + ratchet + 观测

**总计约 9 天工作量。**
