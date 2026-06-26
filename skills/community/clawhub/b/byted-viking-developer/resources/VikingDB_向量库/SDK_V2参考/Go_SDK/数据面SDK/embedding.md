# 概述
Embedding 接口用于将文本、图片、音视频等非结构化内容转为可检索的特征向量，支持同时输出稠密与稀疏向量。
* 当前 Embedding 服务主要面向文本，部分模型支持多模态输入（文/图/视频）。
* 接口暂不承载高并发请求，请求过载时可能被丢弃。

# 请求体参数
| 参数 | 类型 | 是否必选 | 子参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| DenseModel | EmbeddingModelOpt | 二者至少选 1 | Name | string | 是 | 模型名称。 |
|  |  |  | Version | string | 否（豆包模型必填） | 模型版本。 |
|  |  |  | Dim | int | 否 | 稠密向量维度，缺省时使用模型默认值。 |
| SparseModel | EmbeddingModelOpt |  | Name | string | 是 | 模型名称。 |
|  |  |  | Version | string | 否 | 模型版本。 |
|  |  |  | Dim | int | 否 | 稀疏向量的输出维度。 |
| Data | []EmbeddingData | 是 | Text | string | 二选一 | 纯文本内容。 |
|  |  |  | Image | interface{} | 二选一 | 图片或图片 URL，遵循 MediaData 规范。 |
|  |  |  | Video | interface{} | 二选一 | 视频 URL 或配置对象，可附带 `fps`、`value` 等抽帧参数。 |
|  |  |  | FullModalSeq | interface{} | 否 | 多模态序列输入。每个元素可再设置 `text`/`image`/`video` 字段。 |
| ProjectName | string | 否 |  |  |  | 租户项目名称，便于区分不同环境。 |
媒体字段说明：
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| Text | string | UTF-8 编码的纯文本。 |
| Image | interface{} | 可直接填写图片 URL，或按照 MediaData 规范提供带鉴权参数的对象。 |
| Video | map[string]interface{} | 支持 `value`（视频 URL）和 `fps`（抽帧频率，默认 1，范围 0.2-5.0，最少 16 帧）。 |
## 模型列表
| 模型名称 | 模型版本 | 支持向量化类型 | 默认稠密向量维度 | 可选稠密向量维度 | 文本截断长度 | 支持稀疏向量 | 可支持instruction <br>  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bge-large-zh | (default) | text | 1024 | 1024 | 512 | 否 | 是 |
| bge-m3 | (default) | text | 1024 | 1024 | 8192 | 是 | 否 |
| bge-visualized-m3 <br>  | (default) | text、image及其组合 | 1024 | 1024 | 8192 | 否 | 否 |
| doubao-embedding | *240715* | text | 2048 <br>  | 512, 1024, 2048 | 4096 | 否 | 是 <br>  |
| doubao-embedding-large | *240915* | text | 2048 | 512, 1024, 2048, 4096 | 4096 | 否 | 是 |
| doubao-embedding-vision | *250328* | text、image及其组合 | 2048 | 2048, 1024 <br>  | 8192 | 否 | 是 |
| doubao-embedding-vision | *250615* | 兼容*241215*和*250328*的用法*。​*另外，支持full_modal_seq（文/图/视频序列） | 2048 <br>  | 2048, 1024 <br>  | 128k | 否 | 是 |
# 返回参数
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| RequestID | string | 请求链路 ID。 |
| Code | string | 错误码。 |
| Message | string | 错误信息。 |
| Api | string | API 名称。 |
| Result | EmbeddingResult | 向量化结果，失败时为 `None`。 |
EmbeddingResult 结构：
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| Data | []Embedding | 与请求顺序对应的向量结果列表。 |
| TokenUsage | map[string]interface{} | 按模型统计的 token 使用量，包含 `prompt_tokens`、`completion_tokens`、`image_tokens`、`total_tokens` 等字段。 |
Embedding 结构：
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| DenseVectors | []float32 | 稠密向量。 |
| SparseVectors | map[string]float32 | 稀疏向量（键为 token，值为权重）。 |
# 示例
```Go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "github.com/volcengine/vikingdb-go-sdk/vector"
    "github.com/volcengine/vikingdb-go-sdk/vector/model"
    "os"
    "time"
)

func valuePtr[T any](v T) *T {
    return &v
}

func main() {
    var (
       accessKey = os.Getenv("VIKINGDB_AK")
       secretKey = os.Getenv("VIKINGDB_SK")
       endpoint  = "https://api-vikingdb.vikingdb.cn-beijing.volces.com"
       region    = "cn-beijing"
    )

    client, err := vector.New(
       vector.AuthIAM(accessKey, secretKey), // IAM auth
       vector.WithEndpoint(endpoint),
       vector.WithRegion(region),
       vector.WithTimeout(time.Second*30),
       vector.WithMaxRetries(3),
    )
    if err != nil {
       fmt.Println("New client failed, err: ", err)
       panic(err)
    }
    ctx := context.Background()

    var (
       text = "vikingdb is a vector database"
    )

    resp, err := client.Embedding().Embedding(ctx, model.EmbeddingRequest{
       DenseModel: &model.EmbeddingModelOpt{
          ModelName:    valuePtr("doubao-embedding"),
          ModelVersion: valuePtr("240715"),
          Dim:          valuePtr(2048),
       },
       SparseModel: &model.EmbeddingModelOpt{
          ModelName:    valuePtr("bge-m3"),
          ModelVersion: valuePtr("default"),
          Dim:          valuePtr(1024),
       },
       Data: []*model.EmbeddingData{
          {
             Text: &text,
          },
       },
    })

    if err != nil {
       fmt.Println("Embedding failed, err: ", err)
       panic(err)
    }

    jsonData, err := json.Marshal(resp.Result)
    if err != nil {
       fmt.Println("Marshal result failed, err: ", err)
       panic(err)
    }
    fmt.Println(string(jsonData))
}
```

