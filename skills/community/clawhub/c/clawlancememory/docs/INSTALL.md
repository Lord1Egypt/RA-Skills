# 安装指南

## 系统要求

- Python 3.8+
- Linux/macOS/Windows
- 2GB+ RAM
- 1GB+ 磁盘空间

## 快速安装

### 1. 克隆仓库

```bash
git clone https://github.com/asbinbin/claw_lance.git
cd claw_lance
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 API Key

获取智谱 AI API Key: https://open.bigmodel.cn/

```bash
# 临时设置
export ZHIPU_API_KEY="your-key-here"

# 永久设置（添加到 ~/.bashrc）
echo 'export ZHIPU_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### 5. 测试安装

```bash
python3 skill.py stats
```

如果显示统计信息，说明安装成功！

## 启用 Hook

```bash
# 方法 1: 使用启用脚本
bash enable.sh

# 方法 2: OpenClaw 命令
openclaw hooks enable memory-system
```

## 故障排查

### Python 版本过低

```bash
python3 --version  # 需要 3.8+
```

如果版本过低，请升级 Python。

### 依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### API Key 无效

检查 API Key 是否正确：

```bash
echo $ZHIPU_API_KEY
```

确保没有多余的空格或引号。

### Hook 不工作

检查 Hook 文件是否存在：

```bash
ls -la hooks/memory-system/
```

查看 OpenClaw 日志：

```bash
tail -f ~/.openclaw/logs/openclaw.log | grep "Memory"
```

## 下一步

安装完成后，查看 [使用手册](USAGE.md) 开始使用！
