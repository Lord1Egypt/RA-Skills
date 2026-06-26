#!/bin/bash
# collect-baseline.sh — OpenEuler 系统基线收集脚本
# 用法: sudo ./collect-baseline.sh [输出目录]
# 收集目标系统的安全相关配置，生成带时间戳的基线快照
# 供 diff-analysis.py 使用

set -euo pipefail

OUTPUT_DIR="${1:-./baseline-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$OUTPUT_DIR"

info() { echo "[INFO] $*"; }
warn() { echo "[WARN] $*" >&2; }

# ---- 系统信息 ----
info "收集系统信息..."
{
    echo "=== 系统发行版 ==="
    cat /etc/openEuler-release 2>/dev/null || cat /etc/os-release 2>/dev/null || echo "N/A"
    echo
    echo "=== 内核版本 ==="
    uname -a
    echo
    echo "=== 主机名 ==="
    hostname
    echo
    echo "=== 运行时间 ==="
    uptime
} > "$OUTPUT_DIR/system-info.txt"

# ---- 安装的包 ----
info "收集已安装软件包列表..."
rpm -qa --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}\n' | sort > "$OUTPUT_DIR/packages.txt"

# ---- 文件系统挂载 ----
info "收集文件系统挂载信息..."
mount > "$OUTPUT_DIR/mounts.txt"
cat /etc/fstab > "$OUTPUT_DIR/fstab.txt" 2>/dev/null || echo "N/A" > "$OUTPUT_DIR/fstab.txt"

# ---- 内核参数 ----
info "收集内核参数..."
SYSCTL_KEYS=(
    net.ipv4.ip_forward
    net.ipv4.conf.all.rp_filter
    net.ipv4.conf.all.accept_redirects
    net.ipv4.conf.all.send_redirects
    net.ipv4.conf.all.secure_redirects
    net.ipv4.tcp_syncookies
    net.ipv4.conf.all.log_martians
    net.ipv4.icmp_echo_ignore_broadcasts
    net.ipv4.icmp_ignore_bogus_error_responses
    net.ipv4.conf.all.accept_source_route
    net.ipv6.conf.all.accept_redirects
    kernel.randomize_va_space
    fs.suid_dumpable
)
for key in "${SYSCTL_KEYS[@]}"; do
    echo "$key = $(sysctl -n "$key" 2>/dev/null || echo 'N/A')"
done > "$OUTPUT_DIR/sysctl-params.txt"

# ---- 加载的内核模块 ----
info "收集已加载的内核模块..."
lsmod > "$OUTPUT_DIR/lsmod.txt"

# ---- 禁用模块检查 ----
info "检查禁用模块配置..."
for mod in cramfs freevxfs hfs hfsplus jffs2 squashfs udf dccp sctp rds tipc; do
    echo "$mod: $(lsmod | grep -c "^$mod " 2>/dev/null || echo 0)"
done > "$OUTPUT_DIR/disabled-modules.txt"

# ---- SSH 配置 ----
info "收集 SSH 服务配置..."
sshd -T 2>/dev/null > "$OUTPUT_DIR/sshd-config.txt" || \
    cat /etc/ssh/sshd_config > "$OUTPUT_DIR/sshd-config.txt" 2>/dev/null || \
    echo "N/A" > "$OUTPUT_DIR/sshd-config.txt"

# ---- SELinux ----
info "收集 SELinux 状态..."
{
    echo "=== getenforce ==="
    getenforce 2>/dev/null || echo "N/A"
    echo
    echo "=== config ==="
    cat /etc/selinux/config 2>/dev/null || echo "N/A"
    echo
    echo "=== SELinux mounts ==="
    mount | grep selinuxfs
} > "$OUTPUT_DIR/selinux.txt"

# ---- 防火墙 ----
info "收集防火墙状态..."
{
    echo "=== firewalld status ==="
    systemctl is-active firewalld 2>/dev/null || echo "inactive"
    echo
    echo "=== firewalld zone ==="
    firewall-cmd --list-all 2>/dev/null || echo "firewalld not running"
    echo
    echo "=== nftables ==="
    nft list ruleset 2>/dev/null || echo "nftables not active"
} > "$OUTPUT_DIR/firewall.txt"

# ---- 服务状态 ----
info "收集关键服务状态..."
SERVICES=(auditd rsyslog crond sshd firewalld)
for svc in "${SERVICES[@]}"; do
    enabled=$(systemctl is-enabled "$svc" 2>/dev/null || echo 'unknown')
    active=$(systemctl is-active "$svc" 2>/dev/null || echo 'unknown')
    echo "$svc: enabled=$enabled active=$active"
done > "$OUTPUT_DIR/services.txt"

# ---- auditd ----
info "收集 auditd 配置..."
{
    echo "=== auditd.conf ==="
    cat /etc/audit/auditd.conf 2>/dev/null || echo "N/A"
    echo
    echo "=== audit rules ==="
    auditctl -l 2>/dev/null || echo "N/A"
    echo
    echo "=== audit.rules file ==="
    cat /etc/audit/rules.d/*.rules 2>/dev/null || echo "N/A"
} > "$OUTPUT_DIR/auditd.txt"

# ---- rsyslog ----
info "收集 rsyslog 配置..."
{
    echo "=== rsyslog.conf ==="
    cat /etc/rsyslog.conf 2>/dev/null || echo "N/A"
    echo
    echo "=== rsyslog.d ==="
    cat /etc/rsyslog.d/*.conf 2>/dev/null || echo "N/A"
    echo
    echo "=== logrotate ==="
    cat /etc/logrotate.conf 2>/dev/null || echo "N/A"
    echo
    echo "=== log dirs ==="
    ls -la /var/log/ 2>/dev/null
} > "$OUTPUT_DIR/logging.txt"

# ---- 密码策略 ----
info "收集密码策略..."
{
    echo "=== login.defs ==="
    grep -E '^PASS_|^ENCRYPT_' /etc/login.defs 2>/dev/null || echo "N/A"
    echo
    echo "=== pwquality ==="
    cat /etc/security/pwquality.conf 2>/dev/null || echo "N/A"
    echo
    echo "=== faillock ==="
    cat /etc/security/faillock.conf 2>/dev/null || echo "N/A"
    echo
    echo "=== shadow (users only) ==="
    awk -F: '($2 != "*" && $2 != "!!"){print $1": "substr($2,1,3)"..."}' /etc/shadow 2>/dev/null | head -20 || echo "N/A"
    echo
    echo "=== passwd (UID 0) ==="
    awk -F: '($3 == 0){print $1}' /etc/passwd 2>/dev/null
    echo
    echo "=== 空密码用户检查 ==="
    awk -F: '($2 == ""){print $1}' /etc/shadow 2>/dev/null || echo "none"
} > "$OUTPUT_DIR/password-policy.txt"

# ---- sudo ----
info "收集 sudo 配置..."
{
    echo "=== sudoers ==="
    cat /etc/sudoers 2>/dev/null || echo "N/A"
    echo
    echo "=== sudoers.d ==="
    cat /etc/sudoers.d/* 2>/dev/null || echo "N/A"
    echo
    echo "=== sudo 版本 ==="
    sudo --version 2>/dev/null | head -1 || echo "N/A"
} > "$OUTPUT_DIR/sudo.txt"

# ---- 定时任务 ----
info "收集定时任务..."
{
    echo "=== crontabs ==="
    for dir in cron.hourly cron.daily cron.weekly cron.monthly cron.d; do
        echo "[$dir permissions]"
        stat /etc/$dir 2>/dev/null | grep Access | head -1
    done
    echo
    echo "=== crontab root ==="
    crontab -u root -l 2>/dev/null || echo "no crontab for root"
    echo
    echo "=== /etc/crontab ==="
    cat /etc/crontab 2>/dev/null || echo "N/A"
    echo
    echo "=== at.deny ==="
    cat /etc/at.deny 2>/dev/null || echo "not present"
    echo
    echo "=== cron.deny ==="
    cat /etc/cron.deny 2>/dev/null || echo "not present"
} > "$OUTPUT_DIR/cron-jobs.txt"

# ---- 警告横幅 ----
info "收集登录横幅..."
{
    echo "=== /etc/issue ==="
    cat /etc/issue 2>/dev/null || echo "N/A"
    echo "=== permissions ==="
    stat /etc/issue 2>/dev/null | grep Access | head -1 || echo "N/A"
    echo
    echo "=== /etc/issue.net ==="
    cat /etc/issue.net 2>/dev/null || echo "N/A"
} > "$OUTPUT_DIR/banners.txt"

# ---- 用户/组 ----
info "收集用户和组信息..."
{
    echo "=== /etc/passwd user list ==="
    awk -F: '{print $1": uid="$3", gid="$4", shell="$7}' /etc/passwd
    echo
    echo "=== 用户 home 目录 .forward 文件 ==="
    find /home -name .forward 2>/dev/null || echo "none"
    echo
    echo "=== 组 ==="
    grep -E '^root:' /etc/group
} > "$OUTPUT_DIR/users-groups.txt"

# ---- UEFI / 安全启动 ----
info "收集 UEFI/安全启动信息..."
{
    echo "=== Secure Boot ==="
    mokutil --sb-state 2>/dev/null || echo "N/A (not UEFI or mokutil not found)"
    echo
    echo "=== Boot params ==="
    cat /proc/cmdline 2>/dev/null || echo "N/A"
} > "$OUTPUT_DIR/uefi.txt"

# ---- 签名校验 ----
{
    echo "=== 生成时间戳 ==="
    date -u '+%Y-%m-%dT%H:%M:%SZ'
    echo
    echo "=== 收集文件的 SHA256 ==="
    find "$OUTPUT_DIR" -type f -name '*.txt' | sort | while read -r f; do
        sha256sum "$f" | awk '{print $2"  "$1}'
    done
} > "$OUTPUT_DIR/checksums.txt"

info "基线收集完成: $OUTPUT_DIR"
echo "报告文件："
ls -lh "$OUTPUT_DIR"/*.txt
