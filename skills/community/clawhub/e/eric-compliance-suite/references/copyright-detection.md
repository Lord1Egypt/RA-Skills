# C001 版权检测 API 参考

## 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/copyright/v1/detection`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

## 注意事项

1. 图片传参仅支持 base64，以数组形式传入（`img_64lis`），目前仅支持单张图片
2. 每次调用收取 1 点费用（1 点/次）
3. `enable_radar` 为必传参数，控制是否开启雷达风险分析

## 请求参数

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `img_64lis` | array | true | 检测的产品图片 base64 编码列表 |
| `top_number` | integer | false | 召回数量（默认 100，最大 200） |
| `enable_radar` | boolean | true | 是否开启雷达风险分析 |

## 请求示例

```json
{
  "img_64lis": ["/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAo..."],
  "top_number": 100,
  "enable_radar": false
}
```

## 响应结构

### 顶层

| Parameter | Type | Description |
|-----------|------|-------------|
| `success` | boolean | 调用是否成功 |
| `code` | integer | 状态码 |
| `message` | string | 调用信息 |
| `data` | object | 返回数据 |

### data

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | int | 检测记录 ID |
| `list` | array | 版权画结果列表 |

### data.list[]

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | string | 版权画图片路径 |
| `path_thumb` | string | 版权画缩略图路径 |
| `rights_owner` | string | 权利人 |
| `link` | string | 版权官网链接 |
| `design_url` | string | 版权画来源页面 |
| `design_code` | string | 版权标识码 |
| `cosine` | float | 相似度（0-1） |
| `cas_risk` | string | 风险等级（null=未进行雷达检测，如需请使用 C002 接口） |

## 错误码

### 通用错误码

| code | 常量名 | 说明 |
|--------|--------------------------------------|--------------------------------------|
| 0 | SYSTEM_ERROR | 系统异常 |
| 500 | SERVER_ERROR | 服务器错误 |
| 100007 | PARAM_INVALID | 参数错误（缺少必填字段或格式不正确） |
| 30007 | INVALID_ACCESS_TOKEN | Token 无效或已过期 |

### 积分相关

| code | 常量名 | 说明 |
|---------|------------------------|------------------------|
| 4000011 | CONSUME_EMPTY_ERROR | 扣点 API 返回为空 |
| 4000012 | PRE_DEDUCT_POINT_ERROR | 预扣点失败（余额不足） |
| 4000013 | DEDUCT_POINT_ERROR | 扣点失败 |
| 4000014 | ROLLBACK_POINT_ERROR | 回滚积分失败 |

### 图片上传相关

| code | 常量名 | 说明 |
|---------|----------------------|--------------------------|
| 4000020 | OSS_UPLOAD_ERROR | 图片上传 OSS 异常 |
| 4000021 | OSS_UPLOAD_URL_ERROR | 图片 URL 上传 OSS 异常 |

### 版权检测相关

| code | 常量名 | 说明 |
|---------|------------------------|--------------------------------------|
| 4005001 | COPYRIGHT_DETECT_ERROR | 版权检测接口异常 |
| 4005002 | COPYRIGHT_CAS_ERROR | 版权雷达分析异常 |
| 4005003 | COPYRIGHT_NO_DATA | 未找到相似版权数据 |

### 超时

| code | 常量名 | 说明 |
|---------|-----------------|--------------------------------------|
| 5000504 | GATEWAY_TIMEOUT | 请求超时（检测时间较长时可能触发） |

### 错误响应示例

```json
{
  "success": false,
  "code": 100007,
  "message": "参数错误",
  "data": null
}
```

## 响应示例

```json
{
  "success": true,
  "code": 200,
  "message": "success",
  "data": {
    "id": "748955404365561856",
    "list": [
      {
        "path": "https://eric-oss-image.oss-cn-shenzhen.aliyuncs.com/copyright/redbubble/design/104108784.jpg",
        "path_thumb": "",
        "rights_owner": "benmaydart",
        "link": "https://www.redbubble.com",
        "design_url": "https://www.redbubble.com/shop/ap/104108784",
        "note": null,
        "design_code": "RB104108784",
        "cosine": 0.6254262924194336,
        "cas_risk": null
      },
      {
        "path": "https://eric-oss-image.oss-cn-shenzhen.aliyuncs.com/copyright/redbubble/design/92914010.jpg",
        "path_thumb": "",
        "rights_owner": "HorrorsShop",
        "link": "https://www.redbubble.com",
        "design_url": "https://www.redbubble.com/shop/ap/92914010",
        "note": null,
        "design_code": "RB92914010",
        "cosine": 0.5950914621353149,
        "cas_risk": null
      }
    ]
  },
  "request_id": "20250214172122-L7qa4UKTBRuPrkNm"
}
```

## 代码示例

### Shell

```bash
# 检查 Token 环境变量
if [ -z "${ERIC_API_TOKEN}" ]; then
  echo "错误：请先设置 ERIC_API_TOKEN 环境变量" >&2
  exit 1
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
  IMG_B64=$(base64 -i /path/to/image.png | tr -d '\n')
else
  IMG_B64=$(base64 -w 0 /path/to/image.png)
fi

curl -s -X POST "https://saas.eric-bot.com/v1.0/eric-api/copyright/v1/detection" \
  -H "Content-Type: application/json" \
  -H "Token: ${ERIC_API_TOKEN}" \
  -d "$(cat <<EOF
{
  "img_64lis": ["${IMG_B64}"],
  "top_number": 100,
  "enable_radar": false
}
EOF
)"
```

### Python

```python
import base64, requests, os, sys

if "ERIC_API_TOKEN" not in os.environ:
    print("错误：请先设置 ERIC_API_TOKEN 环境变量", file=sys.stderr)
    sys.exit(1)

with open("/path/to/image.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

resp = requests.post(
    "https://saas.eric-bot.com/v1.0/eric-api/copyright/v1/detection",
    headers={"Content-Type": "application/json", "Token": os.environ["ERIC_API_TOKEN"]},
    json={"img_64lis": [img_b64], "top_number": 100, "enable_radar": False},
)
data = resp.json()
```
