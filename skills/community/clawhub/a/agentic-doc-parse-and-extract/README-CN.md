<div align="center">
<a id="agentic_doc_parse_and_extract"></a>

# 📄 来也智能体文档处理官方CLI (agentic_doc_parse_and_extract)

agentic_doc_parse_and_extract 是来也科技ADP（Agentic Document Processing）产品发布的官方命令行工具，让人类和 AI Agent 都能在终端中调用ADP能力进行文档解析与抽取

[English](README.md) | [简体中文](README-CN.md)

</div>

## 🚀 关于来也ADP

ADP是来也科技公司**智能体文档处理产品 (Agentic Document Processing，简称 ADP)**， 基于大模型的通用理解能力，不依赖规则与标注，具备对多语言、多模态、多场景的通用理解能力；智能体的自主规划与执行，能够理解任务目标、自主规划步骤、调用工具、完成复杂任务；端到端的业务自动化，从文档输入到业务决策再到人机协同，形成完整闭环。

**agentic-doc-parse-and-extract** 是 ADP 官方开源 CLI 工具，同时支持人工终端调用 + AI Skill 自动调用。一条命令即可完成：文档结构化解析 + 关键字段智能抽取，覆盖发票、订单、证件、票据、通用文档全场景，输出标准 JSON，无缝对接自动化与 AI 流程。

---

### 💡 核心功能

agentic-doc-parse-and-extract 聚焦文档全流程智能处理，兼顾人工终端调用与 AI Agent 自动调用，核心功能覆盖解析、抽取、批量处理全场景，无需复杂配置，一条命令即可完成操作：

| 功能名称 | 功能描述 | 最佳场景 |
|---------|------------------|----------|
| **文档解析** | 自动识别 PDF、图片等多格式文档，将杂乱的非结构化内容（如扫描件、手写体、复杂排版文档）转化为标准化结构化数据，保留原始文档层级与关键关联关系 | 将非结构化文档转换为结构化数据，供 LLM 阅读和后续抽取使用 |
| **开箱即用文档抽取** | 基于 ADP 大模型原生 AI 能力，内置发票、收据、订单、中国地区常用证件等标准化抽取模型，无需配置规则、无需人工标注，一键提取各类通用单据关键字段，输出标准 JSON | 应付账款自动化、费用管理、采购自动化、卡证信息快速录入系统 |
| **自定义文档抽取** | 支持自主创建、编辑与管理个性化抽取应用，可针对企业专属单据、行业定制表单配置专属抽取字段与识别逻辑 | 企业专属单据、行业定制表单、非标准化文档的私有化抽取需求 |
| **任务查询** | 支持异步任务提交与状态查询，可快速查看任务执行进度、成功/失败状态，以及任务最终处理结果 | 批量任务处理、异步文档处理、问题排查与处理记录追溯 |
| **应用管理** | 提供完整的应用管理能力，可查看所有可用的抽取应用（系统内置 + 自定义）、查询应用详情、应用标签 | 多场景业务切换、应用全生命周期管控、自定义应用管理 |

---

### 🎯 适用人群

- **AI Agent 开发者：** 通过标准 Skill 快速集成文档解析抽取能力，赋能智能体自动化办公流程
- **企业研发与架构团队：** 统一接入 CLI 工具，低成本落地全品类单据结构化自动化处理
- **财务 & 行政运营团队：** 批量解析发票、收据、报销单，减少人工录入与核对成本
- **业务系统集成方：** 依赖标准化 JSON 输出，无缝对接 ERP、RPA、业务中台等上下游系统
- **内部平台建设者：** 支持本地部署与环境适配，满足企业内网安全与权限管控要求


## 📁 项目文件结构与文件说明

```
agentic-doc-parse-and-extract/
├── skill.md                  # Skill配置与调用说明
├── README.md                 # 来也ADP产品介绍与CLI下载与调用说明
├── references/               # 参数枚举、错误码、JSON返回说明
    ├── examples.md           # 调用与返回示例代码 参数说明
    ├── commands.md           # 所有命令列表
    ├── response-schema.md    # 返回参数说明
    ├── error-handling.md     # 错误与应对措施
├──  License                  # 授权许可
```


## 📋 API Key
### 获取API Key
1. 访问 [ADP 中国地区网址](https://adp.laiye.com/?utm_source=clawhub)、 [ADP 全球地区网址](https://adp-global.laiye.com/?utm_source=clawhub)
2. 注册新账户（新用户每月 100 免费积分）


## 💻 环境与安装
### 支持平台与版本
| 平台 | 最低要求 |
|---------|------------------|
| **Windows** | Windows 10 或更高版本 |
| **Linux** | Ubuntu 18.04+, CentOS 7+, 或主流Linux发行版 |
| **macOS** | macOS 10.14 (Mojave) 或更高版本 |
---

### 安装

  ```bash
  # 方法 1: npm（推荐，全平台通用，国内可通过 npmmirror 镜像加速）
  npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli --registry=https://registry.npmmirror.com/ || npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli

  # 方法 2: Shell 脚本（Linux / macOS，无 npm 环境时使用）
  curl -fsSL https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.sh | bash

  # 方法 3: PowerShell 脚本（Windows，无 npm 环境时使用）
  Invoke-WebRequest -Uri "https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.ps1" -OutFile "$env:TEMP\adp-init.ps1"; & "$env:TEMP\adp-init.ps1"
  ```

---

## ✨ 核心特性

### 📦 开箱即用产品

| 产品 | 提取内容 | 最佳场景 |
|---------|------------------|----------|
| **文档解析** | 提取文档内的文本、表格、图片、印章等元素 | 将文档转换成结构化数据供LLM阅读 |
| **发票/收据抽取** | 发票号码、日期、供应商、明细项目、总额、税费 | 应付账款自动化、费用管理 |
| **订单抽取** | 采购单号、商品、数量、价格、交付信息 | 采购自动化、电商集成 |
| **卡证抽取** | 身份证、银行卡、驾驶证、营业执照等11种常用卡证 | 卡证信息快速录入系统 |

### 🛠️ 技术能力

- **10+ 种文件格式** ： 覆盖主流图片与办公文档格式（.jpg, .jpeg, .png, .bmp, .tiff, .tif, .pdf, .doc, .docx, .xls, .xlsx）
- **VLM + LLM 双引擎** ： 视觉理解 + 语义提取，实现最大准确率
- **同步与异步模式** ： 所有功能均对外开放同步、异步 API
- **文件限制：** 最大文件大小：50MB
- **批量处理：** 支持文件夹递归处理

### 🌟 产品优势
- 依托来也科技 ADP 大模型核心能力，结合 CLI 工具轻量化特性，打造高效、灵活、易集成的文档处理解决方案，核心优势突出：
- 零门槛上手：无需专业技术背景，无需规则配置与数据标注，内置标准化抽取模型，开箱即用，一条命令完成文档解析与抽取。
- 全场景适配：覆盖发票、收据、订单、证件等通用场景，同时支持自定义扩展，适配企业专属单据、行业定制表单，兼顾通用性与个性化需求。
- 高效集成适配：支持 AI Agent Skill 原生调用、终端手动调用，输出标准 JSON 格式，无缝对接 RPA、ERP、业务中台等上下游系统，降低集成成本。
- 多终端兼容：Windows、macOS、Linux 全平台支持，无需额外安装依赖，配置环境变量后全局可调用，适配本地部署与多场景办公需求。
- 高精度高稳定：基于 ADP 大模型优化，非结构化文档（扫描件、手写体、复杂排版）识别准确率高，支持异步任务管理，保障业务流程稳定运行。

<a id="credit"></a>
### 💰 计费

- **新用户福利：** 每月获得 100 免费积分，不限制使用应用
- **资产消耗规则：**
    | 处理阶段 | 费用 |
    |-----------------|------|
    | 文档解析 | 0.5 积分/页 |
    | 采购订单抽取 | 1.5 积分/页 |
    | 发票/收据抽取 | 1.5 积分/页 |
    | 自定义抽取 | 1 积分/页 |

- **资产充值：** 可直接登录ADP门户网站进行资产充值，我们为国内外用户提供了独立公有云接入地址，需要按区域分开配置，就近访问可更大程度保障全网高速稳定调用。
  - 中国大陆地区[登录](https://adp.laiye.com/?utm_source=clawhub)
  - 非中国大陆地区用户[登录](https://adp-global.laiye.com/?utm_source=clawhub)

  如支付遇到问题，请联系支持邮箱：📧 global_product@laiye.com

## 📜 授权许可

我们采用 开源工具 + 付费服务 的组合模式：CLI 工具完全免费开源，方便大家快速接入；而核心的 ADP 智能解析能力为公有云商业服务，按实际使用量计费，旨在为用户提供高精准、高稳定的文档处理体验。

- **CLI 工具**：MIT License 开源许可，可自由使用、修改和分发
- **ADP 服务**：基于公有云的 AI 文档处理服务，按使用量计费，[计费规则](#credit)

### 💰 免费额度
新用户注册后每月可获得 **100 免费积分**，可体验完整功能


## 📞 支持与联系
- **CLI 使用指南：** [ADP CLI 使用指南](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- **API 接口文档：** [Open API 使用指南](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- **ADP 产品操作手册：** [公有云操作手册](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)

- **问题反馈：** [GitHub Issues](https://github.com/laiye-ai-repos/adp-skill/issues)
- **邮箱：** global_product@laiye.com
- **官网：** [来也科技](https://laiye.com)

---

<div align="center">
[⬆ 返回顶部](#agentic_doc_parse_and_extract)

**用 ❤️ 构建智能体 AI 的未来**
版权所有 © 2026 [来也科技（北京）有限公司] 保留所有权利。

</div>
