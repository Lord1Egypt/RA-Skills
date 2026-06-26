# DolphinDB 技能套件 - 完整标准化解决方案

## 📋 问题总结

### 原始问题

> 每次第一次要求调用 dolphindb 读写时，不会按照本地 dolphindb skills 套件的要求，先进行环境搜索，是否存在 python sdk，然后再后续操作

### 延伸问题

> 是否有考虑 dolphindb-docker, dolphindb-stream, dolphindb-basic 和 dolphindb-quant-finance 其它组件引用以及这些组件单独运行时，是否可以也强制运行 dolphin_wrapper.sh？

### 问题根源

1. **没有强制的环境检测流程** - 环境检测是可选的，不是强制的
2. **子技能独立运行时无法找到环境** - 使用相对路径，离开技能目录就失效
3. **环境变量不持久** - 每次都需要重新检测
4. **缺少统一的执行入口** - 各技能各自为政

## 🎯 完整解决方案

### 架构设计

```
                                    用户调用
                                       │
                                       ▼
                        ┌──────────────────────────┐
                        │  主技能 (dolphindb-skills) │
                        └───────────┬──────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
    │ dolphindb-    │       │ dolphindb-    │       │ dolphindb-    │
    │ basic         │       │ docker        │       │ streaming     │
    └───────────────┘       └───────────────┘       └───────────────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    │
                                    ▼
                        ┌──────────────────────────┐
                        │  统一环境检测层           │
                        │  - dolphin_global.sh     │
                        │  - init_dolphindb_env.py │
                        └──────────────────────────┘
                                    │
                                    ▼
                        ┌──────────────────────────┐
                        │  Python 环境              │
                        │  (已安装 dolphindb SDK)   │
                        └──────────────────────────┘
```

### 核心组件

#### 1. 环境检测脚本 (`init_dolphindb_env.py`)

**功能**:
- 搜索所有可能的 Python 环境
- 检查是否安装了 dolphindb SDK
- 找到后返回 Python 路径和 SDK 版本
- 未找到时提供自动安装选项

**使用**:
```bash
python3 scripts/init_dolphindb_env.py
python3 scripts/init_dolphindb_env.py --export  # 导出环境变量
```

#### 2. 全局包装器 (`dolphin_global.sh`)

**功能**:
- 可在任何位置调用（使用绝对路径）
- 自动调用环境检测
- 设置环境变量
- 提供 `dolphin_python` 命令

**使用**:
```bash
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh
dolphin_python script.py
```

#### 3. 本地包装器 (`dolphin_wrapper.sh`)

**功能**:
- 在技能目录内使用（使用相对路径）
- 自动调用环境检测
- 设置环境变量

**使用**:
```bash
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-skills
source scripts/dolphin_wrapper.sh
dolphin_python script.py
```

#### 4. 环境检查入口 (`check_env.sh`)

**功能**:
- 只提供环境状态检查
- 不加载环境变量
- 用于预检查场景

**使用**:
```bash
bash scripts/check_env.sh
```

### 文件结构

```
dolphindb-skills/
├── scripts/
│   ├── init_dolphindb_env.py    # ✅ 核心：环境检测
│   ├── dolphin_global.sh        # ✅ 核心：全局包装器
│   ├── dolphin_wrapper.sh       # ✅ 核心：本地包装器
│   ├── check_env.sh             # ✅ 环境检查入口
│   └── update_subskills.sh      # ✅ 批量更新脚本
├── SKILL.md                     # ✅ 已更新：添加强制流程
├── USAGE_GUIDE.md               # ✅ 新增：使用指南
├── MIGRATION_GUIDE.md           # ✅ 新增：迁移指南
├── README_STANDARDIZATION.md    # ✅ 新增：改造总结
├── SUBSKILLS_INTEGRATION.md     # ✅ 新增：子技能集成指南
├── COMPLETE_SOLUTION.md         # ✅ 新增：完整解决方案（本文件）
└── QUICK_REFERENCE.md           # ✅ 新增：快速参考卡
```

## 🚀 使用场景

### 场景 1: 主技能调用

```bash
# 用户调用主技能
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-skills
source scripts/dolphin_wrapper.sh
dolphin_python scripts/setup_eth_usdt_backtest.py
```

### 场景 2: 子技能单独运行

```bash
# 用户单独使用 dolphindb-basic
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-basic
source ../dolphindb-skills/scripts/dolphin_global.sh
dolphin_python -c "
import dolphindb as ddb
s = ddb.session()
s.connect('localhost', 8848)
print(s.run('select now()'))
"
```

### 场景 3: 子技能被引用

```python
# dolphindb-quant-finance 中的 Python 脚本
#!/usr/bin/env python3
"""
量化金融技能示例
"""

import sys

def check_env():
    try:
        import dolphindb
        print(f"✅ DolphinDB SDK {dolphindb.__version__}")
    except ImportError:
        print("❌ 请运行：source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh")
        sys.exit(1)

check_env()

# 正常操作
import dolphindb as ddb
# ...
```

### 场景 4: 在任何位置调用

```bash
# 用户在 /tmp 目录
cd /tmp

# 加载全局包装器
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh

# 执行任何 DolphinDB 操作
dolphin_python my_script.py
```

## 📊 强制流程

```
┌─────────────────────────────────────────────────────────┐
│  任何 DolphinDB 操作                                      │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  1. 是否已加载环境？                                     │
│     (检查 DOLPHINDB_PYTHON_BIN)                        │
└─────────────────┬───────────────────────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
        YES               NO
         │                 │
         │                 ▼
         │      ┌────────────────────────┐
         │      │ 2. 加载环境             │
         │      │ source dolphin_global.sh│
         │      └───────────┬────────────┘
         │                  │
         │                  ▼
         │      ┌────────────────────────┐
         │      │ 3. 环境检测成功？       │
         │      │ YES → 继续             │
         │      │ NO  → 安装/报错        │
         │      └───────────┬────────────┘
         │                  │
         ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│  4. 执行操作                                            │
│     dolphin_python script.py                            │
└─────────────────────────────────────────────────────────┘
```

## 📝 子技能更新清单

### 需要更新的技能

- [x] `dolphindb-basic` - 已更新 SKILL.md
- [ ] `dolphindb-docker` - 待更新
- [ ] `dolphindb-streaming` - 待更新
- [ ] `dolphindb-quant-finance` - 待更新

### 更新内容

每个子技能的 SKILL.md 开头添加：

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

## 🧪 测试验证

### 测试 1: 主技能

```bash
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-skills
source scripts/dolphin_wrapper.sh
dolphin_python -c "import dolphindb; print(dolphindb.__version__)"
```

### 测试 2: 子技能独立运行

```bash
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-basic
source ../dolphindb-skills/scripts/dolphin_global.sh
dolphin_python -c "import dolphindb; print('OK')"
```

### 测试 3: 任意位置调用

```bash
cd /tmp
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh
dolphin_python -c "import dolphindb; print('OK')"
```

### 测试 4: 环境未安装

```bash
unset DOLPHINDB_PYTHON_BIN
unset DOLPHINDB_SDK_VERSION
python3 ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/init_dolphindb_env.py
```

## 📞 文档索引

| 文档 | 用途 | 目标读者 |
|------|------|----------|
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 快速参考 | 所有用户 |
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | 详细使用指南 | 所有用户 |
| [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) | 迁移指南 | 技能开发者 |
| [SUBSKILLS_INTEGRATION.md](SUBSKILLS_INTEGRATION.md) | 子技能集成 | 技能开发者 |
| [COMPLETE_SOLUTION.md](COMPLETE_SOLUTION.md) | 完整方案 | 架构师/维护者 |
| [README_STANDARDIZATION.md](README_STANDARDIZATION.md) | 改造总结 | 所有读者 |

## 🎯 核心原则

1. **强制检测** - 所有 DolphinDB 操作前必须先检测环境
2. **全局可用** - 使用 `dolphin_global.sh` 可在任何位置调用
3. **自动安装** - 未找到 SDK 时自动安装
4. **明确提示** - 错误时有明确的解决步骤
5. **文档完善** - 有完整的使用和迁移指南

## 📊 效果对比

| 方面 | 改造前 | 改造后 |
|------|--------|--------|
| 环境检测 | 手动/可选 | ✅ **强制/自动** |
| 子技能独立运行 | ❌ 无法找到环境 | ✅ **全局包装器支持** |
| 环境一致性 | 不保证 | ✅ **始终一致** |
| 错误提示 | 不明确 | ✅ **明确的解决步骤** |
| 资源浪费 | 可能重复安装 | ✅ **复用已有环境** |
| 用户体验 | 需要手动处理 | ✅ **一键加载** |

## 🎉 总结

通过这次完整的标准化改造：

1. **强制流程** - 每次调用都必须先检测环境
2. **全局支持** - 子技能在任何位置都能独立运行
3. **自动检测** - 自动找到已有的 Python SDK 环境
4. **避免重复** - 不会重复安装 SDK
5. **明确提示** - 错误时有明确的解决步骤
6. **文档完善** - 有完整的使用和迁移指南

**核心原则**: 
> 先检测 → 再使用；有现成 → 不重装；有问题 → 明提示

---

**更新日期**: 2026-04-02  
**版本**: v1.0  
**维护者**: DolphinDB Skills Team
