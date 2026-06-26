# FBox MCP Server 技能

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.4-green.svg)](https://github.com/flexem/fbox-skills)

通过 Model Context Protocol (MCP) 为 Claude Code 和 OpenClaw 提供 FBox 工业物联网设备管理能力。

## 功能特性

- 📊 **设备管理** - 查看设备在线状态、统计信息、系统配置
- 📈 **监控点读写** - 实时读取和写入 PLC 监控点数据
- 🚨 **报警处理** - 查看当前报警、确认报警、查询报警历史
- 📉 **历史数据** - 查询历史采集数据趋势和聚合统计
- 🖥️ **远程控制** - 打开设备 VNC 远程监控画面
- 📡 **物联网卡** - 查看 SIM 卡流量和运营商信息

## 快速开始

### 安装

详细安装步骤请参考 [INSTALL.md](INSTALL.md)。

**快速安装（Claude Code）：**

```bash
# 设置 API Key
export FBOXMCP_API_KEY=sk-xxxxxx

# 添加 MCP Server
claude mcp add --transport http fboxmcp https://fboxmcp.fbox360.com --header "Authorization: Bearer ${FBOXMCP_API_KEY}"

# 安装插件
claude plugin marketplace add https://github.com/flexem/fbox-skills
claude plugin install fboxmcp
```

### 使用示例
 
在 Claude Code 或 OpenClaw 对话中直接描述需求：

```
查看所有在线设备
显示设备"生产线1"的温度监控点
查询最近24小时的温度历史数据
确认设备报警
打开设备远程监控画面
```

## 文档

- [安装指南](INSTALL.md) - Claude Code 和 OpenClaw 安装步骤
- [技能说明](SKILL.md) - 完整的技能配置和使用规则
- [设备管理](references/device-management.md) - 设备相关工具参考
- [监控点](references/monitoring.md) - 监控点读写工具参考
- [报警管理](references/alarm-management.md) - 报警处理工具参考
- [历史数据](references/historical-data.md) - 历史数据查询工具参考

## 认证方式

支持两种认证方式：

| 方式 | 格式 | 说明 |
|------|------|------|
| API Key（推荐） | `Bearer sk-xxxxxx` | 长期有效 |
| JWT Token | `Bearer eyJhbGci...` | OAuth2 JWT，需自行管理续期 |

获取 API Key 请联系 FBox 平台管理员。

## 技术架构

- **传输协议**: Streamable HTTP
- **端点地址**: `https://fboxmcp.fbox360.com`
- **工具数量**: 20 个（设备管理 7 个、监控点 5 个、报警 4 个、历史数据 2 个、远程控制 1 个、系统工具 1 个）
- **时区处理**: 服务端 UTC，展示时自动转换为北京时间（UTC+8）

## 许可证

MIT License

## 联系方式

- 官网: [https://fbox360.com](https://fbox360.com)
- 作者: flexem
- 问题反馈: [GitHub Issues](https://github.com/flexem/fbox-skills/issues)
