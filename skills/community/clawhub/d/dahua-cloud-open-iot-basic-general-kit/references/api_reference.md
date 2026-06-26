# 设备基础服务API接口参考文档

## API调用基础信息

### 接入地址
- 中国数据中心: `https://open.cloud-dahua.com`

### 请求方式
- 所有API接口使用POST方法
- Content-Type: `application/json`

### 请求头参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Content-Type | String | 是 | application/json |
| Accept-Language | String | 是 | 国际化语言类型，如：zh-CN |
| Version | String | 是 | 协议版本号，如：v1 |
| AccessKey | String | 是 | 产品对应的AccessKey |
| AppAccessToken | String | 否 | 授权API非必填；业务API必填 |
| UserAccessToken | String | 否 | 业务应用开放相关API选填 |
| Timestamp | Long | 是 | 13位标准时间戳，请求时间与服务端相差不能超过5分钟 |
| Nonce | String | 是 | 随机数，用于安全验证 |
| Sign | String | 是 | 采用指定签名算法计算出的签名 |
| X-TraceId-Header | String | 是 | 链路跟踪ID，如UUID生成随机字符串 |
| ProductID | Integer | 是 | 产品ID |
| Sign-Type | String | 否 | 值为simple表示使用简化签名模式 |

### 简化签名模式

#### 授权API签名算法
```
strAuthFactor = AccessKey + Timestamp + Nonce;
sign = HMAC-SHA512(strAuthFactor, secretAccessKey).toUpperCase();
```

#### 业务API签名算法
```
strAuthFactor = AccessKey + AppAccessToken + Timestamp + Nonce;
sign = HMAC-SHA512(strAuthFactor, secretAccessKey).toUpperCase();
```

## 鉴权认证

### 获取AppAccessToken

**接口说明**: 开发者可以通过调用当前接口来获取AppAccessToken，只有经过AppAccessToken身份验证后才能调用常用API。

**URL**: `/open-api/api-base/auth/getAppAccessToken`

**请求参数**: 无请求体，通过请求头传递参数

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.appAccessToken | string | 是 | 鉴权令牌 |
| data.validitySeconds | string | 是 | 令牌的有效时间（单位：秒） |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
请求头:
{
  "AccessKey": "1680145896563675136",
  "Timestamp": "1689838378183",
  "Nonce": "lgfm8vnhu3qxu3csv8d0fuuj7elsftq0",
  "Sign": "85119125974213185EB25E1198350B8EDDF74A54EA08E092E472675E36FB353B953257F62A71A9EA8058C6882BDFBB80466CF770D3EC3E734A2C0BC817BB4E49",
  "Version": "v1",
  "X-TraceId-Header": "6tefz7oa3uvncpb2edui5svs29zia538",
  "ProductId": "856047897"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {
    "appAccessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "validitySeconds": 604800
  },
  "msg": "Operation is successful."
}
```

## 设备管理

### 添加设备

**接口说明**: 在添加设备之前，需要初始化设备并设置设备的密码。

**设备密码加密方式**:

**方式一：Base64加密**
```
格式："Dolynk_" + "Base64(设备web密码)"
例如：若设备密码为 admin123
Base64(admin123) = YWRtaW4xMjM=
加密后字符串为 = Dolynk_YWRtaW4xMjM=
```

**方式二：AES256加密**
```
格式：Base64(Aes256(待加密内容, AesKey, IV初始向量))
加密算法：Aes256/CBC/PKCS7
初始化向量IV：86E2DB6D77B5E9CD
AesKey：Cut32(UpperCase(MD5-32位(UpperCase(sk))))
```

**URL**: `/open-api/api-iot/device/addDevice`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| devCode | string | 是 | 设备密码（加密后） |
| categoryCode | string | 否 | 设备品类 |
| devAccount | string | 否 | 目前支持admin或非admin添加 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceId": "8E0******7D",
  "categoryCode": "IPC",
  "devCode": "1H14BbU*******9b+MJQ=="
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": null,
  "msg": "Operation is successful."
}
```

### 添加国标设备

**接口说明**: 国标设备接入说明

**URL**: `/open-api/api-iot/device/addGbDevice`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| devCode | string | 是 | 注册密码（AES256加密） |
| gbCode | string | 是 | 国标码 |
| manufacturer | string | 否 | 厂商：Dahua、HIKVSION、UNKNOW |
| channelNumber | integer | 是 | 通道总数 |
| gbStreamModel | string | 否 | 拉流协议：TCP或UDP，默认UDP |
| deviceClass | string | 否 | 设备类型：NVR（默认）、IPC |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.deviceId | string | 是 | 设备序列号 |
| data.manufacturer | string | 是 | 厂商 |
| data.state | string | 是 | 设备状态 |
| data.deviceNo | string | 是 | 设备编号 |
| data.protocolType | string | 是 | 协议类型 |
| data.name | string | 是 | 设备名称 |
| data.deviceClass | string | 是 | 设备类型 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "devCode": "7FXsUuW2uvyJONMreznmTA==",
  "gbCode": "00043363807410000003",
  "manufacturer": "Dahua",
  "channelNumber": 10,
  "gbStreamModel": "TCP",
  "deviceClass": "IPC"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {
    "deviceId": "QO1Y7OAGMDL5V6RSUUXDXDTV0001",
    "manufacturer": "Dahua",
    "state": "offline",
    "deviceNo": "00043363807410000003",
    "protocolType": "GB28181",
    "name": "",
    "deviceClass": "IPC"
  },
  "msg": "Operation is successful."
}
```

### 获取国标码列表

**接口说明**: 该接口用于获取指定数量的国标码。

**URL**: `/open-api/api-iot/device/listGbCode`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| count | number | 是 | 单次查询数量（最大10000，最小1） |
| prefix | number | 否 | 自定义国标码前缀（长度必须13位） |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.maxGbCode | string | 是 | 最大国标编码 |
| data.minGbCode | string | 是 | 最小国标编码 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "count": 5,
  "prefix": "00161****0395"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {
    "minGbCode": "00057981****0000039",
    "maxGbCode": "00057981****0000044"
  },
  "msg": "操作成功"
}
```

### 获取国标设备注册信息

**接口说明**: 该接口用于获取Sip服务器IP和端口号。

**URL**: `/open-api/api-iot/device/getSipInfo`

**请求参数**: 无请求体

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.sipServerIp | string | 是 | Sip服务器Ip和端口 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {
    "sipServerIp": "121.41.9.73:5060"
  },
  "msg": "操作成功"
}
```

### 删除设备

**接口说明**: 删除已添加的设备。

**URL**: `/open-api/api-iot/device/deleteDevice`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceId": "8D******C0"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": null,
  "msg": "Operation is successful."
}
```

## SD卡管理

### 格式化设备SD卡

**接口说明**: 设备需要有LocalStorage能力集。

**URL**: `/open-api/api-aiot/device/formatSDCard`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| index | number | 否 | SD卡编号（单卡设备无需传；多卡设备不传默认格式化第一张） |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| msg | string | 是 | 响应消息 |
| success | boolean | 是 | 响应状态 |
| code | string | 是 | 响应状态码 |
| data | object | 是 | 响应数据 |
| data.result | string | 是 | 设备响应结果：start-recover、no-sdcard、in-recover、sdcard-error、formated |

**请求示例**:
```json
{
  "deviceId": "8H0C6F5YAG05880",
  "index": 1
}
```

**响应示例**:
```json
{
  "msg": "操作成功。",
  "success": true,
  "code": "200",
  "data": {
    "result": "start-recover"
  }
}
```

### 获取设备SD卡状态

**接口说明**: 设备需要有LocalStorage能力集。

**URL**: `/open-api/api-aiot/device/getSDCardStatus`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| index | number | 否 | SD卡编号（单卡设备无需传；多卡设备不传默认查询第一张） |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| msg | string | 是 | 响应消息 |
| success | boolean | 是 | 响应状态 |
| code | string | 是 | 响应状态码 |
| data | object | 是 | 响应数据 |
| data.status | string | 是 | 存储卡状态：empty、normal、abnormal、recovering、needinit等 |

**请求示例**:
```json
{
  "deviceId": "8HXXXXXXXX80",
  "index": 1
}
```

**响应示例**:
```json
{
  "msg": "操作成功。",
  "success": true,
  "code": "200",
  "data": {
    "status": "normal"
  }
}
```

### 查询设备SD卡容量

**接口说明**: 设备需要有LocalStorage能力集。

**URL**: `/open-api/api-aiot/device/getSDCardStorage`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| index | string | 否 | SD卡编号（单卡设备无需传；多卡设备不传默认查询第一张） |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| msg | string | 是 | 响应消息 |
| success | boolean | 是 | 响应状态 |
| code | string | 是 | 响应状态码 |
| data | object | 是 | 响应数据 |
| data.totalBytes | number | 是 | 总容量（单位：Byte） |
| data.usedBytes | number | 是 | 已使用容量（单位：Byte） |

**请求示例**:
```json
{
  "deviceId": "8HXXXXXXXXX880",
  "index": "1"
}
```

**响应示例**:
```json
{
  "msg": "操作成功。",
  "success": true,
  "code": "200",
  "data": {
    "totalBytes": 7816249344,
    "usedBytes": 6856704000
  }
}
```

### 获取设备SD卡列表

**接口说明**: 设备需要有MultipleLocalStorage能力集。

**URL**: `/open-api/api-aiot/device/listSDCardStorage`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| msg | string | 是 | 响应消息 |
| success | boolean | 是 | 响应状态 |
| code | string | 是 | 响应状态码 |
| data | object | 是 | 响应数据 |
| data.storageList | object[] | 是 | SD卡的信息列表 |
| data.storageList[].name | string | 是 | SD卡名称 |
| data.storageList[].index | string | 是 | SD卡编号（从1开始） |

**请求示例**:
```json
{
  "deviceId": "8HXXXXXXX80"
}
```

**响应示例**:
```json
{
  "msg": "success。",
  "success": true,
  "code": "200",
  "data": {
    "storageList": [
      {
        "index": "1",
        "name": "/dev/mmc0"
      },
      {
        "index": "2",
        "name": "/dev/mmc1"
      }
    ]
  }
}
```

## 设备查询

### 查询设备品类

**接口说明**: 区分设备类别以获得不同类别支持的不同设备类型。

**URL**: `/open-api/api-iot/device/getCategory`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| secondCategoryCode | string | 否 | 2级设备类别代码 |
| primaryCategoryCode | string | 否 | 1级设备类别代码 |
| deviceModel | string | 否 | 设备型号（仅支持每次传一个） |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.categoryList | object[] | 否 | 类别列表 |
| data.categoryList[].primaryCategoryName | string | 是 | 1级设备品类名称 |
| data.categoryList[].primaryCategoryCode | string | 是 | 1级设备品类编号 |
| data.categoryList[].secondCategoryName | string | 是 | 2级设备品类名称 |
| data.categoryList[].secondCategoryCode | string | 是 | 2级设备品类编码 |
| data.categoryList[].deviceModel | string[] | 否 | 设备型号列表 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "secondCategoryCode": "IPC"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {
    "categoryList": [
      {
        "primaryCategoryCode": "Camera",
        "primaryCategoryName": "视频通用",
        "secondCategoryName": "双目IPC",
        "secondCategoryCode": "BinocularIPC",
        "deviceModel": [
          "DH-H6B-E2"
        ]
      }
    ]
  },
  "msg": "Operation is successful."
}
```

### 查询设备绑定状态

**接口说明**: 查询单个设备是否绑定到某个帐户。

**URL**: `/open-api/api-iot/device/checkDeviceBindInfo`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.bindStatus | string | 是 | 绑定状态 |
| data.deviceExist | string | 是 | 平台上是否存在设备 |
| data.status | string | 是 | 设备在线状态 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceId": "<设备序列号>"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {
    "bindStatus": "bind",
    "deviceExist": null,
    "status": null
  },
  "msg": "Operation is successful."
}
```

### 获取设备在线状态

**接口说明**: 获取设备的在离线状态。

**URL**: `/open-api/api-iot/device/deviceOnline`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.deviceId | string | 否 | 设备序列号 |
| data.onLine | string | 否 | 1：设备在线，0：设备离线 |
| data.channels | object[] | 否 | 通道列表 |
| data.channels[].channelId | string | 否 | 设备通道号 |
| data.channels[].onLine | string | 否 | 通道在线状态 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceId": "<设备序列号>"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {
    "channels": [
      {
        "channelId": "0",
        "onLine": "1"
      }
    ],
    "deviceId": "<设备序列号>",
    "onLine": "1"
  },
  "msg": "Operation is successful."
}
```

### 获取设备通道信息

**接口说明**: 查询设备通道下挂载设备的序列号、设备大类、设备型号信息。

**URL**: `/open-api/api-aiot/device/getDeviceChannelInfo`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| msg | string | 是 | 响应消息 |
| success | boolean | 是 | 响应状态 |
| code | string | 是 | 响应状态码 |
| data | object | 是 | 响应数据 |
| data.channels | object[] | 是 | 通道列表 |
| data.channels[].channelId | string | 否 | 设备通道号 |
| data.channels[].deviceInfo | object | 否 | 通道设备信息 |
| data.channels[].deviceInfo.deviceClass | string | 否 | 通道设备大类 |
| data.channels[].deviceInfo.deviceType | string | 否 | 通道设备型号 |
| data.channels[].deviceInfo.deviceId | string | 否 | 通道下设备序列号 |

**请求示例**:
```json
{
  "deviceId": "AA03012XXXXXX"
}
```

**响应示例**:
```json
{
  "msg": "Operation is successful.",
  "success": true,
  "code": "200",
  "data": {
    "channels": [
      {
        "channelId": 0,
        "deviceInfo": {
          "deviceClass": "IPC",
          "deviceType": "DH-IPC-xxxxx",
          "deviceId": "9C063xxxx"
        }
      }
    ]
  }
}
```

### 批量查询设备详细信息

**接口说明**: 批量查询设备详细信息。

**URL**: `/open-api/api-iot/device/listDeviceDetailsByIds`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceList | object[] | 是 | 设备序列号列表（最大size=100） |
| deviceList[].deviceId | string | 是 | 设备序列号 |
| deviceList[].channelId | string[] | 否 | 通道列表（最大size=100） |

**响应参数**: 复杂的嵌套结构，包含设备详细信息、通道信息等。

**请求示例**:
```json
{
  "deviceList": [
    {
      "deviceId": "<设备序列号>",
      "channelId": ["0"]
    }
  ]
}
```

### 查询设备列表

**接口说明**: 查询设备和设备下通道的信息。

**URL**: `/open-api/api-iot/device/getDeviceList`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| pageNum | number | 是 | 页码（最小为1） |
| pageSize | string | 是 | 每页条数（最小为1，最大100） |
| deviceId | string | 否 | 设备序列号（支持模糊查询） |
| primaryCategoryCodeList | string[] | 否 | 设备品类列表 |

**响应参数**: 复杂的嵌套结构，包含分页信息和设备列表。

**请求示例**:
```json
{
  "pageSize": "1",
  "pageNum": "10"
}
```

### 国标设备查询详细信息

**接口说明**: 该接口用于批量查询国标设备的详细信息。

**URL**: `/open-api/api-iot/device/deviceInfoDetailAll`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceIds | string[] | 是 | 设备序列号列表 |

**响应参数**: 复杂的嵌套结构，包含设备详细信息和通道信息。

**请求示例**:
```json
{
  "deviceIds": ["QO1Y7OAGMDL5V6RSUUXDXDTV0001"]
}
```

## 设备配置

### 基础配置

#### 修改国标设备信息

**接口说明**: 该接口用于修改国标设备信息。

**URL**: `/open-api/api-iot/device/modifyGbDevice`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| devCode | string | 否 | 设备密码（AES256加密） |
| gbStreamModel | string | 否 | 国标设备拉流协议：TCP或UDP |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| msg | string | 是 | 响应消息 |
| data | object | 是 | 响应数据 |

**请求示例**:
```json
{
  "deviceId": "QO1Y7OAGMDL5V6RSUUXDXDTV0001",
  "devCode": "7FXsUuW2uvyJONMreznmTA=="
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {},
  "msg": "Operation is successful."
}
```

#### 验证设备密码

**接口说明**: 适用于需要验证密码的场景。

**URL**: `/open-api/api-iot/device/verifyDevCode`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| devCode | string | 是 | 设备密码（AES-256加密） |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceId": "<设备序列号>",
  "devCode": "xxxx"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {},
  "msg": "Operation is successful."
}
```

#### 修改设备或通道名称

**接口说明**: 更改设备或通道名称并将其直接下发到设备。

**URL**: `/open-api/api-iot/device/modifyDeviceName`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| channelId | string | 否 | 设备通道号 |
| name | string | 是 | 设备或者通道名称 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 否 | 响应数据 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceId": "<设备序列号>",
  "name": "developerTest01"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {},
  "msg": "Operation is successful."
}
```

#### 修改设备密码

**接口说明**: 修改设备密码。

**URL**: `/open-api/api-iot/device/modifyDevCode`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| oldDevCode | string | 是 | 设备老密码（AES-256加密） |
| newDevCode | string | 是 | 设备新密码（AES-256加密） |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceId": "<设备序列号>",
  "oldDevCode": "1H14BbU+W7AD5vm09b+MJQ==",
  "newDevCode": "1H14BbU+W7AD5vm09b+MJQ=="
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {},
  "msg": "Operation is successful."
}
```

### 设备使能

#### 获取设备使能开关状态

**接口说明**: 获取设备使能开关状态。

**URL**: `/open-api/api-iot/device/getAbilityStatus`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| abilityType | string | 是 | 设备使能类型 |
| channelId | string | 否 | 通道号（设备级使能无需传；通道级使能需要传） |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.status | string | 是 | 开关状态：on、off |
| data.abilityType | string | 是 | 启用的设备功能的类型 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceId": "<设备序列号>",
  "abilityType": "localRecord",
  "channelId": "0"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {
    "abilityType": "localRecord",
    "status": "off"
  },
  "msg": "Operation is successful."
}
```

#### 设置设备使能开关

**接口说明**: 远程配置使能开关的状态以启用或禁用设备功能。

**URL**: `/open-api/api-iot/device/setAbilityStatus`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| abilityType | string | 是 | 要启用的能力的类型 |
| status | string | 是 | 生效与否：on：已启用，off：禁用 |
| channelId | string | 否 | 通道号（设备级使能无需传；通道级使能需要传） |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceId": "<设备序列号>",
  "abilityType": "localRecord",
  "status": "on",
  "channelId": "1"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {},
  "msg": "Operation is successful."
}
```

### 设备时间配置

#### 设备校时

**接口说明**: 用于修改设备时间。

**URL**: `/open-api/api-aiot/device/setCurrentUTC`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| tolerance | number | 是 | 容差（单位：秒） |
| utc | number | 是 | UTC时间戳（不带时区夏令时偏差0时区时间戳截止到秒） |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 返回错误码 |
| success | boolean | 是 | 是否成功 |
| msg | string | 是 | 返回消息 |
| data | object | 是 | 响应数据 |

**请求示例**:
```json
{
  "deviceId": "AB0233BPAJXXXX",
  "tolerance": 5,
  "utc": 1718696202
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "msg": "操作成功。",
  "data": {}
}
```

### 铃音配置

#### 新增自定义铃声

**接口说明**: 设备需要有CustomRing的能力集。

**URL**: `/open-api/api-aiot/device/addCustomRing`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| channelId | string | 否 | 通道序列号 |
| name | string | 是 | 铃声名称（长度不超过32） |
| type | string | 是 | 铃声文件格式类型：wav、pcm、aac |
| url | string | 是 | 铃声文件地址（长度不超过512） |
| relateType | string | 否 | 铃声关联类型：device、reply、local、quickReply、chime |
| language | string | 否 | 文件语言：English、Russian、Turkey等 |
| version | string | 否 | 文件版本 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| msg | string | 是 | 响应消息 |
| success | boolean | 是 | 响应状态 |
| code | string | 是 | 响应状态码 |
| data | object | 是 | 响应数据 |

**请求示例**:
```json
{
  "name": "q666677778888",
  "channelId": "1",
  "relateType": "device",
  "type": "aac",
  "deviceId": "AEXXXXXXXX193",
  "url": "http://s3.ap-southeast-...",
  "language": "English",
  "version": "V1.000.0000000.0.R.240521"
}
```

**响应示例**:
```json
{
  "code": "200",
  "msg": "success",
  "success": true,
  "data": {}
}
```

#### 删除自定义铃声

**接口说明**: 能力集：CustomRing。

**URL**: `/open-api/api-aiot/device/deleteCustomRing`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| index | string | 是 | 铃声序列号 |
| relateType | string | 是 | 铃声关联类型：device、reply、local、quickReply、chime |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态码 |
| success | boolean | 是 | 响应状态 |
| msg | string | 是 | 响应消息 |
| data | object | 是 | 响应数据 |

**请求示例**:
```json
{
  "deviceId": "AE0XXXXXXX193",
  "index": "3",
  "relateType": "device"
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "msg": "success",
  "data": {}
}
```

#### 获取铃声列表

**接口说明**: 设备需要有CustomRing能力集。

**URL**: `/open-api/api-aiot/device/listCustomRing`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| relateType | string | 是 | 铃声关联类型：device、reply、local、quickReply、chime |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态码 |
| msg | string | 是 | 响应消息 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.list | object[] | 是 | 铃声列表 |
| data.list[].name | string | 是 | 铃声名称 |
| data.list[].index | number | 是 | 铃声序列号 |
| data.list[].ringMode | string | 是 | 铃声模式：default、custom |
| data.list[].state | string | 是 | 铃声状态：play、download |
| data.list[].type | string | 是 | 铃声类型：wav、pcm、aac |
| data.ringIndex | number | 是 | 用户配置的铃声索引 |

**请求示例**:
```json
{
  "deviceId": "AEXXXXXXXX193",
  "relateType": "device"
}
```

**响应示例**:
```json
{
  "code": "200",
  "msg": "success",
  "success": true,
  "data": {
    "list": [
      {
        "index": "0",
        "name": "You are under surveillance",
        "ringMode": "default",
        "state": "play",
        "type": "wav"
      }
    ],
    "ringIndex": 1
  }
}
```

#### 设置铃声

**接口说明**: 设备需要有CustomRing能力集。

**URL**: `/open-api/api-aiot/device/setCustomRing`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| channelId | string | 否 | 通道序列号 |
| index | string | 是 | 铃声序列号 |
| relateType | string | 是 | 铃声关联类型：device、reply、local、quickReply、chime |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态码 |
| msg | string | 是 | 响应消息 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |

**请求示例**:
```json
{
  "deviceId": "AEXXXXXXX193",
  "channelId": "1",
  "index": "4",
  "relateType": "device"
}
```

**响应示例**:
```json
{
  "code": "200",
  "msg": "success",
  "success": true,
  "data": {}
}
```

### 网络配置

#### 获取设备周边热点信息

**接口说明**: 要求设备具有WIFI能力集。

**URL**: `/open-api/api-aiot/device/wifiAround`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| msg | string | 是 | 响应信息 |
| success | boolean | 是 | 响应状态 |
| code | string | 是 | 响应状态码 |
| data | object | 是 | 响应数据 |
| data.wLan | object[] | 是 | 热点信息集合 |
| data.wLan[].linkStatus | number | 是 | 连接状态：0未连接、1连接中、2已连接 |
| data.wLan[].intensity | number | 是 | 信号强度（1~5） |
| data.wLan[].auth | string | 是 | 认证模式：OPEN、WEP、WPA/WPA2、WPA/WPA2 PSK |
| data.wLan[].bssid | string | 是 | BSSID（MAC地址） |
| data.wLan[].ssid | string | 是 | 热点ID |
| data.enable | boolean | 是 | 是否开启了wifi |

**请求示例**:
```json
{
  "deviceId": "abc123"
}
```

#### 获取设备当前连接的热点信息

**接口说明**: 要求设备具有WIFI能力集。

**URL**: `/open-api/api-aiot/device/currentDeviceWifi`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| msg | string | 是 | 响应信息 |
| success | boolean | 是 | 响应状态 |
| code | string | 是 | 响应状态码 |
| data | object | 是 | 响应数据 |
| data.intensity | string | 是 | 信号强度（1~5） |
| data.ssid | string | 是 | 当前连接的热点名称 |
| data.linkEnable | boolean | 是 | 是否连接了wifi |

**请求示例**:
```json
{
  "deviceId": "abc123"
}
```

#### 修改设备连接热点

**接口说明**: 要求设备具有WIFI能力集。

**URL**: `/open-api/api-aiot/device/controlDeviceWifi`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| ssid | string | 是 | 需要连接的SSID |
| bssid | string | 否 | 需要连接的BSSID |
| password | string | 否 | wifi密码（base64加密） |
| linkEnable | boolean | 否 | 连接或断开：true连接，false断开 |
| channelSn | string | 否 | 配件序列号 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| msg | string | 是 | 响应信息 |
| code | string | 是 | 响应状态码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |

**请求示例**:
```json
{
  "deviceId": "123456",
  "password": "123456",
  "ssid": "123456",
  "bssid": "12:34:56:78:90:12",
  "password": "qFgssFdfRuDFweHasdfDFJ03xfv2POjblccUYOmX8=",
  "linkEnable": true
}
```

#### 查询单SIM卡设备的SIM、IMEI信息

**接口说明**: 需要设备具有 SMSCSS 或 SSIM 能力集。

**URL**: （未提供）

#### 获取sim信号强度

**接口说明**: 需要设备具有 SMSCSS 或 SSIM 能力集。

**URL**: `/open-api/api-aiot/device/getSimSignalStrength`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| msg | string | 是 | 响应消息 |
| success | boolean | 是 | 响应状态 |
| code | string | 是 | 响应状态码 |
| data | object | 是 | 响应数据 |
| data.intensity | number | 是 | 信号强度（单位：dbm） |
| data.sigStrength | string | 是 | 信号强度等级：0-5（5最强） |

**请求示例**:
```json
{
  "deviceId": "abc123"
}
```

**响应示例**:
```json
{
  "msg": "操作成功。",
  "success": true,
  "code": "200",
  "data": {
    "intensity": 94,
    "sigStrength": "5"
  }
}
```

## 消息订阅

### 图片解密

**接口说明**: 解密加密的报警信息缩略图。

**URL**: `/open-api/api-decrypto/image/decrypto`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |
| imageUrl | string | 是 | 需要解密的加密图像地址（有效期一天） |
| devCode | string | 否 | 设备密码（AES256加密，密钥使用SK） |
| isTcmDevice | boolean | 否 | 设备能力集包含TCM或ESB5时需要密码校验 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.url | string | 否 | 图像URL（有效期一天） |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceId": "AC02295PHA00343",
  "imageUrl": "https://lc-jn-hs-online-paas-private-picture...",
  "isTcmDevice": false
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": {
    "url": "http://test-developer-bkt-oss-bucket..."
  },
  "msg": "Operation is successful."
}
```

### 按照设备订阅消息

#### 分页获取回调配置ID和回调配置地址

**接口说明**: 分页获取回调配置ID和回调配置地址。

**URL**: `/open-api/api-message/getAllCallbackConfigId`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 默认值 | 描述 |
|---------|---------|---------|--------|------|
| pageSize | number | 否 | 20 | 每页记录数 |
| pageNum | number | 否 | 1 | 页码 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.currentPage | number | 是 | 当前页 |
| data.totalPage | number | 是 | 总页数 |
| data.pageSize | number | 是 | 每页数量 |
| data.totalRows | number | 是 | 总数量 |
| data.pageData | object[] | 是 | 当前页数据 |
| data.pageData[].callbackConfigId | number | 否 | 回调配置ID |
| data.pageData[].callbackUrl | string | 否 | 回调配置地址 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "pageSize": 10,
  "pageNum": 1
}
```

#### 根据设备ID查询消息订阅信息

**接口说明**: 根据设备ID查询消息订阅信息。

**URL**: `/open-api/api-message/getMessageSubscribeInfoByDeviceId`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceId | string | 是 | 设备序列号 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object[] | 是 | 响应数据 |
| data[].callbackUrl | string | 否 | 回调配置地址 |
| data[].isPush | boolean | 否 | 是否开启推送：false关闭，true开启 |
| data[].messageTypeCodes | string[] | 否 | 消息类型列表 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceId": "8E034DAPAJ00XXX"
}
```

#### 按设备ID列表订阅消息

**接口说明**: 相同类型消息的第二个配置不会覆盖原始配置。列表中的设备必须属于同一产品且为相同品类编码。

**URL**: `/open-api/api-message/messageSubscribeByDeviceIds`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| deviceIds | string[] | 是 | 设备序列号列表（最大数量为50） |
| messageTypeCodes | string[] | 是 | 消息类型 |
| categoryCode | string | 是 | 设备品类编码 |
| callbackConfigId | number | 是 | 回调配置ID |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "deviceIds": ["AF741****S41001"],
  "messageTypeCodes": ["TiltAlarm", "online"],
  "callbackConfigId": 1781218942140944393,
  "categoryCode": "ARC"
}
```

#### 按回调配置ID更新回调配置

**接口说明**: 更新回调配置。

**URL**: `/open-api/api-message/updateByCallbackConfigId`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| callbackConfigId | number | 是 | 回调配置ID |
| callbackUrl | string | 否 | 回调地址URL |
| isPush | boolean | 否 | 是否开启消息推送：false关闭，true开启 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "callbackConfigId": 1781218942140944393,
  "callbackUrl": "https://open.cloud-dahua.com/message/api-message/test/get",
  "isPush": true
}
```

#### 按回调配置ID搜索回调配置信息

**接口说明**: 获取回调配置信息。

**URL**: `/open-api/api-message/getInfoByCallbackConfigId`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| callbackConfigId | number | 是 | 回调配置ID |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.isPush | boolean | 否 | 是否开启消息推送 |
| data.callbackUrl | string | 否 | 回调配置地址URL |
| data.callbackConfigId | number | 否 | 回调配置ID |
| data.productId | string | 否 | 产品ID |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "callbackConfigId": 1881891823266938880
}
```

#### 添加回调配置信息

**接口说明**: 添加回调配置信息。

**URL**: `/open-api/api-message/addCallbackConfig`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 默认值 | 描述 |
|---------|---------|---------|--------|------|
| callbackUrl | string | 是 | | 回调配置地址URL |
| isPush | boolean | 否 | true | 是否开启消息推送：false关闭，true开启 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | number | 是 | 回调配置ID |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "callbackUrl": "https://open.cloud-dahua.com/message/api-message/test/get",
  "isPush": true
}
```

**响应示例**:
```json
{
  "code": "200",
  "success": true,
  "data": 39875492375432451,
  "msg": "Operation is successful."
}
```

#### 按设备品类获取可订阅的消息类型

**接口说明**: 按设备品类获取支持的消息类型。

**URL**: `/open-api/api-message/getMessageTypePage`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 默认值 | 描述 |
|---------|---------|---------|--------|------|
| categoryCode | string | 是 | | 设备品类编码 |
| pageSize | number | 否 | 10 | 每页记录数（范围10-50） |
| pageNum | number | 否 | 1 | 页码 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| data.totalPage | number | 是 | 总页数 |
| data.pageSize | number | 是 | 每页记录数 |
| data.pageData | object[] | 是 | 当前页数据 |
| data.pageData[].code | string | 否 | 消息类型编码 |
| data.pageData[].createTime | string | 否 | 创建时间 |
| data.pageData[].memo | string | 否 | 消息说明 |
| data.pageData[].type | string | 否 | 消息类型 |
| data.totalRows | number | 是 | 总数量 |
| data.currentPage | number | 是 | 当前页码 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "categoryCode": "IPC",
  "pageNum": 1,
  "pageSize": 10
}
```

#### 根据回调配置ID更新设备订阅消息

**接口说明**: 根据CallbackConfigId和DeviceId修改订阅的MessageTypeCode。

**URL**: `/open-api/api-message/updateSubscribeByCallbackConfigId`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| callbackConfigId | number | 是 | 回调配置ID |
| deviceId | string | 是 | 设备序列号 |
| messageTypeCodes | string[] | 否 | 消息类型列表 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "callbackConfigId": 1781218942140944390,
  "deviceId": "B874AC****Q1002",
  "messageTypeCodes": ["online"]
}
```

#### 删除回调配置及相关订阅消息

**接口说明**: 根据CallbackConfigId删除消息时，删除与CallbackConfigId相关的设备的所有订阅消息。

**URL**: `/open-api/api-message/deleteCallbackId`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| callbackConfigIds | number[] | 是 | 回调配置ID列表 |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object | 是 | 响应数据 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "callbackConfigIds": ["1781218942140944390"]
}
```

#### 根据回调配置ID搜索已订阅的设备消息

**接口说明**: 根据回调配置ID搜索已订阅的设备消息。

**URL**: `/open-api/api-message/getSubscribeInfoByCallbackConfigId`

**请求参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| callbackConfigId | number | 是 | 回调配置ID |

**响应参数**:

| 参数名称 | 参数类型 | 是否必需 | 描述 |
|---------|---------|---------|------|
| code | string | 是 | 响应状态代码 |
| success | boolean | 是 | 响应状态 |
| data | object[] | 是 | 响应数据 |
| data[].deviceId | string | 否 | 设备序列号 |
| data[].messageTypeCodes | string[] | 否 | 消息类型列表 |
| msg | string | 是 | 响应消息 |

**请求示例**:
```json
{
  "callbackConfigId": 1781218942140944390
}
```

## 通道类型枚举

| unitType | 描述 |
|----------|------|
| 1 | 通用视频通道 |
| 2 | 解码单元 |
| 3 | 报警输入通道 |
| 4 | 报警输出通道 |
| 5 | 大屏输入单元 |
| 6 | 大屏输出单元 |
| 7 | 门禁单元 |
| 8 | 声卡单元 |
| 9 | 转码单元 |
| 12 | 消防通道 |
| 13 | 消防主机单元 |
| 14 | 道闸单元 |
| 15 | 动环外设单元 |
| 16 | 警号通道 |
| 17 | 融合通道 |
| 99 | 模拟通道 |

## 设备使能类型表

| abilityType | 应用级别 |
|-------------|----------|
| localRecord | channel |
| motionDetect | channel |
| faceCapture | channel |
| speechRecognition | device |
| breathingLight | device |
| smartLocate | all |
| smartTrack | all |
| localAlarmRecord | channel |
| regularCruise | all |
| headerDetect | channel |
| numberStat | channel |
| manNumDec | channel |
| alarmPIR | channel |
| autoZoomFocus | channel |
| audioEncodeControl | channel |
| aecv3 | channel |
| faceDetect | channel |
| localStorageEnable | device |
| whiteLight | all |
| linkageWhiteLight | channel |
| linkageSiren | all |
| infraredLight | device |
| searchLight | device |
| hoveringAlarm | channel |
| beOpenedDoor | device |
| closeCamera | channel |
| mobileDetect | channel |
| rtFaceDetect | channel |
| rtFaceCompa | channel |
| closeDormant | device |
| heatMap | channel |
| tlsEnable | device |
| aiHumanCar | channel |
| aiHuman | channel |
| aiCar | channel |
| openDoorByFace | device |
| openDoorByTouch | device |
| linkDevAlarm | channel |
| linkAccDevAlarm | device |
| abAlarmSound | channel |
| playSound | device |
| wideDynamic | channel |
| smdHuman | channel |
| smdVehicle | channel |
| instantDisAlarm | device |
| periodDisAlarm | device |
| ccss | channel |
| inll | channel |
| ledsw | device |
