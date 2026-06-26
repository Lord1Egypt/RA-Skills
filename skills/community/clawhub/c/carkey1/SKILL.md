---
name: carkey
description: 车辆信息查询技能。查询车辆位置、车况（车锁、车门、车窗、空调、电源状态等）。触发词：查车、车辆位置、车况、我的车在哪。跨平台支持 Linux/macOS/Windows。
---

## 何时使用

- 用户查询车辆位置："我的车在哪"、"查一下车在哪"
- 用户查询车况信息："车锁了吗"、"车窗关了吗"、"车辆状态"
- 用户需要提供认证信息时，引导输入 `vehicleToken####accessToken`

## 快速使用

**方式 1：绝对路径（推荐 Agent 使用）**
```bash
# 假设技能安装在 ~/.openclaw/workspace/skills/carkey
~/.openclaw/workspace/skills/carkey/scripts/vehicle-query.sh
~/.openclaw/workspace/skills/carkey/scripts/vehicle-query.sh position
~/.openclaw/workspace/skills/carkey/scripts/vehicle-query.sh condition
```

**方式 2：相对路径（用户手动执行）**
```bash
cd carkey
./scripts/vehicle-query.sh
./scripts/vehicle-query.sh position
./scripts/vehicle-query.sh condition
```

## 认证

**格式：** `vehicleToken####accessToken`（4 个 `#` 分隔）

首次使用会提示输入，自动缓存。

| 系统 | 缓存路径 |
|------|----------|
| Linux/macOS | `~/.carkey_cache.json` |
| Windows | `%USERPROFILE%/.carkey_cache.json` |

## 状态码

| 字段 | 值含义 |
|------|--------|
| power | 0=熄火, 1=ACC, 2=ON |
| gear | 1=P, 2=N, 3=D, 4=R, 5=S |
| door/window/trunk | 0=关闭, 1=开启 |
| lock | 0=解锁, 1=上锁 |

## 错误处理

| 场景 | 处理 |
|------|------|
| 无缓存 | 引导用户提供 token |
| Token 过期 | 提示重新认证，删除旧缓存 |
| 请求失败 | 自动重试 2 次，30 秒超时 |
| 缺少依赖 | 提示安装 curl/jq |

## 系统支持

| 系统 | 依赖安装 |
|------|----------|
| Linux (Ubuntu/Debian) | `sudo apt-get install curl jq` |
| Linux (CentOS/RHEL) | `sudo yum install curl jq` |
| macOS | `brew install curl jq` |
| Windows (Git Bash) | 已包含 |
| Windows (WSL) | `wsl sudo apt-get install curl jq` |

## 文件结构

```
carkey/
├── SKILL.md              # 本文档
├── README.md             # 详细说明
├── _meta.json            # 元数据
└── scripts/
    └── vehicle-query.sh  # 查询脚本（跨平台）
```