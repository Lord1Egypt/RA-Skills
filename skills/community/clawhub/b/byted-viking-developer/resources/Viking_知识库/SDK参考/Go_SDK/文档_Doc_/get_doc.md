# 概述
get_doc 用于查看知识库下的文档信息。
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| CollectionName | string | 否 | -- | **知识库名称** |
| ProjectName | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在 default 项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| ResourceID | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 ResourceID，或同时传 CollectionName 和 ProjectName 作为知识库的唯一标识 |
| DocID | string | 是 | -- | **要查询的文档 id** |
| ReturnTokenUsage | bool | 否 | false | **是否返回文档向量化和文档生成摘要所消耗的 tokens** |
# **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| CollectionName | *string | 知识库名称 |
| DocName | *string | 文档名称 |
| DocHash | *string | 文档 hash |
| DocID | *string | 文档 id |
| AddType | *string | 导入方式 |
| DocType | *string | 文档类型 |
| Description | *string | 文档描述（当前仅支持图片文档） |
| CreateTime | *int64 | 文档创建时间 |
| AddedBy | *string | 添加人 |
| UpdateTime | *int64 | 文档更新时间 |
| URL | *string | 原始文档链接 |
| TOSPath | *string | tos 路径 |
| PointNum | *int | 切片数量 |
| Status | *DocStatus | DocStatus |
| Title | *string | 文档标题 |
| Source | *string | 知识来源（url，tos 等） |
| TotalTokens | interface{} | token 统计 |
| DocSummaryTokens | *int | 摘要 token 统计 |
| DocPremiumStatus | *DocPremiumStatus | DocPremiumStatus |
| DocSummary | *string | 文档摘要 |
| BriefSummary | *string | 简要摘要 |
| DocSize | *int | 文档大小 |
| Meta | *string | meta 信息 |
| Labels | map[string]string | 标签信息 |
| VideoOutline | map[string]interface{} | 视频大纲 |
| AudioOutline | map[string]interface{} | 音频大纲 |
| Statistics | map[string]interface{} | 统计信息 |
| Project | *string | 项目名 |
| ResourceID | *string | 知识库唯一 id |
### **DocStatus**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| ProcessStatus | *int | 处理状态 |
| FailedCode | *int | 失败错误码 |
| FailedMsg | *string | 失败错误信息 |
### **DocPremiumStatus**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| DocSummaryStatusCode | *int | 摘要状态码 |
## failed_code 报错码：
| **failed_code** | **错误描述** | **处理建议** |
| --- | --- | --- |
| 10001 | 文档下载超时 | 请上传重试。如果问题仍然存在，请联系我们 |
| 10003 | url 校验失败，请确认 url 链接 | 请确认 url 链接正确后重试。如果问题仍然存在，请联系我们 |
| 10005 | 飞书文档获取异常，请确认有效且授权 | 请确认飞书文档权限问题，通过飞书开放平台 OpenAPI [飞书开放平台](https://open.larkoffice.com/document/server-docs/docs/docs-overview)确认权限 |
| 30001 | 超过知识库文件限制大小 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 35001 | 超过知识库切片数量限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 35002 | FAQ 文档解析为空 | FAQ 文档解析结果为空，切片数为 0。请确保文档中包含有效数据 |
| 35004 | 超过知识库 FAQ 文档 sheet 数量限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 36003 | 结构化文档表头不匹配 | 结构化文档表头不匹配，请确保上传文档中每个 sheet 的表头与预定义的知识库表结构完全一致 |
| 36004 | 结构化文档数据类型转换失败 | 结构化文档数据类型转换失败，请确保上传文档中每个 sheet 的单元格的内容格式与预定义的知识库表结构数据类型完全一致 |
| 36005 | 超过知识库结构化文档 sheet 数量限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 36006 | 超过知识库结构化文档有效行数限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 36007 | 结构化文档解析为空 | 结构化文档解析结果为空，切片数为 0。请确保文档中包含有效数据 |
| 36008 | embedding 的列组合长度超出限制 | 缩短待 embedding 原始文本长度 |
| 其他错误码 | 未知错误，请联系我们 | 未知错误，请联系我们 |
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
本示例演示了知识库 Go SDK 中 GetDoc 的基础使用方法，通过指定知识库名称和文档 ID 实现单篇文档查询，使用前需配置 AK/SK 鉴权参数。
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

    docID := "your_doc_id"
    resp, err := collection.GetDoc(ctx, docID, true)
    if err != nil {
       fmt.Printf("GetDoc failed, err: %v\n", err)
       return
    }

    jsonData, _ := json.Marshal(resp)
    fmt.Printf("Response: %s\n", string(jsonData))
}
```


