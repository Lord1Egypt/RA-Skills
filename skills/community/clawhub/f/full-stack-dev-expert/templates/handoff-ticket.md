# 交接单（handoff-ticket）

> 每次委派由总指挥构造一份；跨角色传递的唯一载体。归档至 `docs/handoffs/`。

```yaml
task_id: FS-20261112-001          # FS-<yyyymmdd>-<序号>
stage: 设计                        # 逆向/需求/设计/实现/质保/交付/文档
role: architect                    # 本次委派的目标角色

user_brief: |                      # 用户原话，逐字保留，不转述
  <原话>

stack:                             # 已锁定的技术栈（未定则"待选型"）
  backend: Java17/SpringBoot3
  frontend: React18
  database: MySQL8
  cache: Redis7

artifacts:                         # 已有产出物（docs/ 相对路径）
  - docs/requirements-spec.md

handoff_notes: |                   # 上一角色的关键决策与关注点摘要
  <上一角色交接说明>

scope: |                           # 本次委派范围：做什么 / 不做什么
  <范围>

constraints: |                     # 约束：deadline、环境、兼容性、红线
  <约束>

dissent: |                         # 技术异议留痕（可选）：架构师终审后仍保留的异议与论据
  <异议>
```

**填写规则**：
- `user_brief` 全流水线原样透传，任何角色不得改写。
- 角色产出时在文末追加 `blocked_on`（所需他人信息）与交接字段（见各角色文件第 8 节）。
- `dissent` 仅在技术方案经架构师终审后仍存异议时填写（仲裁留痕，见 collaboration.md 第 3 节）。
