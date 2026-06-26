# 概述
ListVikingdbCollection 接口用于查询当前项目下的 Collection 列表，支持分页与名称关键字过滤。
# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `ListVikingdbCollection(input)` 方法发起集合创建请求，input 参数类型为 `vikingdb.ListVikingdbCollectionInput` ，包含集合名称、描述、项目名称和字段定义等配置
# **请求参数**
| **参数** | **类型** | **是否必选** | **说明** |
| --- | --- | --- | --- |
| ProjectName | string | 否 | 项目名称，对应 API 字段 `ProjectName`，默认 default。 |
| PageSize | int | 否 | 分页大小，对应 API 字段 `PageSize`，取值 1-100，默认 10。 |
| PageNumber | int | 否 | 分页页码，对应 API 字段 `PageNumber`，从 1 开始。 |
| Filter | FilterForListVikingdbCollectionInput | 否 | 过滤条件，对应 API 字段 `Filter`。 |

* FilterForListVikingdbCollectionInput

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| CollectionNameKeyword | string | 否 | 集合名称关键字，对应 API 字段 `CollectionNameKeyword`，用于模糊搜索。 |
# 返回参数
接口返回 `ListVikingdbCollectionResponse`，包含分页信息与集合列表。
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| TotalCount | int | 集合总数，对应 API 字段 `TotalCount`。 |
| PageNumber | int | 当前页码，对应 API 字段 `PageNumber`。 |
| PageSize | int | 本页返回条数，对应 API 字段 `PageSize`。 |
| Collections | []CollectionForListVikingdbCollectionOutput | 集合详情列表，对应 API 字段 `Collections`。 |

* CollectionForListVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| CollectionName | string | 集合名称，对应 API 字段 `CollectionName`。 |
| ProjectName | string | 所属项目，对应 API 字段 `ProjectName`。 |
| ResourceId | string | 集合 ID，对应 API 字段 `ResourceId`。 |
| Description | string | 集合描述，对应 API 字段 `Description`。 |
| CreateTime | string | 创建时间 (RFC3339)，对应 API 字段 `CreateTime`。 |
| UpdateTime | string | 更新时间，对应 API 字段 `UpdateTime`。 |
| UpdatePerson | string | 最近操作人，对应 API 字段 `UpdatePerson`。 |
| EnableKeywordsSearch | bool | 是否开启关键词检索，对应 API 字段 `EnableKeywordsSearch`。 |
| IndexCount | int | 索引数量，对应 API 字段 `IndexCount`。 |
| IndexNames | []string | 索引名称列表，对应 API 字段 `IndexNames`。 |
| Fields | []FieldForListVikingdbCollectionOutput | 字段列表，对应 API 字段 `Fields`。 |
| CollectionStats | CollectionStatsForListVikingdbCollectionOutput | 统计信息，对应 API 字段 `CollectionStats`。 |
| Tags | []TagForListVikingdbCollectionOutput | 标签信息，对应 API 字段 `Tags`。 |
| Vectorize | VectorizeForListVikingdbCollectionOutput | 向量化配置，对应 API 字段 `Vectorize`。 |

* FieldForListVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| FieldName | string | 字段名称，对应 API 字段 `FieldName`。 |
| FieldType | string | 字段类型，对应 API 字段 `FieldType`。 |
| IsPrimaryKey | bool | 是否主键，对应 API 字段 `IsPrimaryKey`。 |
| Dim | int | 向量维度，对应 API 字段 `Dim`。 |
| DefaultValue | interface{} | 默认值，对应 API 字段 `DefaultValue`。 |

* CollectionStatsForListVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| DataCount | int | 集合中文档条数，对应 API 字段 `DataCount`。 |
| DataStorage | int | 存储量（Byte），对应 API 字段 `DataStorage`。 |

* TagForListVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| Key | string | 标签键，对应 API 字段 `Key`。 |
| Value | string | 标签值，对应 API 字段 `Value`。 |

* VectorizeForListVikingdbCollectionOutput

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| DenseVectors | DenseForListVikingdbCollectionOutput | 稠密向量化配置，对应 API 字段 `Dense`，字段含义同 Get 接口。 |
| SparseVectors | SparseForListVikingdbCollectionOutput | 稀疏向量化配置，对应 API 字段 `Sparse`。 |
# 示例
## 请求示例
```python
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

    var (
       projectName = "default"
    )

    input := &vikingdb.ListVikingdbCollectionInput{
       ProjectName: volcengine.String(projectName),
       PageSize:    volcengine.Int32(1),
       PageNumber:  volcengine.Int32(10),
    }
    output, err := svc.ListVikingdbCollection(input)
    if err != nil {
       panic(err)
    }
    fmt.Println(output)
}
```

