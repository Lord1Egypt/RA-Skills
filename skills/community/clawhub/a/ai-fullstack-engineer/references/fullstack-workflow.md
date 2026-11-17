# AI-native 全栈工作流

> 把「前端 + 后端 + 数据库」从三件割裂的事，变成一条 AI 可并联推进的流水线。本 playbook 是 AI 全栈应用工程师的总纲。

## 为什么需要这条工作流

传统全栈开发的最大摩擦在**联调**：前端等后端接口、后端改字段前端崩、类型对不上只能运行时才发现。AI-native 工作流用三件事消掉摩擦：

1. **契约优先（Contract-First）** —— 先定 OpenAPI，前后端按同一份契约并行。
2. **类型安全（Type-Safe）** —— 用 [scripts/gen_types_from_openapi.py](../scripts/gen_types_from_openapi.py) 从契约生成 TS 类型，编译期拦截字段错位。
3. **脚手架即基线（Scaffold-as-Baseline）** —— 用 [scripts/scaffold_fullstack.py](../scripts/scaffold_fullstack.py) 一次性产出可运行骨架，把"搭环境"从 hours 降到 minutes。

## 端到端流程

```
1. 需求与领域模型
   └─ 识别实体/聚合、读写比例、权限层级 → 产出领域词汇表
2. 契约优先：定义 API（references/backend-playbook.md → api-design）
   └─ 产出 openapi-spec.yaml（用 assets/openapi-spec-template.yaml 起手）
3. 脚手架：scaffold_fullstack.py 生成前后端骨架
   └─ 后端（fastapi/express）+ 前端（react/vue）+ 数据库占位
4. 并行推进
   ├─ 后端：按契约实现端点、数据库 Schema、架构分层（backend-playbook）
   └─ 前端：gen_types_from_openapi.py 生成类型 → 组件开发 + CSS 布局（frontend-playbook）
5. 类型安全联调：前端用生成类型调用后端，编译期校验
6. AI 辅助调试：browser-devtools 自动化验证 UI 与接口（frontend-playbook → devtools）
7. 性能与质量门禁：Lighthouse / CWV + 后端压测（frontend-playbook → performance）
8. 交付：docker-compose 一体编排 + CI 联合构建（assets/）
```

## 阶段 1：需求与领域模型

不要直接写代码。先和用户的业务语言对齐：

- 列出核心实体（User / Order / Product…）与关系（1:N、M:N）。
- 标注每个实体的**读写比例**（决定索引与缓存策略，见 backend-playbook → database-design）。
- 标注权限层级（决定 API 鉴权与后端中间件）。
- 产出一张**领域词汇表**，前后端共用同一术语（避免 `userId` vs `uid` 之争）。

产物：`DOMAIN.md` 或直接在对话里确认实体清单。

## 阶段 2：契约优先（关键）

在写任何实现前，先写 OpenAPI 规范。好处：

- 前端可基于契约**立即**生成类型并开始组件开发，无需等后端。
- 后端实现被契约"钉死"，减少随意改字段。
- 可自动生成文档、Mock Server、客户端。

起点：复制 [assets/openapi-spec-template.yaml](../assets/openapi-spec-template.yaml)，补全 `paths` 与 `components.schemas`。

> 契约稳定性原则（详见 backend-playbook → api-design）：名词复数、HTTP 语义准确、状态码精确、分页统一、错误可调试。

## 阶段 3：脚手架

```bash
python3 scripts/scaffold_fullstack.py --name my-saas --be fastapi --fe react
```

生成的骨架包含：

- `backend/`：FastAPI 应用骨架（main / config / models / schemas / api / services / dependencies）+ `requirements.txt`
- `frontend/`：Vite + React 骨架（package.json / src/App.tsx / src/api/client.ts / src/components/）
- `docker-compose.yaml`：compose 占位（引用 assets 模板思路）
- `README.md`：本地启动说明

> 脚手架是"基线"不是"成品"——它解决重复劳动，业务逻辑仍需你填充。

## 阶段 4：并行推进（前后端解耦）

- **后端**：按 [references/backend-playbook.md](backend-playbook.md) 的 api-design / backend-patterns / database-design / fastapi-python 落地。
- **前端**：先跑 `gen_types_from_openapi.py` 把契约变 TS 类型，再按 [references/frontend-playbook.md](frontend-playbook.md) 的 component-builder / css-master / web-performance 开发。

两端可以**同时开工**，唯一硬依赖是那份 OpenAPI 契约。

## 阶段 5：类型安全联调

前端调用后端用生成的类型：

```ts
import type { User, CreateUserReq } from "./api/types";
// 字段名/类型由契约保证，拼错编译期就报错
const res: User = await api.post<User>("/users", body as CreateUserReq);
```

若后端改了字段 → 重新生成类型 → 前端编译报错点 → 精准定位，而非线上 500。

## 阶段 6：AI 辅助调试

用 `browser-devtools` 子技能自动化验证：

```bash
npx -y chrome-devtools-axi open http://localhost:5173
# 基于快照 ref 交互、截图、跑 lighthouse 审计
```

把"人肉点页面"变成可复现的脚本，调试结果可回放、可交给 CI。

## 阶段 7：性能与质量门禁

- 前端：`web-performance` 跑 Lighthouse，盯 LCP / INP / CLS。
- 后端：压测关键端点，查 N+1、慢查询、连接池（backend-playbook → backend-patterns / database-design）。
- 门禁：把 [assets/ci-fullstack.yml](../assets/ci-fullstack.yml) 接进仓库，PR 阶段卡 build / test / lint。

## 阶段 8：交付

- 本地：`docker-compose up` 一键起前后端 + 数据库（基于 [assets/docker-compose.fullstack.yaml](../assets/docker-compose.fullstack.yaml)）。
- CI：[assets/ci-fullstack.yml](../assets/ci-fullstack.yml) 联合构建前后端、跑测试。
- 文档：`docs-writer` 生成 API 文档与 README。

## 常见反模式

| 反模式 | 后果 | 正确做法 |
|--------|------|----------|
| 后端先写完前端才开始 | 联调地狱、进度翻倍 | 契约优先，两端并行 |
| 手写重复类型 | 字段错位、运行时崩 | `gen_types_from_openapi.py` 生成 |
| 每个项目手搭骨架 | 重复劳动、风格漂移 | `scaffold_fullstack.py` 基线 |
| 性能上线前才测 | 返工成本高 | 阶段 7 提前进流程 |

## 决策速查

- **技术栈**：Python 后端 → FastAPI（async + Pydantic）；Node 后端 → Express + 分层。前端 → React/Vue + Tailwind。
- **数据库**：关系型首选 PostgreSQL；ORM 选型见 backend-playbook → database-design。
- **何时引入子技能**：具体技能问题（如"这个 Grid 怎么写"）直接调 [skills/css-master](../skills/css-master/SKILL.md)；方法论/跨端问题回本 playbook。
