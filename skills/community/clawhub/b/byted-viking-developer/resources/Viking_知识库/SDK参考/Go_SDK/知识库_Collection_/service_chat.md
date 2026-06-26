# 概述
service_chat 支持基于一个已创建的知识服务进行检索/问答。
# 请求参数
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| ServiceResourceID | string | 是 | -- | **知识服务唯一 id** |
| Messages | []model.ChatMessage | 是 | -- | **检索/问答多轮对话消息** <br> 格式为一问一答形式，发出消息的对话参与者角色，可选值包括： <br>  <br> * user：User Message 用户消息 <br> * assistant：Assistant Message 对话助手消息 <br>  <br> 其中 **最后一个元素 role == user ，content 为当前最新的提问 query** <br> **纯文本对话：** <br> 例如： <br> ```python <br> [ <br>      { <br>          "role": "system", <br>          "content": "你是一位在线客服，你的首要任务是通过巧妙的话术回复用户的问题，你需要根据「参考资料」来回答接下来的「用户问题」，这些信息在 <context></context> XML tags 之内，你需要根据参考资料给出准确，简洁的回答。参考资料中可能会包含图片信息，图片的引用说明在<img></img>XML tags 之内，参考资料内的图片顺序与用户上传的图片顺序一致。" <br>      }, <br>      {"role": "user", "content": "你好"}, <br>      {"role": "assistant", "content": "你好！有什么我可以帮助你的？"}， <br>      {"role": "user", "content": "当前轮次用户问题"} <br>  ] <br> ``` <br>  <br> **图文对话**： <br> 例如： <br> ```json <br> [ <br>      { <br>          "role": "system", <br>          "content": "你是一位在线客服，你的首要任务是通过巧妙的话术回复用户的问题，你需要根据「参考资料」来回答接下来的「用户问题」，这些信息在 <context></context> XML tags 之内，你需要根据参考资料给出准确，简洁的回答。参考资料中可能会包含图片信息，图片的引用说明在<img></img>XML tags 之内，参考资料内的图片顺序与用户上传的图片顺序一致。" <br>      }, <br>      { <br>          "role": "user", <br>          "content": [ <br>              { <br>                  "type": "text", <br>                  "text": "推荐一个类似的适合 3 岁小孩的玩具" <br>              }, <br>              { <br>                  "type": "image_url", <br>                  "image_url": { <br>                      "url": "https://ark-project.tos-cn-beijing.volces.XXX.jpeg" #客户上传的图片，支持 URL/base 64 编码，协议详见：https://www.volcengine.com/docs/82379/1362931?lang=zh#477e51ce 和 https://www.volcengine.com/docs/82379/1362931?lang=zh#d86010f4 <br>                  } <br>              } <br>          ] <br>      } <br>  ] <br> ``` <br>  |
| QueryParam | map[string]interface{} | 否 | nil | **检索过滤条件** <br> 在创建知识服务时如果您已配置了过滤条件，那么和该附加过滤条件一起生效，逻辑为 and <br>  <br> * 支持对 doc 的 meta 信息过滤 <br> * 详细使用方式和支持字段见[filter表达式](https://www.volcengine.com/docs/84313/1419289#filter-%E8%A1%A8%E8%BE%BE%E5%BC%8F)，可支持对 doc_id 做筛选 <br> * 此处用过过滤的字段，需要在 collection/create 时添加到 index_config 的 fields 上 <br>  <br> 例如： <br> 单层 filter： <br> ```json <br> doc_filter = { <br>     "op": "must", // 查询算子 must/must_not/range/range_out <br>     "field": "doc_id", <br>     "conds": ["tos_doc_id_123", "tos_doc_id_456"] <br>  } <br>  query_param = { <br>      "doc_filter": doc_filter <br>  } <br> ``` <br>  <br> 多层 filter： <br> ```json <br> doc_filter = { <br>    "op": "and",   // 逻辑算子 and/or <br>    "conds": [     // 条件列表，支持嵌套逻辑算子和查询算子 <br>      { <br>        "op": "must", <br>        "field": "type", <br>        "conds": [1] <br>      }, <br>      { <br>          ...         // 支持>=1的任意数量的条件进行组合 <br>      } <br>    ] <br>  } <br>  <br>  query_param = { <br>      "doc_filter": doc_filter <br>  } <br> ``` <br>  |
| Stream | *bool | 否 | true | **是否采用流式返回** <br> 当创建的知识服务为问答类型服务时生效 |
# **响应消息**
目前知识服务主要分为两类，检索类型和问答类型。针对不同类型的知识服务，返回的消息格式也有所不同
检索/问答/流式的差异体现在 Data 内字段是否出现及返回时机：
Count、RewriteQuery、ResultList 通常在首流返回；TokenUsage 通常在尾流返回；GeneratedAnswer、ReasoningContent 在中间流分段返回（SSE）。
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| Code | int | 状态码 |
| Message | string | 返回信息 |
| RequestID | string | 标识每个请求的唯一标识符 |
| Data | *ServiceChatData | ServiceChatData |
### **ServiceChatData**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| Count | *int | 检索结果返回的条数 |
| RewriteQuery | *string | query 改写的结果 |
| TokenUsage | interface{} | Token 使用信息 |
| ResultList | []ServiceChatRetrieveItem | 检索返回的信息 |
| GeneratedAnswer | *string | LLM 模型生成的回答 |
| ReasoningContent | *string | 推理模型生成的内容 |
| Prompt | *string | prompt 内容 |
| End | *bool | 是否结束（流式场景用于标识最后一段） |
### **ServiceChatRetrieveItem**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| ID | *string | 索引的主键 |
| Content | *string | 切片内容 <br> 1、非结构化文件：Content 返回切片内容 <br> 2、faq 文件：Content 返回答案 <br> 3、结构化文件：Content 返回参与索引的字段和取值，以 K:V 对拼接，使用 \n 区隔 |
| MDContent | *string | markdown 格式的解析结果（表格切片可通过 ChunkType == table 判断） |
| Score | *float64 | 向量化语义检索得分 |
| PointID | *string | 切片 id |
| OriginText | *string | 原始文本 |
| OriginalQuestion | *string | faq 数据检索召回答案对应的原始问题 |
| ChunkTitle | *string | 切片标题 |
| ChunkID | *int64 | 切片位次 id（代表在原始文档中的位次顺序） |
| ProcessTime | *int64 | 检索耗时（s） |
| RerankScore | *float64 | 重排得分 |
| DocInfo | *ServiceChatRetrieveItemDocInfo | ServiceChatRetrieveItemDocInfo |
| RecallPosition | *int | 向量化语义检索召回位次 |
| RerankPosition | *int | 重排位次 |
| ChunkType | *string | 切片所属类型（如 doc-image、image、video、table、mixed-table、text、structured、faq 等） |
| ChunkSource | *string | 切片来源 |
| UpdateTime | *int64 | 更新时间 |
| ChunkAttachment | []ChunkAttachment | 检索召回附件的临时下载链接，有效期 10 分钟 |
| TableChunkFields | []PointTableChunkField | 结构化数据检索返回单行全量数据 |
| OriginalCoordinate | map[string]interface{} | 切片在所属文档的原始位置坐标 |
### **ServiceChatRetrieveItemDocInfo**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| DocID | *string | 文档 id |
| DocName | *string | 文档名字 |
| CreateTime | *int64 | 文档的创建时间 |
| DocType | *string | 知识所属原始文档的类型 |
| DocMeta | *string | 文档相关元信息 |
| Source | *string | 知识来源类型 |
| Title | *string | 知识所属文档的标题 |
### **ChunkAttachment**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| UUID | *string | 附件的唯一标识 |
| Caption | *string | 图片所属标题，若未识别到标题则值为 "\n" |
| Type | *string | image 等 |
| Link | *string | 临时下载链接，有效期 10 分钟 |
| InfoLink | *string | 附件 info_link |
| ColumnName | *string | 附件列名 |
### **PointTableChunkField**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| FieldName | *string | 字段名 |
| FieldValue | interface{} | 字段值 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Go SDK 中 ServiceChat 的基础使用方法，包含普通调用和流式调用两种方式；该功能需使用 API Key 鉴权，且需配置知识服务 ID。
```Go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "github.com/volcengine/vikingdb-go-sdk/knowledge"
    "github.com/volcengine/vikingdb-go-sdk/knowledge/model"
    "os"
    "time"
)

func main() {
    var (
       apiKey   = os.Getenv("VIKING_SERVICE_API_KEY")
       endpoint = "https://api-knowledgebase.mlp.cn-beijing.volces.com"
       region   = "cn-beijing"
    )

    client, err := knowledge.New(
       knowledge.AuthAPIKey(apiKey),
       knowledge.WithEndpoint(endpoint),
       knowledge.WithRegion(region),
       knowledge.WithTimeout(time.Second*30),
    )
    if err != nil {
       fmt.Printf("New client failed, err: %v\n", err)
       return
    }
    ctx := context.Background()

    // 1. Prepare messages
    messages := []model.ChatMessage{
       {
          Role:    "user",
          Content: "Help me find some documents.",
       },
    }

    // 2. Call ServiceChat
    stream := false
    resp, err := client.ServiceChat(ctx, model.ServiceChatRequest{
       ServiceResourceID: "your_service_resource_id", // Replace with your service resource id
       Messages:          messages,
       Stream:            &stream,
    })
    if err != nil {
       fmt.Printf("ServiceChat failed, err: %v\n", err)
       return
    }

    jsonData, _ := json.Marshal(resp)
    fmt.Printf("Response: %s\n", string(jsonData))
    
    // 3. Call ServiceChat Stream
    stream = true
    ch, err := client.ServiceChatStream(ctx, model.ServiceChatRequest{
       ServiceResourceID: "your_service_resource_id", // Replace with your service resource id
       Messages:          messages,
       Stream:            &stream,
    })
    if err != nil {
       fmt.Printf("ServiceChatStream failed, err: %v\n", err)
       return
    }
    // Read from channel
    for resp := range ch {
       jsonData, _ := json.Marshal(resp)
       fmt.Printf("Chunk: %s\n", string(jsonData))
    }
}
```


