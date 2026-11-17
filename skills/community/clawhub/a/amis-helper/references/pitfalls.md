# 踩坑手册（排障索引）

格式：症状 → 错误写法 → 见权威规则 ID。本文不含正确写法，命中即读指向文件。

## 弹层与动作

### P-01 点提交接口不调用，submitSucc 不触发，loading 卡死
- 错误：form 配了 `onEvent.submit`（拦截内置提交）→ 见 references/dialog-actions.md §1（`D-06`）

### P-02 提交后弹框立即关闭，看不到 loading
- 错误：提交按钮缺 `close: false`，未在 `submitSucc` 中 `closeDialog` → 见 references/dialog-actions.md §1（`D-01`）

### P-03 submitSucc 里 reload 了但表格不刷新
- 错误：事件动作内用 `target` 定位（此处失效），或目标 crud 未设 `id`（V-18 实测：`componentId` 只认 id，填 name 恒失效）→ 见 references/dialog-actions.md §3（`D-03`）、references/crud.md §1（`C-02`）

### P-04 close:false 弹层提交后表格不刷新
- 实测（V-2，2026-08-31）：`close: false` 下 form api 的 `reload` 不生效，提交也不默认刷新 CRUD，唯一写法见 references/dialog-actions.md §1（`D-05`）

### P-05 headerToolbar 按钮 loadingOn 读不到变量
- 错误：loading 变量依赖 crud 内 `setValue`（变量不向外传播）→ 见 references/dialog-actions.md §4（`D-09`）、references/data-source.md §5（`A-01`）

### P-06 blob 导出拿不到文件 / 后续动作不执行
- 实测（V-16，2026-09-07）：`ajax` + `responseType: "blob"` + `then` → `then` 不触发；且 `then` 恒不触发、与 blob 无关，后续动作须写进 `onEvent.click.actions` 数组 → 见 references/dialog-actions.md §2（`D-02`）

### P-07 custom action 里 fetch() 报 401
- 实测（V-16，2026-09-07）：裸 `fetch()` 绕过 amis fetcher，不携带 auth token → 401 → 见 references/dialog-actions.md §2（`D-02`）

### P-08 弹层提交按钮配 loadingOn 是死配置
- 实测（V-1/V-1-D，2026-08-31）：submit 按钮有内建 loading，`loadingOn` 恒 false 也照常转圈；接口失败时 loading 正常结束、弹层保持打开、可重试 → 见 references/dialog-actions.md §1（`D-04`）

## 表单控件

### P-09 autoComplete 不触发联想
- 实测（V-19，2026-09-08）：三种错法 ① `autoComplete: true` + 外部 `source`；② 只写 `source`（即便加 `searchable`，也只在加载时请求一次，之后纯本地过滤）；③ `autoComplete` 写成布尔以外要靠对象或字符串 URL → 见 references/form-controls.md §3（`F-03`）

### P-10 联想下拉显示 invalid label
- 错误：① adapter 字符串转换（amis 6.13.0 不可用）② 返回字段与 labelField 不匹配 → 见 references/form-controls.md §8（`F-10`）、§7（`F-09`）

### P-11 联想下拉显示 invalid label / 选项错乱
- 错误：autoComplete 的 source 响应 `data` 是 CRUD 式对象（如 `{rows,items}`、`{count,total}`）→ amis 把对象的**值**当选项遍历，显示 `invalid label` 或数字 → 见 references/form-controls.md §3（`F-07`）

### P-12 sendOn 配了但联想请求不发出 / 每敲一个字符就发请求
- 实测（V-19，2026-09-08）：`sendOn` 放在 source 对象内失效（1 字符即发，与不写 sendOn 同构）；另注：已配 autoComplete 时再写一份 source，source 的 url **零请求**；`sendOn` 也管控初始加载请求 → 见 references/form-controls.md §3（`F-04`）

## CRUD/列表

### P-13 每页条数切换器选项不是自定义的 / 显示「请选择」空值
- 实测（V-18，2026-09-07）：切换器恒出现（原「不出现」不成立）。两种错法：① `perPageAvailable` 写进 footerToolbar 组件内 → 被忽略、回退默认 [5,10,20,50,100]；② 列表不含当前 perPage（缺省 10）→ 显示空值 → 见 references/crud.md §1（`C-01`）

### P-14 单页时底部统计条不显示
- 错误：footerToolbar 用 `statistics`（total ≤ perPage 时不渲染，`textContent` 无效）→ 见 references/crud.md §2（`C-04`）

## 通用

### P-15 表单项宽度控制无效
- 实测（V-19，2026-09-08）：`size: "xl"` 确实无效；`columnRatio` 只在 `group` 内生效（form 直接子项下控件仍撑满整行）。有效写法是 `inputClassName`（内置 `w-sm`/`w-lg`/`w-xl` = 150/280/320px）或 `style.width`（内部 input 随之收缩） → 见 references/form-controls.md §6（`F-06`）

### P-16 amis Schema 校验报「JSON 中不允许有注释」
- 错误：配置内含 `//` 或 `/* */` → 见 META.md（`R-01`）

### P-17 隐藏/不可见的必填字段导致提交被拦截
- 实测（V-11 轮次4，2026-09-01）：hidden/visible:false 的 required 字段值空时仍参与校验，提交被拦截图弹「依赖的部分字段没有通过验证」 → 见 references/form-controls.md §2（`F-02`）

### P-18 combo / input-table 行内必填不校验
- 据 amis 官方 issue#9537（未实测）：combo/input-table 行内字段的 required 在整体提交时不触发校验 → 见 references/form-controls.md §2（`F-02`）

## 补充症状

### P-19 地址栏被分页参数污染，分享链接带 page/perPage
- 实测（V-18，2026-09-07）：crud 未设 `syncLocation: false` 时**加载即写 ?page=1**、翻页写 ?page=N&perPage=M；带参 URL 打开会按 URL 参数请求（停在历史分页）→ 见 references/crud.md §1（`C-03`）

### P-20 翻页数据不变 / 后端收不到分页参数
- 实测（V-18，2026-09-07）：后端分页字段非 page/perPage 时 api.data 须显式映射 `${page}` / `${perPage}`；且**一旦 api.data 非空，amis 不再自动附加 page/perPage**（GET/POST 同构）——只映射一个另一个就丢，只写无关字段则分页参数全丢。也可用 crud 的 `pageField`/`perPageField` 替代 → 见 references/crud.md §3（`C-05`）

### P-21 状态列部分行显示「-」占位
- 实测（V-18，2026-09-07）：mapping 缺 `*` 兜底 key，未命中值渲染为表格空值占位「-」（非纯空白）→ 见 references/crud.md §5（`C-07`）

### P-22 多选下拉提交到后端是数组，后端解析失败
- 实测（V-14，2026-09-03）：多选提交值**恒为数组**，配 `joinValues` 也变不成字符串；`joinValues:false` 更糟（元素变 `{label,value}` 对象）。要字符串用 `${field|join:','}` → 见 references/form-controls.md §1（`F-01`）

### P-23 上传 Excel 后端收不到文件
- 实测（V-17，2026-09-07）：真因是**缺 `asBlob: true`**——文件在选中瞬间就被上传到默认 receiver `/api/upload/file`，表单提交体里没有文件（只有上传响应对象）；`dataType: "form-data"` 在 `asBlob` 存在时**可省**（amis 自动转 multipart）→ 见 references/form-controls.md §5（`F-05`）

### P-24 编辑提交后端报缺主键 / 只读字段被误改
- 实测（V-19，2026-09-08）：提交体只含 form 内声明的字段——主键未用 `hidden` 承载则 body 里没有 id（行数据不会自动带上）；只读字段未用 `static` 展示则变成可编辑输入框。另注：**static 的值会随表单提交**（后端需能接收或忽略），且 `static` 的 `value` 非必需（name 与行字段同名即自动取值）→ 见 references/form-controls.md §4（`F-08`）

### P-25 ajax 按钮提交时必填校验不拦截，空值照样发请求
- 实测（V-11 轮次，2026-09-01）：ajax 按钮跳过提交前校验阻断；表单项的实时红字是 onChange 副作用，非提交阻断 → 见 references/form-controls.md §2（`F-02`）

### P-26 行内（columns）读不到外层 Service 的状态变量
- 实测（V-13-B，2026-09-03）：`setValue` 到 Service 后 crud **headerToolbar 可实时读到，columns 行内只能拿到初始快照**；`setValue` 不带 `componentId` 则落在按钮自身域，三处全读不到 → 见 references/data-source.md §5（`A-01`）

### P-27 动作里配了 `then` 但后续动作不执行
- 实测（V-16，2026-09-07）：`then` 作为动作的兄弟字段在 amis 6.13.0 **恒不触发**，与 `responseType` 无关（普通 JSON 的 ajax 对照组同样不触发）；后续动作必须写进 `onEvent.click.actions` 数组顺序执行 → 见 references/dialog-actions.md §2（`D-02`）

### P-28 后端返回业务失败码，前端却当成功（弹层照关 / 提示成功）
- 实测（V-20，2026-09-08）：响应只有 `code:500` 没有 `status` 时，amis 视为成功——`submitSucc` 照触发（实测 `J_SUCC=Y`），只是另外 toast 了 `msg`；用 `adaptor` 把 `code` 转成 `status` 后才正确走失败分支 → 见 references/data-source.md §2（`A-02`）

### P-29 弹层内选择器提交体为空 / 空选也能提交 / 翻页后选中丢失
- 实测（V-20，2026-09-08）：① `selectedItems` 只在 crud 数据域内可见——弹层底部按钮的 `disabledOn: "!${selectedItems.length}"` 不禁用、外层 form api 的 `${selectedItems|pick:id}` 提交成 `{"ids":""}`，提交按钮要放进 crud 的 headerToolbar；② 跨页保留选中须同时配 `keepItemSelectionOnPageChange: true` 与 `syncLocation: false`（`syncLocation` 默认 true 会让保留失效，`loadDataOnce` 无关） → 见 references/dialog-actions.md §5（`D-10`）
