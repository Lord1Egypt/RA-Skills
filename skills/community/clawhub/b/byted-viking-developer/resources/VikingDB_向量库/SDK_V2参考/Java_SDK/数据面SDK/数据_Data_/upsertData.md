# 概述
接口用于在指定的数据集 Collection 内写入数据。指定写入的数据是一个map，允许单次插入一条数据或者多条数据，单次最多可插入100条数据。如提供的主键已存在，则更新对应的数据；否则，插入新的数据。
# 方法定义
```Java
public DataApiResponse<UpsertDataResult> upsertData(UpsertDataRequest request)
        throws ApiClientException, VectorApiException
```

# 请求体参数
| 名称 | 类型 | 描述 | 必选 |
| --- | --- | --- | --- |
| collectionName | String | 数据集的名称。 | 二选一 |
| resourceId | String | 数据集的Id。 |  |
| data | List<Map<String, Object>> | 要更新的数据列表。列表中的每个 Map 代表一条数据，必须包含主键字段。 | 是 |
| ttl | integer | 数据的生存时间（Time-To-Live），单位为秒。超过该时间后数据将被自动删除。 | 否 |
| async | Boolean | 异步写入开关。默认false。以异步写入的方式可以提高10倍QPS，但增大数据进入索引的延迟，适合大批量离线灌库。 | 否 |
# data参数字段值格式
注意：数据插入时主键不能为0

| 字段类型 | 格式 | 说明 |
| --- | --- | --- |
| int64 | 整型数值 | 整数 |
| float32 | 浮点数值 | 浮点数 |
| string | 字符串 | 字符串。内容限制256byte |
| bool | true/false | 布尔类型 |
| list<string> | 字符串数组 | 字符串数组 |
| list<int64> | 整型数组 | 整数数组 |
| vector | * 向量（浮点数数组） <br> * float32/float64压缩为bytes后的base64编码 | 稠密向量 <br>  |
| sparse_vector <br>  |  输入格式<token_id ,token_weight>的字典列表，来表征稀疏稀疏向量的非零位下标及其对应的值, 其中 token_id 是 string 类型, token_weight 是float 类型 | 稀疏向量 <br>  |
| text | 字符串 | 若为向量化字段，则值不能为空。（若否，可以为空） |
| image | Object | 若为向量化字段，则值不能为空。（若否，可以为空） <br>  <br> * 图片tos链接 `tos://{bucket}/{object}` <br> * http/https格式链接 |
| video | Object | { <br> "value": `tos://{bucket}/{object}`，http/https格式url链接，该字段必填 <br> "fps": 0.2 （取值0.2-5，选填） <br> } |
| dateTime | string | 分钟级别： <br> `yyyy-MM-ddTHH:mmZ`或`yyyy-MM-ddTHH:mm±HH:mm` <br> 秒级别： <br> `yyyy-MM-ddTHH:mm:ssZ`或`yyyy-MM-ddTHH:mm:ss±HH:mm` <br> 毫秒级别： <br> `yyyy-MM-ddTHH:mm:ss.SSSZ`或`yyyy-MM-ddTHH:mm:ss.SSS±HH:mm` <br> 例如："2025-08-12T11:33:56+08:00" |
| geoPoint | string | 地理坐标`longitude,latitude`，其中`longitude`取值(-180,180)，`latitude`取值(-90,90) <br> 例如："116.408108,39.915023" |
## 创建时间类型字段(date_time)
只能填写以下格式的其中一种，全部遵循RFC3339标准（https://datatracker.ietf.org/doc/html/rfc3339）
例如："2025-08-12T12:34:56+08:00"
|  | 格式(string) | 示例 | 说明 |
| --- | --- | --- | --- |
| 分钟级别 | `yyyy-MM-ddTHH:mmZ`（utc时间）或 <br> `yyyy-MM-ddTHH:mm±HH:mm`（指定时区） | * `2025-08-12T04:34Z` <br> * `2025-08-12T12:34+08:00` <br>  <br>  | 左侧示例都会解析为北京时间`2025-08-12`的`12:34:00`。 <br>  |
| 秒级别 | `yyyy-MM-ddTHH:mm:ssZ`（utc时间）或 <br> `yyyy-MM-ddTHH:mm:ss±HH:mm`（指定时区） <br>  | * `2025-08-12T04:34:56Z` <br> * `2025-08-12T12:34:56+08:00` <br>  <br>  | 左侧示例都会解析为北京时间`2025-08-12`的`12:34:56`。 <br>  <br>  |
| 毫秒级别 | `yyyy-MM-ddTHH:mm:ss.SSSZ`（utc时间）或 <br> `yyyy-MM-ddTHH:mm:ss.SSS±HH:mm`（带时区） | * `2025-08-12T04:34:56.147Z` <br> * `2025-08-12T12:34:56.147+08:00` <br>  <br>  <br>  | 左侧示例都会解析为北京时间`2025-08-12`的`12:34:56.147`秒。 <br>  |

# 返回参数
| 名称 | 类型 | 描述 |
| --- | --- | --- |
| tokenUsage | Object | 本次请求的 token 使用情况。 |
# **请求示例代码**
```Java
import com.volcengine.vikingdb.runtime.Util;
import com.volcengine.vikingdb.runtime.core.auth.AuthWithAkSk;
import com.volcengine.vikingdb.runtime.core.ClientConfig;
import com.volcengine.vikingdb.runtime.enums.Scheme;
import com.volcengine.vikingdb.runtime.vector.model.request.UpsertDataRequest;
import com.volcengine.vikingdb.runtime.vector.model.response.DataApiResponse;
import com.volcengine.vikingdb.runtime.vector.model.response.UpsertDataResult;
import com.volcengine.vikingdb.runtime.vector.service.VectorService;

import java.util.Arrays;
import java.util.HashMap;

public class UpsertDataExample {

    public static void main(String[] args) {
        // 1. 初始化客户端 (请替换为您的配置)
        VectorService vectorService = null;
        try {
            vectorService = new VectorService(
                    Scheme.HTTPS,
                    "api-vikingdb.vikingdb.cn-beijing.volces.com",
                    "cn-beijing",
                    new AuthWithAkSk("your-access-key", "your-secret-key"),
                    ClientConfig.builder().build()
            );
        } catch (Exception e) {
            System.err.println("Client initialization failed: " + e.getMessage());
            e.printStackTrace();
            return;
        }

        // 2. 准备请求
        UpsertDataRequest request = UpsertDataRequest.builder()
                .collectionName("your_collection_name") // 替换为您的集合名称
                .data(Arrays.asList(
                        new HashMap<String, Object>() {{ put("id", 1); put("field1", "value1"); put("vector", Util.generateRandomVector(128)); }},
                        new HashMap<String, Object>() {{ put("id", 2); put("field1", "value2"); put("vector", Util.generateRandomVector(128)); }},
                        new HashMap<String, Object>() {{ put("id", 3); put("field1", "value3"); put("vector", Util.generateRandomVector(128)); }}
                ))
                .build();

        // 3. 发起请求
        try {
            DataApiResponse<UpsertDataResult> response = vectorService.upsertData(request);
            System.out.println("Upsert data successfully:");
            System.out.println(response);
        } catch (Exception e) {
            System.err.println("Failed to upsert data: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

