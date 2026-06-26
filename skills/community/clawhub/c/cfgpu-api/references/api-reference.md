# CFGPU API Reference

## Base Information

- **Service Domain**: `https://api.cfgpu.com`
- **Authentication**: API Token in Authorization header
- **Response Format**: Standard JSON response with `success`, `errorCode`, `errorMsg`, `content`

## API Endpoints

### 1. Region Management

#### GET /userapi/v1/region/list
Get list of supported regions.

**Response**:
```json
[
  {
    "code": "hz",
    "name": "杭州"
  }
]
```

### 2. GPU Type Management

#### GET /userapi/v1/gpu/list
Get list of available GPU types.

**Response**:
```json
[
  {
    "code": "qnid2x6c",
    "name": "RTX 4090"
  }
]
```

### 3. Image Management

#### GET /userapi/v1/image/privateList
Get user custom images.

**Parameters**:
- `adaptType`: `CONTAINER` or `VM`

**Response**:
```json
[
  {
    "code": "image_gzo9zvxs",
    "name": "ComfyUI 定制版",
    "sysDiskLimitMinSize": 0
  }
]
```

#### GET /userapi/v1/image/systemList
Get system images provided by platform.

**Parameters**:
- `adaptType`: `CONTAINER` or `VM`

**Response** (nested structure):
```json
[
  {
    "name": "Tensorflow",
    "childrenName": "版本",
    "children": [
      {
        "name": "2.15.0",
        "childrenName": "Python 版本",
        "children": [
          {
            "name": "3.11(ubuntu20.04)",
            "childrenName": "Cuda 版本",
            "children": [
              {
                "name": "12.2",
                "code": "image_exc6f72b",
                "sysDiskLimitMinSize": 0
              }
            ]
          }
        ]
      }
    ]
  }
]
```

### 4. Instance Management

#### POST /userapi/v1/instance/create
Create a new GPU instance.

**Request Body**:
```json
{
  "priceType": "Day",
  "regionCode": "hz",
  "gpuType": "qnid2x6c",
  "gpuNum": 1,
  "sysDiskExpandSize": 0,
  "expandSize": 0,
  "imageId": "image_xxxx",
  "serviceTime": 1,
  "instanceName": "测试实例"
}
```

**PriceType Enum**:
- `Usage`: Pay-as-you-go
- `Day`: Daily
- `Week`: Weekly
- `Month`: Monthly

#### GET /userapi/v1/instance/{instanceId}/status
Get instance status.

**Response**:
```json
{
  "instanceId": "instance-xxxxx",
  "statusCode": "RUNNING",
  "status": "运行中"
}
```

#### GET /userapi/v1/instance/status
Get all instances status.

**Response**:
```json
[
  {
    "instanceId": "instance-xxxxx",
    "statusCode": "RUNNING",
    "status": "运行中"
  }
]
```

#### POST /userapi/v1/instance/{instanceId}/start
Start an instance.

#### POST /userapi/v1/instance/{instanceId}/stop
Stop an instance.

#### POST /userapi/v1/instance/{instanceId}/release
Release an instance.

#### POST /userapi/v1/instance/{instanceId}/changeImage
Change instance image.

**Request Body**:
```json
{
  "imageId": "image_xxxx"
}
```

#### POST /userapi/v1/instance/page
Query instances with pagination.

**Request Body**:
```json
{
  "currentPage": 1,
  "pageSize": 10,
  "keyWord": "test",
  "status": "RUNNING"
}
```

**Response**:
```json
{
  "total": 1,
  "pageSize": 10,
  "currentPage": 1,
  "pages": 1,
  "empty": false,
  "notEmpty": true,
  "records": [
    {
      "instanceId": "instance-xxxxx",
      "instanceName": "test",
      "regionCode": "xx",
      "region": "杭州 xxx",
      "statusCode": "RUNNING",
      "status": "运行中",
      "imageId": "image_xxxxxx",
      "imageName": "Tensorflow 版本:xxx Python 版本:xxx(ubuntu xxxx) Cuda 版本:xxx",
      "gpuType": "xxxxxx",
      "gpuName": "RTX 4090",
      "gpus": 1,
      "cpuCode": "xxxx",
      "cpuName": "Intel Xeon E5-2680 v2",
      "cpus": 14.0,
      "memory": 15032385536,
      "createTime": 1741254108397,
      "sysDiskSize": 10737418240,
      "sysDiskUsedSize": 41410560,
      "sysDiskSizeFree": 10737418240,
      "sysDiskSizePaid": 0,
      "dataDiskSize": 10737418240,
      "dataDiskUsedSize": 0,
      "dataDiskSizeFree": 10737418240,
      "dataDiskSizePaid": 0,
      "gpuMemory": 12079595520,
      "consumeTypeCode": "Prepaid",
      "consumeType": "预付费",
      "expireTime": 1742463708398,
      "stopTime": 1741858908398,
      "toBeExpiredCode": 0,
      "toBeExpired": "否",
      "expiredCode": 0,
      "expired": "否",
      "toBeReleasedCode": 0,
      "toBeReleased": "否"
    }
  ]
}
```

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 10001 | 请求参数错误 | Request parameter error |
| 50001 | 余额不足 | Insufficient balance |
| 51001 | 资源不足 | Insufficient resources |
| 51002 | GPU不足 | Insufficient GPU |
| 52001 | 余额不足1小时 | Insufficient balance for 1 hour |
| 52002 | 实例正在开机中 | Instance is starting |
| 52003 | 实例正在运行中 | Instance is running |
| 52004 | 实例正在关机中 | Instance is stopping |
| 52005 | 实例已关机 | Instance is stopped |
| 52006 | 实例正在释放中 | Instance is releasing |
| 52007 | 实例需要关机 | Instance needs to be stopped |
| 52008 | 实例已到期 | Instance has expired |
| 52009 | 未到期包年包月实例暂不支持释放 | Prepaid instance not expired cannot be released |

## Default Resource Limits

- **System Disk**: 30GB (free)
- **Data Disk**: 50GB (free)
- **Expandable**: Both system and data disks can be expanded

## Instance Status Codes

| Status Code | Status | Description |
|-------------|---------|-------------|
| CREATING | 创建中 | Creating |
| RUNNING | 运行中 | Running |
| CLOSED | 已关机 | Stopped |
| STOPPING | 关机中 | Stopping |
| STARTING | 开机中 | Starting |
| RELEASING | 释放中 | Releasing |
| RELEASED | 已释放 | Released |
| ERROR | 错误 | Error |

## Pricing Types

| Type | Code | Description |
|------|------|-------------|
| Pay-as-you-go | Usage | Pay by usage |
| Daily | Day | Pay per day |
| Weekly | Week | Pay per week |
| Monthly | Month | Pay per month |

## Quick Reference Examples

### Create Instance
```bash
curl -X POST https://api.cfgpu.com/userapi/v1/instance/create \
  -H "Authorization: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "priceType": "Day",
    "regionCode": "hz",
    "gpuType": "qnid2x6c",
    "gpuNum": 1,
    "imageId": "image_exc6f72b",
    "serviceTime": 1,
    "instanceName": "My-GPU-Instance"
  }'
```

### Check Instance Status
```bash
curl -H "Authorization: YOUR_API_TOKEN" \
  https://api.cfgpu.com/userapi/v1/instance/instance-xxxxx/status
```

### List All Running Instances
```bash
curl -X POST https://api.cfgpu.com/userapi/v1/instance/page \
  -H "Authorization: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "RUNNING",
    "pageSize": 50
  }'
```

## Best Practices

### 1. Error Handling
Always check the `success` field in response:
```bash
response=$(curl -s ...)
success=$(echo "$response" | jq -r '.success')
if [ "$success" = "true" ]; then
    # Process success
else
    error_code=$(echo "$response" | jq -r '.errorCode')
    error_msg=$(echo "$response" | jq -r '.errorMsg')
    echo "Error $error_code: $error_msg"
fi
```

### 2. Resource Cleanup
Always release instances when not in use:
```bash
# Stop instance first
curl -X POST https://api.cfgpu.com/userapi/v1/instance/$INSTANCE_ID/stop

# Then release
curl -X POST https://api.cfgpu.com/userapi/v1/instance/$INSTANCE_ID/release
```

### 3. Cost Monitoring
Monitor instance status regularly to avoid unexpected charges:
```bash
# Check all instances daily
instances=$(curl -s -H "Authorization: $CFGPU_API_TOKEN" \
  https://api.cfgpu.com/userapi/v1/instance/status)

running_count=$(echo "$instances" | jq '[.[] | select(.statusCode == "RUNNING")] | length')
echo "Currently running instances: $running_count"
```

### 4. Instance Naming
Use descriptive names for easier management:
```bash
# Good naming convention
instance_name="AI-Training-$(date +%Y%m%d)-RTX4090"
```

## Security Notes

1. **API Token Security**
   - Store tokens in environment variables, not in scripts
   - Use token files with restricted permissions (chmod 600)
   - Rotate tokens regularly

2. **Instance Security**
   - Use secure images from trusted sources
   - Regularly update instance software
   - Monitor access logs

3. **Data Security**
   - Encrypt sensitive data on data disks
   - Regular backups
   - Clean up sensitive data before releasing instances