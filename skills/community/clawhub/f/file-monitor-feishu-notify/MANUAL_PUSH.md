# 手动推送到 GitHub

由于 GitHub 认证需要交互式登录，请手动执行以下步骤：

---

## 方式 1: 使用 GitHub Desktop（推荐）

1. **下载并安装 GitHub Desktop**
   - https://desktop.github.com/

2. **添加本地仓库**
   - File → Add Local Repository
   - 选择：`C:\Users\43900\.openclaw\workspace\skills\file-monitor-feishu-notify`

3. **发布到 GitHub**
   - 点击 "Publish repository"
   - 仓库名：`file-monitor-feishu-notify`
   - 勾选 "Keep this code private"（可选）
   - 点击 "Publish"

---

## 方式 2: 使用命令行

### 步骤 1: 配置 Git 凭证

```powershell
# 设置用户名和邮箱
git config --global user.name "huyoujin-cd"
git config --global user.email "your-email@example.com"
```

### 步骤 2: 生成 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选权限：`repo`, `workflow`
4. 点击 "Generate token"
5. **复制 token**（只显示一次！）

### 步骤 3: 推送代码

```powershell
cd C:\Users\43900\.openclaw\workspace\skills\file-monitor-feishu-notify

# 使用 token 推送
git push https://huyoujin-cd:YOUR_TOKEN@github.com/huyoujin-cd/file-monitor-feishu-notify.git main
```

将 `YOUR_TOKEN` 替换为你的实际 token。

---

## 方式 3: 使用 SSH（高级）

### 步骤 1: 生成 SSH 密钥

```powershell
ssh-keygen -t ed25519 -C "your-email@example.com"
```

### 步骤 2: 添加公钥到 GitHub

1. 复制公钥：
   ```powershell
   Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard
   ```

2. 访问 https://github.com/settings/keys
3. 点击 "New SSH key"
4. 粘贴公钥，保存

### 步骤 3: 切换为 SSH 推送

```powershell
cd C:\Users\43900\.openclaw\workspace\skills\file-monitor-feishu-notify
git remote set-url origin git@github.com:huyoujin-cd/file-monitor-feishu-notify.git
git push -u origin main
```

---

## 验证

推送成功后，访问：
https://github.com/huyoujin-cd/file-monitor-feishu-notify

应该能看到代码和 README。

---

## 常见问题

### Q: 认证失败？
A: 使用 GitHub token 而不是密码。

### Q: 找不到远程仓库？
A: 确保已在 GitHub 创建仓库，或首次推送时会自动创建。

### Q: 推送被拒绝？
A: 检查是否有仓库写入权限。

---

**推荐使用 GitHub Desktop，最简单！** 🚀
