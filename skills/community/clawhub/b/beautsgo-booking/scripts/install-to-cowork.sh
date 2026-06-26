#!/bin/bash
# 自动在所有 Cowork 会话目录里安装 beautsgo-booking 技能
# 注意：Cowork 不支持符号链接，必须复制真实文件

SKILL_PATH="/Users/wangning/project/company/beautsgo-booking"
COWORK_BASE="/Users/wangning/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"

count=0
for session_dir in "$COWORK_BASE"/*/*; do
  skills_dir="$session_dir/skills"
  if [ -d "$skills_dir" ]; then
    skill_target="$skills_dir/beautsgo-booking"
    # 删除旧的（无论是链接还是目录）
    rm -rf "$skill_target"
    # 复制新的（排除 .git 和 node_modules）
    rsync -a --exclude='.git' --exclude='node_modules' --exclude='.workbuddy' "$SKILL_PATH/" "$skill_target/"
    echo "✅ 已安装: $skill_target"
    ((count++))
  fi
done

echo ""
echo "完成！共安装到 $count 个会话"