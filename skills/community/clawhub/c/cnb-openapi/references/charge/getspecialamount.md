# GetSpecialAmount

## 原始 Swagger
https://api.cnb.cool/#/operations/GetSpecialAmount

## 接口描述
查看特权额度
## 接口权限
group-resource:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/charge/special-amount

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | group slug|
## 响应信息


**响应类型：** dto.SpecialAmount

**响应结构：**
```json
{
  "compute_build_corehour": 0, // 云原生构建cpu核时
  "compute_build_desc": "string",
  "compute_build_expire": "string", // 过期时间时为 null 时永久有效
  "compute_build_gpu_corehour": 0, // 云原生构建gpu核时
  "compute_build_gpu_desc": "string",
  "compute_build_gpu_expire": "string", // 过期时间时为 null 时永久有效
  "compute_develop_corehour": 0, // 云原生开发cpu核时
  "compute_develop_desc": "string",
  "compute_develop_expire": "string", // 过期时间时为 null 时永久有效
  "compute_develop_gpu_corehour": 0, // 云原生开发gpu核时
  "compute_develop_gpu_desc": "string",
  "compute_develop_gpu_expire": "string", // 过期时间时为 null 时永久有效
  "storage_git_desc": "string",
  "storage_git_expire": "string", // 过期时间时为 null 时永久有效
  "storage_git_gib": 0, // git存储空间
  "storage_object_desc": "string",
  "storage_object_expire": "string", // 过期时间时为 null 时永久有效
  "storage_object_gib": 0 // 对象存储空间
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{slug}/-/charge/special-amount" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
