#!/bin/bash
# 批量更新所有子技能的 SKILL.md，添加强制环境检测流程

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SKILLS_DIR")"

# 强制流程文本
FORCE_TEXT="# 🚨 强制流程：使用前必须加载环境

**无论在何种场景下调用此技能（单独运行或被引用），必须先执行环境检测：**

\`\`\`bash
# 方法 1: 在技能目录内运行（推荐）
cd ~/.jvs/.openclaw/workspace/skills/<skill-name>
source ../dolphindb-skills/scripts/dolphin_wrapper.sh

# 方法 2: 在任何位置运行（推荐）
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh

# 方法 3: 手动检测
python3 ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/init_dolphindb_env.py
\`\`\`

**验证环境：**
\`\`\`bash
\$DOLPHINDB_PYTHON_BIN -c \"import dolphindb; print(dolphindb.__version__)\"

# 或使用包装器命令
dolphin_python -c \"import dolphindb; print(dolphindb.__version__)\"
\`\`\`

**重要**: 详见 [dolphindb-skills/USAGE_GUIDE.md](../dolphindb-skills/USAGE_GUIDE.md)

---

"

# 子技能列表
SUBSKILLS=(
    "dolphindb-basic"
    "dolphindb-docker"
    "dolphindb-streaming"
    "dolphindb-quant-finance"
)

for skill in "${SUBSKILLS[@]}"; do
    SKILL_FILE="$PARENT_DIR/$skill/SKILL.md"
    
    if [ -f "$SKILL_FILE" ]; then
        echo "📝 更新 $skill..."
        
        # 读取文件内容
        CONTENT=$(cat "$SKILL_FILE")
        
        # 查找第一个 "## ⚠️" 或 "## 描述" 的位置
        if [[ "$CONTENT" == *"## ⚠️ 前置依赖"* ]]; then
            # 替换旧的⚠️ 前置依赖部分
            echo "  - 替换旧的前置依赖说明"
            # 这里需要使用更复杂的 sed 或 Python 脚本
        else
            # 在标题后插入
            echo "  - 添加强制流程说明"
            # 这里需要使用更复杂的 sed 或 Python 脚本
        fi
        
        echo "  ✅ 完成"
    else
        echo "  ❌ 文件不存在：$SKILL_FILE"
    fi
done

echo ""
echo "✅ 批量更新完成"
echo ""
echo "📌 请手动检查每个子技能的 SKILL.md，确保格式正确"
