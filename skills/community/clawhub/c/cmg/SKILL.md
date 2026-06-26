---
name: tencent-cloud-migration
description: "腾讯云迁移平台（CMG/MSP）全流程能力。触发词：资源扫描、扫描阿里云/AWS/华为云/GCP资源、生成云资源清单、选型推荐、对标腾讯云、推荐规格、帮我推荐、给我推荐、ECS对应什么腾讯云产品、成本分析、TCO、迁移报价、询价、价格计算器、cmg-scan、cmg-recommend、cmg-tco"
description_zh: "CMG 云迁移：资源扫描 + 选型推荐 + 成本分析"
description_en: "CMG cloud migration: resource scan, product recommendation, TCO analysis"
version: 1.2.0
allowed-tools: Read,Bash,Browser
---

# CMG 云迁移 Skill

云迁移服务平台（CMG/MSP）AI 辅助能力，覆盖迁移前评估的完整流程。

## 能力地图

| 能力                          | 触发场景                                                      | 详细文档                             |
| ----------------------------- | ------------------------------------------------------------- | ------------------------------------ |
| **资源扫描** (cmg-scan)       | 扫描阿里云/AWS/华为云等资源清单，导出 Excel                   | `{baseDir}/references/scan.md`       |
| **选型推荐** (cmg-recommend)  | 将扫描结果对标腾讯云产品规格，生成推荐方案                    | `{baseDir}/references/recommend.md`  |
| **成本分析** (cmg-tco)        | ⚠️ **必须**通过 API/价格计算器获取真实价格，**严禁自行估算价格**，生成 TCO 对比报告 | `{baseDir}/references/tco.md`        |
| **迁移执行引导** (cmg-migrate) | 根据资源类型引导用户使用腾讯云对应迁移工具（主机/对象存储/数据库/文件存储） | `{baseDir}/references/migrate.md`    |

产品代码速查表（所有平台）：`{baseDir}/references/products.md`

---

## 典型工作流

```
1. 资源扫描 (cmg-scan)
   ↓ 产物：xxx_scan_xxxxxx.xlsx（资源清单 Excel）

2. 选型推荐 (cmg-recommend)
   ↓ 输入：xxx_scan_xxxxxx.xlsx
   ↓ 产物：cmg_recommend_result.json（推荐结果，含源端参数 + MCP 原始返回）

3. 成本分析 (cmg-tco)
   ↓ 输入：cmg_recommend_result.json（推荐方式，优先）或 Excel（直接扫描方式）
   ↓ ⚠️ 严禁自行估算/编造价格！必须通过以下真实渠道获取：
   ↓ 方式1(推荐): 调用 tco_pricing.py 脚本通过 API 批量询价
   ↓ 方式2(备选): 通过浏览器访问各云厂商官方价格计算器
   ↓ 产物：pricing_data.json + TCO 对比报告（Excel + HTML）

4. 迁移执行引导 (cmg-migrate)
   ↓ 根据资源类型引导对应迁移工具：
   ↓ 主机 → 云迁移 > 主机迁移
   ↓ 对象存储 → 云迁移 > 对象存储迁移（MSP）
   ↓ 数据库 → DTS
   ↓ 文件存储 → 云迁移 > 文件存储迁移（使用迁移集群）
```

---

## 使用指南

收到用户请求后，先判断属于哪个能力阶段，然后 Read 对应文档：

- 用户想**扫描云资源**：Read `{baseDir}/references/scan.md`
- 用户想**选型推荐/对标腾讯云/推荐规格**：Read `{baseDir}/references/recommend.md`
- 用户想**查价格/TCO 分析/询价/价格计算器**：Read `{baseDir}/references/tco.md`
- 用户想**迁移/问怎么迁移/迁移工具/开始迁移**：Read `{baseDir}/references/migrate.md`
- 用户问**产品代码**：Read `{baseDir}/references/products.md`

### cmg-recommend 特别说明

选型推荐通过 **mcporter + 远端 MCP Server** 执行，Read `recommend.md` 后按以下流程处理：

1. 运行 `{baseDir}/scripts/setup.sh --check-only` 检查环境
2. 若未配置，直接运行 `{baseDir}/scripts/setup.sh --setup` 自动完成安装（内置默认地址，无需询问用户）
3. 环境就绪后，使用 `mcporter call cmg-recommend.<tool>` 调用推荐工具

---

## 🚨🚨🚨 绝对红线：价格数据必须来自真实查询 🚨🚨🚨

> **本 Skill 涉及的所有价格数据都将直接用于商业决策和客户报价。**
> **虚假价格将导致严重的商业损失和信誉损害，后果不可挽回。**

### ❌ 绝对禁止

1. **绝对禁止自行估算、推算、编造任何价格数据** — 不管你对价格有多"自信"，你的知识已经过时，云厂商价格随时在变
2. **绝对禁止使用"根据经验估计"、"大约"、"通常价格"等模糊说法代替真实询价** — 没有真实数据就明确告知用户
3. **绝对禁止基于历史知识推断当前价格** — 你的训练数据中的价格信息已经过时，不具备参考价值
4. **绝对禁止在无法调用 API 或访问价格计算器时自行补充价格** — 应该报错并告知用户原因

### ✅ 必须遵守

1. **所有价格必须通过以下渠道之一获取：**
   - 调用 `{baseDir}/scripts/tco_pricing.py` 脚本通过云厂商 API 获取真实报价
   - 通过浏览器访问云厂商官方价格计算器页面读取真实报价
2. **如果 API 调用失败或浏览器无法访问，必须明确告知用户获取价格失败，说明失败原因，并请用户协助解决** — 绝不能"补一个估算值凑合"
3. **每条价格记录必须包含 `price_source` 字段，标明数据来源**（如"阿里云 DescribePrice API"、"腾讯云 InquiryPriceRunInstances API"、"阿里云价格计算器网页"）
4. **生成报告前必须确认所有 pricing_items 的价格均来自真实查询**
