# 技术栈路由（架构师与总指挥共用）

原则：**既有项目延续既有栈，新项目按决策树选型，选型结论必须记入 ADR。**
禁止"因为我会某栈"而选型；每个决策给出理由与被否方案。

## 1. 后端选型决策树（新项目）

```
项目是什么类型？
├─ 企业级/多人团队/强类型诉求/长生命周期/生态最全
│   → Java 17+ / Spring Boot 3.x  （规范: standards/backend-java-spring.md）
├─ 云原生/Serverless/K8s 常驻低内存/GraalVM native/快速启动
│   → Java 17+ / Quarkus 3.x  （规范: standards/backend-quarkus.md；
│     ORM 层 JPA/Hibernate 共用 standards/backend-jpa-hibernate.md）
├─ 前后端同构/全栈单人效率优先/实时类(IoT/聊天)
│   → Node.js 20+ / NestJS  （规范: standards/backend-node-nestjs.md）
├─ AI/数据科学/快速原型/算法密集
│   → Python 3.11+ / FastAPI  （规范: standards/backend-python-fastapi.md）
└─ 极高并发/网关与基础设施/长连接高密度/追求部署物极简
    → Go 1.22+  （规范: standards/backend-golang.md）
```

**Spring Boot vs Quarkus 仲裁**：默认 Spring Boot（生态与人才储备最全）；
以下任一成立才选 Quarkus——Serverless/FaaS 目标、native image 冷启动硬指标（<100ms）、
K8s 高密度部署内存硬约束、团队明确偏好云原生 Java 栈。

**Java 栈 ORM 统一**：JPA/Hibernate（Spring Data JPA / Quarkus Panache 均是其上封装），
共性纪律见 `standards/backend-jpa-hibernate.md`；MyBatis 仅在既有项目已用时延续。

## 1.1 API 风格选择（REST 默认）

```
REST 是默认风格（standards/api-design.md）
└─ 同时满足以下两条才立项 GraphQL（ADR 强制，规范: standards/api-graphql.md）：
   ① 客户端多样且取数字段差异大 / 多数据源聚合网关 / 字段级高频演进 之一成立
   ② 团队接受服务端复杂度上升（DataLoader/复杂度限制/持久化查询三件套为强制成本）
```

禁止"用 GraphQL 因为它新"；同一资源双轨暴露（REST+GraphQL）需 ADR 明确并存与退役边界。

## 2. 前端选型决策树

```
├─ 复杂状态/大型生态/B 端复杂交互 → React 18+ (standards/frontend-react.md)
├─ 渐进增强/上手快/C 端活动页/亚洲生态 → Vue 3 + Vite (standards/frontend-vue3.md)
├─ SEO/首屏/内容站/全栈一体 React → Next.js 14+ App Router (standards/frontend-nextjs.md)
│   （纯 SPA 不为 SEO 上 Next；Nuxt 对应 Vue 侧同类场景）
└─ HarmonyOS 目标平台 → ArkTS（路由到宿主鸿蒙技能，本包只做契约衔接）
```

### UI 层选型（与框架决策解耦，二选一不混用）

| 场景 | 选型 | 规范 |
|---|---|---|
| **管理后台/中后台（默认）** | React + Ant Design 5 | `standards/frontend-antd.md` |
| C 端高定制/设计系统自持/现代视觉 | React + Tailwind CSS 3.4 + shadcn/ui | `standards/frontend-tailwind-shadcn.md` |
| Vue 侧管理后台 | Vue3 + Element Plus（沿 vue3 规范执行，antd 规范的列表页/表单范式可类比套用） | `standards/frontend-vue3.md` |
| 纯样式工具需求（任意 React 项目内） | Tailwind 作为原子样式层 | `standards/frontend-tailwind-shadcn.md` §1 |

仲裁：管理后台无定制视觉要求 → antd（表格表单开箱即用，交付最快）；
有品牌级视觉定制要求 → Tailwind + shadcn；antd 与 shadcn/ui 同一项目不并存。

## 3. 数据与中间件选型

| 场景 | 选型 | 备注 |
|---|---|---|
| 默认关系库 | MySQL 8 | 通用业务首选 |
| 复杂分析/GIS/JSON 重 | PostgreSQL 16 | 数组、JSONB、窗口函数 |
| 嵌入式/单机工具 | SQLite | 免部署 |
| 缓存/会话/排行榜 | Redis 7 | 必须 DBA 明确淘汰策略 |
| 全文检索 | 先用 DB 内建，量大再 Elasticsearch | 避免过早引入 |
| 消息队列 | 确有削峰/解耦诉求才引入 | ADR 说明 |

## 4. 强制规范索引

| 层 | 必须遵循 |
|---|---|
| API 设计 | `standards/api-design.md`（REST 默认）；GraphQL 走 `standards/api-graphql.md`（ADR 门槛） |
| 数据库 | `standards/database.md`（命名、索引、迁移、事务） |
| 后端实现 | Spring Boot → `backend-java-spring.md`；Quarkus → `backend-quarkus.md`；Java ORM 共用 `backend-jpa-hibernate.md`；NestJS → `backend-node-nestjs.md`；FastAPI → `backend-python-fastapi.md`；Go → `backend-golang.md` |
| 前端实现 | React → `frontend-react.md`；Next.js → `frontend-nextjs.md`；Vue3 → `frontend-vue3.md` |
| UI 组件层 | 管理后台 → `frontend-antd.md`；C 端定制 → `frontend-tailwind-shadcn.md`（二选一不混用） |
| 管理后台角色路由 | 管理域实现由 admin-frontend-dev / admin-backend-dev 承担（见 orchestration.md 管理后台路由规则） |

## 5. 版本与依赖红线

- 锁定主版本（Spring Boot 3.x、Quarkus 3.x、NestJS 10.x、FastAPI 0.11x、Go 1.22+、
  React 18、Next.js 14+/15、Vue 3.4+、Ant Design 5.x、Tailwind 3.4+），禁止 alpha/beta/rc。
- 新增任何依赖需在 ADR 或需求规格中登记：包名、版本、用途、替代品评估。
- GraphQL 立项、antd/shadcn 切换、双 UI 层并存：均需 ADR 显式记录。
- 不为"以后可能用到"引入依赖（YAGNI）。
- 供应链：只从官方源安装；锁文件（pom 需版本锁定 / package-lock.json / uv.lock / go.sum）必须提交。
