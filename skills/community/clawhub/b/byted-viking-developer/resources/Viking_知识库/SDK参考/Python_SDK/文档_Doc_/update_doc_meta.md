# 概述
update_doc_meta 用于更新知识库上文档信息，文档 meta 信息更新会自动触发索引中的数据更新。
# **请求参数**
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| collection_name | -- | string | 否 | -- | **知识库名称** |
| project_name | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| resource_id | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project_name 作为知识库的唯一标识 |
| doc_id | -- | string | 是 | -- | **待更新文档的 id** |
| meta |  | List[MetaItem] | 否 | -- | **meta 信息** |
|  | field_name | Optional[str] | 否 | -- | **要更新的字段名** |
|  | field_type | Optional[str] | 否 | -- | **要更新的字段类型** <br>  <br> * 仅当新增知识库未配置过的标签字段时生效，且新增字段不能用于标量过滤，仅可作为当前文档的描述信息存储 <br> * 支持 "int64"，"float32"，"string"，"bool"，"list" 类型，限制参考[VikingDB的field_type规则和说明](https://www.volcengine.com/docs/84313/1254542#field-type-%E5%8F%AF%E9%80%89%E5%80%BC) |
|  | field_value | Optional[Any] | 否 | -- | **要更新的字段值** <br> 字段值需保证类型符合字段定义，如 "int64"，"float32"，"string" 等 |
# **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| code | Optional[int] | 状态码 |
| message | Optional[str] | 返回信息 |
| request_id | Optional[str] | 标识每个请求的唯一标识符 |
| data | Optional[Any] | 返回数据（通常为空） |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection不存在 |
| 1001001 | 400 | doc not exist | doc不存在 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Python SDK 中 UpdateDocMeta 函数的基础使用方法，通过指定知识库名称、文档 ID 和元数据信息（字段名、类型、值）修改文档元数据，使用前需配置 AK/SK 鉴权参数。
```Python
import os

from vikingdb.knowledge import VikingKnowledge
from vikingdb.auth import IAM
from vikingdb.knowledge.models.doc import MetaItem

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
    
    doc_id = "Your doc id"
    meta = [
        MetaItem(field_name="category", field_type="string", field_value="new_value")
    ]
    
    try:
        collection.update_doc_meta(doc_id=doc_id, meta=meta)
        print("UpdateDocMeta success")
    except Exception as e:
        print(f"UpdateDocMeta failed, err: {e}")

if __name__ == "__main__":
    main()
```


