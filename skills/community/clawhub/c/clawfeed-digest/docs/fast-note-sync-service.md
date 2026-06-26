# Fast Note Sync Service

> Obsidian 与 OpenClaw workspace 自动同步服务

## 简介

Fast Note Sync Service 可以实现 Obsidian Vault 与 OpenClaw workspace 之间的双向同步。

- **GitHub**: https://github.com/haierkeys/fast-note-sync-service
- **相关插件**: https://github.com/haierkeys/obsidian-fast-note-sync

---

## 方案一：BRAT 插件安装（推荐）

### 1. 安装 BRAT 插件

BRAT 是 Obsidian 的第三方插件管理器，可以安装非社区插件。

**方法：通过 Obsidian 社区安装**
1. 打开 Obsidian → 设置 → 第三方插件
2. 关闭安全模式（如果提示）
3. 搜索 "BRAT" 并安装

**方法：手动安装**
1. 下载 BRAT: https://github.com/haierkeys/obsidian-fast-note-sync
2. 解压到 `.obsidian/plugins/brat/` 目录

### 2. 安装 Fast Note Sync 插件

1. 打开 Obsidian → 设置 → 第三方插件
2. 启用 BRAT
3. 点击 BRAT 设置 → Add beta plugin
4. 输入：`haierkeys/obsidian-fast-note-sync`
5. 启用 "Fast Note Sync" 插件

### 3. 配置插件

在插件设置中配置：
- **OpenClaw Workspace Path**: `C:\Users\你的用户名\.openclaw\workspace`
- **Sync Interval**: 5000ms

---

## 方案二：独立服务端（可选）

如果需要更强大的同步功能，可以安装独立服务端。

### 1. 下载服务

从 GitHub Releases 下载：
- Windows: `fast-note-sync-service-{版本}-windows-amd64.zip`
- Mac: `fast-note-sync-service-{版本}-darwin-amd64.tar.gz`

下载链接：https://github.com/haierkeys/fast-note-sync-service/releases

### 2. 解压到合适位置

建议放在 OpenClaw workspace 目录下：
```
C:\Users\你的用户名\.openclaw\workspace\fast-note-sync-service-2.5.1-windows-amd64\
```

### 3. 配置

编辑 `config/config.json`：

```json
{
  "obsidianVaultPath": "C:\\Users\\你的用户名\\OneDrive\\文档\\Obsidian Vault",
  "openclawWorkspacePath": "C:\\Users\\你的用户名\\.openclaw\\workspace",
  "syncIntervalMs": 5000,
  "enableAiSummary": false
}
```

### 4. 运行

```bash
# Windows
.\fast-note-sync-service.exe

# 或者后台运行
start /b .\fast-note-sync-service.exe
```

---

## 定时任务

### 启动 Fast Note Sync 服务

| 项目 | 内容 |
|------|------|
| **名称** | 启动 Fast Note Sync 服务 |
| **ID** | `2cb52248-77d4-4051-98f9-73635d535351` |
| **运行时间** | 每天 08:00 (北京时间) |
| **任务内容** | 启动 fast-note-sync-service 服务（如果未运行） |

**任务消息:**
```
启动 fast-note-sync-service 服务（如果未运行的话），然后汇报状态。
服务路径：C:\Users\whoami\.openclaw\workspace\fast-note-sync-service-2.5.1-windows-amd64\fast-note-sync-service.exe
```

---

## 常见问题

### Q: BRAT 插件找不到？

1. 确保已关闭 Obsidian 安全模式
2. 重启 Obsidian
3. 检查插件是否在 `.obsidian/plugins/` 目录

### Q: 服务启动后不同步？

检查：
1. 配置文件路径是否正确
2. Obsidian Vault 是否存在
3. OpenClaw workspace 权限是否正确

### Q: 同步有延迟？

默认 5 秒同步一次，可以调整配置中的 `syncIntervalMs` 参数。
