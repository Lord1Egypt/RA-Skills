# 概述
search_knowledge 用于对知识库进行检索和前后处理，当前会默认对原始文本加工后的知识内容进行检索。
# **请求参数**
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| CollectionName | -- | string | 否 | -- | **知识库名称** |
| ProjectName | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| ResourceID | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 ResourceID，或同时传 CollectionName 和 ProjectName 作为知识库的唯一标识 |
| Query | -- | string | 是 | -- | **检索文本** <br>  <br> * 最大可输入长度为 8000，query 长度 > 8000 时，接口报错 <br> * 所选 embedding 模型输入最大长度 < query 长度 < 8000 时，query 按所选模型自动截断 <br> * query 长度 < 所选 embedding 模型输入最大长度时，正常检索返回目标切片 |
| ImageQuery | -- | string | 否 | -- | **检索图片** <br> 支持图片 URL 或 Base64 编码，详细要求见[图片像素说明](https://www.volcengine.com/docs/82379/1409291?lang=zh#7a10f532)和[图片文件格式](https://www.volcengine.com/docs/82379/1409291?lang=zh#5c068efa) <br>  <br> * 图片 URL 传入：适用于图片文件已存在公网可访问 URL 的场景，单张图片小于 10 MB <br> * Base64 编码传入：适用于图片文件较小的场景，支持 **JPEG、PNG、WebP、BMP** 四种格式的 Base64 编码，单张图片小于 3 MB，请求体不能超过 4 MB |
| Limit | -- | int | 否 | 10 | **检索结果数量** <br>  <br> * 数量要求：[1, 1000] |
| QueryParam |  | map[string]interface{} | 否 |  | **检索的过滤和返回设置** |
|  | doc_filter | map | 否 | -- | **检索过滤条件** <br>  <br> * 支持对 doc 的 meta 信息过滤 <br> * 详细使用方式和支持字段见[filter表达式](https://www.volcengine.com/docs/84313/1419289#filter-%E8%A1%A8%E8%BE%BE%E5%BC%8F)，可支持对 doc_id 做筛选 <br> * 此处用过过滤的字段，需要在 collection/create 时添加到 index_config 的 fields 上 <br>  <br> 例如： <br> 单层 filter： <br> ```json <br> doc_filter = { <br>      "op": "must", // 查询算子 must/must_not/range/range_out <br>      "field": "doc_id", <br>      "conds": ["tos_doc_id_123", "tos_doc_id_456"] <br>  } <br>  query_param = { <br>      "doc_filter": doc_filter <br>  } <br> ``` <br>  <br> 多层 filter： <br> ```json <br> doc_filter = { <br>    "op": "and",   // 逻辑算子 and/or <br>    "conds": [     // 条件列表，支持嵌套逻辑算子和查询算子 <br>      { <br>        "op": "must", <br>        "field": "type", <br>        "conds": [1] <br>      }, <br>      { <br>          ...         // 支持>=1的任意数量的条件进行组合 <br>      } <br>    ] <br>  } <br>  <br>  query_param = { <br>      "doc_filter": doc_filter <br>  } <br> ``` <br>  |
| DenseWeight | -- | float32 | 否 | 0.5 | **混合检索中稠密向量的权重** <br>  <br> * 1 表示纯稠密检索 ，0 表示纯字面检索，范围 [0.2, 1] <br> * 只有在请求的知识库使用的是混合检索时有效，即索引算法为 hnsw_hybrid |
| PreProcessing |  | map[string]interface{} |  |  | **检索预处理** |
|  | need_instruction | bool | 否 | False | **是否拼接 instruction 进行检索** |
|  | return_token_usage | bool | 否 | False | **是否返回 search 流程中各阶段的 token 使用量** |
|  | rewrite | bool | 否 | False | **是否对 query 进行改写** <br> 根据 messages 字段传入的历史对话信息进行改写，最多 3 轮 <br> **注：​**只有在messages字段长度大于2且不为空时，设置参数值为True，才能返回有效的rewrite_query； <br> ```json <br> "messages"：[ <br>      {"role": "user", "content": "prompt 1"}, <br>      {"role": "assistant", "content": "prompt2"}, <br>      {"role": "user", "content": "prompt 3"}, <br>  ] <br> ``` <br>  |
|  | messages | json | 是 | -- | **多轮对话信息** <br> 仅**开启改写**时需要上传，可根据历史对话内容进行问题改写，注意上传对话轮数需 >= 1 <br> 发出消息的对话参与者角色，可选值包括： <br>  <br> * user：User Message 用户消息 <br> * assistant：Assistant Message 对话助手消息 <br>  <br> ```json <br> [ <br>      {"role": "user", "content": "知识库支持哪些文档格式？"}, <br>      {"role": "assistant", "content": "知识库支持结构化和非结构化文档，其中结构化文档支持 excel、csv、jsonl 等常见格式，非结构化文档支持 pdf、docx、ppt 等常见格式。"}, <br>      {"role": "user", "content": "那大小呢？"}, <br>  ] <br> ``` <br>  |
| PostProcessing |  | map[string]interface{} |  |  | **检索后处理** |
|  | rerank_switch | bool | 否 | False | **自动对结果做 rerank** <br> 打开后，会自动请求 rerank 模型排序 |
|  | retrieve_count | int | 否 | 25 | **进入重排的切片数量，默认为 25** <br> 只有在 rerank_switch 为 True 时生效。retrieve_count 需要大于等于 limit，否则会抛出错误 |
|  | chunk_diffusion_count | int | 否 | 0 | **检索阶段返回命中切片的上下几片邻近切片** <br> 默认为 0，表示不进行 chunk diffusion。范围 [0, 5] |
|  | chunk_group | bool | 否 | False | **文本聚合** <br> 默认不聚合，对于非结构化文件，考虑到原始文档内容语序对大模型的理解，可开启文本聚合。开启后，会根据文档及文档顺序，对切片进行重新聚合排序返回 |
|  | rerank_model | string | 否 | "base-multilingual-rerank" | **rerank 模型选择** <br> 仅在 "rerank_switch" == True 的时候生效 <br> 可选模型： <br>  <br> * "doubao-seed-rerank"（即 doubao-seed-1.6-rerank）：字节自研多模态重排模型、支持文本 / 图片 / 视频混合重排、精细语义匹配、可选阈值过滤与指令设置 <br> * "base-multilingual-rerank"：速度快、长文本、支持70+种语言 <br> * "m3-v2-rerank"：常规文本、支持100+种语言 |
|  | rerank_threshold | float | 否 | -- | **阈值过滤** <br> **仅当 rerank_model=="doubao-seed-rerank" 时生效**，用于设置重排分数的过滤阈值，低于阈值的结果将不会被返回，取值范围为 0 到 1 |
|  | rerank_instruction | string | 否 | -- | **rerank 指令** <br> **仅在 "rerank_switch" == True 且 "rerank_model" == "doubao-seed-rerank" 时生效**，用于提供给模型一个明确的排序指令，提升重排效果。字符串长度不超过 1024 <br> *如，Whether the document answers the query or matches the content retrieval intent* |
|  | rerank_only_chunk | bool | 否 | False | **是否仅根据 chunk 内容计算重排分数** <br> 可选值： <br>  <br> * True： 只根据 chunk 内容计算分 <br> * False：根据 chunk title + 内容 一起计算排序分 |
|  | get_attachment_link | bool | 否 | False | **是否获取切片中图片的临时下载链接** |
# **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| Code | int | 状态码 |
| Message | string | 返回信息 |
| RequestID | string | 标识每个请求的唯一标识符 |
| Data | *SearchKnowledgeResult | SearchKnowledgeResult |
### **SearchKnowledgeResult**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| Count | *int | 检索结果返回的条数 |
| RewriteQuery | *string | query 改写的结果 |
| TokenUsage | map[string]interface{} | Token 使用信息 |
| ResultList | []PointInfo | 检索召回切片信息列表 |
### **PointInfo**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| CollectionName | *string | 知识库名称 |
| PointID | *string | 切片 id（知识库下唯一） |
| ProcessTime | *int64 | 切片处理完成的时间 |
| OriginText | *string | 原始文本 |
| MDContent | *string | 切片 markdown 解析结果，保留更多的原始表格信息（chunk_type 为 table 时会返回） |
| HTMLContent | *string | 切片 html 解析结果，保留更多的原始表格信息（chunk_type 为 table 时会返回） |
| ChunkTitle | *string | 切片标题，是由解析模型识别出来的上一层级的标题。若没有上一层级标题则为空 |
| ChunkType | *string | 切片所属类型 |
| Description | *string | 文档描述（当前仅支持图片文档） |
| Content | *string | 切片内容 <br> 1、非结构化文件：Content 返回切片内容 <br> 2、faq 文件：Content 返回答案 <br> 3、结构化文件：Content 返回参与索引的字段和取值，以 K:V 对拼接，使用 \n 区隔 |
| ChunkID | *int64 | 切片位次 id，代表在原始文档中的位次顺序 |
| OriginalQuestion | *string | faq 数据检索召回答案对应的原始问题 |
| DocInfo | *PointDocInfo | PointDocInfo |
| RerankScore | *float64 | 重排得分 |
| Score | *float64 | 检索得分 |
| ChunkSource | *string | 切片来源 |
| ChunkAttachment | []ChunkAttachment | 临时下载链接，有效期 10 分钟 |
| TableChunkFields | []PointTableChunkField | 结构化数据检索返回单行全量数据 |
| UpdateTime | *int64 | 更新时间 |
| ChunkStatus | *string | 切片状态 |
| VideoFrame | *string | 视频帧 |
| VideoURL | *string | 视频链接 |
| VideoStartTime | *int64 | 视频切片的起始时间（ms） |
| VideoEndTime | *int64 | 视频切片的结束时间（ms） |
| VideoOutline | map[string]interface{} | 视频大纲 |
| AudioStartTime | *int64 | 音频切片的起始时间（ms） |
| AudioEndTime | *int64 | 音频切片的结束时间（ms） |
| AudioOutline | map[string]interface{} | 音频大纲 |
| SheetName | *string | sheet 名称 |
| Project | *string | 项目名 |
| ResourceID | *string | 知识库唯一 id |
### **PointDocInfo**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| DocID | *string | 所属文档 id |
| DocName | *string | 所属文档名字 |
| CreateTime | *int64 | 文档创建时间 |
| DocType | *string | 所属原始文档类型 |
| DocMeta | *string | 所属文档的 meta 信息 |
| Source | *string | 所属文档知识来源（url，tos 等） |
| Title | *string | 所属文档标题 |
| Status | *DocStatus | DocStatus |
### **DocStatus**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| ProcessStatus | *int | 处理状态 |
| FailedCode | *int | 失败错误码 |
| FailedMsg | *string | 失败错误信息 |
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
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 缺乏鉴权信息 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection 不存在 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Go SDK 中 SearchKnowledge 的基础使用方法，通过指定数据集名称和查询语句实现知识库检索，使用前需配置 AK/SK 鉴权参数。
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

    limit := 10
    denseWeight := 0.5
    
    resp, err := collection.SearchKnowledge(ctx, model.SearchKnowledgeRequest{
        Query:       "your query",
        Limit:       &limit,
        DenseWeight: &denseWeight,
    })
    if err != nil {
        fmt.Printf("SearchKnowledge failed, err: %v\n", err)
        return
    }

    jsonData, _ := json.Marshal(resp)
    fmt.Printf("Response: %s\n", string(jsonData))
}
```


