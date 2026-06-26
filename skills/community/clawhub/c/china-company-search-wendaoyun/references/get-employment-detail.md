# get-employment-detail - 企业招聘信息详情

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | long | 是 | 招聘信息ID（从 `get-employment-info` 返回结果中获取） |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| education | string | 学历 |
| experience | string | 经验 |
| duty | string | 岗位职责 |
| requirement | string | 岗位要求 |
| area | string | 区域 |
| salary | string | 月薪 |
| title | string | 职位标题 |
| orgName | string | 企业名称 |
| orgId | long | 企业ID |