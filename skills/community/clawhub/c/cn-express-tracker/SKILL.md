---
name: cn-express-tracker
description: "Query package tracking information from Chinese and international carriers using Kuaidi100 API. Supports auto-detection of carrier from tracking number. Use when user asks to track a package, check delivery status, query express/courier/logistics info, or mentions a tracking number. Triggers: 查快递, 快递查询, 物流查询, track package, tracking number, delivery status, 单号查询, express tracking, courier tracking."
---

# Express Tracker（快递物流查询）

Track packages from 200+ carriers (Chinese domestic + international) via Kuaidi100 API.

## Setup (Required)

Users must obtain their own Kuaidi100 API credentials:

1. **Register** at [Kuaidi100 Open Platform](https://api.kuaidi100.com/register/enterprise)
   - 注册企业版账号（个人也可注册）
   - Free tier: 100 queries/day after verification

2. **Get credentials** from the [Kuaidi100 Dashboard](https://api.kuaidi100.com/home):
   - **授权 Key（API Key）**: Found in 授权信息 → 授权key
   - **Customer ID**: Found in 授权信息 → customer

3. **Set environment variables**:
   ```bash
   export EXPRESS_TRACKER_KEY="your_api_key_here"
   export EXPRESS_TRACKER_CUSTOMER="your_customer_id_here"
   ```

   For persistent config, add to `~/.bashrc` or `~/.zshrc`:
   ```bash
   echo 'export EXPRESS_TRACKER_KEY="your_key"' >> ~/.zshrc
   echo 'export EXPRESS_TRACKER_CUSTOMER="your_customer"' >> ~/.zshrc
   ```

## Usage

```bash
# Auto-detect carrier and query
scripts/track.sh <tracking_number>

# Specify carrier manually
scripts/track.sh <tracking_number> <carrier_code>
```

### Examples

```bash
# Auto-detect (recommended)
scripts/track.sh 770308811947591

# Specify carrier explicitly
scripts/track.sh SF1234567890 shunfeng
```

## How It Works

1. **Carrier auto-detection**: Local rule-based matching by tracking number prefix/length/format
2. **API query**: Sends signed request to Kuaidi100 poll API with `resultv2=4` for advanced status
3. **Output**: Formatted timeline with full tracking history (newest first)

## Supported Carriers (Auto-Detection)

| Prefix/Pattern | Carrier | Code |
|---|---|---|
| `SF` | 顺丰速运 | `shunfeng` |
| `YT` | 圆通速递 | `yuantong` |
| `JT` / `J0` | 极兔速递 | `jitu` |
| `JD` | 京东快递 | `jd` |
| `CN` | 菜鸟速递 | `cainiao` |
| `DPK` | 德邦快递 | `debangkuaidi` |
| `KYE` | 跨越速运 | `kuayue` |
| `AN` | 安能物流 | `annengwuliu` |
| `1Z` | UPS | `ups` |
| `78/73/72/21/68` + digits | 中通快递 | `zhongtong` |
| `10/11/12/13/19/46` + 13 digits | 韵达快递 | `yunda` |
| `77/88/66/55/44` + 13-15 digits | 申通快递 | `shentong` |
| `E` + letter + 9 digits + 2 letters | EMS | `ems` |

If auto-detection fails, specify the carrier code manually as the second argument.

Full carrier code list: [Kuaidi100 Carrier Codes](https://api.kuaidi100.com/manager/openapi/download/kdbm.do)

## Dependencies

- `curl` — HTTP requests
- `jq` — JSON parsing (install: `brew install jq` / `apt install jq`)
- `openssl` or `md5sum` or `md5` — MD5 signature (at least one required)

## Error Codes

| Code | Meaning | Action |
|---|---|---|
| 400 | Incomplete data / wrong carrier | Check carrier code |
| 408 | Phone verification failed | SF/ZTO require phone number |
| 500 | No tracking info found | Verify tracking number and carrier |
| 503 | Signature verification failed | Check API Key and Customer ID |
| 601 | API Key expired / no balance | Recharge account |

## Agent Integration

When a user provides a tracking number, run:

```bash
EXPRESS_TRACKER_KEY="$KEY" EXPRESS_TRACKER_CUSTOMER="$CUSTOMER" scripts/track.sh <number>
```

Parse the output and present the tracking timeline to the user. If carrier detection fails, ask the user which carrier it is.
