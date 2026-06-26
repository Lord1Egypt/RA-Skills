# 概述
listVikingIndexes 用于查询和数据集 Collection 关联的索引 Index列表。
# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用` ListVikingdbIndex(input)` 方法发起索引创建请求，input 参数类型为 `vikingdb.ListVikingdbIndexInput` ，包含索引创建所需的完整配置信息
# **请求参数**
| 参数 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- |
| PageNumber | int | 否 | 翻页页码。起始为1。 |
| PageSize | int | 否 | 翻页每页的大小。 |
| Filter | FilterForListVikingdbIndexInput | 否 | 过滤条件，如下 |

* FilterForListVikingdbIndexInput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| CollectionName | []string | 数据集名称 |
| IndexNameKeyword | string | 索引名 |
| Status | []string | 状态 |

# 返回参数
GO 调用执行上面的任务，返回 Index 实例列表。Index 实例包含的属性如下表所示。
| 参数 | 一级子参数 | 二级子参数 | 类型 | 描述 |
| --- | --- | --- | --- | --- |
| Indexes |  |  | []IndexForListVikingdbIndexOutput | 向量库索引详情列表 |
|  | CollectionName |  | string | 数据集名称 |
|  | ProjectName |  | string | 项目名称 |
|  | ResourceId |  | string | 资源ID |
|  | IndexName |  | string | 索引名称 |
|  | Description |  | string | 索引的自定义描述。 |
|  | VectorIndex |  | VectorIndexForListVikingdbIndexOutput | 向量索引配置 |
|  |  | IndexType | IndexTypeEnum <br> 枚举 | 索引类型 |
|  |  | Distance | DistanceEnum <br> 枚举 | 距离类型，衡量向量之间距离的算法。取值如下： <br> ip：全称是 Inner Product，内积，该算法基于向量的内积，即两个元素的对应元素相乘并求和的结果计算相似度，内积值越大相似度越高。 <br> l2：欧几里得距离，它计算两个向量的欧几里得空间距离，欧式距离越小相似度越高。 <br> cosine：余弦相似度（Cosine Similarity），也称为余弦距离（Cosine Distance），用于计算两个高维向量的夹角余弦值从而衡量向量相似度，夹角余弦值越小表示两向量的夹角越大，则两个向量差异越大。 <br> 当 distance=cosine 时，默认对向量做归一化处理。 <br> 当索引算法选择IVF时，距离类型可选ip、cosine。 <br> 对于hnsw_hybrid索引算法，距离类型选择只对稠密向量生效，稀疏向量仅支持内积。 |
|  |  | Quant | QuantEnum <br> 枚举 | 量化方式。量化方式是索引中对向量的压缩方式，可以降低向量间相似性计算的复杂度。基于向量的高维度和大规模特点，采用向量量化可以有效减少向量的存储和计算成本。取值如下： <br>  <br> * int8：将4字节的 float 压缩为单个字节，以获取内存和计算延迟的收益，会造成微小的损失精度，比如 cosine 距离会出现大于1的分值。 <br> * float：全精度，未做压缩量化。 <br> * fix16：将4字节的 float 压缩为两个字节，以获取内存和计算延迟的收益，会造成微小的损失精度。通过损失一定的检索精度，提升检索性能，节约资源成本。 <br> * pq：将高维向量转换为低维码本向量，以减少内存占用并提高搜索效率。 <br>  <br> int8适用于hnsw、hnsw_hybrid、flat索引算法，距离方式为ip、consine。 <br>  <br> float适用于hnsw、hnsw_hybrid、flat、diskann索引算法，距离方式为ip、l2、consine。 <br>  <br> fix16适用于hnsw、hnsw_hybrid、flat索引算法，距离方式为ip、l2、consine。 <br>  <br> pq适用于diskann、ivf索引算法，距离方式为ip、l2、consine。 |
|  |  | HnswM | int | hnsw 索引参数，表示邻居节点个数。 <br>  <br> * 当 index_type 配置为 hnsw 和 hnsw_hybrid 时可选配置。 |
|  |  | HnswCef | int | hnsw 索引参数，表示构建图时搜索邻居节点的广度。 <br>  <br> * 当 index_type 配置为 hnsw 和 hnsw_hybrid 时可选配置。 |
|  |  | HnswSef | int | hnsw 索引参数，表示线上检索的搜索广度。 <br>  <br> * 当 index_type 配置为 hnsw 和 hnsw_hybrid 时可选配置。 |
|  |  | DiskannM | int | diskann参数，标识邻居节点个数。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |
|  |  | DiskannCef | int | diskann参数，表示构建图时搜索邻居节点的广度。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |
|  |  | PqCodeRatio | float | diskann参数，向量维度编码的大小限制。值越大，召回率越高，但会增加内存使用量，范围 (0.0, 0.25]。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |
|  |  | CacheRatio | float | diskann参数，缓存节点数与原始数据的比率，较大的值会提高索引性能并增加内存使用量。范围 [0.0,0.3)。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |
|  | ScalarIndex |  | []ScalarIndexForListVikingdbIndexOutput | 标量字段列表 |
|  | CpuQuota |  | int | 索引检索消耗的 CPU 配额。 |
|  | ShardPolicy |  | string | 索引分片类型，auto为自动分片、custom为自定义分片。 |
|  | ShardCount |  | int | 索引分片数 |
|  | ActualCU |  | int | 实际CU用量 |
| PageSize |  |  | int | 请求时的PageSize值，如果请求时未指定，则为默认值。 |
| PageNumber |  |  | int | 请求时的PageNumber值，如果请求时未指定，则为默认值。 |
| TotalCount |  |  | int | 查询结果的总数 |

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

    input := &vikingdb.ListVikingdbIndexInput{
       Filter: &vikingdb.FilterForListVikingdbIndexInput{
          CollectionName: volcengine.StringSlice([]string{"Your Collection Name"}),
       },
       ProjectName: volcengine.String("default"),
    }

    output, err := svc.ListVikingdbIndex(input)
    if err != nil {
       panic(err)
    }
    fmt.Printf("List index response: %+v\n", output)
}
```


