# DolphinDB 子技能集成指南

## 📋 问题说明

**用户需求**: 确保 `dolphindb-docker`、`dolphindb-streaming`、`dolphindb-basic`、`dolphindb-quant-finance` 等子技能在单独运行时也能强制执行环境检测流程。

**现状**:
- 子技能有独立 SKILL.md 文件
- 使用相对路径引用主技能的环境检测脚本
- 环境检测不是强制性的
- 独立运行时可能找不到环境检测脚本

## 🎯 解决方案

### 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **全局包装器** (`dolphin_global.sh`) | 可在任何位置调用，不依赖当前目录 | 需要知道绝对路径 | ✅ 推荐用于所有场景 |
| **相对路径包装器** (`dolphin_wrapper.sh`) | 技能目录内调用方便 | 只能在技能目录内使用 | 技能目录内使用 |
| **环境检查入口** (`check_env.sh`) | 提供明确的环境状态 | 只检查不加载 | 预检查场景 |

### 推荐方案：全局包装器

```bash
# 在任何位置都可以调用
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh
dolphin_python script.py
```

## 📁 新增文件

```
dolphindb-skills/
├── scripts/
│   ├── dolphin_global.sh      # ✅ 全局包装器（任何位置可用）
│   ├── dolphin_wrapper.sh     # ✅ 本地包装器（技能目录内使用）
│   ├── check_env.sh           # ✅ 环境检查入口
│   └── init_dolphindb_env.py  # ✅ 环境检测脚本
```

## 🔧 子技能改造清单

### 所有子技能需要更新

- [x] `dolphindb-basic` - 已更新 SKILL.md
- [ ] `dolphindb-docker` - 待更新
- [ ] `dolphindb-streaming` - 待更新
- [ ] `dolphindb-quant-finance` - 待更新

### 更新模板

在每个子技能的 SKILL.md 开头添加：

```markdown
## 🚨 强制流程：使用前必须加载环境

**无论在何种场景下调用此技能（单独运行或被引用），必须先执行环境检测：**

```bash
# 方法 1: 在技能目录内运行（推荐）
cd ~/.jvs/.openclaw/workspace/skills/<skill-name>
source ../dolphindb-skills/scripts/dolphin_wrapper.sh

# 方法 2: 在任何位置运行（推荐）
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh

# 方法 3: 手动检测
python3 ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/init_dolphindb_env.py
```

**验证环境：**
```bash
$DOLPHINDB_PYTHON_BIN -c "import dolphindb; print(dolphindb.__version__)"
```

**重要**: 详见 [dolphindb-skills/USAGE_GUIDE.md](../dolphindb-skills/USAGE_GUIDE.md)
```

## 🚀 使用场景

### 场景 1: 单独运行子技能

```bash
# 用户想单独使用 dolphindb-basic 技能
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-basic

# 加载环境（使用全局包装器）
source ../dolphindb-skills/scripts/dolphin_global.sh

# 执行操作
dolphin_python -c "
import dolphindb as ddb
s = ddb.session()
s.connect('localhost', 8848)
print(s.run('select now()'))
"
```

### 场景 2: 在脚本中引用

```python
#!/usr/bin/env python3
"""
dolphindb-basic 技能示例脚本
"""

import sys
import subprocess

def check_env():
    """验证环境"""
    try:
        import dolphindb
        print(f"✅ DolphinDB SDK {dolphindb.__version__}")
        return True
    except ImportError:
        print("❌ DolphinDB SDK 未安装")
        print("\n请先运行:")
        print("  source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh")
        sys.exit(1)

check_env()

# 正常操作
import dolphindb as ddb
# ...
```

### 场景 3: 在 CI/CD 中调用

```bash
#!/bin/bash
# CI/CD 脚本

# 加载 DolphinDB 环境
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh

# 验证环境
dolphin_python -c "import dolphindb; print(dolphindb.__version__)"

# 运行测试
dolphin_python tests/test_basic.py
```

## 📊 调用流程图

```
用户调用子技能
    │
    ▼
┌───────────────────────────────────┐
│ 是否已加载环境？                   │
│ (检查 DOLPHINDB_PYTHON_BIN)       │
└───────────┬───────────────────────┘
            │
    ┌───────┴───────┐
    │               │
   YES             NO
    │               │
    │               ▼
    │      ┌───────────────────────┐
    │      │ 运行环境检测           │
    │      │ dolphin_global.sh     │
    │      └───────────┬───────────┘
    │                  │
    │                  ▼
    │      ┌───────────────────────┐
    │      │ 找到 SDK?              │
    │      │ YES → 设置环境变量     │
    │      │ NO  → 自动安装         │
    │      └───────────┬───────────┘
    │                  │
    ▼                  ▼
┌───────────────────────────────────┐
│ 执行 Python 脚本                   │
│ dolphin_python script.py          │
└───────────────────────────────────┘
```

## 🧪 测试验证

### 测试 1: 全局包装器

```bash
# 在任意位置
cd /tmp
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh
dolphin_python -c "import dolphindb; print('OK')"
```

**预期**: 正常输出 "OK"

### 测试 2: 子技能独立运行

```bash
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-basic
source ../dolphindb-skills/scripts/dolphin_global.sh
dolphin_python -c "import dolphindb; print(dolphindb.__version__)"
```

**预期**: 输出 SDK 版本号

### 测试 3: 环境未安装

```bash
# 临时清除环境变量
unset DOLPHINDB_PYTHON_BIN
unset DOLPHINDB_SDK_VERSION

# 运行检测
python3 ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/init_dolphindb_env.py
```

**预期**: 自动安装或提示安装

## 📝 更新检查清单

更新所有子技能时，确保：

- [ ] SKILL.md 开头添加强制流程说明
- [ ] 所有示例使用 `dolphin_python` 而不是 `python3`
- [ ] 添加环境验证代码到 Python 脚本
- [ ] 更新引用路径为绝对路径或正确的相对路径
- [ ] 测试独立运行场景
- [ ] 测试被引用场景

## 🎯 最佳实践

### 1. 始终使用全局包装器

```bash
# ✅ 推荐：在任何位置都可用
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh

# ❌ 不推荐：依赖当前目录
source ./scripts/dolphin_wrapper.sh
```

### 2. 在脚本开头验证环境

```python
#!/usr/bin/env python3
import sys

try:
    import dolphindb
except ImportError:
    print("❌ 请先运行：source dolphin_global.sh")
    sys.exit(1)
```

### 3. 提供明确的错误提示

```bash
if ! command -v $DOLPHINDB_PYTHON_BIN &> /dev/null; then
    echo "❌ DolphinDB 环境未加载"
    echo "请运行：source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh"
    exit 1
fi
```

## 📞 相关文档

- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 详细使用指南
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - 迁移指南
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速参考卡

---

**更新日期**: 2026-04-02  
**版本**: v1.0
