# 概述
update_point 用于更新知识库下的切片内容
# **请求参数**
| 参数 | 类型 | 必选 | 默认值 | 备注 |
| --- | --- | --- | --- | --- |
| CollectionName | string | 否 | -- | **知识库名称** |
| ProjectName | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| ResourceID | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 ResourceID，或同时传 CollectionName 和 ProjectName 作为知识库的唯一标识 |
| PointID | string | 是 | -- | **要更新的切片 id** |
| ChunkTitle | *string | 否 | -- | **切片标题** <br> 只有非结构化文档支持修改切片的标题。 |
| Content | *string | 二者只传一个 | -- | **要更新的非结构化文档的切片内容** <br>  <br> * 1、非结构化文件：Content 对应切片原文内容 <br> * 2、faq 文件：Content 对应答案字段内容 <br> * 3、结构化文件：Content 对应参与索引的字段和取值，以 K:V 对拼接，使用 \n 区隔 |
| Fields | []map[string]interface{} |  | -- | **要更新的结构化文档的切片内容** <br> 一行数据全量更新 <br> [ <br> { "field_name": "xxx" // 字段名称 <br> "field_value": xxxx // 字段值 <br> }, <br> ] <br> field_name 必须已在所属知识库的表字段里配置，否则会报错 |
| Question | *string | 否 | -- | **要更新的非结构化 faq 文档切片的问题字段** |
# **响应消息**
| 字段 | 类型 | 备注 |
| --- | --- | --- |
| Code | int32 | 状态码 |
| Message | string | 返回信息 |
| RequestID | string | 标识每个请求的唯一标识符 |
| Data | interface{} | 返回数据（通常为空） |
## **状态码说明**
| code | message | 备注 | http status_code |
| --- | --- | --- | --- |
| 0 | success | 成功 | 200 |
| 1000001 | unauthorized | 缺乏鉴权信息 | 401 |
| 1000002 | no permission | 权限不足 | 403 |
| 1000003 | invalid request：%s | 非法参数 | 400 |
| 1000005 | collection not exist | collection不存在 | 400 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Go SDK 中 UpdatePoint 函数的基础使用方法，通过指定知识库名称和切片 ID 修改切片内容，使用前需配置 AK/SK 鉴权参数。
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
    content := "updated content"
    rsp, err := collection.UpdatePoint(ctx, pointID, model.UpdatePointRequest{
        Content: &content,
    })
    if err != nil {
        fmt.Printf("UpdatePoint failed, err: %v\n", err)
        return
    }
    fmt.Printf("UpdatePoint success, Response: %v\n", rsp)
}
```


