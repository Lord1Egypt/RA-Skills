name: deepseek-balance
description: 查询 DeepSeek API 账户余额。当用户询问 DeepSeek 余额、配额、剩余额度时使用此技能。

# DeepSeek 余额查询技能

## 环境变量配置
脚本需要 API Key。优先检查 `DEEPSEEK_API_KEY`，若未设置则自动回退检查 `ANTHROPIC_AUTH_TOKEN`。

## 执行脚本
直接运行以下 Bash 脚本查询余额：

```bash
#!/bin/bash

# 1. 获取 API Key (优先使用 DEEPSEEK_API_KEY，兼容 ANTHROPIC_AUTH_TOKEN)
API_KEY="${DEEPSEEK_API_KEY:-$ANTHROPIC_AUTH_TOKEN}"

if [ -z "$API_KEY" ]; then
    echo "❌ 错误: 环境变量 DEEPSEEK_API_KEY 或 ANTHROPIC_AUTH_TOKEN 未设置"
    echo ""
    echo "请运行以下命令设置（以 DEEPSEEK_API_KEY 为例）："
    echo "export DEEPSEEK_API_KEY='your-deepseek-api-key'"
    echo ""
    echo "Linux/macOS 永久设置："
    echo "echo 'export DEEPSEEK_API_KEY=\"your-deepseek-api-key\"' >> ~/.bashrc"
    echo "source ~/.bashrc"
    echo ""
    echo "Windows (PowerShell): \$env:DEEPSEEK_API_KEY='your-deepseek-api-key'"
    exit 1
fi

echo "🔍 正在查询 DeepSeek API 余额..."

# 2. 发送请求并捕获 HTTP 状态码与响应体
RESPONSE=$(curl -s -L -w "\n%{http_code}" -X GET 'https://api.deepseek.com/user/balance' \
    -H 'Accept: application/json' \
    -H "Authorization: Bearer $API_KEY")

# 分离 HTTP 状态码和 Body
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

# 3. 处理响应
if [ "$HTTP_CODE" -eq 200 ] 2>/dev/null; then
    # 使用 Python 解析 JSON，比 grep/cut 更稳健，支持格式化输出
    echo "$BODY" | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)
    if data.get('is_available'):
        balance = data.get('balance_infos', [{}])[0]
        currency = balance.get('currency', 'CNY')
        total = balance.get('total_balance', '0.00')
        granted = balance.get('granted_balance', '0.00')
        topped = balance.get('topped_up_balance', '0.00')
        
        print('')
        print('✅ DeepSeek API 余额信息')
        print(f'💰 货币: {currency}')
        print(f'💰 总余额: {total} {currency}')
        print(f'🎁 赠送余额: {granted} {currency}')
        print(f'💳 充值余额: {topped} {currency}')
        print(f'📊 账户状态: 可用')
    else:
        print('⚠️ DeepSeek API 账户无可用余额')
except Exception as e:
    print(f'❌ JSON 解析失败: {e}', file=sys.stderr)
    sys.exit(1)
"
elif [ "$HTTP_CODE" -eq 401 ]; then
    echo "❌ 认证失败: API Key 无效或已过期"
    echo "请检查 API Key 是否正确"
elif [ "$HTTP_CODE" -eq 429 ]; then
    echo "❌ 请求过于频繁，请稍后重试"
elif [ "$HTTP_CODE" -eq 500 ] || [ "$HTTP_CODE" -eq 503 ]; then
    echo "❌ DeepSeek 服务异常，请稍后重试"
else
    echo "❌ 查询失败 (HTTP $HTTP_CODE)"
    echo "$BODY"
fi
```

## 快速执行（一行命令）
适用于终端快速检查，无需创建脚本文件，自动兼容环境变量：

```bash
[ -z "${DEEPSEEK_API_KEY:-$ANTHROPIC_AUTH_TOKEN}" ] && echo "⚠️ 请先设置 DEEPSEEK_API_KEY 或 ANTHROPIC_AUTH_TOKEN" || curl -s -X GET 'https://api.deepseek.com/user/balance' -H "Authorization: Bearer ${DEEPSEEK_API_KEY:-$ANTHROPIC_AUTH_TOKEN}" | python3 -c "import sys,json; d=json.load(sys.stdin); b=d.get('balance_infos',[{}])[0] if d.get('is_available') else None; print(f\"✅ 总余额: {b['total_balance']} {b['currency']}\n🎁 赠送: {b['granted_balance']}\n💳 充值: {b['topped_up_balance']}\") if b else print('⚠️ 无可用余额')"
```

## 输出示例

**成功时：**
```
🔍 正在查询 DeepSeek API 余额...

✅ DeepSeek API 余额信息
💰 货币: CNY
💰 总余额: 110.00 CNY
🎁 赠送余额: 10.00 CNY
💳 充值余额: 100.00 CNY
📊 账户状态: 可用
```

**未设置 API Key 时：**
```
❌ 错误: 环境变量 DEEPSEEK_API_KEY 或 ANTHROPIC_AUTH_TOKEN 未设置
请运行以下命令设置（以 DEEPSEEK_API_KEY 为例）：
export DEEPSEEK_API_KEY='your-deepseek-api-key'
...
```

**认证失败时：**
```
❌ 认证失败: API Key 无效或已过期
请检查 API Key 是否正确
```
