# 仓库结构与开发规范（dev-standards）

> 产出者：技术文档工程师。归档：`docs/dev-standards.md`。
> 真值源：`docs/architecture.md`（目录结构）与 `references/standards/*`（编码规范）——
> 本文件只链接与导航，不复制规范正文（同一信息只维护一处）。
> 受众：全部开发者/新成员。

## 1. 仓库拓扑

- 单仓 or monorepo：<拓扑说明>
- monorepo 判定规则：什么进 `packages/`（被 ≥2 个应用复用且接口稳定），
  什么留 app 内（仅本应用使用）；新增共享包需 ADR。

```
<目录树 + 每目录职责一句话>
```

## 2. 开发工作流

- 分支模型：<trunk-based / 短分支 feature flow>。
- 提交规范：<commit message 约定>。
- CI 门禁：<lint/test/build 通过才可合并>（对齐 DevOps 流水线配置）。

## 3. 编码规范索引（按栈）

| 层 | 规范 | 强制项摘要（≤3 条） |
|---|---|---|
| 后端 | standards/backend-*.md | |
| 前端 | standards/frontend-*.md | |
| API | standards/api-design.md | |
| 数据库 | standards/database.md | |

## 4. 本地开发速查

```bash
# 环境/安装/启动/测试 一屏速查
```

## 5. 例外与豁免

- 偏离规范的例外：<理由 + ADR 链接 + 有效期>；无记录的偏离按违规处理。
