# Credential Auditor 安装指南

## 快速安装

### 步骤1：下载技能

```bash
# 方法1：克隆仓库
git clone https://github.com/jeanphorn/credential_auditor.git
cd credential_auditor

# 方法2：下载压缩包
# 从 GitHub 下载 ZIP 文件并解压
```

### 步骤2：安装到 OpenClaw

```bash
# 创建 OpenClaw 技能目录（如果不存在）
mkdir -p ~/.openclaw/workspace/skills/

# 复制技能到 OpenClaw
cp -r . ~/.openclaw/workspace/skills/credential_auditor/

# 或者使用符号链接（推荐，方便更新）
ln -s $(pwd) ~/.openclaw/workspace/skills/credential_auditor
```

### 步骤3：安装 Python 依赖

```bash
# 安装必需依赖
pip install paramiko requests colorama
```

### 步骤4：验证安装

```bash
# 重启 OpenClaw 或重新加载技能
# 然后在 OpenClaw 中测试
openclaw agent --message "列出所有支持的设备类型"
```

## 安装可选工具

为了获得更好的性能，建议安装专业安全工具：

### macOS

```bash
# 使用 Homebrew 安装
brew install hydra medusa ncrack
```

### Ubuntu/Debian

```bash
# 使用 apt 安装
sudo apt-get update
sudo apt-get install hydra medusa ncrack
```

### Windows

1. 从官方网站下载对应工具
2. 将工具添加到系统 PATH

## 验证安装

运行以下命令验证技能是否正确安装：

```bash
# 测试设备匹配器
cd ~/.openclaw/workspace/skills/credential_auditor
python scripts/device_matcher.py --list-devices

# 测试密码生成器
python scripts/wordlist_generator.py --rule-based \
  --target-info "company:Test,year:2024"

# 检查工具集成
python scripts/tool_integration.py --check-tools
```

## 更新技能

```bash
# 如果使用 git 克隆
cd ~/.openclaw/workspace/skills/credential_auditor
git pull

# 如果使用符号链接
cd /path/to/credential_auditor
git pull
```

## 卸载技能

```bash
# 删除技能目录
rm -rf ~/.openclaw/workspace/skills/credential_auditor
```

## 故障排除

### 问题1：技能未加载

**解决方案**：
- 检查技能是否在正确的目录：`~/.openclaw/workspace/skills/credential_auditor/`
- 确保 `SKILL.md` 文件存在
- 重启 OpenClaw

### 问题2：Python 模块导入失败

**解决方案**：
```bash
pip install paramiko requests colorama
```

### 问题3：工具未找到

**解决方案**：
- 安装对应的工具（Hydra、Medusa、Ncrack）
- 或使用纯 Python 实现（功能有限）

## 下一步

安装完成后，请阅读：
- `README.md` - 完整使用指南
- `SKILL.md` - 技能详细说明

开始使用：
```
在 OpenClaw 中输入："帮我查询 Cisco 路由器的默认密码"
```

---

**安装遇到问题？** 查看 [GitHub Issues](https://github.com/jeanphorn/credential_auditor/issues)
