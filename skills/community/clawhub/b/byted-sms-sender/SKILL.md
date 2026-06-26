---
name: byted-sms-sender
version: 1.2.0
author: volcengine-sms-team
description: 火山引擎短信服务管理工具。在需要使用云通信能力，包括发送短信，查询消息组，模板信息，发送详情，状态以及整体发送统计时，可以使用这个能力。
homepage: https://www.volcengine.com/docs/6361/66704?lang=zh
---

# Byted SMS Sender

火山引擎短信服务 API,版本 2026-01-01

## 何时使用

当用户有以下需求时,使用本 skill:

**发送短信场景:**

- 需要发送验证码短信
- 需要发送通知类短信
- 需要发送营销类短信
- 用户说"发短信""发送验证码""发通知"时

**查询场景:**

- 需要查询可用的消息组(子账号)
- 需要查询已审核通过的短信签名
- 需要查询已审核通过的短信模板
- 需要查询短信发送记录
- 需要查询发送统计(成功率等)

## 使用前检查

检查是否已配置以下凭证:

- `ARK_SKILL_API_KEY` - API 密钥
- `ARK_SKILL_API_BASE` - API 基础地址

这些凭证由 **ArkClaw** 预先配置在终端环境中，配置文件位置: `/root/.openclaw/.env`

检查方式:
```bash
echo $ARK_SKILL_API_KEY
echo $ARK_SKILL_API_BASE
```

如果缺少凭证:
1. 检查配置文件 `/root/.openclaw/.env` 是否存在
2. 如果仍然找不到，请联系 **oncall** 获取帮助

## 6个接口说明

### 1. send\_sms - 发送短信

**场景:** 用户需要发送验证码、通知、营销短信

**使用方式:**

```bash
python3 scripts/volc_sms.py send_sms \
  --sub-account "消息组ID" \
  --signature "签名" \
  --template-id "模板ID" \
  --mobiles "手机号" \
  --template-param '{"code":"123456"}'
```

**参数说明:**

- `--sub-account`: 消息组ID(必填),从 list\_sub\_account 获取
- `--signature`: 短信签名(必填),从 list\_signature 获取
- `--template-id`: 模板ID(必填),从 list\_sms\_template 获取
- `--mobiles`: 手机号(必填),多个用逗号分隔
- `--template-param`: 模板参数(可选),JSON格式

### 2. list\_sub\_account - 查询消息组

**场景:** 需要知道可以用哪个消息组发送短信

**使用方式:**

```bash
python3 scripts/volc_sms.py list_sub_account
```

**参数说明:**

- `--sub-account-name`: 可选,按名称模糊搜索

### 3. list\_signature - 查询签名

**场景:** 需要知道可以用哪个签名,或者查询签名是否审核通过

**使用方式:**

```bash
python3 scripts/volc_sms.py list_signature --signature "火山引擎"
```

**参数说明:**

- `--signature`: 可选,按签名模糊搜索
- `--sub-accounts`: 可选,按子账号过滤
- `--page`: 页码,默认1
- `--page-size`: 每页数量,默认20

### 4. list\_sms\_template - 查询模板

**场景:** 需要知道可以用哪个模板,或者查询模板参数

**使用方式:**

```bash
python3 scripts/volc_sms.py list_sms_template --signatures "火山引擎"
```

**参数说明:**

- `--template-id`: 可选,按模板ID模糊搜索
- `--signatures`: 可选,按签名过滤
- `--sub-accounts`: 可选,按子账号过滤
- `--page`: 页码,默认1
- `--page-size`: 每页数量,默认20

### 5. list\_sms\_send\_log - 查询发送记录

**场景:** 需要查看某条短信的发送状态,或批量查询发送历史

**使用方式:**

```bash
python3 scripts/volc_sms.py list_sms_send_log \
  --sub-account "消息组ID" \
  --from-time 1773113285 \
  --to-time 1773213285
```

**参数说明:**

- `--sub-account`: 必填,消息组ID
- `--from-time`: 开始时间戳(秒)
- `--to-time`: 结束时间戳(秒)
- `--mobile`: 可选,按手机号过滤
- `--template-id`: 可选,按模板ID过滤
- `--signature`: 可选,按签名过滤
- `--message-id`: 可选,按消息ID精确查询
- `--page`: 页码,默认1
- `--page-size`: 每页数量,默认100

### 6. list\_total\_send\_count\_stat - 查询发送统计

**场景:** 需要查看发送成功率、接收成功率等统计信息

**使用方式:**

```bash
python3 scripts/volc_sms.py list_total_send_count_stat \
  --start-time 1773113285 \
  --end-time 1773213285
```

**参数说明:**

- `--start-time`: 必填,开始时间戳(秒)
- `--end-time`: 必填,结束时间戳(秒)
- `--sub-account`: 可选,按消息组过滤
- `--channel-type`: 可选,通道类型
- `--signature`: 可选,按签名过滤
- `--template-id`: 可选,按模板ID过滤

**返回字段:**

- TotalSendCount: 总发送数
- TotalSendSuccessCount: 发送成功数
- TotalSendSuccessRate: 发送成功率
- TotalReceiptSuccessCount: 接收成功数
- TotalReceiptSuccessRate: 接收成功率

## 典型使用流程

### 第一次发送短信

1. **查询可用的消息组**
   ```bash
   python3 scripts/volc_sms.py list_sub_account
   ```
2. **查询可用的签名**
   ```bash
   python3 scripts/volc_sms.py list_signature
   ```
3. **查询可用的模板**
   ```bash
   python3 scripts/volc_sms.py list_sms_template --signatures "火山引擎"
   ```
4. **发送短信**
   ```bash
   python3 scripts/volc_sms.py send_sms \
     --sub-account "xxxx" \
     --signature "xxx" \
     --template-id "ST_xxxx" \
     --mobiles "188xxxxxxx8" \
     --template-param '{"code":"888888"}'
   ```

### 查询发送状态

```bash
python3 scripts/volc_sms.py list_sms_send_log \
  --sub-account "77da1acf" \
  --from-time 1773113285 \
  --to-time 1773213285
```

## 常见错误码

- `RE:0001`: 账号短信服务未开通
- `RE:0003`: 子账号不存在(消息组ID错误)
- `RE:0004`: 签名错误(签名不存在或未审核通过)
- `RE:0005`: 模板错误(模板不存在或未审核通过)
- `RE:0006`: 手机号格式错误
- `RE:0010`: 账号欠费
- `ZJ10200`: 请求参数错误

## 注意事项

1. **签名和模板**: 必须使用已审核通过的签名和模板
2. **手机号格式**:
   - 国内短信: 11位手机号或 +86开头
   - 国际短信: 必须包含国际区号,符合 E.164 标准
3. **批量限制**: 单次最多200个手机号
4. **签名子账号匹配**: 签名和消息组需要匹配,可从 list\_signature 的 SubAccounts 字段确认
5. **模板签名匹配**: 模板和签名需要匹配,可从 list\_sms\_template 的 Signature 字段确认

## 故障排查

- 缺少凭证: 检查 `/root/.openclaw/.env` 文件，如仍找不到请联系 oncall
- 发送失败: 先用 list\_sub\_account、list\_signature、list\_sms\_template 确认参数正确
- 鉴权失败: 检查自己配置的 AK/SK 是否开通正确
- 权限错误: 检查凭证是否正确，如问题持续请联系 oncall
- 欠费错误: 请联系 oncall 处理
