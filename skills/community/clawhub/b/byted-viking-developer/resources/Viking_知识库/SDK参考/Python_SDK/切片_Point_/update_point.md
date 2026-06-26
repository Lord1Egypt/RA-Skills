# 概述
update_point 用于更新知识库下的切片内容
# **请求参数**
| 参数 | 类型 | 必选 | 默认值 | 备注 |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project_name | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| resource_id | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project_name 作为知识库的唯一标识 |
| point_id | string | 是 | -- | **要更新的切片 id** |
| chunk_title | string | 否 | -- | **切片标题** <br> 只有非结构化文档支持修改切片的标题。 |
| content | string | 二者只传一个 | -- | **要更新的非结构化文档的切片内容** <br>  <br> * 1、非结构化文件：content 对应切片原文内容 <br> * 2、faq 文件：content 对应答案字段内容 <br> * 3、结构化文件：content 对应参与索引的字段和取值，以 K:V 对拼接，使用 \n 区隔 |
| fields | list |  | -- | **要更新的结构化文档的切片内容** <br> 一行数据全量更新 <br> [ <br> { "field_name": "xxx" // 字段名称 <br> "field_value": xxxx // 字段值 <br> }, <br> ] <br> field_name 必须已在所属知识库的表字段里配置，否则会报错 |
| question | string | 否 | -- | **要更新的非结构化 faq 文档切片的问题字段** |
# **响应消息**
| 字段 | 类型 | 备注 |
| --- | --- | --- |
| code | Optional[int] | 状态码 |
| message | Optional[str] | 返回信息 |
| request_id | Optional[str] | 标识每个请求的唯一标识符 |
| data | Optional[Any] | 返回数据（通常为空） |
## **状态码说明**
| code | message | 备注 | http status_code |
| --- | --- | --- | --- |
| 0 | success | 成功 | 200 |
| 1000001 | unauthorized | 缺乏鉴权信息 | 401 |
| 1000002 | no permission | 权限不足 | 403 |
| 1000003 | invalid request：%s | 非法参数 | 400 |
| 1000005 | collection not exist | collection不存在 | 400 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Python SDK 中 UpdatePoint 函数的基础使用方法，通过指定知识库名称和切片 ID 修改切片内容，使用前需配置 AK/SK 鉴权参数。
```Python
import os

from vikingdb.knowledge import VikingKnowledge
from vikingdb.auth import IAM
from vikingdb.knowledge.models.point import UpdatePointRequest

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
    
    point_id = "your_point_id"
    
    try:
        collection.update_point(point_id=point_id, update=UpdatePointRequest(
            content="updated content"
        ))
        print("UpdatePoint success")
    except Exception as e:
        print(f"UpdatePoint failed, err: {e}")

if __name__ == "__main__":
    main()
```


