---
name: fly-install
description: 当 ClawHub CLI 速率限制或安装失败时，通过多种备用方式安装技能：1) clawhub.ai 下载 zip；2) GitHub 搜索并克隆；3) 手动流程指导。
---

# Fly Install - ClawHub 备用安装方案

> 当 `clawhub install` 遭遇速率限制时的逃生通道 🚀

## 问题场景

- `npx clawhub install <skill>` 返回 `Rate limit exceeded`
- `clawhub` CLI 无法访问或安装失败
- 急需安装某个技能但官方渠道受阻

## 解决方案（三种方式）

### 方式一：全自动脚本（推荐）

```bash
# 使用 fly-install 脚本，自动尝试多种安装方式
~/.openclaw/workspace/skills/fly-install/fly-install.sh <skill-name>

# 示例
~/.openclaw/workspace/skills/fly-install/fly-install.sh nano-pdf
~/.openclaw/workspace/skills/fly-install/fly-install.sh skill-vetter
```

脚本会按以下顺序尝试：
1. 检查是否已安装
2. 尝试从 GitHub 搜索并克隆
3. 从 clawhub.ai 下载 zip
4. 输出手动安装指导

### 方式二：GitHub 直接克隆

```bash
# 搜索 GitHub 上的技能仓库并克隆
cd ~/.openclaw/workspace/skills

# 搜索技能（示例）
curl -s "https://api.github.com/search/repositories?q=nano-pdf+openclaw" | jq -r '.items[0].clone_url'

# 克隆到本地
git clone --depth 1 <clone_url> <skill-name>
```

### 方式三：ClawHub 下载 zip

访问 https://clawhub.ai/skills 搜索技能，下载 zip 包手动安装。

## 详细使用指南

### 全自动安装脚本

```bash
# 基础用法
~/.openclaw/workspace/skills/fly-install/fly-install.sh <skill-name>

# 指定安装目录
~/.openclaw/workspace/skills/fly-install/fly-install.sh <skill-name> /custom/skills/path

# 查看帮助
~/.openclaw/workspace/skills/fly-install/fly-install.sh --help
```

### 手动 GitHub 克隆流程

#### 步骤 1: 搜索 GitHub 仓库

```bash
# 使用 GitHub API 搜索技能仓库
SEARCH_QUERY="<skill-name>+openclaw+skill"
curl -s "https://api.github.com/search/repositories?q=$SEARCH_QUERY" | jq -r '.items[0:3] | .[] | "\(.full_name): \(.clone_url)"'
```

#### 步骤 2: 验证并克隆

```bash
cd ~/.openclaw/workspace/skills

# 克隆仓库（替换为实际的 clone_url）
git clone --depth 1 <clone_url> <skill-name>

# 验证安装
ls <skill-name>/SKILL.md
cat <skill-name>/SKILL.md
```

### 手动 ClawHub zip 流程

#### 步骤 1: 搜索技能
访问 https://clawhub.ai/skills 搜索你要安装的技能名称

#### 步骤 2: 进入详情页
点击技能卡片进入详情页，确认：
- ✅ 安全扫描状态（VirusTotal + OpenClaw）
- ✅ 作者信息
- ✅ 下载次数和评分

#### 步骤 3: 获取下载链接
在详情页找到 "Download zip" 按钮，复制链接地址

#### 步骤 4: 下载并安装
```bash
cd ~/.openclaw/workspace/skills

# 下载 zip 包（替换为实际的下载链接）
wget -O <skill-name>.zip "<下载链接>"

# 解压到独立文件夹
unzip -q <skill-name>.zip -d <skill-name>

# 删除 zip 包
rm <skill-name>.zip

# 验证安装
ls <skill-name>/SKILL.md
```

## 批量安装

```bash
# 创建技能列表
cat > skills-to-install.txt << EOF
nano-pdf
skill-vetter
clawshield
atxp
EOF

# 批量安装
while read skill; do
  ~/.openclaw/workspace/skills/fly-install/fly-install.sh "$skill"
done < skills-to-install.txt
```

## 安装方式对比

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **GitHub 克隆** | 版本控制、可更新 | 需要找到正确仓库 | 开源技能 |
| **ClawHub zip** | 官方来源、安全可靠 | 需手动下载 | 闭源/官方技能 |
| **fly-install 脚本** | 全自动、多方式尝试 | 依赖网络 | 快速安装 |

## 安全提醒 ⚠️

- **只从可信来源安装**：clawhub.ai 官方或知名 GitHub 仓库
- **安装前检查 VirusTotal 扫描结果**
- **审查 SKILL.md 内容后再使用**
- **不要安装来源不明的技能**

## 故障排除

### GitHub 克隆失败
```bash
# 检查仓库是否存在
curl -s https://api.github.com/repos/<owner>/<repo> | jq -r '.message'

# 使用 https 替代 ssh
git clone https://github.com/<owner>/<repo>.git
```

### zip 下载失败
```bash
# 使用 curl 替代 wget
curl -L -o skill.zip "<下载链接>"
```

### 解压失败
```bash
# 安装 unzip
apt-get install unzip  # Ubuntu/Debian
brew install unzip     # macOS
```

## 更新技能

```bash
# GitHub 克隆的技能
cd ~/.openclaw/workspace/skills/<skill-name>
git pull

# zip 安装的技能（需重新下载）
mv <skill-name> <skill-name>-backup
~/.openclaw/workspace/skills/fly-install/fly-install.sh <skill-name>
```

## 相关技能

- `find-skills` - 搜索发现新技能
- `healthcheck` - 检查系统健康状态
- `security-check` - 扫描技能安全性

---

*🦞 大龙虾的逃生通道，CLI 受阻时的救命稻草。*
