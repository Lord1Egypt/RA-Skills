# Byted SMS Sender — 凭证配置指南

本文档说明 Byted SMS Sender 所需的 API 凭证配置。

## 凭证说明

本技能使用以下两个环境变量进行认证：

- `ARK_SKILL_API_KEY` - API 密钥（Bearer Token）
- `ARK_SKILL_API_BASE` - API 基础地址



```bash
cat /root/.openclaw/.env
```

### 凭证示例

```
ARK_SKILL_API_KEY=sk-xxxx
ARK_SKILL_API_BASE=http://xxx
```

## 凭证缺失处理

如果检查后发现凭证缺失：

1. 确认配置文件 `/root/.openclaw/.env` 是否存在
2. 确认环境变量是否正确加载
3. 如果仍然找不到，请联系 **oncall** 获取帮助

## 验证配置

```bash
cd skills/byted-sms-sender
python3 scripts/volc_sms.py list_sub_account
```

如果返回消息组列表，说明配置正确。

## 认证方式说明

所有 API 请求使用 Bearer Token 认证，请求格式如下：

```bash
curl -X POST 'https://<ARK_SKILL_API_BASE>?Action=ListSubAccountForAgent&Version=2026-01-01' \
  -H 'Content-Type: application/json' \
  -H 'ServiceName: volcSMS' \
  -H 'Authorization: Bearer <ARK_SKILL_API_KEY>' \
  -d '{}'
```

### 请求头说明

| Header | 说明 |
|--------|------|
| `Content-Type` | 固定为 `application/json` |
| `ServiceName` | 固定为 `volcSMS` |
| `Authorization` | 格式为 `Bearer <ARK_SKILL_API_KEY>` |

## 常见问题

### Q: 环境变量未生效怎么办?

A: 检查以下几点：
1. 确认配置文件路径正确：`/root/.openclaw/.env`
2. 确认环境变量名称正确（区分大小写）
3. 尝试重新加载配置：`source /root/.openclaw/.env`

### Q: 找不到凭证怎么办?

A: 凭证由 ArkClaw 预先配置，如果找不到请联系 oncall 获取帮助。

### Q: API 调用返回认证错误?

A: 检查：
1. 自己配置的 AK/SK 是否正确
2. 凭证是否已过期，如过期请联系 oncall
