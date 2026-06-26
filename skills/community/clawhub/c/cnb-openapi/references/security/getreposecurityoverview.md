# GetRepoSecurityOverview

## 原始 Swagger
https://api.cnb.cool/#/operations/GetRepoSecurityOverview

## 接口描述
查询仓库安全模块概览数据。Query the security overview data of a repository
## 接口权限
repo-security:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/security/overview

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 仓库名称|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| types | 字符串 | 否| 类型，多个类型用逗号分隔code_sensitive,code_vulnerability,code_issue，为空默认查询所有类型|
| tab | 字符串 | 否| 查询类型下开启或忽略的各风险类型概览数量,可选值：open,ignore,all，默认all|
## 响应信息


**响应类型：** dto.RepoSecurityOverview

**响应结构：**
```json
{
  "code_issue": {
    "critical_count": 0, // 严重风险问题数量
    "critical_ignore_count": 0, // 严重风险问题忽略数量
    "enable": false, // 是否开启源码信息扫描
    "high_count": 0, // 高风险问题数量
    "high_ignore_count": 0, // 高风险问题忽略数量
    "ignored": 0, // 忽略的问题数量
    "low_count": 0, // 低风险问题数量
    "low_ignore_count": 0, // 低风险问题忽略数量
    "medium_count": 0, // 中风险问题数量
    "medium_ignore_count": 0, // 中风险问题忽略数量
    "open": 0 // 开启中问题数量
  },
  "code_license": {
    "enable": false, // 是否开启 License 扫描
    "high_risk_cnt": 0, // 高风险 License 数量
    "low_risk_cnt": 0, // 低风险 License 数量
    "medium_risk_cnt": 0, // 中风险 License 数量
    "na_risk_cnt": 0 // 未知风险 License 数量
  },
  "code_sensitive": {
    "enable": false, // 是否开启代码敏感信息扫描
    "high_count": 0, // 高风险问题数量
    "high_ignore_count": 0, // 高风险问题忽略数量
    "ignored": 0, // 忽略问题数量
    "low_count": 0, // 低风险问题数量
    "low_ignore_count": 0, // 低风险问题忽略数量
    "medium_count": 0, // 中风险问题数量
    "medium_ignore_count": 0, // 中风险问题忽略数量
    "open": 0 // 开启中问题数量
  },
  "code_vulnerability": {
    "critical_vul_ignore_cnt": 0, // 忽略的严重风险漏洞的数量
    "critical_vul_open_cnt": 0, // 打开的严重风险级别漏洞的数量
    "enable": false, // 是否开启代码漏洞扫描
    "high_vul_ignore_cnt": 0, // 忽略的高风险级别漏洞的数量
    "high_vul_open_cnt": 0, // 打开的高风险级别漏洞的数量
    "ignored": 0, // 忽略问题数量
    "low_vul_ignore_cnt": 0, // 忽略的低风险级别漏洞的数量
    "low_vul_open_cnt": 0, // 打开的低风险级别漏洞的数量
    "medium_vul_ignore_cnt": 0, // 忽略的中风险级别漏洞的数量
    "medium_vul_open_cnt": 0, // 打开的中风险级别漏洞的数量
    "open": 0 // 开启中问题数量
  },
  "risk_cnt": {
    "code_issue_enable": false, // 是否开启源码扫描
    "code_issue_risk_cnt": 0, // 源码扫描风险数量 (严重+高风险）
    "code_license_enable": false, // 是否开启代码 License 扫描
    "code_license_risk_cnt": 0, // License风险数量 (高风险）
    "code_sensitive_enable": false, // 是否开启代码敏感信息扫描
    "code_sensitive_risk_cnt": 0, // 敏感信息风险数量（高风险）
    "code_vulnerability_enable": false, // 是否开启代码漏洞扫描
    "code_vulnerability_risk_cnt": 0, // 代码漏洞风险数量（严重+高风险）
    "enable": false, // 是否开启安全模块
    "total": 0 // 总计数
  }
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/security/overview" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "types=<types>" \
-d "tab=<tab>" \
```
