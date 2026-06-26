# 🔑 SSH Key 配置说明

## 当前状态

✅ Git 仓库连接成功
❌ 服务器 SSH 需要配置公钥认证

---

## 配置步骤

### 步骤 1：复制公钥内容

执行以下命令复制公钥：

```bash
cat ~/.ssh/server_deploy.pub
```

公钥内容如下：

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGymgZxZ3XEWHkQHjeu5A0GhgVQfbp1VZziZQQXjq9nt openclaw-server
```

### 步骤 2：登录服务器添加公钥

**方式 A：使用 SSH 密码连接（推荐）**

```bash
# 登录服务器
ssh root@192.168.1.168
# 输入密码：zhangjiamin

# 创建 .ssh 目录
mkdir -p ~/.ssh

# 编辑 authorized_keys 文件
vi ~/.ssh/authorized_keys

# 按 i 进入插入模式，粘贴上面的公钥内容
# 按 Esc，输入 :wq 保存退出

# 设置正确权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# 退出服务器
exit
```

**方式 B：使用 ssh-copy-id（如果有密码认证）**

```bash
sshpass -p 'zhangjiamin' ssh-copy-id -o StrictHostKeyChecking=no -i ~/.ssh/server_deploy.pub root@192.168.1.168
```

### 步骤 3：验证连接

```bash
ssh -i ~/.ssh/server_deploy root@192.168.1.168 "echo 连接成功"
```

如果输出 "连接成功"，说明配置完成！✅

---

## 完成后

配置好 SSH 后，告诉我：**"SSH 配置好了"**，我会验证连接并测试部署！

---

## 备选方案：使用密码认证部署

如果不想配置 SSH Key，可以修改部署脚本使用密码认证。但这样不太安全，且每次都需要输入密码。
