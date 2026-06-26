---
name: get-public-ip
description: 检测公网出口 IP，支持国内和国际网络环境，自动切换最优节点，超时保护，秒级完成。
emoji: 🌐
openclaw:
  version: ">=2026.1"
tags:
  - network
  - utility
  - ip-check
  - windows
  - cross-platform
---

# get-public-ip

检测本机公网出口 IP，兼容国内/国际网络环境，自动选择最快节点。

## 功能

- ✅ 自动识别网络环境，优先使用国内节点（更快）
- ✅ 多节点自动 fallback，确保高可用性
- ✅ 超时保护（单节点最多 5 秒）
- ✅ IP 格式验证，结果可信
- ✅ 纯系统命令执行，不耗 LLM token
- ✅ 零外部依赖

## 触发方式

直接说或写中文即可：
- "获取公网IP"
- "我的IP是多少"
- "检查出口IP"

## 国内节点（优先，延迟 150~700ms）
| 节点 | 地址 | 延迟 |
|------|------|------|
| ipip.net | https://myip.ipip.net | ~157ms |
| ip.sb | https://ip.sb | ~680ms |
| icanhazip | https://icanhazip.com | ~580ms |

## 国际节点（fallback，延迟 500~900ms）
| 节点 | 地址 | 延迟 |
|------|------|------|
| httpbin | https://httpbin.org/ip | ~890ms |

## 输出格式

成功：
> 当前公网IP：171.83.108.245 | 来源：ip.sb | 耗时：681ms

失败：
> ❌ 无法获取公网IP，请检查网络连接

## 执行逻辑

当收到获取 IP 请求时，用 PowerShell 执行以下逻辑（Windows 直接调用，macOS/Linux 用 curl）：

### 国内节点优先

依次尝试：
1. `https://ip.sb` - 提取纯文本 IP，格式验证
2. `https://myip.ipip.net` - 提取 `当前 IP：xxx` 中的 IP
3. `https://icanhazip.com` - 提取纯文本 IP

### 国际节点兜底

国内全失败时尝试：
4. `https://httpbin.org/ip` - 解析 JSON 中的 origin

每个节点最多 5 秒超时，任一成功立即返回。

## 超时保护

每个节点最多 5 秒，全节点总超时 20 秒。远超即判定失败。

## 依赖

无外部依赖。Windows 使用内置 `Invoke-WebRequest`，macOS/Linux 使用 `curl`。

## 设计原则

1. **不调用 LLM**：纯命令执行，毫秒级响应
2. **结果可验证**：IP 格式正则验证，假 IP 不返回
3. **多节点兜底**：任一节点可用即成功，不依赖单一服务
4. **国内优先**：国内节点比国际快 3~5 倍