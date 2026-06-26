# 概述
list_docs 用于查询知识库上文档的列表，默认按照文档的上传时间倒序。
# **请求参数**
| **参数** | 子参数 | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| CollectionName | -- | string | 否 | -- | **知识库名称** |
| ProjectName | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| ResourceID | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 ResourceID，或同时传 CollectionName 和 ProjectName 作为知识库的唯一标识 |
| Filter |  | map[string]interface{} | 否 | -- | **过滤条件** <br> 用于对返回结果进行过滤，支持使用 doc_id 过滤 |
|  | DocIDList | []string | 否 | -- | **指定 doc_id 过滤条件** <br> 只返回列表中指定的文档信息 |
| Offset | -- | int | 否 | 0 | **查询起始位置** <br> 表示从结果的第几个文档后开始取，需要大于等于0 <br> 注：如果设置 Offset ≥ 100，需同时传入 Limit 参数才能生效 |
| Limit | -- | int | 否 | -1 | **查询文档数** <br> -1 表示获取所有，最大值不超过 100，每次返回最多不超过 100 |
| DocType | -- | *string | 否 | -- | **文档类型筛选** |
| ReturnTokenUsage | -- | *bool | 否 | false | **是否返回文档向量化和文档摘要生成所消耗的 tokens** |
# **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| Code | int | 状态码 |
| Message | string | 返回信息 |
| RequestID | string | 标识每个请求的唯一标识符 |
| Data | *ListDocsResult | ListDocsResult |
### **ListDocsResult**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| DocList | []DocInfo | 文档信息列表 |
| Count | *int | 本次查询返回的文档总数 |
| TotalNum | *int | 该知识库下的文档总数 |
### **DocInfo**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| CollectionName | *string | 知识库名称 |
| DocName | *string | 文档名称 |
| DocID | *string | 文档 id |
| DocHash | *string | 文档 hash |
| AddType | *string | 导入方式 |
| DocType | *string | 文档类型 |
| Description | *string | 文档描述（当前仅支持图片文档） |
| CreateTime | *int64 | 文档创建时间 |
| AddedBy | *string | 添加人 |
| UpdateTime | *int64 | 文档更新时间 |
| URL | *string | 原始文档链接 |
| TOSPath | *string | tos 路径 |
| PointNum | *int | 切片数量 |
| Status | *DocStatus | DocStatus |
| Title | *string | 文档标题 |
| Source | *string | 知识来源（url，tos 等） |
| TotalTokens | interface{} | token 统计 |
| DocSummaryTokens | *int | 摘要 token 统计 |
| DocPremiumStatus | *DocPremiumStatus | DocPremiumStatus |
| DocSummary | *string | 文档摘要 |
| BriefSummary | *string | 简要摘要 |
| DocSize | *int | 文档大小 |
| Meta | *string | meta 信息 |
| Labels | map[string]string | 标签信息 |
| VideoOutline | map[string]interface{} | 视频大纲 |
| AudioOutline | map[string]interface{} | 音频大纲 |
| Statistics | map[string]interface{} | 统计信息 |
| Project | *string | 项目名 |
| ResourceID | *string | 知识库唯一 id |
### **DocStatus**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| ProcessStatus | *int | 处理状态 |
| FailedCode | *int | 失败错误码 |
| FailedMsg | *string | 失败错误信息 |
### **DocPremiumStatus**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| DocSummaryStatusCode | *int |  |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection不存在 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Go SDK 中 ListDocs 的基础使用方法，通过指定知识库名实现文档列表查询，使用前需配置 AK/SK 鉴权参数。
```Go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "os"
    "time"

    "github.com/volcengine/vikingdb-go-sdk/knowledge"
    "github.com/volcengine/vikingdb-go-sdk/knowledge/model"
)

func main() {
    var (
       accessKey = os.Getenv("VIKINGDB_AK")
       secretKey = os.Getenv("VIKINGDB_SK")
       endpoint  = "https://api-knowledgebase.mlp.cn-beijing.volces.com"
       region    = "cn-beijing"
    )

    client, err := knowledge.New(
       knowledge.AuthIAM(accessKey, secretKey),
       knowledge.WithEndpoint(endpoint),
       knowledge.WithRegion(region),
       knowledge.WithTimeout(time.Second*30),
    )
    if err != nil {
       fmt.Printf("New client failed, err: %v\n", err)
       return
    }
    ctx := context.Background()

    collection := client.Collection(model.CollectionMeta{
       CollectionName: "your_collection_name",
       ProjectName:    "default",
    })

    resp, err := collection.ListDocs(ctx, model.ListDocsRequest{
       Offset: 0,
       Limit:  10,
    })
    if err != nil {
       fmt.Printf("ListDocs failed, err: %v\n", err)
       return
    }

    jsonData, _ := json.Marshal(resp)
    fmt.Printf("Response: %s\n", string(jsonData))
}
```


