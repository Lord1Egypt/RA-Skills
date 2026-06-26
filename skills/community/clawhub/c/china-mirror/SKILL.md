---
name: china-mirror
description: "国内镜像源加速。生成下载/安装命令时自动添加大厂/高校背书的可信镜像参数。"
version: 3.0.0
---

# China Mirror — 国内镜像源

## 核心规则
1. **任何可能触发网络下载的命令**，自动添加国内镜像参数                                                                
2. **只使用以下镜像源**，禁止使用无背书的不明镜像  

示例：
- 用户："安装 lodash" → 生成：`npm install lodash --registry=https://registry.npmmirror.com`
- 用户："pip 安装 requests" → 生成：`pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple`

## 可信镜像源（大厂/高校背书）

### 命令行参数

| 工具 | 参数 | 镜像 | 背书方 |
|------|------|------|--------|
| npm/pnpm/yarn/bun | `--registry=https://registry.npmmirror.com` | 淘宝 | 阿里巴巴 ✅ |
| pip/pip3/uv/poetry | `-i https://pypi.tuna.tsinghua.edu.cn/simple` | 清华 | 清华大学 ✅ |
| conda/mamba | `-c https://mirrors.tuna.tsinghua.edu.cn/anaconda` | 清华 | 清华大学 ✅ |
| gem/bundle | `--source https://mirrors.tuna.tsinghua.edu.cn/rubygems/` | 清华 | 清华大学 ✅ |
| flutter pub/dart pub | `--server=https://pub.flutter-io.cn` | Flutter CN | 社区 ✅ |
| composer | `--repository-url=https://mirrors.aliyun.com/composer/` | 阿里云 | 阿里云 ✅ |
| nuget/dotnet | `--source https://repo.huaweicloud.com/repository/nuget/v3/index.json` | 华为云 | 华为云 ✅ |

### 环境变量配置

| 工具 | 环境变量 | 值 |
|------|----------|-----|
| cargo | `CARGO_REGISTRY` | 配置 `~/.cargo/config.toml` |
| rustup | `RUSTUP_DIST_SERVER` | `https://mirrors.ustc.edu.cn/rust-static` |
| go | `GOPROXY` | `https://goproxy.cn,direct` |
| docker | `registry-mirrors` | 配置 `daemon.json` |
| brew | `HOMEBREW_*` | 清华镜像环境变量 |
| pyenv | `PYTHON_BUILD_MIRROR_URL` | `https://mirrors.tuna.tsinghua.edu.cn/python-build/` |
| nvm | `NVM_NODEJS_ORG_MIRROR` | `https://npmmirror.com/mirrors/node/` |
| fnm/volta | `*_MIRROR` | `https://npmmirror.com/mirrors/node/` |
| rbenv | `RUBY_BUILD_MIRROR_URL` | `https://mirrors.tuna.tsinghua.edu.cn/ruby-build/` |
| gvm | `GO_BINARY_BASE_URL` | `https://mirrors.ustc.edu.cn/golang/` |
| sdkman | `sdkman_candidates_mirror` | `https://mirrors.tuna.tsinghua.edu.cn/sdkman/` |
| tfenv | `TFENV_TERRAFORM_MIRROR` | `https://mirrors.tuna.tsinghua.edu.cn/terraform/` |
| asdf | `ASDF_*_MIRROR` | 参考上述各语言镜像 |
| julia | `JULIA_PKG_SERVER` | `https://mirrors.ustc.edu.cn/julia/` |
| R | `options(repos)` | `https://mirrors.tuna.tsinghua.edu.cn/CRAN/` |
| maven/gradle | 配置文件 | `https://maven.aliyun.com/repository/public` |
| helm | `helm repo add` | `https://mirror.azure.cn/kubernetes/charts/` |

### 系统包管理器

| 系统 | 镜像源 | 背书方 |
|------|--------|--------|
| Ubuntu/Debian | `mirrors.aliyun.com` | 阿里云 ✅ |
| CentOS/RHEL | `mirrors.aliyun.com` | 阿里云 ✅ |
| Alpine | `mirrors.aliyun.com/alpine/` | 阿里云 ✅ |
| Arch | `mirrors.tuna.tsinghua.edu.cn/archlinux/` | 清华 ✅ |

## 备选镜像

| 工具 | 备选 | 背书方 |
|------|------|--------|
| npm | `https://repo.huaweicloud.com/repository/npm/` | 华为云 ✅ |
| pip | `https://mirrors.aliyun.com/pypi/simple/` | 阿里云 ✅ |
| pip | `https://pypi.mirrors.ustc.edu.cn/simple/` | 中科大 ✅ |
| cargo | `https://rsproxy.cn/` | 字节跳动 ✅ |
| go | `https://mirrors.aliyun.com/goproxy/` | 阿里云 ✅ |
| docker | `https://mirror.ccs.tencentyun.com` | 腾讯云 ✅ |

## 判断逻辑

AI 生成命令时，自动判断：

### 1. 是否涉及网络下载？

**直接下载命令：**
- 包安装：`npm install`, `pip install`, `gem install`, `composer require`...
- 版本安装：`pyenv install`, `nvm install`, `rustup toolchain install`...
- 镜像拉取：`docker pull`, `docker build`...
- 仓库克隆：`git clone`（GitHub 可提示使用代理）
- 系统更新：`apt install`, `brew install`, `apk add`...

**间接触发下载的命令：**
- `npm run` / `yarn run` / `pnpm run` — 依赖缺失时自动下载
- `npm test` / `npm start` / `npm build` — 同上
- `npx <package>` — 临时下载执行
- `uv run` — 自动安装依赖
- `cargo build` / `cargo run` — 首次构建下载依赖
- `go build` / `go run` — 下载模块依赖

**判断原则：**
- 如果命令可能触发网络请求，且环境未配置镜像 → 提示配置镜像
- 如果用户已配置镜像环境变量 → 正常执行

### 2. 如何添加镜像？

**支持命令行参数：**
```
npm install pkg --registry=https://registry.npmmirror.com
pip install pkg -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**不支持命令行参数：**
- 提示用户配置环境变量（如 `GOPROXY`, `NVM_NODEJS_ORG_MIRROR`）
- 或在命令前临时设置：`NVM_NODEJS_ORG_MIRROR=https://npmmirror.com/mirrors/node/ nvm install 20`

### 3. 跳过情况

- 命令中已有镜像参数 → 跳过
- 用户明确指定其他源 → 跳过
- 纯本地命令（无网络请求）→ 跳过

## 安全声明

**背书方：**
- 大厂：阿里巴巴、华为云、腾讯云、字节跳动、网易、七牛云
- 高校：清华大学、中国科学技术大学

**禁止使用无背书的不明镜像源。**
