---
name: awi
version: 0.1.0
description: |
  AWI (Agentic Web Interface) — 联网读取+搜索，单二进制零配置。
  三级自动降级：直连 → 智能适配 → 浏览器渲染。
  不需要 API Key，不需要 Docker。
homepage: https://github.com/jzOcb/awi
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["awi"]
    install:
      - id: awi-binary
        kind: script
        script: scripts/install.sh
        bins: ["awi"]
        label: "Install AWI binary from GitHub releases"
allowed-tools:
  - exec
---

# AWI — Agentic Web Interface

单二进制零配置的联网工具。读取网页内容 + DuckDuckGo 搜索。

## 安装

```bash
# 自动安装（检测系统和架构）
bash ~/clawd/skills/awi/scripts/install.sh

# 或手动下载
# macOS ARM: https://github.com/jzOcb/awi/releases/download/v0.1.0/awi-darwin-arm64
# macOS Intel: https://github.com/jzOcb/awi/releases/download/v0.1.0/awi-darwin-amd64
# Linux: https://github.com/jzOcb/awi/releases/download/v0.1.0/awi-linux-amd64
```

## 用法

### 读取网页
```bash
awi read "https://example.com/article"
```

### 搜索
```bash
awi search "AI agent frameworks"
```

### 批量读取
```bash
awi batch urls.txt
```

## 参数

| 参数 | 说明 |
|------|------|
| `--backend direct\|stealth\|browser` | 指定后端，默认自动降级 |
| `--format json\|markdown\|text` | 输出格式 |
| `--timeout 30s` | 超时时间 |
| `--proxy http://...` | 代理 |
| `--no-cache` | 禁用缓存 |

## 降级策略

1. **direct** — 直接 HTTP 请求，最快
2. **stealth** — 智能适配，绕过基础反爬
3. **browser** — 无头浏览器渲染，处理 JS 页面

大部分链接第一级就搞定，碰到反爬的自动升级，不需要手动干预。
