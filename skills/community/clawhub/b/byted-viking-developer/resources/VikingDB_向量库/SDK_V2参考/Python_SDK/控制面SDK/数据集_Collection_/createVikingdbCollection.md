# 概述
接口用于对向量数据库的创建，单账号下最多创建200个数据集。
* 每一个 Collection 必须指定主键字段。
* 当定义字段 fields 添加了一个向量类型 vector 的字段后，再添加新的字段时，字段类型不可选择 vector 类型。因为目前只支持单向量，不可添加多个向量字段。
* 创建数据集时，请根据数据类型明确配置方式：若为已有向量数据，请填写 vector 字段；若需对多模态数据（如图文）进行向量化，请配置 vectorize 参数。二者为不同的数据处理逻辑，创建时仅可选择其一，不可同时使用。
* 一个 Collection 里的 fields 数量上限是 200个。

# 方法定义
Python SDK 通过 `VIKINGDBApi().create_vikingdb_collection(request)` 发起调用，`request` 类型为 `volcenginesdkvikingdb.CreateVikingdbCollectionRequest`。
# **请求参数**
下表仅列出该接口特有的请求参数和部分公共参数。更多信息请见[公共参数](https://www.volcengine.com/docs/6369/67268)。
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| project_name | str | 否 | 项目名称，对应 API 字段 `ProjectName`，不填则默认当做default处理。 |
| collection_name | str | 是 | 数据集名称，对应 API 字段 `CollectionName` <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空 <br> * 长度（字节）要求：[1, 128] <br> * 同账号下，所有 Collection 名称不能重复 <br> * 同账号下， collection 数量不超过200个 |
| description | str | 否 | 数据集描述，对应 API 字段 `Description`，最长 65535 字节。 |
| fields | list[FieldForCreateVikingdbCollectionInput] | 是 | 字段定义列表，对应 API 字段 `Fields` <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空。 <br> * 长度（字节）要求：[1, 128] <br> * 同一个 Collection 下，Field 名称不能重复 <br> * 需包含至少一个主键字段（string/int64） <br> * 单个 collection 下，field 数量不超过200个 |
| vectorize | VectorizeForCreateVikingdbCollectionInput | 否 | 向量化配置，对应 API 字段 `Vectorize`，支持稠密/稀疏模型组合。 |

* FieldForCreateVikingdbCollectionInput 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| field_name | str | 是 | 字段名，对应 API 字段 `FieldName`。需以字母开头，可包含字母、数字、下划线，长度 1-128 字节。 |
| field_type | str | 是 | 字段类型，对应 API 字段 `FieldType`。可选值见下方 `field_type` 列表。 |
| default_value | object | 否 | 字段默认值，对应 API 字段 `DefaultValue`。vector / sparse_vector / text / image / video 类型不支持默认值。 |
| dim | int | 否 | 稠密向量维度，对应 API 字段 `Dim`。vector 字段必填，范围 4-4096，需为 4 的倍数。 |
| is_primary_key | bool | 否 | 是否为主键，对应 API 字段 `IsPrimaryKey`。仅 string / int64 字段可设为主键；如未指定，系统将生成 `"__AUTO_ID__"`。 |

* VectorizeForCreateVikingdbCollectionInput 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| dense | DenseForCreateVikingdbCollectionInput | 是 | 稠密向量化配置，对应 API 字段 `Dense`，用于指定 embedding 模型、维度与输入字段。 |
| sparse | SparseForCreateVikingdbCollectionInput | 否 | 稀疏向量化配置，对应 API 字段 `Sparse`。 |

* DenseForCreateVikingdbCollectionInput 和 SparseForCreateVikingdbCollectionInput 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| model_name | str | 是 | 模型名称，对应 API 字段 `ModelName`。可选值见下方 embedding 模型列表。 |
| model_version | str | 否 | 模型版本，对应 API 字段 `ModelVersion`。Doubao 系模型必填，bge 系默认 `default`。 |
| dim | int | 否 | 稠密向量维度。各模型支持的维度见embedding模型列表。 |
| text_field | str | 否 | 文本向量化字段名，对应 API 字段 `TextField`。 |
| image_field | str | 否 | 图片向量化字段名，对应 API 字段 `ImageField`。 |
| video_field | str | 否 | 视频向量化字段名，对应 API 字段 `VideoField`。 |
# field_type

| 字段类型 | 格式 | 可为主键 | 说明 |
| --- | --- | --- | --- |
| int64 | 整型数值 | 是 | 整数 <br>  <br> * 作为主键时，要求不能为0 |
| float32 | 浮点数值 | 否 | 浮点数 |
| string | 字符串 | 是 | 字符串。 <br>  <br> * 推荐使用方式：当用于枚举值过滤时，推荐长度不超过128字节 <br> * 硬性限制：要求不超过65535字节；当作为主键时，需满足长度不超过256字节 |
| bool | true/false | 否 | 布尔类型 |
| list<string> | 字符串数组 | 否 | 字符串数组 <br>  <br> * 推荐使用方式：当用于枚举值过滤时，列表长度不超过32个，单元素不超过1024字节 <br> * 硬性限制：列表长度不超过20000，单元素不超过1024字节，总大小不超过1MB |
| list<int64> | 整型数组 | 否 | 整数数组 <br>  <br> * 硬性限制：列表长度不超过1024 |
| vector | * 向量（浮点数数组） <br> * float32/float64压缩为bytes后的base64编码 | 否 | 稠密向量 <br>  <br> * 硬性限制：长度不小于4，不大于4096，且为4的整数倍数。 |
| sparse_vector <br>  | 输入格式的字典列表，来表征稀疏稀疏向量的非零位下标及其对应的值, 其中 token_id 是 string 类型, token_weight 是float 类型 | 否 | 稀疏向量 <br>  |
| text | 字符串 | 否 | 若为向量化字段，则值不能为空。（若否，可以为空） <br>  <br> * 若为向量化字段，则值不能为空。（若否，可以为空） <br> * 硬性限制：需小于65535字节 |
| image | 字符串 | 否 | 若为向量化字段，则值不能为空。（若否，可以为空） <br>  <br> * 图片tos链接 `tos://{bucket}/{object}` <br> * http/https格式链接 <br> * 对应图片需满足宽高长度大于14px，像素小于3600万 <br> * 可参考：[多模态向量化](https://www.volcengine.com/docs/82379/1409291?lang=zh#a256838b) |
| video | Object | 否 | 若为向量化字段，则值不能为空。（若否，可以为空） <br>  <br> * 视频tos链接 `tos://{bucket}/{object}` <br> * http/https格式url链接 <br> * 对应视频需满足大小不超过50mb <br> * 可参考：[多模态向量化](https://www.volcengine.com/docs/82379/1409291?lang=zh#a256838b) <br>  <br> ```Plain Text <br> { <br>     "value": tos://{bucket}/{object}     # 或http/https格式url链接，该字段必填 <br>     "fps": 0.2     # 取值0.2-5，选填 <br> } <br> ``` <br>  |
| date_time | string | 否 | 分钟级别： <br> `yyyy-MM-ddTHH:mmZ`或`yyyy-MM-ddTHH:mm±HH:mm` <br> 秒级别： <br> `yyyy-MM-ddTHH:mm:ssZ`或`yyyy-MM-ddTHH:mm:ss±HH:mm` <br> 毫秒级别： <br> `yyyy-MM-ddTHH:mm:ss.SSSZ`或`yyyy-MM-ddTHH:mm:ss.SSS±HH:mm` <br> 例如："2025-08-12T11:33:56+08:00" |
| geo_point | string | 否 | 地理坐标`longitude,latitude`，其中`longitude`取值(-180,180)，`latitude`取值(-90,90) <br> 例如："116.408108,39.915023" |
## 模型列表
| 模型名称 | 模型版本 | 支持向量化类型 | 默认稠密向量维度 | 可选稠密向量维度 | 文本截断长度 | 支持稀疏向量 | 可支持instruction <br>  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bge-large-zh | (default) | text | 1024 | 1024 | 512 | 否 | 是 |
| bge-m3 | (default) | text | 1024 | 1024 | 8192 | 是 | 否 |
| bge-visualized-m3 <br>  | (default) | text、image及其组合 | 1024 | 1024 | 8192 | 否 | 否 |
| doubao-embedding | *240715* | text | 2048 <br>  | 512, 1024, 2048 | 4096 | 否 | 是 <br>  |
| doubao-embedding-large | *240915* | text | 2048 | 512, 1024, 2048, 4096 | 4096 | 否 | 是 |
| doubao-embedding-vision | *250328* | text、image及其组合 | 2048 | 2048, 1024 <br>  | 8192 | 否 | 是 |
| doubao-embedding-vision | *250615* | 兼容*241215*和*250328*的用法*。​*另外，支持full_modal_seq（文/图/视频序列） | 2048 <br>  | 2048, 1024 <br>  | 128k | 否 | 是 |
# **返回参数**
下表仅列出本接口特有的返回参数。更多信息请参见[返回结构](https://www.volcengine.com/docs/6369/80336)。
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| message | str | 请求状态描述，对应 API 字段 `Message`。 |
| resource_id | str | 新建数据集 ID，对应 API 字段 `ResourceId`。 |
# 请求示例
### 创建带vector字段的数据集
```python
import os
import volcenginesdkcore
import volcenginesdkvikingdb as vdb
from volcenginesdkvikingdb.api.vikingdb_api import VIKINGDBApi

configuration = volcenginesdkcore.Configuration()
configuration.ak = os.environ["VIKINGDB_AK"]
configuration.sk = os.environ["VIKINGDB_SK"]
configuration.region = os.environ["VIKINGDB_REGION"]
configuration.host = os.environ["VIKINGDB_HOST"]
configuration.scheme = "https"
volcenginesdkcore.Configuration.set_default(configuration)

client = VIKINGDBApi()

request = vdb.CreateVikingdbCollectionRequest(
    collection_name="sdk_demo_collection",
    description="Create collection with vector fields",
    project_name="default",
    fields=[
        vdb.FieldForCreateVikingdbCollectionInput(
            field_name="item_id",
            field_type="int64",
            is_primary_key=True,
        ),
        vdb.FieldForCreateVikingdbCollectionInput(
            field_name="title",
            field_type="string",
        ),
        vdb.FieldForCreateVikingdbCollectionInput(
            field_name="dense_vector",
            field_type="vector",
            dim=768,
        ),
        vdb.FieldForCreateVikingdbCollectionInput(
            field_name="sparse_vector",
            field_type="sparse_vector",
        ),
        vdb.FieldForCreateVikingdbCollectionInput(
            field_name="f_int64",
            field_type="int64",
            default_value=123456,
        ),
    ],
)

response = client.create_vikingdb_collection(request)
print("message:", response.message)
print("resource_id:", response.resource_id)
```

### 创建带vectorize(向量化)的数据集
```python
import os
import volcenginesdkcore
import volcenginesdkvikingdb as vdb
from volcenginesdkvikingdb.api.vikingdb_api import VIKINGDBApi

configuration = volcenginesdkcore.Configuration()
configuration.ak = os.environ["VIKINGDB_AK"]
configuration.sk = os.environ["VIKINGDB_SK"]
configuration.region = os.environ["VIKINGDB_REGION"]
configuration.host = os.environ["VIKINGDB_HOST"]
configuration.scheme = "https"
volcenginesdkcore.Configuration.set_default(configuration)

client = VIKINGDBApi()

request = vdb.CreateVikingdbCollectionRequest(
    collection_name="sdk_demo_vectorize",
    description="Auto vectorize text and image",
    project_name="default",
    fields=[
        vdb.FieldForCreateVikingdbCollectionInput(
            field_name="doc_id",
            field_type="string",
            is_primary_key=True,
        ),
        vdb.FieldForCreateVikingdbCollectionInput(
            field_name="content",
            field_type="text",
        ),
        vdb.FieldForCreateVikingdbCollectionInput(
            field_name="cover_image",
            field_type="image",
        ),
        vdb.FieldForCreateVikingdbCollectionInput(
            field_name="f_int64",
            field_type="int64",
            default_value=123456,
        ),
    ],
    vectorize=vdb.VectorizeForCreateVikingdbCollectionInput(
        dense=vdb.DenseForCreateVikingdbCollectionInput(
            model_name="bge-m3",
            text_field="content",
        ),
        sparse=vdb.SparseForCreateVikingdbCollectionInput(
            model_name="bge-m3",
            text_field="content",
        ),
    ),
)

response = client.create_vikingdb_collection(request)
if response.resource_id:
    print("collection created:", response.resource_id)
else:
    print("request failed:", response.message)
```



