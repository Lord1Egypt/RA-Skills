#!/bin/bash
# A 股股票技能 - 快速配置脚本

echo "📈 A 股每日精选 - 快速配置"
echo ""

# 检测邮箱服务商
echo "请选择你的邮箱服务商:"
echo "  1) QQ 邮箱"
echo "  2) Gmail"
echo "  3) 163 邮箱"
echo "  4) Outlook/Hotmail"
echo "  5) 其他（手动配置）"
echo ""
read -p "选择 [1-5]: " choice

case $choice in
  1)
    SMTP_HOST="smtp.qq.com"
    SMTP_PORT="587"
    echo ""
    echo "📧 QQ 邮箱配置说明:"
    echo "  1. 登录 https://mail.qq.com"
    echo "  2. 设置 → 账户 → 开启 POP3/SMTP 服务"
    echo "  3. 生成授权码（不是 QQ 密码！）"
    echo ""
    read -p "输入 QQ 邮箱号码: " EMAIL_USER
    read -p "输入授权码: " -s EMAIL_PASS
    echo ""
    ;;
  2)
    SMTP_HOST="smtp.gmail.com"
    SMTP_PORT="587"
    echo ""
    echo "📧 Gmail 配置说明:"
    echo "  1. 登录 Google 账户"
    echo "  2. 开启两步验证"
    echo "  3. 生成应用专用密码: https://myaccount.google.com/apppasswords"
    echo ""
    read -p "输入 Gmail 地址: " EMAIL_USER
    read -p "输入应用专用密码: " -s EMAIL_PASS
    echo ""
    ;;
  3)
    SMTP_HOST="smtp.163.com"
    SMTP_PORT="587"
    echo ""
    echo "📧 163 邮箱配置说明:"
    echo "  1. 登录 https://mail.163.com"
    echo "  2. 设置 → POP3/SMTP/IMAP → 开启 SMTP 服务"
    echo "  3. 生成授权码"
    echo ""
    read -p "输入 163 邮箱地址: " EMAIL_USER
    read -p "输入授权码: " -s EMAIL_PASS
    echo ""
    ;;
  4)
    SMTP_HOST="smtp-mail.outlook.com"
    SMTP_PORT="587"
    echo ""
    echo "📧 Outlook 邮箱配置说明:"
    echo "  1. 登录 Outlook 账户"
    echo "  2. 可能需要开启应用访问权限"
    echo ""
    read -p "输入 Outlook 邮箱地址: " EMAIL_USER
    read -p "输入密码: " -s EMAIL_PASS
    echo ""
    ;;
  *)
    read -p "输入 SMTP 服务器: " SMTP_HOST
    read -p "输入端口 [587]: " SMTP_PORT
    SMTP_PORT=${SMTP_PORT:-587}
    read -p "输入用户名 (邮箱): " EMAIL_USER
    read -p "输入密码: " -s EMAIL_PASS
    echo ""
    ;;
esac

# 创建 SMTP 配置
SMTP_CONFIG="{\"host\":\"$SMTP_HOST\",\"port\":$SMTP_PORT,\"secure\":false,\"user\":\"$EMAIL_USER\",\"pass\":\"$EMAIL_PASS\",\"from\":\"$EMAIL_USER\"}"

echo ""
echo "⚙️  正在保存配置..."

# 保存到 .env 文件
cat > .env << EOF
SMTP_CONFIG='$SMTP_CONFIG'
EOF

echo "✅ 配置已保存到 .env 文件"

# 添加到 shell 配置文件
SHELL_RC=""
if [ -f ~/.zshrc ]; then
  SHELL_RC=~/.zshrc
elif [ -f ~/.bashrc ]; then
  SHELL_RC=~/.bashrc
elif [ -f ~/.bash_profile ]; then
  SHELL_RC=~/.bash_profile
fi

if [ -n "$SHELL_RC" ]; then
  echo ""
  read -p "是否添加到 $SHELL_RC 以便全局使用？(y/n): " add_to_rc
  if [ "$add_to_rc" = "y" ]; then
    # 检查是否已存在
    if ! grep -q "SMTP_CONFIG" "$SHELL_RC" 2>/dev/null; then
      echo "" >> "$SHELL_RC"
      echo "# A 股股票技能 SMTP 配置" >> "$SHELL_RC"
      echo "export SMTP_CONFIG='$SMTP_CONFIG'" >> "$SHELL_RC"
      echo "✅ 已添加到 $SHELL_RC"
      echo "💡 运行 'source $SHELL_RC' 使其生效"
    else
      echo "⚠️  $SHELL_RC 中已存在 SMTP_CONFIG，跳过"
    fi
  fi
fi

# 配置 cron
echo ""
echo "⏰ 配置定时任务..."
read -p "是否添加每天 9:30 自动运行（周一至周五）? (y/n): " setup_cron

if [ "$setup_cron" = "y" ]; then
  NODE_PATH=$(which node)
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  CRON_LINE="30 9 * * 1-5 cd $SCRIPT_DIR && $NODE_PATH index.js >> /tmp/astock-daily.log 2>&1"
  
  # 检查 crontab 中是否已存在
  if crontab -l 2>/dev/null | grep -q "astock-daily"; then
    echo "⚠️  crontab 中已存在 astock-daily 任务"
  else
    (crontab -l 2>/dev/null | grep -v "astock-daily"; echo "$CRON_LINE") | crontab -
    echo "✅ 已添加 cron 任务：每天 9:30 运行（周一至周五）"
  fi
  
  echo ""
  echo "💡 查看日志：tail -f /tmp/astock-daily.log"
  echo "💡 查看 cron: crontab -l"
fi

echo ""
echo "=========================================="
echo "✅ 配置完成！"
echo "=========================================="
echo ""
echo "🧪 测试运行:"
echo "   source .env && node index.js"
echo ""
echo "📧 目标邮箱：8@batype.com"
echo "💰 价格上限：20 元"
echo ""
