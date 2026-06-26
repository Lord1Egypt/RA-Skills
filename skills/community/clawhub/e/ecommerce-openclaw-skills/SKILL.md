---
name: E-commerce Skills
description: 电商领域 OpenClaw 技能集合，提供选品调研、市场分析、内容生成等能力。支持淘宝/拼多多/抖音/小红书/1688平台。Use when: (1) you need to do product research for ecommerce; (2) you want to get market competition analysis before launching new product; (3) you need AI-assisted ecommerce operation tools.
---

# E-commerce Skills - 电商技能集合

OpenClaw 电商领域技能集合，为电商商家、运营、开发者提供 AI 增强的工具链。

## 架构设计

采用四层分层架构：

```
┌─────────────────────────────────────────────────────────────┐
│  业务场景层 (Business Scenarios) - 面向终端用户完整流程        │
├─────────────────────────────────────────────────────────────┤
│  领域能力层 (Domain Capabilities) - 可复用的电商能力         │
├─────────────────────────────────────────────────────────────┤
│  平台适配层 (Platform Adapters) - 各电商平台 API 封装        │
├─────────────────────────────────────────────────────────────┤
│  基础设施层 (Infrastructure) - 公共基础：配置、认证、HTTP      │
└─────────────────────────────────────────────────────────────┘
```

## 已包含技能

### 基础设施层
- **ecommerce-infrastructure** - 统一配置管理、认证管理、HTTP 客户端、日志、错误处理、数据类型定义

### 平台适配层
- **taobao-api** - 淘宝/天猫开放平台 API 适配

### 领域能力层
- **product-research** - 产品调研，搜索商品，统计价格分布、销量分布，分析竞争度

### 业务场景层
- **ecommerce-product-research** - 完整选品调研流程，输入关键词，输出完整市场调研报告

## 配置

在环境变量中配置：

```bash
# 淘宝开放平台
ECOMMERCE_TAOBAO_APP_KEY=your_app_key
ECOMMERCE_TAOBAO_APP_SECRET=your_app_secret
```

## 使用示例

```
帮我调研一下"户外露营椅"这个品类在淘宝的市场情况，给我选品建议
```

技能会自动：
1. 调用淘宝 API 搜索关键词
2. 统计价格分布、销量分布
3. 分析竞争度
4. 输出完整 Markdown 调研报告

## 安装

```bash
npx skills add your-username/ecommerce-openclaw-skills
```

## 许可证

MIT

---

*企业开发·定制skills请联系Wx：CChenJ_*
