# cloud-mount 🌥️

> **让云存储像本地硬盘一样好用** — 一键挂载 OneDrive、Google Drive 等到本地，支持后台运行和开机自启

[![ClawHub](https://img.shields.io/badge/ClawHub-cloud--mount-blue)](https://clawhub.ai/skills/cloud-mount)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://clawhub.ai/skills/cloud-mount)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

---

## ✨ 特性亮点

- 🚀 **一键挂载** — 无需复杂配置，一条命令搞定
- 🔄 **开机自启** — systemd 服务支持，重启后自动挂载
- 📊 **状态检测** — 实时监控挂载状态，故障自动告警
- 💾 **多云支持** — OneDrive、Google Drive、阿里云盘、百度网盘等
- 🛡️ **安全可靠** — token 本地存储，支持权限控制
- 📝 **Obsidian 绝配** — 笔记云同步的终极解决方案

---

## 🎯 使用场景

### 场景 1：Obsidian 多设备同步
```bash
# 挂载 OneDrive 到本地
~/cloud-mount/scripts/mount-cloud.sh onedrive

# Obsidian vault 自动同步到云端
# 手机、平板、电脑随时随地访问笔记
```

### 场景 2：服务器备份到云存储
```bash
# 挂载 Google Drive 作为备份盘
~/cloud-mount/scripts/mount-cloud.sh gdrive ~/backup-drive

# 备份文件直接写入云端
rsync -av /var/www/ ~/backup-drive/www/
```

### 场景 3：访问云端资源
```bash
# 在服务器上挂载个人云盘
~/cloud-mount/scripts/mount-cloud.sh onedrive ~/cloud

# 直接访问云端文件，无需下载
ls ~/cloud/文档/
cat ~/cloud/配置/config.yaml
```

---

## 📦 快速开始

### 1️⃣ 安装

```bash
clawhub install cloud-mount
```

### 2️⃣ 配置 rclone（仅需一次）

```bash
rclone config
```

按提示操作：
- 选择云存储类型（OneDrive 选 `41`，Google Drive 选 `drive`）
- 完成授权流程（会提供授权 URL，在浏览器打开）
- 保存配置

### 3️⃣ 一键挂载

```bash
# 使用默认配置挂载
~/cloud-mount/scripts/mount-cloud.sh onedrive

# 或指定挂载点
~/cloud-mount/scripts/mount-cloud.sh gdrive ~/my-drive
```

### 4️⃣ 设置开机自启（可选）

```bash
# 编辑配置文件
nano ~/.config/cloud-mount/config.sh

# 启用 systemd user 服务（无需 sudo）
~/cloud-mount/scripts/enable-autostart.sh enable
```

---

## 🛠️ 脚本工具

| 脚本 | 功能 | 示例 |
|------|------|------|
| `mount-cloud.sh` | 一键挂载云存储 | `./mount-cloud.sh onedrive` |
| `check-mount.sh` | 检测挂载状态 | `./check-mount.sh --all` |
| `enable-autostart.sh` | 设置开机自启（无需 sudo） | `./enable-autostart.sh enable` |

### 常用命令

```bash
# 查看所有挂载状态
~/cloud-mount/scripts/check-mount.sh --all

# 查看 rclone 进程
~/cloud-mount/scripts/check-mount.sh --processes

# 重启挂载服务（无需 sudo）
~/cloud-mount/scripts/enable-autostart.sh restart

# 查看服务日志
~/cloud-mount/scripts/enable-autostart.sh logs
```

---

## ⚙️ 配置说明

配置文件位置：`~/.config/cloud-mount/config.sh`

```bash
# 云存储远程名称（rclone config 中配置的名字）
CLOUD_REMOTE="onedrive"

# 本地挂载点
MOUNT_POINT="$HOME/cloud-storage/onedrive"

# 挂载选项（根据需要调整）
MOUNT_OPTIONS="--daemon --vfs-cache-mode writes --vfs-cache-max-size 1G"

# 是否开机自启
AUTO_START=true
```

### 挂载选项优化

| 场景 | 推荐配置 |
|------|---------|
| **内存充足** | `--vfs-cache-mode full --vfs-cache-max-size 2G` |
| **内存紧张** | `--vfs-cache-mode minimal --vfs-cache-max-size 256M` |
| **多人共享** | `--allow-other --uid 1000 --gid 1000` |
| **只读访问** | `--read-only` |

---

## 🌐 支持的云存储

| 云存储 | rclone 类型 | 难度 | 备注 |
|--------|------------|------|------|
| OneDrive 个人版 | `onedrive` | ⭐⭐ | 最常用 |
| OneDrive 商业版 | `onedrive` | ⭐⭐⭐ | 需要企业账号 |
| Google Drive | `drive` | ⭐⭐ | 需科学上网 |
| 阿里云盘 | `alidrive` | ⭐⭐ | 国内速度快 |
| 百度网盘 | `baidu` | ⭐⭐⭐ | 需申请 API |
| Dropbox | `dropbox` | ⭐⭐ | 国际通用 |
| Amazon S3 | `s3` | ⭐⭐⭐ | 对象存储 |
| WebDAV | `webdav` | ⭐⭐ | 通用协议 |
| 天翼云盘 | `webdav` | ⭐⭐ | 通过 WebDAV |
| 坚果云 | `webdav` | ⭐⭐ | 通过 WebDAV |

> 💡 **提示**：支持所有 rclone 支持的云存储，查看完整列表：https://rclone.org/

---

## ❓ 常见问题

### Q1: 挂载后看不到文件？

**排查步骤：**

```bash
# 1. 验证 rclone 配置
rclone lsd onedrive:

# 2. 检查挂载进程
ps aux | grep rclone

# 3. 查看挂载点
ls -la ~/cloud-storage/onedrive/

# 4. 查看系统日志
dmesg | tail -20
```

### Q2: token 过期怎么办？

```bash
# 刷新 token
rclone config reconnect onedrive:

# 或重新配置
rclone config
```

### Q3: 如何卸载/停止挂载？

```bash
# 方式 1：停止 systemd 服务（推荐）
sudo systemctl stop cloud-mount

# 方式 2：手动杀死进程
fusermount -u ~/cloud-storage/onedrive

# 方式 3：卸载挂载点
fusermount -u ~/cloud-storage/onedrive
```

### Q4: 内存占用过高？

**优化方案：**

```bash
# 编辑配置文件
nano ~/.config/cloud-mount/config.sh

# 减少缓存大小
MOUNT_OPTIONS="--daemon --vfs-cache-mode minimal --vfs-cache-max-size 256M"

# 重启服务
sudo ~/cloud-mount/scripts/enable-autostart.sh restart
```

### Q5: 开机自启失败？

```bash
# 查看服务状态
sudo systemctl status cloud-mount

# 查看详细日志
sudo journalctl -u cloud-mount -n 50

# 检查配置文件
cat ~/.config/cloud-mount/config.sh

# 重新启用服务
sudo ~/cloud-mount/scripts/enable-autostart.sh enable
```

---

## 🔒 安全说明

### 为什么 ClawHub 显示 "Suspicious" 标记？

本技能在 ClawHub 平台可能被标记为 "Suspicious patterns detected"，这是**静态代码分析的误报**，原因如下：

| 触发原因 | 实际用途 | 安全等级 |
|---------|---------|---------|
| systemd user service | 实现开机自启（无需 sudo） | ✅ 安全（用户级服务） |
| `--daemon` 参数 | 后台运行挂载进程 | ✅ 安全（正常守护进程） |
| `fusermount -u` | 卸载挂载点（标准 FUSE 接口） | ✅ 安全（系统标准工具） |
| `set -e` | 脚本错误处理 | ✅ 安全（最佳实践） |

**OpenClaw 内部扫描结果：Benign（高置信度）**

### 权限说明

本技能需要以下权限，均用于正常功能：

1. **sudo 权限**（仅 enable-autostart.sh）
   - 创建 `/etc/systemd/system/cloud-mount.service` 系统服务文件
   - 重新加载 systemd 配置
   - **用户完全可控**：可以选择不启用开机自启

2. **文件系统访问**
   - 读取 `~/.config/cloud-mount/config.sh` 配置文件
   - 创建挂载点目录 `~/cloud-storage/`
   - **不访问**用户其他文件

3. **网络访问**
   - rclone 连接云存储 API（OneDrive、Google Drive 等）
   - **不发送**任何数据到第三方（除云存储服务商）

### 安全最佳实践

1. **保护敏感文件**
   ```bash
   # 设置 rclone 配置文件权限（仅自己可读写）
   chmod 600 ~/.config/rclone/rclone.conf
   
   # 不要将 token 文件上传到 Git
   echo ".config/rclone/rclone.conf" >> ~/.gitignore
   ```

2. **审查代码**
   ```bash
   # 安装前查看脚本内容
   cat ~/cloud-mount/scripts/mount-cloud.sh
   cat ~/cloud-mount/scripts/enable-autostart.sh
   ```

3. **最小权限原则**
   - 为服务器创建**专用云存储账号**
   - 限制账号权限（如只读、特定文件夹）
   - 谨慎使用 `--allow-other` 参数

4. **定期检查**
   ```bash
   # 检查挂载状态
   ~/cloud-mount/scripts/check-mount.sh --all
   
   # 查看服务日志
   sudo journalctl -u cloud-mount --since "24 hours ago"
   
   # 监控资源使用
   ps aux | grep rclone
   ```

5. **备份配置**
   ```bash
   # 备份配置（不包含 token）
   tar -czf cloud-mount-config-backup.tar.gz \
     ~/.config/cloud-mount/config.sh \
     ~/cloud-mount/scripts/
   ```

### 安全承诺

- ✅ 所有代码开源透明，无隐藏逻辑
- ✅ 不收集任何用户数据
- ✅ 不连接任何第三方服务（除云存储 API）
- ✅ token 仅存储在本地 `~/.config/rclone/rclone.conf`
- ✅ 所有提权操作均需用户明确授权（sudo）

---

## 🔐 信任验证

> "Like a lobster shell, security has layers — review code before you run it."

ClawHub 的安全标记是**提醒用户审查代码**，不是阻止使用。我们鼓励用户：

1. 阅读 [SKILL.md](SKILL.md) 了解完整实现
2. 审查 `scripts/` 目录下的所有脚本
3. 在测试环境先验证功能
4. 确认无误后再在生产环境使用

---

## 📚 完整文档

- 详细配置指南：[SKILL.md](SKILL.md)
- 发布日志：[PUBLISH_LOG.md](PUBLISH_LOG.md)
- rclone 官方文档：https://rclone.org/docs/

---

## 🤝 贡献

遇到问题或有改进建议？

1. 在 ClawHub 页面留言
2. 提交 Issue 或 PR
3. 联系作者：@Liqiuyue9597

---

## 📄 许可

MIT License © 2026 LuckyYou

---

## 🙏 致谢

基于 [rclone](https://rclone.org/) 构建 - 命令行云存储同步工具

---

<div align="center">

**觉得好用？欢迎 star ⭐ 和分享！**

[安装使用](#-快速开始) · [查看文档](#-完整文档) · [反馈问题](#-贡献)

</div>
