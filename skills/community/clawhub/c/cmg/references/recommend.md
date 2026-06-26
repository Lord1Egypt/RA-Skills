# CMG 选型推荐 (cmg-recommend)

将友商云资源（阿里云/华为云/IDC）自动映射为等价的腾讯云规格。

**执行层**：通过 mcporter 调用远端 MCP Server，无需 JobID，实时返回推荐结果。

---

## 首次使用 — 自动设置

当用户首次触发推荐请求时，先检查环境：

```bash
{baseDir}/scripts/setup.sh --check-only
```

若 mcporter 未安装或未配置，直接运行：

```bash
{baseDir}/scripts/setup.sh --setup
```

脚本会自动使用内置默认地址完成：安装 mcporter、写入 `~/.mcporter/mcporter.json`、验证连通性。**无需重启客户端，立即可用。无需向用户询问地址。**

---

## 执行策略

### 第一步：规格去重（必须执行，大幅减少 MCP 调用次数）

> **推荐引擎对相同输入返回确定性结果**，因此相同规格的多台实例只需调用一次。

去重 key 由以下字段组合确定（所有字段相同 = 同一规格）：

| 产品 | 去重 key 字段 |
|------|-------------|
| CVM | `vendor` + `cpu` + `memory` + `src_instance_family` + `src_region_id` + `os_type` + `system_disk(type+size)` |
| MySQL | `vendor` + `cpu` + `memory` + `total_disk` + `src_region_id` + `engine_version` + `architecture` + `instance_type` |
| Redis | `vendor` + `capacity` + `src_region_id` + `version` + `architecture` |
| MongoDB | `vendor` + `cpu` + `memory` + `total_disk` + `src_region_id` + `mongodb_version` + `cluster_type` |
| 其他产品 | `vendor` + `src_region_id` + 各产品的关键规格参数 |

**去重流程：**
```
解析 Excel / 用户输入
    ↓
按产品类型分组
    ↓
每个产品内按 key 去重 → 得到唯一规格列表
    ↓
只对唯一规格调用 MCP（不是对每台实例调用）
    ↓
推荐结果按 key 映射回所有实例（一对多展开）
    ↓
保存 cmg_recommend_result.json（每台实例一条记录，data 字段指向对应推荐结果）
```

**示例：**
```
输入：100 台 ECS，实际只有 8 种规格组合
→ 只调用 8 次 MCP（而非 100 次）
→ 每种规格的推荐结果复制给对应的所有实例
```

---

### 第二步：按产品类型并行调用

去重后，按以下策略调用 MCP：

```
去重后的唯一规格列表
    │
    ├─ 检查 mcporter 是否可用（which mcporter && 配置存在）
    │    ├─ 可用 → 直接调用 mcporter（见下方）
    │    └─ 不可用 → 运行 setup.sh 安装配置
    │
    ├─ 单个资源，参数明确
    │    └─ 调对应单品工具（recommend_cvm / recommend_mysql / ...）
    │
    ├─ 多个资源（仅含 CVM/MySQL/Redis/MongoDB）
    │    └─ 全部打包进一次 recommend_batch（内部并发 5）
    │
    ├─ 多个资源（含其他产品：CBS/CLB/EIP/NAT/VPN/ES/CKafka 等）
    │    ├─ CVM/MySQL/Redis/MongoDB 部分 → 一次 recommend_batch
    │    └─ 其余产品 → 并行调用各单品工具（同时发起，不要串行等待）
    │
    ├─ 提供扫描 Excel 文件
    │    ├─ python3 {baseDir}/scripts/summarize.py <file.xlsx>  获取资源总览
    │    ├─ 用 openpyxl 读取各 Sheet 提取详细规格参数
    │    └─ 去重 → 按上述策略调用
    │
    └─ 参数不完整（缺 CPU/内存/地域等必填字段）
         └─ 向用户追问缺失参数，不要猜测
```

**判断 mcporter 是否可用**：`which mcporter` 且 `cat ~/.mcporter/mcporter.json | grep cmg-recommend` 有输出。

---

## mcporter 调用格式

```bash
mcporter call cmg-recommend.<tool_name> \
  --config ~/.mcporter/mcporter.json \
  --output json \
  --args '<JSON参数>'
```

列出所有可用工具：
```bash
mcporter list cmg-recommend --config ~/.mcporter/mcporter.json --schema
```

---

## 工具清单

### 计算类

#### recommend_cvm
将源端云服务器推荐为腾讯云 CVM 规格。

**必填**：`vendor`、`cpu`、`memory`、`src_region_id`

| 参数 | 类型 | 说明 |
|------|------|------|
| `vendor` | string | `aliyun` / `huaweicloud` / `idc` |
| `cpu` | number | CPU 核数，如 2、4、8 |
| `memory` | number | 内存 GB，如 4、8、16 |
| `src_region_id` | string | 源端地域 ID |
| `src_instance_family` | string | 源端实例族，如阿里云 `g7`、`c7`；华为云 `c6`。**非 IDC 必填**，不填引擎返回空结果 |
| `os_type` | string | `linux`（默认）/ `windows` |
| `system_disks` | array | `[{"disk_type":"cloud_essd","disk_size":50}]` |
| `data_disks` | array | 格式同 system_disks |
| `strategy` | string | `standard`（默认）/ `cost` |
| `tencent_region_id` | string | 目标地域，不填则自动映射 |

```bash
mcporter call cmg-recommend.recommend_cvm \
  --config ~/.mcporter/mcporter.json --output json \
  --args '{"vendor":"aliyun","cpu":4,"memory":8,"src_region_id":"cn-beijing","src_instance_family":"g7","os_type":"linux"}'
```

#### recommend_cbs
将源端云硬盘推荐为腾讯云 CBS。

**必填**：`vendor`、`disk_type`、`disk_size`、`src_region_id`

```bash
mcporter call cmg-recommend.recommend_cbs \
  --config ~/.mcporter/mcporter.json --output json \
  --args '{"vendor":"aliyun","disk_type":"cloud_essd","disk_size":200,"src_region_id":"cn-beijing"}'
```

---

### 数据库类

#### recommend_mysql
**必填**：`vendor`、`cpu`、`memory`、`total_disk`、`src_region_id`

可选：`engine_version`（5.6/5.7/8.0）、`architecture`（`SingleNode`/`DoubleNode`/`Finance`/`Cluster`，**推荐引擎必填**）、`instance_type`（`BASIC_V2`/`UNIVERSAL`/`EXCLUSIVE`/`CLOUD_NATIVE_CLUSTER`/`CLOUD_NATIVE_CLUSTER_EXCLUSIVE`，**推荐引擎必填**）

```bash
mcporter call cmg-recommend.recommend_mysql \
  --config ~/.mcporter/mcporter.json --output json \
  --args '{"vendor":"aliyun","cpu":4,"memory":8,"total_disk":100,"src_region_id":"cn-shanghai","engine_version":"5.7","architecture":"DoubleNode","instance_type":"EXCLUSIVE"}'
```

#### recommend_redis
**必填**：`vendor`、`capacity`（GB）、`src_region_id`

可选：`version`（`4.0`/`5.0`/`6.0`/`7.0`）、`architecture`（`standalone`/`cluster`/`sentinel`/`standard`）

```bash
mcporter call cmg-recommend.recommend_redis \
  --config ~/.mcporter/mcporter.json --output json \
  --args '{"vendor":"aliyun","capacity":4,"src_region_id":"cn-beijing","version":"6.0","architecture":"sentinel"}'
```

#### recommend_mongodb
**必填**：`vendor`、`cpu`、`memory`、`total_disk`、`src_region_id`

可选：`mongodb_version`、`cluster_type`（REPLSET/SHARD）

#### recommend_postgresql
**必填**：`vendor`、`cpu`、`memory`、`total_disk`、`src_region_id`

可选：`engine_version`（9.5/10/11/12/13/14）

#### recommend_sqlserver
**必填**：`vendor`、`cpu`、`memory`、`total_disk`、`src_region_id`

可选：`engine_version`（2012/2014/2016/2017/2019）、`instance_type`（`HA`/`SI`）

---

### 存储类

#### recommend_cos
**必填**：`vendor`、`src_region_id`

可选：`bucket_type`（standard/infrequent）

```bash
mcporter call cmg-recommend.recommend_cos \
  --config ~/.mcporter/mcporter.json --output json \
  --args '{"vendor":"aliyun","src_region_id":"cn-hangzhou"}'
```

---

### 网络类

| 工具 | 额外必填参数 | 可选枚举 | 说明 |
|------|------------|---------|------|
| `recommend_vpc` | 无 | - | VPC → 腾讯云 VPC |
| `recommend_clb` | 无 | `network_type`（`INTERNAL`/`BGP`）、`ip_version`（`IPv4`/`IPv6`/`IPv6_Nat`）、`instance_type`（`shared`/`exclusive`） | SLB/ELB → CLB |
| `recommend_eip` | `bandwidth_limit`（Mbps） | - | 弹性公网 IP |
| `recommend_nat` | 无 | - | NAT 网关 |
| `recommend_vpn` | 无 | `vpn_type`（`SSL`/`IPSEC`） | VPN 网关 |

所有网络工具均需 `vendor` + `src_region_id`。

---

### 中间件类

| 工具 | 额外可选参数 | 枚举值 | 说明 |
|------|------------|-------|------|
| `recommend_es` | `es_version`、`license_type`、`multi_zone_deploy` | `license_type`：`oss`/`basic`/`platinum`；`multi_zone_deploy`：`1`/`2`/`3` | Elasticsearch → 腾讯云 ES |
| `recommend_ckafka` | `spec_type`、`io_max`、`disk_size` | `spec_type`：`profession`/`premium` | Kafka → CKafka |

---

### 批量推荐

#### recommend_batch
一次调用推荐多个资源，并发执行（最大并发 5）。

**支持产品**：`CVM`、`MySQL`、`Redis`、`MongoDB`（其他产品用单品工具）

```bash
mcporter call cmg-recommend.recommend_batch \
  --config ~/.mcporter/mcporter.json --output json \
  --args '{
    "requests": [
      {
        "product": "CVM",
        "vendor": "aliyun",
        "params": {"cpu":4,"memory":8,"src_region_id":"cn-beijing","src_instance_family":"g7"}
      },
      {
        "product": "MySQL",
        "vendor": "aliyun",
        "params": {"cpu":4,"memory":8,"total_disk":100,"src_region_id":"cn-beijing","engine_version":"5.7"}
      },
      {
        "product": "Redis",
        "vendor": "aliyun",
        "params": {"capacity":4,"src_region_id":"cn-beijing","version":"6.0"}
      }
    ]
  }'
```

返回格式：
```json
[
  {"index": 0, "product": "CVM", "vendor": "aliyun", "data": {...}},
  {"index": 1, "product": "MySQL", "vendor": "aliyun", "data": {...}},
  {"index": 2, "product": "Redis", "vendor": "aliyun", "error": "...（若失败）"}
]
```

单条失败不影响其他条目。

---

## 地域 ID 参考

### 阿里云 → 腾讯云地域映射

| 阿里云 | 腾讯云（自动映射） |
|--------|-----------------|
| `cn-beijing` | `ap-beijing` |
| `cn-shanghai` | `ap-shanghai` |
| `cn-hangzhou` | `ap-shanghai` |
| `cn-shenzhen` | `ap-guangzhou` |
| `cn-guangzhou` | `ap-guangzhou` |
| `cn-chengdu` | `ap-chengdu` |
| `ap-southeast-1` | `ap-singapore` |
| `us-east-1` | `na-ashburn` |

### 华为云地域

| 华为云 | 说明 |
|--------|------|
| `cn-north-4` | 华北四（北京） |
| `cn-south-1` | 华南一（广州） |
| `cn-east-2` | 华东二（上海） |
| `cn-east-3` | 华东三（上海二） |

不填 `tencent_region_id` 时，引擎自动按地理位置映射。

---

## 推荐结果输出规范

每次完成推荐后，**必须将结果保存为 JSON 文件**，供后续 cmg-tco 步骤直接消费，避免结果只存在于对话上下文中。

### 输出文件

默认路径：`cmg_recommend_result.json`（当前工作目录，可由用户指定）

### 格式

```json
{
  "generated_at": "2026-03-25T10:00:00",
  "source_vendor": "aliyun",
  "items": [
    {
      "index": 0,
      "product": "CVM",
      "vendor": "aliyun",
      "status": "ok",
      "src_params": { "cpu": 4, "memory": 8, "src_region_id": "cn-beijing", "src_instance_family": "g7" },
      "data": { <mcporter 原始返回，原样透传，不做任何修改> }
    },
    {
      "index": 1,
      "product": "MySQL",
      "vendor": "aliyun",
      "status": "ok",
      "src_params": { "cpu": 4, "memory": 8, "total_disk": 100, "src_region_id": "cn-beijing" },
      "data": { <mcporter 原始返回> }
    },
    {
      "index": 2,
      "product": "Redis",
      "vendor": "aliyun",
      "status": "error",
      "src_params": { "capacity": 4, "src_region_id": "cn-beijing" },
      "error": "推荐引擎调用失败: ..."
    }
  ]
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `generated_at` | 生成时间（ISO 8601） |
| `source_vendor` | 源端云厂商（`aliyun` / `huaweicloud` / `idc` / `aws`） |
| `items[].index` | 条目序号，与调用顺序对应 |
| `items[].product` | 产品类型（`CVM` / `MySQL` / `Redis` 等） |
| `items[].vendor` | 该条目的源端厂商 |
| `items[].status` | `ok`（推荐成功）/ `error`（推荐失败） |
| `items[].src_params` | 调用时传入的源端参数，原样记录（用于 tco 查找源端规格） |
| `items[].data` | mcporter 返回的原始推荐结果，**原样透传，不做任何字段修改** |
| `items[].error` | 仅 `status=error` 时存在，记录失败原因 |

### 写入方式

推荐完成后，用以下 Bash 命令将结果写入文件：

```bash
# 将推荐结果 JSON 写入文件（python3 保证 UTF-8 + 格式化输出）
echo '<JSON内容>' | python3 -c "
import sys, json
data = json.load(sys.stdin)
with open('cmg_recommend_result.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('已保存到 cmg_recommend_result.json')
"
```

或直接在拼装完整 JSON 后用重定向写入：

```bash
python3 -c "
import json, datetime
result = {
    'generated_at': datetime.datetime.now().isoformat(timespec='seconds'),
    'source_vendor': 'aliyun',
    'items': [ <推荐结果列表> ]
}
with open('cmg_recommend_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print('已保存到 cmg_recommend_result.json')
"
```

### 与 cmg-tco 的衔接

cmg-tco 步骤可直接读取 `cmg_recommend_result.json`：
- `src_params` 提供源端规格，用于查询源端价格
- `data` 提供腾讯云推荐规格，用于查询目标端价格
- `status=error` 的条目跳过询价，在报告中标注"推荐失败"

---

## 常见问题

**Q: mcporter 调用返回 "connection refused"**
- 先运行 `{baseDir}/scripts/setup.sh --check-only` 检查配置
- 确认 MCP Server 已正常运行，地址配置正确

**Q: 推荐返回 "推荐引擎调用失败"**
- MCP Server 后端的 recommend-engine gRPC 服务未启动
- 联系服务运维确认 `RECOMMEND_ENGINE_ADDR` 对应服务状态

**Q: 推荐结果规格偏大/偏小**
- 使用 `strategy: "cost"` 切换成本优先策略
- 或通过 `tencent_region_id` 指定目标地域，不同地域售卖机型不同

**Q: recommend_batch 中某些产品不在支持列表（如 CBS、CLB）**
- batch 工具目前仅支持 CVM/MySQL/Redis/MongoDB
- 其他产品单独调用对应工具（recommend_cbs、recommend_clb 等）
