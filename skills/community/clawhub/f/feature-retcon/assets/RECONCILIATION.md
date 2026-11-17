---
schema_version: {{SCHEMA_VERSION}}
round_id: {{ROUND_ID}}
status: executing
authority_root: {{AUTHORITY_ROOT}}
target_stage: {{TARGET_STAGE}}
completion_stage: {{COMPLETION_STAGE}}
created_at: {{CREATED_AT}}
confirmed_at: {{CONFIRMED_AT}}
version_control: {{VERSION_CONTROL}}
baseline_ref: {{BASELINE_REF}}
---

# 追平契约

> 本文件含本轮恢复载荷，仅限本地使用。保持文件权限为 `0600`，不要暂存或提交。

## 权威依据

- 待填写：权威根及判定证据。

## 已确认的变更断言

### 被推翻的行为

- 待填写。

### 当前目标行为

- 待填写。

### 保持不变

- 待填写。

### 明确排除

- 待填写。

### 兼容性与迁移影响

- 待填写。

## 目标与边界

- 本次执行上限（target_stage）：待填写。
- 整轮闭环终点（completion_stage）：待填写；达到执行上限不等于可以关闭。
- 可写工作根：待填写。
- 只读工作根：待填写。
- 已确认删除：待填写。
- 已授权 Hook：待填写。

## 产物依赖图与影响范围

- 待填写各语义阶段、路径和数量。

## 冲突与风险

- 待填写工作树冲突、无版本基线、敏感载荷和不可验证项。

## 阶段检查

- [ ] 需求
- [ ] 设计
- [ ] 任务
- [ ] 实现
- [ ] 验证

## 残留签名

- 待填写词法签名与行为签名。

## 验证基线

- 待填写命令、环境和结果。

## 写前恢复日志

<!-- feature-retcon:journal:begin -->
```json
{{JOURNAL_JSON}}
```
<!-- feature-retcon:journal:end -->

## 执行记录与阻塞

- 待填写每层结果、闭包补充、实质范围扩张和阻塞。
- 阶段性暂停时记录：已完成、剩余工作、下次所需授权；保留本契约和原始恢复日志。

## 完成门槛

- [ ] 变更断言已全部吸收。
- [ ] 整轮闭环终点及全部上游阶段已通过门槛，剩余工作为零。
- [ ] 新需求可追踪到闭环终点。
- [ ] 所有残留签名命中均已解释。
- [ ] 追平水位和阶段陈旧状态已更新。
- [ ] 契约未被 Git 跟踪或暂存。
- [ ] 恢复日志通过机械校验。
- [ ] 本契约不再包含独有的有效要求。

逐项填写证据依据。清单用于人工复核；脚本关闭还需要独立关闭证据，不能批量勾选代替验证。
