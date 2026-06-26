# configure（配置AK）

## 功能说明

查看或设置 AK 认证密钥。支持无参数查看状态、带参数设置新 AK。

## 认证机制

网关请求（`skills-gateway.1688.com`）使用 HMAC-SHA256 签名认证。

### AK 来源优先级
1. **环境变量**（优先）：`ALI_1688_AK`（OpenClaw 自动注入）
2. **配置文件**（fallback）：`~/.openclaw/openclaw.json` 中 `skills.entries["1688-reception-assistant"].apiKey`

### AK 格式
- 前 32 字符 = AccessKeySecret，其余 = AccessKeyId
- 可选 Base64 URL-safe 编码
- 合法字符：`A-Za-z0-9_-=+/`

## CLI 调用

```bash
python3 cli.py configure              # 查看当前配置状态
python3 cli.py configure YOUR_AK      # 设置新的 AK
```

## 输出格式

### 查看状态 - 已配置
```json
{
  "success": true,
  "markdown": "AK 已配置: `AbCd****5678`（来源: 环境变量（已生效））",
  "data": { "configured": true }
}
```

### 查看状态 - 未配置
```json
{
  "success": false,
  "markdown": "AK 尚未配置\n\n运行: `cli.py configure YOUR_AK`",
  "data": { "configured": false }
}
```

## 注意事项

1. AK 展示时始终脱敏（前4位 + **** + 后4位）
2. AK 长度必须至少 32 位，否则校验失败
3. 配置写入后，新开会话自动生效
