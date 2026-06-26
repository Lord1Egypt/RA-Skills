# 推送到 GitHub 指南

由于当前环境网络限制，需要手动推送到 GitHub。

## 方法 1：在本地电脑推送（推荐）

### 1. 克隆空仓库

```bash
# 在你的本地电脑执行
cd /path/to/your/workspace
git clone https://github.com/KoonChaoSo/agent-error-logger.git
cd agent-error-logger
```

### 2. 复制文件

将以下文件从服务器复制到本地：

```
/home/gem/workspace/agent/skills/agent-error-logger/
├── .gitignore
├── README.md
├── SKILL.md
├── USAGE.md
├── clawhub.json
├── create-repo.sh
├── example-error-log.md
└── scripts/
    ├── record_error.py
    └── search_errors.py
```

可以用 scp：
```bash
scp -r gem@your-server:/home/gem/workspace/agent/skills/agent-error-logger/* .
```

### 3. 推送

```bash
git add .
git commit -m "Initial commit: Agent Error Logger v1.0.0"
git branch -M main
git push -u origin main
```

---

## 方法 2：下载 ZIP 上传

### 1. 在服务器打包

```bash
cd /home/gem/workspace/agent/skills/agent-error-logger
tar -czvf agent-error-logger.tar.gz \
  .gitignore README.md SKILL.md USAGE.md \
  clawhub.json create-repo.sh example-error-log.md scripts/
```

### 2. 下载到本地

```bash
scp gem@your-server:/home/gem/workspace/agent/skills/agent-error-logger/agent-error-logger.tar.gz .
```

### 3. 解压并推送

```bash
tar -xzvf agent-error-logger.tar.gz -C agent-error-logger/
cd agent-error-logger
git add .
git commit -m "Initial commit: Agent Error Logger v1.0.0"
git push -u origin main
```

---

## 方法 3：使用 GitHub Desktop

1. 下载 https://desktop.github.com/
2. 登录 GitHub
3. File → Add Local Repository → 选择解压后的文件夹
4. 点击 "Push origin"

---

## 推送后检查

访问 https://github.com/KoonChaoSo/agent-error-logger

确认所有文件都已上传：
- ✅ .gitignore
- ✅ README.md
- ✅ SKILL.md
- ✅ USAGE.md
- ✅ clawhub.json
- ✅ scripts/record_error.py
- ✅ scripts/search_errors.py

---

## 下一步：发布到 ClawHub

1. 访问 https://clawhub.com
2. 登录 GitHub 账号
3. 选择 "Publish Skill"
4. 填写信息：
   - Name: `agent-error-logger`
   - Repository: `https://github.com/KoonChaoSo/agent-error-logger`
   - Branch: `main`
   - Skill File: `SKILL.md`
5. 提交审核

---

## 需要帮助？

如果遇到问题，可以：
1. 检查 GitHub 仓库权限
2. 确认网络连接
3. 尝试使用 Personal Access Token 代替密码

```bash
# 使用 PAT 推送
git push https://YOUR_USERNAME:YOUR_PAT@github.com/KoonChaoSo/agent-error-logger.git main
```
