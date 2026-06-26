# TOML Schema 说明

本文件定义流体网络描述文件的 TOML 格式。

## 整体结构

```toml
[nodes]          # 节点定义，每个节点一个子表
[[edges]]        # 边定义，列表形式
[scenarios]      # 工况定义，每个工况一个子表
节点 ([nodes])
每个节点由唯一的 ID 标识，例如 [nodes.source1]。节点属性：

字段	类型	必填	说明
type	string	是	节点类型：source（源）、pump（泵）、valve（阀门）、load（负载）、junction（汇流点）
pressure	float	条件	对于 source 和 pump，表示出口压力
min_flow	float	仅 load	负载最小工作流量
min_pressure	float	仅 load	负载最小工作压力
initial_state	string	仅 valve	阀门初始状态："open" 或 "closed"，默认 "open"
边 ([[edges]])
每条边是一个管路，属性：

字段	类型	必填	说明
from	string	是	起始节点 ID
to	string	是	终止节点 ID
resistance	float	是	流阻系数 R
model	string	否	"linear" 或 "quadratic"，默认 "quadratic"（当前仅支持线性）
工况 ([scenarios])
每个工况是一个子表，例如 [scenarios.normal]。字段：

字段	类型	必填	说明
description	string	否	工况描述
node_states	array	是	节点状态修改列表，每个元素：{ node = "节点ID", 属性1 = 新值, ... }
