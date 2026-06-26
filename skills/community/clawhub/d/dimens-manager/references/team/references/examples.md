# dimens-manager 团队上下文章节 接口案例

本文档聚焦团队与项目上下文相关的真实接口案例。由于当前 `dimens-cli` 主要封装的是 `project` 域，团队侧更多是通过 `teamId` 作为上下文进入，所以示例重点放在：

1. 团队上下文如何进入项目接口
2. 项目列表 / 项目详情的真实入参与出参
3. CLI 默认上下文如何影响结果

更细的规则说明请分别查看：

- `context-sources.md`
- `project-entry.md`
- `isolation.md`

---

## 1. 设置默认团队

### CLI 命令

```bash
dimens-cli auth use-team TTFFEN
```

入参：

| 参数位置 | 必填 | 说明 |
| --- | --- | --- |
| `<teamId>` | 是 | 团队 ID |

成功输出：

```json
{
  "success": true,
  "message": "默认团队已更新",
  "data": {
    "teamId": "TTFFEN"
  }
}
```

作用：

- 写入本地 profile 的默认 `teamId`
- 后续部分命令可以省略 `--team-id`

---

## 2. 查询团队下的项目列表

### 2.1 服务端接口

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/org/:teamId/project/page` |
| 入口角色 | 团队项目分页入口 |
| 鉴权 | `Authorization: Bearer {token}` |

请求体：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `page` | `number` | 否 | 页码，CLI 默认 `1` |
| `size` | `number` | 否 | 每页条数，CLI 默认 `20` |
| `keyword` | `string` | 否 | 项目名称关键词 |

请求示例：

```json
{
  "page": 1,
  "size": 20
}
```

返回字段重点：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.list` | `array` | 项目列表 |
| `data.list[].id` | `string` | 项目 ID |
| `data.list[].name` | `string` | 项目名称 |
| `data.list[].teamId` | `string` | 所属团队 |
| `data.list[].visibility` | `string` | `private` / `public_read` |
| `data.list[].publicRoleId` | `string` | 公开项目角色 ID |
| `data.list[].membercount` | `string \| null` | 成员数量 |
| `data.pagination.page` | `number` | 当前页 |
| `data.pagination.size` | `number` | 每页大小 |
| `data.pagination.total` | `number` | 总数 |

### 2.2 CLI 命令

```bash
dimens-cli project list --team-id TTFFEN --output json
```

CLI 入参：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--team-id` | 是，若 profile 无默认值 | 团队 ID |
| `--page` | 否 | 页码，默认 `1` |
| `--size` | 否 | 每页条数，默认 `20` |
| `--keyword` | 否 | 搜索关键词 |
| `--output` | 否 | `json` / `table` / `raw` |

基于本次实测的真实结果：

```json
{
  "success": true,
  "message": "项目列表获取成功",
  "data": {
    "list": [
      {
        "id": "PUQUNFE",
        "name": "xcv",
        "teamId": "TTFFEN",
        "visibility": "public_read",
        "publicRoleId": "role_1Pe28cwWtI0XO4"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 22
    }
  }
}
```

---

## 3. 查询项目详情

### 3.1 服务端接口

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/org/:teamId/project/info?id=:projectId` |
| 入口角色 | 团队项目详情入口 |
| 鉴权 | `Authorization: Bearer {token}` |

查询参数：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | `string` | 是 | 项目 ID |

返回字段重点：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.id` | `string` | 项目 ID |
| `data.name` | `string` | 项目名 |
| `data.teamId` | `string` | 所属团队 |
| `data.config` | `object \| null` | 项目配置，包含菜单、品牌、外观等 |
| `data.visibility` | `string` | 可见性 |
| `data.publicRoleId` | `string` | 公开项目角色 ID |

### 3.2 CLI 命令

```bash
dimens-cli project info --team-id TTFFEN --id PUQUNFE --output json
```

### 3.3 菜单配置案例

本次实测项目 `PUQUNFE` 返回的菜单配置位于：

```json
{
  "config": {
    "appearance": {
      "topMenu": {
        "showManageButton": true,
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

这类项目级菜单配置，是 Skill 解释“项目菜单、项目入口、项目里能看到什么资源”时必须引用的真实案例。

---

## 4. 切换默认项目

### CLI 命令

```bash
dimens-cli auth use-project PUQUNFE
```

入参：

| 参数位置 | 必填 | 说明 |
| --- | --- | --- |
| `<projectId>` | 是 | 项目 ID |

作用：

- 写入本地 profile 默认 `projectId`
- 影响后续 `sheet/column/row/ai` 等命令的默认上下文

---

## 5. Skill 输出要求

当用户问团队、项目、上下文时，Skill 至少要说清这几件事：

1. 当前问题依赖哪个 `teamId`。
2. 项目接口是从哪个团队路径进入的。
3. `project list` 和 `project info` 的必填入参分别是什么。
4. 项目详情里哪些字段可以反映菜单、可见性和公开角色。
5. profile 默认值、显式参数、环境变量会共同影响结果，不能只看一条命令表面参数。

## 6. 这份文档的职责边界

这份文档只负责接口级案例总览，不再展开：

- 上下文来源优先级
- 系统建设时为什么要先从项目入口进入
- 团队级 / 项目级隔离与角色判断细则

这些内容已经拆到独立 references 中，方便后续 Skill 精确引用。
