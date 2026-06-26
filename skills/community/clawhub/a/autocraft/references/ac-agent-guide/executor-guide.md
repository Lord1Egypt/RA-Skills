# 执行子代理规范

**适用角色**: 执行子代理（ac-glm5 / ac-minimax / ac-kimi）

---

## 执行流程

1. **识别任务类型** — 确定 BUILD-CODE / BUILD-TEST / TEST-RUN / BUILD-ENV / DOC / DESIGN
2. **选择辅助skill** — 根据任务类型，参考下方skill索引，读取对应skill
3. **读取输入文件** — 理解设计文档、需求说明等输入材料
4. **执行任务** — 按照skill指引生成代码/文档/测试
5. **质量自检** — 代码类任务运行语法检查，文档类任务检查结构完整性
6. **写JSON结果文件** — 格式见 `shared-rules.md`
7. **结束** — AutoCraft引擎会自动读取JSON结果文件并启动验证

---

## 任务类型与质量要求

### BUILD-CODE（程序代码）

**质量标准**:
- 代码可运行，无语法错误
- 有类型注解和docstring
- 有错误处理
- 新路由必须在main.py中注册（后端）

**后端（FastAPI + Python）**:
- 使用FastAPI路由 + Pydantic模型
- SQLAlchemy ORM操作数据库，禁止原始SQL
- 错误处理用HTTPException

**前端（Vue3 + Element Plus）**:

| 场景 | 读取skill | 路径 |
|------|----------|------|
| Vue3开发 | Vue | `~/.openclaw/workspace/skills/vue/SKILL.md` |
| Element Plus组件 | element-plus-vue3 | `~/.agents/skills/element-plus-vue3/SKILL.md` |

### BUILD-TEST（测试生成）

**质量标准**:
- 覆盖核心场景
- 只写测试不运行
- 断言严格度不低于设计文档验收标准
- 测试用例数量不少于设计文档要求

### TEST-RUN（测试执行）

**质量标准**:
- 运行测试，如实报告结果
- **不得修改任何代码**（测试代码和程序代码都不改）
- 失败分类：`test_issue`(测试代码问题) / `code_issue`(程序代码bug) / `env_issue`(环境问题)

### BUILD-ENV（环境搭建）

- 数据库迁移、依赖安装、配置初始化等
- 产出物写入项目目录

### DOC（文档生成）

- 开发报告：总结实现过程、产出物、关键变更
- 测试报告：总结测试结果、覆盖率、发现问题

### DESIGN（设计文档）

按设计规范生成，必须读取对应规范文件：

| 文档类型 | 规范文件 |
|---------|---------|
| PRD | `references/design-specs/doc-specs/01-PRD规范.md` |
| 系统功能设计 | `references/design-specs/doc-specs/03-系统功能设计文档规范.md` |
| 技术方案 | `references/design-specs/doc-specs/04-技术方案文档规范.md` |
| API设计 | `references/design-specs/doc-specs/07-API设计文档规范.md` |
| 数据库设计 | `references/design-specs/doc-specs/08-数据库设计文档规范.md` |
| UI设计 | `references/design-specs/doc-specs/05-UI设计文档规范.md` |
| 组件规范 | `references/design-specs/doc-specs/06-组件规范文档规范.md` |
| 业务流程 | `references/design-specs/doc-specs/02-业务流程文档规范.md` |

---

## Skill索引

| 场景 | 读取skill | 路径 |
|------|----------|------|
| Node.js/Express | NodeJS | `~/.openclaw/workspace/skills/nodejs/SKILL.md` |
| TypeScript | TypeScript | `~/.openclaw/workspace/skills/typescript/SKILL.md` |
| JavaScript | JavaScript | `~/.openclaw/workspace/skills/javascript/SKILL.md` |
| 数据库SQLite | SQLite | `~/.openclaw/workspace/skills/sqlite/SKILL.md` |
| 数据库MySQL | MySQL | `~/.openclaw/workspace/skills/mysql/SKILL.md` |
| 代码格式化+lint修复 | fix | `~/.agents/skills/fix/SKILL.md` |
| Streamlit | developing-with-streamlit | `~/.agents/skills/developing-with-streamlit/SKILL.md` |
| Tailwind CSS | tailwind-design-system | `~/.agents/skills/tailwind-design-system/SKILL.md` |
| 高质量前端界面设计 | frontend-design | `~/.agents/skills/frontend-design/SKILL.md` |
| UI/UX专业设计 | ui-ux-pro-max | `~/.agents/skills/ui-ux-pro-max/SKILL.md` |
