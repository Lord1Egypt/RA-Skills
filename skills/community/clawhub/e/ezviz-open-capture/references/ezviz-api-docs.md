# 萤石开放平台 API 文档

本文档包含玩手机检测告警流程所需的**五个**核心 API 接口详细说明。

**完整工作流程**：
```
获取 Token → 设备抓图 → 玩手机检测 → 上传语音 → 下发语音
```

---

## 0. 获取 AccessToken 接口

**文档 URL**: https://open.ys7.com/help/81  
**更新时间**: 2025.02.21

### 接口说明

AccessToken 是访问令牌，接口调用必备的公共参数之一，用于校验接口访问/调用是否有权限。

**重要特性**：
- 有效期为 **7 天**，有效期内不需要重复申请，可以重复使用
- 有效期 7 天无法变更，请在业务端使用 AccessToken 的场景中，校验老 Token 的有效性和失效时重新获取 Token 的机制
- 新获取 Token 不会使老 Token 失效，每个 Token 独立拥有 7 天生命周期
- 由于 Token 属于用户身份认证令牌，在用户变更身份信息（用户注销、密码修改）后会将旧的 Token 进行失效处理

**最佳实践**：
> 获取到的 accessToken 有效期是 7 天，请在**即将过期**或者**接口报错 10002**时重新获取，**每个 token 具备独立的 7 天生命周期，请勿频繁调用避免占用过多接口调用次数**。最佳实践是在本地进行缓存，给对应有权限的用户使用，而不是在每次使用业务接口前获取一次。

### 请求地址

```
POST https://open.ys7.com/api/lapp/token/get
```

### 请求方式

POST (application/x-www-form-urlencoded)

### 请求参数

| 参数名 | 类型 | 描述 | 是否必选 |
|--------|------|------|----------|
| appKey | String | appKey（在官网 - 开发者服务 - 我的应用中获取） | Y |
| appSecret | String | appSecret | Y |

### HTTP 请求报文

```http
POST /api/lapp/token/get HTTP/1.1
Host: open.ys7.com
Content-Type: application/x-www-form-urlencoded

appKey=9mqitppidgce4y8n54ranvyqc9fjtsrl&appSecret=096e76501644989b63ba0016ec5776
```

### 返回数据

```json
{
  "data": {
    "accessToken": "at.7jrcjmna8qnqg8d3dgnzs87m4v2dme3l-32enpqgusd-1jvdfe4-uxo15ik0s",
    "expireTime": 1470810222045
  },
  "code": "200",
  "msg": "操作成功!"
}
```

### 返回字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| accessToken | String | 获取的 accessToken |
| expireTime | long | 具体过期时间，精确到毫秒 |

### 返回码

| 返回码 | 返回消息 | 描述 |
|--------|----------|------|
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10005 | appKey 异常 | appKey 被冻结 |
| 10017 | appKey 不存在 | 确认 appKey 是否正确 |
| 10030 | appkey 和 appSecret 不匹配 | - |
| 49999 | 数据异常 | 接口调用异常 |

---

## 1. 设备抓拍图片接口

**文档 URL**: https://open.ys7.com/help/687  
**更新时间**: 2025.11.25

### 接口功能

抓拍设备当前画面，**该接口仅适用于 IPC 或者关联 IPC 的 DVR 设备**，该接口并非预览时的截图功能。

**海康型号设备**可能不支持萤石协议抓拍功能，使用该接口可能返回不支持或者超时。

**该接口需要设备支持能力集**：`support_capture=1`

> ⚠️ **注意**：设备抓图能力有限，请勿频繁调用，建议每个摄像头调用的间隔**4s 以上**。

### 请求地址

```
POST https://open.ys7.com/api/lapp/device/capture
```

### 请求方式

POST (application/x-www-form-urlencoded)

### 子账户 token 请求所需最小权限

```
"Permission":"Capture"
"Resource":"Cam:序列号：通道号"
```

### 请求参数

| 参数名 | 类型 | 描述 | 是否必选 |
|--------|------|------|----------|
| accessToken | String | 授权过程获取的 access_token | Y |
| deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |
| channelNo | int | 通道号，IPC 设备填写 1 | Y |
| quality | int | 视频清晰度，0-流畅，1-高清 (720P),2-4CIF,3-1080P,4-400w **注：此参数不生效** | N |

### HTTP 请求报文

```http
POST /api/lapp/device/capture HTTP/1.1
Host: open.ys7.com
Content-Type: application/x-www-form-urlencoded

accessToken=at.12xp95k63bboast3aq0g5hg22q468929&deviceSerial=427734888&channelNo=1
```

### 返回数据

```json
{
  "data": {
    "picUrl": "https://ezviz-fastdfs-gateway.oss-cn-hangzhou.aliyuncs.com/1/capture/003eyM73IFbVHUM6Ktz7K6JXXLeUbFU.jpg?Expires=1654756106&OSSAccessKeyId=LTAIzI38nEHqg64n&Signature=SEGCPK0ExrKYZBEK3hc6ZZ%252FcPSY%3D"
  },
  "code": "200",
  "msg": "操作成功!"
}
```

### 返回字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| picUrl | String | 抓拍后的图片路径，**图片保存有效期为 2 小时** |

### 返回码

| 返回码 | 返回消息 | 描述 |
|--------|----------|------|
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken 异常或过期 | 重新获取 accessToken |
| 10005 | appKey 异常 | appKey 被冻结 |
| 10028 | 抓图接口调用次数超限 | 抓图接口调用次数超限 |
| 10031 | 子账户或萤石用户没有权限 | 子账户或萤石用户没有权限 |
| 10051 | 无权限进行抓图 | 设备不属于当前用户或者未分享给当前用户 |
| 20002 | 设备不存在 | - |
| 20006 | 网络异常 | 检查设备网络状况，稍后再试 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20008 | 设备响应超时 | 操作过于频繁或者设备不支持萤石协议抓拍 |
| 20014 | deviceSerial 不合法 | - |
| 20032 | 该用户下该通道不存在 | 检查设备是否包含该通道 |
| 49999 | 数据异常 | 接口调用异常 |
| 60012 | 设备抓图未知错误 | 可联系设备研发定位问题 |
| 60017 | 设备抓图失败，2030 等 | 可联系设备研发定位问题 |
| 60020 | 不支持该命令 | 确认设备是否支持抓图 |
| 60058 | 设备存在高风险，需求确权 | - |

---

## 2. 玩手机算法分析接口

**文档 URL**: https://open.ys7.com/help/3956  
**更新时间**: 2024.12.23

### 前置条件

- 开通 AI 算法服务，如未开通可联系客服支持
- 需联系客服手动开通该接口调用权限

### 接口 URL

```
POST https://open.ys7.com/api/service/intelligence/algo/analysis/play_phone_detection
```

### 请求参数

#### Header

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| accessToken | string | Y | 萤石开放 API 访问令牌 |

#### Body (JSON)

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| requestId | string | N | 请求 Id，请使用 uuid |
| stream | boolean | Y | 必传 false |
| dataInfo | array\<object\> | Y | 请求的输入数据内容 |
| └─ modal | string | Y | 数据模态：image（图片） |
| └─ type | string | Y | 数据类型：url |
| └─ data | object | Y | url 地址 |
| dataParams | array\<object\> | N | 请求的输入图片信息 |
| └─ modal | string | Y | 数据模态：image（图片） |
| └─ img_width | int | Y | 图片宽度 |
| └─ img_height | int | Y | 图片高度 |

### 请求示例

```bash
curl --location --request POST 'https://open.ys7.com/api/service/intelligence/algo/analysis/play_phone_detection' \
  --header 'accessToken: at.3xwsj8em6p28dw3t92nf4itq4mote8qr-6t75j5aq2m-1i7rkyf-pwz8z7rfi' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "taskType": "",
    "dataInfo": [
      {
        "data": "https://qna.smzdm.com/202403/20/65fa423e718c83216.jpg_e680.jpg",
        "type": "url",
        "modal": "image"
      }
    ],
    "dataParams": [
      {
        "modal": "image",
        "img_width": 1280,
        "img_height": 720
      }
    ]
  }'
```

### 返回数据

| 名称 | 类型 | 描述 |
|------|------|------|
| meta | object | 响应信息 |
| └─ code | int | 服务响应状态码 |
| └─ message | string | 服务响应状态描述 |
| └─ moreInfo | object | 服务响应描述 |
| data | object | 算法分析结果 |
| └─ taskType | string | 算法类型：play_phone_detection |
| └─ requestId | string | 请求唯一 ID |
| └─ images | list[Object] | 图片结果 |
| └─ └─ contentAnn | Object | 结构化分析结果 |
| └─ └─ ─ bboxes | List[object] | 检测数据结果 |
| └─ └─ └─ └─ points | list[List[float]] | 检测框（归一化值） |
| └─ └─ └─ └─ weight | float | 置信度 |
| └─ └─ └─ └─ tagInfo | Object | 标签信息 |
| └─ └─ └─ └─ └─ tag | String | "person" |
| └─ └─ └─ └─ └─ labels | List[object] | 行为标签 |
| └─ └─ └─ └─ └─ └─ key | String | "behavior" |
| └─ └─ └─ └─ └─ └─ label | String | "play_phone"（玩手机） |
| └─ └─ └─ └─ └─ └─ labelWeight | float | 置信度 |

### 返回示例

```json
{
  "meta": {
    "code": 200,
    "message": "success",
    "moreInfo": {},
    "success": true
  },
  "data": {
    "requestId": "56442d3243cc45a2bec4e9b2fe596ad1",
    "taskType": "play_phone_detection",
    "images": [
      {
        "frameIdx": 0,
        "imageHeight": 510,
        "imageWidth": 680,
        "contentAnn": {
          "bboxes": [
            {
              "points": [
                {"x": 0.2623883, "y": 0.08050475},
                {"x": 0.8080127, "y": 0.9986414}
              ],
              "weight": 0.993,
              "tagInfo": {
                "tag": "person",
                "labels": [
                  {
                    "key": "behavior",
                    "label": "play_phone",
                    "labelWeight": 1.0
                  }
                ]
              }
            }
          ]
        }
      }
    ]
  }
}
```

### 错误码

| 错误码 | 错误信息 | 解决方案 |
|--------|----------|----------|
| 10002 | accessToken 过期或异常 | 重新获取 accessToken |
| 60202 | 参数解析错误 | 检查请求参数格式 |
| 60203 | 未开通相关服务 | 联系客服开通服务 |
| 60206 | 并发数超限 | 降低请求频率 |
| 60205 | 服务内部错误 | 联系技术支持 |

---

## 3. 语音文件上传接口

**文档 URL**: https://open.ys7.com/help/1241  
**更新时间**: 2026.03.09

### 接口功能

上传本地语音文件到萤石云

### 请求地址

```
POST https://open.ys7.com/api/lapp/voice/upload
```

### 请求方式

POST (multipart/form-data)

### 请求参数

| 参数名 | 类型 | ParameterType | 描述 | 是否必填 |
|--------|------|-------------|------|----------|
| accessToken | String | body | 访问令牌 | Y |
| voiceFile | MultipartFile | form-data | 语音文件，支持 wav、mp3、aac 格式，最大 5M，最长 60s | Y |
| voiceName | String | body | 语音名称，最长 50 个字符 | N |
| force | boolean | body | 如果已存在相同 voiceName 的语音文件，则替换原语音文件，true 表示强制替换，false 表示如果存在不替换，默认为 false | N |

### 请求报文

```http
POST /api/lapp/voice/upload HTTP/1.1
Host: <host>:<port>
Content-Type: multipart/form-data
```

### 返回结果

| 参数名 | 类型 | 描述 |
|--------|------|------|
| msg | String | 操作信息 |
| code | String | 操作码，200 表示操作成功 |
| data | Object | 语音文件信息 |
| └─ name | String | 语音名称 |
| └─ url | String | 语音文件下载地址，有效期 1 天 |

### 返回示例

```json
{
  "msg": "Operation succeeded",
  "code": "200",
  "data": [
    {
      "name": "babble.wav",
      "url": "http://oss-cn-shenzhen.aliyuncs.com/voice/bbe5cc634be34a7484947d63f6361c22.aac?Expires=1583059824&OSSAccessKeyId=testId&&Signature=kM91%2By"
    }
  ]
}
```

---

## 4. 语音文件下发接口

**文档 URL**: https://open.ys7.com/help/1253  
**更新时间**: 2026.03.09

### 接口功能

语音文件下发，指定设备播放，需要设备支持能力集 support_talk=1 或 3

### 请求地址

```
POST https://open.ys7.com/api/lapp/voice/send
```

### 请求方式

POST

### 请求参数

| 参数名 | 类型 | Parameter Type | 描述 | 是否必填 |
|--------|------|---------------|------|----------|
| accessToken | String | body | 访问令牌 | Y |
| deviceSerial | String | body | 设备序列号 | Y |
| channelNo | int | body | 通道号，默认通道号为 1 | N |
| fileUrl | String | body | 下载音频文件的 url（上传接口返回的 url） | Y |

### 请求报文

```http
POST /api/lapp/voice/send HTTP/1.1
Host: <host>:<port>
Content-Type: application/x-www-form-urlencoded
```

### 返回数据

| 参数名 | 类型 | 描述 |
|--------|------|------|
| msg | String | 操作成功! |
| code | String | 200 |

### 返回示例

```json
{
  "msg": "操作成功!",
  "code": "200"
}
```

### 错误码

| 返回值 | 返回信息 | 描述 |
|--------|----------|------|
| 10001 | fileUrl 参数不合法 | 检查 fileUrl 格式 |
| 10001 | channels 参数不合法 | 检查通道号 |
| 20002 | 设备不存在 | 检查设备序列号 |
| 10031 | 子账户或萤石用户没有权限 | 检查权限 |
| 20018 | 该用户不拥有该设备 | 检查设备归属 |
| 49999 | Data error | 未知错误 |
| 20007 | 设备不在线 | 设备离线 |
| 20008 | 设备响应超时 | 网络问题 |
| 20001 | 通道不存在 | 检查通道号 |
| 20035 | 该通道被隐藏 | 通道被隐藏 |
| 20015 | 设备不支持对讲 | 设备不支持此功能 |
| 111000 | 用户资源包余量不足 | 前往控制台购买 |
| 111012 | 文件下发失败，内部错误 | 参考下方内部错误码 |

### 内部错误码（111012 详情）

| 内部错误码 | 错误描述 | 说明 |
|-----------|----------|------|
| 1 | 排队超时 | 请求排队超时 |
| 2 | 处理超时 | 处理过程超时 |
| 3 | 设备链接失败 | 设备网络状况不佳 |
| 4 | 服务器内部错误 | 服务器问题 |
| 5 | 消息错误 | 消息格式问题 |
| 6 | 请求重定向 | 请求被重定向 |
| 7 | 无效 URL | URL 格式错误 |
| 8 | 认证 token 失败 | token 无效 |
| 9 | 验证码或者秘钥不匹配 | 验证失败 |
| 10 | 设备正在对讲 | 设备忙 |
| 11 | 设备通信超时 | 通信超时 |
| 12 | 设备不在线 | 设备离线 |
| 13 | 设备开启隐私保护 | 隐私模式 |
| 14 | token 无权限 | 权限不足 |
| 15 | session 不存在 | session 失效 |
| 16 | 验证 token 其他问题 | token 问题 |
| 17 | 设备监听超时 | 监听超时 |
| 18 | 设备链路断开 | 连接断开 |
| 19 | 隐私遮蔽 | 隐私保护 |
| 20 | 声源定位 | 声源功能 |
| 21 | ticket 认证失败 | ticket 问题 |
| 22 | ticket 未开启 | ticket 未启用 |
| 23 | ticket bizcode 错误 | bizcode 错误 |
| 1003 | 设备网络异常断开 | 网络问题 |
| 10001 | 创建 ticket 失败 | ticket 创建失败 |
| 10002 | 连接 tts 失败 | TTS 连接问题 |
| 10003 | 下载文件失败 | 文件下载失败 |
| 10004 | kafka 消息格式错误 | 消息格式问题 |
| 10005 | tts 断开连接 | TTS 断开 |
| 10006 | tts url 异常 | TTS URL 问题 |
| 10007 | 超过并发限制 | 并发超限 |
| 10008 | 连接已经存在，重复请求 | 重复请求 |
| 10009 | 发送 kafka 失败 | kafka 发送失败 |
| 10010 | 不支持的音频格式 | 格式不支持 |

---

## 完整工作流程

```
1. 抓图 → 2. 玩手机检测 → 3. 生成 TTS → 4. 上传语音 → 5. 下发到设备
```

### 步骤说明

1. **抓图**: 使用摄像头抓拍当前画面，获取图片 URL
2. **玩手机检测**: 调用接口 1，传入图片 URL，分析是否有人玩手机
3. **生成 TTS**: 如检测到玩手机，生成"检测到有人玩手机"语音文件
4. **上传语音**: 调用接口 2，上传语音文件，获取 fileUrl
5. **下发到设备**: 调用接口 3，传入 deviceSerial 和 fileUrl，设备播放告警

### 判断逻辑

从接口 1 的返回结果中判断是否玩手机：

```javascript
const isPhoneDetected = data.images?.[0]?.contentAnn?.bboxes?.some(bbox => 
  bbox.tagInfo?.labels?.some(label => 
    label.key === "behavior" && label.label === "play_phone" && label.labelWeight > 0.5
  )
);
```
