# dimens-manager 报表章节 能力状态说明

## 1. 文档目标

这份文档专门解释：

`dimens-manager/references/report/overview.md` 当前哪些能力只是 server 真实接口，哪些并不是 CLI 已封装能力。

---

## 2. 三种状态口径

| 状态 | 含义 | 输出要求 |
| --- | --- | --- |
| `已封装` | 当前已有 CLI 命令 | 可以直接给命令案例 |
| `server-only` | 当前只有后端接口或服务入口 | 只能给接口案例，不能伪装成 CLI 能力 |
| `部分对齐` | CLI 有上游或下游能力，但不能等同于完整报表能力 | 必须提示边界 |

---

## 3. 当前报表能力状态

### 3.1 已封装

当前 `dimens-cli` 已经具备以下最小报表主链能力：

| 能力 | 当前状态 | 说明 |
| --- | --- | --- |
| 报表主资源管理 | `已封装` | 已支持 `report list`、`report info`、`report create`、`report update`、`report copy`、`report publish`、`report delete`、`report archive`、`report validate`、`report sort`、`report move`；其中 `report create` 走项目菜单 `sheet/create type=report`，返回 `reportId=sheetId` |
| 报表查询 | `已封装` | 已支持 `report query`、`report query-widget`、`report preview`，可按 `widgetIds` 做定向查询，也可单组件试跑和预览数据 |
| 组件管理 | `已封装` | 已支持 `report widget-add`、`report widget-update`、`report widget-delete`、`report widget-batch`、`report widget-sort` |
| 组件结构校验 | `已封装` | CLI 已对 Recharts 组件类型和 `sheet.columns`、`fieldIds`、`recommendedMapping`、`previewMapping`、`dataMapping` 做基础校验 |

如果用户目标是“让 AI 一次生成成功”，不要只盯着“已封装”三个字，还要继续补一句：

- 已封装不等于可以跳过固定预检链
- 默认仍应按 `report create -> report preview -> report widget-add -> report query-widget -> report query` 推进

### 3.2 部分对齐

下面这些能力仍然不能被表述成“报表 CLI 已完整支持”：

| 能力 | 当前状态 | 说明 |
| --- | --- | --- |
| 组件高级管理 | `部分对齐` | 当前已补主操作，但更细粒度的单组件查询、预览联动、复杂布局协同仍未完全 CLI 化 |
| 报表生命周期高级能力 | `部分对齐` | 主资源生命周期已基本 CLI 化，但更复杂的跨项目联动、副作用校验和批量运维动作仍未完全封装 |
| 查询扩展能力 | `部分对齐` | 单组件查询和数据预览已封装，但更复杂的预览联动、批量调试和可视化诊断仍未 CLI 化 |

### 3.3 server-only

以下能力当前依旧主要停留在服务端接口层：

| 能力 | 当前状态 | 说明 |
| --- | --- | --- |
| 模板与版本管理 | `server-only` | 模板、版本、导出等能力仍以后端接口为主 |

---

## 4. Skill 输出要求

当用户问“报表能不能直接用 CLI 操作”时，建议固定这样回答：

1. 先说明当前能力状态。
2. 对 `已封装` 能力，优先给真实 CLI 命令案例。
3. 对 `部分对齐` 和 `server-only` 能力，明确边界，不要伪装成已有命令。
4. 如果涉及多维表数据源，再补一句需要联动 `dimens-manager/references/table/overview.md` 和权限链路。
5. 如果涉及“直接生成报表”，要明确提醒先走固定预检链，防止 AI 直接跳到 `widget-add`。

---

## 5. 与其他 references 的关系

建议按下面顺序组合使用：

1. 先看 `usage.md`，确认问题属于主资源、组件、查询还是参数与数据源。
2. 再看 `examples.md`，确认真实接口。
3. 最后看本文件，确认当前是不是 CLI 已支持能力。
