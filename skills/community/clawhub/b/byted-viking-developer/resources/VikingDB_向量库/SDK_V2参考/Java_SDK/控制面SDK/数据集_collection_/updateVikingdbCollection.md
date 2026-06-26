# 概述
updateCollection 用于为指定数据集 Collection 增加字段。
Collection 支持新增字段 fields，已定义字段 fields 不支持修改，仅支持修改数据集描述。

# 方法定义
```Java
public UpdateVikingdbCollectionResponse updateVikingdbCollection(UpdateVikingdbCollectionRequest body) throws ApiException 
```

# **请求参数**
请求参数是 UpdateCollectionParam，UpdateCollectionParam 类包括的参数如下表所示。
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| projectName | String | 否 | 项目的名称。对应火山引擎“项目”（project）的概念。不填则默认当做default处理。 |
| collectionName | String | 二选一 | 数据集的名称。 <br> 限制：英文字母、数字、或下划线。且必须以英文字母开头。长度不超过64Byte。 |
| resourceId | String |  | 数据集的Id。 |
| description | String | 否 | 数据集的描述。 <br> 限制：英文字母、数字、或下划线。且必须以英文字母开头。长度不超过64Byte。 |
| fields | List<FieldForUpdateVikingdbCollectionInput> | 是 | 数据集中的字段。 <br> 限制：数据集内最多128个字段。 |

* Field 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| fieldName | String | 是 | 字段名。 <br> 限制：英文字母、数字、或下划线。且必须以英文字母开头。长度不超过64Byte。 |
| fieldType | FieldTypeEnum（枚举类型） | 是 | 字段类型。 <br> 枚举值包括： <br> vector,sparse_vector,string,int64,float32,bool,list<string>,list<int64>,text,image,video |
| defaultValue | Object | 否 | 字段内容默认值。 <br> 注意：vector/sparse_vector/text/image/video类型字段不支持默认值。 |

# 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| message | String | success | 操作结果信息 |
## 示例
## 请求参数
```Python
package org.example.newsubproduct.console.collection;

import com.volcengine.ApiClient;
import com.volcengine.ApiException;
import com.volcengine.sign.Credentials;
import com.volcengine.vikingdb.VikingdbApi;
import com.volcengine.vikingdb.model.*;

import java.util.Arrays;

public class UpdateVikingdbCollection {
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


        UpdateVikingdbCollectionRequest request = new UpdateVikingdbCollectionRequest()
                .collectionName("test_collection_for_sdk_with_vector")
                .fields(Arrays.asList(
                        new FieldForUpdateVikingdbCollectionInput().fieldName("f_string_add_1").fieldType(FieldForUpdateVikingdbCollectionInput.FieldTypeEnum.STRING),
                        new FieldForUpdateVikingdbCollectionInput().fieldName("f_float32_add_1").fieldType(FieldForUpdateVikingdbCollectionInput.FieldTypeEnum.FLOAT32)
                ));

        try {
            UpdateVikingdbCollectionResponse response = api.updateVikingdbCollection(request);
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
