# L1-BE测试方案生成提示词模板

> 执行子代理读取此模板生成L1后端测试方案

**适用规范：** 30-L1-BE测试方案规范.md
**适用Checklist：** 32-L1-BE测试方案审核Checklist.md
**生成时机：** BE-DEV任务单执行（pytest闭环内部）

---

## 任务说明

本模板用于指导执行子代理在BE-DEV任务单pytest闭环内部动态生成测试代码。

**核心设计**：L1测试不生成独立方案文档，测试代码在pytest闭环内部动态生成。

---

## 输入文档清单

| 输入文档 | 提取内容 | 用途 |
|---------|---------|------|
| API设计文档 | API方法清单、参数约束、错误响应 | 测试场景提取 |
| 系统功能设计文档 | 功能边界条件 | 边界场景提取 |
| 数据库设计文档 | 字段约束、外键关系 | 数据边界场景 |

---

## 测试代码生成要求

### 1. 测试文件命名

```
tests/backend/{module}/test_{功能名}.py
```

### 2. 测试代码结构

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class Test{APIName}:
    """{API名称}测试类"""
    
    def test_{method}_success(self):
        """正向场景：{场景描述}"""
        # 准备测试数据
        # 执行API调用
        # 验证响应
    
    def test_{method}_error_{error_type}(self):
        """异常场景：{场景描述}"""
        # 准置测试数据（触发错误）
        # 执行API调用
        # 验证错误响应
```

### 3. 场景覆盖规则

| 规则 | 说明 | 数量要求 |
|------|------|---------|
| 每个API方法≥1正向场景 | 成功路径测试 | 1+ |
| 每个参数边界≥1边界场景 | 参数验证测试 | 1+ |
| 每个错误响应≥1异常场景 | 错误处理测试 | 1+ |

### 4. 场景命名规范

```
test_{API方法}_{场景类型}_{描述}

场景类型：
  success   正向场景
  error     异常场景
  edge      边界场景
```

---

## pytest执行要求

### 命令

```bash
pytest tests/backend/{module}/test_{功能名}.py \
    --cov=backend/{module} \
    --cov-report=json \
    --cov-fail-under=80
```

### 验收标准

| 指标 | 阈值 | Guardian验证 |
|------|------|-------------|
| pytest通过率 | 100% | E4: pytest_passed=true |
| 代码覆盖率 | ≥80% | E5: coverage_percent≥80% |

---

## quality_check结构

```json
{
  "pytest_passed": true,
  "coverage_percent": 85,
  "ruff_errors": 0,
  "mypy_errors": 0,
  "radon_max_complexity": 8
}
```

---

## Checklist对照（确保生成代码能通过审核）

| 检查项 | 检查内容 | 生成要求 |
|--------|---------|---------|
| E11 | pytest通过率100% | 所有测试函数必须通过 |
| E12 | 覆盖率≥80% | 覆盖所有代码分支 |
| E13 | Ruff lint无Error | 代码符合lint规范 |
| E14 | mypy无Error | 类型注解完整 |

---

## 执行流程

```
Step1: 读取API设计文档 → 提取API方法和参数
Step2: 根据规则生成测试代码
Step3: 执行pytest + 覆盖率采集
Step4: 失败 → 检查lint → 修复 → pytest → 循环最多3次
Step5: 产出quality_check → Guardian验证
```

---

**模板版本：** v1.0
**创建时间：** 2026-04-15
**作者：** 皮皮虾 🦐