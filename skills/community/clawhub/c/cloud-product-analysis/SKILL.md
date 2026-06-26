---
name: cloud-product-analysis
description: 云产品技术文档对比工具，自动抓取阿里云、华为云、AWS、腾讯云官方文档，生成结构化对比资料，辅助技术选型和学习
author: cloud-product-analysis
version: "1.1.0"
license: Apache-2.0
allowed-tools: web_fetch, bash
---

# 云产品文档对比工具

## 工具说明
这是一个云产品技术文档聚合工具，帮助开发者和架构师快速了解不同云厂商的产品特性。

**适用场景**：
- 技术选型前了解产品差异
- 学习云计算产品知识
- 对比不同云厂商的产品能力
- 快速查阅官方文档关键信息

## 快速开始

### 方式一：使用文档抓取脚本（推荐）

脚本位于 `scripts/cloud_doc_scraper.py`，自动解析文档目录、抓取核心页面、输出 markdown。

> **依赖需手动安装**：`pip install playwright httpx beautifulsoup4 && playwright install chromium`

```bash
# 默认对比阿里云和华为云
python scripts/cloud_doc_scraper.py --product ecs

# 对比阿里云、华为云、AWS（三方对比）
python scripts/cloud_doc_scraper.py --product oss --providers aliyun,huawei,aws

# 只对比阿里云和 AWS
python scripts/cloud_doc_scraper.py --product rds --providers aliyun,aws

# 自定义输出和页数
python scripts/cloud_doc_scraper.py --product redis --providers aliyun,huawei,aws --output redis_3way.md --max-pages 15

# 查看所有支持的产品
python scripts/cloud_doc_scraper.py --list
```

**支持的产品**：ecs, oss, rds, redis, ack, fc, slb, maxcompute, pai, bailian, cdn, nas, flink, elasticsearch, dws

**支持的厂商**：
- `aliyun`（阿里云）
- `huawei`（华为云）
- `aws`（亚马逊云）
- `tencent`（腾讯云）

**输出**：markdown 文件，包含各厂商的官方文档原文 + 更新日志，可直接粘贴给 AI 做竞品分析。

**工作原理**：
1. 检测依赖是否就绪，缺失时提示安装命令并退出
2. 用 Playwright 打开文档首页，解析左侧目录导航
3. 按优先级筛选核心页面（产品介绍 > 规格参数 > 计费 > 应用场景）
4. 并发抓取各页面内容，输出去噪后的纯文本
5. 支持 HTTP fallback（Playwright 抓取失败时自动用 httpx+BS4）
6. 支持 deep_links（目录解析失败时使用预配置的页面 URL）
7. 扩展兼容模式（`--stealth`）默认关闭，仅在显式启用时为 JS 重型站点提供额外的浏览器上下文配置

### 方式二：手动用 web_fetch 逐页抓取

参考下方"官方文档入口"表格，用 `web_fetch` 工具逐页抓取文档内容。

---

## 官方文档入口

### 文档 URL 说明

**华为云文档**：
- 旧版文档（productdesc-*）：部分产品已 404（OBS, RDS, DCS, CDN, SFS 等），脚本已内置正确的 deep_links
- 新版文档（SPA index.html）：需要 JS 渲染，web_fetch 只能拿到空壳，建议用脚本
- 更新日志：`https://support.huaweicloud.cn/wtsnew-{product}/index.html`

**阿里云文档**：
- 主入口：`https://help.aliyun.com/zh/{product}`
- 更新日志：`https://help.aliyun.com/zh/{product}/product-overview/release-notes`
- URL 可能变更，脚本会自动从目录导航发现链接

**AWS 文档**：
- 中文文档：`https://docs.aws.amazon.com/zh_cn/{service}/`
- 更新日志：各产品文档内的 `document-history.html` 或 `WhatsNew.html`
- 脚本使用预配置的 deep_links 直接抓取核心页面

### 阿里云
| 品类 | 产品 | 文档 | 更新日志 |
|------|------|------|----------|
| 计算 | 云服务器ECS | https://help.aliyun.com/zh/ecs | https://help.aliyun.com/zh/ecs/product-overview/release-notes |
| 计算 | 函数计算FC | https://help.aliyun.com/zh/fc | https://help.aliyun.com/zh/fc/product-overview/release-notes |
| 存储 | 对象存储OSS | https://help.aliyun.com/zh/oss | https://help.aliyun.com/zh/oss/product-overview/release-notes |
| 存储 | 文件存储NAS | https://help.aliyun.com/zh/nas | https://help.aliyun.com/zh/nas/product-overview/release-notes |
| 数据库 | 云数据库RDS | https://help.aliyun.com/zh/rds | https://help.aliyun.com/zh/rds/product-overview/release-notes |
| 数据库 | 云数据库Redis | https://help.aliyun.com/zh/redis | https://help.aliyun.com/zh/redis/product-overview/release-notes |
| 数据库 | AnalyticDB PG | https://help.aliyun.com/zh/analyticdb-for-postgresql | https://help.aliyun.com/zh/analyticdb-for-postgresql/product-overview/release-notes |
| 容器 | 容器服务ACK | https://help.aliyun.com/zh/ack | https://help.aliyun.com/zh/ack/product-overview/release-notes |
| 网络 | 负载均衡SLB | https://help.aliyun.com/zh/slb | https://help.aliyun.com/zh/slb/product-overview/release-notes |
| 网络 | CDN | https://help.aliyun.com/zh/cdn | https://help.aliyun.com/zh/cdn/product-overview/release-notes |
| 大数据 | MaxCompute | https://help.aliyun.com/zh/maxcompute | https://help.aliyun.com/zh/maxcompute/product-overview/Release-notes |
| 大数据 | 实时计算Flink | https://help.aliyun.com/zh/flink | https://help.aliyun.com/zh/flink/product-overview/release-note |
| 大数据 | Elasticsearch | https://help.aliyun.com/zh/elasticsearch | https://help.aliyun.com/zh/elasticsearch/product-overview/release-notes |
| AI | 人工智能平台PAI | https://help.aliyun.com/zh/pai | https://help.aliyun.com/zh/pai/user-guide/api-aiworkspace-2021-02-04-changeset |
| AI | 百炼平台 | https://help.aliyun.com/zh/bailian | https://help.aliyun.com/zh/bailian/release-notes |

### 华为云
| 品类 | 产品 | 文档 | 更新日志 |
|------|------|------|----------|
| 计算 | 弹性云服务器ECS | https://support.huaweicloud.cn/ecs/index.html | https://support.huaweicloud.cn/wtsnew-ecs/index.html |
| 计算 | 函数工作流FunctionGraph | https://support.huaweicloud.cn/functiongraph/index.html | https://support.huaweicloud.cn/wtsnew-functiongraph/index.html |
| 存储 | 对象存储OBS | https://support.huaweicloud.cn/obs/index.html | https://support.huaweicloud.cn/wtsnew-obs/index.html |
| 存储 | 文件存储SFS | https://support.huaweicloud.cn/sfs/index.html | https://support.huaweicloud.cn/wtsnew-sfs/index.html |
| 数据库 | 云数据库RDS | https://support.huaweicloud.cn/rds/index.html | https://support.huaweicloud.cn/wtsnew-rds/index.html |
| 数据库 | 分布式缓存DCS | https://support.huaweicloud.cn/dcs/index.html | https://support.huaweicloud.cn/wtsnew-dcs/index.html |
| 数据库 | 数据仓库GaussDB(DWS) | https://support.huaweicloud.cn/dws/index.html | https://support.huaweicloud.cn/wtsnew-dws/index.html |
| 容器 | 云容器引擎CCE | https://support.huaweicloud.cn/cce/index.html | https://support.huaweicloud.cn/wtsnew-cce/index.html |
| 网络 | 弹性负载均衡ELB | https://support.huaweicloud.cn/elb/index.html | https://support.huaweicloud.cn/wtsnew-elb/index.html |
| 网络 | CDN | https://support.huaweicloud.cn/cdn/index.html | https://support.huaweicloud.cn/wtsnew-cdn/index.html |
| 大数据 | MapReduce服务MRS | https://support.huaweicloud.cn/mrs/index.html | https://support.huaweicloud.cn/wtsnew-mrs/index.html |
| 大数据 | 数据湖探索DLI | https://support.huaweicloud.cn/dli/index.html | https://support.huaweicloud.cn/wtsnew-dli/index.html |
| 搜索 | 云搜索服务CSS | https://support.huaweicloud.cn/css/index.html | https://support.huaweicloud.cn/wtsnew-css/index.html |
| AI | AI开发平台ModelArts | https://support.huaweicloud.cn/modelarts/index.html | https://support.huaweicloud.cn/wtsnew-modelarts/index.html |
| AI | 盘古大模型平台 | https://support.huaweicloud.cn/pangu/index.html | https://support.huaweicloud.cn/wtsnew-pangu/index.html |

### AWS（亚马逊云）
| 品类 | 产品 | 文档 | 对应阿里云/华为云 |
|------|------|------|----------|
| 计算 | EC2 | https://docs.aws.amazon.com/zh_cn/ec2/ | ECS / ECS |
| 计算 | Lambda | https://docs.aws.amazon.com/zh_cn/lambda/ | FC / FunctionGraph |
| 存储 | S3 | https://docs.aws.amazon.com/zh_cn/AmazonS3/ | OSS / OBS |
| 存储 | EFS | https://docs.aws.amazon.com/zh_cn/efs/ | NAS / SFS |
| 数据库 | RDS | https://docs.aws.amazon.com/zh_cn/AmazonRDS/ | RDS / RDS |
| 数据库 | ElastiCache | https://docs.aws.amazon.com/zh_cn/AmazonElastiCache/ | Redis / DCS |
| 数据库 | Redshift | https://docs.aws.amazon.com/zh_cn/redshift/ | AnalyticDB / DWS |
| 容器 | EKS | https://docs.aws.amazon.com/zh_cn/eks/ | ACK / CCE |
| 网络 | ELB | https://docs.aws.amazon.com/zh_cn/elasticloadbalancing/ | SLB / ELB |
| 网络 | CloudFront | https://docs.aws.amazon.com/zh_cn/AmazonCloudFront/ | CDN / CDN |
| 大数据 | EMR | https://docs.aws.amazon.com/zh_cn/emr/ | MaxCompute / MRS |
| 大数据 | Managed Flink | https://docs.aws.amazon.com/zh_cn/managed-flink/ | Flink / DLI |
| 搜索 | OpenSearch | https://docs.aws.amazon.com/zh_cn/opensearch-service/ | Elasticsearch / CSS |
| AI | SageMaker | https://docs.aws.amazon.com/zh_cn/sagemaker/ | PAI / ModelArts |
| AI | Bedrock | https://docs.aws.amazon.com/zh_cn/bedrock/ | 百炼 / 盘古 |

### 腾讯云
| 品类 | 产品 | 文档 | 对应阿里云/华为云 |
|------|------|------|----------|
| 计算 | 云服务器 CVM | https://cloud.tencent.com/document/product/213 | ECS / ECS |
| 计算 | 云函数 SCF | https://cloud.tencent.com/document/product/583 | FC / FunctionGraph |
| 存储 | 对象存储 COS | https://cloud.tencent.com/document/product/436 | OSS / OBS |
| 存储 | 文件存储 CFS | https://cloud.tencent.com/document/product/582 | NAS / SFS |
| 数据库 | 云数据库 MySQL | https://cloud.tencent.com/document/product/236 | RDS / RDS |
| 数据库 | 云数据库 Redis | https://cloud.tencent.com/document/product/239 | Redis / DCS |
| 数据库 | 数据仓库 CDWPG | https://cloud.tencent.com/document/product/878 | AnalyticDB / DWS |
| 容器 | 容器服务 TKE | https://cloud.tencent.com/document/product/457 | ACK / CCE |
| 网络 | 负载均衡 CLB | https://cloud.tencent.com/document/product/214 | SLB / ELB |
| 网络 | CDN | https://cloud.tencent.com/document/product/228 | CDN / CDN |
| 大数据 | 弹性 MapReduce | https://cloud.tencent.com/document/product/589 | MaxCompute / MRS |
| 大数据 | 流计算 Oceanus | https://cloud.tencent.com/document/product/849 | Flink / DLI |
| 搜索 | Elasticsearch | https://cloud.tencent.com/document/product/845 | Elasticsearch / CSS |
| AI | 机器学习平台 TI | https://cloud.tencent.com/document/product/851 | PAI / ModelArts |
| AI | 腾讯混元大模型 | https://cloud.tencent.com/document/product/1729 | 百炼 / 盘古 |

---

## 使用方式

用户输入目标产品后，执行以下步骤：

**第一步：查找对应产品**
从上表查找两个云厂商的对应产品。若预置清单无对应产品，告知用户并提供已知的文档入口。

**第二步：运行文档抓取脚本**
```bash
python scripts/cloud_doc_scraper.py --product {product_key} --output {product_key}_docs.md
```
脚本会自动完成：依赖检查 → 目录解析 → 核心页面筛选 → 并发抓取 → 输出 markdown。

若脚本不可用，可使用 web_fetch 手动逐页抓取（参考上方文档入口表格）。

**第三步：文档内容优先级**
按以下优先级抓取文档内容：

1. **产品概述/简介页面**（了解产品定位和核心价值）
2. **组件版本表**（大数据类产品，如 EMR 组件版本、MRS 组件版本）
3. **核心特性/功能说明页面**（了解能力边界）
4. **规格参数/性能指标页面**（了解性能上限）
5. **内核增强说明页面**（了解自研能力）
6. **最佳实践/使用场景页面**（了解适用场景）
7. **更新日志**（了解近12个月更新动态）

**第四步：整理对比信息**
基于抓取的文档内容，整理以下信息：
- 产品形态差异（托管服务 vs PaaS 平台等）
- 关键指标的数字差距（性能上限、规格范围、SLA 等）
- 功能支持差异（一方有、一方没有的能力）
- 实现路径差异（相同功能的不同实现方式）
- 更新动态差异（近期迭代重点）

**第五步：生成对比文档**
输出结构化对比文档，包含：
1. 两款产品的核心差异点
2. 各自的优势和适用场景
3. 功能/性能对比表格

所有结论必须基于官方文档，标注信息来源。

**第六步：保存并展示结果**
1. 将完整分析报告保存为 markdown 文件（如 `{product_key}_competitive_analysis.md`），写入 workspace
2. **必须将分析报告的核心内容直接展示给用户**——不要只说"已保存到文件"，而是把关键结论、对比表格、选型建议等直接输出到对话中，让用户一眼就能看到结果
3. 在展示末尾附上文件路径，方便用户后续引用

---

## 对比维度参考

根据产品类型，优先对比以下维度：

**基础维度（必选）**：
- 开源组件版本支持（如 Elasticsearch 7.10/8.x、OpenSearch 2.x）
- 内核增强能力（自研内核、性能优化、稳定性增强）
- 核心功能完整性（向量检索、存算分离、智能运维）
- 规格与性能上限（单节点存储、分片数、QPS）

**增强维度（按产品类型选择）**：
- 搜索类：向量检索算法、量化方式、向量维度、AI 搜索能力
- 数据库类：高可用架构、备份恢复、容灾能力
- 大数据类：计算引擎、存储格式、数据源集成
- AI 类：模型管理、推理能力、RAG 支持

**迭代维度（可选）**：
- 近 12 个月功能更新记录
- 产品迭代重点（从更新日志推断）

---

## 使用约束
- 所有信息来自官方文档，不使用第三方信息或推测内容
- 若文档抓取失败，明确说明失败原因
- 若预置清单无对应产品，告知用户并提供已知入口
- 若产品形态差异过大，说明差异后再对比可对比的维度
- 对比基于事实数据，避免主观评价
- 版本号、性能数据、规格参数等必须标注来源文档

---

## 脚本技术细节

### 依赖（需手动安装）
- Python 3.10+
- playwright + chromium（浏览器自动化）
- httpx + beautifulsoup4（HTTP fallback）

安装命令：
```bash
pip install playwright httpx beautifulsoup4
playwright install chromium
```

### 已知限制
- 华为云部分产品（OBS, RDS, DCS, CDN, SFS）旧版 productdesc 页面已 404，脚本使用 deep_links 兜底
- 华为云文档站部分页面需要 JS 渲染，web_fetch 只能拿到空壳，建议用脚本
- 华为云 changelog 页面（wtsnew-*）部分在 .cn 域名 404，脚本自动回退 .com
- 阿里云部分子页面可能返回空内容，脚本会尝试 HTTP fallback
- 个别 deep_links URL 可能随文档更新而失效，需定期维护
- 扩展兼容模式（`--stealth`）默认关闭，仅在用户显式启用时生效，用于为 JS 重型站点提供额外的浏览器上下文配置
