# 概述
createIndex 用于为指定的数据集 Collection 创建索引 Index。
创建索引可以加速向量的相似度搜索，它根据指定的索引算法和数据结构将向量库中的原始数据进行分组排序，提高相似度搜索的效率和准确性，是驱动向量数据库在短时间内筛选出候选的核心所在。
对于索引的数据集只存在稠密向量（即 vector 类型字段）的情况，我们称这种索引为纯稠密索引；对于索引的数据集中存在稠密向量和稀疏向量（vector 和 sparse_vector 类型字段）的情况，我们称这种索引为混合索引。
# 方法定义
```Java
public CreateVikingdbIndexResponse createVikingdbIndex(CreateVikingdbIndexRequest body) throws ApiException
```

# **请求参数**
请求参数是 CreateIndexParam，CreateIndexParam 类包括的参数如下表所示。
| **参数** | **类型** | **是否必选** | **参数说明** |
| --- | --- | --- | --- |
| projectName | String | 否 | 项目名称 |
| collectionName | String | 2选1 | 数据集名称 |
| resourceId | String |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| indexName | string | 是 | 指定创建的索引 Index 名称。 <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空。 <br> * 长度要求：[1, 128]。 <br> * 索引名称不能重复。 <br> * 同账号下，index 数量不超过200个 |
| description | String | 否 | 索引的自定义描述。 |
| scalarIndex | List<String> | 否 | 标量字段列表，用于设置需要构建到标量索引的字段。 |
| shardPolicy | ShardPolicyEnum | 否 | 索引分片类型 <br>  <br> * 可选值为ShardType.Auto/ShardType.Custom，auto为自动分片、custom为自定义分片。 |
| shardCount | Integer | 否 | 自定义分片数。 |
| CpuQuota | Integer | 否 | 索引检索消耗的 CPU 配额，格式为正整数。 |
| vectorIndex | VectorIndexForCreateVikingdbIndexInput | 是 | 见下 |

* VectorIndexForCreateVikingdbIndexInput

| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| indexType | IndexTypeEnum <br> 枚举 | 是 | IndexType.HNSW | 向量索引类型。取值如下： <br>  <br> * IndexType.HNSW：全称是 Hierarchical Navigable Small World，一种用于在高维空间中采用 ANN 搜索的数据结构和算法，是基于图的索引。HNSW通过构建多层网络减少搜索过程中需要访问的节点数量，实现快速高效地搜索最近邻，适合对搜索效率要求较高的场景。 <br> * IndexType.HNSW_HYBRID：支持混合索引的 hnsw 算法。混合索引算法可以同时对数据集中的稠密向量和稀疏向量进行索引，并在检索时返回兼顾两种类型相似性的结果。适用于对搜索效率要求较高，且需要同时检索稀疏和稠密向量的场景。 <br>    HNSW_HYBRID索引的数据集必须包含 sparse_vector类型数据，即定义了sparse_vector类型字段，或绑定了能产生sparse_vector 类型向量的 pipeline。 <br> * IndexType.FLAT：暴力索引，搜索时遍历整个向量数据库的所有向量与目标向量进行距离计算和比较，查询速度较慢，但是 flat 能提供100％的检索召回率，适用于向量候选集较少，且需要100％检索召回率的场景。 <br> * IndexType.IVF：倒排索引，利用倒排的思想保存每个聚类中心下的向量，每次查询向量的时候找到最近的几个中心，分别搜索这几个中心下的向量，速度较快，但是精度略低，适合中等规模数据量，对搜索效率要求高，精度次之的场景。 <br> * IndexType.DISKANN：基于 Vamana 图的磁盘索引算法，将 Vamana 图与 PQ 量化压缩方案结合，构建DiskANN索引。图索引和原始数据存在SSD中，压缩索引放在内存中。检索请求时会将query向量与聚簇中心比较，然后从磁盘读取对应的原始数据进行算分。适用于大规模数据量，性能不是特别敏感，内存成本更低，且召回率较高的场景。 |
| distance | DistanceEnum枚举 | 否 | DistanceType.IP | 距离类型，衡量向量之间距离的算法。取值如下： <br>  <br> * DistanceType.IP：全称是 Inner Product，内积，该算法基于向量的内积，即两个元素的对应元素相乘并求和的结果计算相似度，内积值越大相似度越高。 <br> * DistanceType.L2：欧几里得距离，它计算两个向量的欧几里得空间距离，欧式距离越小相似度越高。 <br> * DistanceType.COSINE：余弦相似度（Cosine Similarity），也称为余弦距离（Cosine Distance），用于计算两个高维向量的夹角余弦值从而衡量向量相似度，夹角余弦值越小表示两向量的夹角越大，则两个向量差异越大。 <br>    当 distance=DistanceType.COSINE 时，默认对向量做归一化处理。 <br>  <br> 对于hnsw_hybrid索引算法，距离类型选择只对稠密向量生效，稀疏向量仅支持内积。 |
| quant | QuantEnum枚举 | 否 | QuantType.Int8 | 量化方式。量化方式是索引中对向量的压缩方式，可以降低向量间相似性计算的复杂度。基于向量的高维度和大规模特点，采用向量量化可以有效减少向量的存储和计算成本。取值如下： <br>  <br> * QuantType.Int8：将4字节的 float 压缩为单个字节，以获取内存和计算延迟的收益，会造成微小的损失精度，比如 cosine 距离会出现大于1的分值。 <br> * QuantType.Float：全精度，未做压缩量化。 <br> * QuantType.Fix16:将4字节的 float 压缩为两个字节，以获取内存和计算延迟的收益，会造成微小的损失精度。通过损失一定的检索精度，提升检索性能，节约资源成本。 <br> * QuantType.PQ：将高维向量转换为低维码本向量，以减少内存占用并提高搜索效率。 |
| hnswM | Integer | 否 | 20 | hnsw 索引参数，表示邻居节点个数。 <br>  <br> * 当 indexType 配置为 IndexType.HNSW 时可选配置。 |
| hnswCef | Integer | 否 | 400 | hnsw 索引参数，表示构建图时搜索邻居节点的广度。 <br>  <br> * 当 indexType 配置为 IndexType.HNSW 时可选配置。 |
| hnswSef | Integer | 否 | 800 | hnsw 索引参数，表示线上检索的搜索广度。 <br>  <br> * 当 indexType 配置为 IndexType.HNSW 时可选配置。 |
| diskannM | Integer | 否 |  | diskann参数，标识邻居节点个数。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |
| diskannCef | Integer | 否 |  | diskann参数，表示构建图时搜索邻居节点的广度。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |
| pqCodeRatio | Float <br>  | 否 |  | diskann参数，向量维度编码的大小限制。值越大，召回率越高，但会增加内存使用量，范围 (0.0, 0.25]。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |
| cacheRatio | Float | 否 |  | diskann参数，缓存节点数与原始数据的比率，较大的值会提高索引性能并增加内存使用量。范围 [0.0,0.3)。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |

# 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| message | String | success | 操作结果信息 |
# 示例
## 请求参数
```Java
package org.example.newsubproduct.console.index;

import com.volcengine.ApiClient;
import com.volcengine.ApiException;
import com.volcengine.sign.Credentials;
import com.volcengine.vikingdb.VikingdbApi;
import com.volcengine.vikingdb.model.*;

import java.util.Arrays;

public class CreateVikingdbIndexWithScalarIndex {
    public static void main(String[] args) {
        String ak = System.getenv("AK"); // ak
        String sk = System.getenv("SK"); // sk
        String endpoint = "vikingdb.cn-beijing.volcengineapi.com"; // 填写向量库控制面v2的域名  https://www.volcengine.com/docs/84313/1792715
        String region = "cn-beijing"; // 服务区域

        ApiClient apiClient = new ApiClient()
                .setEndpoint(endpoint)
                .setCredentials(Credentials.getCredentials(ak, sk))
                .setRegion(region);

        VikingdbApi api = new VikingdbApi(apiClient);

        CreateVikingdbIndexRequest request = new CreateVikingdbIndexRequest()
                .collectionName("test_collection_for_product")
                .indexName("idx_with_scalar_index")
                .vectorIndex(new VectorIndexForCreateVikingdbIndexInput()
                        .indexType(VectorIndexForCreateVikingdbIndexInput.IndexTypeEnum.HNSW_HYBRID)
                        .distance(VectorIndexForCreateVikingdbIndexInput.DistanceEnum.IP)
                        .quant(VectorIndexForCreateVikingdbIndexInput.QuantEnum.INT8)
                )
                .scalarIndex(Arrays.asList("product_type", "brand_name", "price", "sales")
                );

        try {
            CreateVikingdbIndexResponse response = api.createVikingdbIndex(request);
            System.out.println("response body: " + response);
            System.out.println();
            System.out.println("response meta RequestId: " + response.getResponseMetadata().getRequestId());
            System.out.println("response meta Service: " + response.getResponseMetadata().getService());
            System.out.println("response meta Region: " + response.getResponseMetadata().getRegion());
            System.out.println("response meta Action: " + response.getResponseMetadata().getAction());
            System.out.println("response meta Version: " + response.getResponseMetadata().getVersion());
        } catch (ApiException e) {
            System.out.println("exception http code: " + e.getCode());
            System.out.println("exception response body: " + e.getResponseBody());
            System.out.println();
            System.out.println("exception RequestId: " + e.getResponseMetadata().getRequestId());
            System.out.println("exception Action: " + e.getResponseMetadata().getAction());
            System.out.println("exception Region: " + e.getResponseMetadata().getRegion());
            System.out.println("exception Service: " + e.getResponseMetadata().getService());
            System.out.println("exception Error.Code: " + e.getResponseMetadata().getError().getCode());
            System.out.println("exception Error.Message: " + e.getResponseMetadata().getError().getMessage());
        }
    }
}
```




