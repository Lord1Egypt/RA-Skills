# 概述
list_points 用于查看知识库下的切片列表，默认按照 point_id 从小到大排序
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| CollectionName | string | 否 | -- | **知识库名称** |
| ProjectName | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| ResourceID | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 ResourceID，或同时传 CollectionName 和 ProjectName 作为知识库的唯一标识 |
| Offset | int | 否 | 0 | **用于分页** <br> 表示从结果的第几个后开始取，需要大于等于 0 |
| Limit | int | 否 | -1 | **返回切片个数** <br> -1 表示获取所有，最大值不超过 100，每次返回最多不超过 100 |
| DocIDs | []string | 否 | -- | **按文档 id 筛选** <br> 指定文档返回对应切片列表，不传或为 null 表示不筛选，传入的 size 为 0 将返回空结果。限制 list 长度，最大长度为 100 |
| PointIDs | []string | 否 | -- | **按照切片 id 筛选** <br> 指定一个或多个切片 id 返回对应切片内容，不传或为 null 表示不筛选，传入的 size 为 0 将返回空结果。限制切片id 最大长度为 100 |
| GetAttachmentLink | *bool | 否 | False | **是否获取切片中图片的临时下载链接** <br> 10 分钟有效期 |
# **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| Code | int | 状态码 |
| Message | string | 返回信息 |
| RequestID | string | 标识每个请求的唯一标识符 |
| Data | *ListPointsResult | ListPointsResult |
| Count | *int | 本次返回的结果数量 |
| TotalNum | *int | 总共有多少个结果 |
### **ListPointsResult**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| PointList | []PointInfo | 切片信息列表 |
### **PointInfo**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| CollectionName | *string | 知识库名称 |
| PointID | *string | 切片 id（知识库下唯一） |
| DocInfo | *PointDocInfo | PointDocInfo |
| ProcessTime | *int64 | 切片处理完成的时间 |
| OriginText | *string | 原始文本 |
| MDContent | *string | 切片 markdown 解析结果，保留更多的原始表格信息（chunk_type 为 table 时会返回） |
| HTMLContent | *string | 切片 html 解析结果，保留更多的原始表格信息（chunk_type 为 table 时会返回） |
| ChunkTitle | *string | 切片标题，是由解析模型识别出来的上一层级的标题。若没有上一层级标题则为空 |
| ChunkType | *string | 切片所属类型 |
| Description | *string | 文档描述（当前仅支持图片文档） |
| Content | *string | 切片内容 |
| ChunkID | *int64 | 切片位次 id，代表在原始文档中的位次顺序 |
| OriginalQuestion | *string | faq 数据检索召回答案对应的原始问题 |
| TableChunkFields | []PointTableChunkField | 结构化数据检索返回单行全量数据 |
| ChunkAttachment | []ChunkAttachment | 附件信息（GetAttachmentLink 为 true 时返回临时链接，10 分钟有效期） |
| RerankScore | *float64 | 重排得分 |
| Score | *float64 | 检索得分 |
| UpdateTime | *int64 | 更新时间 |
| ChunkSource | *string | 切片来源 |
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
| UUID | *string | 附件 uuid |
| Caption | *string | 附件说明 |
| Type | *string | 附件类型 |
| Link | *string | 附件链接 |
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
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection不存在 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Go SDK 中 ListPoints 函数的基础使用方法，通过指定知识库名称查询切片列表，使用前需配置 AK/SK 鉴权参数。
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

    resp, err := collection.ListPoints(ctx, model.ListPointsRequest{
       Offset: 0,
       Limit:  10,
       //DocIDs: []string{"your_doc_id"},
    })
    if err != nil {
       fmt.Printf("ListPoints failed, err: %v\n", err)
       return
    }

    jsonData, _ := json.Marshal(resp)
    fmt.Printf("Response: %s\n", string(jsonData))
}
```


