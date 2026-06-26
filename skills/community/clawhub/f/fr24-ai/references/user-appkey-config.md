# 采购 APPKEY 配置（对用户说明用）

用户询问「如何配置 appkey / 采购密钥 / 开通预订」时，**只按本文回答**。  
**禁止**向用户说明内部联调、跳过校验/白名单等非公开配置方式。  
**禁止**在对话中让用户粘贴密钥明文；引导用户在本机自行配置。

## 前提

1. 已在 [航路官网](https://www.flightroutes24.com/) 注册并开通 API 采购，取得三项密钥：
   - **APPKEY**（采购编号）
   - **SHA512 签名密钥**
   - **AES 密钥**（16 字节，用于乘客信息加密）
2. 演示查价无需配置；仅 **采购搜索 + 预订** 需要。

## 方式一：命令行配置（推荐，无需重启 Agent）

在 Skill 目录下运行（将参数替换为真实值，**勿在聊天中发送**）：

```bash
python scripts/config_keys.py set --appkey "你的APPKEY" --sign-secret "你的签名密钥" --aes-secret "你的AES密钥"
```

配置后**无需重启** Claude Code，下次搜索即自动使用采购账号。

## 方式二：`.env` 文件（无需重启 Agent）

在 Skill 根目录创建 `.env` 文件（与 `config.py` 同级）：

```
FR_NEWAPI_APPKEY=你的APPKEY
FR_NEWAPI_SIGN_SECRET=你的签名密钥
FR_NEWAPI_AES_SECRET=你的AES密钥
```

配置后**无需重启** Claude Code。`.env` 文件已被 `.gitignore` 忽略，不会被提交到版本库。

## 方式三：Windows「用户环境变量」（需重启 Agent）

1. `Win + R` → 输入 `sysdm.cpl` → 回车  
2. **高级** → **环境变量**  
3. 在 **用户变量** 中 **新建** 三条（值由用户在航路后台复制，勿在聊天里发送）：

| 变量名 | 说明 |
|--------|------|
| `FR_NEWAPI_APPKEY` | 采购 APPKEY |
| `FR_NEWAPI_SIGN_SECRET` | SHA512 签名密钥 |
| `FR_NEWAPI_AES_SECRET` | 16 字节 AES 密钥 |

4. 全部 **确定** 保存后，**完全退出并重新打开 Claude Code**（或重启电脑），环境变量才会被 Skill 读到。

## 备选：PowerShell（用户变量，永久）

在用户自己的 PowerShell 中执行（将引号内替换为真实值，**勿发给 Agent**）：

```powershell
[System.Environment]::SetEnvironmentVariable("FR_NEWAPI_APPKEY", "你的APPKEY", "User")
[System.Environment]::SetEnvironmentVariable("FR_NEWAPI_SIGN_SECRET", "你的SHA512签名密钥", "User")
[System.Environment]::SetEnvironmentVariable("FR_NEWAPI_AES_SECRET", "你的16字节AES密钥", "User")
```

执行后同样需要 **重启 Claude Code**。

## 验证（用户可在本机执行）

在 Skill 目录（如 `~/.claude/skills/fr24-ai`）打开终端：

```bash
python scripts/config_keys.py status
```

或：

```powershell
python -c "import config; print('configured:', config.is_newapi_configured()); print('booking_ready:', config.is_booking_ready())"
```

| 输出 | 含义 |
|------|------|
| `configured: True` | 已识别 APPKEY 与签名密钥 |
| `booking_ready: True` | 三项密钥齐全，可预订 |

若为 `False`，检查变量是否在 **用户变量**、名称是否拼写正确、是否已重启 Claude Code。

## 配置优先级

当多个方式同时配置时，按以下优先级读取：**环境变量 > `.env` 文件 > `.cache/keys.json`**。

## Agent 禁止事项

