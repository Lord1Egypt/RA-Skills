# Python 工具栈集成方案

> AutoCraft 代码质量检测工具栈详细设计，与 FlowTicket 流程整合

**版本**: v2.0  
**日期**: 2026-04-15  
**编制**: 皮皮虾 🦐

---

## 一、工具栈定位

> **核心设计**：代码质量检查在执行子代理内部 pytest 闭环执行，Guardian 节点3只验证 quality_check 结果字段

| 工具 | 检查类型 | 集成位置 | 执行时机 | Guardian处理 |
|------|----------|----------|----------|-------------|
| **pytest-cov** | 测试覆盖率 | 执行子代理内部（pytest闭环）| 代码生成后立即执行 | 验证 quality_check.coverage_percent≥80% |
| **Ruff** | Lint + Format | 执行子代理内部（pytest闭环修复阶段）| pytest失败后修复阶段 | 验证 quality_check.ruff_errors=0 |
| **mypy** | 类型检查 | 执行子代理内部（pytest闭环修复阶段）| pytest失败后修复阶段（可选）| 验证 quality_check.mypy_errors=0（渐进）|
| **bandit** | 安全扫描 | **L2测试阶段** | BE-L2最后任务单 | 验证 bandit_high_issues=0 |

**精简效果**：7 个工具（pylint + flake8 + black + isort + mypy + bandit + pytest-cov） → 4 个工具

**层级划分说明**：
- **L1（pytest闭环内部）**：pytest-cov + Ruff + mypy
- **L2（集成测试阶段）**：bandit + 代码重复率 + 圈复杂度汇总

---

## 二、pytest-cov 详细方案

### 2.1 定位

**集成位置**: 执行子代理内部 pytest 闭环

**执行时机**: 代码生成后立即执行，在执行子代理内部完成

### 2.2 配置文件

**文件位置**: `backend/pyproject.toml`

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--tb=short",
    "--cov=app",
    "--cov-report=term-missing",
    "--cov-report=html:tests/reports/coverage",
    "--cov-fail-under=80",
]

[tool.coverage.run]
source = ["app"]
branch = true
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/config.py",
]

[tool.coverage.report]
fail_under = 80
show_missing = true
skip_covered = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

### 2.3 执行命令

```bash
# 基础执行（pytest 闭环内）
pytest --cov=app --cov-fail-under=80

# 详细报告（HTML）
pytest --cov=app --cov-report=html:tests/reports/coverage

# 仅覆盖率检查（不运行测试）
coverage report --fail-under=80
```

### 2.4 覆盖率阈值分级

| 任务类型 | 覆盖率阈值 | 说明 |
|----------|------------|------|
| **A类任务**（pytest闭环） | ≥ 80% | 代码生成任务强制达标 |
| **核心模块**（M-03 FlowTicket） | ≥ 90% | 关键业务逻辑提高要求 |
| **前端任务** | ≥ 70% | Vitest 覆盖率，阈值略低 |

### 2.5 pytest 闭环逻辑

> **pytest闭环详细流程**：见第六章6.1节

**闭环核心逻辑**：
```
Crush生成代码 → pytest执行（覆盖率）→ 
  【失败】进入修复阶段 → 循环最多3次 → 
    【超限】创建问题单
    【成功】产出quality_check
```

**产出字段**：pytest_passed、coverage_percent、report_path

### 2.6 覆盖率报告存储

| 报告类型 | 存储位置 | 用途 |
|----------|----------|------|
| HTML 报告 | `tests/reports/coverage/` | 可视化查看覆盖率详情 |
| XML 报告 | `tests/reports/coverage.xml` | CI/CD 集成（可选） |
| JSON 摘要 | `execution_logs.coverage_data` | 任务单记录 |

---

## 三、Ruff 详细方案

### 3.1 定位

**集成位置**: 执行子代理内部 pytest 闭环（修复阶段）

**执行时机**: pytest 失败后针对性修复阶段

> **Guardian 节点3职责**：验证 `quality_check.ruff_errors=0`，不执行 Ruff 检查

### 3.2 配置文件

**文件位置**: `backend/pyproject.toml`

```toml
[tool.ruff]
target-version = "py311"
line-length = 100
src = ["app"]

exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "tests/reports",
    "*.egg-info",
]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle 错误
    "F",      # Pyflakes
    "I",      # isort（导入排序）
    "N",      # pep8-naming（命名规范）
    "W",      # pycodestyle 警告
    "UP",     # pyupgrade（现代 Python 语法）
    "B",      # flake8-bugbear（常见 bug 模式）
    "C4",     # flake8-comprehensions（推导式优化）
    "SIM",    # flake8-simplify（简化建议）
    "DTZ",    # flake8-datetimez（时区安全）
    "RUF",    # Ruff 特有规则
]

ignore = [
    "E501",   # 行长度（由 formatter 处理）
    "N805",   # 类方法首参数命名（兼容 FastAPI）
    "B008",   # 函数默认参数（FastAPI Depends 使用）
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["DTZ001", "DTZ002"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

### 3.3 执行命令

```bash
# Lint 检查（仅检查，不修复）
ruff check app/ tests/

# Lint 检查 + 自动修复
ruff check app/ tests/ --fix

# Format 格式化（仅检查）
ruff format --check app/ tests/

# Format 格式化 + 自动修复
ruff format app/ tests/

# 输出 JSON（供 Guardian 解析）
ruff check app/ --output-format=json
```

### 3.4 阻断级别设计（pytest闭环内部）

| 问题级别 | Ruff 规则 | pytest闭环处理 | 说明 |
|----------|-----------|----------------|------|
| **Error** | E/F/B/RUF | **自动修复** | pytest闭环内针对性修复 |
| **Warning** | W/SIM/C4 | 仅提示 | 不阻断pytest闭环 |
| **Format** | format 检查 | **自动格式化** | 执行子代理内部自动处理 |

### 3.5 pytest闭环修复流程

```
执行子代理内部 pytest 闭环：
    │
    ├─ Crush生成代码
    │
    ├─ pytest执行
    │     ├─ pytest通过 → 继续
    │     └─ pytest失败 → 进入修复阶段
    │
    ├─ 修复阶段（针对性修复）：
    │     ├─ Ruff Lint检查 → 发现error → `ruff check --fix`自动修复
    │     ├─ Ruff Format → `ruff format`自动格式化
    │     ├─ 重新pytest → 循环最多3次
    │     └─ 超限 → 返回超限结果 → FlowTicket创建问题单
    │
    └─ pytest通过 → 产出quality_check字段
          ├─ ruff_errors: 0
          ├─ ruff_warnings: 2
          └─ format_fixed: true
```

> **Guardian节点3验证**：检查 `quality_check.ruff_errors=0`，不为0则返工节点2

### 3.6 工具替代对比

| 功能 | 原工具 | Ruff 替代 | 优势 |
|------|--------|-----------|------|
| 代码风格检查 | flake8 | Ruff lint (E/F) | 速度快 10-100 倍 |
| 导入排序 | isort | Ruff lint (I) | 无需单独配置 |
| 命名规范 | pep8-naming | Ruff lint (N) | 内置支持 |
| 格式化 | black | Ruff format | 配置一致 |
| Bug 模式检测 | flake8-bugbear | Ruff lint (B) | 内置支持 |

---

## 四、mypy 详细方案

### 4.1 定位

**集成位置**: 执行子代理内部 pytest 闭环（修复阶段，可选）

**执行时机**: pytest 失败后针对性修复阶段（渐进采用）

> **Guardian 节点3职责**：验证 `quality_check.mypy_errors=0`（核心模块渐进采用）

### 4.2 渐进采用策略

| 阶段 | 检查范围 | 严格程度 | 时间 |
|------|----------|----------|------|
| **阶段1** | 新模块 | 基础检查 | 立即 |
| **阶段2** | 核心模块（M-03/M-06） | 严格检查 | 2周后 |
| **阶段3** | 全项目 | 严格检查 | 项目成熟后 |

### 4.3 配置文件

**文件位置**: `backend/pyproject.toml`

```toml
[tool.mypy]
python_version = "3.11"

# 渐进采用（阶段1：宽松检查）
strict = false
warn_return_any = false
warn_unused_configs = true

# 阶段2 后启用（当前注释）
# strict = true
# warn_return_any = true
# disallow_untyped_defs = true

ignore_missing_imports = true

exclude = [
    "tests/",
    "venv/",
    ".venv/",
]

# 每模块配置（核心模块严格）
[[tool.mypy.overrides]]
module = "app.flowticket.*"
strict = true

[[tool.mypy.overrides]]
module = "app.guardian.*"
strict = true
```

### 4.4 执行命令

```bash
# 基础检查（渐进采用）
mypy app/

# 严格检查（核心模块）
mypy app/flowticket/ app/guardian/ --strict

# JSON 输出（供 Guardian 解析）
mypy app/ --output=json

# 仅检查错误（忽略警告）
mypy app/ --no-error-summary 2>&1 | grep "error:"
```

### 4.5 阈值设计（pytest闭环内部处理）

| 阶段 | 阈值 | pytest闭环处理 | Guardian验证 |
|------|------|----------------|-------------|
| **阶段1** | 仅提示 | 新模块类型错误提示，不阻断 | quality_check.mypy_errors记录（不验证）|
| **阶段2** | 核心模块 error=0 | 核心模块类型错误在pytest闭环内修复 | E7验证：mypy_errors=0（核心模块）|
| **阶段3** | 全项目 error=0 | 所有模块类型错误在pytest闭环内修复 | E7验证：mypy_errors=0 |

> **说明**：类型检查在pytest闭环修复阶段执行，Guardian节点3只验证结果字段

---

## 五、bandit 详细方案

### 5.1 定位

**集成位置**: **L2测试阶段**（BE-L2最后任务单）

**功能**: Python 安全扫描，检测常见安全漏洞

> **设计理由**：安全扫描适合在集成测试阶段执行，单任务pytest闭环不包含安全检查

### 5.2 检测内容

| 漏洞类型 | bandit ID | 说明 | 严重级别 |
|----------|-----------|------|----------|
| 硬编码密码 | B105/B106 | 密码、token 硬编码 | **High** |
| SQL 注入 | B608 | 字符串拼接 SQL | **High** |
| exec 使用 | B102 | 动态执行代码 | **Medium** |
| 弱加密 | B303 | MD5/SHA1 等 | **Medium** |
| 请求无验证 | B310 | urllib 无 SSL 验证 | **Medium** |
| YAML 加载 | B506 | yaml.load 不安全 | **Medium** |

### 5.3 配置文件

**文件位置**: `backend/.bandit.yaml`

```yaml
targets:
  - app

exclude_dirs:
  - tests
  - .venv
  - venv

skips:
  - B101  # assert 使用（测试允许）

severity_level: high
confidence_level: medium
```

### 5.4 执行命令

```bash
# 基础扫描
bandit -r app/

# 仅高危问题
bandit -r app/ -ll

# JSON 输出（供 Guardian 解析）
bandit -r app/ -f json

# 自定义配置
bandit -r app/ -c .bandit.yaml
```

### 5.5 阻断级别设计（L2测试阶段）

| 严重级别 | L2 Guardian处理 | 说明 |
|----------|-----------------|------|
| **High** | **Block** | L2最后任务单Guardian阻断，必须修复 |
| **Medium** | Warning | 提示但不阻断L2通过 |
| **Low** | Ignore | 不报告 |

> **执行时机**：BE-L2计划最后一个任务单（DOC-BE-L2-REPORT）的post_guardian检查

### 5.6 常见问题修复建议

| 漏洞 | 检测示例 | 修复建议 |
|------|----------|----------|
| 硬编码密码 | `password = "123456"` | 使用 `os.getenv("PASSWORD")` |
| SQL 注入 | `f"SELECT * FROM {table}"` | 使用参数化查询 |
| exec 使用 | `exec(user_input)` | 禁止动态执行，使用沙箱隔离 |
| 弱加密 | `hashlib.md5(data)` | 使用 `hashlib.sha256(data)` |
| YAML 加载 | `yaml.load(data)` | 使用 `yaml.safe_load(data)` |

---

## 六、执行流程整合

### 6.1 pytest闭环内部检查流程（节点2）

```
执行子代理内部 pytest 闭环：

1. Crush生成代码
   ↓
2. pytest执行（pytest-cov）
   ├── pytest通过 + coverage≥80% → 产出quality_check
   └── pytest失败 → 进入修复阶段
       ↓
3. 修复阶段（针对性修复）：
   ├── Ruff Lint检查 → `ruff check --fix`自动修复
   ├── Ruff Format → `ruff format`自动格式化
   ├── mypy类型检查（可选，核心模块）→针对性修复
   └── 重新pytest → 循环最多3次
       ├── 成功 → 产出quality_check
       └── 超限 → 返回超限结果 → FlowTicket创建问题单
```

### 6.2 Guardian节点3验证流程

> **Guardian节点3验证流程详见**：[项目整体测试方案.md](./项目整体测试方案.md) 第三章3.2节

**Python后端Guardian验证要点**：

| 检查项ID | 验证内容 | Python阈值 |
|---------|----------|-----------|
| E4 | pytest_passed=true | 无差异 |
| E5 | coverage_percent≥阈值 | **≥80%（后端）** |
| E6 | ruff_errors=0 | 无差异 |
| E7 | mypy_errors=0 | 可选，核心模块渐进 |

> **B类任务处理**：quality_check字段为null，跳过E4-E7

### 6.3 L2测试阶段bandit检查流程

```
BE-L2最后任务单（DOC-BE-L2-REPORT）post_guardian：

1. bandit安全扫描
   ├── 高危问题=0 → 继续
   └── 存在高危 → Block，返回修复

2. 代码重复率检测（可选）
   └── Warning级别，不阻断

3. 圈复杂度汇总（可选）
   └── Warning级别，不阻断

4. 全部通过 → BE-L2计划完成
```

---

## 七、FlowTicket 流程图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        FlowTicket 执行流程                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  节点1: Pre-Guardian（前置检查）                                         │
│  ├── 检查前置任务已完成                                                  │
│  ├── 检查测试文件存在                                                    │
│  └── 检查输入文档存在                                                    │
│                                                                         │
│           ↓                                                             │
│                                                                         │
│  节点2: 执行子代理（pytest 闭环）                                         │
│  ├── Crush 生成代码                                                      │
│  ├── pytest 执行（pytest-cov ≥ 80%）                                    │
│  │   ├── 成功 → 产出quality_check → 继续                                │
│  │   └── 失败 → 进入修复阶段                                             │
│  │       ├── Ruff Lint自动修复                                          │
│  │       ├── Ruff Format自动格式化                                       │
│  │       ├── mypy类型检查（可选）                                        │
│  │       └── 重新pytest → 循环最多3次                                    │
│  │           └── 超限 → 创建问题单 → 暂停                               │
│  └── 产出 execution_log.quality_check                                   │
│                                                                         │
│           ↓                                                             │
│                                                                         │
│  节点3: Guardian（结果验证）                                              │
│  ├── E1: 产出物文件存在                                                  │
│  ├── E2: 产出物文件非空                                                  │
│  ├── E3: execution_log格式正确                                          │
│  ├── E4: quality_check.pytest_passed=true                              │
│  ├── E5: quality_check.coverage_percent≥阈值                           │
│  ├── E6: quality_check.ruff_errors=0                                   │
│  ├── E7: quality_check.mypy_errors=0（可选）                            │
│  └── 不通过 → 返工节点2（上限2次）                                        │
│                                                                         │
│           ↓                                                             │
│                                                                         │
│  节点4: 验证子代理（业务逻辑验证）                                         │
│  ├── 检查功能正确性                                                      │
│  ├── 检查边界情况                                                        │
│  ├── 检查安全逻辑                                                        │
│  └── 返回结论（通过/不通过）                                              │
│                                                                         │
│           ↓                                                             │
│                                                                         │
│  节点5: Final-Guardian（最终检查）                                        │
│  ├── 检查验证子代理结论                                                   │
│  ├── 检查产出物完整                                                      │
│  └── 任务完成                                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        L2测试阶段补充流程                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  BE-L2最后任务单（DOC-BE-L2-REPORT）post_guardian：                      │
│  ├── bandit 安全扫描（高危阻断）                                          │
│  ├── 代码重复率检测（Warning）                                           │
│  ├── 圈复杂度汇总（Warning）                                              │
│  └── 全部通过 → BE-L2计划完成                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 八、数据库记录方案

### 8.1 execution_logs 表扩展

```sql
-- execution_logs 表新增字段
ALTER TABLE execution_logs ADD COLUMN coverage_percent INTEGER;
ALTER TABLE execution_logs ADD COLUMN coverage_report_path VARCHAR(500);
ALTER TABLE execution_logs ADD COLUMN ruff_errors INTEGER;
ALTER TABLE execution_logs ADD COLUMN ruff_warnings INTEGER;
ALTER TABLE execution_logs ADD COLUMN bandit_high INTEGER;
ALTER TABLE execution_logs ADD COLUMN bandit_medium INTEGER;
ALTER TABLE execution_logs ADD COLUMN mypy_errors INTEGER;
ALTER TABLE execution_logs ADD COLUMN mypy_warnings INTEGER;
```

### 8.2 质量检查记录 JSON

```json
// execution_logs.quality_data 字段示例
{
  "pytest": {
    "passed": true,
    "coverage": 85,
    "report_path": "tests/reports/coverage/index.html"
  },
  "ruff": {
    "lint_errors": 0,
    "lint_warnings": 2,
    "format_fixed": 5
  },
  "bandit": {
    "high_issues": 0,
    "medium_issues": 1
  },
  "mypy": {
    "errors": 0,
    "warnings": 3
  }
}
```

---

## 九、实施步骤

### 9.1 安装工具

```bash
pip install ruff pytest-cov mypy bandit
```

### 9.2 创建配置文件

```bash
cd /data/projects/autocraft/backend

# pyproject.toml 追加配置（pytest、coverage、ruff、mypy）

# 创建 bandit 配置
cat > .bandit.yaml << 'EOF'
targets:
  - app
exclude_dirs:
  - tests
  - .venv
skips:
  - B101
severity_level: high
confidence_level: medium
EOF
```

### 9.3 创建 Guardian 模块

```bash
mkdir -p autocraft/guardian
touch autocraft/guardian/code_quality.py
```

### 9.4 测试验证

```bash
# Ruff
ruff check app/ tests/
ruff format app/ tests/

# bandit
bandit -r app/ -ll

# mypy
mypy app/

# pytest-cov
pytest --cov=app --cov-fail-under=80
```

---

## 十、预期效果

| 维度 | 原方案 | 新方案 | 效果 |
|------|--------|--------|------|
| **工具数量** | 7 个 | 4 个 | 精简 43% |
| **Lint 速度** | pylint（慢） | Ruff | 提升 10-100 倍 |
| **覆盖率** | 无量化 | pytest-cov ≥ 80% | 强制达标 |
| **类型安全** | 无检查 | mypy 渐进 | 渐进采用 |
| **安全扫描** | 无检查 | bandit 高危阻断 | 安全保障 |

---

## 十一、参考资料

| 文档 | 位置 |
|------|------|
| 代码质量检测调研汇总 | `memory/research/汇总-代码质量检测与系统测试清单.md` |
| 任务单执行规范 | `docs/design/任务单执行规范.md` |
| B类任务验证设计 | `memory/research/b-class-task-validation-design.md` |

---

## 十二、版本历史

| 版本 | 日期 | 作者 | 变更说明 |
|------|------|------|----------|
| v1.0 | 2026-04-14 | 皮皮虾 🦐 | 初始版本 |
| **v2.0** | 2026-04-15 | 皮皮虾 🦐 | **架构修正**：①第一章工具栈定位改为pytest闭环内部执行；②第三章Ruff改为pytest闭环修复阶段；③第四章mypy改为pytest闭环修复阶段；④第五章bandit改为L2测试阶段；⑤第六章重写为执行流程整合（pytest闭环+Guardian验证+L2检查）；⑥删除旧Guardian检查函数代码；⑦第七章流程图更新为结果验证模式 |

---

_版本: v2.0_  
_编制: 皮皮虾 🦐_  
_日期: 2026-04-15_