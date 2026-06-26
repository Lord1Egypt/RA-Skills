---
name: "governance-asset-inventory"
description: "全域资产盘点：自动化扫描和登记数据库实例、库、表等资产，构建企业级数据地图。"
---

# 全域资产盘点 (Global Asset Inventory)

全域资产盘点是数据治理的第一步，旨在摸清“家底”，建立完整、准确的数据资产清单。通过自动化扫描，可以发现未登记的“影子资产”，监控资产规模变化。

## 核心目标

1.  **资产发现**：自动发现所有数据库实例、数据库和表。
2.  **变更监控**：识别新增或删除的资产。
3.  **资产统计**：统计各业务线的存储量、表数量等指标。
4.  **影子资产治理**：找出未在 CMDB 或元数据中心登记的数据库。

## 盘点流程

### 1. 实例层盘点

首先获取云账号下所有的数据库实例信息。

```python
from toolbox import create_client
client = create_client()

# 获取所有实例（支持分页）
instances = []
page = 1
while True:
    res = list_instances(client, page_number=page, page_size=50)
    if not res['success']:
        break
    data = res['data'].get('instances', [])
    if not data:
        break
    instances.extend(data)
    page += 1

print(f"共发现 {len(instances)} 个数据库实例")
```

**关注指标**：
-   实例 ID (`instance_id`)
-   实例名称 (`instance_name`)
-   实例类型 (`instance_type`): MySQL, Postgres, Redis 等
-   运行状态 (`status`): Running, Stopped 等
-   地域信息 (`region`)

### 2. 数据库层盘点

对每个运行中的实例，获取其包含的逻辑数据库列表。

```python
for inst in instances:
    if inst['status'] != 'Running':
        continue
        
    print(f"正在扫描实例: {inst['name']} ({inst['id']})")
    
    # 获取该实例下的数据库
    db_res = list_databases(client, instance_id=inst['id'], page_size=100)
    if db_res['success']:
        dbs = db_res['data'].get('databases', [])
        print(f"  - 发现 {len(dbs)} 个数据库")
        # TODO: 存入资产清单数据库
```

**关注指标**：
-   数据库名 (`db_name`)
-   字符集 (`charset`)
-   创建时间

### 3. 表级资产盘点

深入到每个数据库，获取表清单。这是构建数据地图的基础。

```python
# 伪代码示例
for db in dbs:
    table_res = list_tables(client,
        instance_id=inst['id'], 
        database=db['name'],
        page_size=100
    )
    if table_res['success']:
        tables = table_res['data'].get('tables', [])
        print(f"    - 库 {db['name']} 包含 {len(tables)} 张表")
```

## 盘点产出物

建议将盘点结果存储为结构化数据（如 Excel 或 数据库表），包含以下字段：

| 字段名 | 描述 | 示例 |
| :--- | :--- | :--- |
| `asset_id` | 资产唯一标识 | `inst-xxx.db_name.table_name` |
| `instance_name` | 实例名称 | `prod-main-db` |
| `db_name` | 数据库名称 | `order_center` |
| `table_name` | 表名称 | `t_order_main` |
| `owner` | 负责人 | `zhangsan` |
| `last_check_time` | 最后盘点时间 | `2024-03-20 10:00:00` |
| `status` | 状态 | `Active` / `Deleted` |

## 常见问题

-   **Q: 如何处理海量表的扫描？**
    -   A: 建议使用多线程或异步任务队列（Celery）并发扫描不同的实例。
-   **Q: 盘点频率多少合适？**
    -   A: 建议每日凌晨执行一次全量盘点，或者针对生产环境进行高频（每小时）的变更检测。
