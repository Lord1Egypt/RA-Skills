# CreateOrganization

## 原始 Swagger
https://api.cnb.cool/#/operations/CreateOrganization

## 接口描述
创建新组织。Create new organization.
## 接口权限
group-manage:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/groups

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 请求体参数


**请求体结构：**

```json
{
  "bind_domain": "string", // BindDomain 根组织绑定的域名
  "description": "string",
  "path": "string",
  "remark": "string"
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/groups" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "bind_domain": "string",
  "description": "string",
  "path": "string",
  "remark": "string"
}'
```
