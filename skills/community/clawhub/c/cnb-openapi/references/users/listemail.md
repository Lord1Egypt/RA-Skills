# ListEmail

## 原始 Swagger
https://api.cnb.cool/#/operations/ListEmail

## 接口描述
获取用户邮箱列表
## 接口权限
account-email:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/user/emails

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |

## 响应信息


**响应类型：** dto.UserEmails

**响应结构：**
```json
{
  "contact_email": "string", // ContactEmail 用户通知邮箱
  "email": "string", // Email 用户git提交邮箱，是 emails 里面的某一个
  "emails": ["string"], // Emails 邮箱列表
  "system_email": "string", // 系统默认邮箱
  "system_email_contact": false // 系统默认邮箱是否可以通知
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/user/emails" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
