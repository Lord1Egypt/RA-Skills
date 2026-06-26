# 概述
`UpdateVikingdbCollection`用于为指定数据集 Collection 增加字段。
Collection 支持新增字段 fields，已定义字段 fields 不支持修改，仅支持修改数据集描述。

# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `ListVikingdbCollection(input)` 方法发起集合创建请求，input 参数类型为 `vikingdb.ListVikingdbCollectionInput` ，包含集合名称、描述、项目名称和字段定义等配置
# **请求参数**
请求参数是 UpdateCollectionParam，UpdateCollectionParam 类包括的参数如下表所示。
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| ProjectName | string | 否 | 项目名称，对应 API 字段 `ProjectName`，默认 default。 |
| CollectionName | string | 二选一 | 集合名称，对应 API 字段 `CollectionName`。以字母开头，仅可包含字母、数字、下划线，长度 1-128。可与 `resource_id` 二选一。 |
| ResourceId | string |  | 集合资源 ID，对应 API 字段 `ResourceId`。与 `collection_name` 二选一，推荐同时填写确保准确。 |
| Description | string | 否 | 集合描述，对应 API 字段 `Description`，最长 65535 字节。 |
| Fields | []FieldForUpdateVikingdbCollectionInput | 是 | 新增字段列表，对应 API 字段 `Fields`。单个集合总字段数上限 128，仅支持追加新字段。 |

* Field 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| FieldName | string | 是 | 字段名。 <br> 限制：英文字母、数字、或下划线。且必须以英文字母开头。长度不超过64Byte。 |
| FieldType | FieldTypeEnum（枚举类型） | 是 | 字段类型。 |
| DefaultValue | interface{} | 否 | 字段内容默认值。 <br> 注意：vector/sparse_vector/text/image/video类型字段不支持默认值。 |
| Dim | Int | 否 | 若字段类型是vector，该参数指定稠密向量的维度。支持4-4096且为4的整数倍。 |
| IsPrimaryKey | bool | 否 | 是否为主键字段。可以为数据集指定1个主键字段（string或int64类型）。若没有指定，则使用自动生成的主键，字段名为"**__AUTO_ID__**"。 |

# 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| Message | string | success | 操作结果描述，对应 API 字段 `Message`。 |
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
       description    = "Your Collection Description"
    )
    config := volcengine.NewConfig().
       WithRegion(region).
       WithCredentials(credentials.NewStaticCredentials(accessKey, secretKey, ""))

    sess, err := session.NewSession(config)
    if err != nil {
       panic(err)
    }
    svc := vikingdb.New(sess)

    input := &vikingdb.UpdateVikingdbCollectionInput{
       CollectionName: volcengine.String(collectionName),
       Description:    volcengine.String(description),

       Fields: []*vikingdb.FieldForUpdateVikingdbCollectionInput{
          {
             FieldName: volcengine.String("new_tag"),
             FieldType: volcengine.String("string"),
          },
          {
             FieldName: volcengine.String("extra_score"),
             FieldType: volcengine.String("float32"),
          },
       },
    }

    output, err := svc.UpdateVikingdbCollection(input)
    if err != nil {
       panic(err)
    }
    fmt.Println(output)
}
```


