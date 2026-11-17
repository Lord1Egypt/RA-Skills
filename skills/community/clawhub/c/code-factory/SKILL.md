---
name: code-factory
description: "自动生成完整项目结构(README+requirements+test+ASSET_MANIFEST)，运行测试验证后才交付"
allowed-tools:
  - read
  - write
  - edit
  - exec
  - apply_patch
---

# Code Factory — 代码交付工厂 Skill (v1.0)

> 将自然语言需求自动转化为可交付的完整项目资产。
>
> **架构**：分层模块化设计，状态机驱动 + 契约校验 + 事务保护 + 熔断容错。

## 触发方式

| 触发短语 | 动作 |
|---------|------|
| "生产一个项目" | 激活完整交付流程 |
| "交付一个项目" | 激活完整交付流程 |
| "帮我写一个完整的项目" | 激活完整交付流程 |
| "创建一个项目叫..." | 激活完整交付流程 |
| "给我写一个 [功能] 的工具" | 激活完整交付流程 |

## 自动触发条件

当检测到用户请求生成完整项目/工具/应用时自动激活。

---

## 架构概览

```
用户输入
  │
  ▼
┌──────────────────────────────────────────────┐
│  contracts/    数据契约层                     │
│  ├─ input_schema.py    → ProjectRequest      │
│  ├─ output_schema.py   → ProjectResult       │
│  ├─ step_context.py    → StepContext         │
│  ├─ step_outputs.py    → TypedDict 类型定义   │
│  ├─ asset_manifest_schema.py                 │
│  └─ exceptions.py      → 统一异常定义         │
└──────────────────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────────────────┐
│  layers/                     核心执行层         │
│  ├─ orchestrator.py           状态机编排引擎    │
│  ├─ step_registry.py          步骤注册表        │
│  ├─ step_handlers/            步骤处理器 (7个)  │
│  │   ├─ preflight_handler.py                   │
│  │   ├─ snapshot_handler.py                    │
│  │   ├─ spec_handler.py                        │
│  │   ├─ asset_handler.py                       │
│  │   ├─ verify_handler.py                      │
│  │   ├─ retry_handler.py                       │
│  │   └─ delivery_handler.py                    │
│  ├─ preflight.py              Phase 0 预检     │
│  ├─ spec_engine.py            Spec 推导引擎    │
│  ├─ asset_generator.py        资产生成器       │
│  ├─ verifier.py               自动验证器       │
│  ├─ retry_controller.py       智能重试控制器    │
│  └─ deliverer.py              交付组装器       │
│  Phase0 → Step1 → Step2 → ... → Step6          │
│  每步独立执行、独立失败、独立回滚               │
└─────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────┐
│  middlewares/ 横切中间件                         │
│  ├─ circuit_breaker.py      熔断器              │
│  ├─ transaction_manager.py  事务管理 (UoW)       │
│  ├─ anti_corruption.py      防腐层 (ACL)         │
│  ├─ pipeline_guard.py       管道守护者           │
│  ├─ saga_coordinator.py     Saga 补偿协调器      │
│  ├─ side_effect_log.py      副作用追踪器         │
│  └─ service_container.py    DI 容器              │
└─────────────────────────────────────────────────┘
```

---

## 执行流程

### Phase 0: Preflight — 环境预检
> 实现模块: `layers/preflight.py`

生成前先验证环境完整性，避免生成后跑不通：
1. 检查 Python 版本是否满足项目需求
2. 检查目标目录是否存在、可写
3. 检查必要依赖是否已安装
4. 检查磁盘空间是否充足（≥100MB）
5. 不通过则直接报告缺少什么，后续步骤全部 SKIPPED

### Step 1: 环境快照
> 实现模块: `layers/step_handlers/snapshot_handler.py`

结构化采集环境信息，经过 `anti_corruption.py` 校验后存入 `StepContext`。

### Step 2: Spec 推导与计划生成
> 实现模块: `layers/spec_engine.py`

根据用户需求推导内部规格（spec），输出格式受 `contracts/` Schema 约束：
1. **Spec 推导**：从用户需求中提取功能范围、输入输出、边界条件、验收标准
2. **验收标准格式**：每条用 Given/When/Then + P1/P2/P3 优先级标记
3. 用户完全无感知——不要求用户写任何 spec，AI 内部完成

### Step 3: 生成资产文件
> 实现模块: `layers/asset_generator.py` + `templates/`

所有文件写入通过 `TransactionManager` 暂存到 staging 区域：
- 验证全部通过 → `tx.commit()` 原子提交
- 任何步骤失败 → `tx.rollback()` 完整回滚

标准化项目结构：
```
project_assets/[project_name]/
├── src/                        # 源码目录
│   └── main.py                 # 主程序（<!-- HARD-GATE --> 标记）
├── tests/                      # 测试目录
│   └── test_main.py            # pytest 测试
├── docs/                       # 文档目录
│   └── README.md               # 使用说明/安装/依赖
├── requirements.txt            # 依赖清单
├── run.sh                      # 一键运行脚本
├── SKILL.md                     # AI 技能元数据头
├── ASSET_MANIFEST.md           # 人类可读版资源地图表
├── manifest.json               # 机器可读版资产清单
└── environment.toml             # 环境隔离配置
```

### Step 4: 自动验证（含依赖图谱检查）
> 实现模块: `layers/verifier.py`

1. **依赖影响预检**：分析模块间依赖，检查是否有循环引用
2. **HARD-GATE 强制门禁验证**：凡标记 `<!-- HARD-GATE -->` 的关键函数/API，必须通过独立验证
3. 运行 `pytest tests/ -v` → 确认全部测试通过
4. **输出结构化审查报告**（Risk Assessment → 逐个文件 → 缺失测试 → 建议）

### Step 5: 智能重试
> 实现模块: `layers/retry_controller.py`

受 `circuit_breaker.py` 熔断器保护：
- 第 1 次失败：自动分析错误→修改代码→重新验证
- 第 2 次失败：更换修复策略（缩小修改范围）→重新验证
- 第 3 次失败：记录结构化失败模式到 `learnings/failure_patterns.json` → 暂停并报告

### Step 6: 交付
> 实现模块: `layers/deliverer.py`

输出：
- 项目路径（绝对路径）
- README.md 内容预览
- ASSET_MANIFEST.md 资源地图摘要
- manifest.json 机器可读摘要
- 测试结果摘要

---

## 状态机定义

```
PENDING ──→ RUNNING ──→ SUCCESS
                    ├──→ FAILED ──→ (retry ≤ 3) ──→ RUNNING
                    │         └──→ (retry exhausted) ──→ 记录失败模式
                    ├──→ TIMED_OUT (单步骤 > 120s)
                    └──→ ROLLED_BACK (事务回滚)
PENDING ──→ SKIPPED (前置条件不满足，如 Phase 0 失败)
```

全局熔断规则 (`middlewares/circuit_breaker.py`)：
- 全局超时：600s
- 单步骤超时：120s
- 连续 3 次失败 → 熔断打开，拒绝后续请求

---

## 数据契约（见 `contracts/` 目录）

| 契约文件 | 约束内容 |
|:---------|:---------|
| `input_schema.py` | `ProjectRequest` — project_name 格式、description 长度、python_version 格式、安全上限 |
| `output_schema.py` | `ProjectResult`, `StepResult`, `StepStatus` — 统一成功/失败标准（六态转换） |
| `step_context.py` | `StepContext` — 步骤间唯一数据载体，线程安全，TypedDict 类型标注 |
| `step_outputs.py` | TypedDict 定义 — 7 个步骤的输出类型契约 |
| `asset_manifest_schema.py` | `AssetManifest` — 锁定 manifest.json 字段格式 |
| `exceptions.py` | 统一异常定义 — PreflightFailedError |

---

## 代码规范（强制）

1. **简洁优先**：10行能解决→不写20行
2. **单一职责**：每个函数≤30行，只做一件事
3. **命名清晰**：不用 x/tmp/data 等无意义变量名
4. **类型提示**：所有函数参数+返回值加 type hints
5. **错误处理**：不用 `pass` 或裸 `except`
6. **零硬编码**：魔法数字/路径/配置提取为常量或参数
7. **无调试print**：最终代码不含 `print`，用正式日志或异常
8. **HARD-GATE 强制门禁**：关键函数/API 入口前必须插入 `<!-- HARD-GATE -->` 注释标记
9. 每个公开函数≥1个测试用例
10. 必须包含边界条件测试（空列表/零值/文件不存在）

---

## 注意事项

- 所有文件使用 UTF-8 编码
- 如果用户指定了项目名以外的路径偏好，使用用户指定路径
- 不要修改项目目录以外的任何文件
- 如果用户只说了功能没给项目名，用功能名加小写下划线命名
- 技能自身的测试位于 `tests/` 目录，运行 `pytest tests/ -v`

---

## 运行技能自身测试

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## ✅ 自检清单

| 检查项 | 状态 | 说明 |
|--------|:----:|------|
| name 存在 | ✅ | code-factory |
| name = 目录名 | ✅ | vs code-factory |
| description 存在 | ✅ | 自动生成项目结构... |
| 触发方式清晰 | ✅ | 5 个触发短语表 |
| 有 H1 标题 | ✅ | # Code Factory |
| 分层架构 | ✅ | contracts + layers + step_handlers + middlewares + templates |
| 状态机驱动 | ✅ | PENDING→RUNNING→SUCCESS/FAILED/SKIPPED/ROLLED_BACK/TIMED_OUT 六态 |
| 事务保护 | ✅ | TransactionManager prepare→commit→rollback 原子三段式 |
| 熔断容错 | ✅ | CircuitBreaker CLOSED/OPEN/HALF_OPEN 三态 + 全局 600s / 步骤 120s |
| 契约校验 | ✅ | 防腐层 7 步 ACL 校验（含 Step6 出口校验） |
| 副作用追踪 | ✅ | SideEffectTracker 审计 + 补偿计划生成 + 幂等性检测 |
| 跨步骤补偿 | ✅ | SagaCoordinator 逆序补偿 + 精准文件清理 |
| 幂等性 | ✅ | AssetGenerator 内容比对，跳过相同文件 |
| 退避重试 | ✅ | RetryController 3 次重试 + 指数退避 (1s/2s/4s) |
| 零外部 API 依赖 | ✅ | 纯本地生成 |
| 验证机制 | ✅ | Phase 0 预检 + Step 4 验证 + Step 5 智能重试 |
| 双格式输出 | ✅ | ASSET_MANIFEST.md（人类）+ manifest.json（机器） |
| 标准化结构 | ✅ | src/tests/docs 三级目录 |
| 失败闭环 | ✅ | `learnings/failure_patterns.json` 结构化记录 + 原子写入 |
| Spec 驱动 | ✅ | 内部 spec→plan→tasks 三段式 |
| 依赖预检 | ✅ | 依赖图谱 + HARD-GATE 验证 |
| 环境隔离 | ✅ | environment.toml + venv |
| 技能元数据 | ✅ | 自动生成标准 SKILL.md 头部 |
| 审查报告 | ✅ | 结构化输出 Risk→Files→Tests→Suggestions |
| 可测试 | ✅ | `tests/` 17 个测试文件 + 174 测试用例 |

## Agent 执行指令

### 职责边界
| 操作 | 执行方式 | 说明 |
|------|---------|------|
| 项目初始化 | Agent LLM | 创建项目目录结构 |
| Spec推导 | Agent LLM | 从需求推导内部规格 |
| 资产文件生成 | Agent LLM | 生成 src/tests/docs 等文件 |
| 自动验证 | exec脚本 | pytest tests/ -v |
| 依赖安装 | exec脚本 | pip install -e . |
| 重试修复 | Agent LLM + exec | 分析错误->修改代码->重测 |
| 交付 | write文件 | 写入最终交付物 |

### 标准工作流
1. 接收任务描述 -> 创建项目目录
2. Agent 执行 Spec 推导
3. Agent 生成代码文件
4. 安装依赖: pip install -e .
5. 运行测试: pytest tests/ -v
6. GREEN -> 交付; RED -> 分析报告->修复->重测(最多3轮)
7. 写入交付物

### 错误恢复
- pip失败 -> 检查 requirements.txt 格式
- pytest失败 -> 读取错误信息，定位失败用例
- 3轮重试仍失败 -> 记录失败模式，暂停报告
