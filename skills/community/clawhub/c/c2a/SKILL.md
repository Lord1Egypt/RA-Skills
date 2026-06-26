---
name: appstore-skill
description: 应用商店管理 Skill。当用户想要搜索、安装、卸载或查看已安装应用时使用此 Skill。
---

# App Store Skill

## 概述

此 Skill 提供应用商店管理功能，用户可以通过自然语言对话来：

- **搜索应用商店** - "搜索 Redis"、"查找数据库应用"
- **查看应用详情** - "查看 Redis 详情"、"Redis 有什么版本"
- **查看已安装应用** - "我安装了哪些应用"、"列出所有应用"
- **安装应用** - "帮我安装 MySQL"、"安装应用 nginx"
- **卸载应用** - "卸载 MySQL"、"删除应用 wordpress"

## 配置要求

### 首次使用（推荐方式）

在首次使用时，通过对话设置配置（会自动保存到 Gateway 配置文件，后续对话会自动使用）：

```
用户: 设置 1Panel 配置
       地址：http://your-server:port
       密钥：your-api-key-here
AI: [调用 gateway 配置保存] 配置已保存到 Gateway！
    后续所有对话都会自动使用此配置，无需重复输入。
```

配置会保存到 `openclaw.json` 文件中的 `skills.entries.appstore-skill.config` 路径下。

### 环境变量（备用方式）

如果需要通过环境变量配置，可以使用：

| 变量 | 说明 | 示例 |
|------|------|------|
| `ONEPANEL_BASE_URL` | 1Panel 服务器地址 | `http://your-server:port` |
| `ONEPANEL_API_KEY` | 1Panel API 认证密钥 | `your-api-key-here` |
| `ONEPANEL_TIMEOUT_MS` | 请求超时时间（可选） | `30000` |

> 注：同时也支持 `APPSTORE_*` 环境变量以保持向后兼容
> **推荐使用对话配置方式**，配置会持久化保存，新对话无需重复输入。

## 工作流程

### 搜索应用

1. 用户发起搜索请求
2. 调用 `searchApps` 工具
3. 返回匹配的应用列表（包含名称、描述、是否已安装）

### 查看应用详情

1. 用户请求查看应用详情
2. 调用 `getAppByKey` 获取应用信息
3. 返回应用详情（包含可用版本列表）

### 安装应用

1. 用户请求安装应用
2. 调用 `getAppByKey` 获取应用信息和可用版本
3. 调用 `getAppDetailId` 获取 `appDetailId`（安装必需参数）
4. 调用 `installApp` 执行安装

### 卸载应用

1. 用户请求卸载应用
2. 调用 `listInstalledApps` 获取已安装应用列表
3. 找到目标应用的 `installId`
4. 调用 `uninstallApp` 执行卸载

### 查看已安装应用

1. 用户请求查看已安装应用
2. 调用 `listInstalledApps` 工具
3. 返回所有已安装应用的列表

## 配置示例

```
用户: 设置 1Panel 配置
       地址：http://your-server:port
       密钥：your-api-key-here
       超时：30秒
AI: [保存配置到 Gateway] 配置已保存到 openclaw.json！
    您的 1Panel 服务器地址和密钥已持久化保存。
    后续对话会自动使用此配置，无需重复输入。

用户: 验证一下配置
AI: [调用 search_apps] 测试连接成功，配置有效。
```

## 技术说明

配置读取优先级：
1. **Gateway 配置** (`skills.entries.appstore-skill.config`) - 优先级最高
2. **环境变量** (`ONEPANEL_*` 或 `APPSTORE_*`)
3. **参数直接传递**

## 对话示例

```
用户: 帮我看看安装了哪些应用
AI: [调用 listInstalledApps] 您已安装以下应用：
    - MySQL (ID: 62)
    - WordPress (ID: 63)
    - Hermes Agent (ID: 37)

用户: 搜索一下 Redis
AI: [调用 searchApps] 找到 Redis 应用：
    - Redis: 高性能开源键值数据库
    是否需要查看详情或安装？

用户: Redis 有什么版本？
AI: [调用 getAppByKey] Redis 可用版本：
    - 8.6.2 (最新)
    - 7.4.8
    - 6.2.21

用户: 帮我安装 Redis
AI: [执行安装流程] 正在安装 Redis（版本 8.6.2）...
    安装完成！实例名称: redis
```

## CLI 使用方式

```bash
# 搜索应用
APPSTORE_BASE_URL=http://... APPSTORE_API_KEY=... node dist/cli.js search redis

# 查看应用详情
node dist/cli.js info redis

# 安装应用（默认最新版本）
node dist/cli.js install redis my-redis

# 安装指定版本
node dist/cli.js install redis my-redis 7.4.8

# 列出已安装应用
node dist/cli.js list

# 卸载应用
node dist/cli.js uninstall 67
```

## 注意事项

- 安装应用时，如果不指定版本，默认使用最新版本
- 安装应用时可以指定自定义实例名称，方便区分多个相同应用
- 某些应用可能需要额外的安装参数，会提示用户输入
- 卸载应用需要使用 installId，可以从已安装列表中获取
