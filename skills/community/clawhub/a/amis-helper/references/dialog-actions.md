# 弹层与动作链

规则 ID 前缀 `D-xx`，元数据四要素：`来源|状态|版本|违反后果`。

## §1 弹层提交标准模式

所有「确认操作」弹层（新增/编辑/删除/导入）统一此结构：

```json
{
  "type": "button", "label": "删除", "level": "danger", "icon": "fa fa-trash",
  "actionType": "dialog",
  "dialog": {
    "title": "确认删除",
    "actions": [
      { "type": "button", "label": "取消", "actionType": "close" },
      { "type": "button", "label": "确认删除", "level": "danger", "actionType": "submit", "close": false }
    ],
    "body": {
      "type": "form",
      "onEvent": {
        "submitSucc": { "actions": [
          { "actionType": "reload", "componentId": "目标crud的id" },
          { "actionType": "closeDialog" }
        ] }
      },
      "api": { "method": "post", "url": "/XXX/XXXX/delete", "data": { "id": "${id}" } },
      "body": [ { "type": "alert", "body": "确认删除该条记录?", "level": "warning" } ]
    }
  }
}
```

- **`D-01`** 提交按钮 `close: false` + `submitSucc` 内手动 `closeDialog`；`submitFail` 不用写（默认保持弹层打开可重试，实测失败分支无需处理）
  `来源:实战观察+V-1-D实测(2026-08-31)|状态:已实测|版本:6.13.0|后果:弹层秒关看不到 loading，接口失败无法重试`
- **`D-04`** 弹层提交按钮**不配 `loadingOn`**、不需要 Service 变量与 `setValue`——submit 按钮有内建 loading（实测 loadingOn 恒 false 照样转圈）
  `来源:V-1/V-1-D实测(2026-08-31)|状态:已实测|版本:6.13.0|后果:死配置，误导读者`
  例外：download 导出按钮**必须**配对 → §2（`D-08`）
- **`D-05`** `close: false` 下 form api 的 `reload` **不生效**、提交也**不默认刷新** CRUD（实测带不带 reload 均无 crud 请求），api 里**不要写 reload**；唯一写法是 `submitSucc` 显式 `{"actionType":"reload","componentId":"..."}`（E 组实证）
  `来源:V-2实测(2026-08-31)|状态:已实测|版本:6.13.0|后果:表格不刷新`
- **`D-06`** 禁止 form `onEvent.submit`——会拦截 `actionType:"submit"` 的内置调用，接口不发出（V-13-A 实测 A 组：配了 `onEvent.submit` 后接口零请求、`submitSucc` 不触发、弹层保持打开；B 组基线接口正常发出且弹层关闭）
  `来源:实战观察+V-13-A实测(2026-09-03)|状态:已实测|版本:6.13.0|后果:接口不调用、submitSucc 不触发、弹层不关闭（点了没反应）`
  注：源码中事件动作须显式 `preventDefault:true` 才阻止默认行为，但 form 的 submit 事件属于例外——以实测为准
- **`D-07`** 确认弹层用 `actionType:"dialog"` 自定义弹框，不用 `confirmText`
  `来源:实战观察+V-20实测(2026-09-08)|状态:已实测|版本:6.13.0|后果:失败分支不可控——接口失败时弹层照样关闭，看不到失败态也无法重试`
  实测（V-20）：
  - `confirmText` **不是浏览器原生 `confirm`**（覆盖 `window.confirm` 后未被调用），弹的是 amis 自有确认框（标题「系统消息」+ 文本 + 取消/确认），确认后请求正常发出
  - 真因是**失败分支不可控**：接口 `status=1` 时 confirmText 弹层**照样关闭**；自定义 dialog（`close:false` + `submitSucc` closeDialog）失败时**保持打开**可重试
  - 附带实证：`close:false` 但 `submitSucc` 里漏写 `closeDialog` → 提交成功后**弹层残留**（`D-01` 的配对要求再次被验证）
- **`D-11`** 弹层默认关闭模式（close 缺省）下 form api 的 `reload`（值为 crud 的 `name`）生效，提交后自动刷新 CRUD；可用 `"reload": "none"` 显式关闭
  `来源:官方文档(crud「增」章节)+V-12实测(2026-09-01)|状态:已实测|版本:6.13.0|后果:close 缺省模式下不写 reload 则不刷新；与 D-05（close:false 下不生效）形成对偶边界`

## §2 下载/导出（唯一正确写法）

```json
{
  "type": "button", "label": "Export", "level": "warning", "icon": "fa fa-download",
  "loadingOn": "${exportDownloading}",
  "onEvent": {
    "click": {
      "actions": [
        { "actionType": "setValue", "componentId": "外层service", "args": { "value": { "exportDownloading": true } } },
        { "actionType": "download", "args": { "api": { "method": "get", "url": "/XXX/XXXX/export", "data": { "code": "${code}" } } } },
        { "actionType": "setValue", "componentId": "外层service", "args": { "value": { "exportDownloading": false } } }
      ]
    }
  }
}
```

- **`D-02`** 文件下载/导出只用 `actionType:"download"`；禁止 `ajax`+`responseType:"blob"` 后靠 `then` 收尾、禁止裸 `fetch()`
  `来源:实战观察+V-16实测(2026-09-07)|状态:已实测|版本:6.13.0|后果:then 不触发（拿不到 blob、文件不落盘）/ fetch 无 token 401`
  实测三点（V-16；lab 配全局 fetcher 注入 `Authorization` 模拟真实项目）：
  - download **携带 auth token**：浏览器侧请求头与服务端日志双侧确认 `Bearer ...` → 200 blob。**前提**：token 由项目配置的全局 `fetcher` 注入，amis SDK 本身不注入——未配全局 fetcher 时 download 同样无 token
  - `then` **恒不触发**，与 `responseType` 无关（对照组：普通 JSON 的 ajax 同样不触发）；后续动作必须写进 `onEvent.click.actions` 数组顺序执行（实测正常走完，**不会** loading 卡死——原「卡死」描述已修正）
  - custom action 内裸 `fetch()` 绕过 amis fetcher → **无 token → 401**（实测）
- **`D-08`** download 按钮**必须** `loadingOn` + 外层 Service 变量 + `setValue true/false` 配对（download 无内建 loading）；实测顺序 action 会**等待下载完成**（waitSeconds=3 → loading 持续 3 秒）
  `来源:V-3实测(2026-08-31)|状态:已实测|版本:6.13.0|后果:点击无反馈，用户重复点击`

## §3 reload 定位方式（三分）

| 载体 | 属性 | 值 | 规则 |
|------|------|------|------|
| 事件动作（`onEvent.actions` 内） | `componentId` | 目标组件 `id` | `D-03`（此处 `target` 失效） |
| 按钮级 - 刷新专用按钮（actionType:reload） | `target` | 目标组件 `name` | `D-12` |
| 按钮级 - 业务按钮（ajax/submit 等） | 顶层 `reload` | 目标组件 `name` | `D-12` |
| form api 配置 | `reload` | 目标组件 `name` | `D-11`（仅 close 缺省生效）/ `D-05`（close:false 不生效） |

- **`D-03`** 事件动作内 reload 必须用 `componentId`（`target` 失效），目标组件必须设 `id`；等价写法 `componentName`（按 name 定位，实测与 `componentId` 同样生效），统一推荐 `componentId`
  `来源:实战观察+amis源码+V-14实测(2026-09-03)|状态:已实测|版本:6.13.0|后果:reload 不生效（实测 target 写法零请求；componentId / componentName 均触发刷新）`
- **`D-12`** 按钮级 reload，按按钮类型分两形态（V-10 实测）:
  - 刷新专用按钮（`actionType:"reload"`）→ **必须用 `target`**（值 name）；写顶层 `reload` 属性（无 target）**不生效**
  - 业务按钮（`actionType:"ajax"`/`"submit"` 等）→ 用顶层 `reload` 属性（值 name），操作完成后刷新；`close` 不影响其生效
  `来源:官方文档(action.md)+V-10实测(2026-09-01)|状态:已实测|版本:6.13.0|后果:reload 不生效`
- 被刷新 crud 同时设 `id` 和 `name` → references/crud.md §1（`C-02`）

## §4 Service 包装层（仅无内建 loading 的按钮需要）

- **`D-09`** loading 变量声明在**外层 Service 的 `data`**，`setValue` 的 `componentId` 指向 Service（机制 → references/data-source.md §5 `A-01`；V-13-B 实测确认 crud headerToolbar 按钮能读到 Service 变量，方案成立）；弹层提交按钮不需要 Service → `D-04`
  `来源:实战观察+V-13-B实测(2026-09-03)|状态:已实测|版本:6.13.0|后果:loadingOn 读不到变量恒 false`

```json
{ "type": "service", "id": "pageStateService", "data": { "exportDownloading": false }, "body": [ { "type": "crud", "id": "xxxCrud", "name": "xxxCrud" } ] }
```

作用域链：按钮 → CRUD → **service** → page。

## §5 弹层内嵌选择器

完整可落地配置 → examples/bulk-actions-picker.json。要点：

- **`D-10`** 选择一批数据回填用 dialog/drawer + crud(`loadDataOnce:true`) + `bulkActions`；取选中值的按钮**必须写在 crud 内**（headerToolbar / bulkActions）：`${selectedItems|pick:字段}` 提取字段数组、`${selectedItems.length}` 显示选中数、`disabledOn: "!${selectedItems.length}"` 未选中禁用；需跨页保留选中时再加 `keepItemSelectionOnPageChange: true` 且 `syncLocation: false`
  `来源:实战观察+V-20实测(2026-09-08)|状态:已实测|版本:6.13.0|后果:提交体为空 / 空选可提交 / 翻页后选中丢失`
  实测（V-20）：
  - **`selectedItems` 只在 crud 数据域内可见**（与 `A-01` 同构）：弹层底部按钮的 `disabledOn` 空选时**不禁用**、外层 form api 的 `${selectedItems|pick:id}` 提交体为 `{"ids":""}`；同一弹层内 tpl 对比 → crud 外层读到空、crud headerToolbar 读到 `len=2`。把提交按钮放进 crud headerToolbar 后 body 正常为 `{"ids":[1,2]}`
  - **跨页保留选中 = `keepItemSelectionOnPageChange: true` 且 `syncLocation: false`**（勾选 2 行 → 翻第 2 页 → 回第 1 页）：

    | 组 | keepItemSelectionOnPageChange | syncLocation | loadDataOnce | 结果 |
    |---|---|---|---|---|
    | D | true | 默认(true) | true | 丢 |
    | H | true | 默认(true) | false | 丢 |
    | F | true | false | true | **保留** |
    | G | true | false | false | **保留** |
    | I | 不写 | false | false | 丢 |

  - **`loadDataOnce` 与选中保留无关**（F vs G、D vs H 双对照）：它只决定是否一次拉全量；原「靠 loadDataOnce 保留选中」的说法不准确
- 长内容侧滑用 `drawer`，普通用 `dialog`
