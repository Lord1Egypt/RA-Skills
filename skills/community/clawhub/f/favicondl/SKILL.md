---
name: favicondl
displayName: 任意网站 Favicon 下载工具 · FaviconDL
description: "通过命令行下载任意网站 favicon，支持多种尺寸与格式，无依赖。Using favicondl.com API to download favicon for any domain via CLI."
version: 1.0.0
---

# FaviconDL

> 通过命令行下载任意网站 favicon / Download favicon for any domain via CLI

---

## 简介 / Overview

FaviconDL 是一款基于 [favicondl.com](https://favicondl.com) API 的命令行工具，可一键下载任意网站的高质量 favicon 图标。支持自定义尺寸、多种格式，并提供 PowerShell 与 Bash 双版本，零依赖即可使用。

FaviconDL is a lightweight CLI tool powered by [favicondl.com](https://favicondl.com) API. Download high-quality favicon images for any domain in any supported size — no API key required.

---

## 功能 / Features

| 功能 Feature | 说明 Description |
|------------|-----------------|
| 多尺寸支持 Multi-size | 支持 16 / 32 / 48 / 64 / 128 / 256 / 512 px |
| 302 重定向 redirect | 自动跟随重定向，直接下载 PNG 文件 |
| 无依赖 Zero dependency | 仅需 curl（PowerShell 内置或系统自带） |
| 双端支持 Cross-platform | PowerShell (Windows) + Bash (Linux/macOS) |
| 批量下载 Batch | 支持多域名连续下载 |

---

## 安装 / Installation

### Windows（PowerShell）

```powershell
# 下载脚本到本地
curl -L -o "$env:USERPROFILE\favicondl.ps1" "https://raw.githubusercontent.com/sweesama/favicondl.com/main/favicondl.ps1"

# 添加到 PATH（可选）
# 将 $env:USERPROFILE 加入系统 PATH 环境变量
```

### Linux / macOS（Bash）

```bash
curl -L -o ~/favicondl.sh "https://raw.githubusercontent.com/sweesama/favicondl.com/main/favicondl.sh"
chmod +x ~/favicondl.sh
sudo ln -s ~/favicondl.sh /usr/local/bin/favicondl
```

---

## 使用方法 / Usage

### 基本语法 / Syntax

```bash
# PowerShell
.\favicondl.ps1 -Domain <域名> [-Size <尺寸>] [-Output <保存路径>]

# Bash
./favicondl.sh <域名> [尺寸] [保存路径]
```

### 参数说明 / Parameters

| 参数 Parameter | 必填 Required | 默认值 Default | 说明 Description |
|--------------|-------------|--------------|----------------|
| `-Domain` / `<域名>` | ✅ | — | 目标网站域名，如 `github.com` |
| `-Size` / `[尺寸]` | ❌ | `128` | 图片尺寸，可选 16/32/48/64/128/256/512 |
| `-Output` / `[路径]` | ❌ | `./favicon.png` | 保存文件路径 |

### 示例 / Examples

```powershell
# 下载 GitHub 128px favicon（默认尺寸）
.\favicondl.ps1 -Domain "github.com"

# 下载 256px 大图
.\favicondl.ps1 -Domain "github.com" -Size 256

# 保存到指定路径
.\favicondl.ps1 -Domain "github.com" -Size 128 -Output "C:\icons\gh.png"

# 批量下载多个域名
.\favicondl.ps1 -Domain "github.com"
.\favicondl.ps1 -Domain "openai.com"
.\favicondl.ps1 -Domain "anthropic.com"
```

```bash
# 下载 GitHub favicon
./favicondl.sh github.com

# 下载 256px 版本
./favicondl.sh github.com 256

# 保存到指定路径
./favicondl.sh github.com 128 ./icons/gh.png
```

---

## 输出示例 / Output Example

```
Fetching favicon for github.com at 128px...
Saved: ./github_favicon.png (6518 bytes) ✅
```

---

## API 详情 / API Details

本工具调用 `favicondl.com` 提供的免费 API，无需注册、无需 API Key。

Under the hood, this tool calls the free `favicondl.com` API — no registration, no API key required.

### 端点 / Endpoint

```
GET https://favicondl.com/api/favicon?domain={domain}&size={size}&format=redirect
```

### 参数 / Parameters

| 参数 | 类型 | 说明 |
|------|------|------|
| `domain` | string | 目标域名，如 `github.com` |
| `size` | integer | 图片像素尺寸，可选 16/32/48/64/128/256/512 |
| `format=redirect` | string | 返回 302 重定向到实际 PNG 文件 |

### 响应 / Response

- **状态码 Status**: `302 Found`
- **Location**: 目标网站 favicon URL
- **最终内容**: PNG 图片文件

---

## 适用场景 / Use Cases

| 场景 Scenario | 说明 Description |
|-------------|-----------------|
| 🌍 GEO 外链提交 | 为目录站提交准备网站 logo |
| 🎨 设计素材采集 | 快速获取竞品或参考网站的图标资源 |
| 🔍 SEO / 书签 | 为书签页面、导航页批量获取网站图标 |
| 📱 App Icon 备选 | 快速预览主流网站的品牌图标设计 |
| 🤖 AI Agent 工作流 | 集成进自动化脚本，定向抓取网站图标 |

---

## 错误处理 / Error Handling

| 错误类型 Error | 原因 Cause | 解决方案 Solution |
|--------------|-----------|-----------------|
| `HTTP 404` | 目标网站无 favicon | 换用 Google Favicon 备选方案 |
| `HTTP 5xx` | API 服务端异常 | 稍后重试或检查网络连接 |
| 文件写入失败 | 路径无权限或磁盘满 | 更换输出路径或以管理员运行 |

---

## 相关项目 / Related Projects

| 项目 Project | 地址 Link |
|------------|----------|
| 🌐 FaviconDL 官网 | https://favicondl.com |
| 📦 NPM 版本 | https://www.npmjs.com/package/favicondl |
| 💻 源码仓库 | https://github.com/sweesama/favicondl.com |
| 🐟 水产市场发布 | https://openclawmp.cc/asset/s-5a9fb4e7ff343062 |

---

## 更新日志 / Changelog

### v1.0.0
- 首发版本 / Initial release
- 支持 PowerShell + Bash 双端
- 支持 7 种尺寸（16-512px）
- 302 重定向自动下载 PNG
