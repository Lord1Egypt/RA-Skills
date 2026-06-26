# 手动配置指南

本指南介绍如何**手动配置**八爪鱼 RPA Webhook 技能，无需运行任何脚本。

## 📋 前置条件

- 已获取八爪鱼 RPA Webhook URL
- 已获取签名密钥 (Key)
- Python 3.6+ 已安装

---

## 步骤 1：设置环境变量

### Linux / macOS

编辑你的 shell 配置文件：

```bash
# 使用 bash
nano ~/.bashrc

# 或使用 zsh
nano ~/.zshrc
```

在文件末尾添加：

```bash
# 八爪鱼 RPA Webhook 配置
export BAZHUAYU_WEBHOOK_URL="https://rpa.bazhuayu.com/api/v1/trigger/xxx"
export BAZHUAYU_WEBHOOK_KEY="你的签名密钥"
```

保存后执行：

```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

### Windows (PowerShell)

编辑 PowerShell 配置文件：

```powershell
notepad $PROFILE
```

添加：

```powershell
$env:BAZHUAYU_WEBHOOK_URL="https://rpa.bazhuayu.com/api/v1/trigger/xxx"
$env:BAZHUAYU_WEBHOOK_KEY="你的签名密钥"
```

保存后重启 PowerShell 或执行：

```powershell
. $PROFILE
```

### Windows (命令提示符)

临时设置（仅当前会话）：

```cmd
set BAZHUAYU_WEBHOOK_URL=https://rpa.bazhuayu.com/api/v1/trigger/xxx
set BAZHUAYU_WEBHOOK_KEY=你的签名密钥
```

永久设置需要通过系统环境变量设置界面。

---

## 步骤 2：验证配置

运行以下命令检查环境变量是否已设置：

```bash
echo $BAZHUAYU_WEBHOOK_URL
echo $BAZHUAYU_WEBHOOK_KEY
```

应该能看到你设置的值（密钥会显示完整值，请注意不要泄露）。

---

## 步骤 3：初始化配置文件

```bash
python3 bazhuayu-webhook.py init
```

这会创建 `config.json` 文件。

---

## 步骤 4：安全检查

```bash
python3 bazhuayu-webhook.py secure-check
```

确保所有检查项都通过。

---

## 步骤 5：测试连接

```bash
python3 bazhuayu-webhook.py test
```

如果测试成功，说明配置完成！

---

## 🔐 安全建议

1. **不要将密钥提交到版本控制**
   - `config.json` 已加入 `.gitignore`
   - 不要将包含密钥的截图或日志公开

2. **使用强密钥**
   - 建议至少 16 个字符
   - 包含大小写字母、数字和特殊字符

3. **限制文件权限**
   ```bash
   chmod 600 config.json
   ```

4. **定期轮换密钥**
   - 在八爪鱼 RPA 控制台更新密钥后
   - 同步更新环境变量

---

## 🆘 故障排除

### 环境变量不生效

1. 确认已执行 `source ~/.bashrc` 或 `source ~/.zshrc`
2. 打开新终端后需要重新执行 source
3. 检查拼写是否正确（区分大小写）

### 配置文件权限问题

```bash
chmod 600 config.json
```

### 其他问题

运行 `secure-check` 查看详细诊断信息。
