# 概述
add_point 用于新增知识库下文档的一个切片
# **请求参数**
| **参数** | **类型** | **必选** | **默认值** | **备注** |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project_name | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| resource_id | string | 否 | -- | **知识库唯一 id** <br>  <br> * 可选择直接传 resource_id，或同时传 collection_name 和 project_name 作为知识库的唯一标识 |
| doc_id | string | 是 | -- | **表示新增切片所属的文档** <br>  <br> * 不存在时会报错。 |
| chunk_type | string | 是 | -- | **要添加的切片类型** <br>  <br> * 和知识库支持的类型不匹配时会报错 <br> * 结构化知识库：“structured”， <br> * 非结构化知识库： <br> * “text”： 纯文本切片 <br> * “faq”： faq 类型切片 |
| content | string | 否 | -- | **新增切片文本内容** <br> 当 chunk_type 为 text、faq 时必传 <br> 1、text：content 对应切片原文内容 <br> 2、faq：content 对应**答案字段**内容 |
| chunk_title | string | 否 | -- | **切片标题** <br> 只有非结构化文档支持修改切片的标题。 |
| question | string | 否 | -- | **新增 faq 切片中的问题字段** <br> 当 chunk_type 为 faq 时必传 <br>  <br> * 字段长度范围为 [1，{Embedding模型支持的最大长度}] |
| fields | list | 否 | -- | **表示传入的结构化数据** <br> 当 chunk_type 为 structured 时必传。 <br> [ <br> { "field_name": "xxx" // 字段名称 <br> "field_value": xxxx // 字段值 <br> }, <br> ] <br>  <br> * field_name 必须已在所属知识库的表字段里配置，否则会报错 <br> * 和文档导入时的向量字段长度校验保持一致，拼接后的做 embedding 的文本长度不超过 65535 |
# **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| code | Optional[int] | 状态码 |
| message | Optional[str] | 返回信息 |
| request_id | Optional[str] | 标识每个请求的唯一标识符 |
| data | Optional[PointAddResult] | PointAddResult |
### **PointAddResult**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| collection_name | Optional[str] | 知识库的名字 |
| resource_id | Optional[str] | 知识库唯一标识 |
| project | Optional[str] | 项目名 |
| doc_id | Optional[str] | 文档 id |
| chunk_id | Optional[int] | 切片在文档下的 id，文档下唯一 |
| point_id | Optional[str] | 切片 id，知识库下唯一 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Python SDK 中 AddPoint 函数的基础使用方法，使用前需配置 AK/SK 鉴权参数。
```Python
import os

from vikingdb.knowledge import VikingKnowledge
from vikingdb.auth import IAM
from vikingdb.knowledge.models.point import AddPointRequest

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
    
    content = "Point content"
    question = "What is the point about?"
    chunk_title = "Point Highlights"
    
    try:
        resp = collection.add_point(AddPointRequest(
            doc_id="Your doc id", # Replace with a valid doc ID
            chunk_type="text",
            content=content,
            question=question,
            chunk_title=chunk_title,
            fields=[
                {"field_name": "topic", "field_type": "string", "field_value": "field value"}
            ]
        ))
        print(f"Response: {resp}")
    except Exception as e:
        print(f"AddPoint failed, err: {e}")

if __name__ == "__main__":
    main()
```


