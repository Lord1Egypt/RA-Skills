# dimens-manager 团队上下文章节 项目入口说明

## 1. 文档目标

这份文档专门解释：

为什么 `dimens-manager/references/team/overview.md` 是系统建设类 Skill 和多维表格 Skill 的上游入口，以及为什么项目真正的创建与初始化主链要继续路由到 `dimens-manager/references/project/overview.md`。

用户表面上常常是在问：

- 我怎么创建项目
- 我怎么进入表格
- 我为什么在项目里能看到这些菜单

但这些问题本质上都离不开 `teamId -> projectId -> 项目资源入口` 这条主线。

---

## 2. 默认主线

在维表智联里，默认应按下面顺序理解业务入口：

1. 先进入团队
2. 再进入项目
3. 再由 `dimens-manager/references/project/overview.md` 承接项目创建 / 初始化
4. 再从项目进入表、文档、报表、微模块等资源

因此当用户说“帮我搭一个系统”时，默认应该先确认：

- 系统建在哪个团队下
- 项目是否已经存在
- 项目里要挂哪些资源入口

---

## 3. 项目为什么是系统建设的上游入口

### 3.1 项目是业务容器

对于大多数系统建设任务，项目承担的是业务容器角色：

- 归属哪个团队
- 下面有哪些表 / 文档 / 报表 / 微模块
- 菜单里对外暴露哪些入口

### 3.2 表格能力默认从项目进入

例如多维表相关接口：

- `sheet list`
- `sheet tree`
- `sheet create`

本质上都先依赖 `projectId`。

所以当用户说“我要搭一个客户管理系统”，默认主线应该是：

1. 先建项目
2. 先补项目初始化步骤和默认公开视图
3. 再在项目里建表
4. 再设计字段、示例数据和查询案例

### 3.3 项目菜单决定用户先看到什么

项目详情里通常会携带菜单配置，这决定：

- 首页导航显示哪些资源
- 用户先进入哪张表、哪份文档、哪个报表
- 系统搭出来之后，看起来是不是一个完整的业务入口

---

## 4. 真实项目入口案例

结合当前实测项目 `PUQUNFE`，项目菜单配置可体现为：

```json
{
  "config": {
    "appearance": {
      "topMenu": {
        "items": [
          {
            "id": "sh_ja2IwgaBhV1jUWB4",
            "title": "数据管理",
            "type": "sheet",
            "targetId": "sh_ja2IwgaBhV1jUWB4"
          },
          {
            "id": "sh_Zp60Au58FrE9FhVi",
            "title": "工作表 2",
            "type": "sheet",
            "targetId": "sh_Zp60Au58FrE9FhVi"
          }
        ]
      }
    }
  }
}
```

这个案例说明了两件事：

1. 项目不是抽象配置，而是真正承接资源入口的容器。
2. 后续 `dimens-manager/references/table/overview.md` 在解释“为什么能看到这张表”时，也要回到项目入口看。

---

## 5. 系统建设时的默认输出建议

当用户说“帮我搭一个系统”时，涉及 `dimens-manager/references/team/overview.md` 的默认输出建议至少包括：

1. 这个系统归属于哪个团队
2. 项目名称是什么
3. 这个项目里需要哪些主入口
4. 哪些入口是表，哪些是文档，哪些是报表
5. 后续表格、文档、工作流能力分别从哪个项目入口继续落下去

不要一上来直接掉进字段、权限或工作流，而忽略“项目入口”这层容器。

---

## 6. 与其他 Skill 的关系

### 6.1 与 `dimens-system-orchestrator`

总控 Skill 在做系统拆解时，应先把项目作为默认容器，再把表、字段、查询案例往下展开。

### 6.2 与 `dimens-manager/references/table/overview.md`

`dimens-manager/references/table/overview.md` 负责项目里的表、字段、行；但它默认已经建立在项目入口清楚的前提下。

### 6.2.1 与 `dimens-manager/references/project/overview.md`

`dimens-manager/references/team/overview.md` 负责给出 `teamId / projectId` 的上下文边界；一旦用户进入“创建项目、初始化项目、准备建表”的执行阶段，应该继续把主链交给 `dimens-manager/references/project/overview.md`，而不是停留在团队上下文说明层。

### 6.3 与 `dimens-manager/references/permission/overview.md`

只有当项目入口和资源归属清楚后，再谈谁能看到项目、谁能看到项目内资源，逻辑才稳定。

---

## 7. 与其他 references 的关系

建议按下面顺序组合使用：

1. 先看 `context-sources.md`，确认当前到底进的是哪个团队 / 项目。
2. 再看本文件，确认项目为什么是系统建设和表格能力的默认入口。
3. 如果要真正创建项目并推进到建表链路，继续进入 `dimens-manager/references/project/overview.md` 技能目录，并查看其中的 `references/bootstrap-flow.md`。
4. 最后看 `examples.md`，确认项目接口、菜单案例和 CLI 命令的真实结构。
