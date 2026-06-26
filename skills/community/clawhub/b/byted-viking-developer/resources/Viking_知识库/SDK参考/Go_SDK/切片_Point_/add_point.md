# 概述
add_point 用于新增一个知识库下文档的一个切片
# **请求参数**
| **参数** | **类型** | **必选** | **默认值** | **备注** |
| --- | --- | --- | --- | --- |
| CollectionName | string | 否 | -- | **知识库名称** |
| ProjectName | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| ResourceID | string | 否 | -- | **知识库唯一 id** <br>  <br> * 可选择直接传 ResourceID，或同时传 CollectionName 和 ProjectName 作为知识库的唯一标识 |
| DocID | string | 是 | -- | **表示新增切片所属的文档** <br>  <br> * 不存在时会报错。 |
| ChunkType | string | 是 | -- | **要添加的切片类型** <br>  <br> * 和知识库支持的类型不匹配时会报错 <br> * 结构化知识库：“structured”， <br> * 非结构化知识库： <br> * “text”： 纯文本切片 <br> * “faq”： faq 类型切片 |
| Content | *string | 否 | -- | **新增切片文本内容** <br> 当 ChunkType 为 text、faq 时必传 <br> 1、text：Content 对应切片原文内容 <br> 2、faq：Content 对应**答案字段**内容 |
| ChunkTitle | *string | 否 | -- | **切片标题** <br> 只有非结构化文档支持修改切片的标题。 |
| Question | *string | 否 | -- | **新增 faq 切片中的问题字段** <br> 当 ChunkType 为 faq 时必传 <br>  <br> * 字段长度范围为 [1，{Embedding模型支持的最大长度}] |
| Fields | []map[string]interface{} | 否 | -- | **表示传入的结构化数据** <br> 当 ChunkType 为 structured 时必传。 <br> [ <br> { "field_name": "xxx" // 字段名称 <br> "field_value": xxxx // 字段值 <br> }, <br> ] <br>  <br> * field_name 必须已在所属知识库的表字段里配置，否则会报错 <br> * 和文档导入时的向量字段长度校验保持一致，拼接后的做 embedding 的文本长度不超过 65535 |
# **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| Code | int | 状态码 |
| Message | string | 返回信息 |
| RequestID | string | 标识每个请求的唯一标识符 |
| Data | *PointAddResult | PointAddResult |
### **PointAddResult**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| CollectionName | *string | 知识库的名字 |
| ResourceID | *string | 知识库唯一标识 |
| Project | *string | 项目名 |
| DocID | *string | 文档 id |
| ChunkID | *int64 | 切片在文档下的 id，文档下唯一 |
| PointID | *string | 切片 id，知识库下唯一 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Go SDK 中 AddPoint 函数的基础使用方法，使用前需配置 AK/SK 鉴权参数。
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

    content := "example content"
    question := "example question"
    chunkTitle := "example chunk title"

    resp, err := collection.AddPoint(ctx, model.AddPointRequest{
       DocID:      "your_doc_id",
       ChunkType:  "text",
       Content:    &content,
       Question:   &question,
       ChunkTitle: &chunkTitle,
       Fields: []map[string]interface{}{
          {
             "field_name": "example_field",
             "field_value":  "example_value",
          },
       },
    })
    if err != nil {
       fmt.Printf("AddPoint failed, err: %v\n", err)
       return
    }

    jsonData, _ := json.Marshal(resp)
    fmt.Printf("Response: %s\n", string(jsonData))
}
```


