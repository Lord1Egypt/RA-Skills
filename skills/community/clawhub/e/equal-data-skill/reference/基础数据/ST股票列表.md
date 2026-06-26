# ST股票列表

> 分类: 基础数据 | 目录: `基础数据` | 索引见 `SKILL.md`

<!-- generated_at: 2026-04-30T09:29:07.184-1777512547186 -->


### 描述

查询A股所有ST股票列表，返回公司基本信息等。查询A股范围内，所有ST股票，包含公司基本信息，可指定需要查询的公司的股票代码。分页每页最多20条。

### 请求参数

| 名称 | 类型 | 必填 | 默认值 | 说明 |
|:---|:---|:---|:---|:---|
| `interfaceId` | `str` | 是 | "F4" | 接口ID |
| `pageNum` | `int` | 否 | `0` | 分页偏移量，从 0 开始（第 1 页为 0，第 2 页为 pageSize） |
| `pageSize` | `int` | 否 | `10` | 每页条数 |
| `stockCodes` | `str` | 是 | - | 股票代码或公司全称、简称，可多个使用逗号隔开；示例：000001,600519 |

### 返回参数

ResultData.data 为 List，元素为ST股票

| 名称 | 类型 | 是否必返回 | 说明 |
|:---|:---|:---|:---|
| `data` | `list[ListedCompanyVo]` | 否 | ST股票列表 |
| `stockCode` | `str` | 否 | 股票代码 |
| `companyName` | `str` | 否 | 公司全称 |
| `companyShortName` | `str` | 否 | 公司简称 |
| `formername` | `str` | 否 | 曾用名 |
| `industry` | `str` | 否 | 所属行业 |
| `subIndustry` | `str` | 否 | 所属子行业 |
| `establishmentDate` | `str` | 否 | 成立日期 |
| `registrationDate` | `str` | 否 | 注册日期 |
| `registeredCapital` | `str` | 否 | 注册资金（亿） |
| `province` | `str` | 否 | 所属地域 |
| `registeredProvince` | `str` | 否 | 注册地点省 |
| `registeredCity` | `str` | 否 | 注册地点市 |
| `registeredCounty` | `str` | 否 | 注册地点县 |
| `legalRepresentative` | `str` | 否 | 法人代表 |
| `listingDate` | `str` | 否 | 上市时间 |
| `companyType` | `str` | 否 | 公司类型 |
| `businessOverview` | `str` | 否 | 业务概述 |
| `actualController` | `str` | 否 | 实际控制人 |
| `companyIntroduction` | `str` | 否 | 公司简介 |
| `industryDomain` | `str` | 否 | 行业领域 |
| `stockType` | `str` | 否 | 证券类别 |
| `businessScope` | `str` | 否 | 经营范围 |
| `delistedDate` | `str(datetime)` | 否 | 退市时间 |

### 调用示例

```python
from equal_data import EqualDataApi  
api = EqualDataApi('your API_KEY') 
# 调用接口
data = api.query_equal_data(
    interfaceId="F4",
    pageNum=None,  # int  # 默认: 0
    pageSize=None,  # int  # 默认: 10
    stockCodes=None,  # str  # 默认: 
)
```


