# Emby 问题排查指南

## 诊断优先级

遇到问题时，按此顺序检查：
1. **服务是否运行** → `GET /System/Info/Public`（无需认证，能访问说明服务正常）
2. **认证是否正确** → `GET /System/Info?api_key=<KEY>`（401 = Key 错误）
3. **查看最新日志** → `GET /System/Logs` 找最新的 `.txt` 日志
4. **查看任务状态** → `GET /ScheduledTasks` 看是否有失败任务

---

## 常见错误及解决

### 🔴 连接失败 / 无法访问

**症状**：`fetch` 超时或 `ECONNREFUSED`

排查步骤：
1. 确认服务器 IP 和端口是否正确（默认 8096）
2. 检查 Linux 防火墙：
   ```bash
   sudo ufw status
   sudo ufw allow 8096/tcp  # 如果被拦截
   ```
3. 确认 Emby 服务正在运行：
   ```bash
   systemctl status emby-server
   # 如果未运行：
   sudo systemctl start emby-server
   ```
4. 检查 Emby 是否监听正确的接口：
   ```bash
   ss -tlnp | grep 8096
   ```

---

### 🔴 401 Unauthorized

**症状**：API 返回 401

解决：
- 在 Emby 后台重新生成 API Key：`Dashboard → Advanced → API Keys`
- 确认 Key 完整复制，没有多余空格
- 确认使用的是 `api_key=` 参数（注意下划线）

---

### 🟡 元数据刮削失败

**症状**：刷新后封面/简介仍为空，或日志中有 `metadata provider` 错误

排查：
1. 检查 Emby 服务器是否能访问外网（TheMovieDb、TheTVDB 等）：
   ```bash
   curl -I https://api.themoviedb.org
   ```
2. 检查文件命名是否规范：
   - 电影：`电影名 (年份)/电影名 (年份).mkv`
   - 剧集：`剧集名/Season 01/S01E01.mkv`
3. 在 Emby 后台确认刮削器已启用：`Dashboard → Libraries → 对应媒体库 → 编辑`
4. 查看日志中的具体错误：
   ```
   GET /System/Logs/Log?name=<最新日志名>&api_key=<KEY>
   ```

---

### 🟡 转码性能问题

**症状**：播放卡顿、CPU 占用过高

通过会话 API 查看转码情况：
```
GET /Sessions?api_key=<KEY>
```
查看 `TranscodingInfo` 字段：
- `IsVideoDirect: false` → 视频在转码（耗 CPU）
- `IsAudioDirect: false` → 音频在转码
- `TranscodeReasons` → 转码原因列表

**常见原因及解决**：
| 原因 | 说明 | 解决方案 |
|------|------|---------|
| 客户端不支持格式 | 如 HEVC/H.265 在旧设备 | 建议用户升级客户端或使用 Emby 官方 App |
| 字幕格式 | PGS/ASS 字幕触发转码 | 提前转换为 SRT 字幕 |
| 码率过高 | 客户端设置了码率上限 | 客户端调整流媒体画质设置 |
| 硬件加速未启用 | 纯软件转码 | 在 Emby Dashboard → Transcoding 中启用 VAAPI/NVENC |

**Linux 检查硬件加速可用性**：
```bash
# Intel QSV / VAAPI
ls /dev/dri/

# NVIDIA
nvidia-smi

# 查看 Emby 转码日志
GET /System/Logs/Log?name=ffmpeg-transcode-xxx.txt&api_key=<KEY>
```

---

### 🟡 媒体库扫描后文件不出现

**症状**：新加的文件扫描后没显示

排查：
1. 确认媒体目录权限（Emby 用户需要读取权限）：
   ```bash
   ls -la /path/to/media/
   # Emby 用户通常是 emby 或 jellyfin
   chown -R emby:emby /path/to/media/
   chmod -R 755 /path/to/media/
   ```
2. 确认该目录已添加到 Emby 媒体库：`Dashboard → Libraries`
3. 检查文件格式是否被 Emby 支持（`.mkv`, `.mp4`, `.avi` 等均支持）
4. 查看扫描任务日志中是否有权限错误

---

### 🟡 数据库问题

**症状**：界面显示异常、数据丢失、服务启动慢

```bash
# 停止 Emby
sudo systemctl stop emby-server

# 备份数据库
cp -r /var/lib/emby/ /var/lib/emby_backup_$(date +%Y%m%d)

# 重启 Emby（会自动修复轻微数据库问题）
sudo systemctl start emby-server
```

也可以通过 API 触发数据库清理任务：
```
POST /ScheduledTasks/Running/CleanDatabase?api_key=<KEY>
```

---

## 日志位置（Linux）

| 日志类型 | 路径 |
|---------|------|
| Emby 主日志 | `/var/log/emby/` 或通过 API 获取 |
| systemd 日志 | `journalctl -u emby-server` |
| ffmpeg 转码日志 | 通过 `GET /System/Logs` 找 `ffmpeg-` 开头的文件 |

---

## 快速健康检查脚本

告知用户可以让 Claude 执行以下一键健康检查（提供服务器地址和 Key 后）：

1. `GET /System/Info` — 版本和内存
2. `GET /Sessions` — 当前连接数和转码数
3. `GET /ScheduledTasks` — 是否有失败任务
4. `GET /Items/Counts` — 媒体库规模
5. `GET /System/Logs` — 最新日志名（供进一步查看）

综合以上结果，给出健康状态报告。