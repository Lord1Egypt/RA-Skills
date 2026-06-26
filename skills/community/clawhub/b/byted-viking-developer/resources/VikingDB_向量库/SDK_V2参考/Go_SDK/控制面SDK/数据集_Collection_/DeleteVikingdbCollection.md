# 概述
deleteVikingdbCollection 用于删除已创建的数据集 Collection。
* 执行 Collection 删除将会永久删除指定 Collection 下的所有数据，请谨慎操作。
* 在删除 Collection 之前，必须先删除 Collection 关联的所有 Index，才能成功删除 Collection。

# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `DeleteVikingdbCollection(input)` 方法发起集合创建请求，input 参数类型为 `vikingdb.DeleteVikingdbCollectionInput` ，包含集合名称、描述、项目名称和字段定义等配置
# **请求参数**
| **参数** | **类型** | **是否必选** | **参数说明** |
| --- | --- | --- | --- |
| ProjectName | string | 否 | 项目名称，对应 API 字段 `ProjectName`，默认 default。 |
| CollectionName | strgin | 2选1 | 待删除集合名称，对应 API 字段 `CollectionName`。 <br>  <br> * 以字母开头，仅可包含字母、数字、下划线，长度 1-128。 <br> * 服务端允许与 `resource_id` 二选一，但当前 Python SDK 强制要求填写 `collection_name`。 |
| ResourceId | string |  | 集合资源 ID，对应 API 字段 `ResourceId`。可与 `collection_name` 组合使用，帮助在控制面追踪。 |
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
    )
    config := volcengine.NewConfig().
       WithRegion(region).
       WithCredentials(credentials.NewStaticCredentials(accessKey, secretKey, ""))

    sess, err := session.NewSession(config)
    if err != nil {
       panic(err)
    }
    svc := vikingdb.New(sess)

    input := &vikingdb.DeleteVikingdbCollectionInput{
       CollectionName: volcengine.String(collectionName),
    }

    output, err := svc.DeleteVikingdbCollection(input)
    if err != nil {
       panic(err)
    }
    fmt.Println(output)
}
```


