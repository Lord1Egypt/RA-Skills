# China Mirror Skill 🇨🇳

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-green.svg)](https://openclaw.ai)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-purple.svg)](https://claude.ai/code)

**AI 生成命令时自动添加国内镜像源参数。** 所有镜像源均为大厂/高校背书。

## 为什么需要这个 Skill？

在使用 **OpenClaw** 或 **Claude Code** 执行任务时，你是否遇到过：

- ❌ 安装依赖时网络超时，任务失败
- ❌ 下载包速度极慢，等待数分钟甚至更久
- ❌ 构建环境时因网络问题反复重试
- ❌ 浪费大量时间和 Token 在等待下载上

**原因：** AI 执行任务时经常需要下载包来构建运行环境（npm install、pip install、docker pull 等），而国内访问海外源速度慢、不稳定，导致任务超时失败。

**解决方案：** 让 AI 在生成命令时自动使用国内镜像源，大幅加速下载，减少任务失败率。

## 安装

### Claude Code

```bash
# 克隆仓库
git clone https://github.com/xiaomiba0904/china-mirror-skill.git

# 安装到 Claude Code skills 目录
mkdir -p ~/.agents/skills
ln -s $(pwd)/china-mirror-skill ~/.agents/skills/china-mirror

# 可选：创建符号链接到 .claude/skills
mkdir -p ~/.claude/skills
ln -s ~/.agents/skills/china-mirror ~/.claude/skills/china-mirror
```

### OpenClaw

```bash
# 克隆仓库
git clone https://github.com/xiaomiba0904/china-mirror-skill.git

# 安装到 OpenClaw skills 目录
mkdir -p ~/.openclaw/skills
ln -s $(pwd)/china-mirror-skill ~/.openclaw/skills/china-mirror
```

## 效果对比

| 场景 | 未使用镜像 | 使用镜像 |
|------|-----------|----------|
| npm install | 超时/数分钟 | 几秒完成 |
| pip install | 经常失败 | 稳定快速 |
| docker pull | 极慢 | 秒级拉取 |
| pyenv install | 可能超时 | 稳定下载 |

## 支持范围

**包管理器：** npm/pnpm/yarn/bun, pip/uv/poetry, conda, gem, composer, nuget, cargo, go, docker, brew, maven/gradle...

**版本管理：** pyenv, nvm/fnm/volta, rbenv, gvm, sdkman, tfenv, asdf, julia...

**系统包：** apt, yum/dnf, apk, pacman

## 镜像源背书方

| 类型 | 背书方 |
|------|--------|
| 大厂 | 阿里巴巴、华为云、腾讯云、字节跳动、网易、七牛云 |
| 高校 | 清华大学、中国科学技术大学 |

**禁止使用无背书的不明镜像源。**

## 许可证

[MIT License](./LICENSE)
