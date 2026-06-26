---
name: fortigate-config
description: 自动配置 FortiGate 防火墙，支持基础策略管理及工控协议（Modbus、IEC104、S7等）的安全配置。
author: jiansiting
version: 2.0.0
tags: [fortigate, firewall, industrial, security, automation]
---

# FortiGate 自动配置技能（工控增强版）

## 功能说明
本技能通过 FortiGate REST API 实现防火墙的自动化配置，特别增加了对工业控制系统（ICS）协议的支持。您可以：

- 管理防火墙策略（增、删、改、查）
- 管理地址对象
- 配置 Industrial Connectivity（协议转换，仅 Rugged 系列）
- 创建基于工控协议的服务对象（Modbus TCP、IEC104 等）
- 创建针对工控协议的 IPS 配置文件
- 添加工控协议策略并关联安全配置文件

## 许可证要求
使用工控协议签名功能需要以下许可证之一：
- FortiGuard 工业安全服务
- ATP（高级威胁防护）套装
- UTP（统一威胁防护）套装

## 配置项
在使用本技能前，需要在 OpenClaw 的环境变量或配置文件中设置以下项：

| 配置项 | 说明 | 必填 | 默认值 |
| :--- | :--- | :--- | :--- |
| `FORTIGATE_HOST` | FortiGate 设备的 IP 地址或域名 | 是 | 无 |
| `FORTIGATE_TOKEN` | API 访问令牌 | 是 | 无 |
| `FORTIGATE_PORT` | API 端口 | 否 | 443 |
| `FORTIGATE_VERIFY_SSL` | 是否验证 SSL 证书 | 否 | false |

## 使用方法
@openclaw fortigate-config <操作> <参数（JSON 格式）>

### 基础操作
| 操作 | 说明 | 参数示例 |
|------|------|----------|
| `list-policies` | 列出所有防火墙策略 | `{}` |
| `add-address` | 添加地址对象 | `{"name": "web-server", "subnet": "192.168.1.10/32"}` |
| `delete-address` | 删除地址对象 | `{"name": "web-server"}` |
| `add-policy` | 添加防火墙策略 | `{"name": "allow-web", "srcintf": "port1", "dstintf": "port2", "srcaddr": "all", "dstaddr": "all", "action": "accept"}` |
| `update-policy` | 更新防火墙策略 | `{"policyid": 1, "action": "deny", "name": "new-name"}` |

### 工控协议操作
| 操作 | 说明 | 参数示例 |
|------|------|----------|
| `configure-icond` | 配置 Industrial Connectivity 服务（协议转换） | `{"interface": "internal1", "protocol_type": "modbus-serial-tcp", "tty_device": "serial0"}` |
| `create-industrial-service` | 创建工控协议服务对象 | `{"name": "modbus-tcp", "protocol": "TCP", "port": 502}` |
| `create-industrial-ips` | 创建工控 IPS 配置文件 | `{"name": "plc-protection", "protocols": ["Modbus", "IEC104"], "action": "monitor"}` |
| `add-industrial-policy` | 添加工控协议策略（带安全防护） | `{"name": "hmi-to-plc", "srcintf": "port1", "dstintf": "port2", "srcaddr": "hmi-net", "dstaddr": "plc-net", "service": "modbus-tcp", "ips_profile": "plc-protection"}` |

## 常见工控协议端口
| 协议 | 端口 | 描述 |
|------|------|------|
| Modbus TCP | TCP 502 | 工业自动化常用协议 |
| IEC 104 | TCP 2404 | 电力系统远程控制协议 |
| S7 Plus | TCP 102 | 西门子 PLC 协议 |
| Ethernet/IP | TCP 44818 | Rockwell/ODVA 工业协议 |
| DNP3 | TCP 20000 | 电力/水务自动化协议 |

## 注意事项
- 所有写操作（添加、删除、更新）均会先检查对象是否存在，避免重复创建或误删。
- 输出格式优先使用表格（需安装 `tabulate`），否则使用简单文本对齐。
- 生产环境请将 `FORTIGATE_VERIFY_SSL` 设为 `true` 并使用有效证书。

## 反馈与支持
如有问题，请联系 jiansiting@gmail.com