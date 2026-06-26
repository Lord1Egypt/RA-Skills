# 概述
add_doc_v2 用于向已创建的知识库添加文档。
# **请求参数**
| **参数** | **类型** | **是否必传** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| collection_name | Optional[str] | 否 | -- | 知识库名称 |
| project_name | Optional[str] | 否 | default | 知识库所属项目，获取方式参考文档 [API 接入与技术支持](https://www.volcengine.com/docs/84313/1606319?lang=zh#1ab381b9) <br> 若需要操作指定项目下的知识库，需正确配置该字段 |
| resource_id | Optional[str] | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project_name 作为知识库的唯一标识 |
| doc_id | Optional[str] | 是 | -- | **知识库下的文档唯一标识** <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母或下划线开头，不能为空 <br> * 长度要求：[1, 128] |
| doc_name | Optional[str] | 否 | -- | **文档名称** <br>  <br> * 对于 tos 导入的方式，未传入时直接使用 tos path 下面的文档名 <br> * 对于 url 导入的方式，先通过 url 提取带后缀的文档名，如果没有则返回错误码 400，要求用户再传 doc_name <br>  <br> 格式要求： <br>  <br> * 不能包含有特殊用途的字符(< > : " / \ <br> * 长度要求：[1, 255] |
| doc_type | Optional[str] | 否 | -- | **上传文档的类型** <br>  <br> * 非结构化文档支持类型：txt, doc, docx, pdf, markdown, pptx, ppt, jpeg, png, webp, bmp, mp4, mp3, wav, aac, flac, ogg <br> * .jpg 和 .jpeg 文件 doc_type 均为 jpeg <br> * .markdown 和 .md 文件 doc_type 均为 markdown <br> * 结构化文档支持类型：xlsx, csv, jsonl <br>  <br> 优先使用传入的值；若未传入，将尝试自动提取；若自动提取失败，则接口返回错误 |
| description | Optional[str] | 否 | -- | **文档描述** <br> 描述会参与对图片的检索，如电商场景下，描述可以用于存放图片对应的详细商品说明，售卖亮点，价格等 <br> 注： <br>  <br> * 暂**只在** doc_type 为**图片类型文档时支持**，其他类型文档设置无效。 <br> * 长度 [0，4000] |
| tag_list | Optional[List[MetaItem]] | 否 | -- | Tag 为结构体，包含 <br>  <br> * field_name：标签名，类型为string <br> * 不能为 "doc_id" <br> * 需对齐创建知识库时的 field_name <br> * 在创建知识库时先初始化标签索引，再在上传文档时打标，以用于检索时实现标签过滤能力 <br> * 若需新增过滤标签，请先编辑知识库新增标签后，再进行文档打标 <br> * field_type：标签类型 <br> * 支持 "int64"，"float32"，"string"，"bool"，"list"，"list" ，"date_time"，"geo_point" 类型 <br> * 需对齐创建知识库时的 field_type <br> * field_value：标签值 <br> * 与 field_type 指定类型一致 |
| uri | Optional[str] | 是 | -- | 待上传的文件 uri 链接，示例： <br>  <br> * http://a/b/c.pdf <br> * tos://a/b/c.pdf |
# **响应消息**
| **参数** | **类型** | **参数说明** | **备注** |
| --- | --- | --- | --- |
| code | Optional[int] | 状态码 |  |
| message | Optional[str] | 返回信息 |  |
| request_id | Optional[str] | 标识每个请求的唯一标识符 |  |
| data | Optional[AddDocResponseData] | AddDocResponseData |  |
### **AddDocResponseData**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| collection_name | Optional[str] | 知识库的名字 |
| resource_id | Optional[str] | 知识库唯一标识 |
| project | Optional[str] | 项目名 |
| doc_id | Optional[str] | 文档唯一标识 |
| task_id | Optional[int] | 任务 id |
| dedup_info | Optional[DedupInfo] | DedupInfo |
| more_info | Optional[str] | 更多信息 |
### **DedupInfo**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| skip | Optional[bool] | 是否跳过（去重命中） |
| same_doc_ids | Optional[List[str]] | 重复的文档 id 列表 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection 不存在 |
| 1001002 | 400 | invalid request: doc_id:xxx is duplicated with doc_ids:xxx | 文档内容与现有文档重复 |
| 1001010 | 400 | doc num is exceed 3000000 | doc 数量已达限额，点击详情查看[知识库配额限制](https://www.volcengine.com/docs/84313/1339026) |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Python SDK 中 AddDocV2 函数的基础使用方法，使用前需配置 AK/SK 鉴权参数。
```Python
import os

from vikingdb.knowledge import VikingKnowledge
from vikingdb.auth import IAM
from vikingdb.knowledge.models.doc import AddDocV2Request, MetaItem

def main():
    access_key = os.getenv("VIKINGDB_AK")
    secret_key = os.getenv("VIKINGDB_SK")
    endpoint = "api-knowledgebase.mlp.cn-beijing.volces.com"
    region = "cn-beijing"
    
    client = VikingKnowledge(
        host=endpoint,
        region=region,
        auth=IAM(ak=access_key, sk=secret_key),
        scheme="https"
    )
    
    collection = client.collection(
        collection_name="Your collection name",
        project_name="default",
    )
    
    try:
        resp = collection.add_doc_v2(AddDocV2Request(
            doc_id="Your doc id",
            doc_name="Your new doc name",
            doc_type="doc",
            uri="Your doc link url",
            tag_list=[
                MetaItem(field_name="tag key", field_type="string", field_value="tag value")
            ]
        ))
        print(f"Response: {resp}")
    except Exception as e:
        print(f"AddDocV2 failed, err: {e}")

if __name__ == "__main__":
    main()
```


