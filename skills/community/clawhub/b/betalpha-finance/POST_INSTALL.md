# 安装后配置指南

## ✅ 安装成功！

Betalpha Gateway Skill 已成功安装。在开始使用前，请完成以下配置：

## 📝 第一步：获取 API Token

1. 访问或扫描小程序码：[https://ai.firstindex.cn/qr.jpg](https://ai.firstindex.cn/qr.jpg)
2. 在小程序中获取您的 API Token
3. Token 格式示例：`BA-*****************`

## 🔐 第二步：配置 API Token（推荐手动配置）

### Linux / macOS
```bash
# 创建配置目录
mkdir -p ~/.config/betalpha

# 写入 Token（替换 YOUR_TOKEN_HERE 为您的实际 Token）
echo "YOUR_TOKEN_HERE" > ~/.config/betalpha/api_key.txt

# 设置安全权限（仅您可读写）
chmod 600 ~/.config/betalpha/api_key.txt

# 验证配置
cat ~/.config/betalpha/api_key.txt
```

### Windows (PowerShell)
```powershell
# 创建配置目录
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\betalpha"

# 写入 Token（替换 YOUR_TOKEN_HERE 为您的实际 Token）
Set-Content -Path "$env:USERPROFILE\.config\betalpha\api_key.txt" -Value "YOUR_TOKEN_HERE"

# 设置安全权限（仅当前用户可访问）
$acl = Get-Acl "$env:USERPROFILE\.config\betalpha\api_key.txt"
$acl.SetAccessRuleProtection($true, $false)
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule($env:USERNAME,"FullControl","Allow")
$acl.SetAccessRule($rule)
Set-Acl "$env:USERPROFILE\.config\betalpha\api_key.txt" $acl

# 验证配置
Get-Content "$env:USERPROFILE\.config\betalpha\api_key.txt"
```

## 🧪 第三步：测试功能

配置完成后，尝试以下命令测试：

```
查询 000001 的股票价格
```

如果返回平安银行的实时行情数据，说明配置成功！

## 📚 使用示例

### 股票查询
- "查询 000001 的股票价格"
- "查询 000001、000002、600000 的股价"
- "获取平安银行 000001 的分钟 K 线"

### 基金查询
- "查询基金 110022 的估值"
- "查询易方达中小盘基金的估值"

### ETF 查询
- "查询中证500ETF的数据"
- "查询 ETF 实时行情"
- "查询 ETF 折溢价率"

## ⚠️ 安全提示

- ✅ 已设置文件权限为 600（仅用户可读写）
- ❌ 不要在聊天中直接粘贴 Token
- ❌ 不要将配置文件加入 Git 版本控制
- ✅ 定期更换 Token 以提高安全性
- ❌ 不要与他人分享您的 Token

## 🗑️ 卸载与数据删除

如需删除所有本地数据：

```bash
# Linux/macOS
rm -rf ~/.config/betalpha/

# Windows (PowerShell)
Remove-Item -Recurse -Force "$env:USERPROFILE\.config\betalpha\"
```

## ❓ 遇到问题？

1. **Token 无效**: 确认 Token 格式正确，没有多余空格或换行
2. **权限错误**: 检查文件权限 `ls -la ~/.config/betalpha/api_key.txt`
3. **网络错误**: 确认可以访问 `https://ai.firstindex.cn`
4. **其他问题**: 提交 Issue 到 GitHub 仓库

## 📖 更多信息

- 完整文档: README.md
- API 信息: https://ai.firstindex.cn/api/discovery
- 隐私政策: https://ai.firstindex.cn/privacy

---

**开始使用**: 配置完成后，直接对我说 "查询 000001 的股票价格" 即可开始！
