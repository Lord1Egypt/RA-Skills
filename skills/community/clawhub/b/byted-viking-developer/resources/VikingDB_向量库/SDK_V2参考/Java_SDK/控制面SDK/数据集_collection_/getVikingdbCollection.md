# 概述
getCollection 用于查询指定数据集 Collection 的详情信息。
# 方法定义
```Java
public GetVikingdbCollectionResponse getVikingdbCollection(GetVikingdbCollectionRequest body) throws ApiException
```

# **请求参数**
| **参数** | **类型** | **是否必选** | **参数说明** |
| --- | --- | --- | --- |
| projectName | String | 否 | 项目名称 |
| collectionName | string | 2选1 | 指定查询的 Collection 名称。 <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空。 <br> * 长度要求：[1, 128]。 <br> * Collection 名称不能重复。 |
| resourceId | String |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
# 返回参数
Java 调用执行上面的任务，返回 Collection 实例。Collection 实例包含的属性如下表所示。
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| projectName | String | 项目名称 |
| resourceId | String | 资源ID |
| collectionName | String | 数据集名称 |
| description | String | 数据集描述 |
| enableKeywordsSearch | Boolean | 是否可支持关键词检索 |
| fields | List<FieldForGetVikingdbCollectionOutput>  | 字段列表 |
| vectorize | VectorizeForGetVikingdbCollectionOutput | 向量化配置 |
| createTime | String | 创建时间 |
| updateTime | String | 更新时间 |
| updatePerson | String | 更新人 |
| collectionStats | CollectionStatsForGetVikingdbCollectionOutput | 统计信息 |
| indexNames | List<String> | 数据集下的索引名称列表 |
| indexCount | Integer | 数据集下的索引个数 |

* List<FieldForGetVikingdbCollectionOutput> 

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| fieldName | String | 字段名称 |
| fieldType | String | 字段类型 |
| dim | Integer | 若字段类型是vector，该参数指定稠密向量的维度 |
| isPrimaryKey | Boolean | 是否为主键字段。可以为数据集指定1个主键字段（string或int64类型）。若没有指定，则使用自动生成的主键，字段名为"**AUTO_ID**"。 |
| defaultValue | Object | 字段内容默认值 |


* VectorizeForGetVikingdbCollectionOutput

| 参数 |  | 类型 | 说明 |
| --- | --- | --- | --- |
| dense |  | DenseForGetVikingdbCollectionOutput | 稠密向量化模型配置 |
|  | modelName | String | 模型名称 |
|  | modelVersion | String | 模型版本 |
|  | textField | String | 文本向量化字段名称 |
|  | imageField | String | 图片向量化模型 |
|  | dim | Integer | 如果需要生成稠密向量，指定向量维度。默认使用模型默认的维度。 |
|  | videoField | String | 视频向量化字段 |
| sparse |  | SparseForGetVikingdbCollectionOutput | 稀疏向量化配置 |
|  | modelName | String | 模型名称 |
|  | modelVersion | String | 模型版本 |
|  | textField | String | 文本向量化字段名称 |

* CollectionStatsForGetVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| dataCount | Long | 数据条数 |
| dataStorage | Long | 数据存储量(byte) |

# 示例
## 请求参数
```Java
package org.example.newsubproduct.console.collection;

import com.volcengine.ApiClient;
import com.volcengine.ApiException;
import com.volcengine.sign.Credentials;
import com.volcengine.vikingdb.VikingdbApi;
import com.volcengine.vikingdb.model.*;

public class GetVikingdbCollection {
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

        GetVikingdbCollectionRequest request = new GetVikingdbCollectionRequest()
                .collectionName("test_collection_for_sdk_with_vector");

        try {
            GetVikingdbCollectionResponse response = api.getVikingdbCollection(request);
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
