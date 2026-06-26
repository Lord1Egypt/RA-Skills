---
name: auto-conda-python-env
description: 自动为Python项目创建或复用匹配的Conda环境，扫描项目依赖文件自动配置运行环境。Auto-create or reuse a Conda env for any Python project — scans deps, matches envs, handles CUDA/GPU needs.
triggers: 创建conda环境, 配置python环境, 新建虚拟环境, 初始化项目环境, python环境配置, create conda env, setup python env, new virtual environment, project environment
version: 1.1.0
metadata:
  openclaw:
    emoji: "🐍"
    requires:
      bins: ["python3", "pip"]
---

# Auto Conda Env for Python Project / 自动为Python项目配置Conda环境

## 触发条件 / When to Use
当用户需要为Python项目配置独立运行环境、自动创建Conda环境，或希望复用已有的匹配环境时，使用本技能。
Use when: setting up an isolated Python env, creating a new Conda env, or reusing an existing one for a project.

---

## 执行步骤 / Execution Steps

### 1. 获取项目路径 / Get Project Path
- 询问用户提供Python项目文件夹路径，若未指定则默认使用当前工作目录。
  Ask for the project folder path; default to current working directory if not provided.
- 验证路径是否存在且为有效文件夹。
  Verify the path exists and is a valid directory.

### 2. 扫描项目依赖文件 / Scan Dependency Files
进入项目文件夹，按以下优先级扫描：Scan in this order:

| 优先级 / Priority | 文件 / File | 提取内容 / What to Extract |
|---|---|---|
| 1 | `environment.yml` / `environment.yaml` | Python版本 + 所有依赖 / Python version + all deps |
| 2 | `pyproject.toml` | `project.requires-python` + `project.dependencies` |
| 3 | `requirements.txt` | 依赖包列表（检查 `.python-version` 获取版本）|
| 4 | `setup.py` | `python_requires` + `install_requires` |
| 5 | `Pipfile` | `[packages]` 节 |
| 6 | `setup.cfg` | `install_requires` |

- 若未找到任何依赖配置文件，默认使用 **Python 3.10**，无额外依赖。
  Default to Python 3.10 with no extra packages if nothing found.

### 3. 查找 conda 可执行文件 / Find Conda Executable
`conda` 可能不在 PATH 中，按以下顺序尝试：Try these paths if conda is not in PATH:

```bash
which conda
~/.local/bin/conda                                  # pip-installed conda
~/miniconda3/bin/conda                              # standard Miniconda
~/anaconda3/bin/conda                               # standard Anaconda
$HOME/miniconda3/bin/conda
$HOME/anaconda3/bin/conda
```

保存找到的 conda 路径为 `CONDA`，后续所有 conda 命令用 `CONDA` 前缀执行。
Save the working conda path as `CONDA`; prefix all conda commands with it.

### 4. 检查现有Conda环境 / Check Existing Environments
- 执行 `CONDA info --envs` 获取环境列表。
- 对每个环境验证：
  1. `CONDA run -n <env> which python` — 确认 python 存在（避免 ghost env）
  2. `CONDA run -n <env> python --version` — 验证 Python 版本
  3. `CONDA run -n <env> pip list` — 验证依赖已安装

> ⚠️ 部分 conda 环境 python 不在 PATH（如损坏/空环境），`conda run` 会失败，此时跳过该环境。
> Some envs fail `conda run` — skip them.

若找到完全匹配的环境 → 复用。
若未找到 → 进入步骤 5 创建。

### 5. 复用或创建环境 / Reuse or Create

**复用 / Reuse：**
- 确认环境 python 可执行且版本匹配
- 验证核心依赖已安装
- 配置 OpenClaw 后续操作使用此环境

**创建新环境 / Create New：**
1. **生成环境名**：`项目文件夹名` → 小写 → 特殊字符替换为 `_` → 追加 `_env`
   例 / e.g.：`MyProject-2.0` → `myproject_2_0_env`

2. **创建环境**：
   ```bash
   CONDA create -n <env_name> python=<version> -y
   ```

3. **安装依赖 / Install Dependencies：**

   | 依赖文件 / File | 安装命令 / Command |
   |---|---|
   | `environment.yml` | `CONDA env update -n <env> -f environment.yml --prune` |
   | `pyproject.toml` | `CONDA run -n <env> pip install .` |
   | `requirements.txt` | `CONDA run -n <env> pip install -r requirements.txt` |
   | `setup.py` | `CONDA run -n <env> pip install .` |
   | `Pipfile` | `CONDA run -n <env> pip install pipenv && CONDA run -n <env> pipenv sync` |
   | 无配置文件 / None | 仅创建空环境 / create empty env only |

   > 💡 pip 安装失败时（如系统保护 `PEP 668`），追加 `--break-system-packages` 参数重试。
   > If pip refuses due to PEP 668, add `--break-system-packages`.

4. **GPU / CUDA 处理（如需要）/ Handle GPU / CUDA if needed：**
   - 检查项目是否 import torch / tensorflow 等
   - 若需要 GPU：`CONDA run -n <env> pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118`
   - 验证：`CONDA run -n <env> python -c "import torch; print(torch.cuda.is_available())"`

5. **验证环境可用 / Verify Env Works：**
   ```bash
   CONDA run -n <env> python -c "import numpy, scipy, sklearn; print('OK')"
   ```
   若失败，记录缺失的包并重新安装。

### 6. 输出结果 / Output Summary

最终告知用户：
```
环境名称 / Env name: <name>
Python 版本 / Python: <version>
已安装依赖 / Installed: <list>
环境路径 / Path: /path/to/env
激活命令 / Activate: conda activate <name>
```

---

## 注意事项 / Notes

- `conda` 不在 PATH 是常见问题，优先搜索常见安装路径
  Missing `conda` in PATH is common; search standard install locations first
- ghost 环境（python 不存在）用 `conda run ... which python` 排除
  Use `which python` via `conda run` to detect ghost/broken envs
- pip 安装失败先尝试加 `--break-system-packages`
  Try `--break-system-packages` when pip is blocked by OS package protection
- GPU 项目安装 torch 后务必验证 CUDA 可用
  Always verify CUDA availability after installing torch
- 不修改用户现有 conda 安装，只读和复用/创建新环境
  Read-only on existing installs; only create/reuse envs, don't modify base

---

## 适用场景 / Use Cases

- 新项目初始化 / New project setup
- 不同项目需要不同 Python 版本 / Projects needing different Python versions
- 有 CUDA 依赖的 ML/DL 项目 / ML/DL projects with CUDA dependencies
- 依赖冲突隔离 / Isolating dependency conflicts
- 团队环境标准化 / Team environment standardization
