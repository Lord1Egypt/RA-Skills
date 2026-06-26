# 概述
update_doc_meta 用于更新知识库上文档信息，文档 meta 信息更新会自动触发索引中的数据更新。
# **请求参数**
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| CollectionName | -- | string | 否 | -- | **知识库名称** |
| ProjectName | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| ResourceID | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 ResourceID，或同时传 CollectionName 和 ProjectName 作为知识库的唯一标识 |
| DocID | -- | string | 是 | -- | **待更新文档的 id** |
| Meta |  | []model.MetaItem | 否 | -- | **meta 信息** |
|  | FieldName | *string | 否 | -- | **要更新的字段名** |
|  | FieldType | *string | 否 | -- | **要更新的字段类型** <br>  <br> * 仅当新增知识库未配置过的标签字段时生效，且新增字段不能用于标量过滤，仅可作为当前文档的描述信息存储 <br> * 支持 "int64"，"float32"，"string"，"bool"，"list" 类型，限制参考[VikingDB的field_type规则和说明](https://www.volcengine.com/docs/84313/1254542#field-type-%E5%8F%AF%E9%80%89%E5%80%BC) |
|  | FieldValue | interface{} | 否 | -- | **要更新的字段值** <br> 字段值需保证类型符合字段定义，如 "int64"，"float32"，"string" 等 |
# **响应消息**
| **字段** | **类型** | **参数说明** |
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
本示例演示了知识库 Go SDK 中 UpdateDocMeta 函数的基础使用方法，通过指定知识库名称、文档 ID 和元数据信息（字段名、类型、值）修改文档元数据，使用前需配置 AK/SK 鉴权参数。
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

    docID := "your_doc_id"
    meta := []model.MetaItem{
       {
          FieldName:  func() *string { s := "category"; return &s }(),
          FieldType:  func() *string { s := "string"; return &s }(),
          FieldValue: "new_value",
       },
    }
    
    rsp, err := collection.UpdateDocMeta(ctx, docID, meta)
    if err != nil {
        fmt.Printf("UpdateDocMeta failed, err: %v\n", err)
        return
    }
    fmt.Printf("UpdateDocMeta success, Response: %v\n", rsp)
}
```


