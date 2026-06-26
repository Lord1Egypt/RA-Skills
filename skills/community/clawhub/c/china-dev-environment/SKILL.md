---
name: china-dev-environment
description: "Configure development environments for Chinese developers. Teach AI agents how to set up mirrors, proxies, and alternative services for npm/pip/Docker/GitHub/Google that work behind the Great Firewall. Covers: npm/pip/Docker mirror configuration, GitHub acceleration, Google API replacement, VPN/proxy setup for dev tools, and China-friendly project templates. Triggers on: 中国开发者环境, china dev environment, npm镜像, npm mirror, pip镜像, pip mirror, Docker镜像, docker mirror china, GitHub加速, github acceleration, 国内开发环境, china development setup, 翻墙开发, GFW workaround, 中国npm, china npm registry, 开发者代理, developer proxy, 国内Docker, china docker registry"
---

# China Dev Environment - 中国开发者环境配置专家

You are an expert at configuring development environments that work reliably in China. You know every mirror, proxy, and alternative service that keeps Chinese developers productive behind the Great Firewall.

## Core Philosophy

**A developer in China who can't `npm install` is a developer who can't work.** Your job is to make every package manager, every registry, every cloud service work smoothly — without VPN if possible, with minimal VPN if not.

## Registry Mirrors

### npm (Node.js)
```bash
# Set China npm mirror (淘宝镜像)
npm config set registry https://registry.npmmirror.com

# Or use nrm to switch between mirrors
npm install -g nrm
nrm use taobao

# Verify
npm config get registry
# Should show: https://registry.npmmirror.com/

# For specific packages not on mirror
npm install package-name --registry=https://registry.npmjs.org
```

### pip (Python)
```bash
# Set Tsinghua PyPI mirror (most reliable)
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# Alternative mirrors
# Aliyun: https://mirrors.aliyun.com/pypi/simple/
# Douban: https://pypi.doubanio.com/simple/
# USTC: https://pypi.mirrors.ustc.edu.cn/simple/

# Temporary use
pip install package -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Docker
```bash
# Configure Docker mirror (daemon.json)
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me",
    "https://docker.m.daocloud.io"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

# Pull image through mirror
docker pull nginx  # Will use mirror automatically

# For images not on mirror, use proxy
# docker pull --platform linux/amd64 nginx
```

### Maven (Java)
```xml
<!-- settings.xml mirror configuration -->
<mirrors>
  <mirror>
    <id>aliyun</id>
    <mirrorOf>central</mirrorOf>
    <url>https://maven.aliyun.com/repository/central</url>
  </mirror>
</mirrors>
```

### Go
```bash
# Set Go module proxy
go env -w GOPROXY=https://goproxy.cn,direct
go env -w GONOSUMCHECK=gitlab.company.com

# Alternative: https://goproxy.io
```

### Rust / Cargo
```toml
# ~/.cargo/config.toml
[source.crates-io]
replace-with = "ustc"

[source.ustc]
registry = "sparse+https://mirrors.ustc.edu.cn/crates.io-index/"
```

## GitHub Acceleration

### Method 1: Mirror Sites
```bash
# Clone via mirror
git clone https://ghproxy.com/https://github.com/user/repo.git
git clone https://mirror.ghproxy.com/https://github.com/user/repo.git

# Or set URL rewrite
git config --global url."https://ghproxy.com/https://github.com/".insteadOf "https://github.com/"
```

### Method 2: SSH with Proxy
```bash
# ~/.ssh/config
Host github.com
  HostName github.com
  User git
  ProxyCommand nc -X 5 -x 127.0.0.1:1080 %h %p
```

### Method 3: Gitee Import
```bash
# Import to Gitee first, then clone from Gitee
# https://gitee.com/projects/import/url
```

### Method 4: GitHub Codespaces
```bash
# Use GitHub Codespaces (works from China)
gh codespace create -r owner/repo
gh codespace ssh
```

## Google API Replacements

| Google Service | China Replacement | Setup |
|---------------|-------------------|-------|
| Google Fonts | fonts.font.im | Replace `fonts.googleapis.com` → `fonts.font.im` |
| Google Analytics | Baidu Tongji | `hm.baidu.com/hm.js?xxx` |
| Google Maps | Amap/Gaode | `webapi.amap.com/maps?v=2.0` |
| reCAPTCHA | Tencent Captcha | `captcha.tencentcloudapi.com` |
| Firebase | Tencent CloudBase | `tcb-api.tencentcloudapi.com` |
| Google Search | Baidu SEO | Submit at `ziyuan.baidu.com` |
| Google Cloud Storage | COS/OSS | Use Tencent/Alibaba SDK |
| Gmail SMTP | Aliyun DirectMail | `dm.aliyuncs.com` |

## Workflow 1: New Project Bootstrap (China Edition)

```bash
#!/bin/bash
# china-project-init.sh — Bootstrap a new project that works in China

echo "🔧 Setting up China-friendly dev environment..."

# 1. Configure package managers
npm config set registry https://registry.npmmirror.com
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
go env -w GOPROXY=https://goproxy.cn,direct

# 2. Create .npmrc for project
cat > .npmrc << 'EOF'
registry=https://registry.npmmirror.com
# For packages that fail on mirror, fallback to official
# package-name:registry=https://registry.npmjs.org
EOF

# 3. Create .pip.conf for project
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << 'EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF

# 4. Docker mirror (if Docker installed)
if command -v docker &> /dev/null; then
  sudo mkdir -p /etc/docker
  sudo tee /etc/docker/daemon.json << 'DOCKER'
{
  "registry-mirrors": ["https://docker.1ms.run"]
}
DOCKER
  sudo systemctl restart docker
fi

# 5. Git config for GitHub acceleration
git config --global url."https://ghproxy.com/https://github.com/".insteadOf "https://github.com/"

echo "✅ China dev environment configured!"
```

## Workflow 2: Fix Broken Dependencies

When `npm install` or `pip install` fails in China:

```bash
# npm: Clear cache and retry with mirror
npm cache clean --force
rm -rf node_modules package-lock.json
npm install --registry=https://registry.npmmirror.com

# pip: Clear cache and retry
pip cache purge
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Docker: Pull with explicit mirror
docker pull registry.npmmirror.com/library/nginx:latest
docker tag registry.npmmirror.com/library/nginx:latest nginx:latest

# Go: Clear module cache
go clean -modcache
GOPROXY=https://goproxy.cn,direct go mod download
```

## Workflow 3: CI/CD Pipeline (China)

```yaml
# GitHub Actions with China mirrors
name: CI China
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Use China npm mirror
      - run: npm config set registry https://registry.npmmirror.com
      
      # Use China pip mirror
      - run: pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
      
      - run: npm ci
      - run: npm test
      
      # Deploy to China cloud
      - run: npx tccli scf UpdateFunctionCode ...
```

## Safety Rules

1. **Never commit proxy credentials** — use environment variables
2. **Mirror reliability** — npmmirror.com is backed by Alibaba, most reliable
3. **Security** — official mirrors are safe; unknown mirrors may inject code
4. **Sync delay** — mirrors may lag by minutes to hours; for latest packages, use official registry
5. **Binary packages** — native modules (node-gyp) may still fail; prebuild binaries often unavailable on mirrors
6. **Test without VPN** — always verify your setup works without VPN, as most Chinese devs don't have one

## Quick Reference

| Tool | Mirror | Official |
|------|--------|----------|
| npm | npmmirror.com | npmjs.org |
| pip | pypi.tuna.tsinghua.edu.cn | pypi.org |
| Docker | docker.1ms.run | hub.docker.com |
| Maven | maven.aliyun.com | repo1.maven.org |
| Go | goproxy.cn | proxy.golang.org |
| Rust | mirrors.ustc.edu.cn | crates.io |
| GitHub | ghproxy.com | github.com |
