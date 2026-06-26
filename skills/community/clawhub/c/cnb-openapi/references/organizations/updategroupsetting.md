# UpdateGroupSetting

## 原始 Swagger
https://api.cnb.cool/#/operations/UpdateGroupSetting

## 接口描述
更新指定组织的配置。Updates the configuration for the specified organization.
## 接口权限
group-manage:rw
## 请求信息

**请求方法：** PUT

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/settings

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | slug|

### 请求体参数


**请求体结构：**

```json
{
  "email_verification": ["string"], // 组织限制指定邮箱认证才能加入
  "group_protection": 0, // 组织保护开关，0 - 关闭，1 - 打开
  "hide_members": 0, // 是否对外隐藏组织成员，0 - 否, 1 - 是
  "hide_sub_groups": 0, // 是否对外隐藏子组织，0 - 否, 1 - 是
  "show_private_repo_watermark": 0, // 是否对外显示私有仓库水印，0 - 否, 1 - 是
  "values": "string" // SettingValue 组织设置值，多个选项，用逗号拼接。可选值来自 SettingNamesArray 的值，e.g. disable_organization_readme,cloud_native_dev_only
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X PUT \
  "${CNB_API_ENDPOINT}/{slug}/-/settings" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "email_verification": ["string"],
  "group_protection": 0,
  "hide_members": 0,
  "hide_sub_groups": 0,
  "show_private_repo_watermark": 0,
  "values": "string"
}'
```
