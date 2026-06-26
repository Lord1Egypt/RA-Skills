#!/bin/bash
# 初始化脚本 - 安装后自动配置，替换原有 clawhub 安装方式
# 用法：./init.sh [AGENT_WORKSPACE]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(dirname "$SCRIPT_DIR")"
AGENT_WORKSPACE="${1:-/Users/xubangbang/.openclaw/workspace}"
MEMORY_FILE="${AGENT_WORKSPACE}/agents/MAIN/memory/$(date +%Y-%m-%d).md"
MEMORY_FILE_YESTERDAY="${AGENT_WORKSPACE}/agents/MAIN/memory/$(date -d 'yesterday' +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d 2>/dev/null || echo 'yesterday.md')"

echo "🚀 初始化 China Install Skills..."
echo ""

# 1. 检查是否已安装
if [ ! -f "${SKILLS_DIR}/SKILL.md" ]; then
  echo "❌ 错误：SKILL.md 不存在，技能未正确安装"
  exit 1
fi

echo "✅ 技能已安装：${SKILLS_DIR}"
echo ""

# 2. 配置 crontab 定时任务（可选，询问用户）
echo "⏰ 配置每周自动更新检查？"
echo "   时间：每周日 凌晨 3:00"
echo "   功能：自动检查技能更新"
echo ""
read -p "是否配置？(Y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [ -z "$REPLY" ]; then
  "${SCRIPT_DIR}/setup-cron.sh" "$AGENT_WORKSPACE"
else
  echo "⚠️  跳过 crontab 配置"
  echo "   需要时运行：./setup-cron.sh"
fi
echo ""

# 3. 写入 Memory（记录安装信息和使用方式）
echo "📝 记录到 Memory..."

# 创建 memory 目录
mkdir -p "$(dirname "$MEMORY_FILE")"

# 检查今天的 memory 文件是否存在
if [ ! -f "$MEMORY_FILE" ]; then
  # 尝试找昨天的
  if [ -f "$MEMORY_FILE_YESTERDAY" ]; then
    MEMORY_FILE="$MEMORY_FILE_YESTERDAY"
  fi
fi

# 写入安装记录
cat >> "$MEMORY_FILE" << 'EOF'

## 📦 China Install Skills 已安装

**安装时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**技能路径:** ${SKILLS_DIR}  
**版本:** v1.1.0+

### 使用方式

现在可以使用以下命令安装技能（绕过 clawhub.com 限流）：

```bash
cd ${SKILLS_DIR}/scripts

# 搜索技能
./search.sh <关键词>

# 一键安装（推荐）
./quick-install.sh <技能名> <目标目录>

# 或创建别名方便使用
alias cinstall='${SKILLS_DIR}/scripts/quick-install.sh'
```

### 示例

```bash
# 安装天气技能到 MAIN
./quick-install.sh weather /Users/xubangbang/.openclaw/workspace/agents/MAIN/skills

# 安装 GitHub 技能到 SKILL-01
./quick-install.sh github-cli /Users/xubangbang/.openclaw/workspace/agents/SKILL-01/skills
```

### 自动更新

已配置每周日 3:00 自动检查更新（如果选择了配置）。

---

EOF

# 替换变量
if [ -f "$MEMORY_FILE" ]; then
  sed -i.bak "s|\$(date '+%Y-%m-%d %H:%M:%S')|$(date '+%Y-%m-%d %H:%M:%S')|g" "$MEMORY_FILE"
  sed -i.bak "s|\${SKILLS_DIR}|${SKILLS_DIR}|g" "$MEMORY_FILE"
  rm -f "${MEMORY_FILE}.bak" 2>/dev/null || true
fi

echo "✅ 已记录到：$MEMORY_FILE"
echo ""

# 4. 创建便捷脚本（可选）
echo "🔧 创建便捷命令..."

BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

# 创建 cinstall 命令
cat > "$BIN_DIR/cinstall" << BINSCRIPT
#!/bin/bash
# China Install Skills - 快速安装命令
# 用法：cinstall <技能名> [目标目录]

SKILLS_DIR="${SKILLS_DIR}/scripts"

if [ -z "\$1" ]; then
  echo "用法：cinstall <技能名> [目标目录]"
  echo ""
  echo "示例:"
  echo "  cinstall weather"
  echo "  cinstall github-cli /path/to/agent/skills"
  exit 1
fi

SKILL_NAME="\$1"
TARGET_DIR="\${2:-/Users/xubangbang/.openclaw/workspace/agents/MAIN/skills}"

echo "⚡ 安装技能：\${SKILL_NAME}"
echo "   目标：\${TARGET_DIR}"
echo ""

"\${SKILLS_DIR}/quick-install.sh" "\${SKILL_NAME}" "\${TARGET_DIR}"
BINSCRIPT

chmod +x "$BIN_DIR/cinstall"

echo "✅ 创建便捷命令：cinstall"
echo "   位置：$BIN_DIR/cinstall"
echo ""

# 5. 提示添加到 PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
  echo "💡 提示：将 $BIN_DIR 添加到 PATH"
  echo ""
  echo "   添加到 ~/.zshrc 或 ~/.bashrc:"
  echo "   export PATH=\"$BIN_DIR:\$PATH\""
  echo ""
  read -p "是否现在添加？(Y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]] || [ -z "$REPLY" ]; then
    # 检测 shell
    SHELL_RC="$HOME/.zshrc"
    [ ! -f "$SHELL_RC" ] && SHELL_RC="$HOME/.bashrc"
    
    if [ -f "$SHELL_RC" ]; then
      if ! grep -q "$BIN_DIR" "$SHELL_RC" 2>/dev/null; then
        echo "" >> "$SHELL_RC"
        echo "# China Install Skills" >> "$SHELL_RC"
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$SHELL_RC"
        echo "✅ 已添加到 $SHELL_RC"
        echo "   运行 'source $SHELL_RC' 或重启终端生效"
      else
        echo "✅ PATH 已配置"
      fi
    else
      echo "⚠️  未找到 ~/.zshrc 或 ~/.bashrc"
      echo "   请手动添加：export PATH=\"$BIN_DIR:\$PATH\""
    fi
  fi
else
  echo "✅ PATH 已包含 $BIN_DIR"
fi
echo ""

# 6. 显示使用帮助
echo "=========================================="
echo "🎉 初始化完成！"
echo "=========================================="
echo ""
echo "📦 现在可以这样安装技能："
echo ""
echo "方式 1: 使用便捷命令（推荐）"
echo "   cinstall weather"
echo "   cinstall github-cli /path/to/agent/skills"
echo ""
echo "方式 2: 直接使用脚本"
echo "   cd ${SKILLS_DIR}/scripts"
echo "   ./quick-install.sh weather /path/to/agent/skills"
echo ""
echo "方式 3: 分步操作"
echo "   ./search.sh weather      # 搜索"
echo "   ./download.sh weather    # 下载"
echo "   ./install.sh weather /path/to/skills  # 安装"
echo ""
echo "📝 查看使用记录："
echo "   cat $MEMORY_FILE"
echo ""
echo "🔧 移除定时任务："
echo "   ${SCRIPT_DIR}/setup-cron.sh --remove"
echo ""
echo "=========================================="
