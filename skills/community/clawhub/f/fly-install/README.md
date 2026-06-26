# Fly Install - ClawHub 备用安装方案

> 当 `clawhub install` 遭遇速率限制时的逃生通道 🚀

## 功能特性

- ✅ **GitHub 自动搜索克隆** - 优先从 GitHub 搜索并克隆技能仓库
- ✅ **ClawHub zip 下载** - 从 clawhub.ai 直接下载 zip 包安装
- ✅ **全自动安装流程** - 一键尝试多种安装方式
- ✅ **手动安装指导** - 自动安装失败时提供详细手动步骤

## 快速开始

```bash
# 安装此技能
cd ~/.openclaw/workspace/skills
git clone https://github.com/shensiglea-collab/fly-install.git

# 使用脚本安装其他技能
~/.openclaw/workspace/skills/fly-install/fly-install.sh <skill-name>
```

## 使用方法

### 全自动安装

```bash
~/.openclaw/workspace/skills/fly-install/fly-install.sh nano-pdf
```

脚本会按以下顺序尝试：
1. 检查是否已安装
2. **GitHub 搜索并克隆**
3. ClawHub zip 下载
4. 输出手动安装指导

### GitHub 直接克隆

```bash
# 搜索并克隆
curl -s "https://api.github.com/search/repositories?q=nano-pdf+openclaw" | jq -r '.items[0].clone_url'
git clone --depth 1 <clone_url> nano-pdf
```

### ClawHub zip 手动安装

1. 访问 https://clawhub.ai/skills
2. 搜索技能，点击 "Download zip"
3. 解压到 skills 目录

## 安装方式对比

| 方式 | 速度 | 安全性 | 适用场景 |
|------|------|--------|----------|
| GitHub 克隆 | 快 ⭐⭐⭐ | 中 | 开源技能 |
| ClawHub zip | 快 ⭐⭐⭐ | 高 ⭐⭐⭐ | 官方技能 |
| fly-install 脚本 | 全自动 ⭐⭐⭐ | 高 ⭐⭐⭐ | 快速安装 |

## 安全提示

- ⚠️ 只从可信来源安装（clawhub.ai 或知名 GitHub 仓库）
- ⚠️ 检查 VirusTotal 安全扫描结果
- ⚠️ 审查 SKILL.md 内容后再使用

## GitHub 仓库

https://github.com/shensiglea-collab/fly-install

## License

MIT
