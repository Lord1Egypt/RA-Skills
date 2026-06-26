# 快速配置指南 - 安全模式

> 📝 5 分钟完成安全配置，签名密钥使用环境变量存储

---

## 📖 第一步：获取 Webhook URL 和签名

在配置技能之前，首先需要在八爪鱼 RPA 中创建 Webhook 触发器。

### 步骤 1：创建 Webhook 触发器

1. 登录 [八爪鱼 RPA 控制台](https://rpa.bazhuayu.com/)
2. 进入【触发器】栏目
3. 点击 **"Webhook 触发器"**

### 步骤 2：填写触发器信息

按顺序填写：

1. **触发器名称** → 输入易于识别的名称（如：订单处理、数据采集等）
2. **指定运行的机器人** → 选择要执行任务的机器人
3. **选择要运行的应用** → 选择对应的 RPA 应用
4. 点击 **"确定"**

### 步骤 3：获取 Webhook 信息

创建成功后，会显示 Webhook 的详细信息：

- **Webhook URL** → 复制保存（格式：`https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/xxx/invoke`）
- **签名密钥 (Key)** → 复制保存（用于签名验证）

### 步骤 4：启动触发器

⚠️ **重要**：勾选 **"启动触发器"**，否则 Webhook 不会生效！

---

## 🚀 方式一：运行配置向导（推荐）

```bash
cd ~/.openclaw/workspace/skills/bazhuayu-webhook
./setup-secure.sh
```

按提示输入：
1. Webhook URL
2. 签名密钥

脚本会生成环境变量配置示例，**但不会自动修改你的 shell 配置文件**。

配置完成后，请手动将 export 命令添加到 `~/.bashrc` 或 `~/.zshrc`。

---

## 📝 方式二：手动配置

### 步骤 1: 设置环境变量

```bash
# 临时设置（当前终端会话）
export BAZHUAYU_WEBHOOK_KEY="你的签名密钥"
export BAZHUAYU_WEBHOOK_URL="https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/xxx/invoke"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export BAZHUAYU_WEBHOOK_KEY="你的签名密钥"' >> ~/.bashrc
echo 'export BAZHUAYU_WEBHOOK_URL="https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/xxx/invoke"' >> ~/.bashrc
source ~/.bashrc
```

### 步骤 2: 编辑配置文件

```bash
vim config.json
```

填入配置（**key 留空**）：

```json
{
  "url": "https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/你的 ID/invoke",
  "key": "",
  "paramNames": ["keyword", "url"],
  "defaultParams": {
    "keyword": "默认关键词",
    "url": "https://example.com"
  }
}
```

### 步骤 3: 验证配置

```bash
python3 bazhuayu-webhook.py secure-check
```

应显示：
```
✅ 配置文件权限正确 (600)
✅ 签名密钥使用环境变量存储
✅ Webhook URL 使用环境变量存储
```

### 步骤 4: 测试连接

```bash
python3 bazhuayu-webhook.py test
```

---

## 🔄 从旧配置迁移

如果已有配置存储在 config.json 中：

```bash
./migrate-to-env.sh
```

自动完成：
- ✅ 提取密钥到环境变量配置示例
- ✅ 更新配置文件移除密钥
- ✅ 备份原配置
- ⚠️ **不会**自动更新 Shell 配置文件（需手动添加）

迁移完成后，请手动将 export 命令添加到 `~/.bashrc` 或 `~/.zshrc`。

---

## ✅ 验证清单

配置完成后检查：

- [ ] `echo $BAZHUAYU_WEBHOOK_KEY` 显示密钥（部分）
- [ ] `python3 bazhuayu-webhook.py secure-check` 无警告
- [ ] `python3 bazhuayu-webhook.py test` 成功

---

## 🆘 常见问题

### Q: 环境变量不生效？

```bash
# 检查是否设置
echo $BAZHUAYU_WEBHOOK_KEY

# 重新加载 Shell 配置
source ~/.bashrc  # 或 source ~/.zshrc
```

### Q: 如何修改密钥？

```bash
# 1. 编辑 Shell 配置文件
vim ~/.bashrc

# 2. 修改 export 行
export BAZHUAYU_WEBHOOK_KEY="新密钥"

# 3. 重新加载
source ~/.bashrc
```

### Q: 可以 URL 用配置文件，密钥用环境变量吗？

可以！这正是推荐做法：

```json
{
  "url": "https://...",  // 配置文件存储（非敏感）
  "key": ""              // 留空，从环境变量读取
}
```

---

**配置完成后，运行 `python3 bazhuayu-webhook.py run` 开始使用！**
