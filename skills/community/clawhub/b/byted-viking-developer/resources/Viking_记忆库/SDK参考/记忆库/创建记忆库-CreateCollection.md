# 接口概述
创建一个新的记忆库，用于存储和管理特定场景下的记忆数据。支持用户自定义记忆库存储的事件类型和画像类型，用于匹配具体业务场景下的数据建模需求。每个记忆库都拥有独立的记忆结构，如果业务场景中的记忆抽象不同，应创建新的记忆库。
# **请求接口**
| **URL** | /api/memory/collection/create | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对记忆库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 基于AK/SK生成的签名信息 |
# 请求参数
注：

* 原entity概念已替换为profile，建议统一替换为profile，原entity相关参数仍然兼容支持。
* "sys_profile_collect_v1"不再需要配置，配置"sys_profile_v1"时，平台会默认进行该事件的抽取与相关画像的更新。

| **参数名** | **类型** | **是否必须** | **描述** |
| --- | --- | --- | --- |
| CollectionName | String | 是 | 记忆库的唯一名称。只能使用英文字母、数字、下划线，**并以英文字母开头**。 |
| ProjectName | String | 否 | 项目名称。默认为 default。 |
| CollectionType | String | 否 <br>  | 记忆库的类型。默认为旗舰版。 <br>  <br> * standard：标准版记忆库，适用于小量级场景。最高支持2000万条向量和30QPS。标准版采用资源共享模式，价格更便宜。 <br> * ultimate：旗舰版记忆库，适用于大量级场景。向量条数和QPS不限。支持配置高额计算资源，性能更优。 |
| CpuQuota | Integer | 否 | 选择旗舰版时必传。范围[1, 100]。不传则默认为1CU，即1核8G，可支撑100QPS和约400万条向量。CPU超额后将限流，内存超额后将自动扩容。 |
| CollectionModalType | String | 否 | 记忆库的模态类型，默认为 text，需要输入多模态内容进行记忆抽取时，填写 multimodal。 |
| Description | String | 否 | 记忆库的描述信息，最多 10000 个字符。 |
| TtlRelative | Integer | 否 | 事件记忆的过期时间，单位为秒。不传则默认永不过期。为保证记忆的完整性，建议不要设置过低的值。范围: (0, 315576000] |
| BuiltinEventTypes | Array of String | 否 | 可选择内置提供的事件类型，可选值包括 "sys_event_v1"，会基于该内置模板生成自定义的事件类型。详细介绍见本节末尾。默认值为空。 |
| BuiltinProfileTypes | Array of String | 否 | 可选择内置提供的画像类型，可选值为 "sys_profile_v1"，会基于该内置模板生成自定义的画像类型。详细介绍见本节末尾。 |
| CustomEventTypeSchemas | Array of EventTypeSchema | 否 | 根据业务需求自定义的事件类型列表。 |
| * EventType | String | 是 | 事件类型的唯一名称，例如 "customer_feedback", "learning_progress"。 |
| * Description | String | 是 | 事件类型的详细描述，最多 10000 个字符。 |
| * Properties | Array of EventProperty | 是 | 构成此事件类型的属性列表。 |
|    * -PropertyName | String | 是 | 属性名称，例如 score, total_interactions。 |
|    * -PropertyValueType | String | 是 | 属性值的类型，可选值包括 ["int64", "list<int64>", "string", "list<string>", "float32", "bool"] |
|    * -Description | String | 是 | 属性的详细描述，最多 10000 个字符。 |
| * CustomWeightExpression  | String | 否 | 自定义事件权重表达式，可配置为固定值，或使用事件配置的多个字段于+-*/（）符号组合计算。 |
| CustomProfileTypeSchemas | Array of ProfileTypeSchema | 否 | 用户自定义的画像类型模式列表。 |
| * ProfileType | String | 是 | 画像类型的唯一名称，例如 user_profile, product_summary。 |
| * Description | String | 是 | 画像类型的详细描述，最多 10000 个字符。 |
| * UpdateTiming | String | 否 | 画像的更新触发时机。可选值如下： <br>  <br> *  realtime（默认）：事件产生后立即更新画像记忆。 <br> *  daily：每日更新画像记忆。在每日 00:00 触发，处理 *上次更新后至昨日 23:59* 期间产生的事件。 <br> *  weekly：每周更新画像记忆。在每周一 00:00 触发，处理 *上次更新后至上周日 23:59* 期间产生的事件。 <br> *  manual：仅在手动调用 TriggerUpdateProfile 接口时更新画像记忆。 |
| * UpdateMode | String | 否 | 在更新时机为 daily 或 weekly 时，控制画像记忆的更新方式。可选值如下： <br>  <br> *  overwrite（默认）：覆盖写入，在原有画像基础上更新内容。 <br> *  append：追加写入，每次更新生成一条新记忆。适用于日报、周报等保留历史记录的场景。 |
| * EnableAssistantIsolation | Boolean | 否 | 画像是否按照 assistant_id 隔离。默认为 True，即隔离。 |
| * Properties | Array of ProfileProperty | 是 | 构成此画像类型的属性列表。 |
|    * -PropertyName | String | 是 | 属性名称，例如 user_id, total_interactions。 |
|    * -PropertyValueType | String | 是 | 属性值的类型，可选值包括 ["int64", "list<int64>", "string", "list<string>", "float32", "bool"] |
|    * -Description | String | 是 | 属性的详细描述，最多 10000 个字符。 |
|    * -AggregateExpression | AggregateExpression | 否 | 聚合表达式，定义此属性如何从关联的事件中聚合计算而来。 |
|    * --Op | String | 否 | 聚合操作符，例如 SUM、MAX、AVG、COUNT、LLM_MERGE。 |
|    * --EventType | String | 否 | 参与聚合的事件类型名称。 |
|    * --EventPropertyName | String | 否 | 参与聚合的事件类型中的属性名称。 |
|    * -IsPrimaryKey | Boolean | 否 | 是否为画像的主键。默认为 false。 |
| Tags | Array of Tag | 否 | 标签，可用于资源管理和分账。 |
| * Key | String | 是 | 标签的键。 |
| * Value | String | 是 | 标签的值。 |
# 响应消息
| **字段** | **类型** | **描述** |
| --- | --- | --- |
| ResponseMetadata | Object | 响应元数据信息。 |
| * Action | String | 操作类型。 |
| * Region | String | 服务区域，例如"cn-beijing"。 |
| * RequestId | String | 请求唯一标识符 |
| * Service | String | 服务名称，如"knowledge_base_server"。 |
| * Version | String | API版本号。 |
| Result | Object | 实际业务数据。 |
| * ResourceId | String | 创建成功的记忆库资源 ID。 |
# 示例代码
## Python 代码
```Python
import json
import requests
from volcengine.base.Request import Request
from volcengine.Credentials import Credentials
from volcengine.auth.SignerV4 import SignerV4

AK = "your AK" 
SK = "your SK" 
Domain = "api-knowledgebase.mlp.cn-beijing.volces.com"

def prepare_request(method, path, ak, sk, data=None):
  r = Request()
  r.set_shema("http")
  r.set_method(method)
  r.set_host(Domain)
  r.set_path(path)

  if data is not None:
    r.set_body(json.dumps(data))
  credentials = Credentials(ak, sk, 'air', 'cn-north-1')
  SignerV4.sign(r, credentials)
  return r

def internal_request(method, api, payload, params=None):

  req = prepare_request(
                        method = method,
                        path = api,
                        ak = AK,
                        sk = SK,
                        data = payload)

  r = requests.request(method=req.method,
          url="{}://{}{}".format(req.schema, req.host, req.path),
          headers=req.headers,
          data=req.body,
          params=params,
      )
  return r
  
path = '/api/memory/collection/create'
playload = {
    'CollectionName': "my_first_memory_collection",
    'Description': "test description",
    'BuiltinEventTypes': ["sys_event_v1",],
    'BuiltinProfileTypes': ["sys_profile_v1"],
}
rsp = internal_request('POST', path, playload)
print(rsp.json())
```


# 附：模板Event和Profile说明
## sys_event_v1 
<a href="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/3a51ef404a364804b276fb54ead7610c~tplv-goo7wpa0wc-image.image" filename="sys_event_v1.py" download>sys_event_v1.py</a>
捕获对话中的所有重要事件。
| **属性名** | **数据类型** | **描述** |
| --- | --- | --- |
| summary | string | 基于字段内容编写的完整事实描述. |
## sys_profile_v1
<a href="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/bb0b12da8b5241659ef05dbc452ee531~tplv-goo7wpa0wc-image.image" filename="sys_profile_v1.py" download>sys_profile_v1.py</a>
基于原始对话更新的用户画像信息。
| **字段名** | **数据类型** | **描述** |
| --- | --- | --- |
| user_profile | string | 用户画像字段分为基础信息和兴趣偏好两类。基础信息包含生日、性别、年龄等 11 项内容，兴趣偏好涵盖人物、文学等 15 个领域； |
