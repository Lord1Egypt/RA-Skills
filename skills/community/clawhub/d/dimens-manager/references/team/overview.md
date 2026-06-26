---
name: dimens-manager-team
slug: dimens-manager-team
description: 用于维表智联团队、成员、项目和租户隔离上下文分析，确认 teamId/projectId 与资源归属。
version: 1.0.0
author: 方块智联工作室
tags: [team, project, tenant, context, dimens-cli]
---

# dimens-manager 团队上下文章节

适用产品：

- 产品名称：`维表智联`
- 开发方：`方块智联工作室`
- 官网：[https://dimens.bintelai.com/](https://dimens.bintelai.com/)

## 执行前必读

- ✅ 团队是资源的最高隔离边界，绝大多数业务问题先确认 `teamId`
- ✅ 项目是团队下的业务单元，项目问题通常要同时带上 `teamId` 与 `projectId`
- ✅ 成员能否访问项目，不只取决于项目成员关系，还可能取决于团队角色与部门角色
- ✅ Guest、Member、Admin、Owner 的可见范围不能混为一谈
- ✅ 分析资源访问问题时，先判断团队可见性，再判断项目级权限
- ✅ 很多 CLI 命令支持显式参数、本地 profile、环境变量三种上下文来源，不能只看单次命令参数

## 命令维护表

| 命令 | 作用 | 必填参数 | 常用可选 | 细节说明 |
| --- | --- | --- | --- | --- |
| `dimens-cli team info` | 获取团队详情 | `teamId` | - | 团队是最高隔离边界，很多问题先从这里确认上下文 |
| `team_user_list` | 查询团队成员池 | `teamId` | `projectId`, `keyword` | 用于先看用户是否在团队范围内，再判断项目访问问题 |
| `dimens-cli project list` | 查询团队下项目列表 | `teamId` | `page`, `keyword`, `status` | 项目永远从团队上下文进入，排查时建议显式传 `teamId` |
| `dimens-cli project info` | 获取项目详情 | `teamId`, `id` | - | 项目更新前默认先拿当前项目数据，确认团队归属和资源边界 |
| `dimens-cli project create` | 从团队上下文创建项目 | `teamId`, `name` | `description`, `projectType` | 这是项目初始化入口，创建后应路由到 `dimens-manager/references/project/overview.md` 继续完成资源搭建 |
| `dimens-cli auth use-team` | 切换默认团队上下文 | `teamId` | - | 影响后续默认上下文，但不替代真实详情读取 |
| `dimens-cli auth use-project` | 切换默认项目上下文 | `projectId` | - | 仅在已有正确团队上下文下才安全 |

### 强调细节

- 团队和项目上下文是所有资源判断的上游前提，很多“命令没问题但数据不对”的情况，本质都是上下文拿错了。
- 如果后续要做项目更新，默认先 `project info` 拿当前数据，再改字段再 update，而不是跳过读取阶段。
- `auth use-team` / `auth use-project` 只是在本地切换默认上下文，不等于真实资源校验。
- 处理跨团队、跨项目问题时，要同时检查显式参数、本地 profile、环境变量三类上下文来源。

## 核心约束

### 1. 隔离边界

- 团队 / 空间是最高资源隔离边界
- 项目是团队下的业务单元
- 绝大多数数据访问都应该先过团队隔离，再过项目隔离

### 2. 角色分层

团队级角色决定：

- 能否管理团队
- 能否管理部门
- 能否看到团队级公共资源

项目级角色决定：

- 能否管理具体项目
- 能否编辑项目内内容
- 能否仅只读访问

### 3. 部门与权限叠加

- 部门主管可能对本部门或子部门关联项目具有更高权限
- 不能只根据“是否在项目成员表里”来判断最终权限
- Team Admin / Owner 也可能天然拥有更高项目权限

### 4. 上下文来源

CLI 的团队、项目上下文通常有三种来源：

1. 显式命令参数
2. 本地 profile 默认值
3. 环境变量覆盖

判断命令行为时要按优先级一起看，不能只盯当前命令参数。

### 5. 风险边界

- 团队与项目上下文错误，会连带影响表格、文档、工作流、权限判断
- 任何缺失 `teamId` 的结论都要谨慎，尤其是跨项目问题

## 必查文档

| Skill / references | 作用 | 什么时候必须看 |
| --- | --- | --- |
| `dimens-system-orchestrator` | 系统级任务入口与整体路由 | 处理系统建设任务时建议先看 |
| `dimens-manager/references/project/overview.md` | 项目创建、项目初始化与默认公开视图补偿 | 用户要开始落项目时必须看 |
| `dimens-manager/references/permission/overview.md` | 权限分层与资源可见性 | 分析能看不能看时建议看 |
| `dimens-manager/references/table/overview.md` | 表格、文档、字段、行数据会继承项目上下文 | 进入表域前建议看 |
| `references/context-sources.md` | 显式参数、profile、环境变量三类上下文来源 | 处理上下文覆盖时必须看 |
| `references/project-entry.md` | 如何从团队进入项目资源 | 判断项目入口时必须看 |
| `references/isolation.md` | 团队与项目隔离边界 | 处理跨团队、跨项目问题时必须看 |
| `references/examples.md` | 团队 / 项目典型问题案例 | 需要快速举例时看 |

## 使用场景示例

### 场景 1：解释为什么某个用户看不到某个项目

建议检查顺序：

1. 用户是否属于该团队
2. 用户在团队中的角色是什么
3. 项目是否为公开可见
4. 用户是否被邀请进项目
5. 用户是否因部门角色、团队角色而获得默认管理权限

如果用户下一步是“直接创建项目并继续搭系统”，不要停在 `dimens-manager/references/team/overview.md`，应继续路由到 `dimens-manager/references/project/overview.md`。

### 场景 2：查询某团队下的项目列表

```bash
dimens-cli project list --team-id TEAM1
```

注意：

- 如果当前 profile 已设置默认团队，也可以省略 `--team-id`
- 但在排查问题时，建议显式传入 `teamId`，避免被默认上下文误导

### 场景 3：切换默认上下文

```bash
dimens-cli auth use-team TEAM1
dimens-cli auth use-project PROJ1
```

注意：

- `use-project` 不应脱离团队上下文单独理解
- 变更默认上下文后，后续项目、表格、文档、AI 命令都可能受影响

## 常见错误与排查

| 错误现象 | 根本原因 | 解决方案 |
| --- | --- | --- |
| 能登录但看不到团队资源 | 用户不在该团队或角色受限 | 先查团队成员关系与团队角色 |
| 能看到团队但看不到项目 | 没被邀请进项目，或项目不可公开访问 | 继续查项目成员关系与项目可见性 |
| 某部门主管没有被拉进项目却还能管理项目 | 部门级权限向项目级继承 | 结合部门与团队角色一起判断 |
| CLI 命令结果和预期团队不一致 | 命令被本地 profile 或环境变量上下文覆盖 | 检查显式参数、profile、环境变量三者优先级 |
| 同一用户在不同项目权限不一致 | 项目级角色不同或项目挂载部门不同 | 分项目分别检查项目角色与部门关系 |

## 参考文档

- `references/context-sources.md`
- `references/project-entry.md`
- `references/isolation.md`
- `references/examples.md`
- 如需查看整个 Skill 体系的能力总览，请返回 `dimens-cli/skills/README.md`
