# CMS Executor — Architecture Design

> **Gradial GEO 时代的 Agent 集群能力扩展**  
> 将"洞察→执行"闭环从分析层推进到 CMS 直连写入层，让现有 30 个 Agent 拥有直接操作电商/建站平台的能力。

---

## 1. 系统全景

```
┌─────────────────────────────────────────────────────────────────┐
│                    M-A3 Agent Cluster (30 agents)                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ GEO      │ │ Amazon   │ │ Content  │ │ Finance  │   ...     │
│  │ Analyst  │ │ Operator │ │ Creator  │ │ Agent    │           │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘           │
│       └─────────── │ ──────────│────────────┘                 │
│                     ▼                                           │
│          ┌─────────────────────┐                               │
│          │   CMS Executor API  │  ← agent_integration.py       │
│          │  (MCP Protocol)    │                               │
│          └─────────┬───────────┘                               │
│                    │                                            │
│   ┌────────────────┼──────────────────────────────────────┐   │
│   │                ▼                                          │   │
│   │  ┌─────────────────────────────────────────────────┐    │   │
│   │  │              Execution Engine                   │    │   │
│   │  │  ┌─────────┐  ┌──────────┐  ┌──────────────┐  │    │   │
│   │  │  │Executor │  │Approval  │  │ Rollback     │  │    │   │
│   │  │  │         │←→│ Workflow │←→│ Manager      │  │    │   │
│   │  │  └────┬────┘  └──────────┘  └──────────────┘  │    │   │
│   │  │       │                                    │    │   │
│   │  │       ▼                                    │    │   │
│   │  │  ┌─────────┐  ┌──────────┐  ┌────────────┐  │    │   │
│   │  │  │ Audit  │  │Safety   │  │ Version   │  │    │   │
│   │  │  │ Logger │  │Sandbox  │  │ Snapshot  │  │    │   │
│   │  │  └─────────┘  └──────────┘  └────────────┘  │    │   │
│   │  └─────────────────────────────────────────────────┘    │   │
│   │                     │                                  │   │
│   └─────────────────────┼──────────────────────────────────┘   │
│                         ▼                                        │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│   │WordPress │ │ Shopify  │ │ Amazon   │ │ Magento  │  Custom  │
│   │Connector │ │Connector │ │Connector │ │Connector │  Sites   │
│   │ (REST)   │ │(GraphQL) │ │ (SP-API) │ │ (REST)   │          │
│   └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 核心设计原则

| 原则 | 说明 |
|------|------|
| **零信任写入** | 所有 CMS 写入必须经过审批流程（手动/自动） |
| **幂等性优先** | 所有写操作支持幂等执行，防止重复提交 |
| **快照回滚** | 每次变更前自动创建可恢复快照 |
| **Agent 沙箱** | Agent 调用 CMS 能力前必须在安全沙箱中预演 |
| **全链路审计** | 每次操作产生不可篡改的审计记录 |
| **渐进式暴露** | 能力按 Agent 角色分级暴露（read → write → admin） |

---

## 3. CMS 连接器抽象层

### 3.1 连接器基类 (`connectors/base_connector.py`)

```
BaseCMSConnector (ABC)
├── platform: str              # "wordpress" | "shopify" | "amazon" | "magento" | "custom"
├── credentials: Credentials     # 加密存储的凭据
├── capabilities: list[str]    # ["create_post", "update_post", "delete_post", ...]
├── api_base: str             # API endpoint base URL
│
├── async connect()            # 建立连接（带连接池复用）
├── async disconnect()         # 断开连接
├── async health_check()       # 健康检查
│
├── async read(resource_id)   # 读取单个资源
├── async list(filters)        # 列表查询
├── async create(data)         # 创建资源（幂等 Key 防止重复）
├── async update(resource_id, data)   # 更新资源（先快照）
├── async delete(resource_id)  # 删除资源（软删除优先）
│
├── async snapshot(resource_id)  # 创建变更前快照
├── async rollback(snapshot_id)   # 从快照恢复
│
├── to_cms_operation(op)      # 将统一操作转换为平台原生格式
└── normalize_response(resp)   # 归一化响应格式
```

### 3.2 平台能力矩阵

| 操作 | WordPress | Shopify | Amazon SP-API | Magento | Custom |
|------|-----------|---------|---------------|---------|--------|
| 读取内容 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 创建内容 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 更新内容 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 删除内容 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 上传媒体 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 更新库存 | - | ✅ | ✅ | ✅ | ✅ |
| 更新价格 | - | ✅ | ✅ | ✅ | ✅ |
| SEO 元数据 | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 4. 执行引擎 (`engine/`)

### 4.1 执行编排器 (`executor.py`)

```
CMSTaskExecutor
│
├── execute(plan, context)    # 主入口，编排完整执行流程
│   ├── 1. validate_plan()    # 验证执行计划合法性
│   ├── 2. check_sandbox()    # Agent 沙箱预演（高风险操作）
│   ├── 3. submit_approval()  # 提交审批（根据风险等级）
│   ├── 4. await_approval()   # 等待审批（同步/异步）
│   ├── 5. create_snapshot()   # 创建变更前快照
│   ├── 6. execute_ops()      # 执行写操作（幂等保护）
│   ├── 7. verify_result()    # 验证执行结果
│   └── 8. emit_audit()       # 记录审计日志
│
├── execute_batch(plans)      # 批量执行（并行/串行）
├── preview(plan)             # 仅预览，不实际执行
└── cancel(execution_id)      # 取消正在执行的任务
```

### 4.2 审批工作流 (`approval.py`)

```
ApprovalWorkflow
│
├── RiskLevel 枚举: LOW / MEDIUM / HIGH / CRITICAL
│
├── determine_risk_level(op)  # 基于操作类型+数据量+目标平台评估风险
│
├── ApprovalChain
│   ├── LOW:     Auto-Approve（记录即放行）
│   ├── MEDIUM:  Content-Creator Agent 自审
│   ├── HIGH:    Chief-of-Staff 审批
│   └── CRITICAL: 人工介入（发送通知）
│
├── submit(plan, risk_level)  # 提交审批
├── approve(execution_id)     # 批准
├── reject(execution_id, reason)  # 拒绝
├── escalate(execution_id)    # 升级
└── get_status(execution_id) # 查询审批状态
│
├── 审批超时: MEDIUM=10min, HIGH=1h, CRITICAL=24h
└── 超时处理: 自动降级或通知
```

### 4.3 回滚机制 (`rollback.py`)

```
RollbackManager
│
├── SnapshotStore            # 快照存储（文件系统/S3）
│   ├── snapshots/           # 按平台/日期组织
│   │   ├── wordpress/
│   │   ├── shopify/
│   │   └── amazon/
│
├── create_snapshot(op)      # 创建变更前快照
│   ├── 资源当前状态 JSON
│   ├── 操作元数据（时间/执行人/Agent）
│   └── 变更指纹（SHA256）
│
├── rollback(snapshot_id)    # 从快照恢复
│   ├── 验证快照完整性
│   ├── 确认回滚目标仍存在
│   ├── 执行逆向操作
│   └── 验证恢复结果
│
├── list_snapshots(filters)  # 列出可用快照
├── compare_versions(id1, id2) # 对比两个版本差异
└── auto_cleanup(retention_days=30)  # 自动清理过期快照
```

### 4.4 审计日志 (`audit.py`)

```
CMSAuditLogger
│
├── 继承自 agent-cluster/safety/audit_logger.py 的 AuditLogger
│
├── 扩展事件类型:
│   ├── CMS_CONNECT        # CMS 连接建立
│   ├── CMS_DISCONNECT     # CMS 连接断开
│   ├── CMS_READ           # 内容读取
│   ├── CMS_WRITE          # 内容写入（核心事件）
│   ├── CMS_APPROVAL       # 审批动作
│   ├── CMS_ROLLBACK       # 回滚操作
│   └── CMS_SANDBOX        # 沙箱执行
│
├── log_cms_operation(op)  # 结构化记录 CMS 操作
│   ├── platform, resource_id, operation_type
│   ├── before_snapshot_id, after_snapshot_id
│   ├── risk_level, approval_status
│   └── agent_id, execution_id
│
├── generate_compliance_report()  # 生成合规报告
└── export_audit_trail(start, end)  # 导出审计轨迹
```

---

## 5. Agent 集成 (`agent_integration.py`)

### 5.1 调用接口

```python
# 方式 1: 直接调用（通过 Python import）
from agent_integration import CMSExecutorClient

client = CMSExecutorClient(agent_id="geo_analyst_01")
result = await client.execute(
    platform="wordpress",
    operation="update_post",
    resource_id="post_12345",
    data={"content": "Updated SEO content..."},
    agent_context={"agent_id": "geo_analyst_01", "intent": "seo_optimization"}
)

# 方式 2: MCP Protocol（通过 MCP Gateway）
# MCP 工具: cms_execute, cms_preview, cms_rollback, cms_health
```

### 5.2 角色权限矩阵

| Agent 角色 | READ | WRITE | ADMIN | 特殊权限 |
|------------|------|-------|-------|---------|
| geo_analyst | ✅ | ✅ (preview) | ❌ | cms_preview |
| content_creator | ✅ | ✅ (own content) | ❌ | cms_preview |
| amazon_operator | ✅ | ✅ (inventory/price) | ❌ | amazon specific |
| chief_of_staff | ✅ | ✅ | ✅ | cms_rollback |
| admin | ✅ | ✅ | ✅ | ALL |

### 5.3 与 GEO MCP 连接器的集成

```
GEO Intent → GEO Analyst Agent
              ↓
    Gradial GEO Engine（分析/生成）
              ↓
    CMS Executor Client（执行）
              ↓
    CMS Executor API → Approval → CMS Connector
```

---

## 6. 安全设计

### 6.1 四层安全模型

```
Layer 1 — Authentication（认证）
  └── API Key / OAuth Token（平台级别加密存储）

Layer 2 — Authorization（授权）
  └── RBAC: Agent 角色 → CMS 能力映射表

Layer 3 — Safety Sandbox（安全沙箱）
  └── 高风险操作（delete/mass_update）在沙箱中预演
  └── 危险关键词检测（"DROP TABLE"、"rm -rf"）

Layer 4 — Audit Logging（全链路审计）
  └── 所有操作不可篡改记录
  └── SOC 2 合规报告
```

### 6.2 危险操作黑名单

```
🚫 DELETE 整站 / 全量删除
🚫 UPDATE price/quantity 为 0（无下限保护）
🚫 修改管理员账户凭据
🚫 执行任意 SQL / 代码注入
🚫 批量覆盖（非增量更新）
```

---

## 7. 文件结构

```
agent-cluster/cms-executor/
├── ARCHITECTURE.md                    # 本文档
├── __init__.py
├── agent_integration.py               # Agent 调用接口 + MCP 暴露
│
├── connectors/
│   ├── __init__.py
│   ├── base_connector.py              # ABC 连接器基类
│   ├── wordpress_connector.py         # WordPress REST API
│   ├── shopify_connector.py           # Shopify GraphQL
│   ├── amazon_connector.py            # Amazon SP-API
│   └── magento_connector.py           # Magento REST
│
├── engine/
│   ├── __init__.py
│   ├── executor.py                    # 任务编排引擎
│   ├── approval.py                    # 审批流程
│   ├── rollback.py                    # 快照回滚
│   └── audit.py                       # CMS 专用审计
│
└── tests/
    ├── __init__.py
    ├── test_base_connector.py
    ├── test_wordpress_connector.py
    ├── test_shopify_connector.py
    ├── test_executor.py
    ├── test_approval.py
    └── test_rollback.py
```

---

## 8. 依赖关系

```
agent-cluster/
├── safety/audit_logger.py   ← CMSAuditLogger 继承
├── error_handling/          ← 异常处理复用
├── execution/circuit_breaker.py  ← 熔断保护
└── quality/gate.py          ← 质量门禁复用
```

---

## 9. 验收标准

- [ ] 4 个平台连接器（WordPress/Shopify/Amazon/Magento）全部实现
- [ ] 执行引擎支持同步/异步审批
- [ ] 回滚机制在 5 秒内完成单资源恢复
- [ ] 审计日志覆盖 100% 的写操作
- [ ] 沙箱预演对 Agent 透明，执行时间 < 2 秒
- [ ] 所有测试通过 pytest（≥ 85% 覆盖率）
- [ ] MCP 协议正确暴露 CMS 工具集
