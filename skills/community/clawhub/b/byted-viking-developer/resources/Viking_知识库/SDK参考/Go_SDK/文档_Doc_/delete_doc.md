# 概述
delete_doc 用于删除知识库下的文档
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| CollectionName | string | 否 | -- | **知识库名称** |
| ProjectName | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| ResourceID | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 ResourceID，或同时传 CollectionName 和 ProjectName 作为知识库的唯一标识 |
| DocID | string | 是 | -- | **要删除的文档 id** |
# **响应消息**
| **参数** | **类型** | **参数说明** |
| --- | --- | --- |
| Code | int32 | 状态码 |
| Message | string | 返回信息 |
| RequestID | string | 标识每个请求的唯一标识符 |
| Data | interface{} | 返回数据（通常为空） |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection不存在 |
| 1001001 | 400 | doc not exist | doc不存在 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Go SDK 中 DeleteDoc 函数的基础使用方法，通过指定知识库名称和文档 ID 实现文档删除，使用前需配置 AK/SK 鉴权参数。
```Go
package main

import (
    "context"
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

    // Replace with a valid doc ID from your collection
    docID := "example_doc_id"
    rsp, err := collection.DeleteDoc(ctx, docID)
    if err != nil {
        fmt.Printf("DeleteDoc failed, err: %v\n", err)
        return
    }
    fmt.Printf("DeleteDoc Response: %v\n", rsp)
}
```


