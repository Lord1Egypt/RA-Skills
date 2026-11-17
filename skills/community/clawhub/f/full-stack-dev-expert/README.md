# full-stack-dev-expert

全栈编程开发专家技能包：以**一个总指挥 + 14 个子角色**的开发团队模式组织的 agent/subagent 协作技能。
总指挥不写业务代码，只做接收需求、分诊路由、调度子角色、把控质量门禁四件事；
专业产出全部由子角色完成，角色间通过**交接单**传递上下文；
全体角色的一切决策遵循**《软件工程宪法》**（最高工程原则，冲突时以宪法为准）。

## 团队模型

```
              ┌──────────── 总指挥（SKILL.md） ────────────┐
              │ 分诊路由 · 调度 · 质量门禁 · 宪法守护        │
              └───────────────────┬────────────────────────┘
    ┌─────────┬─────────┬─────────┼─────────┬─────────┬─────────┐
  需求分析师   架构师    UI/UX设计师  数据库工程师  测试工程师  安全工程师
    └────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┘
       前端工程师   后端工程师          管理后台前端   管理后台后端
       （C 端域）   （通用域）          （管理后台任务时替换上两者）
                          逆向融合工程师（ORRI：观察→逆向→重建→创新）
                          代码审查员 · DevOps 工程师 · 技术文档工程师
```

**主流程**：① 需求澄清 → ② 架构设计 → ③ 并行实现 → ④ 质量保障 → ⑤ 交付部署 → ⑥ 文档归档
（按任务类型裁剪，路由表见 `references/orchestration.md`）

**管理后台路由**：任务命中"管理后台/中后台/admin/运营平台/控制台"时，管理域实现由
管理后台前后端两位专才**替换**通用前后端工程师（RBAC、审计、CRUD 三件套、权限路由）。

**逆向融合路由**：任务指向外部/未知系统的能力、协议、架构或 UI 提取融合时，先经
**逆向融合工程师**按 ORRI 方法论完成观察与逆向，再按场景子路由移交下游；合法性门禁
不通过立即终止（融合竞品能力、提取协议格式、重构摸底、未知代码库学习、UI/架构复刻）。

**执行模式**：A · Task subagent 委派（宿主支持子代理时）／ B · 上下文内换装（Read 角色文件后按契约履职）。
两种模式角色契约完全一致。

## 技术栈覆盖

| 层 | 支持栈（规范文件见 references/standards/） |
|---|---|
| 后端 | Java 17 / Spring Boot 3 · Java 17 / Quarkus 3（云原生/Serverless/native）· Node 20 / NestJS · Python 3.11 / FastAPI · Go 1.22+ |
| ORM | JPA / Hibernate（Spring 与 Quarkus 共用纪律）· TypeORM/Prisma · SQLAlchemy |
| 前端框架 | React 18 · Vue 3.4 · Next.js 14+/15（SSR/SSG/ISR）· HarmonyOS ArkTS（契约衔接） |
| UI 组件层 | Ant Design 5（管理后台默认）· Tailwind CSS 3.4 + shadcn/ui（C 端定制，与 antd 二选一不混用） |
| API 风格 | REST（默认）· GraphQL（ADR 门槛立项：DataLoader/复杂度限制/持久化查询三件套强制） |
| 数据 | MySQL 8 · PostgreSQL 16 · SQLite · Redis 7 · 迁移（Flyway/Liquibase/版本化脚本） |

## 目录结构

```
full-stack-dev-expert/
├── SKILL.md                       # 总指挥：调度中心（入口）
├── agents/                        # 14 个子角色定义
│   ├── requirements-analyst.md    #   需求分析师
│   ├── architect.md               #   架构师
│   ├── ui-ux-designer.md          #   UI/UX 设计师
│   ├── dba.md                     #   数据库工程师
│   ├── frontend-dev.md            #   前端开发工程师（C 端域）
│   ├── backend-dev.md             #   后端开发工程师（通用域）
│   ├── admin-frontend-dev.md      #   管理后台前端工程师（antd 布局/权限路由/CRUD 三件套）
│   ├── admin-backend-dev.md       #   管理后台后端工程师（RBAC/审计/列表导入导出 API）
│   ├── reverse-fusion-dev.md      #   逆向融合工程师（ORRI：观察→逆向→重建→创新）
│   ├── test-engineer.md           #   测试工程师
│   ├── security-engineer.md       #   安全工程师
│   ├── code-reviewer.md           #   代码审查员
│   ├── devops-engineer.md         #   DevOps 工程师
│   └── tech-writer.md               #   技术文档工程师（README/API/arc42+C4+ADR/专业文档集/业务流程与时序/Runbook/CHANGELOG/部署文档）
├── references/
│   ├── constitution.md            # 软件工程宪法（最高效力，全体角色必读）
│   ├── orchestration.md           # 调度协议：路由表、管理后台路由、裁剪、并行、门禁、失败处理
│   ├── stack-routing.md           # 技术栈路由：栈指纹、选型决策树、UI 层选型
│   ├── collaboration.md           # 协作协议：交接单、冲突仲裁、落盘约定
│   └── standards/                 # 14 份多栈编码规范
│       ├── api-design.md          #   REST API 设计（契约唯一依据）
│       ├── api-graphql.md         #   GraphQL（ADR 门槛 + DataLoader/复杂度/持久化查询）
│       ├── database.md            #   数据库建模与迁移纪律
│       ├── backend-java-spring.md #   Java / Spring Boot
│       ├── backend-quarkus.md     #   Java / Quarkus（云原生/Serverless）
│       ├── backend-jpa-hibernate.md #  JPA/Hibernate（Java 栈共用 ORM 纪律）
│       ├── backend-node-nestjs.md #   Node / NestJS
│       ├── backend-python-fastapi.md # Python / FastAPI
│       ├── backend-golang.md      #   Go（错误处理/并发/context 纪律）
│       ├── frontend-react.md      #   React
│       ├── frontend-vue3.md       #   Vue 3
│       ├── frontend-nextjs.md     #   Next.js App Router（Server/Client 纪律）
│       ├── frontend-antd.md       #   Ant Design 5（管理后台 UI）
│       └── frontend-tailwind-shadcn.md # Tailwind CSS + shadcn/ui
├── templates/                     # 20 个交付物模板
│   ├── handoff-ticket.md          #   交接单（角色间唯一传递载体）
│   ├── requirements-spec.md       #   需求规格
│   ├── prd.md                     #   产品需求文档（真值源 requirements-spec）
│   ├── user-stories.md            #   用户故事与用例（故事地图 + 追踪矩阵）
│   ├── architecture-design.md    #   架构设计 + ADR 索引
│   ├── arc42-doc.md               #   架构文档（arc42 12 章 + C4 分层图 + ADR 索引）
│   ├── adr.md                     #   ADR 分离档案（一个决策一个文件，Nygard 格式）
│   ├── ddd-design.md              #   领域设计与数据合同（限界上下文 → 模型 → 合同）
│   ├── dev-standards.md           #   仓库结构与开发规范（含 monorepo 判定规则）
│   ├── roadmap.md                 #   实施路线与里程碑（出口条件可验证）
│   ├── business-process.md        #   业务流程与时序文档（流程图 + 时序图 + 追踪矩阵）
│   ├── api-contract.md            #   API 契约
│   ├── ui-spec.md                 #   UI/UX 规格
│   ├── reverse-analysis.md        #   逆向分析报告（ORRI：证据档案/置信度/等价性测试）
│   ├── test-plan.md               #   测试计划
│   ├── test-report.md             #   测试报告
│   ├── deploy-guide.md            #   部署指南
│   ├── runbook.md                 #   运维手册（告警响应/故障处置/应急预案）
│   ├── changelog.md               #   变更日志（Keep a Changelog，项目根）
│   └── pr-summary.md              #   交付摘要
├── evals/evals.json               # 19 个验收用例
└── FILES.md                       # 文件清单
```

## 使用方式

- **OpenCode / Claude Code 类宿主**：将本目录复制到技能目录
  （如 `~/.local/share/opencode/skills/full-stack-dev-expert/`），由 SKILL.md 的
  description 触发加载；总指挥按宿主能力自动选择执行模式 A 或 B。
- **直接投喂**：将 SKILL.md 作为入口 prompt，按其指引 Read 对应角色与协议文件。

## 设计要点

- **宪法至上**：`references/constitution.md` 定义 29 条工程宪法与冲突优先级
  （正确性与数据安全 > 安全 > 契约与诚实 > 简单 > 交付速度），效力高于一切协议文件。
- **管理后台专才路由**：admin-frontend-dev / admin-backend-dev 替换通用前后端工程师，
  内置 RBAC、审计日志、CRUD 三件套、权限路由等管理域模式；管理端任务安全工程师强制启用。
- **逆向融合（ORRI）**：reverse-fusion-dev 以 观察→逆向→重建→创新 四阶段提取外部系统
  核心设计并融合，六类场景（竞品能力/协议格式/重构摸底/未知代码库/UI 复刻/架构复刻）
  各有子路由；观察零推测、结论挂证据与置信度、净室纪律、合法性门禁前置、等价性测试门禁。
- **契约先行**：架构阶段先出 API 契约草案，前端 Mock、后端实现、测试验证三方共用一份契约。
- **文档工程**：架构文档集（arc42 + C4 + ADR 分离档案）与专业文档集
  （PRD/用户故事与用例/领域设计/开发规范/路线图/业务流程与时序）每份单一真值源，
  技术文档工程师只转译不发明决策；INDEX.md 承担文档治理（类型/归属/更新触发/真值源映射/风险登记）。
- **交接单唯一真值源**：跨阶段只认交接单与产出物，不认"我以为"；用户原话全程逐字透传。
- **质量门禁**：每阶段有明确退出条件；同一阶段最多打回 2 次，第 3 次如实上报分歧。
- **安全一票否决**：仅限高危及以上，否决必须附带修复建议与工作量评估。
- **选型有据**：延续既有栈优先；Quarkus/GraphQL/shadcn 切换均设 ADR 门槛，不为新而新；
  任何新增依赖必须在 ADR 登记。

## 版本

- 1.4.8（2026-11-13）：第十五轮评审修复——门禁③"无 TODO 遗留关键路径"此前在
  4 个 dev 角色契约中零锚定（执行者不承载门禁要求，仅靠判定人事后打回），补
  backend/frontend/admin-frontend/admin-backend 红线：关键路径不留 TODO/FIXME
  （临时绕过必须注明原因与回归计划）；本轮同时验证：交接单 10 字段三处闭环、
  14 角色第 8 节交接字段齐全、FILES.md 与文件树双向零缺漏（54/54）、
  门禁①-⑥与角色输出契约逐项对齐。
- 1.4.7（2026-11-13）：第十四轮评审修复——evals 覆盖矩阵缺口：需求分析师、
  UI/UX 设计师、DBA 三个设计阶段核心角色此前无专属深度用例（与 description 声称的
  "各角色契约完整性"不符），补 EVAL-20「设计阶段三角色产出契约」综合用例一次覆盖；
  同时验证 pr-summary 模板归属（SKILL.md:81 总指挥交付步骤）、v1.4.6 增量引用
  真值源（宪法第 2/27/28 条、stack-routing 第 5 节）全部有效。
- 1.4.6（2026-11-13）：外部评审第二轮修复——deploy-guide 回滚步骤补迁移回滚
  破坏性警告（仅可逆迁移提供 down；down 前置：可逆性评估 + 已验证备份 + 用户
  批准，宪法第 2 条），DevOps 工作流与 database.md 迁移纪律同步补可逆性标注
  （不可逆迁移走前滚修复）；shadcn CLI 版本锁定措辞强化为显式 @x.y.z 后缀示例；
  api-contract 与 deploy-guide 的两处外发提示复核仍为占位变量/localhost 误报，不改。
- 1.4.5（2026-11-13）：第十三轮评审修复——外部评审同类脱敏缺口横向泛化：
  backend-dev 自测记录样例、test-engineer 缺陷报告复现数据、test-report 模板
  缺陷清单补脱敏纪律（真实令牌/账号/个人数据占位符呈现，宪法第 28 条）；
  reverse-analysis 模板质量门禁补"证据已脱敏"（与 1.4.4 角色侧修复对齐）；
  未锁定执行（@latest/npx）全包扫描零残留。
- 1.4.4（2026-11-13）：外部评审修复——管理后台审计日志改前改后值补敏感字段脱敏
  （密码/令牌/密钥只记 [REDACTED] 不落明文，宪法第 10 条；admin-backend-dev
  输出契约/最佳实践/红线三处 + EVAL-07 同步）；逆向观察证据归档前补脱敏步骤与
  红线（HAR/截图/录制中的认证头/Cookie/个人数据遮蔽剥离，宪法第 28 条；
  reverse-fusion-dev 工作流/红线 + EVAL-12 同步）；shadcn 组件 CLI 添加由
  @latest 改为锁定版本执行（供应链红线对齐）；api-contract 占位变量示例与
  deploy-guide localhost 健康检查经人工复核为扫描误报，不改。
- 1.4.3（2026-11-13）：第十一轮评审修复——冲突仲裁引用的交接单 `dissent`（技术异议
  留痕）字段补进协作协议字段表与交接单模板（此前为"被引用但未定义"的孤儿字段，
  与 1.4.1 修复的"业务规则编号"同类）；14 个角色文件 8 节结构与 frontmatter
  完整性程序化核查通过；全部编号体系与特殊字段定义闭环核查通过。
- 1.4.2（2026-11-13）：第十轮评审修复——ui-spec 核心交互流与 business-process
  业务流程图补双向边界声明与互链（页面交互视角 vs 端到端业务全景，消除同类重复风险，
  上轮未覆盖的交叉点）；14 份 standards 规范全量深读通过（宪法条款引用、包内引用
  完整性核查零缺陷）。
- 1.4.1（2026-11-13）：第九轮评审修复——业务流程与时序文档的"业务规则编号/GWT 编号"
  引用改为 FR 编号及其验收标准（GWT）（requirements-spec 无独立规则/GWT 编号体系，
  消除真值源缺口）；arc42 运行视图与用户故事模板补与 business-process 的双向互链；
  roadmap 模板变更记录表分隔行笔误修复。
- 1.4.0（2026-11-13）：技术文档工程师新增业务流程与时序文档能力：新增
  templates/business-process.md（流程清单/业务流程图 flowchart/关键场景时序图
  sequenceDiagram/流程-需求追踪矩阵；流程步骤真值源 requirements-spec，
  交互时序真值源 api-contract + architecture + 代码实现；必画失败分支，
  与 arc42 运行视图和用户故事行为场景互链不重复）；路由表与 pr-summary 角色表
  同步；验收用例扩至 19 个（EVAL-19）。
- 1.3.2（2026-11-13）：第八轮评审修复——roadmap 模板"变更记录"补与项目根
  CHANGELOG 的职责边界（记录路线图自身调整 vs 产品发布变更，不重复）。
- 1.3.1（2026-11-13）：第七轮评审修复——"按需裁剪"措辞显式覆盖变更日志
  （tech-writer 工作流/交接字段、质量门禁 ⑥）；EVAL-18 runbook 真值源列表与
  tech-writer 契约对齐（补可观测性基线与监控）；DevOps 交接字段标注运维素材位置。
- 1.3.0（2026-11-13）：技术文档工程师新增运维文档能力：新增 templates/runbook.md
  （运维手册：告警响应表/常见故障处置/例行操作 SOP/应急预案，真值源 DevOps 产出，
  处置命令须经 DevOps 验证）与 templates/changelog.md（Keep a Changelog 格式，
  落项目根）；DevOps 输出契约补运维素材供给；验收用例扩至 18 个（EVAL-18）。
- 1.2.10（2026-11-13）：第六轮评审修复——ui-ux-designer 输出契约"组件复用清单"的
  五态列举与同文件最佳实践及 ui-spec 模板定义统一（默认/悬停或聚焦/激活/禁用/加载）。
- 1.2.9（2026-11-13）：第五轮评审修复——pr-summary 角色启用表技术文档工程师行补
  专业文档集与 INDEX.md 产出；test-engineer 工作流"每轮出报告"补 FR 验收矩阵；
  质量门禁 ⑥ 文档行补专业文档集真值源纪律；EVAL-17 开发规范与路线图真值源措辞
  与模板对齐；README 设计要点补"文档工程"条目。
- 1.2.8（2026-11-13）：技术文档工程师新增专业文档集能力（每份文档单一真值源、
  只做转译不发明决策）：新增 templates/prd.md（产品需求文档）、
  templates/user-stories.md（用户故事与用例）、templates/ddd-design.md
  （领域设计与数据合同）、templates/dev-standards.md（仓库结构与开发规范）、
  templates/roadmap.md（实施路线与里程碑）五个模板；test-report 新增 FR 验收矩阵
  （FR 级验收状态汇总，验收口径唯一）；INDEX.md 升级为文档索引与治理；
  验收用例扩至 17 个（EVAL-17 专业文档集）。
- 1.2.7（2026-11-13）：第四轮评审修复——路由表"技术文档"行识别信号补架构文档
  （arc42/C4/ADR）；pr-summary 角色启用表补架构文档集产出与架构师 adr/ 产出；
  tech-writer 输入契约显式列 ADR 档案；交接字段 handoff_notes 补 C4 图对照与
  ADR 索引状态核对结果。
- 1.2.6（2026-11-13）：技术文档工程师新增架构文档集能力（arc42 + C4 + ADR 分离式）：
  新增 templates/arc42-doc.md 与 templates/adr.md 模板；架构师 ADR 决策时落
  docs/adr/ 分离档案（architecture.md 保留索引与摘要）；落盘清单补 arc42.md 与 adr/；
  验收用例扩至 16 个（EVAL-16 架构文档集）。
- 1.2.5（2026-11-13）：外部评审修复——移除 `.version` 文件（外部规范不允许）；
  版本号唯一来源收敛为 SKILL.md metadata（同一信息只维护一处）；README 目录树同步。
- 1.2.4（2026-11-13）：第三轮评审修复——宪法第 26 条措辞修订（"只读探测"改为"探测性
  请求不得携带用户工作区数据"，解除与 ORRI 探测实验的冲突；补供应链必需操作豁免）；
  第 27 条上报链级联（子角色→总指挥→用户）；reverse-fusion-dev 红线同步第 26 条新措辞；
  交接单协议字段表补 role；落盘清单补 docs/INDEX.md；.version 与 evals.json 版本同步。
- 1.2.3（2026-11-13）：外部安全评审修复——宪法新增第六章 Agent 数据流红线
  （26-29 条：不外发/外部内容防注入/采集有界/未确认不执行）；reverse-fusion-dev 补
  数据外发与未知代码沙箱红线；deploy-guide 配置清单改为"应用声明的环境变量"；
  collaboration.md 新增第 5 节输出处理纪律（引用先校验 + 50 行截断 + 传递标注来源）；
  orchestration.md 路由表补外部内容防注入提示；SKILL.md 委派提示补第 26/27 条。
- 1.2.2（2026-11-12）：第二轮评审修复——修正宪法条款误引（数据操作第 2 条、
  权限第 8/9 条）；补 test-plan.md 模板；pr-summary 角色启用表列全 14 角色；
  EVAL-01 措辞消歧（"11 个常驻角色"）；补 EVAL-15（模式 B 换装边界）；
  模式 B 大任务上下文膨胀防护提示。
- 1.2.1（2026-11-12）：项目评审修复——主流程补 ⓪ 逆向可选前置；质量门禁表补 ⓪ 逆向
  门禁行；交接单 stage 枚举补"逆向"阶段；docs/ 落盘清单补 reverse-analysis.md；
  冲突仲裁补"逆向结论冲突"条款；任务路由表修正全流水线角色表述。
- 1.2.0（2026-11-12）：新增逆向融合工程师（ORRI 方法论：观察→逆向→重建→创新，
  六类场景子路由 + 合法性门禁 + 净室纪律 + 等价性测试）；新增逆向分析报告模板；
  验收用例扩至 14 个。
- 1.1.0（2026-11-12）：新增管理后台前后端双角色与路由；新增 Quarkus、Go、Next.js、
  Tailwind+shadcn/ui、Ant Design、JPA/Hibernate、GraphQL 七组技术栈规范；
  新增软件工程宪法（25 条 + 冲突优先级）；验收用例扩至 11 个。
- 1.0.0（2026-11-12）：首个版本，11 子角色 + 7 规范 + 8 模板 + 6 验收用例。
