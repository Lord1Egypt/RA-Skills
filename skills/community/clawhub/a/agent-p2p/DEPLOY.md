# Agent P2P 部署踩坑指南

## 前置检查清单

### 1. 域名解析

**必须完成：** 在域名服务商处添加 A 记录

```
类型: A
主机: @ 或 www
值: VPS 的 IP 地址
TTL: 600（10分钟）
```

**验证解析：**
```bash
nslookup your-domain.com
# 应该返回你的 VPS IP
```

**常见问题：**
- ❌ DNS 未生效就部署 → SSL 证书申请失败
- ✅ 等待 5-10 分钟，确认解析成功后再部署

---

### 2. 防火墙设置

#### 2.1 云服务商安全组（必须）

**腾讯云：**
```bash
# 控制台 → 安全组 → 入站规则
TCP 22    # SSH
TCP 80    # HTTP
TCP 443   # HTTPS
```

**阿里云：**
```bash
# 控制台 → 安全组 → 入方向
允许 22/22    # SSH
允许 80/80    # HTTP
允许 443/443  # HTTPS
```

**AWS：**
```bash
# EC2 → Security Groups → Inbound rules
Type: SSH, HTTP, HTTPS
Source: 0.0.0.0/0
```

#### 2.2 系统防火墙

**Ubuntu（ufw）：**
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

**CentOS（firewalld）：**
```bash
sudo firewall-cmd --permanent --add-port=22/tcp
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

**常见问题：**
- ❌ 只开了云防火墙，没开系统防火墙 → 连接失败
- ❌ 端口冲突（如 80 被 Nginx 占用）→ 部署失败
- ✅ 两者都要开放

---

### 3. SSH 密钥

**生成密钥：**
```bash
ssh-keygen -t ed25519 -C "agent-p2p" -f ~/.ssh/agent-p2p
# 不要设置密码（直接回车）
```

**复制公钥到 VPS：**
```bash
ssh-copy-id -i ~/.ssh/agent-p2p.pub ubuntu@your-vps-ip
```

**验证免密登录：**
```bash
ssh -i ~/.ssh/agent-p2p ubuntu@your-vps-ip
# 应该无需密码直接登录
```

**常见问题：**
- ❌ 密钥权限 644 → SSH 拒绝
- ✅ 必须是 600：`chmod 600 ~/.ssh/agent-p2p`
- ❌ 设置了密钥密码 → 自动化脚本卡住
- ✅ 生成时不要设置密码

---

### 4. VPS 系统要求

**推荐：** Ubuntu 20.04/22.04 LTS

**最低配置：**
- 1 vCPU
- 1GB 内存
- 10GB 磁盘

**检查：**
```bash
# 内存
free -h

# 磁盘
df -h

# 系统版本
cat /etc/os-release
```

---

## 部署流程

### 自动部署（推荐）

Agent 会自动执行以下步骤：

1. **检查域名解析**
   - 等待 DNS 生效
   - 超时 5 分钟则提示用户检查 DNS

2. **检查防火墙**
   - 检测云服务商
   - 提示开放端口命令

3. **SSH 连接测试**
   - 验证免密登录
   - 检查密钥权限

4. **安装依赖**
   - Python3、pip、Nginx、Certbot

5. **部署代码**
   - 从 GitHub 拉取
   - 安装 Python 依赖

6. **配置 Nginx**
   - 反向代理到 8080
   - SSL 证书申请

7. **启动服务**
   - 创建 systemd 服务
   - 启动并设置开机自启

8. **获取 API Key**
   - 从数据库读取默认 Key
   - 配置到本地 Bridge

9. **测试连接**
   - Bridge → Portal
   - Portal → OpenClaw

---

## 常见错误

### 错误 1：SSL 证书申请失败

**原因：**
- 域名未解析到 VPS
- 80 端口被占用
- 防火墙阻止

**解决：**
```bash
# 检查域名解析
nslookup your-domain.com

# 检查 80 端口
sudo lsof -i :80

# 临时停止占用 80 端口的服务
sudo systemctl stop nginx

# 重新部署
```

---

### 错误 2：SSH 连接失败

**原因：**
- 密钥权限不对
- 未复制公钥到 VPS
- VPS 未开放 22 端口

**解决：**
```bash
# 检查密钥权限
ls -la ~/.ssh/agent-p2p
# 应该是 -rw------- (600)

# 修复权限
chmod 600 ~/.ssh/agent-p2p

# 重新复制公钥
ssh-copy-id -i ~/.ssh/agent-p2p ubuntu@your-vps-ip
```

---

### 错误 3：Nginx 配置失败

**原因：**
- 域名格式错误
- SSL 证书路径错误
- 权限不足

**解决：**
```bash
# 检查 Nginx 配置语法
sudo nginx -t

# 查看错误日志
sudo tail -f /var/log/nginx/error.log

# 手动测试证书申请
certbot certonly --standalone -d your-domain.com
```

---

### 错误 4：Bridge 无法连接 Portal

**原因：**
- API Key 错误
- Portal 未启动
- 防火墙阻止

**解决：**
```bash
# 检查 Portal 状态
ssh ubuntu@your-vps-ip "sudo systemctl status agent-p2p"

# 重启 Portal
ssh ubuntu@your-vps-ip "sudo systemctl restart agent-p2p"

# 检查日志
ssh ubuntu@your-vps-ip "sudo journalctl -u agent-p2p -n 50"
```

---

## 手动排查命令

```bash
# 1. 检查域名解析
nslookup your-domain.com

# 2. 检查端口开放
telnet your-vps-ip 22
telnet your-vps-ip 80
telnet your-vps-ip 443

# 3. 检查 SSH 连接
ssh -i ~/.ssh/agent-p2p ubuntu@your-vps-ip

# 4. 检查 Portal 状态
curl https://your-domain.com/api/portal/info

# 5. 检查 Bridge 日志
tail -f ~/.openclaw/workspace/skills/agent-p2p/local/bridge.log
```

---

## 安全建议

1. **使用专用 SSH 密钥**
   - 不要和主密钥混用
   - 仅授权 Portal VPS

2. **定期更新系统**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **备份数据**
   ```bash
   # 备份数据库
   scp ubuntu@your-vps-ip:/opt/agent-p2p/data/portal.db ./backup/
   ```

4. **监控日志**
   ```bash
   # 设置日志轮转
   sudo logrotate -f /etc/logrotate.d/agent-p2p
   ```
