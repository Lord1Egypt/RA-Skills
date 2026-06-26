# Betalpha Gateway - 金融数据网关

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/betalpha-gateway-skill)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)](#)

高性能中国金融数据网关，为 AI 助手提供 A 股、基金、ETF 实时行情查询能力。

## 📋 功能特性

- ✅ **A股实时行情** - 查询多只股票实时价格
- ✅ **A股分钟K线** - 查询股票当日分钟级K线数据
- ✅ **基金实时估值** - 查询基金实时估值
- ✅ **ETF实时行情** - 查询场内ETF实时行情
- ✅ **ETF/LOF折溢价** - 查询场内ETF/LOF折溢价率
- ✅ **实时新闻** - 查询实时新闻
- ✅ **动态API发现** - 自动获取最新API端点列表

## ⚠️ 安装前必读

### 所需凭据

此 Skill 需要 **API Token** 才能使用：

- **获取方式**: 扫描小程序码 [https://ai.firstindex.cn/qr.jpg](https://ai.firstindex.cn/qr.jpg)
- **存储位置**: `~/.config/betalpha/api_key.txt`
- **用途**: 认证用户身份，访问金融数据 API

### 文件系统访问

安装此 Skill 后，它将：

- ✅ **读取**: `~/.config/betalpha/api_key.txt` (API Token)
- ✅ **写入**: `~/.config/betalpha/api_key.txt` (自动配置Token时)
- ✅ **写入**: `~/.config/betalpha/api_cache.json` (缓存API端点，可选)

### 网络访问

此 Skill 将连接到：

- 🌐 **ai.firstindex.cn** - 获取API端点和查询金融数据
  - 发送数据: API Token (在请求头中)、股票/基金代码
  - 使用协议: HTTPS (加密传输)

### 隐私与安全

**我们承诺**：
- ❌ 不收集用户个人信息
- ❌ 不上传聊天记录
- ❌ 不追踪用户行为
- ✅ API Token 仅用于访问金融数据
- ✅ 所有通信使用 HTTPS 加密
- ✅ 用户可随时删除本地数据

**安全建议**：
1. **不要在聊天中粘贴 Token** - 使用手动配置方法
2. **设置文件权限** - `chmod 600 ~/.config/betalpha/api_key.txt`
3. **定期更换 Token** - 提高账户安全性
4. **不要分享 Token** - Token 与您的账户绑定

## 📦 安装

### 前置要求

- OpenCode CLI (版本 1.0.0+)
- 有效的 API Token (从 [这里](https://ai.firstindex.cn/qr.jpg) 获取)

### 安装步骤

1. **安装 Skill**
   ```bash
   # 从 ClawHub 安装
   opencode skill install betalpha-gateway
   ```

2. **配置 API Token**（推荐手动配置）
   
   **Linux/macOS**:
   ```bash
   mkdir -p ~/.config/betalpha
   echo "YOUR_API_TOKEN_HERE" > ~/.config/betalpha/api_key.txt
   chmod 600 ~/.config/betalpha/api_key.txt
   ```
   
   **Windows (PowerShell)**:
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\betalpha"
   Set-Content -Path "$env:USERPROFILE\.config\betalpha\api_key.txt" -Value "YOUR_API_TOKEN_HERE"
   # 设置文件权限（仅当前用户可访问）
   $acl = Get-Acl "$env:USERPROFILE\.config\betalpha\api_key.txt"
   $acl.SetAccessRuleProtection($true, $false)
   $rule = New-Object System.Security.AccessControl.FileSystemAccessRule($env:USERNAME,"FullControl","Allow")
   $acl.SetAccessRule($rule)
   Set-Acl "$env:USERPROFILE\.config\betalpha\api_key.txt" $acl
   ```

3. **验证安装**
   ```
   用户: 查询 000001 的股票价格
   助手: [应返回平安银行的实时行情]
   ```

## 🚀 使用示例

### 查询单只股票
```
用户: 查询 000001 的股票价格
助手: 返回平安银行实时行情数据
```

### 批量查询股票
```
用户: 查询 000001、000002、600000 的股价
助手: 返回三只股票的实时行情
```

### 查询基金估值
```
用户: 查询基金 110022 的估值
助手: 返回基金实时估值数据
```

### 查询ETF行情
```
用户: 查询中证500ETF的数据
助手: 返回510500 ETF实时行情
```

### 查询分钟K线
```
用户: 获取 000001 的分钟K线
助手: 返回平安银行当日分钟级K线数据
```

## 🔧 配置文件

### api_key.txt
```
BA-***************
```
- 第一行为 API Token 值
- 不要添加额外空格或换行

### api_cache.json (自动生成)
```json
{
  "last_update": "2026-03-17T10:00:00Z",
  "endpoints": [
    {
      "name": "A股实时行情",
      "path": "/api/realtime-stock",
      "description": "查询股票实时行情"
    }
  ]
}
```

## 🗑️ 卸载与数据删除

### 卸载 Skill
```bash
opencode skill uninstall betalpha-gateway
```

### 删除所有本地数据
```bash
# Linux/macOS
rm -rf ~/.config/betalpha/

# Windows (PowerShell)
Remove-Item -Recurse -Force "$env:USERPROFILE\.config\betalpha\"
```

## ❓ 常见问题

### Q: 为什么需要 API Token？
A: API Token 用于认证您的身份并确保数据访问的合法性。通过小程序获取的 Token 与您的账户绑定。

### Q: Token 存储在哪里？安全吗？
A: Token 存储在您本地主目录的配置文件中 (`~/.config/betalpha/api_key.txt`)。建议设置文件权限为 600（仅用户可读写），不要分享给他人。

### Q: 可以在聊天中直接提供 Token 吗？
A: 虽然支持，但**不推荐**。最佳实践是通过命令行手动配置，避免 Token 在聊天记录中暴露。

### Q: 如何更换 Token？
A: 编辑 `~/.config/betalpha/api_key.txt` 文件，替换为新的 Token 即可。

### Q: API 端点会变化吗？
A: 可能会。此 Skill 每次使用时会检查 Discovery API (`/api/discovery`) 以获取最新的端点列表，确保兼容性。

### Q: 数据准确吗？
A: 数据来源公开数据，可能存在延迟。仅供参考，不构成投资建议。

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🤝 支持

- **问题反馈**: [GitHub Issues](https://github.com/yourusername/betalpha-gateway-skill/issues)
- **API 文档**: [https://ai.firstindex.cn/api/discovery](https://ai.firstindex.cn/api/discovery)

## ⚖️ 免责声明

本 Skill 提供的金融数据仅供参考，不构成任何投资建议。使用本工具进行投资决策的风险由用户自行承担。数据可能存在延迟或错误，请以官方渠道信息为准。

---

**安装前请确认**：
- [ ] 我已阅读并理解此 Skill 需要的凭据和权限
- [ ] 我了解 API Token 将存储在本地文件中
- [ ] 我信任 ai.firstindex.cn 域名及其服务提供方
- [ ] 我将通过安全方式配置 API Token
- [ ] 我了解可以随时删除本地数据

如同意以上条款，请继续安装。
