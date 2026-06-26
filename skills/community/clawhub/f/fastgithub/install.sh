#!/bin/bash
# FastGithub 自动安装脚本

INSTALL_DIR="/workspace/skills/fastgithub"

echo "正在安装 FastGithub..."

# 检查是否已解压
if [ ! -d "$INSTALL_DIR/publish" ]; then
    echo "正在解压安装包..."
    tar -xzf "$INSTALL_DIR/fastgithub-linux-x64.tar.gz" -C "$INSTALL_DIR"
fi

# 检查是否已在运行
if pgrep -f "fastgithub" > /dev/null; then
    echo "FastGithub 已在运行中"
    exit 0
fi

# 启动服务
echo "正在启动 FastGithub..."
cd "$INSTALL_DIR/publish"
nohup ./fastgithub > /workspace/fastgithub.log 2>&1 &
sleep 2

# 验证启动
if pgrep -f "fastgithub" > /dev/null; then
    echo "✅ FastGithub 启动成功！"
    echo "代理地址: http://127.0.0.1:38457"
    
    # 设置代理环境变量
    export http_proxy=http://127.0.0.1:38457
    export https_proxy=http://127.0.0.1:38457
    
    echo ""
    echo "请运行以下命令设置 Git 代理："
    echo "export http_proxy=http://127.0.0.1:38457"
    echo "export https_proxy=http://127.0.0.1:38457"
else
    echo "❌ 启动失败，请查看日志: /workspace/fastgithub.log"
fi