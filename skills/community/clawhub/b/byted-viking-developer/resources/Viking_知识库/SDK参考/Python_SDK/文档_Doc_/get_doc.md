# 概述
get_doc 用于查看知识库下的文档信息。
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project_name | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/c8p1dfoq/y97x844a) <br> 若不指定该字段，则在 default 项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| resource_id | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project_name 作为知识库的唯一标识 |
| doc_id | string | 是 | -- | **要查询的文档 id** |
| return_token_usage | bool | 否 | false | **是否返回文档向量化和文档生成摘要所消耗的 tokens** |
# **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| code | Optional[int] | 状态码 |
| message | Optional[str] | 返回信息 |
| request_id | Optional[str] | 标识每个请求的唯一标识符 |
| data | Optional[DocInfo] | DocInfo |
### **DocInfo**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| collection_name | Optional[str] | 知识库名称 |
| doc_name | Optional[str] | 文档名称 |
| doc_id | Optional[str] | 文档 id |
| doc_hash | Optional[str] | 文档 hash |
| add_type | Optional[str] | 导入方式 |
| doc_type | Optional[str] | 文档类型 |
| description | Optional[str] | 文档描述（当前仅支持图片文档） |
| create_time | Optional[int] | 文档创建时间 |
| added_by | Optional[str] | 添加人 |
| update_time | Optional[int] | 文档更新时间 |
| url | Optional[str] | 原始文档链接 |
| tos_path | Optional[str] | tos 路径 |
| point_num | Optional[int] | 切片数量 |
| status | Optional[DocStatus] | DocStatus |
| title | Optional[str] | 文档标题 |
| source | Optional[str] | 知识来源（url，tos 等） |
| total_tokens | Optional[int] | token 统计 |
| doc_summary_tokens | Optional[int] | 摘要 token 统计 |
| doc_premium_status | Optional[DocPremiumStatus] | DocPremiumStatus |
| doc_summary | Optional[str] | 文档摘要 |
| brief_summary | Optional[str] | 简要摘要 |
| doc_size | Optional[int] | 文档大小 |
| meta | Optional[str] | meta 信息 |
| labels | Optional[Dict[str, str]] | 标签信息 |
| video_outline | Optional[Dict[str, Any]] | 视频大纲 |
| audio_outline | Optional[Dict[str, Any]] | 音频大纲 |
| statistics | Optional[Dict[str, Any]] | 统计信息 |
| project | Optional[str] | 项目名 |
| resource_id | Optional[str] | 知识库唯一 id |
### **DocStatus**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| process_status | Optional[int] | 处理状态 |
| failed_code | Optional[int] | 失败错误码 |
| failed_msg | Optional[str] | 失败错误信息 |
### **DocPremiumStatus**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| doc_summary_status_code | Optional[int] | 摘要状态码 |
## failed_code 报错码：
| **failed_code** | **错误描述** | **处理建议** |
| --- | --- | --- |
| 10001 | 文档下载超时 | 请上传重试。如果问题仍然存在，请联系我们 |
| 10003 | url 校验失败，请确认 url 链接 | 请确认 url 链接正确后重试。如果问题仍然存在，请联系我们 |
| 10005 | 飞书文档获取异常，请确认有效且授权 | 请确认飞书文档权限问题，通过飞书开放平台 OpenAPI [飞书开放平台](https://open.larkoffice.com/document/server-docs/docs/docs-overview)确认权限 |
| 30001 | 超过知识库文件限制大小 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 35001 | 超过知识库切片数量限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 35002 | FAQ 文档解析为空 | FAQ 文档解析结果为空，切片数为 0。请确保文档中包含有效数据 |
| 35004 | 超过知识库 FAQ 文档 sheet 数量限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 36003 | 结构化文档表头不匹配 | 结构化文档表头不匹配，请确保上传文档中每个 sheet 的表头与预定义的知识库表结构完全一致 |
| 36004 | 结构化文档数据类型转换失败 | 结构化文档数据类型转换失败，请确保上传文档中每个 sheet 的单元格的内容格式与预定义的知识库表结构数据类型完全一致 |
| 36005 | 超过知识库结构化文档 sheet 数量限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 36006 | 超过知识库结构化文档有效行数限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 36007 | 结构化文档解析为空 | 结构化文档解析结果为空，切片数为 0。请确保文档中包含有效数据 |
| 36008 | embedding 的列组合长度超出限制 | 缩短待 embedding 原始文本长度 |
| 其他错误码 | 未知错误，请联系我们 | 未知错误，请联系我们 |
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
本示例演示了知识库 Python SDK 中 GetDoc 的基础使用方法，通过指定知识库名称和文档 ID 实现单篇文档查询，使用前需配置 AK/SK 鉴权参数。
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
    
    # Replace with a valid doc ID from your collection
    doc_id = "Your doc id"
    
    try:
        resp = collection.get_doc(doc_id, return_token_usage=True)
        print(f"Response: {resp}")
    except Exception as e:
        print(f"GetDoc failed, err: {e}")

if __name__ == "__main__":
    main()
```


