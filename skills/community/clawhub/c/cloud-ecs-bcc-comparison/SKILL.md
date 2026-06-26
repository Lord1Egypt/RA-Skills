---
name: cloud-ecs-bcc-comparison
description: >
  阿里云ECS与百度智能云BCC云主机规格智能对标询价工具。
  用户输入CPU核数、内存大小、磁盘规格（类型/容量）、带宽类型及大小、地域等参数，
  自动匹配计算型/通用型/内存型实例族的对应规格，并输出两家云厂商的预付费1个月价格。
  支持Skill文档外规格的智能匹配（按处理器主频/睿频/CPU/内存推断），
  若阿里云对应实例售罄则降代处理并说明。严禁输出非预付费1个月以外的价格。
---

# 云主机规格智能对标询价技能

通过调用阿里云 DescribePrice API 和百度智能云 BCC/CDS/EIP 询价 API，对相同配置的云主机进行实时价格对比。

> **价格输出原则（严格执行）**：
> - 本技能**仅输出预付费（包年包月）1个月**的价格，严禁输出按量付费、按年、按小时折算或其他计费方式的价格。
> - 带宽计费若用户选择"按流量计费"，则带宽项仅显示单价，不影响实例和磁盘的包月对比。

---

## 首次使用 — 自动设置

当用户首次要求查询云主机价格对比时，按以下流程操作：

### 步骤 1：检查当前状态

```bash
{baseDir}/../alicloud_ecs_price-1.0.0/scripts/setup.sh --check-only
```

```bash
{baseDir}/../baidu-bcc-price-1.0.1/scripts/setup.sh --check-only
```

如果输出显示两家云凭证均已配置，跳到「执行策略」。

### 步骤 2：如果未配置，引导用户提供凭证

**阿里云凭证配置：**
> 我需要你的阿里云凭证来查询 ECS 价格。请提供：
> 1. **AccessKeyId** — 阿里云 AK
> 2. **AccessKeySecret** — 阿里云 SK
>
> 可在 [阿里云控制台 > 访问控制 > AccessKey 管理](https://ram.console.aliyun.com/manage/ak) 获取。

```bash
{baseDir}/../alicloud_ecs_price-1.0.0/scripts/setup.sh --ak "<AK>" --sk "<SK>" --region "cn-beijing"
```

**百度智能云凭证配置：**
> 我需要你的百度智能云凭证来查询 BCC 价格。请提供：
> 1. **AccessKeyId** — 百度云 AK
> 2. **SecretAccessKey** — 百度云 SK
>
> 可在 [百度智能云控制台 > 安全认证 > Access Key](https://console.bce.baidu.com/iam/#/iam/accesslist) 获取。

```bash
{baseDir}/../baidu-bcc-price-1.0.1/scripts/setup.sh --ak "<AK>" --sk "<SK>" --region "bcc.bj.baidubce.com"
```

---

## 执行策略

收集完整配置后，执行以下命令进行价格对比：

### 方式 A（按实例族和核数，由 CPU+内存自动推导）

```bash
python3 {baseDir}/scripts/compare_price.py \
  --region "<地域>" \
  --family "<g|ga|c|ca|r|ra>" \
  --vcpu <核数> \
  --disk-size <磁盘GB> \
  --disk-type "<磁盘类型>" \
  --bandwidth <带宽Mbps> \
  --bandwidth-type <ByBandwidth|ByTraffic>
```

> **固定参数**：`--charge-type PrePaid --period 1` 已在脚本中硬编码，确保只查询包年包月1个月价格。

### 方式 B（直接指定规格）

```bash
python3 {baseDir}/scripts/compare_price.py \
  --region "<地域>" \
  --ali-spec "<阿里云规格>" \
  --bcc-spec "<百度云规格>" \
  --disk-size <磁盘GB> \
  --disk-type "<磁盘类型>" \
  --bandwidth <带宽Mbps> \
  --bandwidth-type <ByBandwidth|ByTraffic>
```

### 实例族参数说明

| 参数值 | 实例族类型 | 处理器 | 阿里云默认规格 | 百度云默认规格 |
|---|---|---|---|---|
| `g` | 通用型 Intel | Intel 5代 | ecs.g8i.{size} | bcc.g7.c{cpu}m{mem} |
| `c` | 计算型 Intel | Intel 5代 | ecs.c8ine.{size} | bcc.c7.c{cpu}m{mem} |
| `r` | 内存型 Intel | Intel 5代 | ecs.r8i.{size} | bcc.m7.c{cpu}m{mem} |
| `ga` | 通用型 AMD | AMD EPYC 3代 | ecs.g8a.{size} | bcc.ga3.c{cpu}m{mem} |
| `ca` | 计算型 AMD | AMD EPYC 3代 | ecs.c8a.{size} | bcc.ca3.c{cpu}m{mem} |
| `ra` | 内存型 AMD | AMD EPYC 3代 | ecs.r8a.{size} | bcc.ma3.c{cpu}m{mem} |

### 典型示例

```bash
# 4核16GB + 100GB SSD + 5Mbps按带宽 → 自动识别通用型Intel
python3 {baseDir}/scripts/compare_price.py \
  --region 北京 --family g --vcpu 4 \
  --disk-size 100 --disk-type SSD云盘 \
  --bandwidth 5 --bandwidth-type ByBandwidth

# 8核16GB + 200GB ESSD_PL1 + 10Mbps → 自动识别计算型Intel
python3 {baseDir}/scripts/compare_price.py \
  --region 广州 --family c --vcpu 8 \
  --disk-size 200 --disk-type ESSD_PL1 \
  --bandwidth 10 --bandwidth-type ByBandwidth

# 4核32GB + 100GB SSD + 5Mbps → 自动识别内存型AMD
python3 {baseDir}/scripts/compare_price.py \
  --region 北京 --family ra --vcpu 4 \
  --disk-size 100 --disk-type SSD云盘 \
  --bandwidth 5 --bandwidth-type ByBandwidth

# 用户直接指定规格
python3 {baseDir}/scripts/compare_price.py \
  --region 北京 \
  --ali-spec ecs.r8i.xlarge --bcc-spec bcc.m7.c4m32 \
  --disk-size 100 --disk-type SSD云盘 \
  --bandwidth 5 --bandwidth-type ByBandwidth

# 不含公网IP（仅对比实例+磁盘）
python3 {baseDir}/scripts/compare_price.py \
  --region 北京 --family g --vcpu 4 \
  --disk-size 100 --disk-type SSD云盘
```

### 指定百度云可用区（可选）

```bash
python3 {baseDir}/scripts/compare_price.py \
  --region 北京 --family g --vcpu 4 \
  --disk-size 100 --disk-type SSD云盘 \
  --bcc-zone cn-bj-e
```

---

## 交互式信息收集

如果用户未在一次请求中提供完整配置，依次询问以下信息：

### 1. 地域（必填）

| 选项 | 阿里云地域 | 百度云 Endpoint |
|------|-----------|----------------|
| **北京** | cn-beijing | bcc.bj.baidubce.com |
| **广州/深圳** | cn-shenzhen | bcc.gz.baidubce.com |
| **成都** | cn-chengdu | bcc.cd.baidubce.com |
| **苏州** | cn-shanghai | bcc.su.baidubce.com |
| **保定** | cn-beijing | bcc.bd.baidubce.com |
| **香港** | cn-hongkong | bcc.hkg.baidubce.com |

> 若用户未指定地域，默认使用**北京**。

### 2. CPU 与内存（必填）

> 请提供以下信息：
> - **CPU 核数**：如 2 / 4 / 8 / 16 / 32 / 64
> - **内存大小（GB）**：如 4 / 8 / 16 / 32 / 64
> - **处理器架构（可选）**：Intel / AMD（不填则默认查询 Intel 系列）

**根据 CPU:内存 比例自动判断实例族类型：**

| 内存/CPU 比 | 实例族类型 | Intel 参数 | AMD 参数 |
|------------|-----------|-----------|----------|
| 约 2:1 | 计算型 | `--family c` | `--family ca` |
| 约 4:1 | 通用型 | `--family g` | `--family ga` |
| 约 8:1 | 内存型 | `--family r` | `--family ra` |

非标准配比处理：
- 内存/CPU比 < 2 → 按计算型匹配
- 内存/CPU比 2~3 → 按计算型匹配
- 内存/CPU比 3~6 → 按通用型匹配
- 内存/CPU比 6~10 → 按内存型匹配
- 内存/CPU比 > 10 → 按内存型匹配，注明"高内存非标配比"

### 3. 磁盘配置（必填）

| 通用磁盘类型 | 阿里云对应（EBS） | 百度云对应（CDS） | 脚本参数值 |
|------------|-----------------|-----------------|----------|
| **高效云盘** | cloud_efficiency | 高性能云磁盘(hp1) | `--disk-type 高效云盘` |
| **SSD云盘** | cloud_ssd | 通用型SSD(cloud_hp1) | `--disk-type SSD云盘` |
| **ESSD_PL1** | cloud_essd | 增强型SSD_PL1 | `--disk-type ESSD_PL1` |
| **ESSD_PL2** | cloud_essd_pl2 | 增强型SSD_PL2 | `--disk-type ESSD_PL2` |
| **ESSD_PL3** | cloud_essd_pl3 | 增强型SSD_PL3 | `--disk-type ESSD_PL3` |

磁盘大小（GB）：如 40 / 100 / 200 / 500，默认 100

### 4. 带宽配置（可选）

- **带宽大小（Mbps）**：如 1 / 5 / 10 / 20 / 50（0 = 不含公网IP）
- **带宽计费方式**：
  - **按带宽计费 (`ByBandwidth`)**：查询包年包月1个月费用，可直接对比（**推荐**）
  - **按流量计费 (`ByTraffic`)**：仅显示单价（元/GB），**不计入月度合计**

---

## 实例规格族对标关系（完整映射表）

> 以下为阿里云ECS与百度智能云BCC的规格世代对标关系，是智能匹配的核心依据。

### 计算型（CPU:内存 = 1:2）

| 阿里云ECS规格族 | 百度智能云BCC规格族 | 处理器代数 | 处理器型号 | 主频 | 睿频 |
|---|---|---|---|---|---|
| c9i | 暂不支持 | Intel 9代 | Xeon Granite Rapids 6982P | 3.2 GHz | 3.6 GHz |
| c8i / c8ine | c7 | Intel 5代 | Xeon Emerald Rapids / Sapphire Rapids | 2.7 GHz | 3.2 GHz |
| c7 | c5 | Intel 3代 | Xeon 3代 Ice Lake | 2.7 GHz | 3.5 GHz |
| c6 / c5 | c4 / e1 | Intel 2代 | Xeon 2代 Cascade Lake | 2.5 GHz | 3.1 GHz |
| c9ae | 暂不支持 | AMD 4代+ | EPYC Turin-X 9T95 | 2.25 GHz | 3.7 GHz |
| c9a | ca4 | AMD 4代 | EPYC Turin | - | 最高 3.7 GHz |
| c8a | ca3 | AMD 3代 | EPYC Genoa 9T24 | 2.7 GHz | 3.7 GHz |
| c7a | ca2 | AMD 2代 | EPYC Milan | 2.55 GHz | 3.5 GHz |
| c6a | ca1 / e2 | AMD 1代 | EPYC Rome | 2.0 GHz | 3.3 GHz |

### 通用型（CPU:内存 = 1:4）

| 阿里云ECS规格族 | 百度智能云BCC规格族 | 处理器代数 | 处理器型号 | 主频 | 睿频 |
|---|---|---|---|---|---|
| g9i | g8 | Intel 9代 | Xeon Granite Rapids 6972P | 3.2 GHz | 3.6 GHz |
| g8i / g8ine | g7 | Intel 5代 | Xeon Emerald Rapids / Sapphire Rapids | 2.7 GHz | 3.2 GHz |
| g7 | g5 | Intel 3代 | Xeon 3代 Ice Lake | 2.7 GHz | 3.5 GHz |
| g6 / g5 | g4 / e1 | Intel 2代 | Xeon 2代 Cascade Lake | 2.5 GHz | 3.1 GHz |
| g9ae | 暂不支持 | AMD 4代+ | EPYC Turin-X | - | 最高 3.7 GHz |
| g9a | ga4 | AMD 4代 | EPYC Turin | - | 最高 3.7 GHz |
| g8a | ga3 | AMD 3代 | EPYC Genoa 9T24 | 2.7 GHz | 3.7 GHz |
| g7a | ga2 | AMD 2代 | EPYC Milan | 2.55 GHz | 3.5 GHz |
| g6a | ga1 / e2 | AMD 1代 | EPYC Rome | 2.0 GHz | 3.3 GHz |

### 内存型（CPU:内存 = 1:8）

| 阿里云ECS规格族 | 百度智能云BCC规格族 | 处理器代数 | 处理器型号 | 主频 | 睿频 |
|---|---|---|---|---|---|
| r9i | 暂不支持 | Intel 9代 | Xeon Granite Rapids | 3.2 GHz | 3.6 GHz |
| r8i | m7 | Intel 5代 | Xeon Emerald Rapids / Sapphire Rapids | 2.7 GHz | 3.2 GHz |
| r7 | m5 | Intel 3代 | Xeon 3代 Ice Lake | 2.7 GHz | 3.5 GHz |
| r6 / r5 | m4 / e1 | Intel 2代 | Xeon 2代 Cascade Lake | 2.5 GHz | 3.1 GHz |
| r9ae | 暂不支持 | AMD 4代+ | EPYC Turin-X | - | 最高 3.7 GHz |
| r9a | ma4 | AMD 4代 | EPYC Turin | - | 最高 3.7 GHz |
| r8a | ma3 | AMD 3代 | EPYC Genoa | 2.7 GHz | 3.7 GHz |
| r7a | ma2 | AMD 2代 | EPYC Milan | 2.55 GHz | 3.5 GHz |
| r6a | ma1 / e2 | AMD 1代 | EPYC Rome | 2.0 GHz | 3.3 GHz |

### 规格代数降级链（售罄时使用）

```
Intel系（计算型）：c9i → c8i/c8ine → c7 → c6 → c5
Intel系（通用型）：g9i → g8i/g8ine → g7 → g6 → g5
Intel系（内存型）：r9i → r8i → r7 → r6 → r5
AMD系（计算型）：c9ae → c9a → c8a → c7a → c6a
AMD系（通用型）：g9ae → g9a → g8a → g7a → g6a
AMD系（内存型）：r9ae → r9a → r8a → r7a → r6a
```

### 规格族内具体规格推导（根据 vCPU 数量）

**阿里云ECS** — `ecs.{族}.{大小}`

| vCPU | 2 | 4 | 8 | 16 | 32 | 64 | 96 |
|---|---|---|---|---|---|---|---|
| 后缀 | large | xlarge | 2xlarge | 4xlarge | 8xlarge | 16xlarge | 24xlarge |

**百度智能云BCC** — `bcc.{族}.c{核}m{内存}`

示例：4核8GB计算型c7 → `bcc.c7.c4m8`

---

## Skill文档外规格的智能匹配规则

当用户请求的实例规格**不在上述对标表中**（如用户指定了某款具体处理器型号、非标准内存配比，或云厂商未来新发布的规格），按以下规则推断并匹配：

### 匹配优先级

1. **处理器型号精确匹配**：通过用户提供的处理器型号（如 Xeon 6972P、EPYC 9654）直接确定代际
2. **主频/睿频区间匹配**：根据用户提供的主频/睿频，与下表对比选最接近代际
3. **CPU品牌 + 代际描述**：结合 Intel/AMD 品牌和代际描述（如"第5代"）进行匹配
4. **内存/CPU比推断族类型**：根据内存与CPU核数比确定通用/计算/内存族

### Intel Xeon 代际与主频参考

| 代际 | Xeon 系列 | 典型型号 | 主频范围 | 睿频范围 | 对应阿里云 | 对应百度云 |
|---|---|---|---|---|---|---|
| 9代（2024+） | Xeon 6 P系列 | 6972P, 6982P | 3.0~3.2 GHz | 3.5~3.6 GHz | c9i/g9i/r9i | 暂不支持 |
| 5代（2023） | Xeon Emerald Rapids / Sapphire Rapids | 8575C, 8563C | 2.5~2.7 GHz | 3.0~3.2 GHz | c8i/c8ine/g8i/r8i | c7/g7/m7 |
| 3代（2021） | Xeon Ice Lake | ICX系列 | 2.0~2.7 GHz | 2.8~3.5 GHz | c7/g7/r7 | c5/g5/m5 |
| 2代（2019） | Xeon Cascade Lake | CAS系列 | 1.8~2.5 GHz | 2.5~3.5 GHz | c6/g6/r6 | c4/g4/m4 |

### AMD EPYC 代际与主频参考

| 代际 | EPYC 系列 | 典型型号 | 主频范围 | 睿频范围 | 对应阿里云 | 对应百度云 |
|---|---|---|---|---|---|---|
| 4代+（2024+，Turin-X） | EPYC 9005X系列 | 9T95 | 2.0~2.25 GHz | 最高3.7 GHz | c9ae/g9ae/r9ae | 暂不支持 |
| 4代（2024，Turin） | EPYC 9005系列 | 9755, 9965 | 2.0~2.7 GHz | 最高3.7 GHz | c9a/g9a/r9a | ca4/ga4/ma4 |
| 3代（2022，Genoa） | EPYC 9004系列 | 9T24, 9W24, 9654 | 2.4~2.7 GHz | 3.5~3.7 GHz | c8a/g8a/r8a | ca3/ga3/ma3 |
| 2代（2021，Milan） | EPYC 7003系列 | 7763, 7543 | 2.0~2.55 GHz | 3.0~3.5 GHz | c7a/g7a/r7a | ca2/ga2/ma2 |
| 1代（2019，Rome） | EPYC 7002系列 | 7742, 7302 | 1.5~2.1 GHz | 2.5~3.3 GHz | c6a/g6a/r6a | ca1/ga1/ma1 |

> **智能匹配输出时必须注明**：匹配依据（主频/内存比/处理器代际），并标注"基于处理器特征智能推断，建议以官网实际参数为准"。

---

## 售罄降代处理规则

### 阿里云售罄处理

脚本返回 `sold_out` 标记时：
1. 输出: "**匹配对应实例规格售罄**"
2. 按降级链找到低一代规格族
3. 用方式B（`--ali-spec` + `--bcc-spec`）调用低一代规格的询价
4. 输出低一代规格的预付费1个月价格，并注明"已降代至 [规格名]"

降级链示例（Intel 通用型）：
```bash
# g8i 售罄 → 降代查询 g7
python3 {baseDir}/scripts/compare_price.py \
  --region 北京 \
  --ali-spec ecs.g7.xlarge --bcc-spec bcc.g5.c4m16 \
  --disk-size 100 --disk-type SSD云盘 --bandwidth 5
```

### 百度智能云售罄处理

脚本返回售罄错误时：
1. 输出: "**匹配对应实例规格售罄**"（百度智能云侧）
2. 尝试切换可用区（如 `--bcc-zone cn-bj-e`）
3. 若所有可用区均售罄，按降级链降代处理
4. 输出低一代规格的预付费1个月价格

### 双方均售罄

若阿里云和百度云双方在所有可用区的对应规格均售罄：
1. 输出: "**双方匹配对应实例规格均售罄**"
2. 按降级链输出低一代规格的价格对比

---

## 故障排查

| 错误信息 | 可能原因 | 解决方案 |
|---------|---------|---------|
| 凭证未配置 | AK/SK 未设置 | 运行对应 setup.sh 配置凭证 |
| 阿里云SDK未安装 | 缺少 Python 依赖 | 运行 `alicloud_ecs_price-1.0.0/scripts/setup.sh` |
| 匹配对应实例规格售罄 | 百度云该可用区无货 | 添加 `--bcc-zone` 指定其他可用区 |
| 未找到规格 | 规格名称有误 | 检查规格名称格式（如 bcc.g7.c4m16） |
| 未找到云盘规格 | 磁盘类型/大小不支持 | 尝试其他磁盘大小或类型 |
| 未获取到EIP价格 | 带宽计费方式不支持 | 切换 `--bandwidth-type` |

---

## 相关技能

- [阿里云ECS单独价格查询](../alicloud_ecs_price-1.0.0/SKILL.md)
- [百度智能云BCC单独价格查询](../baidu-bcc-price-1.0.1/SKILL.md)
- [规格对标参考](../对比关系SKILL.md)

## 官方文档

- [阿里云 ECS DescribePrice API](https://help.aliyun.com/zh/ecs/developer-reference/api-ecs-2014-05-26-describeprice)
- [百度智能云 BCC 实例规格族](https://cloud.baidu.com/doc/BCC/s/wjwvynogv)
- [百度智能云 BCC 价格查询 API](https://cloud.baidu.com/doc/BCC/s/uk5dt23r8)
- [百度智能云 CDS 价格查询 API](https://cloud.baidu.com/doc/BCC/s/blu16n1zm)
- [百度智能云 EIP 询价 API](https://cloud.baidu.com/doc/EIP/s/Hk9gy7w7q)
