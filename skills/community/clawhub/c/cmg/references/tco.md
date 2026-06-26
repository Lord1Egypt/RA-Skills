# CMG 成本分析 (cmg-tco)

> ## 🚨🚨🚨 最高优先级规则：所有价格必须来自真实 API 查询或官方价格计算器 🚨🚨🚨
>
> **你（AI）绝对不可以自行估算、推测、编造任何价格数据！**
>
> - ❌ **禁止**：基于你的训练知识估算价格（你的知识已过时，云厂商价格随时变化）
> - ❌ **禁止**：使用"大约"、"估计"、"通常"等模糊价格（没有真实数据就不给价格）
> - ❌ **禁止**：当 API 调用失败时自己编一个价格凑数（应报错让用户处理）
> - ❌ **禁止**：跳过询价步骤直接给出"参考价格"（所有价格都必须经过真实查询）
> - ✅ **必须**：通过 `tco_pricing.py` 脚本调用云厂商 API 获取真实报价
> - ✅ **必须**：或通过浏览器访问云厂商官方价格计算器读取真实报价
> - ✅ **必须**：API 失败时明确告知用户"询价失败"并说明原因，请用户协助
> - ✅ **必须**：每条价格记录包含 `price_source` 字段标明真实数据来源
>
> **违反此规则产出的虚假价格将直接导致商业决策失误，后果灾难性且不可逆。**
> **宁可告诉用户"我无法获取价格"，也绝不能给出一个编造的数字。**

通过访问各云厂商官方价格计算器网页，完成资源询价并生成迁移前后 TCO 对比分析报告。

**数据来源：** 扫描清单 Excel（cmg-scan）、推荐配置清单（cmg-recommend）、或用户手动输入的资源配置。

## 核心流程

```
数据来源（三选一）
  ├─ 扫描清单 Excel (cmg-scan 产出)
  ├─ 推荐配置清单 (cmg-recommend 产出)
  └─ 用户手动输入配置
        │
        ▼
┌───────────────────────────────────┐
│      资源配置标准化                 │
│  提取产品类型、规格、地域、数量      │
│  按云厂商分组                      │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│   ⚠️ 各厂商价格获取（真实询价）      │
│   🚨 此步骤禁止估算/编造价格！       │
│                                   │
│  方式1(推荐): API 批量询价          │
│    → tco_pricing.py 调用真实 API   │
│  方式2(备选): 浏览器自动化          │
│    → 访问官方价格计算器读取真实报价  │
│                                   │
│  ❌ 禁止方式: 自行估算/推测/编造    │
│  ❌ API失败时: 报错,不要自己编价格  │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│      TCO 汇总与分析                │
│  生成 Excel 询价明细表             │
│  生成 HTML 可视化分析报告          │
│  源端 vs 目标端成本对比            │
└───────────────────────────────────┘
```

---

## 🚀 快速询价 (推荐方式: API 批量询价)

**⚠️ 这是获取真实价格的首选方式。** 通过 API 批量获取云厂商官方实时报价，比浏览器自动化快 10 倍以上。

> 🚨 **重要提醒**：执行 TCO 分析时，你**必须**运行下面的脚本来获取真实价格。
> 不要试图跳过这一步直接给用户"估算价格"——那样做会产生不准确的商业报价，后果严重。

### 方式1: 提供 AKSK 全自动 (扫描 + 询价 + 报告)

```bash
python3 {baseDir}/scripts/tco_pricing.py \
  --source aliyun \
  --ak <AccessKeyId> \
  --sk <AccessKeySecret> \
  --region cn-hangzhou \
  --title "XX项目迁移TCO分析" \
  --output-dir /tmp/tco_output
```

一条命令完成：扫描阿里云 ECS → 阿里云 DescribePrice API 批量询价 → 自动映射腾讯云规格 → 腾讯云 InquiryPriceRunInstances API 批量询价 → 生成 pricing_data.json → 生成 Excel + HTML 报告。

### 方式2: 从已有扫描结果询价

```bash
# 首次扫描会保存 scan_result.json，后续可直接复用
python3 {baseDir}/scripts/tco_pricing.py \
  --from-scan scan_result.json \
  --ak <AK> --sk <SK> \
  --title "XX项目迁移TCO分析"
```

### 方式3: 从手动配置文件询价

```bash
python3 {baseDir}/scripts/tco_pricing.py \
  --from-config resources.json \
  --ak <AK> --sk <SK> \
  --title "XX项目迁移TCO分析"
```

### 前置要求

- **阿里云**: 提供 AKSK (脚本内置签名计算，无需安装 aliyun-cli)
- **腾讯云**: 需要先安装并授权 tccli (`pip3 install tccli && tccli auth login`)
- **依赖**: `pip3 install openpyxl` (报告生成)

### 脚本内置能力

| 能力 | 说明 |
|------|------|
| 阿里云 API 签名 | 内置 HMAC-SHA1 签名，无需安装 aliyun-cli |
| 并行询价 | 多台实例并行调用 DescribePrice，速度 5x |
| 地域映射 | 阿里云 → 腾讯云地域自动映射 (如 cn-hangzhou → ap-shanghai) |
| 规格映射 | 按 CPU/内存 自动映射腾讯云 S5 系列 |
| 磁盘类型映射 | cloud_efficiency → CLOUD_PREMIUM 等 |
| 扫描结果缓存 | 首次扫描保存 scan_result.json，可复用 |

---

---

## 🔧 备选方式: 浏览器自动化询价

> 当 API 询价不可用时（如无 AKSK、需要查询非 ECS 产品），可退回浏览器自动化方式。
> 🚨 **即使使用浏览器方式，价格也必须从官方页面上真实读取，绝不能自行编造！**

## 支持的云厂商价格计算器

| 厂商 | 价格计算器 URL | 适用场景 |
|------|---------------|---------|
| **阿里云** | https://www.aliyun.com/price/product | 源端为阿里云时查询现有成本 |
| **华为云** | https://www.huaweicloud.com/pricing/calculator.html | 源端为华为云时查询现有成本 |
| **腾讯云** | https://buy.cloud.tencent.com/price | 目标端腾讯云询价（迁移目标） |
| **AWS** | https://calculator.aws/#/addService | 源端为 AWS 时查询现有成本 |
| **Azure** | https://azure.microsoft.com/en-us/pricing/calculator/ | 源端为 Azure 时查询现有成本 |
| **Google Cloud** | https://cloud.google.com/products/calculator?hl=zh-CN | 源端为 GCP 时查询现有成本 |

---

## 各厂商询价操作指南

> **前置要求：** 使用浏览器自动化工具（Skill 中配置 `browser-automation`）访问以下价格计算器页面。
> 每个厂商的操作步骤不同，下面按厂商分别说明。

### 1. 阿里云询价

**阿里云产品 → URL 路径映射：**
| 产品 | URL | 说明 |
|------|-----|------|
| ECS 云服务器 | `https://www.aliyun.com/price/product#/ecs/detail/vm` | 配置器模式，自动计算总价 |
| RDS MySQL | `https://www.aliyun.com/price/product#/rds/detail/rds` | |
| Redis | `https://www.aliyun.com/price/product#/kvstore/detail/kvstore` | |
| SLB 负载均衡 | `https://www.aliyun.com/price/product#/slb/detail/slb` | |
| OSS 对象存储 | `https://www.aliyun.com/price/product#/oss/detail/oss` | |
| EIP 弹性公网IP | `https://www.aliyun.com/price/product#/eip/detail/eip_pre` | |
| NAS 文件存储 | `https://www.aliyun.com/price/product#/nas/detail/nas` | |
| MongoDB | `https://www.aliyun.com/price/product#/mongodb/detail/mongodb` | |
| Elasticsearch | `https://www.aliyun.com/price/product#/elasticsearch/detail/elasticsearch` | |

---

#### 1.1 阿里云 ECS 询价（重点）

##### 价格组成规则（⚠️ 必读）

ECS 包月总价 = **实例费** + **系统盘费** + **数据盘费** + **带宽费**

各项费用**必须全部配置**才能得到正确总价。不能只查实例价格表（那里只显示实例费，不含磁盘和带宽）。

##### 推荐入口

**必须使用配置器页面**（自动计算总价）：`https://www.aliyun.com/price/product#/ecs/detail/vm`

该页面是一个完整的 ECS 配置器，选好所有参数后页面右下角会显示**预估费用**（包含实例+系统盘+数据盘+带宽的合计价），这就是我们需要的包月总价。

> ⚠️ **不要用** `#/ecs/detail/ecs-ee` 页面（实例价格表），那里只显示纯实例价格，不含磁盘和带宽。

##### 操作步骤

1. **打开配置器页面**
   - URL: `https://www.aliyun.com/price/product#/ecs/detail/vm`
   - 页面顶部有两个 Tab："云服务器 ECS（包年包月）" 和 "云服务器 ECS（按量付费）"
   - **默认选择"包年包月"** Tab（TCO 对比统一用包月价格）

2. **选择实例规格**
   - 页面上方会显示实例规格族列表
   - 根据扫描数据中的 `InstanceType` 找到对应的规格族和具体规格
   - 例如：`ecs.t6-c1m2.large` → 找到"突发性能实例 t6"族 → 选择 `ecs.t6-c1m2.large`
   - 确认 vCPU 和内存与扫描数据一致

3. **选择地域**
   - 在"地域"区域点击对应地域按钮
   - 例如：扫描数据 `RegionId: cn-hangzhou` → 点击"华东 1 (杭州)"

4. **配置操作系统**
   - 选择 Linux 或 Windows（影响实例价格）
   - 根据扫描数据的 `OSType` 字段判断

5. **配置系统盘** ⚠️ 关键步骤
   - **系统盘类型**：根据扫描数据的 `SystemDisk.Category` 字段选择
     - `cloud_efficiency` → 高效云盘
     - `cloud_ssd` → SSD 云盘
     - `cloud_essd` → ESSD 云盘（还需看 PL 等级）
     - `cloud_auto` → ESSD AutoPL 云盘
   - **系统盘大小**：根据扫描数据的 `SystemDisk.Size` 字段输入（单位 GiB）
   - 系统盘**默认值可能不是扫描数据中的值**，必须手动修改

6. **配置数据盘**
   - 如果扫描数据中有 `DataDisks`，需要逐一添加
   - 每块数据盘需配置：类型（同系统盘类型映射）+ 大小（GiB）
   - 如果没有数据盘，确保页面上数据盘数量为 0

7. **配置带宽**
   - **带宽计费方式**：根据扫描情况选择
     - 如果有固定带宽 → 选"按固定带宽"，输入带宽值（Mbps）
     - 如果是按流量计费或使用弹性公网 IP → 选"按使用流量"，带宽设为 0 Mbps
   - ⚠️ 对于使用 EIP 的实例，ECS 本身不含公网带宽费，应选"按使用流量 0 Mbps"，EIP 费用单独计算

8. **配置购买时长**
   - **统一选择"1个月"**（TCO 统一用月价格 × 12 算年费用）
   - 不要选包年（包年有折扣，会导致月价不准）

9. **读取预估费用**
   - 页面右下角会显示 **"预估费用 ¥xxx.xxx"**
   - 这个金额已经包含了 **实例 + 系统盘 + 数据盘 + 带宽** 的合计
   - 旁边有"费用明细"链接可以查看各项费用的拆分
   - **记录这个总价作为该 ECS 的包月费用**

##### 磁盘单价参考（用于验证，非操作步骤）

以下是阿里云各磁盘类型的**大致**包月单价，仅用于粗略验证，实际以配置器显示为准：

| 磁盘类型 | 产品代码 | 大致包月单价 |
|----------|---------|-------------|
| 高效云盘 | `cloud_efficiency` | ≈ ¥0.35/GiB/月 |
| SSD 云盘 | `cloud_ssd` | ≈ ¥1.00/GiB/月 |
| ESSD PL0 | `cloud_essd` PL0 | ≈ ¥0.50/GiB/月 |
| ESSD PL1 | `cloud_essd` PL1 | ≈ ¥1.00/GiB/月 |
| ESSD PL2 | `cloud_essd` PL2 | ≈ ¥2.00/GiB/月 |
| ESSD PL3 | `cloud_essd` PL3 | ≈ ¥4.00/GiB/月 |

> 以上单价可能随地域和时间变化，**仅用于粗略验证**总价是否合理。

##### 验证检查清单

完成询价后，执行以下检查确保结果准确：

- [ ] 实例规格与扫描数据的 `InstanceType` 完全一致
- [ ] 地域与扫描数据的 `RegionId` 一致
- [ ] 操作系统类型正确（Linux/Windows）
- [ ] 系统盘类型和大小与扫描数据一致
- [ ] 数据盘数量、类型、大小全部匹配
- [ ] 带宽配置正确（使用 EIP 的实例应选按流量 0 Mbps）
- [ ] 购买时长选的是"1个月"
- [ ] 记录的价格是"预估费用"总价（非仅实例价格）
- [ ] 点击"费用明细"确认各项费用拆分合理

##### 常见错误

| 错误 | 原因 | 正确做法 |
|------|------|---------|
| 价格偏低（只有实例费） | 用了价格表页面，没配置磁盘 | 用配置器页面 `#/ecs/detail/vm` |
| 价格偏高 | 带宽配了固定值但实际用 EIP | EIP 用户带宽选按流量 0 Mbps |
| 价格偏高 | 系统盘类型选错（SSD 选成了 ESSD） | 严格按扫描数据的 `SystemDisk.Category` |
| 价格偏高 | 购买时长选了包年，折算月价不准 | 统一选"1个月" |
| 价格偏低 | 漏了数据盘 | 检查扫描数据的 `DataDisks` |

---

#### 1.2 阿里云其他产品询价

**通用操作步骤：**

1. 打开对应产品的价格计算器页面（见上方 URL 表）
2. 根据扫描结果配置规格参数：
   - **RDS**：选择数据库引擎、实例规格、存储类型+空间、备份空间
   - **Redis**：选择架构（标准/集群）、内存规格、节点数
   - **SLB**：选择实例规格、带宽
   - **OSS**：选择存储类型、预估用量
   - **EIP**：选择带宽计费模式、带宽值
3. 页面会显示预估费用（按量/包年包月）
4. 记录费用数据：产品、规格、计费方式、单价、数量、小计

**关键页面元素：**
- 产品分类导航：左侧 Tab 切换
- 规格配置区域：表单中的下拉框、输入框
- 价格显示：页面右侧价格栏，通常包含"配置费用"或"预估费用"字段
- 计费周期切换：包年包月 / 按量计费 Tab

---

### 2. 华为云询价

**URL：** `https://www.huaweicloud.com/pricing/calculator.html`

> ⚠️ 华为云价格计算器功能可能未完全上线，备选方案：直接访问各产品的价格详情页。

**备选产品价格详情页：**
| 产品 | 价格详情 URL |
|------|-------------|
| ECS 云服务器 | `https://www.huaweicloud.com/pricing/calculator.html#/ecs` |
| RDS 数据库 | `https://www.huaweicloud.com/pricing/calculator.html#/rds` |
| Redis (DCS) | `https://www.huaweicloud.com/pricing/calculator.html#/dcs` |
| OBS 对象存储 | `https://www.huaweicloud.com/pricing/calculator.html#/obs` |
| ELB 负载均衡 | `https://www.huaweicloud.com/pricing/calculator.html#/elb` |
| EVS 云硬盘 | `https://www.huaweicloud.com/pricing/calculator.html#/evs` |

**操作步骤：**

1. 打开价格计算器页面或产品价格详情页
2. 选择计费模式（包年包月/按需计费）
3. 配置产品规格参数（地域、规格、磁盘等）
4. 读取页面上的价格信息
5. 记录费用数据

---

### 3. 腾讯云询价

**URL：** `https://buy.cloud.tencent.com/price/cvm/overview`

**腾讯云产品 → URL 路径映射：**
| 产品 | URL |
|------|-----|
| CVM 云服务器 | `https://buy.cloud.tencent.com/price/cvm/overview` |
| CDB MySQL | `https://buy.cloud.tencent.com/price/cdb/overview` |
| Redis | `https://buy.cloud.tencent.com/price/redis/overview` |
| CLB 负载均衡 | `https://buy.cloud.tencent.com/price/clb/overview` |
| COS 对象存储 | `https://buy.cloud.tencent.com/price/cos/overview` |
| CBS 云硬盘 | `https://buy.cloud.tencent.com/price/cbs/overview` |
| CFS 文件存储 | `https://buy.cloud.tencent.com/price/cfs/overview` |
| MongoDB | `https://buy.cloud.tencent.com/price/mongodb/overview` |
| ES Elasticsearch | `https://buy.cloud.tencent.com/price/es/overview` |
| CKafka | `https://buy.cloud.tencent.com/price/ckafka/overview` |

**操作步骤：**

1. 打开对应产品的价格总览页面
2. 切换到「价格计算器」Tab（部分产品叫「费用预算」）
3. 配置产品规格：
   - **CVM**：选择地域、可用区、实例规格（如 S5.LARGE8）、镜像、系统盘、数据盘、带宽、购买时长
   - **CDB**：选择数据库版本、架构（单节点/双节点/三节点）、实例规格、磁盘
   - **Redis**：选择版本、架构、内存、副本数
4. 页面实时计算并显示费用
5. 记录所有费用数据

**关键信息提取：**
- 配置费用数值
- 计费周期（月/年/按量）
- 各配置项的单独费用明细

---

### 4. AWS 询价

**URL：** `https://calculator.aws/#/addService`

**操作步骤：**

1. 打开 AWS Pricing Calculator
2. 点击 "Add service" 或搜索产品名
3. 选择产品（如 Amazon EC2、Amazon RDS 等）
4. 配置参数：
   - **EC2**：Region、OS、Instance Type (如 m5.xlarge)、Pricing Model (On-Demand/Reserved/Savings Plans)、Storage
   - **RDS**：Engine、Instance Class、Storage、Multi-AZ
   - **ElastiCache**：Engine、Node Type、Nodes
   - **S3**：Storage Class、Storage Amount、Requests
   - **ELB**：Type (ALB/NLB/CLB)、Processed Bytes
5. 点击 "Save and view summary"
6. 在 Summary 页面读取月费用

**AWS 产品搜索关键字：**
| 产品 | 搜索关键字 |
|------|-----------|
| EC2 | `Amazon EC2` |
| RDS | `Amazon RDS for MySQL/PostgreSQL/...` |
| ElastiCache | `Amazon ElastiCache` |
| S3 | `Amazon S3` |
| ELB | `Elastic Load Balancing` |
| EFS | `Amazon EFS` |
| EBS | `Amazon EBS` |
| MSK (Kafka) | `Amazon MSK` |
| OpenSearch | `Amazon OpenSearch Service` |

---

### 5. Azure 询价

**URL：** `https://azure.microsoft.com/en-us/pricing/calculator/`

**操作步骤：**

1. 打开 Azure Pricing Calculator
2. 在产品列表中选择或搜索产品
3. 产品会被添加到估算清单中
4. 配置每个产品的参数：
   - **Virtual Machines**：Region、OS、Type (如 D2s v3)、Tier、Payment Option (Pay as you go/1yr Reserved/3yr Reserved)
   - **SQL Database**：Service Tier、Compute、Storage
   - **Cache for Redis**：Tier、Instance
   - **Blob Storage**：Redundancy、Capacity
5. 页面底部自动显示月度估算费用
6. 可导出为 Excel

**Azure 产品分类：**
| 产品 | 分类路径 |
|------|---------|
| Virtual Machines | Compute > Virtual Machines |
| SQL Database | Databases > SQL Database |
| Redis Cache | Databases > Azure Cache for Redis |
| Blob Storage | Storage > Storage Accounts |
| Load Balancer | Networking > Load Balancer |
| Managed Disks | Storage > Managed Disks |

---

### 6. Google Cloud 询价

**URL：** `https://cloud.google.com/products/calculator?hl=zh-CN`

**操作步骤：**

1. 打开 Google Cloud Pricing Calculator
2. 点击 "Add to estimate" 按钮
3. 从产品列表中选择产品（如 Compute Engine、Cloud SQL 等）
4. 配置参数：
   - **Compute Engine**：Machine type (如 e2-standard-4)、Region、OS、Persistent disk
   - **Cloud SQL**：Database engine、Machine type、Storage、HA
   - **Memorystore**：Tier、Capacity
   - **Cloud Storage**：Location、Storage class、Amount
5. 右侧面板实时显示月度费用估算
6. 可下载为 CSV

**GCP 产品添加关键字：**
| 产品 | 搜索/选择名称 |
|------|-------------|
| 云服务器 | `Compute Engine` |
| 数据库 MySQL | `Cloud SQL for MySQL` |
| Redis | `Memorystore for Redis` |
| 对象存储 | `Cloud Storage` |
| 负载均衡 | `Cloud Load Balancing` |
| Kafka | `Managed Service for Apache Kafka` |
| Elasticsearch | `Elastic Cloud` |

---

## TCO 询价数据记录格式

每完成一个产品的询价，需要记录以下字段：

```json
{
  "vendor": "aliyun",
  "product": "ECS",
  "resource_id": "i-bp1abc...",
  "resource_name": "web-server-01",
  "region": "cn-hangzhou",
  "spec_summary": "ecs.c7.xlarge (4C8G) + 50G 高效云盘",
  "billing_mode": "monthly",
  "unit_price_monthly": 500.00,
  "quantity": 1,
  "subtotal_monthly": 500.00,
  "subtotal_yearly": 6000.00,
  "currency": "CNY",
  "price_source": "阿里云价格计算器",
  "query_time": "2026-03-24",
  "price_breakdown": {
    "instance": 400.00,
    "system_disk": "50GiB cloud_efficiency = 17.50",
    "data_disks": "无",
    "bandwidth": "按流量 0Mbps = 0"
  },
  "notes": ""
}
```

> `price_breakdown` 字段为可选但**强烈建议填写**。它记录价格拆分明细，方便后续验证和排错。对于 ECS 产品，应包含实例费、系统盘费、数据盘费、带宽费四项。`spec_summary` 也应包含磁盘信息（如 `+ 50G 高效云盘`）。

---

## TCO 分析报告

### 报告内容

询价完成后，执行汇总脚本生成 TCO 分析报告：

```bash
# 安装依赖（仅首次）
pip3 install openpyxl jinja2

# 生成 TCO 报告（Excel + HTML）
python3 {baseDir}/scripts/tco_report.py <pricing_data.json> [--title "XX项目迁移TCO分析"]
```

**输入：** `pricing_data.json` — 所有询价记录的 JSON 文件（格式见上方）

**输出：**
1. `tco_report_YYYYMMDD.xlsx` — Excel 询价明细 + 汇总表
2. `tco_report_YYYYMMDD.html` — 可视化 HTML 分析报告

### Excel 报告包含

| Sheet | 内容 |
|-------|------|
| 询价明细 | 所有资源的询价记录明细，按厂商+产品排列 |
| 按厂商汇总 | 各厂商的月度/年度总成本 |
| 按产品汇总 | 各产品类型的月度/年度总成本 |
| 成本对比 | 源端 vs 目标端（腾讯云）的成本对比，计算节省比例 |

### HTML 报告包含

1. **项目概览** — 资源总数、涉及厂商、总成本
2. **成本对比看板** — 源端 vs 腾讯云 月/年成本对比（柱状图）
3. **成本节省分析** — 各产品的节省金额和节省比例
4. **按产品明细** — 每种产品的详细成本分解
5. **按厂商明细** — 每个厂商的费用占比（饼图）
6. **询价明细表** — 全部询价记录的可排序表格

---

## 询价 JSON 文件结构

完整的 pricing_data.json 结构：

```json
{
  "project_name": "XX公司云迁移项目",
  "analysis_date": "2026-03-24",
  "source_vendor": "aliyun",
  "target_vendor": "tencent",
  "currency": "CNY",
  "pricing_items": [
    {
      "side": "source",
      "vendor": "aliyun",
      "product": "ECS",
      "resource_id": "i-bp1abc...",
      "resource_name": "web-server-01",
      "region": "cn-hangzhou",
      "spec_summary": "ecs.c7.xlarge (4C8G) + 50G 高效云盘",
      "billing_mode": "monthly",
      "unit_price_monthly": 500.00,
      "quantity": 1,
      "subtotal_monthly": 500.00,
      "subtotal_yearly": 6000.00,
      "currency": "CNY",
      "price_source": "阿里云价格计算器",
      "query_time": "2026-03-24",
      "price_breakdown": {
        "instance": 400.00,
        "system_disk": "50GiB cloud_efficiency = 17.50",
        "data_disks": "无",
        "bandwidth": "按流量 0Mbps = 0"
      },
      "notes": ""
    },
    {
      "side": "target",
      "vendor": "tencent",
      "product": "CVM",
      "resource_id": "",
      "resource_name": "web-server-01 (推荐)",
      "region": "ap-guangzhou",
      "spec_summary": "S5.LARGE8 (4C8G)",
      "billing_mode": "monthly",
      "unit_price_monthly": 450.00,
      "quantity": 1,
      "subtotal_monthly": 450.00,
      "subtotal_yearly": 5400.00,
      "currency": "CNY",
      "price_source": "腾讯云价格计算器",
      "query_time": "2026-03-24",
      "notes": "推荐规格"
    }
  ]
}
```

### side 字段说明

| 值 | 含义 |
|----|------|
| `source` | 源端（迁移前）— 当前云厂商的费用 |
| `target` | 目标端（迁移后）— 腾讯云的费用 |

---

## 询价工作流

### 场景 1：从扫描清单询价

```
1. 用户提供扫描结果 Excel（cmg-scan 产出）
2. 解析 Excel，提取资源列表（产品、规格、地域、数量）
3. 访问源端厂商价格计算器，逐项询价记录源端成本
4. 访问腾讯云价格计算器，按推荐规格逐项询价记录目标端成本
5. 汇总生成 pricing_data.json
6. 运行 tco_report.py 生成报告
```

### 场景 2：从推荐配置询价

```
1. 用户提供推荐配置清单（cmg-recommend 产出）
2. 解析推荐结果，提取源端规格 + 推荐规格
3. 访问源端厂商价格计算器，按源端规格询价
4. 访问腾讯云价格计算器，按推荐规格询价
5. 汇总生成 pricing_data.json
6. 运行 tco_report.py 生成报告
```

### 场景 4：从 recommend 产物文件询价（推荐）

```
1. 读取 cmg_recommend_result.json
2. 遍历 items，跳过 status=error 的条目
3. 从 src_params 提取源端规格 → 询源端厂商价格
4. 从 data 提取腾讯云推荐规格 → 询腾讯云价格
5. 汇总生成 pricing_data.json
6. 运行 tco_report.py 生成报告
```

### 场景 3：用户手动输入

```
1. 用户描述资源配置（如"阿里云 cn-hangzhou 8台 ecs.c7.xlarge"）
2. 逐条访问对应厂商价格计算器询价
3. 询问用户目标端规格或按等价规格推荐
4. 访问腾讯云价格计算器询价
5. 汇总生成 pricing_data.json
6. 运行 tco_report.py 生成报告
```

---

## 注意事项

> ### 🚨 第一条铁律：绝不估价
> **无论任何情况，你都不得自行估算/推测/编造价格。所有价格必须通过 tco_pricing.py API 调用或浏览器访问官方价格计算器获得。如果获取失败，向用户报告错误，不要试图用估算值替代。这是不可违反的红线。**

1. **价格完整性**：云服务器（ECS/CVM/EC2）价格必须包含实例+系统盘+数据盘+带宽的完整费用，不能只取实例价格
2. **使用配置器页面**：优先使用各厂商的"配置器"或"费用预算"页面（自动计算总价），而非"价格表"页面（只有单项价格）
3. **价格时效性**：云厂商价格随时可能调整，报告中必须标注询价日期
4. **计费模式统一**：对比时应统一计费模式（推荐统一用包月价格 × 12 计算年成本），购买时长统一选"1个月"
5. **币种统一**：跨国厂商注意币种转换（AWS/Azure/GCP 可能为 USD）
6. **折扣与优惠**：官网计算器通常显示刊例价，实际采购可能有商务折扣，报告中可增加折扣列
7. **页面变动**：云厂商可能更新网页结构，如遇到页面元素变化需适配
8. **价格验证**：每条询价记录完成后，应记录 `price_breakdown` 费用拆分，便于验证和排错
9. **EIP 单独计价**：使用弹性公网 IP (EIP) 的实例，EIP 费用应单独一条记录，ECS 侧带宽费为 0
10. **🚨 价格来源强制标注**：每条 pricing_item 的 `price_source` 字段必须填写真实来源（如"阿里云 DescribePrice API"、"腾讯云 InquiryPriceRunInstances API"、"阿里云价格计算器网页"），不得留空
11. **🚨 禁止估价替代**：当某台资源的 API 询价失败时，不得用估算值替代，应在结果中标注该条目为"询价失败"，并在 notes 字段说明失败原因

---

## 🚫 询价失败处理规范

当 API 调用或浏览器询价失败时，**必须按以下流程处理**：

```
询价失败
  │
  ├─ 单条失败 → 在该条目标注 "询价失败"
  │   ├─ price_source: "询价失败"
  │   ├─ unit_price_monthly: 0 (不要填估算值！)
  │   ├─ notes: "API报错: <具体错误信息>"
  │   └─ 继续处理其他资源
  │
  ├─ 批量失败 → 向用户报告错误
  │   ├─ 说明失败原因（AKSK无效/网络超时/权限不足等）
  │   ├─ 建议解决方案
  │   └─ 等待用户确认后重试
  │
  └─ ❌ 绝对禁止的做法：
      ├─ 自行编一个"差不多"的价格
      ├─ 用历史知识中的价格替代
      ├─ 用其他规格的价格推算
      └─ 跳过失败项不说明
```

**记住：一个标注为"询价失败"的 0 元记录，远比一个编造的虚假价格要好得多。**

## 常见问题

**Q: 价格计算器页面加载很慢或无法访问**
- 确保网络可以正常访问目标厂商官网
- 部分厂商（AWS/Azure/GCP）可能需要科学上网
- 华为云价格计算器可能功能不全，可改用各产品单独的价格详情页

**Q: 怎么处理非标产品/自定义配置**
- 在 notes 字段中标注特殊说明
- 询价时选择最接近的规格，并备注差异

**Q: 不同厂商的产品如何对应**
- 参考 `{baseDir}/references/products.md` 中的产品对照表
- 参考 `{baseDir}/references/recommend.md` 中的产品映射关系
