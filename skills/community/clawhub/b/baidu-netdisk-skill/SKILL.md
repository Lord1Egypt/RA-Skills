---
name: baidu-netdisk-skill
description: Baidu Netdisk file management for OpenClaw - List, search, download, upload with OAuth 2.0 (百度网盘文件管理 - OAuth 一键授权)
---

# 百度网盘 Skill (Baidu Netdisk Skill)

> AI Agent 的云端数据连接器 | Cloud Data Connector for AI Agents —— 无需本地存储即可访问百度网盘文件

**安全状态**：✅ 已自审 | 🔒 Token 加密存储 | 🌐 仅调用百度官方 API

## 简介

百度网盘 Skill 是一个专为 OpenClaw 设计的命令行工具，支持文件列表、搜索、下载、上传等核心功能。

**核心优势**：
- 🔐 **OAuth 一键授权** - 1 分钟完成，无需申请百度 API（推荐）
- ☁️ **云端零存储** - 流式读取，不占用本地磁盘空间
- 🗂️ **深层文件夹遍历** - 支持 4 层 + 深度目录
- 🔒 **Token 加密存储** - 本地安全
- 🔧 **灵活认证** - 支持自带 API key（适合高用量用户）

## 安装

```bash
npx skills install github:niukesi/baidu-netdisk-skill
```

## 授权（首次使用）

### 方式一：OAuth 一键授权 ⭐ 推荐

适合大多数用户，无需申请百度 API：

```bash
npx baidu-netdisk-auth
```

按提示操作：
1. 打开授权 URL
2. 登录百度账号
3. 授权应用
4. 复制授权码粘贴回终端

### 方式二：自带 API key 🔧 高级

适合高用量用户或技术用户，使用自己的百度 API 配额：

```bash
npx baidu-netdisk-skill config -k <apikey> -s <secret> -t <token>
```

**获取 API key 步骤：**
1. 访问 [百度开放平台](https://pan.baidu.com/union/console)
2. 创建应用获取 API Key 和 Secret Key
3. 按提示完成授权获取 Access Token

## 使用示例

### 查看用户信息
```bash
npx baidu-netdisk-skill whoami
```

### 列出文件
```bash
# 根目录
npx baidu-netdisk-skill list /

# 指定目录（支持深层文件夹）
npx baidu-netdisk-skill list "/教程/第一层/第二层"
```

### 搜索文件
```bash
npx baidu-netdisk-skill search "关键词"
```

### 获取下载链接
```bash
npx baidu-netdisk-skill download <fs_id>
```

### 上传文件
```bash
npx baidu-netdisk-skill upload ./本地文件.pdf /备份/
```

## 配置项

| 配置项 | 说明 | 必填 |
|--------|------|------|
| `apiKey` | 百度 API Key（自带 API key 模式使用） | 否 |
| `secretKey` | 百度 Secret Key（自带 API key 模式使用） | 否 |
| `accessToken` | Access Token（OAuth 授权后自动保存） | 否 |
| `refreshToken` | Refresh Token（OAuth 授权后自动保存） | 否 |
| `encryptionKey` | 自定义加密密钥（可选，增强安全性） | 否 |

## 安全说明

- ✅ Token 本地加密存储（AES-256）
- ✅ 仅调用百度官方 API
- ✅ 代码开源可审计
- ✅ 无数据收集

**注意**：删除操作不可恢复，请谨慎使用。

## 常见问题

**Q: 授权后提示凭证无效？**
A: 授权码有效期较短，请在 5 分钟内完成授权。如已过期，重新运行 `npx baidu-netdisk-auth`。

**Q: 列出文件时提示权限不足？**
A: 请确认已正确完成 OAuth 授权，或检查 BDUSS/STOKEN 是否有效。

**Q: 支持大文件上传吗？**
A: 支持，但大文件上传时间较长，建议在稳定网络环境下使用。

## 更多文档

- [GitHub 仓库](https://github.com/niukesi/baidu-netdisk-skill)
- [完整 README](https://github.com/niukesi/baidu-netdisk-skill/blob/main/README.md)

---

**Made with ❤️ by Miaozai Studio**
