# 表单控件

规则 ID 前缀 `F-xx`，元数据四要素：`来源|状态|版本|违反后果`。

## §1 字典/枚举下拉（source + adaptor）

```json
{
  "type": "select", "name": "country", "label": "Country",
  "clearable": true, "multiple": true, "searchable": true,
  "labelField": "name", "valueField": "name",
  "source": {
    "method": "get",
    "url": "/XXX/XXXX/dict/list?type=Country",
    "adaptor": "return { status: payload.code === 200 ? 0 : payload.code, data: payload.data };"
  }
}
```

- **`F-01`** 多选 select 的提交值**恒为数组**（6.13.0 实测五种配置无一产生逗号字符串）：
  - **禁止 `joinValues: false`**——数组元素会变成 `{label,value}` 整个选项对象
  - `joinValues: true` / `extractValue` / `delimiter` 对提交值形态**无影响**，非必需（实测五种组合提交值均为 `["a","b"]`）
  - 后端要逗号分隔字符串时，在 api.data 里用 `join` 过滤器：`"codes": "${field|join:','}"`（实测得到 `a,b`）
  `来源:实战观察+V-14实测(2026-09-03)|状态:已实测|版本:6.13.0|后果:joinValues:false 时提交对象数组后端解析失败；误以为配了 joinValues 就能拿到字符串`
- 后端返回 `{code:200,data:[...]}` 非 amis 标准时用 `adaptor` 转 status → references/data-source.md §2（`A-02`）
- 后端已标准时 source 可字符串简写

## §2 必填与校验

- **`F-02`** 必填只写 `required: true`，**勿双写** `validations: {"isRequired": true}`（幂等无增强，双写唯一差异是多一颗红星，无功能价值）
  `来源:官方文档+amis-core源码+V-11实测(2026-09-01)|状态:已实测|版本:6.13.0|后果:冗余配置，误导读者以为 required 不拦截`
  不拦截的已知场景（实测边界）:
    - ajax 按钮提交跳过「提交前校验阻断」，必填为空仍发请求（F-02 起源；input 的 onChange 实时红字是副作用，非提交阻断）
    - 值 0 / false 视为有值放行
    - combo / input-table 行内必填不校验（据 issue#9537，未实测）→ P-18
  仍拦截的边界（实测修正源码推断）:
    - 全空格串 ' ' 被拦截（源码推断「不拦截」，实测相反，疑似 required 链对字符串 trim）
    - hidden / visible:false 字段仍参与校验，值空时误拦截 → P-17
- 邮箱：`"validations": {"isEmail": true}` + `"validateOnChange": true`；远程唯一性：`"validateApi": "/XXX/XXXX/validate?mail=${email}"`；textarea 长度：`"maxLength": 200`

## §3 远程联想 select（autoComplete）

```json
{
  "type": "select", "name": "code", "label": "Item",
  "placeholder": "Search by code or name", "clearable": true,
  "overlayStyle": { "width": "450px" },
  "autoComplete": {
    "method": "get",
    "url": "/XXX/XXXX/search?keyword=${term}",
    "sendOn": "${term != null && term.length >= 3}"
  }
}
```

- **`F-03`** `autoComplete` 只认**对象**与**字符串 URL** 两种形态（`sendOn` 只能在对象形态里写）；`autoComplete: true` 只等价于「可搜索」，配外部 `source` 不触发联想
  `来源:实战观察+V-19实测(2026-09-08)|状态:已实测|版本:6.13.0|后果:联想不触发——只在加载时请求一次，之后输入仅本地过滤`
  实测四组（V-19-A，判据：输入 abc 后服务端是否出现 `term=abc` 请求）：

  | 组 | 配置 | 联想请求 |
  |---|---|---|
  | A | `autoComplete: {method, url}` | ✅ 发 `term=abc` |
  | B | `autoComplete: true` + 外部 `source` | ❌ 有搜索框，只本地过滤 |
  | C | 只写 `source`（补 `searchable: true`） | ❌ 初始加载请求一次，之后本地过滤 |
  | D | `autoComplete: "/api/xxx?term=${term}"` | ✅ 发 `term=abc` |

  - 原「必须是对象」过严：**字符串 URL 与对象等效**（D 组实证）
  - 无 `sendOn` 时页面**加载即发一次 `term=` 空请求**（`F-04` 可拦截）
- **`F-04`** `sendOn` 写在 autoComplete 对象**内**（放 source 内失效）
  `来源:实战观察+V-19实测(2026-09-08)|状态:已实测|版本:6.13.0|后果:请求时机失控——每输入一个字符都发请求`
  实测三组（V-19-B，条件统一为 `${term.length >= 3}`）：

  | 组 | sendOn 位置 | 输入 1 字符 | 输入 3 字符 | 初始加载 |
  |---|---|---|---|---|
  | A | autoComplete 内 | 不发 | 发 | **不发** |
  | B | source 内 | 发 | 发 | 发 |
  | C | 不写（基线） | 发 | 发 | 发 |

  - `sendOn` **同时管控初始加载请求**（A 组连 `term=` 空请求都被拦掉）
  - **autoComplete 与 source 并存时，source 的 url 零请求**（B 组实证）：autoComplete 完全接管数据源，别再写一份 source 指望它兜底
- **`F-07`** autoComplete 的 source 响应，`data` 可以是**直接数组** `[...]` 或**含 `options` 键的对象** `{options:[...]}`，两种都正常渲染（V-15 实测：数组与 `{options}` 各渲染 3 项）
  `来源:实战观察+V-15实测(2026-09-03)|状态:已实测|版本:6.13.0|后果:把 CRUD 式对象（如 {rows,items}/{count,total}）当 data → amis 遍历对象的值当选项，显示 invalid label / 数字`
- `${term}` 是 amis 默认搜索词变量（GET 为 query 参数）；`overlayStyle.width` 控制下拉面板宽度
- 排查链（联想不生效时按序）：请求未发出（sendOn/autoComplete 配置错）→ 404（路由未部署）→ 401（需登录）→ 下拉为空 / 回退显示原始 value（`adaptor` 未生效或误拼成 `adapter` → `F-10`）→ 下拉项显示 invalid label（`labelField` 与返回字段不匹配）→ 选中值不对（valueField 错）

## §4 编辑弹层展示字段

- **`F-08`** 行上下文只读展示用 `static`；提交需要的主键用 `{ "type": "hidden", "name": "id" }`
  `来源:实战观察+V-19实测(2026-09-08)|状态:已实测|版本:6.13.0|后果:提交缺主键 / 可编辑字段被误改`
  实测三组（V-19-D，crud 行编辑弹层，判据：展示文本 + POST 提交体）：

  | 组 | 配置 | 展示 | 提交 body |
  |---|---|---|---|
  | A | `static`(名 `engineStatic` + `value:"${engine}"`) + `hidden id` | Trident - 001 | 含 `engineStatic` 与 `id` |
  | B | `static` **不写 value**（name 与行字段同名 `engine`）+ `hidden id` | Trident - 001 | 含 `engine` 与 `id` |
  | C | 只有 `input-text browser`（无 hidden，对照） | — | **仅 `browser`，无 id** |

  - **`value:"${code}"` 非必需**：name 与行字段同名时自动从数据域取值（B 组），`value` 只在「字段名 ≠ 展示来源」时才写
  - **提交体只含 form 内声明的字段**：不写 `hidden` 就拿不到行数据里的 `id` → `hidden` 必需
  - **static 的值会随表单提交**（A/B 组 body 均含），后端 DTO 需能接收或可忽略

## §5 文件上传（Excel 导入）

```json
{
  "type": "input-file", "name": "file", "label": "Excel File",
  "accept": ".xlsx,.xls", "asBlob": true, "required": true,
  "hint": "Template: code / type / remark", "btnText": "Select File", "reUploadBtnText": "Re-upload"
}
```

提交的 form api 必须加 `"dataType": "form-data"`：

```json
{ "api": { "method": "post", "url": "/XXX/XXXX/import", "dataType": "form-data" } }
```

- **`F-05`** 文件随表单提交的关键是 `asBlob: true`；缺了它，文件在**选中瞬间**即上传到默认 receiver（`/api/upload/file`），表单提交体里没有文件（只有上传响应）
  `来源:实战观察+V-17实测(2026-09-07)|状态:已实测|版本:6.13.0|后果:后端收不到文件`
  实测 2×2 对照（V-17，判据：请求是否 multipart 且含 `filename=`）：

  | 组 | 配置 | 请求体 | 含 filename |
  |---|---|---|---|
  | A | `asBlob` + `dataType:"form-data"` | multipart 290B | ✅ |
  | B | **只 `asBlob`**（不写 dataType） | multipart 290B | ✅ |
  | C | 只 `dataType:"form-data"` | multipart 14140B（文件值=上传响应对象被展开） | ❌ |
  | D | 都不写 | JSON 2286B（文件值=上传响应对象） | ❌ |

  - **原「asBlob 与 dataType 必须成对」不准确**：`asBlob: true` 存在时 amis **自动**把含 File/Blob 的数据转成 multipart，`dataType: "form-data"` **可省**（B 组实证）
  - 建议仍保留 `dataType: "form-data"`（更明确，且未选文件时也保持 multipart），但非必需

## §6 宽度控制

- **`F-06`** 单列表单（form 直接子项）调宽度用 **`inputClassName` 内置宽度类**或 **`style.width`**；`columnRatio` 只在 **`group` 内**生效（列宽比例，如 `"columnRatio": 2`；源码 `r.columnRatio || getWidthRate(r.columnClassName,!0)`）
  `来源:实战观察+form源码(2026-09-02)+V-19实测(2026-09-08)|状态:已实测|版本:6.13.0|后果:宽度设置不生效（选错写法）`
  实测三轮（V-19-C，判据：`getBoundingClientRect().width`，基线宽度 1230px）：

  | 写法 | form 直接子项 | `group` 内 |
  |---|---|---|
  | `columnRatio: 1/2/6` | ❌ 无效（仍 1230，控件撑满） | ✅ 88 / 192 / 607（约 1:2:6） |
  | `size: "xl"` | ❌ 无效（1230） | — |
  | `inputClassName: "w-xl"` | ✅ **320px** | — |
  | `style: { "width": "350px" }` | ✅ **350px**（内部 input 随之收缩为 328px） | — |

  - **`size` 确实不控宽度**（select 与 input-text 均无变化）
  - **推翻原「`w-xl` 无此内置类」**：amis 6.13.0 内置 `w-sm`/`w-lg`/`w-xl` 等宽度类（实测 150 / 280 / 320px），假类名对照组回到基线 1230 证明非巧合；类落在 `.cxd-Form-control`，内部 input 随之变窄
  - **推翻原「style.width 不传到内部 input」**：style 作用在外层容器，但 input 实测随之收缩 → 视觉上控件整体变窄，写法有效

## §7 协作约束（需后端配合，前端无法独立完成）

- **`F-09`** 联想下拉显示完整 label 的最稳方案：后端 DTO 直接返回 amis 标准 `label`/`value` 字段（如 `label = "code | name"`、`value = code`），前端零映射
  `来源:实战观察|状态:实战观察|版本:6.x|后果:改用降级方案则选中框只能显示单字段`
- 降级方案（后端不配合）：前端 `labelField`/`valueField` + `menuTpl` 定制下拉展示，选中后输入框只显示 labelField 指向的单字段
- 后端 SQL 加 `LIMIT 10` 兜底

## §8 invalid label 陷阱

- **`F-10`** `adapter` 字符串转换在 amis 6.13.0 **完全无效**，勿选——属性名只有 `adaptor`，见 `A-02`
  `来源:实战观察+amis源码+V-14实测(2026-09-03)|状态:已实测|版本:6.13.0|后果:数据源不被转换，下拉为空 / 回退显示原始 value`
  实测对照（同一非标准响应，各自注入可识别 label）：`adaptor` 组正常渲染注入值；`adapter` 组与「不写转换」组表现一致，均回退显示原始 value。
  注：「invalid label」是 `labelField` 匹配不上的另一类表现，不是拼写错误的直接后果 → 排查链见 §3（`F-03`）

## §9 常用控件清单

input-text / textarea / select / input-number / input-date / input-date-range / input-quarter / input-year / input-email / input-password / radios / checkboxes / input-file / hidden / static / uuid / combo
