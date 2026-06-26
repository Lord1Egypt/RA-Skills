---
name: cn-dev-setup
description: >
  一键配置国内开发环境镜像源。解决 npm/pip/go/docker/cargo 等工具在国内下载慢、超时的问题。
  支持 npm、yarn、pnpm、pip、Go (GOPROXY)、Docker、Cargo、Maven、Gradle、Homebrew 镜像源切换。
  Use when: 用户说"配置镜像源"、"npm太慢"、"docker pull超时"、"换国内源"、"mirror setup"、
  "开发环境配置"、"proxy setup for China"，或任何国内开发环境加速相关的需求。
---

# CN Dev Setup — 国内开发环境镜像源配置

解决国内开发者最大的痛点：下载慢、超时、连不上。一键切换到国内镜像源。

## 支持的工具

| 工具 | 镜像源 | 命令 |
|---|---|---|
| **npm/yarn/pnpm** | 淘宝 npmmirror | `npm config set registry https://registry.npmmirror.com` |
| **pip** | 清华 TUNA / 阿里云 | `pip config set global.index-url` |
| **Go (GOPROXY)** | 七牛 goproxy.cn | `go env -w GOPROXY=https://goproxy.cn,direct` |
| **Docker** | 多个可选（阿里云/中科大/Docker proxy） | 修改 daemon.json |
| **Cargo (Rust)** | 清华 TUNA / 中科大 | 修改 ~/.cargo/config.toml |
| **Maven** | 阿里云 maven | 修改 settings.xml |
| **Gradle** | 阿里云 maven | 修改 build.gradle |
| **Homebrew** | 清华 TUNA | 环境变量设置 |
| **Git** | 代理配置 | `git config --global http.proxy` |

## Quick Start

### 自动配置（推荐）

```bash
python <skill-dir>/scripts/setup_mirrors.py --all
```

一键配置所有已安装工具的镜像源。

### 按工具配置

```bash
python <skill-dir>/scripts/setup_mirrors.py npm pip go docker
```

只配置指定的工具。

### 查看当前状态

```bash
python <skill-dir>/scripts/setup_mirrors.py --status
```

检查每个工具当前使用的源，标注哪些还是国外源。

### 恢复默认源

```bash
python <skill-dir>/scripts/setup_mirrors.py --reset npm pip
```

恢复到官方默认源。

## 使用指南

### 交互模式

当用户说"配置镜像源"或"npm太慢"时：

1. 运行 `--status` 检查当前源配置
2. 列出需要切换的工具
3. 确认后执行切换
4. 验证切换结果

### Git 代理配置

如果用户有 HTTP 代理（如 clash/v2ray）：

```bash
# 全局代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 仅 GitHub 代理（推荐）
git config --global http.https://github.com.proxy http://127.0.0.1:7890
```

### Docker 镜像源

Docker daemon.json 位置：
- **Linux**: `/etc/docker/daemon.json`
- **macOS**: `~/.docker/daemon.json`
- **Windows**: `%USERPROFILE%\.docker\daemon.json` 或 Docker Desktop 设置

## 镜像源详情

见 `references/mirrors.md` 获取完整的镜像源列表、备选源和测速方法。

## 故障排查

| 问题 | 原因 | 解决方案 |
|---|---|---|
| npm install 仍然慢 | 缓存了旧源地址 | `npm cache clean --force` 后重试 |
| pip 提示证书错误 | 公司网络 MITM | 加 `--trusted-host pypi.tuna.tsinghua.edu.cn` |
| docker pull 超时 | daemon.json 格式错误 | 检查 JSON 格式，重启 Docker 服务 |
| go mod download 失败 | GONOSUMDB 未设置 | `go env -w GONOSUMDB=*` 跳过校验 |
| Cargo 编译慢 | crates.io 索引大 | 用 sparse 协议：`sparse+https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/` |
| Maven 仍用中央仓库 | settings.xml 位置不对 | 确认文件在 `~/.m2/settings.xml` |
| 切换后部分包仍慢 | 镜像同步延迟 | 等几小时或换备选源 |
| 恢复默认源后异常 | 缓存残留 | 清除对应工具缓存目录 |
