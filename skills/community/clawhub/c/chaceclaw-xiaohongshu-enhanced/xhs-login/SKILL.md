---
name: xhs-login
description: 小红书账号登录状态管理与多账号切换。检查登录状态、扫码登录、账号切换。
emoji: 🔐
version: "1.0.0"
triggers:
  - 登录
  - 扫码
  - 切换账号
  - 检查登录
  - logout
  - login
---

# 🔐 xhs-login

> 小红书账号登录状态管理与多账号切换

## 何时触发

用户提到以下表述时激活：
- "登录小红书"
- "检查登录状态"
- "切换账号"
- "扫码登录"
- "账号异常"
- `/xhs-login`

---

## 核心原则

1. **每次操作前必须先检查登录状态** — 未登录时调用其他工具会直接报错
2. **Cookie > 扫码** — Cookie 方式更稳定，适合自动化
3. **多账号必须隔离** — 不同账号的 Cookie 不能混用

---

## 登录状态检查

### 标准检查流程

```python
# Step 1: 调用 check_login_status
status = await mcp.check_login_status()

# Step 2: 解析返回
if status.get("logged_in"):
    print(f"✅ 已登录: {status['nickname']}")
    print(f"   用户ID: {status['user_id']}")
    print(f"   头像: {status['avatar_url']}")
    print(f"   有效期至: {status['expires_at']}")
else:
    print("❌ 未登录，请先完成登录")
    # 触发登录流程（见下方）
```

### 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `logged_in` | boolean | 是否已登录 |
| `user_id` | string | 小红书用户ID |
| `nickname` | string | 昵称 |
| `avatar_url` | string | 头像URL |
| `expires_at` | string | Cookie 过期时间（ISO格式） |
| `device_id` | string | 设备ID |

### 登录状态有效期监控

```python
from datetime import datetime, timedelta

def check_expiry(status):
    expires = datetime.fromisoformat(status['expires_at'].replace('Z', '+08:00'))
    now = datetime.now(expires.tzinfo)
    remaining = expires - now
    
    if remaining.total_seconds() < 0:
        return "❌ 已过期"
    elif remaining.total_seconds() < 86400:  # 24小时
        return f"⚠️ 即将过期（剩余 {remaining_hours}h）"
    else:
        days = remaining.days
        return f"✅ 正常（剩余 {days} 天）"

status = await mcp.check_login_status()
print(check_expiry(status))
```

---

## 登录方式

### 方式一：Cookie 登录（推荐自动化）

```python
# 直接设置 Cookie
await mcp.set_cookies({
    "cookies": "完整的Cookie字符串",
    "device_id": "可选设备ID"
})

# 验证 Cookie 有效性
status = await mcp.check_login_status()
assert status["logged_in"], "Cookie 无效"
```

**Cookie 获取**：
```bash
# 方法1：浏览器插件 EditThisCookie 导出
# 方法2：Chrome DevTools → Application → Cookies 复制
# 方法3：小红书App → 设置 → 账号与安全 → 登录设备管理
```

### 方式二：扫码登录（需要人工介入）

```python
# 生成登录二维码
qr_data = await mcp.generate_qr_code()

# 返回二维码图片的 base64 或 URL
print(f"请扫码登录：{qr_data['qr_url']}")
# 用户扫码后...
result = await mcp.wait_for_scan(qr_data['ticket'])
# result['success'] = True 时登录完成
```

### 方式三：手机号验证码登录

```python
# 发送验证码
await mcp.send_sms_code(phone_number="138xxxxxxx")

# 验证验证码
result = await mcp.verify_sms_code(
    phone="138xxxxxxx",
    code="123456"
)
```

---

## 多账号管理

### 添加新账号

```python
# 添加账号（不激活）
await mcp.add_account(
    id="account_work",
    name="工作号",
    cookies="工作号Cookie"
)

# 激活账号
await mcp.switch_account("account_work")

# 验证切换
status = await mcp.check_login_status()
print(f"当前账号: {status['nickname']}")
```

### 账号列表

```python
accounts = await mcp.list_accounts()
# 返回格式：
# [
#   {"id": "account_personal", "name": "私人号", "enabled": true},
#   {"id": "account_work", "name": "工作号", "enabled": false},
# ]
```

### 账号切换

```python
# 切换前先登出当前账号（可选）
await mcp.logout()

# 切换到指定账号
await mcp.switch_account("account_personal")

# 自动检查登录
status = await mcp.check_login_status()
if status["logged_in"]:
    print(f"✅ 已切换到: {status['nickname']}")
```

### 删除账号

```python
await mcp.remove_account("account_old")
```

---

## Token 刷新机制

### 自动刷新

```python
# 配置自动刷新（建议每12小时）
REFRESH_INTERVAL = 12 * 3600  # 12小时

async def auto_refresh_token():
    while True:
        await asyncio.sleep(REFRESH_INTERVAL)
        try:
            await mcp.refresh_token()
            print("✅ Token 已自动刷新")
        except Exception as e:
            print(f"❌ Token 刷新失败: {e}")
```

### 手动刷新

```python
# 强制刷新
result = await mcp.refresh_token(force=True)

if result["success"]:
    print(f"✅ Token 刷新成功，新有效期: {result['expires_at']}")
else:
    print(f"❌ 刷新失败: {result['error']}")
    # 引导用户重新配置 Cookie
```

### 刷新失败处理

```python
async def safe_call_with_refresh(tool_name, *args, **kwargs):
    try:
        return await mcp.call(tool_name, *args, **kwargs)
    except TokenExpiredError:
        print("Token 已过期，尝试刷新...")
        refresh_result = await mcp.refresh_token()
        if refresh_result["success"]:
            return await mcp.call(tool_name, *args, **kwargs)
        else:
            raise LoginRequiredError("请重新登录")
```

---

## 登录异常处理

| 错误码 | 含义 | 处理方法 |
|--------|------|---------|
| `10001` | Cookie 无效 | 重新获取并配置 Cookie |
| `10003` | Token 过期 | 触发刷新或重新登录 |
| `10010` | 账号被封禁 | 查看封禁详情，无法自动恢复 |
| `10020` | IP 风控 | 等待 24-72 小时或换 IP |
| `10030` | 设备风控 | 换设备登录或联系客服 |

### 被封禁检测

```python
status = await mcp.check_login_status()
if "banned" in status:
    print(f"⚠️ 账号状态异常: {status['banned_reason']}")
    # 被封禁后无法自动恢复，需要人工申诉
```

---

## 账号安全建议

1. **Cookie 不要分享给他人** — 相当于账号密码
2. **不要在公共 WiFi 下操作** — 容易导致账号风控
3. **一个 IP 登录多个账号** — 容易触发关联封禁
4. **新账号前两周保守操作** — 养号期降低频率
5. **定期刷新 Token** — 防止长时间不用过期

---

## 检查命令汇总

```bash
# 1. 检查 MCP 服务状态
curl http://localhost:3100/health

# 2. 检查登录状态
python3 -c "
import asyncio
from xiaohongshu_mcp import Client
async def main():
    client = Client()
    status = await client.check_login_status()
    print(status)
asyncio.run(main())
"

# 3. 查看账号列表
python3 -c "
import asyncio
from xiaohongshu_mcp import Client
async def main():
    client = Client()
    accounts = await client.list_accounts()
    for acc in accounts:
        print(f'{acc['name']}: {acc[\"enabled\"]}')
asyncio.run(main())
"

# 4. 查看 Token 有效期
python3 -c "
import asyncio
from xiaohongshu_mcp import Client
async def main():
    client = Client()
    status = await client.check_login_status()
    print(f'过期时间: {status[\"expires_at\"]}')
asyncio.run(main())
"
```

---

*Version: 1.0.0 | Updated: 2026-04-23*