# 概述
get_point 用于查看知识库下的指定切片的信息
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project_name | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| resource_id | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project_name 作为知识库的唯一标识 |
| point_id | string | 是 | -- | **切片唯一 id** |
| get_attachment_link | bool | 否 | False | **是否获取切片中图片的临时下载链接** <br> 10 分钟有效期 |
# **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| code | Optional[int] | 状态码 |
| message | Optional[str] | 返回信息 |
| request_id | Optional[str] | 标识每个请求的唯一标识符 |
| data | Optional[PointInfo] | PointInfo |
### **PointInfo**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| collection_name | Optional[str] | 知识库名称 |
| point_id | Optional[str] | 切片 id（知识库下唯一） |
| process_time | Optional[int] | 切片处理完成的时间 |
| origin_text | Optional[str] | 原始文本 |
| md_content | Optional[str] | 切片 markdown 解析结果，保留更多的原始表格信息（chunk_type 为 table 时会返回） |
| html_content | Optional[str] | 切片 html 解析结果，保留更多的原始表格信息（chunk_type 为 table 时会返回） |
| chunk_title | Optional[str] | 切片标题，是由解析模型识别出来的上一层级的标题。若没有上一层级标题则为空 |
| chunk_type | Optional[str] | 切片所属类型 |
| description | Optional[str] | 文档描述（当前仅支持图片文档） |
| content | Optional[str] | 切片内容 |
| chunk_id | Optional[int] | 切片位次 id，代表在原始文档中的位次顺序 |
| original_question | Optional[str] | faq 数据检索召回答案对应的原始问题 |
| doc_info | Optional[PointDocInfo] | PointDocInfo |
| rerank_score | Optional[float] | 重排得分 |
| score | Optional[float] | 检索得分 |
| chunk_source | Optional[str] | 切片来源 |
| chunk_attachment | Optional[List[ChunkAttachment]] | 附件信息（get_attachment_link 为 True 时返回临时链接，10 分钟有效期） |
| table_chunk_fields | Optional[List[PointTableChunkField]] | 结构化数据检索返回单行全量数据 |
| update_time | Optional[int] | 更新时间 |
| chunk_status | Optional[str] | 切片状态 |
| video_frame | Optional[str] | 视频帧 |
| video_url | Optional[str] | 视频链接 |
| video_start_time | Optional[int] | 视频切片的起始时间（ms） |
| video_end_time | Optional[int] | 视频切片的结束时间（ms） |
| video_outline | Optional[Dict[str, Any]] | 视频大纲 |
| audio_start_time | Optional[int] | 音频切片的起始时间（ms） |
| audio_end_time | Optional[int] | 音频切片的结束时间（ms） |
| audio_outline | Optional[Dict[str, Any]] | 音频大纲 |
| sheet_name | Optional[str] | sheet 名称 |
| project | Optional[str] | 项目名 |
| resource_id | Optional[str] | 知识库唯一 id |
### **PointDocInfo**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| doc_id | Optional[str] | 所属文档 id |
| doc_name | Optional[str] | 所属文档名字 |
| create_time | Optional[int] | 文档创建时间 |
| doc_type | Optional[str] | 所属原始文档类型 |
| doc_meta | Optional[str] | 所属文档的 meta 信息 |
| source | Optional[str] | 所属文档知识来源（url，tos 等） |
| title | Optional[str] | 所属文档标题 |
| status | Optional[DocStatus] | DocStatus |
### **DocStatus**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| process_status | Optional[int] | 处理状态 |
| failed_code | Optional[int] | 失败错误码 |
| failed_msg | Optional[str] | 失败错误信息 |
### **ChunkAttachment**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| uuid | Optional[str] | 附件 uuid |
| caption | Optional[str] | 附件说明 |
| type | Optional[str] | 附件类型 |
| link | Optional[str] | 附件链接（临时下载链接，有效期 10 分钟） |
| info_link | Optional[str] | 附件 info_link |
| column_name | Optional[str] | 附件列名 |
### **PointTableChunkField**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| field_name | Optional[str] | 字段名 |
| field_value | Optional[Any] | 字段值 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection不存在 |
| 1001001 | 400 | doc not exist | doc不存在 |
| 1002001 | 400 | point not exist | point_id不存在 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Python SDK 中 GetPoint 函数的基础使用方法，通过指定知识库名称和知识点 ID 查询切片信息，使用前需配置 AK/SK 鉴权参数。
```Python
import os

from vikingdb.knowledge import VikingKnowledge
from vikingdb.auth import IAM

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
        resp = collection.get_point(point_id=point_id, get_attachment_link=True)
        print(f"Response: {resp}")
    except Exception as e:
        print(f"GetPoint failed, err: {e}")

if __name__ == "__main__":
    main()
```


