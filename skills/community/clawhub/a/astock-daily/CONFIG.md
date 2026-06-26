# ⚙️ A 股股票技能 - 配置指南

## 1️⃣ SMTP 邮箱配置

### 阿里云企业邮箱配置（已预设）

文件位置：`.env`

```bash
# 编辑 .env 文件，将 YOUR_PASSWORD_HERE 替换为你的邮箱密码
SMTP_CONFIG={"host":"smtp.qiye.aliyun.com","port":465,"secure":true,"user":"8@batype.com","pass":"你的密码","from":"8@batype.com"}
```

### 配置说明

| 参数 | 值 | 说明 |
|------|-----|------|
| host | smtp.qiye.aliyun.com | SMTP 服务器 |
| port | 465 | SSL 加密端口（推荐） |
| secure | true | 启用 SSL |
| user | 8@batype.com | 邮箱账号 |
| pass | 你的密码 | 邮箱密码或授权码 |
| from | 8@batype.com | 发件人地址 |

### 获取授权码（如果启用了安全登录）

1. 登录阿里云企业邮箱：https://qiye.aliyun.com
2. 进入 **设置** → **安全设置**
3. 开启 **客户端授权码**
4. 生成的授权码即为密码

---

## 2️⃣ 定时任务配置

### 方式一：手动添加 crontab

```bash
crontab -e
```

添加以下内容：

```
# A 股每日精选 - 每个交易日 9:30 运行（周一至周五）
30 9 * * 1-5 cd /Users/batype/.openclaw/workspace-work/skills/astock-daily && /opt/homebrew/bin/node index.js >> /tmp/astock-daily.log 2>&1
```

保存后生效。

### 方式二：使用配置脚本

```bash
cd /Users/batype/.openclaw/workspace-work/skills/astock-daily
./setup.sh
```

### 查看/管理定时任务

```bash
# 查看当前 cron 任务
crontab -l

# 删除所有 cron（谨慎！）
crontab -r

# 查看日志
tail -f /tmp/astock-daily.log
```

---

## 3️⃣ 测试发送

### 测试邮件发送

```bash
cd /Users/batype/.openclaw/workspace-work/skills/astock-daily

# 加载环境变量并运行
source .env && node index.js
```

### 预期输出

```
🚀 开始获取 A 股数据...
📧 目标邮箱：8@batype.com
💰 价格上限：¥20
📊 获取到新股：XX 只
📊 获取到低价股：XX 只
💾 数据已保存到：data-2026-02-27.json
✅ 邮件已发送（SMTP）
✅ 完成！
```

---

## 4️⃣ 常见问题

### ❌ 邮件发送失败

**检查项：**
1. 密码是否正确
2. 是否开启了 SMTP 服务
3. 防火墙是否阻止 465 端口
4. 查看错误日志：`tail /tmp/astock-daily.log`

**测试 SMTP 连接：**
```bash
telnet smtp.qiye.aliyun.com 465
```

### ❌ 数据获取失败

- 检查网络连接
- API 可能有访问限制，稍后再试
- 查看控制台错误信息

### ❌ Cron 不执行

**检查 cron 状态：**
```bash
# 查看 cron 日志（macOS）
grep cron /var/log/system.log

# 检查 cron 服务
sudo systemctl status cron  # Linux
sudo launchctl list | grep cron  # macOS
```

**确保 node 路径正确：**
```bash
which node
# 输出应该是：/opt/homebrew/bin/node
```

---

## 5️⃣ 修改配置

### 修改目标邮箱

编辑 `index.js`，找到 `CONFIG` 部分：

```javascript
const CONFIG = {
  email: '8@batype.com',   // 修改这里
  priceLimit: 20,
  maxStocks: 50,
};
```

### 修改价格上限

```javascript
const CONFIG = {
  email: '8@batype.com',
  priceLimit: 30,  // 修改这里，例如改为 30 元
  maxStocks: 50,
};
```

### 修改运行时间

编辑 crontab：
```bash
crontab -e
```

时间格式：`分 时 日 月 周`

示例：
- `30 9 * * 1-5` - 周一至周五 9:30
- `0 9 * * 1-5` - 周一至周五 9:00
- `30 9 * * *` - 每天 9:30

---

## 📞 需要帮助？

查看日志：
```bash
tail -f /tmp/astock-daily.log
```

测试运行：
```bash
cd /Users/batype/.openclaw/workspace-work/skills/astock-daily
source .env && node index.js
```
