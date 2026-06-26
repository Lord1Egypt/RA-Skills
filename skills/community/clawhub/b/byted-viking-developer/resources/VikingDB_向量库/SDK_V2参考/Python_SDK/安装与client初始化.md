向量数据库 Viking DB 现已提供 Python SDK，可直接在数据面（Data / Search / Embedding）完成鉴权、读写、检索与向量化操作。使用前请先完成 SDK 安装与客户端初始化。
# 前提条件

1. 已通过 [注册账号及开通服务](https://www.volcengine.com/docs/84313/1254444)。
2. 已获取火山引擎 AK / SK。详情参考 [Access Key（密钥）管理](https://www.volcengine.com/docs/6291/65568)。
3. 准备可用的 Python 3.9+ 运行环境，并具备安装第三方依赖的权限。

# 安装 SDK
Python 版 SDK 已发布到 PyPI，可选择直接安装发行版或在源码目录中以开发模式安装。
## 1. 数据面依赖配置

1. 使用 pip 安装发行版

推荐通过 pip 或 uv 获取最新稳定版本：
```bash
uv add vikingdb-python-sdk
// or 
python3 -m pip install -U vikingdb-python-sdk
```

安装完成后可通过 `python3 -m pip show vikingdb-python-sdk` 验证版本。

2. 在源码目录中安装

若需调试最新源码，请克隆仓库并以 editable 模式安装：
```bash
git clone https://github.com/volcengine/vikingdb-python-sdk.git
cd vikingdb-python-sdk
uv sync
```

SDK 依赖 `volcengine`、`requests`、`pydantic` 等组件。若处于离线网络，请提前准备对应的离线包。

## 2. 控制面依赖配置

1. 使用 pip 安装发行版

推荐通过 pip 或 uv 获取最新稳定版本：
```bash
uv add volcengine-python-sdk
// or 
python3 -m pip install volcengine-python-sdk
```

安装完成后可通过 `python3 -m pip volcengine-python-sdk` 验证版本。
# 初始化 SDK
初始化步骤包含三部分：配置网络出口（域名/Region）、准备鉴权信息、构造客户端并发起一次请求以验证连通性。
示例代码使用环境变量 `VIKINGDB_AK` / `VIKINGDB_SK` / `VIKINGDB_HOST` / `VIKINGDB_REGION` 等，请在运行前设置好对应值。


1. **数据面 (Data / Search / Embedding)**

数据面域名供 `VikingVector`、`CollectionClient`、`IndexClient` 以及 Embedding 接口使用。
| **Region 中文名称** | **Region ID** | 互联网域名（外网） | 私网连接终端节点服务（**非域名**） |
| --- | --- | --- | --- |
| 华北2（北京） | cn-beijing | [api-vikingdb.vikingdb.cn-beijing.volces.com](http://api-vikingdb.vikingdb.cn-beijing.volces.com/) | com.volces.privatelink.cn-beijing.vikingdb-ann |
| 华南1（广州） | cn-guangzhou | [api-vikingdb.vikingdb.cn-guangzhou.volces.com](http://api-vikingdb.vikingdb.cn-guangzhou.volces.com/) | com.volces.privatelink.cn-guangzhou.vikingdb-ann |
| 华东2（上海） | cn-shanghai | [api-vikingdb.vikingdb.cn-shanghai.volces.com](http://api-vikingdb.vikingdb.cn-shanghai.volces.com/) | com.volces.privatelink.cn-shanghai.vikingdb-ann |
| 亚太东南（柔佛） | ap-southeast-1 | [api-vikingdb.vikingdb.ap-southeast-1.volces.com](http://api-vikingdb.vikingdb.ap-southeast-1.volces.com/) | 该 Region 暂不支持私网访问 |
```python
import os
from vikingdb import IAM
from vikingdb.vector import SearchByRandomRequest, UpsertDataRequest, VikingVector

client = VikingVector(
    host=os.environ["VIKINGDB_HOST"],
    region=os.environ["VIKINGDB_REGION"],
    auth=IAM(ak=os.environ["VIKINGDB_AK"], sk=os.environ["VIKINGDB_SK"]),
    scheme="https",
)

collection_name=os.environ["VIKINGDB_COLLECTION"]
index_name=os.environ["VIKINGDB_INDEX"]

upsert_resp = client.collection(collection_name=collection_name).upsert(UpsertDataRequest(data=[{"text": "something"}]))
response = client.index(collection_name=collection_name,index_name=index_name).search_by_random(SearchByRandomRequest(limit=5))
hits = len(response.result.data) if response.result else 0
if response.result:
    for item in response.result.data:
        print(item.id, item.score, item.fields.get("text"))
```


2. **控制面 (Collection / Index / Task)**

控制面用于管理集合、索引与任务编排，目前仍通过火山引擎 OpenAPI 提供服务。可以复用 `volcengine-python-sdk` 或自定义 HTTP 客户端，只需确保使用下列域名并带上 AK/SK 鉴权签名。
| **Region 中文名称** | **Region ID** | 互联网域名（外网） | 私网连接终端节点服务（**非域名**） |
| --- | --- | --- | --- |
| 华北2（北京） | cn-beijing | [vikingdb.cn-beijing.volcengineapi.com](http://vikingdb.cn-beijing.volcengineapi.com/) | com.volces.privatelink.cn-beijing.api.vikingdb |
| 华南1（广州） | cn-guangzhou | [vikingdb.cn-guangzhou.volcengineapi.com](http://vikingdb.cn-guangzhou.volcengineapi.com/) | com.volces.privatelink.cn-guangzhou.api.vikingdb |
| 华东2（上海） | cn-shanghai | [vikingdb.cn-shanghai.volcengineapi.com](http://vikingdb.cn-shanghai.volcengineapi.com/) | com.volces.privatelink.cn-shanghai.api.vikingdb |
| 亚太东南（柔佛） | ap-southeast-1 | [vikingdb.ap-southeast-1.volcengineapi.com](http://vikingdb.ap-southeast-1.volcengineapi.com/) | com.volces.privatelink.ap-southeast-1.api.vikingdb |
控制面 OpenAPI 可通过 `volcengine-python-sdk` 的通用 `ApiClient` 调用，也可使用 `requests` 手动构造签名。调用方式与数据面一致：设置 X-Date、Authorization，再向上述域名的 HTTPS 接口发送 JSON 请求。

```Plain Text
import volcenginesdkvikingdb as vdb
from volcenginesdkvikingdb.api.vikingdb_api import VIKINGDBApi

client = VIKINGDBApi(
    ak="your_VIKINGDB_AK",
    sk="your_VIKINGDB_SK",
    host="your_VIKINGDB_HOST",
    region="your_VIKINGDB_REGION",
    scheme="https",
)
```

