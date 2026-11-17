# 生成配置自检清单

生成 amis 配置后、交付前逐条自检。本清单只引规则 ID，权威写法见 ID 指向处（META.md / references/ 各域文件）。P-xx 为事后排障索引（pitfalls.md），不在此列。

## 1. 通用（每次必查）

- [ ] 生成的 JSON 内无 `//` 或 `/* */` 注释？→ `R-01`
- [ ] 非 amis 标准响应（业务码 `code`）已用 `adaptor` 转成 `status`（否则后端失败被当成功），且拼写统一为 `adaptor`？→ `A-02`
- [ ] loading 等状态变量声明在外层 Service 的 `data`，而非依赖 crud 内 `setValue` 向外传播？→ `A-01`

## 2. CRUD / 列表页

- [ ] `perPageAvailable` 放 crud 顶层（不在 footerToolbar 组件内），且包含当前 perPage？→ `C-01`
- [ ] 被外部定位 / 刷新的 crud 同时设了 `id` 和 `name`？→ `C-02`
- [ ] `syncLocation: false` 已设？→ `C-03`
- [ ] footerToolbar 统计条用 `tpl`，未用 `statistics`？→ `C-04`
- [ ] 后端分页字段非 page/perPage 时，api.data **同时**映射 `${page}` 与 `${perPage}`（只映射一个另一个会丢），或改用 `pageField`/`perPageField`？→ `C-05`
- [ ] 用 `filter-toggler` 时 crud 已设 `filterTogglable: true`？→ `C-06`
- [ ] mapping 写了 `*` 兜底 key？→ `C-07`
- [ ] 操作列 `fixed: "right"` + `width` 固定，行内多按钮收进 `button-group`？→ `C-08`

## 3. 弹层与动作（新增/编辑/删除/导入/确认/选择器）

- [ ] 提交按钮 `close: false` + `submitSucc` 内手动 `closeDialog`？→ `D-01`
- [ ] 弹层提交按钮**未配** `loadingOn`（submit 有内建 loading）？→ `D-04`
- [ ] `close: false` 下 form api 内**未写** `reload`，刷新靠 `submitSucc` 显式 `componentId` reload？→ `D-05`
- [ ] form 未配 `onEvent.submit`？→ `D-06`
- [ ] 确认操作用 `actionType: "dialog"` 自定义弹层（`close:false` + `submitSucc` 内 `closeDialog`），未用 `confirmText`（失败时弹层照关）？→ `D-01` / `D-07`
- [ ] 事件动作（onEvent.actions）内 reload 用 `componentId`（此处 target 失效）？→ `D-03`
- [ ] 按钮级 reload：刷新专用按钮（actionType:reload）用 `target`、业务按钮（ajax 等）用顶层 `reload` 属性（值均为 name）？→ `D-12`
- [ ] 弹层内选择数据用 crud + `bulkActions`，**取选中值的提交按钮写在 crud 内**（headerToolbar，否则 `selectedItems` 读不到），空选 `disabledOn` 禁用；需跨页保留选中时加了 `keepItemSelectionOnPageChange: true` 且 `syncLocation: false`？→ `D-10`

## 4. 下载 / 导出（loading 要求与弹层提交相反）

- [ ] 文件下载/导出用 `actionType: "download"`，未用 ajax+blob、裸 `fetch()`？→ `D-02`
- [ ] 后续动作写进 `onEvent.click.actions` 数组，未用动作的 `then` 字段（6.13.0 恒不触发）？→ `D-02`
- [ ] download 按钮配了 `loadingOn` + 外层 Service 变量 + `setValue true/false` 配对（download 无内建 loading）？→ `D-08`
- [ ] `setValue` 的 `componentId` 指向外层 Service（loading 变量声明在其 `data`）？→ `D-09`

## 5. 表单控件

- [ ] 多选 select 设了 `multiple`，且 `joinValues` 未被显式设为 false？→ `F-01`
- [ ] 必填字段配了 `required: true`（无需双写 `validations.isRequired`）？→ `F-02`
- [ ] `autoComplete` 是对象或字符串 URL（`sendOn` 只在对象形态内写），不是 `true` + 外部 source？→ `F-03`
- [ ] `sendOn` 在 autoComplete 对象内，未放进 source；已配 autoComplete 时未再另写一份 source（source 不发请求）？→ `F-04`
- [ ] 上传 input-file 设了 `asBlob: true`（文件才随表单提交；否则选中即上传到 receiver）？→ `F-05`
- [ ] 单列表单宽度用 `inputClassName`（`w-sm`/`w-lg`/`w-xl`）或 `style.width`；`columnRatio` 只在 `group` 内用；未用 `size` 控宽度？→ `F-06`
- [ ] autoComplete 联想响应 data 是数组或 `{options:[...]}`，非 CRUD 式 `{rows,items}`？→ `F-07`
- [ ] 编辑弹层只读展示用 `static`（name 与行字段同名即可自动取值，不必写 `value`）、提交主键用 `hidden`（不写则提交体无 id）？→ `F-08`
- [ ] 联想下拉后端响应是否返回标准 `label`/`value` 字段（协作约束，前端不可独立完成，否则用降级方案）？→ `F-09`
- [ ] 未使用 adapter 字符串转换（6.13.0 不可用，报 invalid label）？→ `F-10`

## 6. 刷新定位

- [ ] 弹层默认关闭模式（close 缺省）下 form api 的 `reload`（值 name）生效？→ `D-11`（close:false 下不生效，见 `D-05`）
- [ ] 被 reload 的目标 crud 同时设了 `id` 和 `name`？→ `C-02`
