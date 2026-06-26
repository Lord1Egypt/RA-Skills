本文介绍VikingDB 向量数据库/知识库支持的地域及访问域名。
## 注意事项
VikingDB 向量数据库/知识库当前域名解析的网段地址可能存在变动，请勿使用以下方式：

* 在机器中配置了仅能访问固定 IP 或 IP 段的 ACL 或安全组。
* 直接使用 IP 或在机器中直接配置了 TOS 的域名映射。
* CEN 企业专线中配置了访问固定 IP 或 IP 段的路由。

如果您确实有以上使用方式的需求，请[提交工单](https://console.volcengine.com/workorder/create?step=2&SubProductID=P00001544)联系技术支持人员。
## 地域及访问域名

* 地域（Region）：表示 VikingDB 向量数据库的数据所在物理位置。
* 访问域名（Endpoint）：表示 VikingDB 向量数据库对外服务的访问域名。


**火山引擎 VikingDB 向量数据库 支持的地域和访问域名如下表所示。**
其中**私网连接**请参阅[私网连接方式](/c8p1dfoq/wfkp3iey)，**获取内网域名**；
### API V2 数据面
| **Region 中文名称** | **Region ID** | 互联网域名（外网） | 私网连接终端节点服务（**非域名**，请参考[私网连接](https://www.volcengine.com/docs/84313/1254445)文档） |
| --- | --- | --- | --- |
| 华北2（北京） | cn-beijing | [api-vikingdb.vikingdb.cn-beijing.volces.com](http://api-vikingdb.vikingdb.cn-beijing.volces.com/) | [com.volces.privatelink.cn-beijing.vikingdb-ann](com.volces.privatelink.cn-beijing.vikingdb-ann) |
| 华南1（广州） | cn-guangzhou | [api-vikingdb.vikingdb.cn-guangzhou.volces.com](http://api-vikingdb.vikingdb.cn-guangzhou.volces.com/) | [com.volces.privatelink.cn-guangzhou.vikingdb-ann](com.volces.privatelink.cn-guangzhou.vikingdb-ann) |
| 华东2（上海） | cn-shanghai | [api-vikingdb.vikingdb.cn-shanghai.volces.com](http://api-vikingdb.vikingdb.cn-shanghai.volces.com/) | [com.volces.privatelink.cn-shanghai.vikingdb-ann](com.volces.privatelink.cn-shanghai.vikingdb-ann) |
| 亚太东南（柔佛） | ap-southeast-1 | [api-vikingdb.vikingdb.ap-southeast-1.volces.com](http://api-vikingdb.vikingdb.ap-southeast-1.volces.com/) | 火山柔佛region不支持私网访问 |
### API V2 控制面
| **Region 中文名称** | **Region ID** | 互联网域名（外网） | 私网连接终端节点服务（**非域名**，请参考[私网连接](https://www.volcengine.com/docs/84313/1254445)文档） |
| --- | --- | --- | --- |
| 华北2（北京） | cn-beijing | [vikingdb.cn-beijing.volcengineapi.com](http://vikingdb.cn-beijing.volcengineapi.com/) | com.volces.privatelink.cn-beijing.api.vikingdb |
| 华南1（广州） | cn-guangzhou | [vikingdb.cn-guangzhou.volcengineapi.com](http://vikingdb.cn-guangzhou.volcengineapi.com/) | com.volces.privatelink.cn-guangzhou.api.vikingdb |
| 华东2（上海） | cn-shanghai | [vikingdb.cn-shanghai.volcengineapi.com](http://vikingdb.cn-shanghai.volcengineapi.com/) | com.volces.privatelink.cn-shanghai.api.vikingdb |
| 亚太东南（柔佛） | ap-southeast-1 | [vikingdb.ap-southeast-1.volcengineapi.com](http://vikingdb.ap-southeast-1.volcengineapi.com/) | com.volces.privatelink.ap-southeast-1.api.vikingdb |
### API V1 
推荐使用V2新产品，功能迭代全面
| **Region 中文名称** | **Region ID** | 互联网域名（外网） | 私网连接终端节点服务（**非域名**，请参考[私网连接](https://www.volcengine.com/docs/84313/1254445)文档） |
| --- | --- | --- | --- |
| 华北2（北京） | cn-beijing | [https://api-vikingdb.volces.com](https://api-vikingdb.volces.com) | [com.volces.privatelink.cn-beijing.vikingdb-vector](com.volces.privatelink.cn-beijing.vikingdb-vector) |
| 华南1（广州） | cn-guangzhou | [https://api-vikingdb.mlp.cn-guangzhou.volces.com](https://api-vikingdb.mlp.cn-guangzhou.volces.com) | [com.volces.privatelink.cn-guangzhou.vikingdb-vector](com.volces.privatelink.cn-guangzhou.vikingdb-vector) |
| 华东2（上海） | cn-shanghai | [https://api-vikingdb.mlp.cn-shanghai.volces.com](https://api-vikingdb.mlp.cn-shanghai.volces.com) | [com.volces.privatelink.cn-shanghai.vikingdb-vector](com.volces.privatelink.cn-shanghai.vikingdb-vector) |
| 亚太东南（柔佛） | ap-southeast-1 | https://api-vikingdb.mlp.ap-mya.byteplus.com | 火山柔佛region不支持私网访问 |

**火山引擎 知识库 支持的地域和访问域名如下表所示。**
| **Region 中文名称** | **Region ID** | **Endpoint** |
| --- | --- | --- |
| 华北2（北京） | cn-beijing | * 外网：[https://api-knowledgebase.mlp.cn-beijing.volces.com](https://api-knowledgebase.mlp.cn-beijing.volces.com/) <br> * 终端节点服务（非域名，不可直接访问）：[com.volces.privatelink.cn-beijing.vikingdb-knowledge](com.volces.privatelink.cn-beijing.vikingdb-knowledge) |

