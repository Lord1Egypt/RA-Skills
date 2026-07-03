---
name: bambu-printer
description: 控制 Bambu P1S 拓竹3D打印机。支持文件管理（FTPS）、连接状态检查。可查看文件列表、上传下载gcode/3mf文件、查看延时摄影。
---

# Bambu 打印机控制

## 概述
通过 FTPS 协议控制 Bambu P1S 3D打印机的文件操作。

### ⚠️ 技术说明
本 Skill 使用 `curl`（FTPS）+ `Perl`（MQTT 探测）实现，而非 `bambu-cli` npm 包。
原因：macOS 上 Homebrew 安装的 Node.js/Python 被网络限制，无法 TCP 连接局域网设备，
只有苹果签名的系统工具（curl、nc、perl、ruby）可以正常连接。

## 打印机信息
- **型号**: Bambu P1S
- **序列号**: 0109C4A2200171
- **IP**: 192.168.1.68
- **Access Code**: 31713703

## 可用功能

### 1. 状态检查
检查打印机是否在线、FTPS/MQTT/摄像头端口连通性。
```bash
/usr/bin/perl scripts/status.pl
```
返回 JSON：`{"status":"online","ftps":"ok","mqtt_auth":"ok","camera_port":"open","ping":"ok",...}`

### 2. 文件列表
列出打印机上的文件和目录。
```bash
bash scripts/ftp.sh list [path]
```
- 根目录: `bash scripts/ftp.sh list /`
- 延时摄影: `bash scripts/ftp.sh list /timelapse/`
- 打印缓存: `bash scripts/ftp.sh list /cache/`

**打印机目录结构**:
- `/` - 根目录
- `/cache/` - 打印文件缓存
- `/timelapse/` - 延时摄影视频
- `/recorder/` - 打印记录（.bin）
- `/image/` - 图片
- `/model/` - 模型文件

### 3. 上传文件
上传 gcode 或 3mf 文件到打印机。
```bash
bash scripts/ftp.sh upload <本地文件> [远程目录]
```
默认上传到 `/cache/`。
示例: `bash scripts/ftp.sh upload my_model.gcode.3mf`

### 4. 下载文件
从打印机下载文件（如延时摄影视频）。
```bash
bash scripts/ftp.sh download <远程路径> [本地路径]
```
示例: `bash scripts/ftp.sh download /timelapse/video_2025-01-05_18-36-09.avi ./`

### 5. 删除文件
删除打印机上的远程文件。
```bash
bash scripts/ftp.sh delete <远程路径>
```

### 6. 文件统计
统计指定目录的文件数量和总大小。
```bash
bash scripts/ftp.sh size [path]
```

## ⏳ 暂不可用功能
以下功能因 MQTT SUBSCRIBE 兼容性问题暂不可用：
- ❌ 实时打印状态（温度、进度、剩余时间）
- ❌ 发送打印命令
- ❌ 暂停/恢复/停止打印
- ❌ 摄像头快照
- ❌ 归位/移动等控制命令

**原因**: Perl/Ruby 的 SSL 实现与 Bambu MQTT broker 不完全兼容，
SUBSCRIBE 报文被静默忽略。如需完整 MQTT 功能，建议在有 Node.js 网络权限的环境中使用 `bambu-cli`。

## 使用建议
1. **查看最近的打印记录**: `bash scripts/ftp.sh list /timelapse/`
2. **下载延时视频分享**: `bash scripts/ftp.sh download /timelapse/xxx.avi ./`
3. **检查打印机是否在线**: `/usr/bin/perl scripts/status.pl`
4. **上传打印文件**: 先用 Bambu Studio 切片，然后用 upload 命令上传

## 脚本路径
- 状态检查: `scripts/status.pl`
- FTPS 操作: `scripts/ftp.sh`
- 配置文件: `config.json`
