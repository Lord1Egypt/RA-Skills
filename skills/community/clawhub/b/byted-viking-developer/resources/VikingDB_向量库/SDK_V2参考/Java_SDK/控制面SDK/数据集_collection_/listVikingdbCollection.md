概述
listCollections 用于查询数据集 Collection 列表。
# 方法定义
```Java
public ListVikingdbCollectionResponse listVikingdbCollection(ListVikingdbCollectionRequest body) throws ApiException
```

# **请求参数**
| 参数 | 类型 |
| --- | --- |
| projectName | String |
| pageSize | Integer |
| pageNumber | Integer |
| filter | FilterForListVikingdbCollectionInput |

* FilterForListVikingdbCollectionInput参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| fieldName | String | 是 | 字段名。 <br> 限制：英文字母、数字、或下划线。且必须以英文字母开头。长度不超过64Byte。 |
| fieldType | FieldTypeEnum（枚举类型） | 是 | 字段类型。 <br> 枚举值包括： <br> vector,sparse_vector,string,int64,float32,bool,list<string>,list<int64>,text,image,video |
| defaultValue | Object | 否 | 字段内容默认值。 <br> 注意：vector/sparse_vector/text/image/video类型字段不支持默认值。 |
| dim | Integer | 否 | 若字段类型是vector，该参数指定稠密向量的维度。支持4-4096且为4的整数倍。 |
| isPrimaryKey | Boolean | 否 | 是否为主键字段。可以为数据集指定1个主键字段（string或int64类型）。若没有指定，则使用自动生成的主键，字段名为"AUTO_ID"。 |

# 返回参数
Java 调用执行上面的任务，返回 Collection 实例列表。Collection 实例包含的属性如下表所示。
| 参数 | 一级参数 | 二级参数 | 三级参数 | 类型 | 描述 |
| --- | --- | --- | --- | --- | --- |
| totalCount |  |  |  | Integer | 查询结果的总数 |
| pageSize |  |  |  | Integer | 请求时的PageSize值，如果请求时未指定，则为默认值。 |
| pageNumber |  |  |  | Integer | 请求时的PageNumber值，如果请求时未指定，则为默认值。 |
| collections |  |  |  | List<CollectionForListVikingdbCollectionOutput>  | 向量库数据集列表 |
|  | collectionName |  |  | String | 数据集名称 |
|  | resourceId |  |  | String | 资源ID |
|  | projectName |  |  | String | 项目名称 |
|  | vectorize |  |  | VectorizeForListVikingdbCollectionOutput | 向量化配置 |
|  |  | dense |  | DenseForListVikingdbCollectionOutput | 稠密向量化模型配置 |
|  |  |  | modelName | String | 模型名称 |
|  |  |  | modelVersion | String | 模型版本 |
|  |  |  | textField | String | 文本向量化字段名称 |
|  |  |  | imageField | String | 图片向量化模型 |
|  |  |  | dim | Integer | 如果需要生成稠密向量，指定向量维度。默认使用模型默认的维度。 |
|  |  |  | videoField | String | 视频向量化字段 |
|  |  | sparse |  | SparseForListVikingdbCollectionOutput | 稀疏向量化配置 |
|  |  |  | modelName | String | 模型名称 |
|  |  |  | modelVersion | String | 模型版本 |
|  |  |  | textField | String | 文本向量化字段名称 |
|  | tags |  |  | List<TagForListVikingdbCollectionOutput> | 标签 |
|  |  | key |  | String | 标签键 |
|  |  | value |  | String | 标签值 |
|  | description |  |  | String | 数据集描述 |
|  | fields |  |  | List<FieldForListVikingdbCollectionOutput> | 字段列表 |
|  |  | fieldName |  | String | 字段名称 |
|  |  | fieldType |  | String | 字段类型 |
|  |  | dim |  | Integer | 若字段类型是vector，该参数指定稠密向量的维度 |
|  |  | isPrimaryKey |  | Boolean | 是否为主键字段。可以为数据集指定1个主键字段（string或int64类型）。若没有指定，则使用自动生成的主键，字段名为"**AUTO_ID**"。 |
|  |  | defaultValue |  | Object | 字段内容默认值 |
|  | createTime |  |  | String | 创建时间 |
|  | updateTime |  |  | String | 更新时间 |
|  | updatePerson |  |  | String | 更新人 |
|  | collectionStats |  |  | CollectionStatsForListVikingdbCollectionOutput | 统计信息 |
|  |  | dataCount |  | Long | 数据条数 |
|  |  | dataStorage |  | Long | 数据存储量(byte) |
|  | enableKeywordsSearch |  |  | Boolean | 是否支持关键词检索 |
|  | indexNames |  |  | Array of String | 数据集下的索引名称列表 |
|  | indexCount |  |  | Integer | 数据集下的索引个数 |
# 示例
## 请求参数
```Java
package org.example.newsubproduct.console.collection;

import com.volcengine.ApiClient;
import com.volcengine.ApiException;
import com.volcengine.sign.Credentials;
import com.volcengine.vikingdb.VikingdbApi;
import com.volcengine.vikingdb.model.*;

public class ListVikingdbCollection {
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

        ListVikingdbCollectionRequest request = new ListVikingdbCollectionRequest()
                .filter(new FilterForListVikingdbCollectionInput().collectionNameKeyword("collection_for_sdk"));

        try {
            ListVikingdbCollectionResponse response = api.listVikingdbCollection(request);
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
