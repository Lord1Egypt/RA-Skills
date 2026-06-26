# 🚀 环境变量设置指南

## 方式1：一键设置（最简单 ⭐⭐⭐⭐⭐）

### 运行设置向导

```bash
cd <skill-directory>

./setup.sh
```

**设置向导会自动完成：**
1. ✅ 检查并安装依赖
2. ✅ 引导你创建 `.env` 配置文件
3. ✅ 测试同步功能
4. ✅ 设置定时任务

---

## 方式2：手动创建 .env 文件

### 步骤1：复制模板

```bash
cd <skill-directory>

cp .env.example .env
```

### 步骤2：编辑配置

用你喜欢的编辑器打开 `.env` 文件：

```bash
# 使用 nano（推荐新手）
nano .env

# 或使用 vim
vim .env

# 或使用 VS Code
code .env
```

填入你的真实信息：

```bash
FLOMO_EMAIL=your-email@example.com          # 改成你的邮箱
FLOMO_PASSWORD=your-password                 # 改成你的密码
OBSIDIAN_VAULT=~/Documents/Obsidian/flomo # Obsidian 目录
TAG_PREFIX=flomo/                            # 标签前缀
```

### 步骤3：保存并退出

- **nano**：按 `Ctrl+O` 保存，`Ctrl+X` 退出
- **vim**：按 `Esc`，输入 `:wq`，按 `Enter`
- **VS Code**：按 `Cmd+S` 保存

### 步骤4：设置文件权限（重要！）

```bash
chmod 600 .env
```

这会确保只有你能读写这个文件，保护密码安全。

### 步骤5：测试同步

```bash
./sync.sh --no-headless
```

---

## 方式3：使用 shell 配置文件（全局环境变量）

### macOS / Linux

#### 步骤1：编辑 shell 配置文件

**如果你使用 zsh（macOS 默认）：**

```bash
nano ~/.zshrc
```

**如果你使用 bash：**

```bash
nano ~/.bashrc
```

#### 步骤2：添加环境变量

在文件末尾添加：

```bash
# Flomo 自动同步配置
export FLOMO_EMAIL="your-email@example.com"
export FLOMO_PASSWORD="your-password"
export OBSIDIAN_VAULT="~/Documents/Obsidian/flomo"
export TAG_PREFIX="flomo/"
```

#### 步骤3：保存并重新加载

```bash
# 保存文件后，重新加载配置
source ~/.zshrc   # 如果是 zsh
# 或
source ~/.bashrc  # 如果是 bash
```

#### 步骤4：验证环境变量

```bash
echo $FLOMO_EMAIL
echo $FLOMO_PASSWORD
```

应该能看到你设置的值。

#### 步骤5：运行同步（不需要传参数）

创建一个简化的同步脚本：

```bash
#!/bin/bash
cd <skill-directory>

python scripts/auto_sync.py \
  --email "$FLOMO_EMAIL" \
  --password "$FLOMO_PASSWORD" \
  --output "$OBSIDIAN_VAULT" \
  --tag-prefix "$TAG_PREFIX"
```

---

## 方式4：每次运行时手动设置（临时）

### 单次使用

```bash
export FLOMO_EMAIL="your-email@example.com"
export FLOMO_PASSWORD="your-password"

./sync.sh
```

**注意**：这种方式只在当前终端会话有效，关闭终端后失效。

### 一行命令

```bash
FLOMO_EMAIL="your-email@example.com" FLOMO_PASSWORD="your-password" ./sync.sh
```

---

## 🔐 安全最佳实践

### ✅ 推荐做法

1. **使用 .env 文件**（方式2）
   - 优点：简单、安全、不影响全局环境
   - 记得添加到 `.gitignore`（已自动添加）

2. **设置文件权限**
   ```bash
   chmod 600 .env
   ```

3. **不要提交密码到 Git**
   - `.env` 文件已在 `.gitignore` 中
   - 检查：`git status` 不应该看到 `.env`

### ❌ 不推荐做法

1. ❌ 在命令行中明文输入密码
   ```bash
   # 不推荐！会留在命令历史中
   python auto_sync.py --password "mypassword"
   ```

2. ❌ 将密码提交到 Git
   ```bash
   # 危险！永远不要这样做
   git add .env
   git commit -m "add config"
   ```

3. ❌ 将密码写在脚本中
   ```bash
   # 不安全！
   PASSWORD="mypassword"
   ```

---

## 🧪 验证设置

### 检查 .env 文件

```bash
cat .env
```

应该看到：
```
FLOMO_EMAIL=your-email@example.com
FLOMO_PASSWORD=your-password
OBSIDIAN_VAULT=~/Documents/Obsidian/flomo
TAG_PREFIX=flomo/
```

### 检查文件权限

```bash
ls -la .env
```

应该看到：
```
-rw-------  1 username  staff  203 Mar 11 16:30 .env
```

`-rw-------` 表示只有所有者可读写。

### 测试同步

```bash
./sync.sh --no-headless --verbose
```

如果看到浏览器自动打开并成功登录，说明配置正确！

---

## 🆘 常见问题

### Q1: .env 文件创建后找不到

```bash
# 使用 ls -a 查看隐藏文件
ls -a

# 应该能看到 .env
```

### Q2: sync.sh 提示找不到 .env 文件

```bash
# 确认当前目录
pwd
# 应该在 flomo-to-obsidian 目录下

# 确认 .env 存在
ls -a | grep .env
```

### Q3: 密码中有特殊字符

在 `.env` 文件中，密码不需要引号：

```bash
# 正确
FLOMO_PASSWORD=p@ssw0rd!123

# 错误（会包含引号）
FLOMO_PASSWORD="p@ssw0rd!123"
```

### Q4: 修改 .env 文件后不生效

```bash
# 重新加载环境变量
source .env

# 或重新运行脚本
./sync.sh
```

### Q5: 权限被拒绝

```bash
# 给脚本添加执行权限
chmod +x sync.sh
chmod +x setup.sh
```

---

## 📚 下一步

配置完成后：

1. **测试同步**
   ```bash
   ./sync.sh --no-headless
   ```

2. **设置定时任务**
   ```bash
   crontab -e
   # 添加：0 22 * * * cd /path/to/flomo-to-obsidian && ./sync.sh
   ```

3. **查看日志**
   ```bash
   tail -f auto_sync.log
   ```

4. **阅读文档**
   - `AUTO_SYNC.md` - 自动同步详细说明
   - `README.md` - 项目总览

---

## 🎉 快速开始

懒得看教程？运行这个：

```bash
cd <skill-directory>
./setup.sh
```

一切都会自动完成！
