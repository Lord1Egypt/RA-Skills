# CIS RHEL Benchmark → OpenEuler 检查项映射

本文件是 skill 的核心配置源。每个 CIS Benchmark 检查项映射到 OpenEuler 上可执行的等效检查命令。

## 映射格式

```yaml
# CIS 编号: <CIS编号>
# 标题: <检查项名称>
# 等级: L1/L2
# RHEL 预期值: <期望的配置值>
# OpenEuler 等效检查: <命令或脚本>
# 状态: auto/manual/N/A
# 备注: <差异说明>
```

## 级别 1 — 系统级安全

### 1.1 文件系统配置

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 1.1.1.1 | 禁用 unused filesystems (cramfs) | cramfs 未加载 | `lsmod | grep cramfs || modprobe -n -v cramfs` | auto | 命令一致 |
| 1.1.1.2 | 禁用 unused filesystems (freevxfs) | freevxfs 未加载 | `lsmod | grep freevxfs` | auto | 命令一致 |
| 1.1.1.3 | 禁用 unused filesystems (hfs) | hfs 未加载 | `lsmod | grep hfs` | auto | 命令一致 |
| 1.1.1.4 | 禁用 unused filesystems (hfsplus) | hfsplus 未加载 | `lsmod | grep hfsplus` | auto | 命令一致 |
| 1.1.1.5 | 禁用 unused filesystems (jffs2) | jffs2 未加载 | `lsmod | grep jffs2` | auto | 命令一致 |
| 1.1.1.6 | 禁用 unused filesystems (squashfs) | squashfs 未加载 | `lsmod | grep squashfs` | auto | 命令一致 |
| 1.1.1.7 | 禁用 unused filesystems (udf) | udf 未加载 | `lsmod | grep udf` | auto | 命令一致 |
| 1.1.2 | 独立 /tmp 分区 | /tmp 有单独分区 | `mount | grep -E '\s/tmp\s'` | auto | 命令一致 |
| 1.1.3 | /tmp 启用 nodev | nodev 选项已设置 | `mount | grep -E '\s/tmp\s' | grep nodev` | auto | 命令一致 |
| 1.1.4 | /tmp 启用 nosuid | nosuid 选项已设置 | `mount | grep -E '\s/tmp\s' | grep nosuid` | auto | 命令一致 |
| 1.1.5 | /tmp 启用 noexec | noexec 选项已设置 | `mount | grep -E '\s/tmp\s' | grep noexec` | auto | 命令一致 |
| 1.1.6 | 独立 /var 分区 | /var 有单独分区 | `mount | grep -E '\s/var\s'` | auto | 命令一致 |
| 1.1.7 | 独立 /var/tmp 分区 | /var/tmp 有单独分区 | `mount | grep -E '\s/var/tmp\s'` | auto | 命令一致 |
| 1.1.8 | 独立 /var/log 分区 | /var/log 有单独分区 | `mount | grep -E '\s/var/log\s'` | auto | 命令一致 |
| 1.1.9 | 独立 /var/log/audit 分区 | /var/log/audit 有单独分区 | `mount | grep -E '\s/var/log/audit\s'` | auto | 命令一致 |
| 1.1.10 | 独立 /home 分区 | /home 有单独分区 | `mount | grep -E '\s/home\s'` | auto | 命令一致 |
| 1.1.11 | /home 启用 nodev | nodev 选项已设置 | `mount | grep -E '\s/home\s' | grep nodev` | auto | 命令一致 |
| 1.1.12 | /home 启用 nosuid | nosuid 选项已设置 | `mount | grep -E '\s/home\s' | grep nosuid` | auto | 命令一致 |

### 1.2 软件包配置

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 1.2.1 | 配置 GPG 密钥 | 已配置 | `rpm -q gpg-pubkey --qf '%{name}-%{version}-%{release} --> %{summary}\n'` | auto | 包管理器一致 |
| 1.2.2 | 配置 gpgcheck | gpgcheck=1 | `grep ^gpgcheck /etc/yum.repos.d/*.repo` | auto | OpenEuler 使用 dnf/yum |
| 1.2.3 | 配置 repo 源 | 仓库已配置 | `dnf repolist` | auto | dnf 兼容 |
| 1.2.4 | 更新系统 | 最新 | `dnf check-update` | auto | dnf 兼容 |

### 1.3 文件系统完整性检查

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 1.3.1 | AIDE 安装 | aide 已安装 | `rpm -q aide` | auto | OpenEuler 提供 aide 包 |
| 1.3.2 | AIDE 定时执行 | cron 已配置 | `crontab -u root -l | grep aide` | auto | 命令一致 |

### 1.4 安全启动与引导配置

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 1.4.1 | 配置 GRUB2 密码 | 已设置 | `grep ^set superusers /boot/grub2/grub.cfg` | auto | GRUB2 配置一致 |
| 1.4.2 | 单用户模式需认证 | 需密码 | `grep ^SINGLE /etc/sysconfig/init` | auto | 命令一致 |
| 1.4.3 | 禁用交互式引导 | 已禁用 | `grep ^PROMPT /etc/sysconfig/init` | auto | 命令一致 |

### 1.5 额外进程加固

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 1.5.1 | core dump 限制 | hard core 0 | `grep 'hard core' /etc/security/limits.conf` | auto | 配置一致 |
| 1.5.2 | XD/NX 支持 | 已启用 | `dmesg | grep -i 'NX\|XD'` | auto | 需 cpu 支持 |
| 1.5.3 | ASLR 启用 | 2 | `sysctl kernel.randomize_va_space` | auto | 值应为 2 |
| 1.5.4 | 关闭 PRELINK | 未安装 | `rpm -q prelink | grep 'not installed'` | auto | 多数系统无此包 |

### 1.6 SELinux

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 1.6.1.1 | SELinux 已安装 | selinux 已安装 | `rpm -q libselinux` | auto | OpenEuler 包含 SELinux |
| 1.6.1.2 | SELinux 未禁用 | enforcing/permissive | `grep SELINUX=disabled /etc/selinux/config` | auto | 值不应为 disabled |
| 1.6.1.3 | SELinux 启动模式 | enforcing/permissive | `getenforce` | auto | 命令一致 |
| 1.6.1.4 | SELinux 策略类型 | targeted | `grep SELINUXTYPE /etc/selinux/config` | auto | 值应为 targeted |
| 1.6.2 | SELinux 拒绝日志 | 已启用 | `ausearch -m avc | head -5` | auto | auditd 必须运行 |

### 1.7 警告横幅

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 1.7.1 | 配置登录警告 | 已设置 | `cat /etc/issue` | auto | 文件路径一致 |
| 1.7.2 | 配置远程登录警告 | 已设置 | `cat /etc/issue.net` | auto | 文件路径一致 |
| 1.7.3 | 权限设置 | 644 | `stat /etc/issue` | auto | 权限应一致 |

### 1.8 更新与补丁

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 1.8.1 | 系统更新 | 无可用更新 | `dnf check-update --quiet` | auto | dnf 兼容 |
| 1.8.2 | GPG 密钥更新 | 已配置 | `rpm -q gpg-pubkey` | auto | OpenEuler 有自己的 GPG 密钥 |

## 级别 2 — 服务安全

### 2.1 定时任务

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 2.1.1 | cron daemon | 已启用 | `systemctl is-enabled crond` | auto | 服务名一致 |
| 2.1.2 | crontab 权限 | 600/700 | `stat /etc/crontab` | auto | 命令一致 |
| 2.1.3 | cron 小时目录权限 | 700 | `stat /etc/cron.hourly` | auto | 命令一致 |
| 2.1.4 | cron 每日目录权限 | 700 | `stat /etc/cron.daily` | auto | 命令一致 |
| 2.1.5 | cron 每周目录权限 | 700 | `stat /etc/cron.weekly` | auto | 命令一致 |
| 2.1.6 | cron 每月目录权限 | 700 | `stat /etc/cron.monthly` | auto | 命令一致 |
| 2.1.7 | cron.d 权限 | 700 | `stat /etc/cron.d` | auto | 命令一致 |
| 2.1.8 | at/cron 限制 | 仅 root | `stat /etc/cron.deny; stat /etc/at.deny` | auto | 文件路径一致 |

### 2.2 SSH 服务

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 2.2.1 | SSH 协议版本 | 2 | `grep ^Protocol /etc/ssh/sshd_config` | auto | 值应为 2 |
| 2.2.2 | LogLevel | INFO/VERBOSE | `grep ^LogLevel /etc/ssh/sshd_config` | auto | 值应为 INFO 以上 |
| 2.2.3 | X11Forwarding | no | `grep ^X11Forwarding /etc/ssh/sshd_config` | auto | 值应为 no |
| 2.2.4 | MaxAuthTries | ≤ 4 | `grep ^MaxAuthTries /etc/ssh/sshd_config` | auto | 值应 ≤ 4 |
| 2.2.5 | IgnoreRhosts | yes | `grep ^IgnoreRhosts /etc/ssh/sshd_config` | auto | 值应为 yes |
| 2.2.6 | HostbasedAuthentication | no | `grep ^HostbasedAuthentication /etc/ssh/sshd_config` | auto | 值应为 no |
| 2.2.7 | PermitRootLogin | no | `grep ^PermitRootLogin /etc/ssh/sshd_config` | auto | 值应为 no |
| 2.2.8 | PermitEmptyPasswords | no | `grep ^PermitEmptyPasswords /etc/ssh/sshd_config` | auto | 值应为 no |
| 2.2.9 | PermitUserEnvironment | no | `grep ^PermitUserEnvironment /etc/ssh/sshd_config` | auto | 值应为 no |
| 2.2.10 | Ciphers | 强加密算法 | `sshd -T | grep ciphers` | auto | 应排除弱算法 |
| 2.2.11 | MACs | 强 MAC 算法 | `sshd -T | grep macs` | auto | 应排除弱算法 |
| 2.2.12 | ClientAliveInterval | ≤ 300 | `grep ^ClientAliveInterval /etc/ssh/sshd_config` | auto | 值应 ≤ 300 |
| 2.2.13 | ClientAliveCountMax | ≤ 3 | `grep ^ClientAliveCountMax /etc/ssh/sshd_config` | auto | 值应 ≤ 3 |
| 2.2.14 | LoginGraceTime | ≤ 60 | `grep ^LoginGraceTime /etc/ssh/sshd_config` | auto | 值应 ≤ 60 |
| 2.2.15 | 允许用户 | 限制 | `grep ^AllowUsers /etc/ssh/sshd_config` | auto | 建议配置 |
| 2.2.16 | 允许组 | 限制 | `grep ^AllowGroups /etc/ssh/sshd_config` | auto | 建议配置 |

### 2.3 身份识别服务

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 2.3.1 | NIS Client | 未安装 | `rpm -q ypbind` | auto | OpenEuler 包名一致 |
| 2.3.2 | NIS Server | 未安装 | `rpm -q ypserv` | auto | 命令一致 |
| 2.3.3 | rsh Client | 未安装 | `rpm -q rsh` | auto | OpenEuler 可能不含此包 |
| 2.3.4 | rsh Server | 未安装 | `rpm -q rsh-server` | auto | 命令一致 |
| 2.3.5 | talk | 未安装 | `rpm -q talk` | auto | 命令一致 |
| 2.3.6 | telnet Client | 未安装 | `rpm -q telnet` | auto | 命令一致 |
| 2.3.7 | telnet Server | 未安装 | `rpm -q telnet-server` | auto | 命令一致 |
| 2.3.8 | LDAP Client | 未安装 | `rpm -q openldap-clients` | auto | 命令一致 |

## 级别 3 — 网络与防火墙

### 3.1 网络参数

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 3.1.1 | IP 转发禁用 | 0 | `sysctl net.ipv4.ip_forward` | auto | 值应为 0 |
| 3.1.2 | 源路由验证 | 1 | `sysctl net.ipv4.conf.all.rp_filter` | auto | 值应为 1 |
| 3.1.3 | ICMP redirect 不接受 | 0 | `sysctl net.ipv4.conf.all.accept_redirects` | auto | 值应为 0 |
| 3.1.4 | ICMP redirect 不发送 | 0 | `sysctl net.ipv4.conf.all.send_redirects` | auto | 值应为 0 |
| 3.1.5 | 禁用 secure icmp redirect | 0 | `sysctl net.ipv4.conf.all.secure_redirects` | auto | 值应为 0 |
| 3.1.6 | SYN cookies | 1 | `sysctl net.ipv4.tcp_syncookies` | auto | 值应为 1, OpenEuler 可能默认未开启 |
| 3.1.7 | 日志伪造包 | 1 | `sysctl net.ipv4.conf.all.log_martians` | auto | 值应为 1 |
| 3.1.8 | 忽略 ICMP 请求 | 1 | `sysctl net.ipv4.icmp_echo_ignore_broadcasts` | auto | 值应为 1 |
| 3.1.9 | 忽略所有 ICMP | 0 | `sysctl net.ipv4.icmp_ignore_bogus_error_responses` | auto | 值应为 1 |
| 3.1.10 | TCP SYN backlog | 已设 | `sysctl net.ipv4.tcp_syn_backlog` | auto | 查看当前值 |

### 3.2 防火墙

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 3.2.1 | firewalld 安装 | 已安装 | `rpm -q firewalld` | auto | OpenEuler 使用 firewalld |
| 3.2.2 | firewalld 启用 | 已启用运行 | `systemctl is-enabled firewalld; systemctl is-active firewalld` | auto | 命令一致 |
| 3.2.3 | nftables | 可选 | `rpm -q nftables` | auto | nftables 可选 |
| 3.2.4 | 默认区域策略 | drop | `firewall-cmd --list-all` | auto | 策略应适度 |

### 3.3 网络协议禁用

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 3.3.1 | DCCP 禁用 | 未加载 | `modprobe -n -v dccp` | auto | 命令一致 |
| 3.3.2 | SCTP 禁用 | 未加载 | `modprobe -n -v sctp` | auto | 命令一致 |
| 3.3.3 | RDS 禁用 | 未加载 | `modprobe -n -v rds` | auto | 命令一致 |
| 3.3.4 | TIPC 禁用 | 未加载 | `modprobe -n -v tipc` | auto | 命令一致 |

## 级别 4 — 日志与审计

### 4.1 auditd

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 4.1.1.1 | auditd 安装 | 已安装 | `rpm -q audit` | auto | 命令一致 |
| 4.1.1.2 | auditd 启用 | 已启用运行 | `systemctl is-enabled auditd; systemctl is-active auditd` | auto | 命令一致 |
| 4.1.1.3 | audit 日志保留 | rotate 90 days | `grep max_log_file_action /etc/audit/auditd.conf` | auto | 天数可能不同 |
| 4.1.1.4 | audit 日志大小 | 已设 | `grep max_log_file /etc/audit/auditd.conf` | auto | 查看当前值 |
| 4.1.2 | audit 规则收集 | 已配置 | `auditctl -l` | auto | 命令一致 |
| 4.1.3 | 时间变更审计 | 已配置 | `auditctl -l | grep -i time` | auto | 命令一致 |
| 4.1.4 | 用户/组变更审计 | 已配置 | `auditctl -l | grep -E 'etc/(passwd|shadow|group)'` | auto | 命令一致 |
| 4.1.5 | 网络环境变更审计 | 已配置 | `auditctl -l | grep -i network` | auto | 命令一致 |
| 4.1.6 | 权限变更审计 | 已配置 | `auditctl -l | grep -i perm_mod` | auto | 命令一致 |
| 4.1.7 | 非授权访问尝试审计 | 已配置 | `auditctl -l | grep -i 'access\|auid'` | auto | 命令一致 |
| 4.1.8 | mount 系统调用审计 | 已配置 | `auditctl -l | grep mount` | auto | 命令一致 |
| 4.1.9 | 文件删除审计 | 已配置 | `auditctl -l | grep delete` | auto | 命令一致 |
| 4.1.10 | SELinux 上下文审计 | 已配置 | `auditctl -l | grep selinux` | auto | 命令一致 |
| 4.1.11 | 特权命令审计 | 已配置 | `auditctl -l | grep -i 'setuid\|setgid\|euid\|egid'` | auto | 命令一致 |
| 4.1.12 | 文件挂载审计 | 已配置 | `auditctl -l | grep 'mount'` | auto | 命令一致 |

### 4.2 rsyslog

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 4.2.1.1 | rsyslog 安装 | 已安装 | `rpm -q rsyslog` | auto | 命令一致 |
| 4.2.1.2 | rsyslog 启用 | 已启用运行 | `systemctl is-enabled rsyslog; systemctl is-active rsyslog` | auto | 命令一致 |
| 4.2.1.3 | 远程日志 | 已配置 | `grep '^*.*\s*@' /etc/rsyslog.conf` | auto | 命令一致 |
| 4.2.1.4 | rsyslog 日志文件权限 | 640 | `stat /var/log/messages` | auto | 命令一致 |
| 4.2.2 | syslog-ng | 可选 | `rpm -q syslog-ng` | auto | 可选替代 |

### 4.3 日志轮转

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 4.3.1 | logrotate 安装 | 已安装 | `rpm -q logrotate` | auto | 命令一致 |
| 4.3.2 | logrotate 配置 | 已配置 | `cat /etc/logrotate.conf` | auto | 文件路径一致 |

## 级别 5 — 访问控制、认证与授权

### 5.1 密码策略

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 5.1.1 | 密码过期天数 | ≤ 365 | `grep PASS_MAX_DAYS /etc/login.defs` | auto | 命令一致 |
| 5.1.2 | 密码最短天数 | ≥ 7 | `grep PASS_MIN_DAYS /etc/login.defs` | auto | 命令一致 |
| 5.1.3 | 密码长度 | ≥ 14 | `grep PASS_MIN_LEN /etc/login.defs` | auto | OpenEuler 使用 pwquality |
| 5.1.4 | 密码复杂度 | minclass ≥ 4 | `grep minclass /etc/security/pwquality.conf` | auto | 命令一致 |
| 5.1.5 | 密码 hash 算法 | SHA512 | `grep ENCRYPT_METHOD /etc/login.defs` | auto | 值应为 SHA512 |
| 5.1.6 | 账户锁定策略 | 3 次失败锁定 | `grep deny /etc/security/faillock.conf` | auto | 命令一致 |

### 5.2 用户与组

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 5.2.1 | 无空密码用户 | 无 | `awk -F: '($2 == "")' /etc/shadow` | auto | 命令一致 |
| 5.2.2 | root 唯一 UID 0 | 仅 root | `awk -F: '($3 == 0)' /etc/passwd` | auto | 应只有 root |
| 5.2.3 | root 组 GID 0 | 仅 root | `awk -F: '($1 == "root")' /etc/group` | auto | 命令一致 |
| 5.2.4 | .forward 文件 | 无 | `find /home -name .forward` | auto | 不应存在 |
| 5.2.5 | 默认组 | 正确 | `grep DEFAULT_HOME /etc/login.defs` | auto | 命令一致 |

### 5.3 sudo

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 5.3.1 | sudo 安装 | 已安装 | `rpm -q sudo` | auto | 命令一致 |
| 5.3.2 | sudo 配置 | 安全 | `visudo -c -f /etc/sudoers` | auto | 命令一致 |
| 5.3.3 | sudo 日志 | 已配置 | `grep logfile /etc/sudoers` | auto | 应配置日志 |
| 5.3.4 | sudo 超时 | ≤ 15 min | `grep timestamp_timeout /etc/sudoers` | auto | 值应 ≤ 15 |

### 5.4 UEFI 安全启动

| CIS 编号 | 标题 | RHEL 预期值 | OpenEuler 等效检查 | 状态 | 备注 |
|----------|------|-------------|-------------------|------|------|
| 5.4.1 | UEFI 安全启动 | 已启用 | `mokutil --sb-state` | auto | 命令一致 |
| 5.4.2 | shim 安装 | 已安装 | `rpm -q shim` | auto | OpenEuler 使用 shim |

## 非映射项说明

以下 CIS 检查项在 OpenEuler 上无直接等效项，需手动验证或标记为 N/A：

| CIS 编号 | 标题 | 说明 |
|----------|------|------|
| 1.4.4 | GRUB2 密码 (UEFI) | OpenEuler UEFI 引导配置路径可能不同 |
| 3.6.x | iptables/nftables 细则 | 需根据实际防火墙方案确认 |
| 4.2.1.5 | 远程日志配置 | 取决于实际 syslog 服务器地址 |
| 5.1.7 | libuser 密码策略 | libuser 可能未安装 |

## 维护提示

- 新增检查项时，务必添加 `状态` 标记（auto/manual/N/A）
- `auto`：差异分析脚本可自动判定通过/失败
- `manual`：需要人工判断
- `N/A`：OpenEuler 上不适用
- 定期根据新的 CIS Benchmark 版本更新此映射表
