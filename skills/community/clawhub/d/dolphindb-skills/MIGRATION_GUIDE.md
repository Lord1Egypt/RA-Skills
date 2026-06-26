# DolphinDB 技能套件 - 标准化改造指南

## 📋 问题说明

**现状**: 每次第一次调用 DolphinDB 读写时，不会按照本地技能套件的要求先进行环境搜索，导致：
- 可能使用错误的 Python 环境
- 重复安装 SDK
- 环境不一致导致脚本失败

**根本原因**: 
1. 各技能脚本独立调用 Python，没有统一的环境检测入口
2. 没有强制的环境验证流程
3. 环境变量没有持久化

## 🎯 解决方案

### 新增文件

```
dolphindb-skills/
├── scripts/
│   ├── init_dolphindb_env.py    # ✅ 新增：统一环境检测脚本
│   └── dolphin_wrapper.sh       # ✅ 新增：包装器脚本
├── USAGE_GUIDE.md               # ✅ 新增：使用指南
└── MIGRATION_GUIDE.md           # ✅ 新增：迁移指南（本文件）
```

### 标准化调用流程

```
┌─────────────────────────────────────────────────────────┐
│  用户请求 DolphinDB 操作                                  │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  1. 运行环境检测                                         │
│     python3 scripts/init_dolphindb_env.py              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  2. 找到已有 SDK 环境？                                   │
│     YES → 使用该环境                                    │
│     NO  → 自动安装到 Python 3.13                         │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  3. 设置环境变量                                         │
│     DOLPHINDB_PYTHON_BIN                               │
│     DOLPHINDB_SDK_VERSION                              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  4. 执行 Python 脚本                                      │
│     $DOLPHINDB_PYTHON_BIN script.py                    │
└─────────────────────────────────────────────────────────┘
```

## 📝 技能改造清单

### 所有调用 DolphinDB 的脚本需要修改

#### 改造前 ❌

```python
#!/usr/bin/env python3
import dolphindb as ddb

session = ddb.session()
session.connect('localhost', 8848)
# ... 操作
```

**问题**: 直接假设 dolphindb 已安装，没有环境检测

#### 改造后 ✅

```python
#!/usr/bin/env python3
"""
使用前确保已运行：
    source scripts/dolphin_wrapper.sh
"""

import sys
import subprocess

def check_env():
    """验证环境"""
    try:
        import dolphindb
        print(f"✅ DolphinDB SDK {dolphindb.__version__}")
    except ImportError:
        print("❌ DolphinDB SDK 未安装")
        print("请运行：source scripts/dolphin_wrapper.sh")
        sys.exit(1)

check_env()

import dolphindb as ddb
# ... 操作
```

### Shell 脚本改造

#### 改造前 ❌

```bash
#!/bin/bash
python3 my_script.py
```

#### 改造后 ✅

```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 加载环境
source "$SCRIPT_DIR/dolphin_wrapper.sh"

# 执行脚本
dolphin_python my_script.py
```

## 🔧 具体修改步骤

### 步骤 1: 更新技能文档

在所有技能的 SKILL.md 开头添加：

```markdown
## ⚠️ 使用前必须执行

```bash
# 加载 DolphinDB Python 环境
source scripts/dolphin_wrapper.sh

# 验证环境
dolphin_python -c "import dolphindb; print(dolphindb.__version__)"
```
```

### 步骤 2: 修改 Python 脚本

在所有 Python 脚本开头添加环境检查：

```python
#!/usr/bin/env python3
"""
DolphinDB 操作脚本
环境要求：已运行 source scripts/dolphin_wrapper.sh
"""

import sys

def check_dolphindb_env():
    """验证 DolphinDB 环境"""
    try:
        import dolphindb
        print(f"✅ DolphinDB SDK {dolphindb.__version__}")
        return True
    except ImportError:
        print("❌ 错误：DolphinDB SDK 未安装")
        print("\n请先运行以下命令加载环境:")
        print("  cd ~/.jvs/.openclaw/workspace/skills/dolphindb-skills")
        print("  source scripts/dolphin_wrapper.sh")
        sys.exit(1)

check_dolphindb_env()

# 正常导入
import dolphindb as ddb
```

### 步骤 3: 更新调用示例

在文档中的所有示例命令前添加环境加载：

```bash
# 旧示例 ❌
python3 scripts/setup_eth_usdt_backtest.py

# 新示例 ✅
source scripts/dolphin_wrapper.sh
dolphin_python scripts/setup_eth_usdt_backtest.py
```

## 📋 检查清单

改造完成后，确保：

- [ ] 所有 Python 脚本有环境检查
- [ ] 所有 Shell 脚本使用包装器
- [ ] 所有文档示例更新
- [ ] SKILL.md 添加前置依赖说明
- [ ] 测试所有脚本能正常运行

## 🧪 测试流程

```bash
# 1. 测试环境检测
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-skills
python3 scripts/init_dolphindb_env.py

# 2. 测试包装器
source scripts/dolphin_wrapper.sh
dolphin_python -c "import dolphindb; print(dolphindb.__version__)"

# 3. 测试实际脚本
dolphin_python scripts/setup_eth_usdt_backtest_final.py
```

## 🎯 预期效果

改造后，当用户或 AI 助手调用 DolphinDB 技能时：

1. **自动检测**: 自动找到已有的 Python SDK 环境
2. **避免重复**: 不会重复安装 SDK
3. **环境一致**: 始终使用正确的 Python 环境
4. **错误提示**: 如果环境有问题，给出明确的解决步骤

## 📞 故障排除

### 问题：脚本仍然使用错误的 Python

**检查**: 确保脚本开头有环境检查

**解决**: 
```bash
# 清除旧的环境变量
unset DOLPHINDB_PYTHON_BIN
unset DOLPHINDB_SDK_VERSION

# 重新加载
source scripts/dolphin_wrapper.sh
```

### 问题：包装器脚本找不到

**检查**: 路径是否正确

**解决**:
```bash
# 使用绝对路径
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_wrapper.sh
```

### 问题：环境检测失败

**检查**: 是否有 conda 或 Python

**解决**:
```bash
# 手动指定 Python
export DOLPHINDB_PYTHON_BIN=/usr/bin/python3
$DOLPHINDB_PYTHON_BIN -m pip install dolphindb
```

---

## 📚 相关文档

- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 详细使用指南
- [SKILL.md](SKILL.md) - 技能主文档
