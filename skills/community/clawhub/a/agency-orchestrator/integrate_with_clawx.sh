#!/bin/bash
# ClawX 集成脚本

AGENCY_SKILL_DIR="$HOME/.openclaw/skills/agency-orchestrator"
AGENCY_DIR="$HOME/.openclaw/agency-agents-zh"

echo "🔧 开始集成 Agency Orchestrator 到 ClawX..."
echo ""

# 1. 确保技能目录存在
if [ ! -d "$AGENCY_SKILL_DIR" ]; then
    echo "❌ 技能目录不存在"
    exit 1
fi

# 2. 更新 openclaw.json 配置
echo "📝 更新 ClawX 配置..."
python3 << PYTHON
import json
import os

config_file = os.path.expanduser("~/.openclaw/openclaw.json")
try:
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 添加 agency-orchestrator 技能
    if 'skills' not in config:
        config['skills'] = {}
    if 'entries' not in config['skills']:
        config['skills']['entries'] = {}
    
    config['skills']['entries']['agency-orchestrator'] = {
        'enabled': True,
        'description': '多 Agent 协作调度系统',
        'version': '1.0.0'
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ ClawX 配置已更新")
except Exception as e:
    print(f"⚠️ 配置更新失败：{e}")
PYTHON

# 3. 添加环境变量
echo ""
echo "🔧 添加环境变量..."
if ! grep -q "AGENCY_DIR" ~/.bash_profile 2>/dev/null; then
    echo 'export AGENCY_DIR="$HOME/.openclaw/agency-agents-zh"' >> ~/.bash_profile
    echo 'export PATH="$AGENCY_DIR:$PATH"' >> ~/.bash_profile
    echo "✅ 已添加到 ~/.bash_profile"
else
    echo "✅ 环境变量已存在"
fi

# 4. 创建 Qwen 别名
echo ""
echo "🔧 创建 Qwen 命令别名..."
if ! grep -q "alias qwen-agency" ~/.bash_profile 2>/dev/null; then
    echo 'alias qwen-agency="python3 $HOME/.openclaw/skills/agency-orchestrator/qwen_extension.py"' >> ~/.bash_profile
    echo "✅ 已创建别名 qwen-agency"
else
    echo "✅ 别名已存在"
fi

# 5. 刷新配置
source ~/.bash_profile 2>/dev/null

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  ✅ ClawX 集成完成                                        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📋 使用方式:"
echo ""
echo "1. 在 ClawX 中使用:"
echo "   qwen -p '使用 agency-orchestrator 设计一个电商网站'"
echo ""
echo "2. 命令行使用:"
echo "   qwen-agency execute <任务描述>"
echo "   qwen-agency list [分类]"
echo "   qwen-agency status"
echo ""
echo "3. Python 调用:"
echo "   from agency_orchestrator import AgencyOrchestrator"
echo "   orchestrator = AgencyOrchestrator()"
echo "   result = orchestrator.coordinate('任务描述')"
echo ""
echo "💡 提示：运行 'source ~/.bash_profile' 使配置立即生效"
echo ""
