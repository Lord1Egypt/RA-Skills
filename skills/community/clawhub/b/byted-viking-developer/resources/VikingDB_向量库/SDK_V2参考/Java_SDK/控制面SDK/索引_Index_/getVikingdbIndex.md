# 概述
getIndex 用于查询索引 Index 详情。
# 方法定义
```Java
public GetVikingdbIndexResponse getVikingdbIndex(GetVikingdbIndexRequest body) throws ApiException
```

# **请求参数**
| **参数** | **类型** | **是否必选** | **参数说明** |
| --- | --- | --- | --- |
| projectName | String | 否 | 项目名称 |
| collectionName | String | 2选1 | 数据集名称 |
| resourceId | String |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| indexName | string | 是 | 指定要查询的 Index 名称。 <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空。 <br> * 长度要求：[1, 128]。 <br> * 索引名称不能重复。 |
# 返回参数
Java 调用执行上面的任务，返回 Index 实例。Index 实例包含的属性如下表所示。
| 参数 | 一级子参数 | 类型 | 描述 |
| --- | --- | --- | --- |
| collectionName |  | String | 数据集名称 |
| projectName |  | String | 项目名称 |
| resourceId |  | String | 资源ID |
| indexName |  | String | 索引名称 |
| cpuQuota |  | Integer | 索引检索消耗的 CPU 配额。 |
| shardPolicy |  | String | 索引分片类型，auto为自动分片、custom为自定义分片。 |
| shardCount |  | Integer | 索引分片数 |
| description |  | String | 索引描述 |
| vectorIndex |  | VectorIndexForGetVikingdbIndexOutput | 向量索引配置 |
|  | indexType | IndexTypeEnum <br> 枚举 | 索引类型 |
|  | distance | DistanceEnum <br> 枚举 | 距离类型，衡量向量之间距离的算法。取值如下： <br> ip：全称是 Inner Product，内积，该算法基于向量的内积，即两个元素的对应元素相乘并求和的结果计算相似度，内积值越大相似度越高。 <br> l2：欧几里得距离，它计算两个向量的欧几里得空间距离，欧式距离越小相似度越高。 <br> cosine：余弦相似度（Cosine Similarity），也称为余弦距离（Cosine Distance），用于计算两个高维向量的夹角余弦值从而衡量向量相似度，夹角余弦值越小表示两向量的夹角越大，则两个向量差异越大。 <br> 当 distance=cosine 时，默认对向量做归一化处理。 <br> 当索引算法选择IVF时，距离类型可选ip、cosine。 <br> 对于hnsw_hybrid索引算法，距离类型选择只对稠密向量生效，稀疏向量仅支持内积。 |
|  | quant | QuantEnum <br> 枚举 | 量化方式。量化方式是索引中对向量的压缩方式，可以降低向量间相似性计算的复杂度。基于向量的高维度和大规模特点，采用向量量化可以有效减少向量的存储和计算成本。取值如下： <br>  <br> * int8：将4字节的 float 压缩为单个字节，以获取内存和计算延迟的收益，会造成微小的损失精度，比如 cosine 距离会出现大于1的分值。 <br> * float：全精度，未做压缩量化。 <br> * fix16：将4字节的 float 压缩为两个字节，以获取内存和计算延迟的收益，会造成微小的损失精度。通过损失一定的检索精度，提升检索性能，节约资源成本。 <br> * pq：将高维向量转换为低维码本向量，以减少内存占用并提高搜索效率。 <br>  <br> int8适用于hnsw、hnsw_hybrid、flat索引算法，距离方式为ip、consine。 <br>  <br> float适用于hnsw、hnsw_hybrid、flat、diskann索引算法，距离方式为ip、l2、consine。 <br>  <br> fix16适用于hnsw、hnsw_hybrid、flat索引算法，距离方式为ip、l2、consine。 <br>  <br> pq适用于diskann、ivf索引算法，距离方式为ip、l2、consine。 |
|  | hnswM | Integer | hnsw 索引参数，表示邻居节点个数。 <br>  <br> * 当 index_type 配置为 hnsw 和 hnsw_hybrid 时可选配置。 |
|  | hnswCef | Integer | hnsw 索引参数，表示构建图时搜索邻居节点的广度。 <br>  <br> * 当 index_type 配置为 hnsw 和 hnsw_hybrid 时可选配置。 |
|  | hnswSef | Integer | hnsw 索引参数，表示线上检索的搜索广度。 <br>  <br> * 当 index_type 配置为 hnsw 和 hnsw_hybrid 时可选配置。 |
|  | diskannM | Integer | diskann参数，标识邻居节点个数。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |
|  | diskannCef | Integer | diskann参数，表示构建图时搜索邻居节点的广度。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |
|  | pqCodeRatio | Float | diskann参数，向量维度编码的大小限制。值越大，召回率越高，但会增加内存使用量，范围 (0.0, 0.25]。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |
|  | cacheRatio | Float | diskann参数，缓存节点数与原始数据的比率，较大的值会提高索引性能并增加内存使用量。范围 [0.0,0.3)。 <br>  <br> * 当 index_type 配置为 diskann时可选配置。 |
| scalarIndex |  | List<ScalarIndexForGetVikingdbIndexOutput>  | 标量字段列表 <br> ```JSON <br> "ScalarIndex": [ <br>     { <br>         "FieldName": "f_int64_1", #string <br>         "FieldType": "int64", #string <br>         "DefaultValue": 0 #any <br>     }, <br> ``` <br>  |
|  | defaultValue | Object |  |
|  | dim | Integer |  |
|  | fieldName | String |  |
| actualCU |  | Integer | 实际CU用量 |
# 示例
## 请求参数
```Java
package org.example.newsubproduct.console.index;

import com.volcengine.ApiClient;
import com.volcengine.ApiException;
import com.volcengine.sign.Credentials;
import com.volcengine.vikingdb.VikingdbApi;
import com.volcengine.vikingdb.model.*;

public class GetVikingdbIndex {
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

        GetVikingdbIndexRequest request = new GetVikingdbIndexRequest()
                .collectionName("test_collection_for_sdk_with_vector")
                .indexName("idx_simple");

        try {
            GetVikingdbIndexResponse response = api.getVikingdbIndex(request);
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

## 
