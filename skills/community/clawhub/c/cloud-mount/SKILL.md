# cloud-mount - 云存储挂载工具

> 让服务器/电脑轻松挂载云存储到本地，像访问本地文件夹一样使用 OneDrive、Google Drive 等。

## 📖 目录

- [适用场景](#适用场景)
- [前置条件](#前置条件)
- [快速开始](#快速开始)
- [脚本工具](#脚本工具)
- [配置说明](#配置说明)
- [支持的云存储](#支持的云存储)
- [最佳实践](#最佳实践)
- [故障排查](#故障排查)
- [高级配置](#高级配置)
- [安全建议](#安全建议)

---

## 适用场景

### ✅ 个人使用
- **Obsidian 笔记同步** — 多设备访问同一 vault
- **个人文件备份** — 自动备份到云端
- **跨设备文件访问** — 在任何地方访问家中文件

### ✅ 开发场景
- **代码备份** — 将代码仓库备份到云存储
- **配置文件同步** — 同步 dotfiles 到多台服务器
- **资源文件存储** — 大文件存放在云端，按需访问

### ✅ 服务器运维
- **日志归档** — 自动归档日志到云存储
- **数据备份** — 数据库备份上传到云端
- **资源共享** — 团队共享文件存储

### ✅ 内容创作
- **素材库管理** — 图片、视频素材云端存储
- **协作编辑** — 多人访问同一文件库
- **版本管理** — 云存储的历史版本功能

---

## 前置条件

- ✅ rclone 已安装（未安装会自动检测并提示）
- ✅ 拥有对应云存储账号
- ✅ 有另一台设备（手机/电脑）可以运行授权流程

### 检查 rclone 安装

```bash
rclone --version
```

如果未安装，根据系统选择：

```bash
# macOS
brew install rclone

# Ubuntu / Debian
sudo apt install rclone

# CentOS / RHEL
sudo dnf install rclone

# 其他系统：https://rclone.org/install/
```

---

## 快速开始

### 1️⃣ 安装 rclone

```bash
# macOS
brew install rclone

# Ubuntu / Debian
sudo apt install rclone

# CentOS / RHEL
sudo dnf install rclone

# 验证安装
rclone --version
```

### 2️⃣ 配置云存储

```bash
# 交互式配置（推荐新手）
rclone config
```

**详细步骤：**

1. 输入 `n` 创建新配置
2. 输入名字：`onedrive`（或你喜欢的名字）
3. 选择存储类型：
   - OneDrive 个人版：`41`
   - Google Drive：`drive`
   - 阿里云盘：`alidrive`
   - 其他：查看对应编号
4. client_id 和 client_secret：直接回车（使用默认）
5. Advanced config：`n`（否）
6. Web browser：`n`（使用授权码方式）
7. **在浏览器打开提供的 URL**，登录云存储账号并授权
8. 复制返回的授权码，粘贴到终端
9. 选择 drive（通常选第一个）
10. 确认配置：`y`
11. 保存并退出：`y` → `q`

### 3️⃣ 测试配置

```bash
# 列出云存储根目录文件
rclone lsd onedrive:

# 应该能看到你的云盘文件夹列表
```

### 4️⃣ 创建本地挂载点

```bash
mkdir -p ~/cloud-storage/onedrive
```

### 5️⃣ 挂载云存储

```bash
# 手动挂载（测试用）
rclone mount onedrive: ~/cloud-storage/onedrive --daemon --vfs-cache-mode writes

# 验证挂载
ls ~/cloud-storage/onedrive/

# 应该能看到云盘中的文件
```

### 6️⃣ 设置开机自启（可选）

使用提供的 systemd user service 脚本（无需 sudo）：

```bash
# 编辑配置
nano ~/.config/cloud-mount/config.sh

# 启用服务（无需 sudo）
~/cloud-mount/scripts/enable-autostart.sh enable
```

---

## 脚本工具

### mount-cloud.sh - 一键挂载

**基本用法：**

```bash
# 使用默认配置挂载
~/cloud-mount/scripts/mount-cloud.sh onedrive

# 指定挂载点
~/cloud-mount/scripts/mount-cloud.sh onedrive ~/my-cloud

# 检查状态
~/cloud-mount/scripts/mount-cloud.sh --status
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `remote_name` | rclone 配置的远程名称 | onedrive |
| `mount_point` | 本地挂载点 | ~/cloud-storage/<remote> |

**选项：**

| 选项 | 说明 |
|------|------|
| `--status, -s` | 显示所有挂载状态 |
| `--help, -h` | 显示帮助信息 |

### check-mount.sh - 检测挂载状态

**基本用法：**

```bash
# 检查指定挂载点
~/cloud-mount/scripts/check-mount.sh ~/cloud-storage/onedrive

# 检查所有云存储挂载
~/cloud-mount/scripts/check-mount.sh --all

# 查看 rclone 进程
~/cloud-mount/scripts/check-mount.sh --processes
```

**输出示例：**

```
✓ /home/user/cloud-storage/onedrive - 已挂载
  挂载源：onedrive:
  文件系统：fuse.rclone
  权限：可读写
  进程：运行中 (PID: 12345)
```

### enable-autostart.sh - 设置开机自启

使用 **systemd user service**，无需 `sudo` 权限。

**命令：**

```bash
# 启用服务（无需 sudo）
~/cloud-mount/scripts/enable-autostart.sh enable

# 禁用服务
~/cloud-mount/scripts/enable-autostart.sh disable

# 查看状态
~/cloud-mount/scripts/enable-autostart.sh status

# 重启服务
~/cloud-mount/scripts/enable-autostart.sh restart

# 查看日志
~/cloud-mount/scripts/enable-autostart.sh logs
```

---

## 配置说明

### 配置文件位置

`~/.config/cloud-mount/config.sh`

### 完整配置示例

```bash
#!/bin/bash
# cloud-mount 配置文件

# 云存储远程名称（rclone config 中配置的名字）
CLOUD_REMOTE="onedrive"

# 本地挂载点
MOUNT_POINT="$HOME/cloud-storage/onedrive"

# 挂载选项
MOUNT_OPTIONS="--daemon --vfs-cache-mode writes --vfs-cache-max-size 1G"

# 是否开机自启
AUTO_START=true
```

### 挂载选项详解

| 选项 | 说明 | 推荐值 | 备注 |
|------|------|--------|------|
| `--daemon` | 后台运行 | 必需 | 不要省略 |
| `--vfs-cache-mode` | 缓存模式 | `writes` | 可选：minimal/writes/full |
| `--vfs-cache-max-size` | 最大缓存 | `1G` | 根据内存调整 |
| `--allow-other` | 允许其他用户访问 | 按需 | 需要 fuse 配置 |
| `--uid` | 指定文件所有者 UID | 按需 | 配合 allow-other |
| `--gid` | 指定文件所有者 GID | 按需 | 配合 allow-other |
| `--read-only` | 只读模式 | 按需 | 保护云端数据 |
| `--timeout` | 空闲超时 | `1h` | 自动断开空闲连接 |

### 缓存模式选择

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `minimal` | 最小缓存 | 内存紧张、只读访问 |
| `writes` | 写入缓存（推荐） | 日常使用、平衡性能 |
| `full` | 完整缓存 | 频繁读写、内存充足 |

---

## 支持的云存储

| 云存储 | rclone 类型 | 难度 | 地区 | 备注 |
|--------|------------|------|------|------|
| **OneDrive 个人版** | `onedrive` | ⭐⭐ | 全球 | 最常用，5GB 免费 |
| **OneDrive 商业版** | `onedrive` | ⭐⭐⭐ | 全球 | 需要企业账号 |
| **Google Drive** | `drive` | ⭐⭐ | 海外 | 15GB 免费，需科学上网 |
| **阿里云盘** | `alidrive` | ⭐⭐ | 中国 | 速度快，容量大 |
| **百度网盘** | `baidu` | ⭐⭐⭐ | 中国 | 需申请 API key |
| **Dropbox** | `dropbox` | ⭐⭐ | 全球 | 国际通用 |
| **Amazon S3** | `s3` | ⭐⭐⭐ | 全球 | 对象存储，按量付费 |
| **WebDAV** | `webdav` | ⭐⭐ | 通用 | 支持坚果云、天翼云盘等 |
| **SFTP** | `sftp` | ⭐⭐ | 通用 | 远程服务器 |
| **FTP** | `ftp` | ⭐⭐ | 通用 | 传统文件传输 |

> 💡 **提示**：支持所有 rclone 支持的云存储（70+ 种），查看完整列表：https://rclone.org/

---

## 最佳实践

### 1. Obsidian 云同步

```bash
# 1. 配置 rclone（OneDrive）
rclone config

# 2. 挂载云存储
~/cloud-mount/scripts/mount-cloud.sh onedrive

# 3. 设置开机自启
sudo ~/cloud-mount/scripts/enable-autostart.sh enable

# 4. 在 Obsidian 中打开 vault
# 路径：~/cloud-storage/onedrive/ObsidianVault/
```

**同步说明：**
- 手机/平板安装 OneDrive App
- 所有设备自动同步
- 无需额外配置

### 2. 服务器备份方案

```bash
# 1. 配置 Google Drive 用于备份
rclone config

# 2. 挂载备份盘
~/cloud-mount/scripts/mount-cloud.sh gdrive ~/backup

# 3. 创建备份脚本
cat > ~/backup.sh << 'EOF'
#!/bin/bash
rsync -av --delete /var/www/ ~/backup/www/
rsync -av --delete /etc/ ~/backup/etc/
rsync -av --delete /home/ ~/backup/home/
EOF

# 4. 设置定时任务
crontab -e
# 每天凌晨 2 点备份
0 2 * * * /bin/bash ~/backup.sh
```

### 3. 多云存储管理

```bash
# 配置多个云存储
rclone config
# onedrive-personal
# onedrive-work
# gdrive-backup

# 分别挂载
~/cloud-mount/scripts/mount-cloud.sh onedrive-personal ~/cloud/personal
~/cloud-mount/scripts/mount-cloud.sh onedrive-work ~/cloud/work
~/cloud-mount/scripts/mount-cloud.sh gdrive-backup ~/backup

# 一键检查所有挂载
~/cloud-mount/scripts/check-mount.sh --all
```

### 4. 性能优化

**内存优化（2GB 内存服务器）：**

```bash
# 编辑配置
nano ~/.config/cloud-mount/config.sh

# 使用最小缓存
MOUNT_OPTIONS="--daemon --vfs-cache-mode minimal --vfs-cache-max-size 256M"
```

**性能优化（8GB+ 内存服务器）：**

```bash
# 使用完整缓存
MOUNT_OPTIONS="--daemon --vfs-cache-mode full --vfs-cache-max-size 2G"
```

---

## 故障排查

### 问题 1：挂载后看不到文件

**症状：** 挂载成功，但目录为空

**排查步骤：**

```bash
# 1. 验证 rclone 配置
rclone lsd onedrive:
# 应该能看到云盘文件夹

# 2. 检查挂载进程
ps aux | grep rclone
# 应该有 rclone 进程在运行

# 3. 查看挂载点
ls -la ~/cloud-storage/onedrive/

# 4. 查看系统日志
dmesg | tail -20

# 5. 重新挂载
fusermount -u ~/cloud-storage/onedrive
~/cloud-mount/scripts/mount-cloud.sh onedrive
```

### 问题 2：token 过期

**症状：** `InvalidAuthenticationToken` 错误

**解决方案：**

```bash
# 刷新 token
rclone config reconnect onedrive:

# 或重新配置
rclone config
```

### 问题 3：挂载失败，权限错误

**症状：** `Permission denied` 或 `fusermount: mount failed`

**解决方案：**

```bash
# 1. 确保挂载点目录存在
mkdir -p ~/cloud-storage/onedrive

# 2. 检查目录权限
chmod 755 ~/cloud-storage/onedrive

# 3. 检查 fuse 是否安装
sudo apt install fuse  # Debian/Ubuntu
sudo yum install fuse  # CentOS/RHEL

# 4. 检查 fuse 模块
lsmod | grep fuse
# 如果没有，加载模块
sudo modprobe fuse
```

### 问题 4：内存占用过高

**症状：** 服务器内存紧张，OOM

**解决方案：**

```bash
# 1. 减少缓存大小
nano ~/.config/cloud-mount/config.sh
MOUNT_OPTIONS="--daemon --vfs-cache-mode minimal --vfs-cache-max-size 256M"

# 2. 重启服务
sudo ~/cloud-mount/scripts/enable-autostart.sh restart

# 3. 监控内存使用
watch -n 1 'ps aux | grep rclone | grep -v grep'
```

### 问题 5：开机自启失败

**症状：** 重启后挂载未自动恢复

**排查步骤：**

```bash
# 1. 查看服务状态
sudo systemctl status cloud-mount

# 2. 查看详细日志
sudo journalctl -u cloud-mount -n 50

# 3. 检查配置文件
cat ~/.config/cloud-mount/config.sh

# 4. 检查 rclone 配置
rclone config show onedrive

# 5. 重新启用服务
sudo ~/cloud-mount/scripts/enable-autostart.sh disable
sudo ~/cloud-mount/scripts/enable-autostart.sh enable
```

### 问题 6：文件写入失败

**症状：** 无法创建或修改文件

**解决方案：**

```bash
# 1. 检查云存储权限
# 确认账号有写入权限

# 2. 检查挂载选项
# 确保没有使用 --read-only

# 3. 检查磁盘空间
rclone about onedrive:

# 4. 检查缓存目录权限
ls -la ~/.cache/rclone/
```

---

## 高级配置

### 使用配置文件模板（非交互式）

适合批量部署或自动化配置：

```bash
# 创建 rclone 配置文件
mkdir -p ~/.config/rclone
cat > ~/.config/rclone/rclone.conf << 'EOF'
[onedrive]
type = onedrive
token = {"access_token":"...","refresh_token":"...","expiry":"..."}
drive_id = YOUR_DRIVE_ID
drive_type = personal
EOF

# 获取授权
rclone authorize onedrive

# 将返回的 JSON 替换上面的 token 占位符
```

### 多云存储配置示例

```bash
# ~/.config/cloud-mount/config-onedrive.sh
CLOUD_REMOTE="onedrive-personal"
MOUNT_POINT="$HOME/cloud-storage/personal"
MOUNT_OPTIONS="--daemon --vfs-cache-mode writes"

# ~/.config/cloud-mount/config-gdrive.sh
CLOUD_REMOTE="gdrive-backup"
MOUNT_POINT="$HOME/cloud-storage/backup"
MOUNT_OPTIONS="--daemon --vfs-cache-mode full --vfs-cache-max-size 2G"
```

### systemd 服务模板

手动创建服务文件 `/etc/systemd/system/cloud-mount@.service`：

```ini
[Unit]
Description=Cloud Storage Mount (%i)
After=network-online.target
Wants=network-online.target

[Service]
Type=forking
User=%i
Group=%i
Environment="HOME=/home/%i"
ExecStart=/usr/bin/rclone mount %i: /home/%i/cloud-storage/%i --daemon --vfs-cache-mode writes --vfs-cache-max-size 1G
ExecStop=/usr/bin/fusermount -u /home/%i/cloud-storage/%i || /bin/true
Restart=on-failure
RestartSec=10
StartLimitBurst=3
StartLimitInterval=60s

# 资源限制（防止内存泄漏）
MemoryMax=512M
MemoryHigh=256M

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl enable cloud-mount@onedrive.service
sudo systemctl start cloud-mount@onedrive.service
```

### 监控脚本

创建监控脚本 `/usr/local/bin/watch-cloud-mount.sh`：

```bash
#!/bin/bash
# 监控云存储挂载状态

MOUNT_POINT="$HOME/cloud-storage/onedrive"
LOG_FILE="/var/log/cloud-mount-monitor.log"

if ! mount | grep -q "$MOUNT_POINT"; then
    echo "$(date): Mount point $MOUNT_POINT not found, attempting to remount..." >> $LOG_FILE
    
    # 尝试重新挂载
    ~/cloud-mount/scripts/mount-cloud.sh onedrive
    
    if [ $? -eq 0 ]; then
        echo "$(date): Remount successful" >> $LOG_FILE
    else
        echo "$(date): Remount failed!" >> $LOG_FILE
        # 可以添加邮件/短信通知
    fi
fi
```

添加到 crontab：

```bash
# 每 5 分钟检查一次
*/5 * * * * /usr/local/bin/watch-cloud-mount.sh
```

---

## 安全建议

### 1. 保护敏感信息

```bash
# 设置 rclone 配置文件权限
chmod 600 ~/.config/rclone/rclone.conf

# 不要将配置文件上传到代码仓库
# 添加到 .gitignore
echo ".config/rclone/rclone.conf" >> ~/.gitignore
```

### 2. 限制挂载权限

```bash
# 仅当前用户可访问
MOUNT_OPTIONS="--daemon --vfs-cache-mode writes"

# 多用户共享时（谨慎使用）
MOUNT_OPTIONS="--daemon --allow-other --uid 1000 --gid 1000"
```

### 3. 使用专用账号

- 为服务器创建专用的云存储账号
- 限制账号权限（如只读、特定文件夹）
- 定期更换 token

### 4. 定期审计

```bash
# 检查挂载状态
~/cloud-mount/scripts/check-mount.sh --all

# 查看服务日志
sudo journalctl -u cloud-mount --since "24 hours ago"

# 监控资源使用
ps aux | grep rclone
```

### 5. 备份配置

```bash
# 备份 cloud-mount 配置（不包含 token）
tar -czf cloud-mount-config-backup.tar.gz \
    ~/.config/cloud-mount/config.sh \
    ~/cloud-mount/scripts/

# 注意：不要备份 rclone.conf（包含敏感 token）
```

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `scripts/mount-cloud.sh` | 一键挂载脚本 |
| `scripts/check-mount.sh` | 状态检测脚本 |
| `scripts/enable-autostart.sh` | 开机自启脚本 |
| `~/.config/cloud-mount/config.sh` | 配置文件 |
| `~/.config/rclone/rclone.conf` | rclone 配置（含 token） |

---

## 资源链接

- **rclone 官方文档**: https://rclone.org/docs/
- **rclone 下载**: https://rclone.org/downloads/
- **ClawHub 技能页面**: https://clawhub.ai/skills/cloud-mount
- **GitHub 仓库**: （待添加）

---

## 更新日志

### v1.2.0 (2026-03-21) - 安全说明增强 🔒

- 🔒 **新增详细安全说明**
  - 解释 ClawHub "Suspicious" 标记原因
  - 5 个误报模式及其实际用途
  - 权限使用说明（sudo、文件系统、网络）
  - 安全最佳实践和信任验证指南

### v1.1.0 (2026-03-20) - 文档优化 📝

- 📚 **README.md 全面优化**
  - 增加特性亮点和使用场景
  - 添加徽章和视觉元素
  - 优化表格和代码示例
  - 增加常见问题解答

- 📖 **SKILL.md 深度完善**
  - 添加详细目录导航
  - 扩展最佳实践章节
  - 完善故障排查指南（6 个常见问题）
  - 增加高级配置示例
  - 补充安全建议和资源链接

### v1.0.0 (2026-03-20)

- ✨ 首次发布
- 🔧 提供一站式云存储挂载方案
- 📝 集成 rclone 自动检测与配置
- 🔄 支持 systemd 开机自启
- 📊 内置状态检测工具
- 🛡️ 通过安全审计

---

**版本:** 1.2.0  
**作者:** LuckyYou (@Liqiuyue9597)  
**许可:** MIT License  
**最后更新:** 2026-03-21
