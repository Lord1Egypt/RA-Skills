---
name: dolphindb-init
description: DolphinDB Python 环境初始化技能。自动检测并切换到已安装 DolphinDB SDK 的 Python 环境（含 Anaconda/Miniconda/系统 Python），若未找到则自动安装。**这是 DolphinDB 套件的前置依赖，所有 DolphinDB 相关操作必须首先执行此技能**。
---

# DolphinDB 初始化技能

## 🎯 套件角色

**这是 DolphinDB Skill 套件的前置依赖技能。**

所有 DolphinDB 相关技能在执行前都必须先调用此技能：

```
任何 DolphinDB 请求
    ↓
[必须] dolphindb-init ← 你在这里
    ↓
环境检测 ✓
    ↓
调用功能技能
    ├─ dolphindb-core（连接、读写）
    └─ dolphindb-query（查询、分析）
```

## 触发条件

**任何时候** 用户提到 DolphinDB 并需要操作：

- "连接 DolphinDB"
- "查询 DolphinDB 数据"
- "在 DolphinDB 中建表"
- "DolphinDB 性能分析"
- 任何 DolphinDB Python SDK 相关操作

## 核心流程

### 1. 环境检测（必须第一步）

```bash
# 加载环境检测器
source ~/.openclaw/skills/dolphindb-init/scripts/load_dolphindb_env.sh

# 查看环境信息
dolphin_env_info

# 使用统一的 Python 调用函数
dolphin_python your_script.py
```

### 2. 检测逻辑

检测脚本按以下顺序扫描：

1. **conda 环境列表** → 检查每个环境的 `pip list`，查找 `dolphindb`
2. **Anaconda/Miniconda 路径** → 检查 `$CONDA_BASE_1`, `$CONDA_BASE_2` 等
3. **系统 Python 环境** → 检查 `$SYS_PYTHON_1`, `$SYS_PYTHON_2` 等
4. **决策**：
   - 找到已安装 → 导出环境变量 `DOLPHINDB_PYTHON_BIN`
   - 未找到 → 自动安装到 Python 3.13 环境

### 3. 环境变量

加载后可用的环境变量：

```bash
$DOLPHINDB_PYTHON_BIN    # Python 二进制路径（统一调用入口）
$DOLPHINDB_SDK_VERSION   # DolphinDB SDK 版本
$DOLPHINDB_PYTHON_VER    # Python 版本
$DOLPHINDB_ENV_PATH      # 环境路径
```

### 4. 统一调用方式

```bash
# 运行 Python 脚本
dolphin_python script.py

# 安装包
dolphin_pip install package_name

# 直接使用环境变量
$DOLPHINDB_PYTHON_BIN script.py
```

## 示例：DolphinDB 连接

```python
import dolphindb as ddb

# 创建连接
s = ddb.session()
s.connect("localhost", 8848, "admin", "password")

# 执行查询
result = s.run("select * from trade where date=2024.01.01")
print(result)

# 关闭连接
s.close()
```

使用加载器运行：

```bash
source ~/.openclaw/skills/dolphindb-init/scripts/load_dolphindb_env.sh
dolphin_python connect_dolphindb.py
```

## 隐私保护

所有路径都用变量符号表示，不暴露具体系统地址：

| 变量名 | 含义 |
|--------|------|
| `$CONDA_BASE_1` | 第一个 anaconda/miniconda 路径 |
| `$CONDA_BASE_2` | 第二个 anaconda/miniconda 路径 |
| `$SYS_PYTHON_1` | 第一个系统 Python 路径 |
| `$PY13_CANDIDATE_1` | Python 3.13 候选路径 |

## 故障排除

### 问题 1: 找不到环境

```bash
# 手动运行检测脚本查看详细信息
bash ~/.openclaw/skills/dolphindb-init/scripts/detect_dolphindb_env.sh
```

### 问题 2: SDK 版本不兼容

```bash
dolphin_pip uninstall dolphindb
dolphin_pip install dolphindb==3.0.4.2
```

### 问题 3: Python 版本不是 3.13

```bash
# 检查当前环境
dolphin_env_info

# 强制安装到特定路径
~/anaconda3/bin/python -m pip install dolphindb
```

## 相关文件

- `scripts/detect_dolphindb_env.sh` - 核心检测脚本，输出可 eval 的 export
- `scripts/load_dolphindb_env.sh` - 环境加载器，提供统一调用函数
- `scripts/find_dolphindb_env.sh` - 详细检测脚本（带完整输出）

## 套件关系

- **本技能** - `dolphindb-init`（环境初始化，前置依赖）
- **核心操作** - `dolphindb-core`（连接、表操作、数据读写）
- **高级查询** - `dolphindb-query`（聚合、时间序列、数据分析）

## 注意事项

1. **必须优先检测** - 不要假设 Python 环境已就绪
2. **使用统一接口** - 始终通过 `dolphin_python` 或 `$DOLPHINDB_PYTHON_BIN` 调用
3. **版本兼容** - 优先使用 Python 3.13 环境
4. **环境隔离** - 不同终端可能使用不同环境，必须每次检测
5. **套件前置** - 所有 DolphinDB 技能依赖此技能，必须首先执行
