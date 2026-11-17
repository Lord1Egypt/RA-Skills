# CRUD 规范

规则 ID 前缀 `C-xx`，元数据四要素：`来源|状态|版本|违反后果`。
排障条目见 references/pitfalls.md。

## §1 分页与骨架

```json
{
  "type": "crud",
  "id": "xxxCrud",
  "name": "xxxCrud",
  "syncLocation": false,
  "defaultParams": { "perPage": 50, "page": 1 },
  "perPageAvailable": [20, 50, 100, 150],
  "footerToolbar": [
    "switch-per-page",
    { "type": "tpl", "tpl": "Total ${total} records, Page ${page}" },
    "pagination"
  ]
}
```

- **`C-01`** `perPageAvailable` 必须放 crud **顶层**，不能放 footerToolbar 内组件里
  `来源:V-18实测(2026-09-07)+rest.js renderSwitchPerPage|状态:已实测|版本:6.13.0|后果:切换器照常出现，但自定义项被忽略、回退默认 [5,10,20,50,100]（原「切换器不出现」不成立）；另须包含当前 perPage，否则显示空值`
- 注：`perPageAvailable` 须包含 `defaultParams.perPage`（缺省 10）；实测配 `[7,13,29]` 而 perPage=10 时切换器显示「请选择」空值
- **`C-02`** **被外部定位 / 刷新的** crud 同时设 `id` 和 `name`；无需被定位的 crud（如弹层内选择器）不必设
  `来源:V-18实测(2026-09-07)|状态:已实测|版本:6.13.0|后果:缺 id 则 componentId 定位失效（实测零请求）；缺 name 不影响 target / 顶层 reload`
  - 实测矩阵（3 crud × 3 载体，判据=新增请求数）：`componentId` **只认 id**（填 name 恒失效，即使该 crud 已同时设 id）；`target` 与按钮顶层 `reload` **认 id 也认 name**（仅设 id 的 crud 用 id 定位同样生效）
  - 原「id 供 componentId、name 供 target/reload」的分工不准确：`name` 非 target/reload 的必要条件，同时设只为覆盖全部定位方式
- **`C-03`** `syncLocation: false`，避免分页参数污染 URL
  `来源:V-18实测(2026-09-07)+crud源码(2026-09-02)|状态:已实测|版本:6.13.0|后果:加载即写入 ?page=1、翻页写入 ?page=N&perPage=M；带参 URL 打开会按 URL 参数请求（实测 ?page=3 → 请求 page=3），刷新/分享链接停留在历史分页（crud defaultProps 默认 syncLocation:!0，必须显式关）`
- `defaultParams.perPage` 设默认每页条数；footerToolbar 内 `switch-per-page` 用字符串简写

## §2 统计条

- **`C-04`** footerToolbar 统计条用 `tpl`（如 `"Total ${total} records, Page ${page}"`），不用 `statistics`
  `来源:实战观察+V-13-C实测(2026-09-03)|状态:已实测|版本:6.13.0|后果:total<=perPage 单页时 statistics 整个节点不渲染（实测 total=5 / perPage=10 时 DOM 中无该节点；total=171 时正常渲染「1/18 共：171 项」；同组 tpl 在单页下正常渲染）、textContent 属性无效`

## §3 api 分页参数映射

```json
{
  "api": {
    "method": "post",
    "url": "/XXX/XXXX/page",
    "data": { "current": "${page}", "size": "${perPage}" }
  }
}
```

- **`C-05`** 后端分页字段非 page/perPage 时必须在 api.data 显式映射（crud 数据域自动提供 `${page}`/`${perPage}`/filter 字段）
  `来源:V-18实测(2026-09-07)|状态:已实测|版本:6.13.0|后果:分页失效——且**一旦 api.data 非空，amis 不再自动附加 page/perPage**，故 page 与 perPage 必须都映射`
  - 实测（GET 与 POST 同构）：只映射 `current` 则 `perPage` 丢失；`api.data` 只写无关字段 `foo=bar` 时 `page`/`perPage` **全部丢失**（翻页仍只发 `foo=bar`）
  - 等价替代：crud 上写 `pageField` / `perPageField`（实测 `pageField:current` + `perPageField:size` → 请求 `current=1&size=10`，无需写 api.data）
- 响应结构非 amis 标准（要求 `{items, total}`）时必须加 adaptor → references/data-source.md §2（`A-02`）

## §4 headerToolbar 标准布局

```json
["reload", "filter-toggler", { "type": "button", "label": "Import", "actionType": "dialog", "dialog": {} }]
```

- **`C-06`** 用 `filter-toggler` 需 crud 设 `"filterTogglable": true`；`columns-toggler`/`drag-toggler` 直接使用无需配置
  `来源:V-18实测(2026-09-07)+官方文档(amis 6.13.0)|状态:已实测|版本:6.13.0|后果:开关按钮不显示（实测未设时 headerToolbar 中该按钮 DOM 不存在）；已设时可双向开合，筛选栏默认展开`
  注：`columnsToggled` 属性不存在（v1.1 已修正误记）

## §5 状态列 mapping

```json
{
  "name": "status", "label": "Status", "type": "mapping",
  "map": {
    "Enabled": "<span class='label label-success'>Enabled</span>",
    "Disabled": "<span class='label label-danger'>Disabled</span>",
    "*": "<span class='label label-default'>(blank)</span>"
  }
}
```

- **`C-07`** mapping 必须写 `*` 兜底 key
  `来源:V-18实测(2026-09-07)|状态:已实测|版本:6.13.0|后果:未命中值显示表格空值占位「-」（实测无 `*` 组未命中单元格为 `-`，有 `*` 组为兜底文案）；数字值可匹配字符串 key（实测 id=1/2 命中 "1"/"2"）`

## §6 operation 操作列

```json
{
  "type": "operation", "label": "Action", "fixed": "right", "width": 220,
  "buttons": [ { "type": "button-group", "buttons": [ { "按钮1": "..." }, { "按钮2": "..." } ] } ]
}
```

- **`C-08`** 操作列 `fixed: "right"` + `width` 固定；行内多按钮用 button-group 收拢
  `来源:实战观察|状态:实战观察|版本:6.x|后果:平铺按钮撑爆列宽`
- 行数据字段经数据域直接取（如弹层 title 写 `"Edit - ${code}"`）；弹层 form 传 id 用 hidden → references/form-controls.md §4（`F-08`）

## §7 filter 顶部搜索表单

filter 字段自动进入 crud 数据域，api.data 用 `${字段名}` 引用；actions 放 Reset + Submit 按钮。完整写法见 examples/INDEX.md（crud-base.json + 弹层片段组合）。

## §8 loadDataOnce

小数据量（全量字典/配置类列表）用 `"loadDataOnce": true`：首次请求拉全量，后续分页/排序在前端完成。弹层内嵌选择器常用 → examples/bulk-actions-picker.json（`D-10`）。

## §9 刷新机制（权威定义在弹层域 D-03/D-05/D-11/D-12）

载体与写法对照表见 references/dialog-actions.md §3（唯一权威表）。要点：
事件动作用 `componentId`（`D-03`）；按钮级刷新按按钮类型分两形态（`D-12`）；
弹层 form api 的 `reload` 仅 close 缺省生效（`D-11`），`close:false` 下不生效（`D-05`）。
