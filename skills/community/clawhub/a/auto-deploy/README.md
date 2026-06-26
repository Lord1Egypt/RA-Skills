# 🚀 自动化部署 - 首次配置指南

## 快速开始

完成以下配置后，你就可以对我说：
> "帮我加个积分查询接口"

我会自动完成：开发 → 提交 → 构建 → 部署 全流程！

---

## 步骤 1：生成 SSH Key

### 1.1 生成 Git 仓库 SSH Key（可选，如用 HTTP 认证可跳过）

```bash
ssh-keygen -t ed25519 -C "openclaw-git" -f ~/.ssh/openclaw_git
```

将公钥添加到 Git 服务器：
```bash
cat ~/.ssh/openclaw_git.pub
# 复制输出内容，添加到 Git 服务器的 SSH Keys 设置中
```

### 1.2 生成服务器 SSH Key（必须）

```bash
ssh-keygen -t ed25519 -C "openclaw-server" -f ~/.ssh/server_deploy
```

将公钥添加到部署服务器：
```bash
# 方式 A：使用 ssh-copy-id（推荐）
ssh-copy-id -i ~/.ssh/server_deploy.pub root@<服务器 IP>

# 方式 B：手动添加
cat ~/.ssh/server_deploy.pub
# 复制内容，登录服务器后执行：
# mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
```

### 1.3 验证 SSH 连接

```bash
ssh -i ~/.ssh/server_deploy root@<服务器 IP> "echo 连接成功"
```

---

## 步骤 2：填写配置文件

编辑 `/home/node/clawd/skills/auto-deploy/deploy-config.json`

**必须填写的字段**：

```json
{
  "git": {
    "url": "http://192.168.1.169:8015/peninsula/points",
    "branch": "main"
  },
  "server": {
    "host": "192.168.1.xxx",  // ← 填写服务器 IP
    "port": 22,
    "user": "root",
    "deployPath": "/www/wwwroot/points",
    "backupPath": "/www/backup/points"
  }
}
```

**Git 认证（二选一）**：

方式 A - HTTP 认证：
```json
"git": {
  "auth": {
    "type": "http",
    "username": "your_username",
    "password": "your_password"
  }
}
```

方式 B - SSH Key：
```json
"git": {
  "auth": {
    "type": "ssh",
    "keyPath": "~/.ssh/openclaw_git"
  }
}
```

---

## 步骤 3：配置 OpenClaw 权限

需要配置 `elevated` 权限以执行以下命令：

- `git clone`, `git pull`, `git push`
- `ssh`, `scp`
- `npm`, `mvn`
- `tar`, `rsync`

配置文件位置：`~/.openclaw/config.json`

```json
{
  "tools": {
    "elevated": {
      "enabled": true,
      "allowFrom": {
        "wecom": true
      },
      "allowCommands": [
        "git",
        "ssh",
        "scp",
        "npm",
        "mvn",
        "tar"
      ]
    }
  }
}
```

---

## 步骤 4：测试部署流程

### 4.1 测试 Git 连接

```bash
git ls-remote http://192.168.1.169:8015/peninsula/points
```

### 4.2 测试服务器连接

```bash
ssh -i ~/.ssh/server_deploy root@<服务器 IP> "echo 连接成功 && ls -la /www/wwwroot"
```

### 4.3 执行首次部署

```bash
cd /home/node/clawd/skills/auto-deploy
./scripts/deploy.sh
```

---

## 步骤 5：宝塔面板配置

### 5.1 确认运行环境

登录宝塔面板，确认已安装：

- [ ] Node.js（推荐 v20）
- [ ] Java（推荐 v17）
- [ ] Maven（Java 项目需要）
- [ ] PM2（Node.js 进程管理）

### 5.2 配置项目目录

在宝塔面板中：

1. 创建网站目录：`/www/wwwroot/points`
2. 设置目录权限：`chmod 755 /www/wwwroot/points`
3. 创建备份目录：`/www/backup/points`

### 5.3 配置防火墙

确保以下端口开放：

- SSH 端口（默认 22）
- 应用端口（如 3000、8080 等）

---

## 使用方式

### 简单需求（直接部署）

```
你：帮我加个用户积分查询接口
我：好的，正在开发...
    ✅ 代码已提交
    ✅ 构建完成
    ✅ 部署成功
    接口地址：/api/points/query
```

### 复杂需求（需要 Review）

```
你：实现一个积分排行榜功能，按日/周/月统计
我：好的，这个功能比较复杂，我先开发
    ...开发中...
    ✅ 开发完成，功能包括：
       - 日榜、周榜、月榜
       - 前 100 名展示
       - 实时更新
    请 Review 代码，确认后再部署
```

### 手动部署

```bash
# 部署 main 分支
./scripts/deploy.sh

# 部署指定分支
./scripts/deploy.sh feature/ranking

# 回滚到上一个版本
./scripts/rollback.sh

# 回滚到指定版本
./scripts/rollback.sh points_20260326_120000
```

---

## 常见问题

### Q1: SSH 连接失败

```
Permission denied (publickey)
```

**解决**：
```bash
# 检查 SSH Key 权限
chmod 600 ~/.ssh/server_deploy

# 重新添加公钥到服务器
ssh-copy-id -i ~/.ssh/server_deploy.pub root@<服务器 IP>
```

### Q2: Git 连接失败

```
Authentication failed
```

**解决**：
- 检查用户名密码是否正确
- 或将 SSH Key 添加到 Git 服务器

### Q3: 部署后服务未启动

**解决**：
```bash
# 登录服务器检查
ssh root@<服务器 IP>

# 查看 PM2 进程
pm2 list

# 查看系统服务
systemctl status points-service

# 查看日志
pm2 logs points
```

### Q4: 如何回滚

```bash
# 查看可用备份
ssh root@<服务器 IP> "ls -lt /www/backup/points"

# 执行回滚
./scripts/rollback.sh points_20260326_120000
```

---

## 安全建议

1. **SSH Key 保护**：
   - 私钥权限设置为 `600`
   - 不要将私钥上传到 Git

2. **备份策略**：
   - 每次部署前自动备份
   - 定期清理旧备份（保留最近 10 个）

3. **权限控制**：
   - 使用专用部署用户（非 root）
   - 限制部署目录权限

4. **敏感信息**：
   - 不要将密码写入配置文件
   - 使用环境变量或密钥管理服务

---

## 下一步

配置完成后，告诉我：
> "配置完成了，测试一下部署"

我会执行一次完整的部署流程来验证配置！🐉
