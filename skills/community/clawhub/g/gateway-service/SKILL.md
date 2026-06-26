# Gateway 服务化

将 OpenClaw Gateway 安装为 Windows 定时任务（Scheduled Task），实现进程崩溃后自动重启。

## 安装服务

```bash
openclaw gateway install
```

**注意**：需要管理员权限运行。

## 管理命令

| 命令 | 说明 |
|------|------|
| `openclaw gateway install` | 安装服务（需管理员权限） |
| `openclaw gateway start` | 启动服务 |
| `openclaw gateway stop` | 停止服务 |
| `openclaw gateway restart` | 重启服务 |
| `openclaw gateway status` | 查看状态 |

## 服务信息

- **Windows 任务名称**：OpenClaw Gateway
- **启动方式**：开机自动启动
- **失败策略**：进程退出后自动重新启动

## 适用场景

- Gateway 进程经常崩溃退出
- 需要 7×24 小时运行
- 不想手动重启 Gateway
- 电脑重启后希望 Gateway 自动运行

## 故障排查

1. 查看服务状态：`openclaw gateway status`
2. 查看日志：`%USERPROFILE%\AppData\Local\Temp\openclaw\`
3. 手动启动：`openclaw gateway start`
