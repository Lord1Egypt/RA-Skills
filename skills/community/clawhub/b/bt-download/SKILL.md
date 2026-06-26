---
name: bt-download
description: BT下载助手，支持 aria2 RPC 模式下载、监控和自动做种
homepage: https://aria2.github.io
metadata:
  {
    "openclaw":
      {
        "emoji": "🔽",
        "requires": { "bins": ["aria2c"] },
        "install":
          [
            {
              "id": "apt",
              "kind": "apt",
              "formula": "aria2",
              "bins": ["aria2c"],
              "label": "Install aria2 (apt)",
            },
          ],
      },
  }
---

# BT Download (aria2 RPC)

BT 下载助手，支持磁力链接、BT 文件、普通下载链接，支持 RPC 模式和自动做种监控。

## 功能

- **bt_check_aria2** - 检查 aria2 是否已安装
- **bt_install_aria2** - 安装 aria2
- **bt_get_trackers** - 获取最新 BT tracker 列表
- **bt_check_dht** - 检测 DHT (IPv4/IPv6) 状态
- **bt_enable_dht** - 开启 DHT 支持
- **bt_start_rpc** - 启动 aria2 RPC 服务（自动开启 DHT）
- **bt_download** - 添加下载任务
- **bt_get_status** - 查询做种状态
- **bt_stop_seed** - 停止做种任务
- **bt_monitor_and_stop** - 监控做种并自动停止

## 快速开始

### 1. 检查并安装 aria2

```bash
bt_check_aria2
bt_install_aria2
```

### 2. 启动 RPC 服务

```bash
bt_start_rpc
```

### 3. 添加下载

磁力链接:
```bash
bt_download --url "magnet:?xt=urn:btih:..."
```

BT 文件:
```bash
bt_download --url "/path/to/file.torrent"
```

普通链接:
```bash
bt_download --url "https://example.com/file.ext"
```

### 4. 监控做种

```bash
bt_get_status
bt_monitor_and_stop --targetRatio 500
```

## 参数说明

| 工具 | 参数 | 说明 |
|------|------|------|
| bt_check_dht | - | 检测 DHT 状态 |
| bt_enable_dht | dht | 开启 IPv4 DHT，默认 true |
| bt_enable_dht | dht6 | 开启 IPv6 DHT，默认 true |
| bt_start_rpc | downloadDir | 下载保存目录 |
| bt_start_rpc | seedRatio | 目标做种率，默认 5 |
| bt_start_rpc | seedTime | 最大做种时间（分钟），默认 1440 |
| bt_start_rpc | enableDht | 自动开启 DHT，默认 true |
| bt_download | url | 下载链接、BT 文件路径或磁力链接 |
| bt_download | downloadDir | 保存目录（可选，不填则提示确认） |
| bt_download | useDefaultDir | 直接使用默认目录，跳过确认 |
| bt_download | seedRatio | 目标做种率 |
| bt_download | seedTime | 最大做种时间 |
| bt_stop_seed | gid | 任务 GID（可选） |
| bt_monitor_and_stop | targetRatio | 目标做种率（百分比），默认 500% |

## 下载确认

当用户调用 `bt_download` 但未指定 `downloadDir` 时，会返回确认提示：

```json
{
  "needConfirm": true,
  "defaultDir": "~/Downloads",
  "message": "请确认下载目录：\n1. 使用默认目录: ~/Downloads\n2. 指定其他目录（请回复具体路径）",
  "hint": "回复「1」使用默认目录，或回复具体路径指定其他目录"
}
```

**系统默认目录：**
- Windows: `C:\Users\<用户名>\Downloads`
- macOS: `/Users/<用户名>/Downloads`
- Linux: `/home/<用户名>/Downloads`

用户回复后，再次调用 `bt_download` 并指定目录（或 `useDefaultDir: true` 直接使用默认）。

## 做种监控

`bt_monitor_and_stop` 会：
1. 检查当前做种任务的做种率
2. 达到目标后自动停止该任务
3. 在会话中通知用户
4. 保持 aria2 RPC 持续运行

示例返回：
```json
{
  "checked": 1,
  "stopped": 1,
  "notify": "✅ 做种任务已完成，已自动停止:\n• example.bin (已上传 xx.xx GB)"
}
```
