# 概述
delete_point 用于删除一个知识库下的某个切片
# **请求参数**
| **参数** | **类型** | **必选** | **默认值** | **备注** |
| --- | --- | --- | --- | --- |
| CollectionName | string | 否 | -- | **知识库名称** <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空 <br> * 长度要求：[1, 64] |
| ProjectName | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| ResourceID | string | 否 | -- | **知识库唯一 id** <br>  <br> * 可选择直接传 ResourceID，或同时传 CollectionName 和 ProjectName 作为知识库的唯一标识 |
| PointID | string | 是 | -- | **要删除的切片 id** |
# **响应消息**
| 字段 | 类型 | 备注 |
| --- | --- | --- |
| Code | int32 | 状态码 |
| Message | string | 返回信息 |
| RequestID | string | 标识每个请求的唯一标识符 |
| Data | interface{} | 返回数据（通常为空） |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Go SDK 中 DeletePoint 函数的基础使用方法，通过指定知识库名称和切片 ID 实现切片删除，使用前需配置 AK/SK 鉴权参数。
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

    pointID := "your_point_id"
    rsp, err := collection.DeletePoint(ctx, model.DeletePointRequest{
        PointID: pointID,
    })
    if err != nil {
        fmt.Printf("DeletePoint failed, err: %v\n", err)
        return
    }
    
    fmt.Printf("DeletePoint success, Response: %v\n", rsp)
}
```


