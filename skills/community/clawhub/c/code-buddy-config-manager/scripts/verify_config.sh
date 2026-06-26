#!/bin/bash
# =============================================================================
# CodeBuddy 配置验证脚本
# 安装/更新完成后验证配置状态，输出结构化验证报告
#
# 用法: ./verify_config.sh <config_type> <config_name> [config_scope] [operation]
#
# 参数:
#   config_type  - 配置类型: mcp | skill | plugin | model | cli | other
#   config_name  - 配置项名称
#   config_scope - 作用域: global | project (默认: project)
#   operation    - 操作类型: install | update (默认: install)
#
# 输出: JSON 格式的验证报告
# =============================================================================

set -eo pipefail

# ---------- 参数解析 ----------
CONFIG_TYPE="${1:-}"
CONFIG_NAME="${2:-}"
CONFIG_SCOPE="${3:-project}"
OPERATION="${4:-install}"

if [ -z "$CONFIG_TYPE" ] || [ -z "$CONFIG_NAME" ]; then
  echo '{"error":true,"message":"Usage: verify_config.sh <config_type> <config_name> [config_scope] [operation]"}'
  exit 1
fi

# ---------- 路径常量 ----------
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHECK_STATUS_SCRIPT="$SCRIPT_DIR/check_status.sh"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../../.." 2>/dev/null && pwd || echo "")"

# ---------- 运行状态检测 ----------
run_check() {
  if [ -x "$CHECK_STATUS_SCRIPT" ]; then
    "$CHECK_STATUS_SCRIPT" "$CONFIG_TYPE" "$CONFIG_NAME" "$CONFIG_SCOPE" 2>/dev/null || \
      echo '{"exists":false,"status":"error","version":null,"needs_update":false,"expected_version":null,"details":"状态检测脚本执行失败"}'
  else
    echo '{"exists":false,"status":"error","version":null,"needs_update":false,"expected_version":null,"details":"状态检测脚本不存在或不可执行"}'
  fi
}

# ---------- 获取目标路径 ----------
get_target_path() {
  case "$CONFIG_TYPE" in
    mcp)
      if [ "$CONFIG_SCOPE" = "global" ]; then
        echo "$HOME/.codebuddy/mcp.json"
      else
        echo "$PROJECT_DIR/.codebuddy/mcp.json"
      fi
      ;;
    skill)
      if [ "$CONFIG_SCOPE" = "global" ]; then
        echo "$HOME/.codebuddy/skills-marketplace/skills/$CONFIG_NAME"
      else
        echo "$PROJECT_DIR/.codebuddy/skills/$CONFIG_NAME"
      fi
      ;;
    plugin)
      echo "$HOME/.codebuddy/settings.json"
      ;;
    model)
      echo "$HOME/.codebuddy/settings.json"
      ;;
    cli)
      echo "PATH: $(command -v "$CONFIG_NAME" 2>/dev/null || echo '未安装')"
      ;;
    other)
      echo "自定义路径"
      ;;
  esac
}

# ---------- 验证 CLI 工具 ----------
verify_cli() {
  local bin_path
  bin_path=$(command -v "$CONFIG_NAME" 2>/dev/null || echo "")

  if [ -n "$bin_path" ]; then
    # 测试运行
    if "$CONFIG_NAME" --help &>/dev/null || "$CONFIG_NAME" --version &>/dev/null; then
      return 0
    else
      return 1
    fi
  fi
  return 1
}

# ---------- 验证 MCP 配置 ----------
verify_mcp() {
  local mcp_file
  if [ "$CONFIG_SCOPE" = "global" ]; then
    mcp_file="$HOME/.codebuddy/mcp.json"
  else
    mcp_file="$PROJECT_DIR/.codebuddy/mcp.json"
  fi

  if [ ! -f "$mcp_file" ]; then
    echo "MCP 配置文件不存在"
    return 1
  fi

  if command -v python3 &>/dev/null; then
    if python3 << PYEOF
import json, sys, re

mcp_file = "$mcp_file"
config_name = "$CONFIG_NAME"

def sanitize_value(val, max_len=30):
    """敏感值脱敏：对疑似密钥/令牌的参数值进行遮盖"""
    sensitive_patterns = [
        r'(sk-|pk-|api[_-]?key|token|secret|password|credential|auth)[=:]\s*(\S+)',
        r'(--(api[_-]?key|token|secret|password|auth|credential))\s+(\S+)',
    ]
    s = str(val)
    for pat in sensitive_patterns:
        s = re.sub(pat, lambda m: m.group(1) + '=****', s, flags=re.IGNORECASE)
    return s

def should_mask_arg(arg):
    """判断参数值是否看起来像敏感信息"""
    arg_lower = arg.lower()
    sensitive_indicators = ['key=', 'token=', 'secret=', 'password=', 'sk-', 'pk-', 'api_']
    return any(indicator in arg_lower for indicator in sensitive_indicators)

try:
    with open(mcp_file) as f:
        data = json.load(f)
    servers = data.get('mcpServers', {})
    cfg = servers.get(config_name)
    if cfg is None:
        print(f'\u2717 MCP Server "{config_name}" \u672a\u5728\u914d\u7f6e\u6587\u4ef6\u4e2d\u627e\u5230')
        sys.exit(1)
    required = ['type', 'command']
    missing = [f for f in required if f not in cfg]
    if missing:
        print(f'\u2717 MCP Server \u7f3a\u5c11\u5fc5\u8981\u5b57\u6bb5: {missing}')
        sys.exit(1)
    print(f'\u2713 MCP Server \u914d\u7f6e\u5b8c\u6574')
    # 类型：安全输出
    print(f'  - \u7c7b\u578b: {cfg.get("type")}')
    # 命令：只输出可执行文件名（不含参数），防止内嵌密钥
    cmd = cfg.get("command", "")
    cmd_binary = cmd.split()[0] if cmd else ""
    print(f'  - \u547d\u4ee4: {sanitize_value(cmd_binary)}')
    # 参数：对敏感性参数遮盖
    args = cfg.get("args", [])
    safe_args = ['****' if should_mask_arg(a) else sanitize_value(a) for a in args]
    print(f'  - \u53c2\u6570\u6570\u91cf: {len(args)}')
    if safe_args:
        print(f'  - \u53c2\u6570\u5217\u8868: {safe_args}')
    # 环境变量：仅输出变量名（不输出值）
    env_keys = list(cfg.get("env", {}).keys())
    print(f'  - \u73af\u5883\u53d8\u91cf: {env_keys if env_keys else "\u65e0"}')
except Exception as e:
    print(f'\u2717 \u9a8c\u8bc1\u51fa\u9519: {sanitize_value(str(e))}')
    sys.exit(1)
PYEOF
then
    return 0
  else
    return 1
  fi
  else
    if grep -q "\"$CONFIG_NAME\"" "$mcp_file" 2>/dev/null; then
      echo "✓ MCP Server 配置存在（grep 检测）"
      return 0
    else
      echo "✗ MCP Server 配置未找到"
      return 1
    fi
  fi
}

# ---------- 验证 Skill ----------
verify_skill() {
  local skill_dir
  if [ "$CONFIG_SCOPE" = "global" ]; then
    skill_dir="$HOME/.codebuddy/skills-marketplace/skills/$CONFIG_NAME"
  else
    skill_dir="$PROJECT_DIR/.codebuddy/skills/$CONFIG_NAME"
  fi

  if [ ! -d "$skill_dir" ]; then
    echo "✗ Skill 目录不存在: $skill_dir"
    return 1
  fi

  if [ ! -f "$skill_dir/SKILL.md" ]; then
    echo "✗ Skill 目录缺少 SKILL.md"
    return 1
  fi

  local skill_md_size
  skill_md_size=$(wc -c < "$skill_dir/SKILL.md" 2>/dev/null || echo 0)
  if [ "$skill_md_size" -lt 10 ]; then
    echo "✗ SKILL.md 文件过小，可能内容不完整（$skill_md_size bytes）"
    return 1
  fi

  echo "✓ Skill 安装完整"
  echo "  - 路径: $skill_dir"
  echo "  - SKILL.md: $skill_md_size bytes"

  # 列出子文件和目录
  local sub_items
  sub_items=$(find "$skill_dir" -mindepth 1 -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')
  echo "  - 包含 $sub_items 个子项"

  return 0
}

# ---------- 验证 Plugin ----------
verify_plugin() {
  local settings_file="$HOME/.codebuddy/settings.json"

  if [ ! -f "$settings_file" ]; then
    echo "✗ settings.json 不存在"
    return 1
  fi

  if command -v python3 &>/dev/null; then
    python3 << PYEOF
import json, sys

settings_file = "$settings_file"
config_name = "$CONFIG_NAME"

try:
    with open(settings_file) as f:
        data = json.load(f)
    plugins = data.get('enabledPlugins', {})
    for key, val in plugins.items():
        if key == config_name or key.startswith(config_name + '@'):
            status = '\u5df2\u542f\u7528 \u2713' if val else '\u5df2\u7981\u7528 \u2717'
            print('\u2713 Plugin "' + key + '" ' + status)
            sys.exit(0)
    print('\u2717 Plugin "' + config_name + '" \u672a\u627e\u5230')
    sys.exit(1)
except Exception as e:
    print('\u2717 \u8bfb\u53d6\u914d\u7f6e\u5931\u8d25\uff1a\u8be6\u60c5\u5df2\u9690\u85cf')
    sys.exit(1)
PYEOF
 2>/dev/null && return 0 || return 1
  else
    if grep -q "\"$CONFIG_NAME" "$settings_file" 2>/dev/null; then
      echo "✓ Plugin 配置存在（grep 检测）"
      return 0
    fi
    echo "✗ Plugin 未找到"
    return 1
  fi
}

# ---------- 验证 Model ----------
verify_model() {
  # Model 配置验证：仅检测配置是否存在，不暴露具体变量名和值
  local found=false
  local key_count=0
  local endpoint_count=0

  # 检查常见的 API Key 环境变量（只计数，不输出变量名）
  for var in OPENAI_API_KEY DEEPSEEK_API_KEY ANTHROPIC_API_KEY AZURE_OPENAI_API_KEY GEMINI_API_KEY; do
    if [ -n "${!var:-}" ]; then
      key_count=$((key_count + 1))
      found=true
    fi
  done

  # 检查端点配置
  for var in OPENAI_BASE_URL AZURE_OPENAI_ENDPOINT; do
    if [ -n "${!var:-}" ]; then
      endpoint_count=$((endpoint_count + 1))
      found=true
    fi
  done

  if $found; then
    echo "✓ Model 配置检测完成（已检测到相关配置）"
    echo "  - API 密钥: 已配置 $key_count 项（具体名称已隐藏）"
    echo "  - 端点配置: 已配置 $endpoint_count 项（具体名称已隐藏）"
    echo "  ⚠ 注意：以上信息仅确认配置存在，未输出任何敏感值"
    return 0
  else
    echo "⚠ Model 配置需通过 IDE 设置界面手动配置，请在 设置 → AI Model 中检查"
    return 1
  fi
}

# ---------- 验证 Other ----------
verify_other() {
  echo "⚠ 自定义类型验证："
  # 尝试所有已知验证方法
  local all_ok=true

  if command -v "$CONFIG_NAME" &>/dev/null; then
    echo "  ✓ 在 PATH 中找到可执行文件"
  else
    all_ok=false
  fi

  if [ -d "$HOME/.codebuddy/skills-marketplace/skills/$CONFIG_NAME" ]; then
    echo "  ✓ 作为 Skill 已安装"
    all_ok=true
  fi

  for mcp_file in "$HOME/.codebuddy/mcp.json" "$PROJECT_DIR/.codebuddy/mcp.json"; do
    if [ -f "$mcp_file" ] && grep -q "\"$CONFIG_NAME\"" "$mcp_file" 2>/dev/null; then
      echo "  ✓ 作为 MCP Server 已配置"
      all_ok=true
    fi
  done

  if $all_ok; then
    return 0
  else
    echo "  ✗ 未找到任何有效的配置"
    return 1
  fi
}

# =============================================================================
# 主流程
# =============================================================================

echo ""
echo "═══════════════════════════════════════════"
echo "  CodeBuddy 配置验证报告"
echo "═══════════════════════════════════════════"
echo "  配置类型: $CONFIG_TYPE"
echo "  配置名称: $CONFIG_NAME"
echo "  作用域:   $CONFIG_SCOPE"
echo "  操作:     $OPERATION"
echo "  时间:     $(date '+%Y-%m-%d %H:%M:%S')"
echo "───────────────────────────────────────────"

# 步骤 1: 运行状态检测（获取安装前/更新前状态）
echo ""
echo " [步骤 1/4] 运行状态检测..."
PREV_STATUS=$(run_check)
echo "   检测完成"

# 步骤 2: 验证配置完整性
echo ""
echo " [步骤 2/4] 验证配置完整性..."
VERIFY_RESULT=""
VERIFY_STATUS=0

case "$CONFIG_TYPE" in
  mcp)    verify_mcp && VERIFY_STATUS=0 || VERIFY_STATUS=1 ;;
  skill)  verify_skill && VERIFY_STATUS=0 || VERIFY_STATUS=1 ;;
  plugin) verify_plugin && VERIFY_STATUS=0 || VERIFY_STATUS=1 ;;
  model)  verify_model && VERIFY_STATUS=0 || VERIFY_STATUS=1 ;;
  cli)    verify_cli && VERIFY_STATUS=0 || VERIFY_STATUS=1 ;;
  other)  verify_other && VERIFY_STATUS=0 || VERIFY_STATUS=1 ;;
esac

# 步骤 3: 再次运行状态检测（获取安装后/更新后状态）
echo ""
echo " [步骤 3/4] 二次确认状态..."
POST_STATUS=$(run_check)
echo "   二次确认完成"

# 步骤 4: 生成最终报告
echo ""
echo " [步骤 4/4] 生成验证报告..."

# 从 JSON 中提取状态
PREV_EXISTS=$(echo "$PREV_STATUS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(str(d.get('exists','')).lower())" 2>/dev/null || echo "unknown")
POST_EXISTS=$(echo "$POST_STATUS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(str(d.get('exists','')).lower())" 2>/dev/null || echo "unknown")
POST_STATUS_VAL=$(echo "$POST_STATUS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status','unknown'))" 2>/dev/null || echo "unknown")
POST_VERSION=$(echo "$POST_STATUS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('version') or 'N/A')" 2>/dev/null || echo "unknown")

# 确定总状态
OVERALL_STATUS="failed"
if [ "$POST_EXISTS" = "true" ] && [ "$POST_STATUS_VAL" = "enabled" ] && [ $VERIFY_STATUS -eq 0 ]; then
  OVERALL_STATUS="success"
elif [ "$POST_EXISTS" = "true" ] && [ $VERIFY_STATUS -eq 0 ]; then
  OVERALL_STATUS="success"
elif [ "$POST_EXISTS" = "true" ]; then
  OVERALL_STATUS="partial"
fi

echo ""
echo "───────────────────────────────────────────"
echo "  验证结果: $(if [ "$OVERALL_STATUS" = "success" ]; then echo '✓ 成功'; elif [ "$OVERALL_STATUS" = "partial" ]; then echo '⚠ 部分成功'; else echo '✗ 失败'; fi)"
echo "───────────────────────────────────────────"
echo "  操作前: $( [ "$PREV_EXISTS" = "true" ] && echo '已存在' || echo '不存在' )"
echo "  操作后: $( [ "$POST_EXISTS" = "true" ] && echo '已配置 ✓' || echo '未找到 ✗' )"
echo "  当前状态: $POST_STATUS_VAL"
echo "  版本: $POST_VERSION"
echo "  目标路径: $(get_target_path)"
echo "───────────────────────────────────────────"

if [ "$OVERALL_STATUS" = "success" ]; then
  echo "  推荐操作: $( [ "$OPERATION" = "install" ] && echo '配置完成，重启 IDE 后生效' || echo '更新完成，重启 IDE 后生效' )"
elif [ "$OVERALL_STATUS" = "partial" ]; then
  echo "  推荐操作: 配置部分完成，请手动检查并修复"
else
  echo "  推荐操作: 配置失败，请检查日志后重试"
fi

echo "═══════════════════════════════════════════"
echo ""

# 输出 JSON 格式的详细报告供自动化解析
cat <<REPORT_EOF
{
  "overall_status": "$OVERALL_STATUS",
  "config_type": "$CONFIG_TYPE",
  "config_name": "$CONFIG_NAME",
  "scope": "$CONFIG_SCOPE",
  "operation": "$OPERATION",
  "target_path": "$(get_target_path | sed 's/"/\\"/g')",
  "verification_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "previous_status": $(echo "$PREV_STATUS" | tr -d '\n'),
  "final_status": $(echo "$POST_STATUS" | tr -d '\n'),
  "integrity_check": $([ $VERIFY_STATUS -eq 0 ] && echo 'true' || echo 'false'),
  "recommendations": [
    "重启 IDE 以应用配置更改",
    "使用 check_status.sh 确认持久化状态"
  ]
}
REPORT_EOF

[ "$OVERALL_STATUS" = "success" ] && exit 0 || exit 1
