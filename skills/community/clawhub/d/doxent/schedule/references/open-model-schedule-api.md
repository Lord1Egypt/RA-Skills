# open-model-schedule API

## 必读约束

- 端口、默认入口和 health 检查规则统一见 `../shared/port-and-health.md`
- 写操作与 `/open-model/sync` 规则统一见 `../shared/write-and-sync.md`
- 文本请求体的编码约束统一见 `../shared/encoding-rules.md`

---

## 快速决策

| 用户意图 | 接口 |
| --- | --- |
| 「确认 schedule 能不能用」 | `GET /open-model-schedule/health` |
| 「看今天/某几天的日程和任务」 | `GET /open-model-schedule/overview` |
| 「读取某个事件或任务详情」 | `GET /open-model-schedule/item` |
| 「新建事件」 | `POST /open-model-schedule/create` |
| 「新建任务」 | `POST /open-model-schedule/create` |
| 「更新事件或任务」 | `POST /open-model-schedule/update` |
| 「删除事件或任务」 | `POST /open-model-schedule/delete` |
| 「完成任务 / 取消完成 / 移动任务」 | `POST /open-model-schedule/operate` |
| 「写后补同步」 | `POST /open-model/sync` |

---

## 通用返回

### 成功

```json
{
  "code": 200,
  "msg": "成功",
  "data": {}
}
```

### 失败

```json
{
  "code": 500,
  "msg": "错误信息"
}
```

---

## 数据结构

### OpenModelScheduleEventItem

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | number | 事件 id |
| `uuid` | string | 事件 uuid |
| `title` | string | 标题 |
| `summary` | string | 摘要 |
| `startTime` | number | 开始时间 |
| `endTime` | number | 结束时间 |
| `startDay` | number | 开始日期 |
| `endDay` | number | 结束日期 |
| `remindTime` | number | 绝对提醒时间 |
| `advanceTime` | number | 相对开始时间的提前量 |

### OpenModelScheduleTaskItem

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 任务 id |
| `title` | string | 任务标题 |
| `localId` | string | 所属目录 id |
| `doneFlag` | number | 完成状态 |
| `expireTime` | number | 截止时间 |

---

## 接口详情

### 1. 健康检查

GET `/open-model-schedule/health`

**触发场景**：用户要先确认本地 schedule 能力是否可用。

#### 请求参数

无

#### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `enabled` | boolean | 是否启用 |
| `status` | string | 服务状态 |
| `service` | string | 服务名，通常为 `open-model-schedule` |
| `capabilityDetails` | array | 当前能力清单 |
| `message` | string | 未启用时的提示信息 |
| `configPath` | string | 配置文件路径 |

#### 返回示例

```json
{
  "code": 200,
  "msg": "成功",
  "data": {
    "enabled": true,
    "status": "ok",
    "service": "open-model-schedule",
    "capabilityDetails": [
      { "path": "/open-model-schedule/health", "description": "检查开放日程接口健康状态" },
      { "path": "/open-model-schedule/overview", "description": "获取单日或时间范围内的日程与任务概览" },
      { "path": "/open-model-schedule/item", "description": "获取单个日程或任务详情" },
      { "path": "/open-model-schedule/create", "description": "创建日程或任务" },
      { "path": "/open-model-schedule/update", "description": "更新日程或任务" },
      { "path": "/open-model-schedule/delete", "description": "删除日程或任务" },
      { "path": "/open-model-schedule/operate", "description": "执行任务完成、取消完成或移动操作" }
    ]
  }
}
```

---

### 2. 概览查询

GET `/open-model-schedule/overview`

**触发场景**：用户要查看某一天或某个时间范围内的事件和任务。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `day` | string | 否 | 单天查询，格式如 `2026-04-24` |
| `startDay` | string | 否 | 范围查询开始日期 |
| `endDay` | string | 否 | 范围查询结束日期 |

#### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `scope` | string | `day` 或 `range` |
| `day` | string | 单天查询时返回 |
| `startDay` | string | 范围查询时返回 |
| `endDay` | string | 范围查询时返回 |
| `events` | `OpenModelScheduleEventItem[]` | 事件列表 |
| `tasks` | `OpenModelScheduleTaskItem[]` | 任务列表 |

#### 说明

- 支持单天查询和范围查询两种形态。
- 日期范围无效时会返回错误，例如开始时间晚于结束时间。

单天查询示例：

```http
GET /open-model-schedule/overview?day=2026-04-24
```

范围查询示例：

```http
GET /open-model-schedule/overview?startDay=2026-04-24&endDay=2026-04-30
```

---

### 3. 单条详情

GET `/open-model-schedule/item`

**触发场景**：用户已经定位到某个事件或任务，要进一步读取详情。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `type` | string | 是 | `event` 或 `task` |
| `id` | string | 条件必填 | 任务详情必填；事件详情可与 `uuid` 二选一 |
| `uuid` | string | 条件必填 | 仅事件详情可用；与 `id` 二选一 |

#### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `type` | string | `event` 或 `task` |
| `item` | object | 对应类型的详情对象 |

查询事件示例：

```http
GET /open-model-schedule/item?type=event&uuid=event-301
```

查询任务示例：

```http
GET /open-model-schedule/item?type=task&id=task-301
```

---

### 4. 创建

POST `/open-model-schedule/create`

**触发场景**：用户要新建事件或任务。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `type` | string | 是 | `event` 或 `task` |

事件：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | 条件必填 | 与 `summary` 二选一，至少传一个；默认 `""` |
| `summary` | string | 条件必填 | 与 `title` 二选一，至少传一个；默认取 `title`，否则 `""` |
| `startTime` | number/string | 是 | 可解析开始时间 |
| `endTime` | number/string | 是 | 可解析结束时间 |
| `remindTime` | number/string | 否 | 绝对提醒时间；默认不传 |

任务：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | 是 | 任务标题 |
| `expireTime` | number/string | 否 | 截止时间；默认不传 |
| `localId` | string | 否 | 任务清单 id；默认 `"0"` |

#### 复杂操作补充参数

仅在复杂创建场景传这些字段。

事件：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `startTimeStr` | string | 开始时间字符串 |
| `endTimeStr` | string | 结束时间字符串 |
| `advanceTime` | number/string | 相对开始时间的提前量 |
| `repeatDays` | string | 重复星期配置 |
| `repeatStartTime` | number/string | 重复开始时间 |
| `repeatEndTime` | number/string | 重复结束时间 |
| `startDay` | number/string | 开始日期 |
| `endDay` | number/string | 结束日期 |
| `hasScheduleTime` | boolean/string/number | 是否有明确时间 |
| `configTime` | boolean/string/number | 时间是否已配置 |
| `sn` | string | 来源标识 |
| `allDayAdvTime` | number/string | 全天提醒提前量 |
| `desc` | string | 描述 |
| `extInfo` | string | 扩展信息 |

任务：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 任务 id |
| `doneFlag` | number/string | 完成状态 |
| `fromNote` | number/string | 是否来自笔记 |
| `extInfo` | string | 扩展信息 |
| `advanceTime` | number/string | 提前量 |
| `allDayAdvTime` | number/string | 全天提醒提前量 |
| `hasScheduleTime` | boolean/string/number | 是否有明确时间 |
| `configTime` | boolean/string/number | 时间是否已配置 |

任务截止时间规则：

- 用户表达“截止到 / 截止时间 / deadline / 周五前 / 今晚前”等任务期限时，必须通过 `expireTime` 传截止时间。
- 截止时间可以传毫秒时间戳、秒级时间戳、`YYYY-MM-DD HH:mm:ss`、`YYYY-MM-DD HH:mm`、ISO 时间或 `YYYYMMDDHHmmss` 等可解析字符串。
- `expireTime` 含具体时分时会自动按非全天任务处理；仅日期型截止时间按全天任务处理。
- `expireTime` 含具体时分且未显式传提醒配置时，默认提前 5 分钟提醒。
- 任务提醒时间通过 `advanceTime` 表达提前毫秒数；非 `-1` 的 `advanceTime` 会打开提醒，`advanceTime: -1` 表示不提醒。

#### 提醒时间规则

| 规则 | 说明 |
| --- | --- |
| 同时给 `remindTime` 和 `advanceTime` | 以 `remindTime` 为准 |
| 内部处理 | 会根据 `startTime - remindTime` 反推 `advanceTime` |

创建事件示例：

```json
{
  "type": "event",
  "title": "项目例会",
  "summary": "讨论排期",
  "startTime": 1770002400000,
  "endTime": 1770006000000,
  "remindTime": 1770001500000
}
```

创建任务示例：

```json
{
  "type": "task",
  "title": "写周报",
  "localId": "0",
  "expireTime": 1770020000000
}
```

---

### 5. 更新

POST `/open-model-schedule/update`

**触发场景**：用户要修改事件或任务。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `type` | string | 是 | `event` 或 `task` |

事件：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | number/string | 条件必填 | 与 `uuid` 二选一，至少传一个 |
| `uuid` | string | 条件必填 | 与 `id` 二选一，至少传一个 |
| `title` | string | 否 | 不传则保留原值 |
| `summary` | string | 否 | 不传则保留原值 |
| `startTime` | number/string | 否 | 不传则保留原值 |
| `endTime` | number/string | 否 | 不传则保留原值 |
| `remindTime` | number/string | 否 | 不传则保留原值 |

任务：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | 是 | 任务 id |
| `title` | string | 否 | 不传则保留原值 |
| `expireTime` | number/string | 否 | 不传则保留原值 |
| `localId` | string | 否 | 不传则保留原值 |

#### 复杂操作补充参数

仅在复杂更新场景传这些字段；未传字段保留原值。

事件：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `startTimeStr` | string | 开始时间字符串 |
| `endTimeStr` | string | 结束时间字符串 |
| `advanceTime` | number/string | 相对开始时间的提前量 |
| `repeatDays` | string | 重复星期配置 |
| `repeatStartTime` | number/string | 重复开始时间 |
| `repeatEndTime` | number/string | 重复结束时间 |
| `startDay` | number/string | 开始日期 |
| `endDay` | number/string | 结束日期 |
| `hasScheduleTime` | boolean/string/number | 是否有明确时间 |
| `configTime` | boolean/string/number | 时间是否已配置 |
| `sn` | string | 来源标识 |
| `allDayAdvTime` | number/string | 全天提醒提前量 |
| `desc` | string | 描述 |
| `extInfo` | string | 扩展信息 |

任务：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `doneFlag` | number/string | 完成状态 |
| `fromNote` | number/string | 是否来自笔记 |
| `extInfo` | string | 扩展信息 |
| `advanceTime` | number/string | 提前量 |
| `allDayAdvTime` | number/string | 全天提醒提前量 |
| `hasScheduleTime` | boolean/string/number | 是否有明确时间 |
| `configTime` | boolean/string/number | 时间是否已配置 |

#### 说明

- 该接口按 patch 语义工作：未传字段保留原值。
- 更新任务提醒时传 `advanceTime` 即可；非 `-1` 的 `advanceTime` 会打开提醒，`advanceTime: -1` 表示不提醒。
- 如果底层更新返回字符串错误，接口会直接透出错误信息。

更新事件示例：

```json
{
  "type": "event",
  "uuid": "event-601",
  "title": "已更新日程",
  "remindTime": 1770001500000
}
```

更新任务示例：

```json
{
  "type": "task",
  "id": "task-601",
  "title": "已更新任务"
}
```

---

### 6. 删除

POST `/open-model-schedule/delete`

**触发场景**：用户明确确认后删除事件或任务。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `type` | string | 是 | `event` 或 `task` |

事件：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | number/string | 条件必填 | 与 `uuid` 二选一，至少传一个 |
| `uuid` | string | 条件必填 | 与 `id` 二选一，至少传一个 |

任务：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | 是 | 任务 id |

#### 说明

- 这是直接修改真实数据的风险动作，建议先通过 `overview` 或 `item` 确认对象。

删除事件示例：

```json
{
  "type": "event",
  "id": 501,
  "uuid": "event-501"
}
```

删除任务示例：

```json
{
  "type": "task",
  "id": "task-501"
}
```

---

### 7. 任务操作

POST `/open-model-schedule/operate`

**触发场景**：用户要完成任务、取消完成，或把任务移动到其他目录。

#### 请求参数

任务：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `action` | string | 是 | `complete` / `uncomplete` / `move` |
| `id` | string | 是 | 任务 id |
| `localId` | string | 条件必填 | `move` 时必填 |

#### 说明

- 该接口只作用于任务。
- 当前不需要传 `type`。

| 动作 | 示例 |
| --- | --- |
| 完成任务 | `{ "action": "complete", "id": "task-401" }` |
| 取消完成 | `{ "action": "uncomplete", "id": "task-402" }` |
| 移动任务 | `{ "action": "move", "id": "task-403", "localId": "dir-2" }` |

---

### 8. 写后同步

POST `/open-model/sync`

**触发场景**：`create`、`update`、`delete`、`operate` 成功后补调同步。

#### 请求参数

无

#### 说明

- 这是“写后补同步”接口，不替代具体业务写接口。
- 如果当前动作只是读取，不要额外调用它。
- 返回成功只表示“已触发同步流程”，不代表远端已经完成最终可见。
