# FBox CLI 技能

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/flexem/fbox-skills)

通过命令行工具 `fboxcli` 为 Claude Code 提供 FBox 工业物联网设备管理能力，适合自动化脚本和批量运维场景。

## 功能特性

- 📊 **设备管理** - 列出、添加、删除、重命名 FBox 设备
- 📁 **分组管理** - 创建、重命名、删除设备分组
- 📈 **监控点读写** - 列出、读取、写入、删除监控点，管理数据推送
- 🚨 **报警管理** - 查看报警条目和历史，确认报警，管理报警分组
- 👤 **联系人管理** - 添加、更新、删除报警联系人
- 📉 **历史数据** - 查询历史采集数据，支持多粒度聚合
- 🔧 **设备驱动** - 查看 PLC 设备列表、支持的驱动和寄存器
- 🎛️ **统一写组** - 管理和执行跨设备批量写入
- 📍 **地理位置** - 查询设备地理位置信息
- 🔐 **认证管理** - 支持开发者模式和用户模式登录

## 前置条件

- `fboxcli` 已安装并在系统 PATH 中（[安装指南](INSTALL.md)）
- FBox 平台账号（开发者凭证或用户账号）

## 快速开始

```bash
# 配置并登录（开发者模式）
fboxcli config set --server https://openapi.fbox360.com \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
fboxcli auth login

# 或使用用户模式登录
fboxcli auth login -u user@example.com -p password

# 查看设备
fboxcli box list

# 读取监控点
fboxcli dmon get-value 12345 --ids 1001,1002 --json

# 查询历史数据
fboxcli history query --ids 2001 --begin 1700000000000 --end 1700086400000 --json
```

## 文档

- [安装指南](INSTALL.md) - fboxcli 安装和技能安装步骤
- [技能说明](SKILL.md) - 完整的技能配置和使用规则
- [设备管理](references/device-management.md) - box / group / device / location 命令参考
- [监控点](references/monitoring.md) - dmon 命令参考
- [报警管理](references/alarm-management.md) - alarm / contact 命令参考
- [历史数据](references/historical-data.md) - history 命令参考
- [统一写组](references/control.md) - control 命令参考

## 技术信息

- **工具类型**: 本地 CLI（Rust 编译的二进制文件）
- **API 端点**: `https://openapi.fbox360.com`
- **命令数量**: 11 个模块，40+ 个子命令
- **输出格式**: 表格（默认）/ JSON（`--json` 标志）
- **认证方式**: OAuth2 client_credentials 或 password grant，Token 自动管理

## 许可证

MIT License

## 联系方式

- 官网: [https://fbox360.com](https://fbox360.com)
- 作者: flexem
- 问题反馈: [GitHub Issues](https://github.com/flexem/fbox-skills/issues)
