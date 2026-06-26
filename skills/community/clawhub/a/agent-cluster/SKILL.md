---
name: foreign-trade-silicon-army
description: 亚马逊外贸B2B多CMS Agent协作系统。支持Shopify/WooCommerce/Magento三大平台，A2A架构协调库存/采购/财务/物流四大专家Agent，三层安全网保障审批合规。即装即用，零配置开箱。
version: 3.0.4
triggers:
  - "外贸"
  - "CMS"
  - "Shopify"
  - "WooCommerce"
  - "Magento"
  - "库存"
  - "采购"
  - "Amazon"
  - "B2B"
tags:
  - agent
  - a2a
  - cms
  - ecommerce
  - b2b
  - foreign-trade
  - multi-agent
requires:
  python_packages:
    - httpx
    - pyyaml
    - fastapi
    - uvicorn
  env:
    - SYSTEM_MODE
    - SAP_BASE_URL
    - SAP_API_KEY
    - YONYOU_BASE_URL
    - YONYOU_APPKEY
    - KINGDEE_BASE_URL
    - ANTHROPIC_API_KEY
    - DEEPSEEK_API_KEY
homepage: https://github.com/WangM-A3/agent-cluster
authors:
  - WangM-A3
pricing: free,pro=9.9,enterprise
---

# 产业互联网硅基军团 v2.0

> 企业级Multi-Agent智能体集群系统，基于**1+N架构**（1个幕僚长+20个专业Agent），参考OpenClaw Main Agent、腾讯ADP Router设计。v2.0全面升级：真实ERP API接入、协作流程细化、错误处理体系。

## 核心能力

### v2.0三大升级

**1. 真实API接入层（api_integration/）**
- 多ERP适配器：SAP S/4HANA、用友U8/NC/YonBIP、金蝶K3 Cloud/EAS、通用REST
- 断路器模式（Circuit Breaker）+ 故障自动降级
- 健康检查轮询（10s间隔，自动摘除异常节点）
- 演示模式保留（MockDataGenerator，variance=0.1随机波动）

**2. 跨Agent协作细化（collaboration/）**
- 细粒度任务协议（TaskMessage）：依赖声明、优先级、TTL
- 状态同步（SharedStateManager）：TTL+pub/sub通知机制
- 全链路追踪（CollaborationTracker）：trace_id/span_id + Mermaid时序图可视化

**3. 错误处理与状态管理（error_handling/）**
- 7状态任务状态机：pending→running→success/failed/retry/timeout/cancelled
- 10类异常自动分类：VALIDATION/NETWORK/TIMEOUT/AUTH/RESOURCE/NOT_FOUND等
- 5种重试策略：FIXED/EXPONENTIAL/FIBONACCI/JITTER/ADAPTIVE
- 敏感信息脱敏 + SOC2合规审计日志

## 系统架构

```
用户请求 → Orchestrator（意图识别→任务拆解→智能体调度）
    ↓
20个专业Agent：采购/生产/销售/财务/运营/战略/研发/人力/合规
    ↓
API Integration Layer（v2.0新增）
  ├─ SAP/用友/金蝶适配器（真实ERP）
  └─ 断路器+健康检查+Mock降级
```

## 目录结构

```
agent-cluster/
├── orchestrator.py              # 指挥智能体（核心调度器）
├── api_integration/              # v2.0新增：真实API接入层
│   ├── api_adapter.py           # 多ERP适配器（SAP/用友/金蝶）
│   ├── api_config.py            # 配置化管理
│   ├── api_health.py            # 健康检查+断路器
│   └── mock_data.py             # 模拟数据（开发/演示）
├── collaboration/                # v2.0新增：跨Agent协作
│   ├── task_protocol.py         # 细粒度任务协议
│   ├── state_sync.py            # 状态同步+TTL+pub/sub
│   ├── trace_tracker.py         # 全链路追踪+Mermaid
│   └── workflow_engine.py       # 混合执行引擎
├── error_handling/              # v2.0新增：错误处理
│   ├── task_state_machine.py    # 7状态任务状态机
│   ├── exception_middleware.py  # 统一异常处理
│   ├── retry_policy.py          # 5种重试策略
│   └── operation_log.py         # 操作日志+脱敏+合规
├── specialists/                 # 专业智能体
│   ├── inventory_agent.py      # 库存智能体
│   ├── logistics_agent.py       # 物流智能体
│   ├── procurement_agent.py     # 采购智能体
│   ├── finance_agent.py         # 财务智能体
│   └── doc_agent.py            # 工艺文档智能体
├── mcp_servers/                 # MCP协议封装
│   ├── erp_server.py           # ERP系统接口
│   ├── wms_server.py           # WMS仓库管理接口
│   └── srm_server.py           # SRM供应商管理接口
├── safety/                      # 安全围栏
│   ├── permission_manager.py    # RBAC权限管理
│   ├── audit_logger.py          # 全链路审计日志
│   └── human_loop.py            # 人机回环审批
└── config/                      # 配置文件
    ├── agents.yaml             # 智能体定义
    ├── workflows.yaml          # 工作流配置
    └── permissions.yaml        # 权限矩阵
```

## 快速开始

### 环境要求
- Python 3.10+
- 依赖：`pip install pyyaml fastapi uvicorn httpx aiofiles`

### 运行
```bash
cd agent-cluster
python orchestrator.py
```

### 配置（生产模式）
```bash
export SYSTEM_MODE=production
export SAP_BASE_URL=https://sap.example.com
export SAP_API_KEY=sk-xxx
export YONYOU_BASE_URL=https://yonyou.example.com
```

## 触发词

塑化报价 | 塑料原料采购 | 库存管理 | 生产排产 | 客户跟进 | 供应商比价 | B2B运营 | 工厂管理 | ERP集成 | 智能客服 | 行业KPI | 成本核算 | 硅基军团 | 工业Agent | 制造业AI | 产业互联网

## 标签

制造业AI, 产业互联网, Multi-Agent, ERP集成, 智能排产, 供应商管理, 报价系统, 智能工厂, AI运营, 企业数字化

## 分类

效率工具

## 版本

v2.0.0 - 三大升级：真实API接入层、协作流程细化、错误处理与状态管理
