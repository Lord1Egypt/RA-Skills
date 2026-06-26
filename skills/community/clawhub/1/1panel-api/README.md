# 1Panel API Skills

🎯 **OpenClaw Skill - 1Panel 服务器管理面板 API 接口文档**

[English](./README_en.md) | 中文

## 简介

本 Skill 提供 1Panel 开源服务器管理面板的完整 API 接口文档，包含 **23+ 个模块**，**500+ 个 API 接口**。

## 1Panel 是什么？

[1Panel](https://1panel.cn/) 是一个现代化、开源的 Linux 服务器运维管理面板，由 Go + Gin + Vue 开发。

## 功能特性

- 🌐 **网站管理** - 创建网站、配置 Nginx、反向代理、SSL 证书
- 🐳 **容器管理** - Docker 容器、镜像、网络、卷管理
- 💾 **数据库** - MySQL、PostgreSQL、Redis、MongoDB
- 📁 **文件管理** - 上传、下载、压缩、解压、在线编辑
- ⏰ **定时任务** - 备份、清理、脚本执行
- 📊 **系统监控** - CPU、内存、磁盘、网络监控
- 🔒 **安全防护** - 防火墙 Fail2ban ClamAV

## 快速开始

### 1. 安装 Skill

```bash
# 方式一：从 ClawHub 安装
openclaw skill install 1panel-api

# 方式二：手动复制到 skills 目录
cp -r 1Panel-Skills ~/.openclaw/workspace/skills/
```

### 2. 配置连接

首次使用需要配置 1Panel 服务器连接信息：

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| 面板地址 | 1Panel 面板访问地址 | 浏览器访问你的服务器 IP:8888 |
| API Key | 接口访问密钥 | 面板 → 设置 → API 密钥 → 创建 |

### 3. 开始使用

```bash
# 示例：获取容器列表
# 具体 API 调用请参考各模块文档
```

## 模块列表

| 模块 | 文件 | 说明 |
|------|------|------|
| AI | [SKILL-ai.md](./docs/SKILL-ai.md) | Ollama、MCP Server、TensorRT LLM |
| Apps | [SKILL-apps.md](./docs/SKILL-apps.md) | 应用商店、已安装应用 |
| Auth | [SKILL-auth.md](./docs/SKILL-auth.md) | 登录认证、验证码、MFA |
| Backups | [SKILL-backups.md](./docs/SKILL-backups.md) | 备份与恢复 |
| Containers | [SKILL-containers.md](./docs/SKILL-containers.md) | Docker 容器管理 |
| Cronjobs | [SKILL-cronjobs.md](./docs/SKILL-cronjobs.md) | 定时任务 |
| Dashboard | [SKILL-dashboard.md](./docs/SKILL-dashboard.md) | 系统仪表盘 |
| Databases | [SKILL-databases.md](./docs/SKILL-databases.md) | 数据库管理 |
| Files | [SKILL-files.md](./docs/SKILL-files.md) | 文件管理 |
| Groups | [SKILL-groups.md](./docs/SKILL-groups.md) | 分组管理 |
| Hosts | [SKILL-hosts.md](./docs/SKILL-hosts.md) | 主机监控、防火墙、SSH |
| Logs | [SKILL-logs.md](./docs/SKILL-logs.md) | 日志管理 |
| OpenResty | [SKILL-openresty.md](./docs/SKILL-openresty.md) | OpenResty 管理 |
| Process | [SKILL-process.md](./docs/SKILL-process.md) | 进程管理 |
| Runtimes | [SKILL-runtimes.md](./docs/SKILL-runtimes.md) | 运行环境 |
| Script | [SKILL-script.md](./docs/SKILL-script.md) | 脚本库 |
| Settings | [SKILL-settings.md](./docs/SKILL-settings.md) | 系统设置 |
| Toolbox | [SKILL-toolbox.md](./docs/SKILL-toolbox.md) | 工具箱 |
| Websites | [SKILL-websites.md](./docs/SKILL-websites.md) | 网站管理 |
| Websites SSL | [SKILL-websites_ssl.md](./docs/SKILL-websites_ssl.md) | SSL 证书 |
| Websites CA | [SKILL-websites_ca.md](./docs/SKILL-websites_ca.md) | 自建 CA |
| Websites ACME | [SKILL-websites_acme.md](./docs/SKILL-websites_acme.md) | ACME 账户 |
| Websites DNS | [SKILL-websites_dns.md](./docs/SKILL-websites_dns.md) | DNS 账户 |

## 认证方式

### 请求头

| Header | 说明 | 示例 |
|--------|------|------|
| 1Panel-Token | 认证 Token | `md5("1panel" + APIKey + Timestamp)` |
| 1Panel-Timestamp | Unix 时间戳 | `1709548800` |
| Content-Type | 请求类型 | `application/json` |

### Token 计算

```bash
# Shell 计算方式
api_key="你的API密钥"
timestamp=$(date +%s)
token=$(echo -n "1panel${api_key}${timestamp}" | openssl md5 | awk '{print $2}')

# Python 计算方式
import hashlib
token = hashlib.md5(f"1panel{api_key}{timestamp}".encode()).hexdigest()
```

### 请求示例

```bash
# 获取容器列表
curl -X GET "http://192.168.1.100:8888/api/v2/containers/list" \
  -H "1Panel-Token: your_token" \
  -H "1Panel-Timestamp: 1709548800" \
  -H "Content-Type: application/json"

# 创建网站
curl -X POST "http://192.168.1.100:8888/api/v2/websites" \
  -H "1Panel-Token: your_token" \
  -H "1Panel-Timestamp: 1709548800" \
  -H "Content-Type: application/json" \
  -d '{"type":"static","alias":"mywebsite","websiteGroupID":1}'
```

## 文件路径说明

1Panel 各类文件的存储路径：

| 类型 | 路径 |
|------|------|
| 网站根目录 | `/opt/1panel/www/sites/{网站名}/index` |
| 应用目录 | `/opt/1panel/apps/{应用Key}/{应用名}` |
| 备份目录 | `/opt/1panel/backup/` |
| 日志目录 | `/opt/1panel/logs/` |
| 数据库 | `/opt/1panel/mysql/{数据库名}` |

## 常见问题

### Q: 如何获取 API Key？
A: 登录 1Panel → 设置 → API 密钥 → 创建新密钥

### Q: API 请求失败怎么办？
A: 检查以下几点：
1. 面板地址是否正确
2. API Key 是否有效
3. 时间戳是否与服务器同步
4. Token 计算是否正确

### Q: 支持 HTTPS 吗？
A: 支持，只需将地址改为 `https://` 开头

### Q: 可以管理多台服务器吗？
A: 当前 Skill 配置单服务器，如需管理多台，可以配置多个 Skill 实例

## 源码结构

```
1Panel-Skills/
├── SKILL.md              # Skill 入口文件
├── README.md             # 本文档
├── INDEX.md              # 模块索引（可选）
└── docs/                 # 详细 API 文档
    ├── SKILL-ai.md
    ├── SKILL-apps.md
    ├── SKILL-containers.md
    └── ...
```

## 相关链接

- 🌐 [1Panel 官网](https://1panel.cn/)
- 📚 [1Panel 文档](https://1panel.cn/docs/)
- 💻 [GitHub](https://github.com/1Panel-dev/1Panel)
- 🐳 [Docker Hub](https://hub.docker.com/r/1panel/1panel)

## 贡献

欢迎提交 Issue 和 PR！

## License

本项目基于 MIT License。
