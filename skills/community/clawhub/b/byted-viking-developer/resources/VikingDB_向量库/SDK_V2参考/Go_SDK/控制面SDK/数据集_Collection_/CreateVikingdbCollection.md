# 概述
接口用于对向量数据库的创建，单账号下最多创建200个数据集。
* 每一个 Collection 必须指定主键字段。
* 当定义字段 fields 添加了一个向量类型 vector 的字段后，再添加新的字段时，字段类型不可选择 vector 类型。因为目前只支持单向量，不可添加多个向量字段。
* 创建数据集时，请根据数据类型明确配置方式：若为已有向量数据，请填写 vector 字段；若需对多模态数据（如图文）进行向量化，请配置 vectorize 参数。二者为不同的数据处理逻辑，创建时仅可选择其一，不可同时使用。
* 一个 Collection 里的 fields 数量上限是 200个。

# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `CreateVikingdbCollection(input)` 方法发起集合创建请求，input 参数类型为 vikingdb.CreateVikingdbCollectionInput ，包含集合名称、描述、项目名称和字段定义等配置
# **请求参数**
下表仅列出该接口特有的请求参数和部分公共参数。更多信息请见[公共参数](https://www.volcengine.com/docs/6369/67268)。
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| ProjectName | string | 否 | 项目的名称。对应火山引擎“项目”（project）的概念。不填则默认当做default处理。 |
| CollectionName | String | 是 | 数据集的名称，对应 API 字段 `CollectionName` <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空 <br> * 长度（字节）要求：[1, 128] <br> * 同账号下，所有 Collection 名称不能重复 <br> * 同账号下， collection 数量不超过200个 |
| Description | string | 否 | 数据集的描述 <br> 最长 65535 字节 |
| Fields | []FieldForCreateVikingdbCollectionInput | 是 | 数据集中的字段。 <br> 限制：数据集内最多128个字段。 |
| Vectorize | VectorizeForCreateVikingdbCollectionInput | 否 | 数据集的向量化配置。 |

* FieldForCreateVikingdbCollectionInput 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| FieldName | string | 是 | 字段名。 <br> 限制：英文字母、数字、或下划线。且必须以英文字母开头。长度不超过64Byte。 |
| FieldType | FieldTypeEnum（枚举类型） | 是 | 字段类型。 |
| DefaultValue | interface{} | 否 | 字段内容默认值。 <br> 注意：vector/sparse_vector/text/image/video类型字段不支持默认值。 |
| Dim | Int | 否 | 若字段类型是vector，该参数指定稠密向量的维度。支持4-4096且为4的整数倍。 |
| IsPrimaryKey | bool | 否 | 是否为主键字段。可以为数据集指定1个主键字段（string或int64类型）。若没有指定，则使用自动生成的主键，字段名为"**__AUTO_ID__**"。 |

* VectorizeForCreateVikingdbCollectionInput 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| DenseVectors | DenseForCreateVikingdbCollectionInput | 是 | 稠密向量化模型配置 |
| SparseVectors | SparseForCreateVikingdbCollectionInput | 否 | 稀疏向量化模型配置 |

* DenseForCreateVikingdbCollectionInput 和 SparseForCreateVikingdbCollectionInput 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| ModelName | ModelNameEnum（枚举类型） | 是 | 模型名称。 <br> 枚举值见embedding模型列表。 |
| ModelVersion | string | 否 | 模型版本。若为doubao系模型，则必选模型版本。若为bge系模型，默认为default。 |
| Dim | int | 否 | 稠密向量维度。各模型支持的维度见embedding模型列表。 |
| TextField | string | 否 | 文本向量化字段名称。 |
| ImageField | string | 否 | 图片向量化字段名称。 |
| VideoField | string | 否 | 视频向量化字段名称。 |
# field_type 
| 字段类型 | 格式 | 可为主键 | 说明 |
| --- | --- | --- | --- |
| int64 | 整型数值 | 是 | 整数 <br>  <br> * 作为主键时，要求不能为0 |
| float32 | 浮点数值 | 否 | 浮点数 |
| string | 字符串 | 是 | 字符串 <br>  <br> * 推荐使用方式：当用于枚举值过滤时，推荐长度不超过128字节 <br> * 硬性限制：要求不超过65535字节；当作为主键时，需满足长度不超过256字节 |
| bool | true/false | 否 | 布尔类型 |
| []string | 字符串数组 | 否 | 字符串数组 <br>  <br> * 推荐使用方式：当用于枚举值过滤时，列表长度不超过32个，单元素不超过1024字节 <br> * 硬性限制：列表长度不超过20000，单元素不超过1024字节，总大小不超过1MB |
| []int64 | 整型数组 | 否 | 整数数组 <br>  <br> * 硬性限制：列表长度不超过1024 |
| Vector | * 向量（浮点数数组） <br> * float32/float64压缩为bytes后的base64编码 | 否 | 稠密向量 <br>  <br> * 硬性限制：长度不小于4，不大于4096，且为4的整数倍数。 |
| SparseVector <br>  |  输入格式<token_id ,token_weight>的字典列表，来表征稀疏稀疏向量的非零位下标及其对应的值, 其中 token_id 是 string 类型, token_weight 是float 类型 | 否 | 稀疏向量 <br>  |
| Text | string | 否 | 若为向量化字段，则值不能为空。（若否，可以为空） <br>  <br> * 若为向量化字段，则值不能为空。（若否，可以为空） <br> * 硬性限制：需小于65535字节 |
| Image | string | 否 | 若为向量化字段，则值不能为空。（若否，可以为空） <br>  <br> * 图片tos链接 `tos://{bucket}/{object}` <br> * http/https格式链接 <br> * 对应图片需满足宽高长度大于14px，像素小于3600万 <br> * 可参考：[多模态向量化](https://www.volcengine.com/docs/82379/1409291?lang=zh#a256838b) |
| Video | map[string]interface{} | 否 | 若为向量化字段，则值不能为空。（若否，可以为空） <br>  <br> * 视频tos链接 `tos://{bucket}/{object}` <br> * http/https格式url链接 <br> * 对应视频需满足大小不超过50mb <br> * 可参考：[多模态向量化](https://www.volcengine.com/docs/82379/1409291?lang=zh#a256838b) <br>  <br> ```Plain Text <br> { <br>     "value": tos://{bucket}/{object}     # 或http/https格式url链接，该字段必填 <br>     "fps": 0.2     # 取值0.2-5，选填 <br> } <br> ``` <br>  |
| date_time | string | 否 | 分钟级别： <br> `yyyy-MM-ddTHH:mmZ`或`yyyy-MM-ddTHH:mm±HH:mm` <br> 秒级别： <br> `yyyy-MM-ddTHH:mm:ssZ`或`yyyy-MM-ddTHH:mm:ss±HH:mm` <br> 毫秒级别： <br> `yyyy-MM-ddTHH:mm:ss.SSSZ`或`yyyy-MM-ddTHH:mm:ss.SSS±HH:mm` <br> 例如："2025-08-12T11:33:56+08:00" |
| geo_point | string | 否 | 地理坐标`longitude,latitude`，其中`longitude`取值(-180,180)，`latitude`取值(-90,90) <br> 例如："116.408108,39.915023" |
## 模型列表
| 模型名称 | 模型版本 | 支持向量化类型 | 默认稠密向量维度 | 可选稠密向量维度 | 文本截断长度 | 支持稀疏向量 |  可支持instruction <br>  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bge-large-zh | (default) | text | 1024 | 1024 | 512 | 否 | 是 |
| bge-m3 | (default) | text | 1024 | 1024 | 8192 | 是 | 否 |
| bge-visualized-m3 <br>  | (default) | text、image及其组合 | 1024 | 1024 | 8192 | 否 | 否 |
| doubao-embedding | *240715* | text | 2048 <br>  | 512, 1024, 2048 | 4096 | 否 | 是 <br>  |
| doubao-embedding-large | *240915* | text | 2048 | 512, 1024, 2048, 4096 | 4096 | 否 | 是 |
| doubao-embedding-vision | *250328* | text、image及其组合 | 2048 | 2048, 1024 <br>  | 8192 | 否 | 是 |
| doubao-embedding-vision | *250615* | 兼容*241215*和*250328*的用法*。​*另外，支持full_modal_seq（文/图/视频序列） | 2048 <br>  | 2048, 1024 <br>  | 128k | 否 | 是 |
# **返回参数**
下表仅列出本接口特有的返回参数。更多信息请参见[返回结构](https://www.volcengine.com/docs/6369/80336)。
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| Message | String | 有关请求状态的消息。 |
| ResourceId | String | 新数据集的ID。 |

# 请求示例
### 创建带vector字段的数据集
```Python
package main

import (
    "fmt"
    "os"

    "github.com/volcengine/volcengine-go-sdk/service/vikingdb"
    "github.com/volcengine/volcengine-go-sdk/volcengine"
    "github.com/volcengine/volcengine-go-sdk/volcengine/credentials"
    "github.com/volcengine/volcengine-go-sdk/volcengine/session"
)

func main() {
    var (
       accessKey = os.Getenv("VIKINGDB_AK")
       secretKey = os.Getenv("VIKINGDB_SK")
       region    = "cn-beijing"
    )
    config := volcengine.NewConfig().
       WithRegion(region).
       WithCredentials(credentials.NewStaticCredentials(accessKey, secretKey, ""))

    sess, err := session.NewSession(config)
    if err != nil {
       panic(err)
    }
    svc := vikingdb.New(sess)

    input := vikingdb.CreateVikingdbCollectionInput{
       CollectionName: volcengine.String("Your Collection Name"),
       Description:    volcengine.String("Your Collection Description"),
       ProjectName:    volcengine.String("default"),
       Fields: []*vikingdb.FieldForCreateVikingdbCollectionInput{
          {
             FieldName:    volcengine.String("item_id"),
             FieldType:    volcengine.String("int64"),
             IsPrimaryKey: volcengine.Bool(true),
          },
          {
             FieldName: volcengine.String("title"),
             FieldType: volcengine.String("string"),
          },
          {
             FieldName: volcengine.String("content"),
             FieldType: volcengine.String("text"),
          },
          {
             FieldName:    volcengine.String("f_int64"),
             FieldType:    volcengine.String("int64"),
             DefaultValue: 123456,
          },
       },
       Vectorize: &vikingdb.VectorizeForCreateVikingdbCollectionInput{
          Dense: &vikingdb.DenseForCreateVikingdbCollectionInput{
             ModelName: volcengine.String("bge-m3"),
             TextField: volcengine.String("content"),
          },
          Sparse: &vikingdb.SparseForCreateVikingdbCollectionInput{
             ModelName: volcengine.String("bge-m3"),
             TextField: volcengine.String("content"),
          },
       },
    }

    resp, err := svc.CreateVikingdbCollection(&input)
    if err != nil {
       panic(err)
    }

    fmt.Println(resp.Message)
    fmt.Println(resp.ResourceId)
}
```


### 创建带vectorize(向量化)的数据集
```Go
package main

import (
    "fmt"
    "os"

    "github.com/volcengine/volcengine-go-sdk/service/vikingdb"
    "github.com/volcengine/volcengine-go-sdk/volcengine"
    "github.com/volcengine/volcengine-go-sdk/volcengine/credentials"
    "github.com/volcengine/volcengine-go-sdk/volcengine/session"
)

func main() {
    var (
       accessKey = os.Getenv("VIKINGDB_AK")
       secretKey = os.Getenv("VIKINGDB_SK")
       region    = "cn-beijing"
    )
    config := volcengine.NewConfig().
       WithRegion(region).
       WithCredentials(credentials.NewStaticCredentials(accessKey, secretKey, ""))

    sess, err := session.NewSession(config)
    if err != nil {
       panic(err)
    }
    svc := vikingdb.New(sess)

    input := vikingdb.CreateVikingdbCollectionInput{
       CollectionName: volcengine.String("Your Collection Name"),
       Description:    volcengine.String("Your Collection Description"),
       ProjectName:    volcengine.String("default"),
       Fields: []*vikingdb.FieldForCreateVikingdbCollectionInput{
          {
             FieldName:    volcengine.String("item_id"),
             FieldType:    volcengine.String("int64"),
             IsPrimaryKey: volcengine.Bool(true),
          },
          {
             FieldName: volcengine.String("title"),
             FieldType: volcengine.String("string"),
          },
          {
             FieldName: volcengine.String("dense_vector"),
             FieldType: volcengine.String("vector"),
             Dim:       volcengine.Int32(768),
          },
          {
             FieldName: volcengine.String("sparse_vector"),
             FieldType: volcengine.String("sparse_vector"),
          },
          {
             FieldName:    volcengine.String("f_int64"),
             FieldType:    volcengine.String("int64"),
             DefaultValue: 123456,
          },
       },
    }

    resp, err := svc.CreateVikingdbCollection(&input)
    if err != nil {
       panic(err)
    }

    fmt.Println(resp.Message)
    fmt.Println(resp.ResourceId)
}
```


