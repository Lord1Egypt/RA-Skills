#!/bin/bash
# DolphinDB Python Environment Detector (Privacy Mode)
# 使用变量符号表示环境路径，不暴露具体地址

set -e

echo "🔍 开始扫描 Python 环境..."
echo ""

# 存储可用环境的变量
ENV_VAR_NAME=""
DOLPHINDB_PYTHON=""
DOLPHINDB_VERSION=""
PYTHON_VER=""

# 1. 扫描 conda 环境
echo "├─ [扫描] conda 环境列表..."
if command -v conda &> /dev/null; then
    ENV_LIST=$(conda env list 2>/dev/null | grep -v "^#" | grep -v "^$" || true)
    while IFS= read -r line; do
        ENV_NAME=$(echo "$line" | awk '{print $1}')
        ENV_PATH=$(echo "$line" | awk '{print $NF}')
        
        if [ -d "$ENV_PATH" ] && [ -f "$ENV_PATH/bin/python" ]; then
            PYTHON_BIN="$ENV_PATH/bin/python"
            HAS_DOLPHIN=$("$PYTHON_BIN" -m pip list 2>/dev/null | grep -i "^dolphindb" || true)
            
            if [ -n "$HAS_DOLPHIN" ]; then
                ENV_VAR_NAME="CONDA_ENV_${ENV_NAME^^}"
                DOLPHINDB_PYTHON="$PYTHON_BIN"
                DOLPHINDB_VERSION=$(echo "$HAS_DOLPHIN" | awk '{print $2}')
                PYTHON_VER=$("$PYTHON_BIN" --version 2>&1 | awk '{print $2}')
                echo "│  ✅ [FOUND] 环境变量：\$$ENV_VAR_NAME"
                echo "│     路径：\$${ENV_VAR_NAME}_PATH"
                echo "│     Python: $PYTHON_VER"
                echo "│     DolphinDB SDK: $DOLPHINDB_VERSION"
                echo ""
                export "$ENV_VAR_NAME"="$ENV_PATH"
                export "${ENV_VAR_NAME}_PYTHON"="$PYTHON_BIN"
                break
            fi
        fi
    done <<< "$ENV_LIST"
fi

# 2. 扫描 anaconda/miniconda 直接路径（用变量表示）
if [ -z "$DOLPHINDB_PYTHON" ]; then
    echo "├─ [扫描] Anaconda/Miniconda 路径..."
    
    CONDA_PATHS="$HOME/anaconda3 $HOME/miniconda3 /opt/anaconda3 /opt/miniconda3"
    CONDA_VARS="CONDA_BASE_1 CONDA_BASE_2 CONDA_BASE_3 CONDA_BASE_4"
    
    i=1
    for CONDA_BASE in $CONDA_PATHS; do
        VAR_NAME="CONDA_BASE_$i"
        if [ -d "$CONDA_BASE" ] && [ -f "$CONDA_BASE/bin/python" ]; then
            PYTHON_BIN="$CONDA_BASE/bin/python"
            PY_VERSION=$("$PYTHON_BIN" --version 2>&1 | awk '{print $2}')
            HAS_DOLPHIN=$("$PYTHON_BIN" -m pip list 2>/dev/null | grep -i "^dolphindb" || true)
            
            echo "│  ├─ 检查：\$$VAR_NAME"
            
            if [ -n "$HAS_DOLPHIN" ]; then
                ENV_VAR_NAME="$VAR_NAME"
                DOLPHINDB_PYTHON="$PYTHON_BIN"
                DOLPHINDB_VERSION=$(echo "$HAS_DOLPHIN" | awk '{print $2}')
                PYTHON_VER="$PY_VERSION"
                echo "│  ✅ [FOUND] 环境变量：\$$ENV_VAR_NAME"
                echo "│     路径：\$${ENV_VAR_NAME}"
                echo "│     Python: $PYTHON_VER"
                echo "│     DolphinDB SDK: $DOLPHINDB_VERSION"
                echo ""
                export "$ENV_VAR_NAME"="$CONDA_BASE"
                export "${ENV_VAR_NAME}_PYTHON"="$PYTHON_BIN"
                break
            fi
        fi
        i=$((i + 1))
    done
fi

# 3. 扫描系统 Python（用变量表示）
if [ -z "$DOLPHINDB_PYTHON" ]; then
    echo "├─ [扫描] 系统 Python 环境..."
    
    SYS_PYTHONS="/usr/local/bin/python3 /usr/bin/python3 $HOME/.local/bin/python3"
    SYS_VARS="SYS_PYTHON_1 SYS_PYTHON_2 SYS_PYTHON_3"
    
    i=1
    for PY_BIN in $SYS_PYTHONS; do
        VAR_NAME="SYS_PYTHON_$i"
        if [ -x "$PY_BIN" ]; then
            PY_VERSION=$("$PY_BIN" --version 2>&1 | awk '{print $2}')
            HAS_DOLPHIN=$("$PY_BIN" -m pip list 2>/dev/null | grep -i "^dolphindb" || true)
            
            echo "│  ├─ 检查：\$$VAR_NAME ($PY_VERSION)"
            
            if [ -n "$HAS_DOLPHIN" ]; then
                ENV_VAR_NAME="$VAR_NAME"
                DOLPHINDB_PYTHON="$PY_BIN"
                DOLPHINDB_VERSION=$(echo "$HAS_DOLPHIN" | awk '{print $2}')
                PYTHON_VER="$PY_VERSION"
                echo "│  ✅ [FOUND] 环境变量：\$$ENV_VAR_NAME"
                echo "│     DolphinDB SDK: $DOLPHINDB_VERSION"
                echo ""
                export "$ENV_VAR_NAME"="$PY_BIN"
                break
            fi
        fi
        i=$((i + 1))
    done
fi

# 4. 决策：使用已有环境或安装
echo "└─ [决策] ..."

if [ -n "$DOLPHINDB_PYTHON" ]; then
    echo "   ✅ 找到可用环境"
    echo "   环境变量：\$$ENV_VAR_NAME"
    echo "   Python 版本：$PYTHON_VER"
    echo "   DolphinDB SDK: $DOLPHINDB_VERSION"
    echo ""
    echo "💡 后续使用方式:"
    echo "   # 激活环境变量"
    echo "   source <(echo \"export ACTIVE_DOLPHINDB_ENV=\$$ENV_VAR_NAME\")"
    echo "   "
    echo "   # 调用 Python"
    echo "   \$${ENV_VAR_NAME}_PYTHON your_script.py"
    echo "   或"
    echo "   python=\$${ENV_VAR_NAME}_PYTHON && \$python your_script.py"
else
    echo "   ⚠️  未找到已安装 dolphindb 的环境"
    echo "   开始安装（优先 Python 3.13）..."
    
    TARGET_VAR=""
    TARGET_PYTHON=""
    
    # 优先找 Python 3.13
    PY13_PATHS="$HOME/anaconda3/bin/python $HOME/miniconda3/bin/python"
    PY13_VARS="PY13_CANDIDATE_1 PY13_CANDIDATE_2"
    
    i=1
    for PY_BIN in $PY13_PATHS; do
        VAR_NAME="PY13_CANDIDATE_$i"
        if [ -x "$PY_BIN" ]; then
            PY_VER=$("$PY_BIN" --version 2>&1 | awk '{print $2}')
            if [[ "$PY_VER" == 3.13* ]]; then
                TARGET_VAR="$VAR_NAME"
                TARGET_PYTHON="$PY_BIN"
                echo "   ✅ 找到 Python 3.13 候选：\$$VAR_NAME"
                break
            fi
        fi
        i=$((i + 1))
    done
    
    # 如果没有 3.13，用系统 python3
    if [ -z "$TARGET_PYTHON" ]; then
        FALLBACK_PATHS="/usr/local/bin/python3 /usr/bin/python3"
        FALLBACK_VARS="SYS_FALLBACK_1 SYS_FALLBACK_2"
        
        i=1
        for PY_BIN in $FALLBACK_PATHS; do
            VAR_NAME="SYS_FALLBACK_$i"
            if [ -x "$PY_BIN" ]; then
                TARGET_VAR="$VAR_NAME"
                TARGET_PYTHON="$PY_BIN"
                echo "   → 使用备选：\$$VAR_NAME"
                break
            fi
            i=$((i + 1))
        done
    fi
    
    if [ -z "$TARGET_PYTHON" ]; then
        echo "   ❌ 未找到可用的 Python"
        exit 1
    fi
    
    echo "   安装 dolphindb 到：\$$TARGET_VAR"
    $TARGET_PYTHON -m pip install dolphindb --quiet
    
    DOLPHINDB_VERSION=$($TARGET_PYTHON -m pip list 2>/dev/null | grep -i "^dolphindb" | awk '{print $2}')
    DOLPHINDB_PYTHON="$TARGET_PYTHON"
    ENV_VAR_NAME="$TARGET_VAR"
    
    export "$ENV_VAR_NAME"="$TARGET_PYTHON"
    
    echo "   ✅ 安装完成"
    echo "   环境变量：\$$ENV_VAR_NAME"
    echo "   DolphinDB SDK: $DOLPHINDB_VERSION"
fi

# 导出统一的环境变量供后续脚本使用
export DOLPHINDB_PYTHON_BIN="$DOLPHINDB_PYTHON"
export DOLPHINDB_SDK_VERSION="$DOLPHINDB_VERSION"

echo ""
echo "🎉 环境准备完成"
echo ""
echo "📌 统一调用方式:"
echo "   \$DOLPHINDB_PYTHON_BIN your_script.py"
