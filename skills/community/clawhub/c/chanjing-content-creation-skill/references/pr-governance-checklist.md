# PR 治理清单（最小门禁）

提交涉及 `chanjing-content-creation-skill` 的变更前，按以下清单逐项确认。

## 结构与命名

- [ ] 三层结构未破坏（`common/`、`products/`、`orchestration/`）
- [ ] 新增或变更文件命名符合仓库规范
- [ ] 根 `SKILL.md` 保持“路由入口”定位，未塞入产品级实现细节

## 门控与运行时契约

- [ ] 根 `SKILL.md` frontmatter `metadata.openclaw.requires` 与 `manifest.yaml` 对齐
- [ ] 依赖/环境变量/副作用变更已同步到 `references/top-level-runtime-contract.md`
- [ ] 新增外部依赖（二进制、环境变量）已在契约中声明

## Workflow 与错误语义

- [ ] 变更的 L2/L3 `Standard Workflow` 使用统一模板
- [ ] 失败分支覆盖 `need_param`、`auth_required`、`upstream_error`、`timeout`
- [ ] 跨产品降级场景有“先确认再切换”的描述

## 评测与回归

- [ ] 已至少运行 `evals/router-evals.jsonl` 中与本次变更相关的样例
- [ ] 路由准确率与关键链路结果已记录
- [ ] 文档引用路径可用，无断链

## 安全与边界

- [ ] 未提交任何真实密钥/凭证
- [ ] 未引入越权写盘路径（超出契约约束）
- [ ] 未新增“临时脚本替代正式 scripts 入口”的行为
