# 概述
UpdateVikingdbIndex 接口用于修改已存在索引的描述、标量索引、CPU 配额或分片策略。
# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `UpdateVikingdbIndex(input)` 方法发起索引创建请求，input 参数类型为 `vikingdb.UpdateVikingdbIndexInput` ，包含索引创建所需的完整配置信息
# **请求参数**
| **参数** | **类型** | **是否必选** | **参数说明** |
| --- | --- | --- | --- |
| ProjectName | string | 否 | 项目名称 |
| CollectionName | string | 2选1 | 指定创建索引所属的 Collection 名称。 <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空。 <br> * 长度要求：[1, 128]。 <br> * Collection 名称不能重复。 |
| ResourceId | string |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| IndexName | string | 是 | 指定创建的索引 Index 名称。 <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空。 <br> * 长度要求：[1, 128]。 <br> * 索引名称不能重复。 |
| CpuQuota  | int | 否 | 索引检索消耗的 CPU 配额，格式为正整数。 <br>  <br> * 与吞吐量有关，和延迟无关，1CPU 核约为 100QPS。 <br> * N个分片数量N倍的 CPU 消耗；如果检索消耗的 CPU 超过配额，该索引会被限流。 <br> * 取值范围：[2, 10240]。 |
| Description | string | 否 | 索引的自定义描述。 |
| ScalarIndex | []String | 否 | 标量字段列表。 <br>  <br> * scalarIndex 默认为 None，表示所有字段构建到标量索引。 <br> * scalarIndex 为 [] 时，表示无标量索引。 <br> * scalarIndex 为非空列表时，表示将列表内字段构建到标量索引。 <br>  <br> 如果标量字段进入标量索引，主要用于范围过滤和枚举过滤，会占用额外资源： <br>  <br> * 范围过滤：float32、int64 <br> * 枚举过滤：int64、string、list<int64>、list<string>、bool <br>  <br> 如果标量字段不进入标量索引，仍支持作为正排字段选取使用和部分正排计算。 |
| ShardCount | int | 否 | 分片数。索引分片是指在大规模数据量场景下，可以把索引数据切分成多个小的索引块，分发到同一个集群不同节点进行管理，每个节点负责存储和处理一部分数据，可以将查询负载分散到不同的节点上，并发的进行处理。当一个节点发生故障时，系统可以自动将其上的分片数据迁移到其他的正常节点上，保证稳定性，以实现数据的水平扩展和高性能的读写操作。 <br>  <br> * 取值范围：[1, 256]。 <br> * 默认为1，分片数预估参考：数据预估数据量/3000万。 |

* 



# 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| message | String | success | 操作结果信息 |
# 示例
## 请求示例
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

    input := &vikingdb.UpdateVikingdbIndexInput{
       CollectionName: volcengine.String("Your Collection Name"),
       IndexName:      volcengine.String("Your Index Name"),
       ProjectName:    volcengine.String("default"),
       Description:    volcengine.String("Your Index Description"),
       ShardCount:     volcengine.Int32(2),
    }

    output, err := svc.UpdateVikingdbIndex(input)
    if err != nil {
       panic(err)
    }
    fmt.Printf("Update index response: %+v\n", output)
}
```

## 
