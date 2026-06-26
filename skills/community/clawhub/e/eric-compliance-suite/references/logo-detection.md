# L001 图形商标检测 API 参考

## 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/trademark/graphic/v1/detection`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

## 注意事项

1. 图片传参仅支持 base64
2. 单次调用最多返回 TOP100 条图形商标数据（根据图片实际情况，可能返回数量少于传参设定值）
3. 费用根据是否开启切图和是否开启雷达收取不同费用：
   - `enable_radar=false`：10 点/次
   - `enable_radar=true`：15 点/次

## 请求参数

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_title` | string | false | 产品标题 |
| `top_number` | int | true | 返回商标的最大数量（实际可能少于该值） |
| `trademark_name` | string | false | 可能的图形 logo 名称 |
| `regions` | array | false | 检测国家/地区，不传默认全部。支持：US, WO, ES, GB, DE, IT, CA, MX, EM, AU, FR, JP, TR, BX, CN |
| `base64_image` | string | true | 产品图片 base64 编码 |
| `enable_localizing` | boolean | false | 是否开启切图（自动识别 logo 区域），默认 false |
| `enable_radar` | boolean | false | 是否开启雷达检测，默认 false |

## 请求示例

```json
{
  "product_title": "Spigen Triple-Coated CryoShade Front Windshield Sunshade",
  "base64_image": "iVBORw0KGgoAAAANSUhEUgAA...",
  "trademark_name": "",
  "top_number": 20,
  "regions": ["US"],
  "enable_localizing": true,
  "enable_radar": true
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
| `bounding_box_count` | int | 切图区域数量 |
| `detection_results` | array | 按切图区域分组的检测结果 |
| `radar_result` | string | 整体雷达风险等级（low_risk/high_risk） |

### data.detection_results[]

| Parameter | Type | Description |
|-----------|------|-------------|
| `index` | integer | 切图区域排序序号 |
| `bounding_box` | array | YOLO 坐标 [x1, y1, x2, y2] |
| `top_graphic_trademarks` | array | 按国家/地区分组的商标结果 |
| `total_detection_result_count` | number | 该区域召回商标数量 |

### data.detection_results[].top_graphic_trademarks[]

| Parameter | Type | Description |
|-----------|------|-------------|
| `region` | string | 国家/地区代码 |
| `graphic_trademarks` | array | 该国家/地区的相似商标列表 |

### data.detection_results[].top_graphic_trademarks[].graphic_trademarks[]

| Parameter | Type | Description |
|-----------|------|-------------|
| `bid` | string | 商标标识 ID |
| `similarity` | float | 相似度（0-1） |
| `nice_class` | array | 尼斯分类，`[{code, name}]` |
| `registration_office_code` | string | 商标受理局 |
| `application_number` | string | 申请号 |
| `registration_number` | string | 注册号 |
| `trademark_name` | string | 图片中的文字商标名称 |
| `applicant_name` | array | 权利人列表 |
| `trade_mark_status` | string | 商标状态：DEL, ended, registered, act, pend, filed, Expired |
| `image` | string | 商标图片 URL |
| `application_date` | string | 申请日期 |
| `registration_date` | string | 注册日期 |
| `sub_radar_result` | string | 子雷达结果（low_risk/high_risk） |

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

### 图形商标检测相关

| code | 常量名 | 说明 |
|---------|----------------------------------------------|--------------------------------------|
| 4002001 | GRAPHIC_LOCALIZING_EMPTY_ERROR | 图形定位接口返回为空 |
| 4002002 | GRAPHIC_LOCALIZING_ERROR | 图形定位接口异常 |
| 4002003 | WITHOUT_GRAPHIC_TRADEMARK_DETAIL_EMPTY_ERROR | 无定位商标检测返回为空 |
| 4002004 | WITHOUT_GRAPHIC_LOCALIZING_ERROR | 无定位商标检测异常 |
| 4002005 | GRAPHIC_TRADEMARK_DETAIL_ERROR | 商标详情接口异常 |
| 4002006 | DSC_NC_CODE_EMPTY_ERROR | 尼斯分类返回为空 |
| 4002007 | DSC_NC_CODE_ERROR | 尼斯分类接口异常 |
| 4002008 | NO_GRAPHIC_TRADEMARK_DETAIL_ERROR | 无商标详情数据 |
| 4002009 | RADAR_ERROR | 雷达检测异常 |

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
    "id": 775010390014378000,
    "bounding_box_count": 6,
    "detection_results": [
      {
        "index": 0,
        "bounding_box": [413.48, 520.34, 465.68, 560.03],
        "top_graphic_trademarks": [
          {
            "region": "US",
            "graphic_trademarks": [
              {
                "bid": "1058054724906610688",
                "similarity": 0.534,
                "nice_class": [{"code": 9, "name": "3C、电动工具、科研仪器设备"}],
                "registration_office_code": "US",
                "application_number": "88489418",
                "registration_number": "5934469",
                "trademark_name": "",
                "applicant_name": ["Duracell U.S. Operations, Inc."],
                "trade_mark_status": "Registered",
                "image": "https://patent-oss-image.suntekcorps.com/USPTO_TRADEMARK/88489418.png",
                "application_date": "2019-06-26",
                "registration_date": "2019-12-10",
                "sub_radar_result": "low_risk"
              }
            ]
          }
        ],
        "total_detection_result_count": 2
      }
    ],
    "radar_result": "high_risk"
  },
  "request_id": "20250427145416-73mOBi3eaxH2ztGE"
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

curl -s -X POST "https://saas.eric-bot.com/v1.0/eric-api/trademark/graphic/v1/detection" \
  -H "Content-Type: application/json" \
  -H "Token: ${ERIC_API_TOKEN}" \
  -d "$(cat <<EOF
{
  "base64_image": "${IMG_B64}",
  "top_number": 20,
  "regions": ["US"],
  "enable_localizing": true,
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
    "https://saas.eric-bot.com/v1.0/eric-api/trademark/graphic/v1/detection",
    headers={"Content-Type": "application/json", "Token": os.environ["ERIC_API_TOKEN"]},
    json={
        "base64_image": img_b64,
        "top_number": 20,
        "regions": ["US"],
        "enable_localizing": True,
        "enable_radar": False,
    },
)
data = resp.json()
```
