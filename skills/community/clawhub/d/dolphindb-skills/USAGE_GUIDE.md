# DolphinDB 技能调用规范

## 🚨 强制流程：每次调用 DolphinDB 技能前必须执行

**所有 DolphinDB 相关技能调用时，必须遵循以下流程：**

```
1. 环境检测 → 2. 加载环境 → 3. 验证 SDK → 4. 执行操作
```

### 第一步：环境检测（必须）

```bash
# 方法 1: 使用包装器脚本（推荐）
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-skills
source scripts/dolphin_wrapper.sh

# 方法 2: 手动检测
python3 scripts/init_dolphindb_env.py --export
```

### 第二步：验证环境

```bash
# 验证 SDK 已安装
$DOLPHINDB_PYTHON_BIN -c "import dolphindb; print(dolphindb.__version__)"

# 或
dolphin_python -c "import dolphindb; print(dolphindb.__version__)"
```

### 第三步：执行 Python 脚本

```bash
# 使用包装器
dolphin_python your_script.py

# 或直接使用检测到的 Python
$DOLPHINDB_PYTHON_BIN your_script.py
```

---

## 📋 Python 脚本标准模板

所有 DolphinDB Python 脚本应遵循以下模板：

```python
#!/usr/bin/env python3
"""
DolphinDB 操作脚本

使用前确保已运行：
    source scripts/dolphin_wrapper.sh
"""

import dolphindb as ddb

# 1. 建立连接
session = ddb.session()
session.connect(
    host='localhost', 
    port=8848, 
    userid='admin', 
    password='123456'
)
print("✅ Connected to DolphinDB")

try:
    # 2. 执行数据库操作
    result = session.run('''
        // 你的 DolphinDB 脚本
        select * from kline_1d limit 10
    ''')
    
    # 3. 处理结果
    print(result.toDF())
    
finally:
    # 4. 关闭连接
    session.close()
    print("✅ Disconnected")
```

---

## 🔧 环境变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DOLPHINDB_PYTHON_BIN` | DolphinDB SDK 所在的 Python 路径 | `/Users/mac/anaconda3/bin/python` |
| `DOLPHINDB_SDK_VERSION` | 安装的 SDK 版本 | `3.0.4.2` |
| `DOLPHINDB_ENV_PATH` | Python 环境所在路径 | `/Users/mac/anaconda3` |

---

## 🚀 常用命令

### 环境管理
```bash
# 检测环境
python3 scripts/init_dolphindb_env.py

# 导出环境变量
python3 scripts/init_dolphindb_env.py --export

# 强制重新检测（不清除缓存）
python3 scripts/init_dolphindb_env.py --force
```

### 执行脚本
```bash
# 使用包装器（自动检测环境）
source scripts/dolphin_wrapper.sh
dolphin_python your_script.py

# 或直接使用环境变量
$DOLPHINDB_PYTHON_BIN your_script.py
```

### 安装包
```bash
# 使用包装器
dolphin_pip install some_package

# 或直接使用
$DOLPHINDB_PYTHON_BIN -m pip install some_package
```

---

## ⚠️ 常见错误及解决方案

### 错误 1: `ModuleNotFoundError: No module named 'dolphindb'`

**原因**: 当前 Python 环境没有安装 DolphinDB SDK

**解决**:
```bash
# 运行环境检测
python3 scripts/init_dolphindb_env.py

# 或手动安装
$DOLPHINDB_PYTHON_BIN -m pip install dolphindb
```

### 错误 2: `DOLPHINDB_PYTHON_BIN: command not found`

**原因**: 环境变量未设置

**解决**:
```bash
# 加载环境
source scripts/dolphin_wrapper.sh

# 或手动设置
eval $(python3 scripts/init_dolphindb_env.py --export)
```

### 错误 3: 连接失败 `Connection refused`

**原因**: DolphinDB 服务器未启动

**解决**:
```bash
# 检查 Docker 容器
docker ps | grep dolphindb

# 启动容器
docker start dolphindb

# 检查端口
lsof -i :8848
```

---

## 📁 技能目录结构

```
dolphindb-skills/
├── SKILL.md                 # 主技能文档
├── USAGE_GUIDE.md          # 使用指南（本文件）
├── scripts/
│   ├── init_dolphindb_env.py    # 环境检测脚本
│   ├── dolphin_wrapper.sh       # 包装器脚本
│   ├── detect_dolphindb_env.sh  # 旧版检测脚本（兼容）
│   ├── find_dolphindb_env.sh    # 旧版查找脚本（兼容）
│   └── load_dolphindb_env.sh    # 旧版加载脚本（兼容）
└── ...
```

---

## 🎯 最佳实践

### 1. 始终使用包装器

```bash
# ✅ 推荐
source scripts/dolphin_wrapper.sh
dolphin_python script.py

# ❌ 不推荐（可能使用错误的环境）
python3 script.py
```

### 2. 在脚本开头验证环境

```python
#!/usr/bin/env python3
import sys
import subprocess

def check_dolphindb():
    """验证 dolphindb 已安装"""
    try:
        import dolphindb
        print(f"✅ DolphinDB SDK {dolphindb.__version__}")
        return True
    except ImportError:
        print("❌ DolphinDB SDK 未安装")
        print("请运行：source scripts/dolphin_wrapper.sh")
        sys.exit(1)

check_dolphindb()
```

### 3. 会话管理

```python
# 使用上下文管理器
from contextlib import contextmanager

@contextmanager
def dolphindb_session():
    session = ddb.session()
    try:
        session.connect(host='localhost', port=8848)
        yield session
    finally:
        session.close()

# 使用
with dolphindb_session() as s:
    result = s.run("select * from kline_1d")
```

---

## 📞 技术支持

遇到问题时：

1. 检查环境：`python3 scripts/init_dolphindb_env.py`
2. 查看日志：检查脚本输出
3. 验证连接：`dolphin_python -c "import dolphindb; ddb.session().connect('localhost', 8848)"`
