# 概述
updateIndex 接口用于更新指定 Index 的描述、cpuQuota、scalarIndex。
# 方法定义
```Java
public UpdateVikingdbIndexResponse updateVikingdbIndex(UpdateVikingdbIndexRequest body) throws ApiException 
```

# **请求参数**
请求参数是 CreateIndexParam，CreateIndexParam 类包括的参数如下表所示。
| **参数** | **类型** | **是否必选** | **参数说明** |
| --- | --- | --- | --- |
| projectName | String | 否 | 项目名称 |
| collectionName | String | 2选1 | 指定创建索引所属的 Collection 名称。 <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空。 <br> * 长度要求：[1, 128]。 <br> * Collection 名称不能重复。 |
| resourceId | String |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| indexName | String | 是 | 指定创建的索引 Index 名称。 <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空。 <br> * 长度要求：[1, 128]。 <br> * 索引名称不能重复。 |
| cpuQuota  | Integer | 否 | 索引检索消耗的 CPU 配额，格式为正整数。 <br>  <br> * 与吞吐量有关，和延迟无关，1CPU 核约为 100QPS。 <br> * N个分片数量N倍的 CPU 消耗；如果检索消耗的 CPU 超过配额，该索引会被限流。 <br> * 取值范围：[2, 10240]。 |
| description | String | 否 | 索引的自定义描述。 |
| scalarIndex | List<String> | 否 | 标量字段列表。 <br>  <br> * scalarIndex 默认为 None，表示所有字段构建到标量索引。 <br> * scalarIndex 为 [] 时，表示无标量索引。 <br> * scalarIndex 为非空列表时，表示将列表内字段构建到标量索引。 <br>  <br> 如果标量字段进入标量索引，主要用于范围过滤和枚举过滤，会占用额外资源： <br>  <br> * 范围过滤：float32、int64 <br> * 枚举过滤：int64、string、list<int64>、list<string>、bool <br>  <br> 如果标量字段不进入标量索引，仍支持作为正排字段选取使用和部分正排计算。 |
| shardCount | Integer | 否 | 分片数。索引分片是指在大规模数据量场景下，可以把索引数据切分成多个小的索引块，分发到同一个集群不同节点进行管理，每个节点负责存储和处理一部分数据，可以将查询负载分散到不同的节点上，并发的进行处理。当一个节点发生故障时，系统可以自动将其上的分片数据迁移到其他的正常节点上，保证稳定性，以实现数据的水平扩展和高性能的读写操作。 <br>  <br> * 取值范围：[1, 256]。 <br> * 默认为1，分片数预估参考：数据预估数据量/3000万。 |

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

public class UpdateVikingdbIndex {
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

        UpdateVikingdbIndexRequest request = new UpdateVikingdbIndexRequest()
                .collectionName("test_collection_for_sdk_with_vector")
                .indexName("idx_simple")
                .cpuQuota(2);

        try {
            UpdateVikingdbIndexResponse response = api.updateVikingdbIndex(request);
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
