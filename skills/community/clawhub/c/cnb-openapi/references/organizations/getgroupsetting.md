# GetGroupSetting

## 原始 Swagger
https://api.cnb.cool/#/operations/GetGroupSetting

## 接口描述
获取指定组织的配置详情。Get the configuration details for the specified organization.
## 接口权限
group-manage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/settings

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | group path|
## 响应信息


**响应类型：** dto.OrganizationSettingWithParent

**响应结构：**
```json
{
  "can_show_members": false, // 上级group设置了hide_members为1，则下级都不能显示
  "can_show_sub_groups": false, // 上级group设置了hide_sub_groups为1，则下级都不能显示
  "can_show_watermark": false,
  "email_verification": ["string"],
  "group_protection": 0,
  "hide_members": 0, // 是否对外隐藏组织成员，0 - 否, 1 - 是
  "hide_sub_groups": 0, // 是否对外隐藏子组织，0 - 否, 1 - 是
  "root_email_verification": ["string"],
  "root_group_protection": false,
  "root_values": {
  },
  "show_private_repo_watermark": 0,
  "values": {
  }
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{slug}/-/settings" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
