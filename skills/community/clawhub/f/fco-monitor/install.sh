#!/bin/bash
# FC Online监控Skill安装脚本

set -e

echo "🚀 开始安装FC Online官网监控Skill..."

# 检查必要工具
check_dependencies() {
  echo "🔧 检查依赖..."
  
  local missing_deps=()
  
  # 检查curl
  if ! command -v curl &> /dev/null; then
    missing_deps+=("curl")
  fi
  
  # 检查jq
  if ! command -v jq &> /dev/null; then
    missing_deps+=("jq")
  fi
  
  # 检查node
  if ! command -v node &> /dev/null; then
    missing_deps+=("node")
  fi
  
  if [ ${#missing_deps[@]} -gt 0 ]; then
    echo "⚠️ 缺少依赖: ${missing_deps[*]}"
    echo "尝试继续安装，部分功能可能受限。"
    
    # 尝试安装缺失的依赖
    for dep in "${missing_deps[@]}"; do
      echo "尝试安装 $dep..."
      if command -v yum &> /dev/null; then
        yum install -y "$dep" 2>/dev/null || true
      elif command -v apt-get &> /dev/null; then
        apt-get install -y "$dep" 2>/dev/null || true
      fi
    done
  else
    echo "✅ 所有依赖已满足"
  fi
}

# 安装Skill到OpenClaw
install_to_openclaw() {
  echo "📦 安装Skill到OpenClaw..."
  
  local skill_dir="/root/.openclaw/workspace/skills/fco-monitor"
  local openclaw_skills_dir="/usr/lib/node_modules/openclaw/skills"
  
  # 检查OpenClaw技能目录
  if [ ! -d "$openclaw_skills_dir" ]; then
    echo "⚠️ OpenClaw技能目录不存在: $openclaw_skills_dir"
    echo "尝试查找其他位置..."
    
    # 尝试其他可能的位置
    local possible_locations=(
      "/usr/local/lib/node_modules/openclaw/skills"
      "/opt/openclaw/skills"
      "$HOME/.openclaw/skills"
    )
    
    for location in "${possible_locations[@]}"; do
      if [ -d "$location" ]; then
        openclaw_skills_dir="$location"
        echo "✅ 找到技能目录: $openclaw_skills_dir"
        break
      fi
    done
  fi
  
  if [ ! -d "$openclaw_skills_dir" ]; then
    echo "❌ 无法找到OpenClaw技能目录"
    echo "请手动将本Skill目录复制到OpenClaw的skills目录下。"
    return 1
  fi
  
  # 复制Skill
  local target_dir="$openclaw_skills_dir/fco-monitor"
  
  echo "📁 复制Skill文件到: $target_dir"
  
  # 创建目标目录
  mkdir -p "$target_dir"
  
  # 复制所有文件
  cp -r "$skill_dir"/* "$target_dir"/
  
  # 设置权限
  chmod +x "$target_dir/fco-monitor.sh"
  chmod +x "$target_dir/install.sh"
  
  echo "✅ Skill文件复制完成"
}

# 创建配置文件
create_config() {
  echo "⚙️ 创建配置文件..."
  
  local config_dir="/root/.openclaw/config"
  local config_file="$config_dir/fco-monitor.json"
  
  mkdir -p "$config_dir"
  
  # 默认配置
  cat > "$config_file" << EOF
{
  "fcoMonitor": {
    "enabled": true,
    "checkSchedule": {
      "startHour": 8,
      "endHour": 23,
      "intervalMinutes": 60
    },
    "notification": {
      "enabled": true,
      "format": "detailed",
      "onlyNewActivities": true
    },
    "keywords": {
      "highPriority": [
        "26TOTY",
        "绝版",
        "TY礼包",
        "限时折扣",
        "TOTYN"
      ],
      "normalPriority": [
        "赛季",
        "活动",
        "更新",
        "公告",
        "礼包",
        "球员"
      ]
    },
    "urls": {
      "main": "https://fco.qq.com/main.shtml",
      "versionArea": "https://fco.qq.com/webplat/info/news_version3/33965/34617/38284/m22646/list_1.shtml"
    }
  }
}
EOF
  
  echo "✅ 配置文件创建完成: $config_file"
}

# 创建系统服务（可选）
create_service() {
  echo "🔄 创建系统服务（可选）..."
  
  local service_file="/etc/systemd/system/fco-monitor.service"
  
  if [ ! -d "/etc/systemd/system" ]; then
    echo "⚠️ systemd目录不存在，跳过服务创建"
    return 0
  fi
  
  cat > "$service_file" << EOF
[Unit]
Description=FC Online官网监控服务
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/root/.openclaw/workspace/skills/fco-monitor
ExecStart=/usr/bin/node openclaw-integration.js check-now
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
  
  echo "✅ 服务文件创建完成: $service_file"
  echo "   使用以下命令启用服务:"
  echo "   sudo systemctl daemon-reload"
  echo "   sudo systemctl enable fco-monitor"
  echo "   sudo systemctl start fco-monitor"
}

# 测试安装
test_installation() {
  echo "🧪 测试安装..."
  
  local skill_dir="/root/.openclaw/workspace/skills/fco-monitor"
  
  # 测试脚本执行
  echo "1. 测试监控脚本..."
  if "$skill_dir/fco-monitor.sh" help &> /dev/null; then
    echo "   ✅ 监控脚本测试通过"
  else
    echo "   ❌ 监控脚本测试失败"
    return 1
  fi
  
  # 测试Node集成
  echo "2. 测试Node集成..."
  if node "$skill_dir/openclaw-integration.js" help &> /dev/null; then
    echo "   ✅ Node集成测试通过"
  else
    echo "   ❌ Node集成测试失败"
    return 1
  fi
  
  # 测试连接
  echo "3. 测试官网连接..."
  if curl -s -I --connect-timeout 5 "https://fco.qq.com/main.shtml" | head -1 | grep -q "200"; then
    echo "   ✅ 官网连接测试通过"
  else
    echo "   ⚠️ 官网连接测试异常（可能网络问题）"
  fi
  
  echo "✅ 所有测试完成"
}

# 显示使用说明
show_usage() {
  echo ""
  echo "🎉 FC Online官网监控Skill安装完成！"
  echo ""
  echo "📋 使用说明:"
  echo ""
  echo "1. 立即检查官网活动:"
  echo "   ./fco-monitor.sh check-now"
  echo "   或"
  echo "   node openclaw-integration.js check-now"
  echo ""
  echo "2. 设置定时监控:"
  echo "   ./fco-monitor.sh setup 8 23 60"
  echo "   （8:00-23:00，每小时检查一次）"
  echo ""
  echo "3. 查看监控状态:"
  echo "   ./fco-monitor.sh status"
  echo ""
  echo "4. 在OpenClaw中使用:"
  echo "   技能已安装到OpenClaw，可以在对话中直接使用。"
  echo ""
  echo "📁 文件位置:"
  echo "   技能目录: /root/.openclaw/workspace/skills/fco-monitor"
  echo "   配置文件: /root/.openclaw/config/fco-monitor.json"
  echo "   日志文件: /tmp/fco-monitor-*.log"
  echo ""
  echo "🔧 后续配置:"
  echo "   可以编辑配置文件调整监控参数和关键词。"
  echo ""
  echo "📞 支持:"
  echo "   如有问题，请查看日志文件或联系维护者。"
}

# 主安装流程
main() {
  echo "========================================"
  echo "   FC Online官网监控Skill安装程序"
  echo "   版本: 1.0.0"
  echo "========================================"
  
  # 检查依赖
  check_dependencies
  
  # 安装到OpenClaw
  install_to_openclaw
  
  # 创建配置
  create_config
  
  # 创建服务（可选）
  create_service
  
  # 测试安装
  test_installation
  
  # 显示使用说明
  show_usage
  
  echo ""
  echo "✅ 安装完成！"
  echo "========================================"
}

# 运行主函数
main "$@"