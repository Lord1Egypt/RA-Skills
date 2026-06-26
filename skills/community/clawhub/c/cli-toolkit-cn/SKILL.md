---
name: cli-toolkit-cn
version: 1.0.0
description: 命令行工具箱 - 常用命令速查、脚本生成、效率提升。适合：开发者、运维工程师、终端爱好者。
metadata:
  openclaw:
    emoji: "⌨️"
    requires:
      bins: []
---

# 命令行工具箱 Skill

常用命令速查、脚本生成、终端效率提升。

## 核心功能

| 功能 | 描述 |
|------|------|
| 命令速查 | 常用命令快速查询 |
| 脚本生成 | 自动生成 Shell 脚本 |
| 效率技巧 | 终端使用技巧 |
| 问题排查 | 常见错误解决 |

## 使用方法

### 查询命令

```
怎么查看 Linux 磁盘使用情况
```

### 生成脚本

```
生成一个批量重命名文件的脚本
```

### 问题排查

```
命令报错 permission denied 怎么解决
```

## 常用命令速查

### 文件操作

```bash
# 查找文件
find /path -name "*.txt"           # 按名称
find /path -type f -mtime -7       # 7天内修改
find /path -size +100M             # 大于 100M

# 搜索内容
grep -r "keyword" /path            # 递归搜索
grep -i "keyword" file.txt         # 忽略大小写
grep -A 5 -B 5 "keyword" file.txt  # 显示上下文

# 文件操作
cp -r source/ dest/                # 复制目录
mv oldname newname                 # 重命名
rm -rf directory/                  # 删除目录
touch file.txt                     # 创建文件
mkdir -p path/to/dir               # 创建多级目录

# 文件权限
chmod 755 script.sh                # 设置权限
chmod +x script.sh                 # 添加执行权限
chown user:group file              # 更改所有者

# 查看文件
cat file.txt                       # 查看全部
head -n 20 file.txt                # 前 20 行
tail -n 20 file.txt                # 后 20 行
tail -f log.txt                    # 实时查看
less file.txt                      # 分页查看
wc -l file.txt                     # 统计行数
```

### 系统信息

```bash
# 系统信息
uname -a                           # 系统信息
hostname                           # 主机名
uptime                             # 运行时间
date                               # 当前时间
cal                                # 日历

# CPU 信息
lscpu                              # CPU 详情
nproc                              # CPU 核心数
top                                # 进程监控
htop                               # 增强版 top

# 内存信息
free -h                            # 内存使用
cat /proc/meminfo                  # 详细内存

# 磁盘信息
df -h                              # 磁盘使用
du -sh *                           # 目录大小
du -h --max-depth=1                # 一级目录大小
lsblk                              # 块设备
```

### 进程管理

```bash
# 查看进程
ps aux                             # 所有进程
ps aux | grep python               # 过滤进程
pgrep -f "python script.py"        # 按名称查找
top                                # 动态监控

# 进程控制
kill PID                           # 终止进程
kill -9 PID                        # 强制终止
killall python                     # 按名称终止
pkill -f "script.py"               # 按命令匹配

# 后台运行
nohup python script.py &           # 后台运行
nohup python script.py > log.txt 2>&1 &  # 输出到文件
disown                             # 脱离终端
jobs                               # 查看后台任务
fg %1                              # 前台运行
```

### 网络命令

```bash
# 网络信息
ifconfig                           # 网络接口
ip addr                            # IP 地址
hostname -I                        # 本机 IP
curl ifconfig.me                   # 公网 IP

# 网络测试
ping google.com                    # 测试连通
curl -I https://example.com        # HTTP 头
wget https://example.com/file      # 下载文件
nc -zv host port                   # 测试端口

# 网络监控
netstat -tuln                      # 监听端口
netstat -anp                       # 所有连接
lsof -i :80                        # 占用端口的进程
ss -tuln                           # 现代版 netstat
```

### 文本处理

```bash
# sed 文本替换
sed 's/old/new/g' file.txt         # 替换
sed -i 's/old/new/g' file.txt      # 原地替换
sed '/pattern/d' file.txt          # 删除匹配行

# awk 文本处理
awk '{print $1}' file.txt          # 打印第一列
awk -F, '{print $1,$2}' file.csv   # CSV 处理
awk '{sum+=$1} END {print sum}' file.txt  # 求和

# cut 提取字段
cut -d, -f1,3 file.csv             # 提取第 1,3 列
cut -c1-10 file.txt                # 提取 1-10 字符

# sort 排序
sort file.txt                      # 排序
sort -n file.txt                   # 数字排序
sort -k2 -n file.txt               # 按第 2 列数字排序
sort -u file.txt                   # 排序并去重

# uniq 去重
sort file.txt | uniq               # 去重
sort file.txt | uniq -c            # 统计重复次数
```

## 实用脚本模板

### 批量重命名

```bash
#!/bin/bash
# 批量重命名：添加前缀

for file in *.jpg; do
  mv "$file" "prefix_$file"
done

# 或者使用 rename
rename 's/^/prefix_/' *.jpg
```

### 批量处理

```bash
#!/bin/bash
# 批量处理文件

for file in *.txt; do
  echo "Processing $file..."
  # 处理逻辑
  sed -i 's/old/new/g' "$file"
done
```

### 监控脚本

```bash
#!/bin/bash
# 监控磁盘空间

THRESHOLD=80
ALERT_EMAIL="admin@example.com"

df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }' | while read output; do
  usep=$(echo $output | awk '{ print $1}' | cut -d'%' -f1)
  partition=$(echo $output | awk '{ print $2 }')
  if [ $usep -ge $THRESHOLD ]; then
    echo "Warning: $partition is ${usep}% full" | mail -s "Disk Space Alert" $ALERT_EMAIL
  fi
done
```

### 备份脚本

```bash
#!/bin/bash
# 自动备份

BACKUP_DIR="/backup"
SOURCE_DIR="/data"
DATE=$(date +%Y%m%d)
BACKUP_FILE="backup_$DATE.tar.gz"

# 创建备份
tar -czf "$BACKUP_DIR/$BACKUP_FILE" "$SOURCE_DIR"

# 删除 7 天前的备份
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE"
```

## 效率技巧

### 命令别名

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc

# 常用别名
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Git 别名
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'
alias gd='git diff'

# 快捷命令
alias ports='netstat -tulanp'
alias myip='curl -s ifconfig.me'
alias weather='curl wttr.in'
alias sha='shasum -a 256'
alias www='python3 -m http.server 8000'
```

### 历史命令

```bash
# 搜索历史
history | grep "keyword"           # 搜索历史
Ctrl+R                             # 交互式搜索
!!                                 # 上一条命令
!$                                 # 上一条命令的最后一个参数
!*                                 # 上一条命令的所有参数
!n                                 # 第 n 条历史命令
```

### 管道技巧

```bash
# 组合使用
cat file.txt | grep "error" | wc -l       # 统计错误数
ps aux | grep python | awk '{print $2}'   # 获取 PID
find . -name "*.log" | xargs rm           # 批量删除
curl -s URL | jq '.data[].name'          # JSON 处理

# 输出重定向
command > output.txt               # 覆盖
command >> output.txt              # 追加
command 2>&1                      # 错误也输出
command > /dev/null 2>&1          # 丢弃所有输出
```

## 常见问题解决

### Permission Denied

```bash
# 方案 1：添加执行权限
chmod +x script.sh

# 方案 2：使用 bash 运行
bash script.sh

# 方案 3：使用 sudo
sudo ./script.sh
```

### Command Not Found

```bash
# 检查 PATH
echo $PATH

# 查找命令位置
which command_name
whereis command_name

# 安装缺失命令
# Ubuntu/Debian
sudo apt install package_name

# CentOS/RHEL
sudo yum install package_name

# macOS
brew install package_name
```

### 端口被占用

```bash
# 查找占用进程
lsof -i :8080

# 终止进程
kill -9 $(lsof -t -i:8080)
```

### 磁盘空间不足

```bash
# 查找大文件
find / -type f -size +100M 2>/dev/null

# 清理日志
sudo rm -rf /var/log/*.log

# 清理缓存
sudo apt clean          # Ubuntu/Debian
sudo yum clean all      # CentOS/RHEL

# 清理旧文件
find /tmp -type f -mtime +7 -delete
```

## 注意事项

- 危险命令先测试（rm、mv）
- 重要操作先备份
- 使用 sudo 时小心
- 记录常用命令

---

创建：2026-03-12
版本：1.0