本节将说明如何单独调用rerank模型，以计算两段文本间的相似度
## **概述**
rerank 用于重新批量计算输入文本与检索到的文本之间的 score 值，以对召回结果进行重排序。判断依据 chunk content 能回答 query 提问的概率，分数越高即模型认为该文本片能回答 query 提问的概率越大。
## **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| Datas | []model.RerankDataItem | 是 | -- | **待重排的数据列表** <br> 每个元素为一个 map，数组长度不超过 200，支持以下参数： <br>  <br> * Query（必选）：用于排序的查询内容，interface{} <br> * string：纯文本查询内容，重排模型通用 <br> * object：文或图查询内容，**仅适用于 doubao-seed-rerank 模型** <br> * Content（可选）：待排序的文本内容，string <br> * Image（可选）：待排序的图片内容，interface{}（string 单张或 []string 多张），**仅适用于 doubao-seed-rerank 模型** <br> * 支持传入公开访问的 http/https 链接 <br> * 支持 jpeg、png、webp、bmp 格式的 base64 编码，单张图片小于 3 MB，请求体不能超过 4 MB <br> * Title（可选）：文档的标题 |
| RerankModel | *string | 否 | "base-multilingual-rerank" | **rerank 模型** <br> 可选模型： <br> *"doubao-seed-rerank"（即 doubao-seed-1.6-rerank）：字节自研多模态重排模型、支持文本 / 图片 / 视频 混合重排、精细语义匹配、可选阈值过滤与指令设置**（推荐）** <br>  <br> * "base-multilingual-rerank"：速度快、长文本、支持 70+ 种语言 <br> * "m3-v2-rerank"：常规文本、支持 100+ 种语言 |
| RerankInstruction | *string | 否 | -- | **重排指令** <br> **仅当 rerank_model=="doubao-seed-rerank" 时生效**，用于提供给模型一个明确的排序指令，提升重排效果。字符串长度不超过 1024 <br> *如，Whether the document answers the query or matches the content retrieval intent* |
## **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| Code | int | 状态码 |
| Message | string | 错误信息 |
| RequestID | string | 请求的唯一标识符 |
| Data | *RerankResult | RerankResult |
### **RerankResult**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| Scores | []float64 | float64 数组，与输入 Datas 数组一一对应，表示每个文档与 Query 的相关性得分 |
| TokenUsage | *int | 本次 rerank 调用消耗的总 token 数量 |
### **状态码说明**
| **状态码** | **http 状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 403 | VolcanoErrUnauthorized | 鉴权失败 |
| 1000002 | 400 | VolcanoErrInvalidRequest | 请求参数无效（当 query 缺失，或 datas 中所有文档都未提供任一媒体/文本内容时触发） |
| 300004 | 429 | VolcanoErrQuotaLimiter | 账户的 rerank 调用已达到配额限制 |
| 1000028 | 500 | VolcanoErrInternal | 服务内部错误，rerank模型过载 |
## 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Go SDK 中 Rerank 函数的基础使用方法，通过传入查询语句和待排序文本列表实现结果重排序，使用前需配置 AK/SK 鉴权参数。
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

    content1 := "VikingDB is a vector database."
    content2 := "The weather is good today."
    datas := []model.RerankDataItem{
        {
           Query:   "What is VikingDB?",
           Content: &content1,
        },
        {
           Query:   "What is VikingDB?",
           Content: &content2,
        },
    }

    resp, err := client.Rerank(ctx, model.RerankRequest{
       Datas:       datas,
       RerankModel: nil, // Use default or specify model
    })
    if err != nil {
       fmt.Printf("Rerank failed, err: %v\n", err)
       return
    }

    jsonData, _ := json.Marshal(resp)
    fmt.Printf("Response: %s\n", string(jsonData))
}
```


