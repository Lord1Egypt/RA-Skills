# 概述
embedding 用于将非结构化数据向量化，通过深度学习神经网络提取文本、图片、音视频等非结构化数据里的内容和语义，把文本、图片、音视频等变成特征向量。
* 当前 Embedding 服务仅支持将文本生成向量。
* 当前 Embedding 服务接口不支持承载高并发请求，请求数量过多时请求会被丢弃。

# 方法定义
```Java
    public DataApiResponse<EmbeddingResult> embedding(EmbeddingRequest request)
            throws ApiClientException, VectorApiException
```

# 
# 请求体参数
| 参数 | 类型 | 是否必选 | 子参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| denseModel <br>  | EmbeddingModel <br>  | 2者至少选1 <br>  | name <br>  | string | 是 <br>  | 模型名 |
|  |  |  | version | string | 否，但豆包模型必选 | 模型版本 |
|  |  |  | dim | int | 否 | 维度。不填则使用该模型版本的默认维度。 |
| sparseModel | EmbeddingModel |  | name <br>  | string | 是 <br>  | 模型名 |
|  |  |  | version | string | 否 | 模型版本 |
| data | List<EmbeddingDataItem> | 是 |  |  |  | 数据。详细字段见下。列表长度最大 10。如果数据类型是fullModalSeq则长度为1 |
结构如下：
| 参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| text | string | 至少选一个，也可  text、image和video的组合 <br>  | 文本字符串内容。过长则会截断，各模型的截断阈值见下。 |
| image <br>  | Object |  | * MediaData规则见下 <br>    * 图片tos链接`tos://{bucket}/{object}` <br>    * http/https格式链接 |
| video | Object |  | * MediaData规则见下 <br>  <br> { <br> "value": `tos://{bucket}/{object}`，http/https格式url链接，该字段必填 <br> "fps": 0.2 （取值0.2-5，选填） <br> } |
| fullModalSeq | list | 若选择full_modal_seq，则不能出现上述text等三个参数 | FullModalData结构见下 |


* MediaData（例如image图片、video视频可以为字符串）的格式规范：

| 二选一 | * 同region内的tos资源地址。`tos://{bucket}/{object_key}` |
| --- | --- |
|  | * 可公开访问的http/https链接。`http://`或`https://` |


* FullModalData结构：

| 三选一 | 字段名 | 类型 | 备注 |
| --- | --- | --- | --- |
|  | text <br>  | String | 纯文本 |
|  | image | Object | 若无特殊配置参数，使用string类型填入图片资源地址，参考MediaData规范； |
|  | video <br>  | Object <br>  | 若无特殊配置参数，可使用map类型，子参数包括： <br>  <br> * value：使用string类型填入视频资源地址，参考MediaData规范。 <br> * fps：表示抽帧的频率。不设置则默认为1，范围为0.2-5.0。不过，服务端默认至少抽取16帧。越大，则抽帧更多，同时消耗的token也越多、时延越高。 |

## 模型列表
| 模型名称 | 模型版本 | 支持向量化类型 | 默认稠密向量维度 | 可选稠密向量维度 | 文本截断长度 | 支持稀疏向量 |  可支持instruction <br>  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bge-large-zh | (default) | text | 1024 | 1024 | 512 | 否 | 是 |
| bge-m3 | (default) | text | 1024 | 1024 | 8192 | 是 | 否 |
| bge-visualized-m3 <br>  | (default) | text、image及其组合 | 1024 | 1024 | 8192 | 否 | 否 |
| doubao-embedding | *240715* | text | 2048 <br>  | 512, 1024, 2048 | 4096 | 否 | 是 <br>  |
| doubao-embedding-large | *240915* | text | 2048 | 512, 1024, 2048, 4096 | 4096 | 否 | 是 |
| doubao-embedding-vision | *250328* | text、image及其组合 | 2048 | 2048, 1024 <br>  | 8192 | 否 | 是 |
| doubao-embedding-vision | *250615* | 兼容*241215*和*250328*的用法*。​*另外，支持full_modal_seq（文/图/视频序列） | 2048 <br>  | 2048, 1024 <br>  | 128k | 否 | 是 |
# 返回参数
| 子参数 | 类型 | 说明 |
| --- | --- | --- |
| data | List<EmbeddingItem> | 数据列表 |
| tokenUsage | Object | 按模型粒度的token统计。 <br> 包括prompt_tokens、completion_tokens、image_tokens、total_tokens信息 |
EmbeddingItem结构：
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| dense | List<Float> | 稠密向量结果 |
| sparse | Map<String, Float> | 稀疏向量结果 |

# 请求参数

```Java
package org.example.newsubproduct.data;

import com.volcengine.vikingdb.runtime.core.auth.AuthWithAkSk;
import com.volcengine.vikingdb.runtime.core.ClientConfig;
import com.volcengine.vikingdb.runtime.enums.Scheme;
import com.volcengine.vikingdb.runtime.exception.ApiClientException;
import com.volcengine.vikingdb.runtime.exception.VectorApiException;
import com.volcengine.vikingdb.runtime.vector.model.request.*;
import com.volcengine.vikingdb.runtime.vector.model.response.*;
import com.volcengine.vikingdb.runtime.vector.service.VectorService;

import java.util.Arrays;

public class Embedding {

    public static void main(String[] args) {
        VectorService vectorService = null;
        try {
            vectorService = new VectorService(
                    Scheme.HTTPS,
                    "api-vikingdb.vikingdb.cn-beijing.volces.com", // 填写向量库数据面v2的域名  https://www.volcengine.com/docs/84313/1792715
                    "cn-beijing",
                    new AuthWithAkSk(System.getenv("AK"), System.getenv("SK")),
                    ClientConfig.builder().build()
            );
        } catch (Exception e) {
            System.err.println("Client initialization failed: " + e.getMessage());
            e.printStackTrace();
            return;
        }

        EmbeddingRequest request = EmbeddingRequest.builder()
                .denseModel(EmbeddingModel.builder().name("doubao-embedding-large1").version("240915").dim(1024).build()) // 替换为您的稠密模型
                .data(Arrays.asList(
                        EmbeddingDataItem.builder().text("this is a text for embedding").build()
                ))
                .build();

        try {
            DataApiResponse<EmbeddingResult> response = vectorService.embedding(request);
            System.out.println("request success:");
            System.out.println(response);
        } catch (VectorApiException vectorApiException) {
            System.err.println("request vectorApiException:");
            System.out.println("apiName: " + vectorApiException.getApiName());
            System.out.println("httpStatusCode: " + vectorApiException.getHttpStatusCode());
            System.out.println("code: " + vectorApiException.getCode());
            System.out.println("message: " + vectorApiException.getMessage());
            System.out.println("requestId: " + vectorApiException.getRequestId());
            System.out.println("responseContext: " + vectorApiException.getResponseContext().getBody());
        } catch (Exception e) {
            System.err.println("request exception, message : " + e.getMessage());
            e.printStackTrace();
        }
    }
}

```




