# 概述
add_doc_v2 用于向已创建的知识库添加文档。
# **请求参数**
| **参数** | **类型** | **是否必传** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| CollectionName | string | 否 | -- | 知识库名称 |
| ProjectName | string | 否 | default | 知识库所属项目，获取方式参考文档 [API 接入与技术支持](https://www.volcengine.com/docs/84313/1606319?lang=zh#1ab381b9) <br> 若需要操作指定项目下的知识库，需正确配置该字段 |
| ResourceID | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 ResourceID，或同时传 CollectionName 和 ProjectName 作为知识库的唯一标识 |
| DocID | *string | 是 | -- | **知识库下的文档唯一标识** <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母或下划线开头，不能为空 <br> * 长度要求：[1, 128] |
| DocName | *string | 否 | -- | **文档名称** <br>  <br> * 对于 tos 导入的方式，未传入时直接使用 tos path 下面的文档名 <br> * 对于 url 导入的方式，先通过 url 提取带后缀的文档名，如果没有则返回错误码 400，要求用户再传 DocName <br>  <br> 格式要求： <br>  <br> * 不能包含有特殊用途的字符(< > : " / \ <br> * 长度要求：[1, 255] |
| DocType | *string | 否 | -- | **上传文档的类型** <br>  <br> * 非结构化文档支持类型：txt, doc, docx, pdf, markdown, pptx, ppt, jpeg, png, webp, bmp, mp4, mp3, wav, aac, flac, ogg <br> * .jpg 和 .jpeg 文件 DocType 均为 jpeg <br> * .markdown 和 .md 文件 DocType 均为 markdown <br> * 结构化文档支持类型：xlsx, csv, jsonl <br>  <br> 优先使用传入的值；若未传入，将尝试自动提取；若自动提取失败，则接口返回错误 |
| Description | *string | 否 | -- | **文档描述** <br> 描述会参与对图片的检索，如电商场景下，描述可以用于存放图片对应的详细商品说明，售卖亮点，价格等 <br> 注： <br>  <br> * 暂**只在** DocType 为**图片类型文档时支持**，其他类型文档设置无效。 <br> * 长度 [0，4000] |
| TagList | []model.MetaItem | 否 | -- | Tag 为结构体，包含 <br>  <br> * FieldName：标签名，类型为 string <br> * 不能为 "doc_id" <br> * 需对齐创建知识库时的 FieldName <br> * 在创建知识库时先初始化标签索引，再在上传文档时打标，以用于检索时实现标签过滤能力 <br> * 若需新增过滤标签，请先编辑知识库新增标签后，再进行文档打标 <br> * FieldType：标签类型 <br> * 支持 "int64"，"float32"，"string"，"bool"，"list"，"list" ，"date_time"，"geo_point" 类型 <br> * 需对齐创建知识库时的 FieldType <br> * FieldValue：标签值 <br> * 与 FieldType 指定类型一致 |
| URI | *string | 是 | -- | 待上传的文件 uri 链接，示例： <br>  <br> * http://a/b/c.pdf <br> * tos://a/b/c.pdf |
# **响应消息**
| **参数** | **类型** | **参数说明** | **备注** |
| --- | --- | --- | --- |
| Code | int | 状态码 |  |
| Message | string | 返回信息 |  |
| RequestID | string | 标识每个请求的唯一标识符 |  |
| Data | *AddDocResponseData | AddDocResponseData |  |
### **AddDocResponseData**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| CollectionName | *string | 知识库的名字 |
| ResourceID | *string | 知识库唯一标识 |
| Project | *string | 项目名 |
| DocID | *string | 文档唯一标识 |
| TaskID | *int64 | 任务 id |
| DedupInfo | *DedupInfo | DedupInfo |
| MoreInfo | *string | 更多信息 |
### **DedupInfo**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| Skip | *bool | 是否跳过（去重命中） |
| SameDocIDs | []string | 重复的文档 id 列表 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection 不存在 |
| 1001002 | 400 | invalid request: doc_id:xxx is duplicated with doc_ids:xxx | 文档内容与现有文档重复 |
| 1001010 | 400 | doc num is exceed 3000000 | doc 数量已达限额，点击详情查看[知识库配额限制](https://www.volcengine.com/docs/84313/1339026) |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Go SDK 中 AddDocV2 函数的基础使用方法，使用前需配置 AK/SK 鉴权参数。
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
       CollectionName: os.Getenv("VIKING_COLLECTION_NAME"),
       ProjectName:    os.Getenv("VIKING_PROJECT"),
    })

    docId := "your_doc_id"
    docName := "your_doc_name"
    docType := "doc"
    uri := "your_doc_link_url"

    resp, err := collection.AddDocV2(ctx, model.AddDocV2Request{
       DocID:   &docId,
       DocName: &docName,
       DocType: &docType,
       URI:     &uri,
       TagList: []model.MetaItem{
          {
             FieldName:  func() *string { s := "category"; return &s }(),
             FieldType:  func() *string { s := "string"; return &s }(),
             FieldValue: "financial_report",
          },
       },
    })
    if err != nil {
       fmt.Printf("AddDocV2 failed, err: %v\n", err)
       return
    }

    jsonData, _ := json.Marshal(resp)
    fmt.Printf("Response: %s\n", string(jsonData))
}
```


