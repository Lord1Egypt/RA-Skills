# 飞书文档配置
# 用于 article-archiver skill

# 默认归档位置
DEFAULT_SPACE_ID="7527734827164909572"
DEFAULT_PARENT_NODE="NqZvwBqMTiTEtkkMsRoc76rznce"  # 学习资料抓取 → 待阅读

# 可选的归档位置（可以根据需要切换）
# 格式：LOCATION_NAME="space_id:parent_node_token"

# 学习资料抓取 → 待阅读（默认）
LOCATION_TO_READ="7527734827164909572:NqZvwBqMTiTEtkkMsRoc76rznce"

# 学习资料抓取（根目录）
LOCATION_ROOT="7527734827164909572:Lfj1d3Pcmo0o2IxrHrOcMsffnZb"

# 使用方法：
# 1. 修改 DEFAULT_PARENT_NODE 切换默认位置
# 2. 或在调用时指定：--parent-node <node_token>
