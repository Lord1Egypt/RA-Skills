# DeletePackage

## 原始 Swagger
https://api.cnb.cool/#/operations/DeletePackage

## 接口描述
删除制品。 Delete the specific package.
## 接口权限
registry-package-delete:rw
## 请求信息

**请求方法：** DELETE

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/packages/{type}/{name}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | 资源路径。 Slug.|
| t | 字符串 | 是 | 制品类型。Type.|
| name | 字符串 | 是 | 制品名称。Package name.|
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X DELETE \
  "${CNB_API_ENDPOINT}/{slug}/-/packages/{type}/{name}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
