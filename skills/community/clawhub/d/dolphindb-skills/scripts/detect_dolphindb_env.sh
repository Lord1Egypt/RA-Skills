#!/bin/bash
# DolphinDB Python Environment Detector (Export Mode)
# 输出可直接 eval 的 export 语句

# 存储可用环境的变量
DOLPHINDB_PYTHON=""
DOLPHINDB_VERSION=""
PYTHON_VER=""
ENV_PATH=""

# 1. 扫描 conda 环境
if command -v conda &> /dev/null; then
    ENV_LIST=$(conda env list 2>/dev/null | grep -v "^#" | grep -v "^$" || true)
    while IFS= read -r line; do
        ENV_NAME=$(echo "$line" | awk '{print $1}')
        ENV_PATH=$(echo "$line" | awk '{print $NF}')
        
        if [ -d "$ENV_PATH" ] && [ -f "$ENV_PATH/bin/python" ]; then
            PYTHON_BIN="$ENV_PATH/bin/python"
            HAS_DOLPHIN=$("$PYTHON_BIN" -m pip list 2>/dev/null | grep -i "^dolphindb" || true)
            
            if [ -n "$HAS_DOLPHIN" ]; then
                DOLPHINDB_PYTHON="$PYTHON_BIN"
                DOLPHINDB_VERSION=$(echo "$HAS_DOLPHIN" | awk '{print $2}')
                PYTHON_VER=$("$PYTHON_BIN" --version 2>&1 | awk '{print $2}')
                ENV_PATH="$ENV_PATH"
                break
            fi
        fi
    done <<< "$ENV_LIST"
fi

# 2. 扫描 anaconda/miniconda 直接路径
if [ -z "$DOLPHINDB_PYTHON" ]; then
    CONDA_PATHS="$HOME/anaconda3 $HOME/miniconda3 /opt/anaconda3 /opt/miniconda3"
    
    for CONDA_BASE in $CONDA_PATHS; do
        if [ -d "$CONDA_BASE" ] && [ -f "$CONDA_BASE/bin/python" ]; then
            PYTHON_BIN="$CONDA_BASE/bin/python"
            PY_VERSION=$("$PYTHON_BIN" --version 2>&1 | awk '{print $2}')
            HAS_DOLPHIN=$("$PYTHON_BIN" -m pip list 2>/dev/null | grep -i "^dolphindb" || true)
            
            if [ -n "$HAS_DOLPHIN" ]; then
                DOLPHINDB_PYTHON="$PYTHON_BIN"
                DOLPHINDB_VERSION=$(echo "$HAS_DOLPHIN" | awk '{print $2}')
                PYTHON_VER="$PY_VERSION"
                ENV_PATH="$CONDA_BASE"
                break
            fi
        fi
    done
fi

# 3. 扫描系统 Python
if [ -z "$DOLPHINDB_PYTHON" ]; then
    SYS_PYTHONS="/usr/local/bin/python3 /usr/bin/python3"
    
    for PY_BIN in $SYS_PYTHONS; do
        if [ -x "$PY_BIN" ]; then
            PY_VERSION=$("$PY_BIN" --version 2>&1 | awk '{print $2}')
            HAS_DOLPHIN=$("$PY_BIN" -m pip list 2>/dev/null | grep -i "^dolphindb" || true)
            
            if [ -n "$HAS_DOLPHIN" ]; then
                DOLPHINDB_PYTHON="$PY_BIN"
                DOLPHINDB_VERSION=$(echo "$HAS_DOLPHIN" | awk '{print $2}')
                PYTHON_VER="$PY_VERSION"
                ENV_PATH="system"
                break
            fi
        fi
    done
fi

# 4. 决策：使用已有环境或安装
if [ -n "$DOLPHINDB_PYTHON" ]; then
    # 找到已有环境
    echo "export DOLPHINDB_PYTHON_BIN=\"$DOLPHINDB_PYTHON\""
    echo "export DOLPHINDB_SDK_VERSION=\"$DOLPHINDB_VERSION\""
    echo "export DOLPHINDB_PYTHON_VER=\"$PYTHON_VER\""
    echo "export DOLPHINDB_ENV_PATH=\"$ENV_PATH\""
else
    # 需要安装
    TARGET_PYTHON=""
    
    # 优先找 Python 3.13
    PY13_PATHS="$HOME/anaconda3/bin/python $HOME/miniconda3/bin/python"
    
    for PY_BIN in $PY13_PATHS; do
        if [ -x "$PY_BIN" ]; then
            PY_VER=$("$PY_BIN" --version 2>&1 | awk '{print $2}')
            if [[ "$PY_VER" == 3.13* ]]; then
                TARGET_PYTHON="$PY_BIN"
                break
            fi
        fi
    done
    
    # 如果没有 3.13，用系统 python3
    if [ -z "$TARGET_PYTHON" ]; then
        for PY_BIN in /usr/local/bin/python3 /usr/bin/python3; do
            if [ -x "$PY_BIN" ]; then
                TARGET_PYTHON="$PY_BIN"
                break
            fi
        done
    fi
    
    if [ -z "$TARGET_PYTHON" ]; then
        echo "echo \"❌ 未找到可用的 Python\"" >&2
        exit 1
    fi
    
    # 安装 dolphindb
    $TARGET_PYTHON -m pip install dolphindb --quiet 2>/dev/null
    
    DOLPHINDB_VERSION=$($TARGET_PYTHON -m pip list 2>/dev/null | grep -i "^dolphindb" | awk '{print $2}')
    PYTHON_VER=$($TARGET_PYTHON --version 2>&1 | awk '{print $2}')
    
    echo "export DOLPHINDB_PYTHON_BIN=\"$TARGET_PYTHON\""
    echo "export DOLPHINDB_SDK_VERSION=\"$DOLPHINDB_VERSION\""
    echo "export DOLPHINDB_PYTHON_VER=\"$PYTHON_VER\""
    echo "export DOLPHINDB_ENV_PATH=\"newly_installed\""
fi
