# 自动化部署技能

## 描述

自动化 Git 项目部署技能。支持从私有 Git 仓库拉取代码、构建打包、SSH 部署到 Linux 服务器。

**适用场景**：
- 用户提出开发需求后自动开发并部署
- 代码修改后自动构建部署
- 多项目部署管理

## 前置条件

### 1. Git 访问配置

**方式 A：HTTP 认证**
```bash
# 配置 Git 凭据
git config --global credential.helper store
```

**方式 B：SSH Key（推荐）**
```bash
# 生成 SSH Key
ssh-keygen -t ed25519 -C "openclaw-deploy" -f ~/.ssh/openclaw_deploy

# 将公钥添加到 Git 服务器
cat ~/.ssh/openclaw_deploy.pub
```

### 2. 服务器 SSH 配置

```bash
# 生成部署 SSH Key（如果复用上面的可以跳过）
ssh-keygen -t ed25519 -C "server-deploy" -f ~/.ssh/server_deploy

# 将公钥添加到服务器
ssh-copy-id -i ~/.ssh/server_deploy.pub user@server_ip
```

### 3. 验证连接

```bash
# 测试 Git 连接
git ls-remote http://192.168.1.169:8015/peninsula/points

# 测试服务器连接
ssh -i ~/.ssh/server_deploy user@server_ip "echo connected"
```

## 工作流程

### 标准部署流程

```
1. 接收需求 → 2. 拉取代码 → 3. 开发修改 → 4. Git 提交 
→ 5. 构建打包 → 6. SSH 传输 → 7. 服务器部署 → 8. 服务重启 → 9. 健康检查
```

### 详细步骤

#### 步骤 1：拉取最新代码
```bash
cd /workspace/points
git pull origin main
```

#### 步骤 2：开发修改
根据用户需求修改代码文件。

#### 步骤 3：提交代码
```bash
git add .
git commit -m "feat: [需求描述]"
git push origin main
```

#### 步骤 4：构建项目

**Node.js 部分**：
```bash
cd /workspace/points
npm install
npm run build
```

**Java 部分**：
```bash
cd /workspace/points/java-module
mvn clean package -DskipTests
```

#### 步骤 5：打包部署产物
```bash
# 创建部署包
tar -czf points-deploy.tar.gz dist/ target/*.jar
```

#### 步骤 6：SSH 传输到服务器
```bash
scp -i ~/.ssh/server_deploy points-deploy.tar.gz user@server:/tmp/
```

#### 步骤 7：服务器部署
```bash
ssh -i ~/.ssh/server_deploy user@server << 'EOF'
  # 备份当前版本
  cp -r /www/wwwroot/points /www/backup/points_$(date +%Y%m%d_%H%M%S)
  
  # 解压新代码
  tar -xzf /tmp/points-deploy.tar.gz -C /www/wwwroot/points
  
  # 重启服务（根据实际服务管理方式）
  # systemd:
  systemctl restart points-service
  
  # 或宝塔面板：
  /etc/init.d/points restart
  
  # 或 PM2（Node.js）:
  pm2 restart points
  
  # 清理临时文件
  rm /tmp/points-deploy.tar.gz
EOF
```

#### 步骤 8：健康检查
```bash
ssh -i ~/.ssh/server_deploy user@server "curl -s http://localhost:端口/health || exit 1"
```

## 配置项

在 `DEPLOY_CONFIG.md` 中配置以下信息：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `git.url` | Git 仓库地址 | `http://192.168.1.169:8015/peninsula/points` |
| `git.branch` | 默认分支 | `main` |
| `server.host` | 服务器 IP | `192.168.1.100` |
| `server.port` | SSH 端口 | `22` |
| `server.user` | SSH 用户 | `root` |
| `server.deployPath` | 部署路径 | `/www/wwwroot/points` |
| `project.type` | 项目类型 | `nodejs` / `java` / `nodejs+java` |
| `project.build.node.buildCmd` | Node 构建命令 | `npm run build` |
| `project.build.java.buildCmd` | Java 构建命令 | `mvn clean package` |
| `project.deploy.restartCmd` | 重启命令 | `pm2 restart points` |

## 错误处理

### Git 连接失败
- 检查网络连通性
- 验证认证信息
- 确认 SSH Key 已添加

### SSH 连接失败
- 检查服务器 SSH 服务状态
- 验证 SSH Key 权限（`chmod 600 ~/.ssh/server_deploy`）
- 确认防火墙放行 SSH 端口

### 构建失败
- 检查 Node.js/Java 版本
- 确认依赖安装完整
- 查看详细错误日志

### 部署失败
- 检查部署目录权限
- 确认磁盘空间充足
- 回滚到备份版本

## 安全注意事项

1. **敏感信息保护**：
   - 不要将密码、Token 写入配置文件
   - 使用 SSH Key 代替密码认证
   - SSH Key 设置权限 `chmod 600`

2. **权限控制**：
   - 部署脚本需要 elevated 权限执行
   - 限制可部署的服务器列表
   - 敏感操作需要用户确认

3. **备份策略**：
   - 每次部署前自动备份
   - 保留最近 5 个版本
   - 支持快速回滚

## 使用示例

### 简单需求（直接部署）
用户：帮我加个积分查询接口

```
1. 开发修改代码
2. 提交 Git
3. 自动构建部署
4. 回复用户：已完成部署 ✅
```

### 复杂需求（需要 Review）
用户：实现一个积分排行榜功能

```
1. 开发修改代码
2. 提交到 feature 分支
3. 回复用户：开发完成，请 Review
4. 用户确认后合并到 main 并部署
```

## 回滚流程

```bash
# 获取最新备份版本
BACKUP=$(ssh user@server "ls -t /www/backup/ | head -1")

# 恢复备份
ssh user@server << EOF
  systemctl stop points-service
  rm -rf /www/wwwroot/points/*
  cp -r /www/backup/$BACKUP/* /www/wwwroot/points/
  systemctl start points-service
EOF
```

---

**版本**：1.0.0  
**最后更新**：2026-03-26
