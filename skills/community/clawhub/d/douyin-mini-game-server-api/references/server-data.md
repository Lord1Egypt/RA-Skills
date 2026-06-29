# 数据缓存 API

## setUserStorage — 写用户数据

### 接口说明

以 key-value 形式存储用户数据到小程序平台的云存储服务。若开发者无内部存储服务则可接入，免费且无需申请。一般情况下只存储用户的基本信息，禁止写入大量不相干信息。

**Tip**:
- 当 key 是开发者所配置的排行榜 key 时，value 的内容应满足 KVData 格式，必须是 string 类型
- 该接口为服务端接口，效果与前端 `tt.setUserCloudStorage` 一致
- 通过该接口设置数据后，可在前端通过 `tt.getUserCloudStorage` 或 `tt.getCloudStorageByRelation` 获取

### 基本信息

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/set_user_storage` |
| HTTP Method | POST |
| Scope | open.ttgame.mgplatform |

### 请求参数

**请求头**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content-type | String | 是 | 固定值 `"application/json"` |

**Query**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| access_token | String | 是 | 调用 getAccessToken 生成的 token |
| openid | String | 是 | 登录用户唯一标识 |
| sig_method | String | 是 | 用户登录态签名的编码方法 |
| signature | String | 是 | 用户登录态签名 |

**Body**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| kv_list | Array\<Struct\> | 是 | 要设置的用户数据 |
| kv_list[].key | String | 是 | 键 |
| kv_list[].value | String | 是 | 值 |

### 响应参数

| 参数名 | 类型 | 说明 |
|------|------|------|
| error | Int32 | 错误号，0 为成功 |
| errcode | Int32 | 详细错误号 |
| errmsg | String | 错误信息 |
| message | String | 错误信息（同 errmsg） |

**响应示例**

```json
{
  "error": 0
}
```

### 错误码

| HTTP 状态码 | 错误码 | 描述 | 排查建议 |
|------|------|------|------|
| 200 | 0 | 请求成功 | - |
| 200 | -1 | 系统错误 | - |
| 200 | 40009 | key 长度大于 128 个字节 | 缩短 key 长度 |
| 200 | 40010 | key 和 value 的长度和大于 1024 个字节 | 减少数据量 |
| 200 | 40011 | 排行榜 key 对应的 value 值格式不对 | 检查 KVData 格式 |
| 200 | 60001 | 单用户存储 kv 超过 128 对 | 删除不需要的 kv |

---

## removeUserStorage — 删除用户数据

### 接口说明

删除存储到字节跳动的云存储服务的 key-value 数据。当开发者不需要该用户信息时，需要删除，以免占用过大的存储空间。

**Tip**: 该接口为服务端接口，效果与前端 `tt.removeUserCloudStorage` 一致。

### 基本信息

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/remove_user_storage` |
| HTTP Method | POST |
| Scope | open.ttgame.mgplatform |

### 请求参数

**请求头**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content-type | String | 是 | 固定值 `"application/json"` |

**Query**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| access_token | String | 是 | 调用 getAccessToken 生成的 token |
| openid | String | 是 | 登录用户唯一标识 |
| sig_method | String | 是 | 用户登录态签名的编码方法 |
| signature | String | 是 | 用户登录态签名 |

**Body**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | Array\<String\> | 是 | 要删除的用户数据的 key list |

### 响应参数

| 参数名 | 类型 | 说明 |
|------|------|------|
| error | Int32 | 错误号，0 为成功 |
| errcode | Int32 | 详细错误号 |
| errmsg | String | 错误信息 |
| message | String | 错误信息（同 errmsg） |

**响应示例**

```json
{
  "error": 0
}
```

### 错误码

| HTTP 状态码 | 错误码 | 描述 | 排查建议 |
|------|------|------|------|
| 200 | 0 | 请求成功 | - |
| 200 | -1 | 系统错误 | - |
| 200 | 40009 | key 长度大于 128 个字节 | 检查 key 长度 |

## 数据存储限制

| 限制项 | 值 |
|------|------|
| key 最大长度 | 128 字节 |
| key + value 最大长度 | 1024 字节 |
| 单用户最大 kv 对数 | 128 对 |
| value 格式（排行榜） | 必须是 String 类型，满足 KVData 格式 |
