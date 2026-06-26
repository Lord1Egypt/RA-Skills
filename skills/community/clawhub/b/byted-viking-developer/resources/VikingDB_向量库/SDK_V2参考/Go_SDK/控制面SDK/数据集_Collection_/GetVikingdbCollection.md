# 概述
GetVikingdbCollection 接口用于查询指定 Collection 的元信息、字段配置以及向量化设置。
# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `GetVikingdbCollection(input)` 方法发起集合创建请求，input 参数类型为 `vikingdb.GetVikingdbCollectionInput` ，包含集合名称、描述、项目名称和字段定义等配置
# **请求参数**
| **参数** | **类型** | **是否必选** | **参数说明** |
| --- | --- | --- | --- |
| ProjectName | string | 否 | 项目名称，对应 API 字段 `ProjectName`，默认值为 default。 |
| CollectionName | string | 2选1 | 集合名称，对应 API 字段 `CollectionName`。需以字母开头，只能包含字母/数字/下划线，长度 1-128。 |
| ResourceId | string |  | 集合资源 ID，对应 API 字段 `ResourceId`。可与 `CollectionName` 二选一或同时传递以保证精确定位。 |
# 返回参数
成功响应返回 `GetVikingdbCollectionResponse`，包含如下字段：
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| ProjectName | string | 集合所属项目，对应 API 字段 `ProjectName`。 |
| ResourceId | string | 集合资源 ID，对应 API 字段 `ResourceId`。 |
| CollectionName | string | 集合名称，对应 API 字段 `CollectionName`。 |
| Description | string | 集合描述，对应 API 字段 `Description`。 |
| CreateTime | string | 创建时间 (RFC3339)，对应 API 字段 `CreateTime`。 |
| UpdateTime | string | 最后更新时间，对应 API 字段 `UpdateTime`。 |
| UpdatePerson | string | 最近操作人，对应 API 字段 `UpdatePerson`。 |
| EnableKeywordsSearch | bool | 是否开启关键词检索，对应 API 字段 `EnableKeywordsSearch`。 |
| IndexCount | int | 集合下索引数量，对应 API 字段 `IndexCount`。 |
| IndexNames | []string | 索引名称列表，对应 API 字段 `IndexNames`。 |
| Fields | []FieldForGetVikingdbCollectionOutput | 字段定义列表，对应 API 字段 `Fields`。 |
| CollectionStats | CollectionStatsForGetVikingdbCollectionOutput | 数据量统计，对应 API 字段 `CollectionStats`。 |
| Vectorize | VectorizeForGetVikingdbCollectionOutput | 向量化配置，对应 API 字段 `Vectorize`。 |

* FieldForGetVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| FieldName | string | 字段名称，对应 API 字段 `FieldName`。 |
| FieldType | string | 字段类型，对应 API 字段 `FieldType`。 |
| Dim | int | 当字段类型为 vector 时表示稠密向量维度，对应 API 字段 `Dim`。 |
| IsPrimaryKey | bool | 是否为主键，对应 API 字段 `IsPrimaryKey`。仅 string / int64 字段可设置为主键。 |
| DefaultValue | interface{} | 字段默认值，对应 API 字段 `DefaultValue`。 |

* CollectionStatsForGetVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| DataCount | int | 集合内数据条数，对应 API 字段 `DataCount`。 |
| DataStorage | int | 集合占用存储量（Byte），对应 API 字段 `DataStorage`。 |

* VectorizeForGetVikingdbCollectionOutput 参 S数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| DenseVectors | VectorizeForGetVikingdbCollectionOutput | 是 | 稠密向量化配置，对应 API 字段 `Dense`，用于指定 embedding 模型、维度与输入字段。 |
| SparseVectors | SparseForGetVikingdbCollectionOutput | 否 | 稀疏向量化配置，对应 API 字段 `Sparse`。 |

* DenseForGetVikingdbCollectionOutput 和 SparseForGetVikingdbCollectionOutput 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| ModelName | string | 是 | 模型名称，对应 API 字段 `ModelName`。可选值见下方 embedding 模型列表。 |
| ModelVersion | string | 否 | 模型版本，对应 API 字段 `ModelVersion`。Doubao 系模型必填，bge 系默认 `default`。 |
| Dim | string | 否 | 稠密向量维度。各模型支持的维度见embedding模型列表。 |
| TextField | string | 否 | 文本向量化字段名，对应 API 字段 `TextField`。 |
| ImageField | string | 否 | 图片向量化字段名，对应 API 字段 `ImageField`。 |
| VideoField | string | 否 | 视频向量化字段名，对应 API 字段 `VideoField`。 |
# 示例
## 请求示例
```python
package main

import (
    "fmt"
    "github.com/volcengine/volcengine-go-sdk/service/vikingdb"
    "github.com/volcengine/volcengine-go-sdk/volcengine"
    "github.com/volcengine/volcengine-go-sdk/volcengine/credentials"
    "github.com/volcengine/volcengine-go-sdk/volcengine/session"
    "os"
)

func main() {
    var (
       accessKey      = os.Getenv("VIKINGDB_AK")
       secretKey      = os.Getenv("VIKINGDB_SK")
       region         = "cn-beijing"
       collectionName = "Your Collection Name"
    )
    config := volcengine.NewConfig().
       WithRegion(region).
       WithCredentials(credentials.NewStaticCredentials(accessKey, secretKey, ""))

    sess, err := session.NewSession(config)
    if err != nil {
       panic(err)
    }
    svc := vikingdb.New(sess)

    input := &vikingdb.GetVikingdbCollectionInput{
       CollectionName: volcengine.String(collectionName),
    }

    output, err := svc.GetVikingdbCollection(input)
    if err != nil {
       panic(err)
    }
    fmt.Println(output)
}
```

