# 概述
service_chat 支持基于一个已创建的知识服务进行检索/问答。
# 请求参数
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| service_resource_id | str | 是 | -- | **知识服务唯一 id** |
| messages | List[ChatMessage] | 是 | -- | **检索/问答多轮对话消息** <br> 格式为一问一答形式，发出消息的对话参与者角色，可选值包括： <br>  <br> * user：User Message 用户消息 <br> * assistant：Assistant Message 对话助手消息 <br>  <br> 其中 **最后一个元素 role == user ，content 为当前最新的提问 query** <br> **纯文本对话：** <br> 例如： <br> ```python <br> [ <br>     {"role": "user", "content": "你好"}, <br>     {"role": "assistant", "content": "你好！有什么我可以帮助你的？"}， <br>     {"role": "user", "content": "当前轮次用户问题"} <br> ] <br> ``` <br>  <br> **图文对话**： <br> 例如： <br> ```json <br> [ <br>     { <br>         "role": "user", <br>         "content": [ <br>             { <br>                 "type": "text", <br>                 "text": "推荐一个类似的适合 3 岁小孩的玩具" <br>             }, <br>             { <br>                 "type": "image_url", <br>                 "image_url": { <br>                     "url": "https://ark-project.tos-cn-beijing.volces.XXX.jpeg" #客户上传的图片，支持 URL/base 64 编码，协议详见：https://www.volcengine.com/docs/82379/1362931?lang=zh#477e51ce 和 https://www.volcengine.com/docs/82379/1362931?lang=zh#d86010f4 <br>                 } <br>             } <br>         ] <br>     } <br> ] <br> ``` <br>  |
| query_param | Optional[Dict[str, Any]] | 否 | nil | **检索过滤条件** <br> 在创建知识服务时如果您已配置了过滤条件，那么和该附加过滤条件一起生效，逻辑为 and <br>  <br> * 支持对 doc 的 meta 信息过滤 <br> * 详细使用方式和支持字段见 `https://www.volcengine.com/docs/84313/1419289#filter-%E8%A1%A8%E8%BE%BE%E5%BC%8F` ，可支持对 doc_id 做筛选 <br> * 此处用过过滤的字段，需要在 collection/create 时添加到 index_config 的 fields 上 <br>  <br> 例如： <br> 单层 filter： <br> ```json <br> doc_filter = { <br>    "op": "must", // 查询算子 must/must_not/range/range_out <br>    "field": "doc_id", <br>    "conds": ["tos_doc_id_123", "tos_doc_id_456"] <br> } <br> query_param = { <br>     "doc_filter": doc_filter <br> } <br> ``` <br>  <br> 多层 filter： <br> ```json <br> doc_filter = { <br>   "op": "and",   // 逻辑算子 and/or <br>   "conds": [     // 条件列表，支持嵌套逻辑算子和查询算子 <br>     { <br>       "op": "must", <br>       "field": "type", <br>       "conds": [1] <br>     }, <br>     { <br>         ...         // 支持>=1的任意数量的条件进行组合 <br>     } <br>   ] <br> } <br>  <br> query_param = { <br>     "doc_filter": doc_filter <br> } <br> ``` <br>  |
| stream | Optional[bool] | 否 | true | **是否采用流式返回** <br> 当创建的知识服务为问答类型服务时生效 |
# **响应消息**
检索/问答/流式的差异体现在 data 内字段是否出现及返回时机：
count、rewrite_query、result_list 通常在首流返回；token_usage 通常在尾流返回；generated_answer、reasoning_content 在中间流分段返回（SSE）。
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| code | Optional[int] | 状态码 |
| message | Optional[str] | 返回信息 |
| request_id | Optional[str] | 标识每个请求的唯一标识符 |
| data | Optional[ServiceChatData] | ServiceChatData |
### **ServiceChatData**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| count | Optional[int] | 检索结果返回的条数 |
| rewrite_query | Optional[str] | query 改写的结果 |
| token_usage | Optional[Any] | Token 使用信息 |
| result_list | Optional[List[ServiceChatRetrieveItem]] | 检索返回的信息 |
| generated_answer | Optional[str] | LLM 模型生成的回答 |
| reasoning_content | Optional[str] | 推理模型生成的内容 |
| prompt | Optional[str] | prompt 内容 |
| end | Optional[bool] | 是否结束（流式场景用于标识最后一段） |
### **ServiceChatRetrieveItem**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| id | Optional[str] | 索引的主键 |
| content | Optional[str] | 切片内容 <br> 1、非结构化文件：content 返回切片内容 <br> 2、faq 文件：content 返回答案 <br> 3、结构化文件：content 返回参与索引的字段和取值，以 K:V 对拼接，使用 \n 区隔 |
| md_content | Optional[str] | markdown 格式的解析结果（表格切片可通过 chunk_type == table 判断） |
| score | Optional[float] | 向量化语义检索得分 |
| point_id | Optional[str] | 切片 id |
| origin_text | Optional[str] | 原始文本 |
| original_question | Optional[str] | faq 数据检索召回答案对应的原始问题 |
| chunk_title | Optional[str] | 切片标题 |
| chunk_id | Optional[int] | 切片位次 id（代表在原始文档中的位次顺序） |
| process_time | Optional[int] | 检索耗时（s） |
| rerank_score | Optional[float] | 重排得分 |
| doc_info | Optional[ServiceChatRetrieveItemDocInfo] | ServiceChatRetrieveItemDocInfo |
| recall_position | Optional[int] | 向量化语义检索召回位次 |
| rerank_position | Optional[int] | 重排位次 |
| chunk_type | Optional[str] | 切片所属类型（如 doc-image、image、video、table、mixed-table、text、structured、faq 等） |
| chunk_source | Optional[str] | 切片来源 |
| update_time | Optional[int] | 更新时间 |
| chunk_attachment | Optional[List[ChunkAttachment]] | 检索召回附件的临时下载链接，有效期 10 分钟 |
| table_chunk_fields | Optional[List[PointTableChunkField]] | 结构化数据检索返回单行全量数据 |
| original_coordinate | Optional[Dict[str, Any]] | 切片在所属文档的原始位置坐标 |
### **ServiceChatRetrieveItemDocInfo**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| doc_id | Optional[str] | 文档 id |
| doc_name | Optional[str] | 文档名字 |
| create_time | Optional[int] | 文档的创建时间 |
| doc_type | Optional[str] | 知识所属原始文档的类型 |
| doc_meta | Optional[str] | 文档相关元信息 |
| source | Optional[str] | 知识来源类型 |
| title | Optional[str] | 知识所属文档的标题 |
### **ChunkAttachment**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| uuid | Optional[str] | 附件的唯一标识 |
| caption | Optional[str] | 图片所属标题，若未识别到标题则值为 "\n" |
| type | Optional[str] | image 等 |
| link | Optional[str] | 临时下载链接，有效期 10 分钟 |
| info_link | Optional[str] | 附件 info_link |
| column_name | Optional[str] | 附件列名 |
### **PointTableChunkField**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| field_name | Optional[str] | 字段名 |
| field_value | Optional[Any] | 字段值 |
# 请求示例
首次使用知识库 SDK ，可参考 [使用说明](unknown)
本示例演示了知识库 Python SDK 中 ServiceChat 的基础使用方法，包含普通调用和流式调用两种方式；该功能需使用 API Key 鉴权，且需配置知识服务 ID。
```Python
import os
from vikingdb.knowledge import VikingKnowledge
from vikingdb.auth import APIKey
from vikingdb.knowledge.models.service_chat import ServiceChatRequest
from vikingdb.knowledge.models.chat import ChatMessage

def main():
    # Note: ServiceChat usually uses API Key auth
    api_key = os.getenv("VIKING_SERVICE_API_KEY")
    endpoint = "api-knowledgebase.mlp.cn-beijing.volces.com"
    region = "cn-beijing"
    
    client = VikingKnowledge(
        host=endpoint,
        region=region,
        auth=APIKey(api_key=api_key),
        scheme="https"
    )
    
    # 1. Prepare messages
    messages = [
        ChatMessage(role="user", content="Help me find some documents.")
    ]
    
    # 2. Call ServiceChat
    try:
        resp = client.service_chat(ServiceChatRequest(
            service_resource_id=os.getenv("VIKING_SERVICE_RID", "your_service_resource_id"),
            messages=messages,
            stream=False
        ))
        print(f"Response: {resp}")
    except Exception as e:
        print(f"ServiceChat failed, err: {e}")

    # 3. Call ServiceChat stream
    try:
        resp = client.service_chat(ServiceChatRequest(
            service_resource_id=os.getenv("VIKING_SERVICE_RID", "your_service_resource_id"),
            messages=messages,
            stream=True
        ))
        for chunk in resp:
            print(f"Stream Response: {chunk}")
    except Exception as e:
        print(f"ServiceChat stream failed, err: {e}")


if __name__ == "__main__":
    main()
```


