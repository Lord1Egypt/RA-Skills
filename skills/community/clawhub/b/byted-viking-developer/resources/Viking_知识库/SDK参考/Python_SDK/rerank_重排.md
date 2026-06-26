本节将说明如何单独调用rerank模型，以计算两段文本间的相似度
## **概述**
rerank 用于重新批量计算输入文本与检索到的文本之间的 score 值，以对召回结果进行重排序。判断依据 chunk content 能回答 query 提问的概率，分数越高即模型认为该文本片能回答 query 提问的概率越大。
## **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| datas | List[RerankDataItem] | 是 | -- | **待重排的数据列表** <br> 每个元素为一个 map，数组长度不超过 200，支持以下参数： <br>  <br> * query（必选）：用于排序的查询内容，Any <br>    * str：纯文本查询内容，重排模型通用 <br>    * object：文或图查询内容，**仅适用于 doubao-seed-rerank 模型** <br> * content（必选）：待排序的文本内容，str <br> * image（可选）：待排序的图片内容，Optional[Union[str, List[str]]]，**仅适用于 doubao-seed-rerank 模型** <br>    * 支持传入公开访问的 http/https 链接 <br>    * 支持 jpeg、png、webp、bmp 格式的 base64 编码，单张图片小于 3 MB，请求体不能超过 4 MB <br> * title（可选）：文档的标题，Optional[str] |
| endpoint_id | Optional[str] | 否 | -- | **接入点 ID** |
| rerank_model | string | 否 | "base-multilingual-rerank" | **rerank 模型** <br> 可选模型： <br>  <br> * "doubao-seed-rerank"（即 doubao-seed-1.6-rerank）：字节自研多模态重排模型、支持文本 / 图片 / 视频 混合重排、精细语义匹配、可选阈值过滤与指令设置**（推荐）** <br> * "base-multilingual-rerank"：速度快、长文本、支持 70+ 种语言 <br> * "m3-v2-rerank"：常规文本、支持 100+ 种语言 |
| rerank_instruction | string | 否 | -- | **重排指令** <br> **仅当 rerank_model=="doubao-seed-rerank" 时生效**，用于提供给模型一个明确的排序指令，提升重排效果。字符串长度不超过 1024 <br> *如，Whether the document answers the query or matches the content retrieval intent* |
## **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| code | Optional[int] | 状态码 |
| message | Optional[str] | 错误信息 |
| request_id | Optional[str] | 请求的唯一标识符 |
| data | Optional[RerankResult] | RerankResult |
### **RerankResult**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| scores | List[float] | float 数组，与输入 datas 数组一一对应，表示每个文档与 query 的相关性得分 |
| token_usage | Optional[int] | 本次 rerank 调用消耗的总 token 数量 |
### **状态码说明**
| **状态码** | **http 状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 403 | VolcanoErrUnauthorized | 鉴权失败 |
| 1000002 | 400 | VolcanoErrInvalidRequest | 请求参数无效（当 query 缺失，或 datas 中所有文档都未提供任一媒体/文本内容时触发） |
| 300004 | 429 | VolcanoErrQuotaLimiter | 账户的 rerank 调用已达到配额限制 |
| 1000028 | 500 | VolcanoErrInternal | 服务内部错误，rerank模型过载 |
## 请求示例
首次使用知识库 SDK ，可参考 [使用说明](/docs/undefined/69a6aff55aca5705423bdde1)
本示例演示了知识库 Python SDK 中 rerank 函数的基础使用方法，通过传入查询语句和待排序文本列表实现结果重排序，使用前需配置 AK/SK 鉴权参数。
```Python
import os

from vikingdb.knowledge import VikingKnowledge
from vikingdb.auth import IAM
from vikingdb.knowledge.models.rerank import RerankDataItem

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
    
    datas = [
        RerankDataItem(query="What is VikingDB?", content="VikingDB is a vector database."),
        RerankDataItem(query="What is VikingDB?", content="The weather is good today.")
    ]
    
    try:
        resp = client.rerank(datas=datas)
        print(f"Response: {resp}")
    except Exception as e:
        print(f"Rerank failed, err: {e}")

if __name__ == "__main__":
    main()
```


