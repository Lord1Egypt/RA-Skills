# 规范模板说明

本目录随 **`gen-coding-specs`** 技能发布（`skills/gen-coding-specs/templates/`），不依赖仓库内其他目录。

## 模板列表

| # | 文件 | 说明 | 典型行数 |
|---|------|------|---------|
| 1 | `coding.index.md` | 规范索引与上下文加载策略 | ~90 |
| 2 | `coding.api.md` | API 设计规范（支持统一 POST / RESTful 两种风格） | ~250 |
| 3 | `coding.architecture.md` | 架构原则、设计模式、数据访问 | ~170 |
| 4 | `coding.data-models.md` | 数据库设计、MyBatis-Plus 速查 | ~320 |
| 5 | `coding.vue.md` | Vue 3 + TypeScript + Pinia 规范 | ~190 |
| 6 | `coding.coding-style.md` | 命名、格式、注释、函数设计 | ~220 |
| 7 | `coding.testing.md` | 测试金字塔、AAA 模式、覆盖率 | ~240 |
| 8 | `coding.security.md` | 输入验证、认证授权、加密、漏洞防护 | ~270 |
| 9 | `coding.performance.md` | 性能目标、缓存、数据库优化、监控 | ~250 |
| 10 | `coding.documentation.md` | 注释原则、README/CHANGELOG 结构 | ~50 |
| 11 | `coding.code-review.md` | 审查流程、检查清单 | ~60 |
| 12 | `coding.version-control.md` | Git 工作流、提交信息规范 | ~260 |

## 设计原则

1. **无重复**：每个规范只定义自己关注点的核心内容，通过引用（`> 见 xxx`）避免重复
2. **AI 友好**：内容精炼，重点突出，便于 AI 模型在上下文窗口内加载
3. **按需加载**：通过 `coding.index.md` 的上下文加载策略，按任务类型只加载必要的规范
4. **可定制**：生成后可直接编辑 `docs/coding-specs/` 下的文件适配团队约定

## 规范间关系

- `architecture.md` 是架构层面的核心规范，`data-models.md` 是其数据层的补充
- `coding-style.md` 是代码格式层面的核心规范，引用 `architecture.md` 的 Java 速查
- `security.md` 是安全层面的权威规范，`api.md` 和 `code-review.md` 引用它
- `performance.md` 是性能层面的权威规范，`architecture.md` 不再重复性能内容
- `documentation.md` 已精简为最小化，JSDoc 格式由 `coding-style.md` 负责，OpenAPI 由 `api.md` 负责
