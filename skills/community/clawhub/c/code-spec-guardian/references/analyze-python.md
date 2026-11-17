# Python 规范分析指引 | Python Analyzer

> 覆盖 Python 项目的语言特有规范。PSF 风格 + 项目约定并重。

## 分析流程

1. 读 `references/analyze-code-style.md` 中的通用部分
2. 用 `read` 读 `pyproject.toml` / `setup.cfg` / `requirements.txt`（或从 `project_context.json` → `configs` 中获取片段）
3. 追加写入 `.code-spec/python-style.md`（Python 特有条目，不要写入 code-style.md）

## Python 特有分析维度

### 命名

- **snake_case** 变量/函数/模块（PEP8 强制？看 ruff/flake8 配置确认）
- **PascalCase** 类名
- **UPPER_CASE** 常量
- **`_prefix`** 私有/内部（单下划线 vs 双下划线 `__`）
- **魔术方法** `__init__` / `__str__` / `__repr__` / `__len__` 等使用情况

### 类型注解

- 是否使用类型提示（PEP 484）
- 来源：pyproject.toml 中的 `[tool.mypy]` 或 `[tool.pyright]` 配置
- `--strict` 模式？
- 常用类型：Optional / Union / List / Dict vs list / dict 新语法
- `from __future__ import annotations` 使用

### 导入规范

- `import` 顺序：标准库 → 第三方 → 本地（PEP8）
- 是否使用 `isort`（pyproject.toml 中 `[tool.isort]`）
- `from x import y` vs `import x`
- `import *` 是否禁止

### 代码风格

- **缩进**：4 空格（PEP8）
- **行长**：79 / 88 / 120？（black 默认 88，flake8 默认 79）
- **引号**：单引号还是双引号？black 默认双引号
- **空行**：顶层 2 空行，方法间 1 空行（PEP8）
- **docstring**：Google / NumPy / reStructuredText 风格？
- **f-string** vs `.format()` vs `%` 使用比例

### 工具链

- **Linter**：ruff / flake8 / pylint / mypy
- **Formatter**：black / isort / autopep8 / yapf
- **来源**：`pyproject.toml` 中的 `[tool.ruff]` / `[tool.black]` / `[tool.isort]`
- **pre-commit** 配置（`.pre-commit-config.yaml`）

### 包/模块结构

- `__init__.py` 使用：空 vs 重导出
- `if __name__ == "__main__"` 使用
- `setup.py` vs `pyproject.toml` 打包方式
- 虚拟环境管理：venv / poetry / pipenv / conda

### 错误处理

- try/except 粒度
- 自定义异常类的使用
- 是否用 `raise ... from ...` 链式异常

### 异步

- async/await 使用率
- asyncio 生态：FastAPI 项目应高
- 同步 vs 异步函数命名区分？

### 框架特定

- **Django**：settings 模块拆分、INSTALLED_APPS 组织、urls 模块化、middleware 使用
- **Flask**：blueprint 组织、app factory 模式、config 管理
- **FastAPI**：router 模块化、dependency injection、Pydantic models 组织

### 测试

- pytest 配置（`pyproject.toml` 中 `[tool.pytest.ini_options]`）
- 测试文件命名：`test_*.py` 还是 `*_test.py`
- fixture 使用模式
- 覆盖率配置

### 数据库（Django ORM / SQLAlchemy）

- Model 定义位置：`models.py` 集中 vs 分文件
- QuerySet / Manager 自定义
- migration 管理方式
