# CHANGELOG

## 1.2.10（2026-09-08）

V-20 实测收尾 3 条（详见 `docs/verify-lab-260908.yaml` §v20），`A-02/D-07/D-10` 全部由「据源码 / 实战观察」升「已实测」（27→30 条），**三条全部修正机制或理由**：

- **`A-02` 机制修正**：原「非标准响应不转换就渲染不出」**不成立（过严）**——实测无 `status` 字段时 amis 视为成功并渲染：select `{code:200,data:[...]}` 不写 adaptor 照样 3 项；crud `data.records`（字段名完全不被识别）照样渲染 10 行（amis 会遍历 `data` 的值找数组）。**真正的必要性在「失败判定」**：提交返 `{code:500,msg}` 不转换时 **`submitSucc` 照触发**（J 组 `J_SUCC=Y`，后端失败被当成功 → 弹层照关、后续动作照执行）；转换后正确走失败分支（K 组 `K_SUCC=UNSET`）
- **`D-07` 理由修正**：`confirmText` **不是浏览器原生 `confirm`**（覆盖 `window.confirm` 后未被调用），弹的是 amis 自有确认框（标题「系统消息」+ 文本 + 取消/确认），基础功能可用。不用的真因是**失败分支不可控**：接口 `status=1` 时 confirmText 弹层**照样关闭**（A2），而自定义 dialog（`close:false` + `submitSucc` closeDialog）失败时保持打开可重试（B2）；附带实证漏写 `closeDialog` 会导致提交成功后**弹层残留**（C 组）
- **`D-10` 机制修正**：① **`selectedItems` 只在 crud 数据域内可见**（与 `A-01` 同构）——弹层底部按钮的 `disabledOn` 空选时**不禁用**、外层 form api 的 `${selectedItems|pick:id}` 提交体为 `{"ids":""}`；把提交按钮放进 crud headerToolbar 后 body 正常为 `{"ids":[1,2]}`。② **跨页保留选中 = `keepItemSelectionOnPageChange: true` 且 `syncLocation: false`**（2×2 矩阵：keep+sync默认→丢；keep+sync:false→保留；不写 keep→丢）。③ **`loadDataOnce` 与选中保留无关**（F vs G、D vs H 双对照），原归因不准确
- 新增排障 `P-28`（后端业务失败被当成功）、`P-29`（弹层内选择器提交体为空 / 空选可提交）；`self-check.md` §1/§3 三条措辞同步；`META.md` 已实测 27→30，「据源码」级别清空
- 排障 27→29；归档 `_amis-lab/schemas/v20a1~v20c5`（10 个）+ README 归档表；lab mock 新增 `?nested=1`（data.records）与 `?errcode=1`（业务失败无 status）
- 剩余未实测 3 条：`F-09`（后端协作约束，建议降级为约定类规则）/ `C-08` / `R-01`（规范建议，不排实测）

## 1.2.9（2026-09-08）

V-19 实测表单域 4 条（详见 `docs/verify-lab-260908.yaml`），`F-03/F-04/F-06/F-08` 全部升「已实测」（23→27 条），其中 **2 条推翻原断言、1 条大幅修正**：

- **`F-03` 部分推翻**：`autoComplete` **字符串 URL 与对象等效**（D 组实证 `term=abc` 正常请求并渲染 3 项），原「必须是对象」过严。不触发联想的是：① `autoComplete: true` + 外部 `source`（实测只等价于「可搜索」，有搜索框但零请求、纯本地过滤）；② 只写 `source`（即便补 `searchable`，也只在加载时请求一次）。附带观察：无 `sendOn` 时**加载即发一次 `term=` 空请求**
- **`F-04` 成立 + 两个新发现**：sendOn 在 autoComplete 内 → 1 字符不发、3 字符发，且**连初始加载请求一起拦掉**；写在 source 内 → 完全失效（1 字符即发，与不写 sendOn 同构）。**新发现：autoComplete 与 source 并存时 source 的 url 零请求**（autoComplete 完全接管数据源，别再写 source 兜底）
- **`F-06` 大幅修正**（三轮对照，判据 `getBoundingClientRect().width`，基线 1230px）：
  - `columnRatio` **只在 `group` 内生效**（1/2/6 → 88/192/607）；form 直接子项下**无效**（仍撑满 1230）→ 原「宽度只认 columnRatio」仅对 group 场景成立
  - `size: "xl"` 无效（原断言成立）
  - **推翻「`inputClassName` 无此内置 CSS 类」**：内置 `w-sm`/`w-lg`/`w-xl` = 150/280/320px，假类名对照组回到 1230 证明非巧合；类落在 `.cxd-Form-control`，内部 input 随之变窄
  - **推翻「`style.width` 不传到内部 input」**：style 作用外层容器（350px），内部 input 实测收缩为 328px，控件整体变窄 → 写法有效
- **`F-08` 升实测 + 修正**：`value: "${code}"` **非必需**（name 与行字段同名即自动取值）；`hidden` 必需（不写则提交体无 id——弹层 form 只提交 form 内声明的字段，不会自动带行数据）；**新发现：static 的值会随表单提交**，后端 DTO 需能接收或忽略
- 同步修正：`P-09/P-12/P-15/P-24`（P-15 原措辞与实测相反，已重写）；`self-check.md` §5 四条措辞同步；`META.md` 已实测 23→27 条；`SKILL.md` F-03/F-06 索引行同步
- 排障条目维持 27 条；归档 `_amis-lab/schemas/v19a-f03-autocomplete.json`、`v19b-f04-sendon.json`、`v19c1/c2/c3-f06-*.json`、`v19d-f08-static-hidden.json`
- 剩余未实测 6 条：`F-09`（最后做，后端协作）/ `A-02` / `D-07` / `D-10` / `C-08` / `R-01`（后两条为规范建议，不排实测）

## 1.2.8（2026-09-07）

V-18 实测 CRUD 高频 6 条（详见 `docs/verify-lab-260907.yaml` §V-18），`C-01/C-02/C-03/C-05/C-06/C-07` 全部由「实战观察/据文档/据源码」升「已实测」（17→23 条），其中 **2 条修正原断言**、1 条强化：

- **`C-01` 修正后果**：`perPageAvailable` 写错位置（footerToolbar 组件内）时**切换器照常出现**（原「切换器不出现」不成立），只是自定义项被忽略、回退默认 `[5,10,20,50,100]`；另实测列表不含当前 perPage 时切换器显示「请选择」空值 → `perPageAvailable` 须包含 `defaultParams.perPage`
- **`C-02` 修正机制**（3 crud × 3 载体定位矩阵，判据=新增请求数）：`componentId` **只认 id**（填 name 恒失效，即使 crud 已同时设 id）；`target` 与按钮顶层 `reload` **认 id 也认 name**（仅设 id 的 crud 用 id 定位同样生效）——原「id 供 componentId、name 供 target/reload」分工不准确，`name` 非 target/reload 的必要条件；「同时设 id+name」仍为稳妥写法（覆盖全部定位方式）
- **`C-05` 强化（新发现）**：原断言成立且更严重——**一旦 `api.data` 非空，amis 不再自动附加 `page`/`perPage`**（GET/POST 同构，原生 fetcher 与 lab fetcher 双验证）：只映射 `current` 则 `perPage` 丢；`api.data` 只写无关字段 `foo=bar` 时分页参数**全部丢失**（翻页仍只发 `foo=bar`）→ **page 与 perPage 必须都映射**；等价替代：crud 的 `pageField`/`perPageField`（实测生效）
- **`C-03` 升实测**：加载即写 `?page=1`、翻页写 `?page=N&perPage=M`；带参 URL 打开会按 URL 参数请求（实测 `?page=3` → 请求 `page=3`）
- **`C-06` 升实测**：未设 `filterTogglable` 时开关按钮 DOM 不存在；已设时可双向开合、筛选栏默认展开
- **`C-07` 升实测并修正后果**：缺 `*` 时未命中值显示表格空值占位「-」（原「显示空白」）；数字值可匹配字符串 key（id=1 命中 `"1"`）
- 同步修正：`P-13`（症状改为「选项不对/空值」）、`P-19/P-20/P-21` 补实测、`P-03` 补 C-02 引用；`self-check.md` C-01/C-05 自检项强化；`SKILL.md` F-05 索引行同步 V-17 修正（「成对」→「必设 asBlob」，上轮遗留）
- 排障条目维持 27 条（新发现并入 P-13/P-20，未新增）；lab 新增 `index-raw.html`（原生 fetcher 对照壳）

## 1.2.7（2026-09-07）

V-17 实测（详见 `docs/verify-lab-260907.yaml` §V-17），`F-05` 由「实战观察」升「已实测」，并**修正断言**（原「必须成对」不准确）：

- **2×2 对照实测**（判据：请求是否 multipart 且含 `filename=`）：

  | 组 | 配置 | 请求体 | 含 filename |
  |---|---|---|---|
  | A | `asBlob` + `dataType:"form-data"` | multipart 290B | ✅ |
  | B | **只 `asBlob`**（不写 dataType） | multipart 290B | ✅ |
  | C | 只 `dataType:"form-data"` | multipart 14140B（文件值=上传响应对象被展开） | ❌ |
  | D | 都不写 | JSON 2286B | ❌ |

- **真因是缺 `asBlob: true`**：不写 `asBlob` 时，文件在**选中瞬间**即上传到默认 receiver `/api/upload/file`（实测 multipart 含 filename，198B），表单提交体里只剩上传响应对象——这才是「后端收不到文件」的机制
- **原「`asBlob` 与 `dataType` 必须成对」不准确**：`asBlob` 存在时 amis **自动**把含 File/Blob 的数据转成 multipart，`dataType: "form-data"` **可省**（B 组实证）；仍建议保留以求明确，但非必需
- 同步修正 `P-23`（真因改为「缺 asBlob」）、`self-check.md` F-05 自检项；`META.md` 已实测 16→17 条

## 1.2.6（2026-09-07）

V-16 实测（详见 `docs/verify-lab-260907.yaml`），`D-02` 由「实战观察」升「已实测」，并**修正因果与后果**（原断言部分不成立）：

- **V-16-A `D-02` 成立（补重要前提）**：download action **携带 auth token**（浏览器侧 `request-headers` 与服务端日志双侧确认 `Bearer ...` → 200 blob）。**前提**：token 由项目配置的全局 `fetcher` 注入——**amis SDK 本身不注入 `Authorization`**，未配全局 fetcher 时 download 同样无 token（原规则「自带 auth token」易被误解为 amis 天然行为，已补注）
- **V-16-B 因果修正**：`then` 确实不触发，但**对照组（普通 JSON 的 ajax，无 blob）同样不触发** → `then` 在 6.13.0 **恒不触发、与 `responseType` 无关**（原规则归因于 blob 属错误因果）；且**动作链照常走完**（`setValue` 复位执行、loading 变量回到 false），**「loading 卡死」未复现**。后果由「卡死」改为「拿不到 blob」
- **V-16-C 裸 `fetch()` 401 成立**：custom action 内裸 `fetch()` 绕过 amis fetcher → 无 token → 实测 401（与 A 组同端点对照：download 200 / 裸 fetch 401）
- 新增 `P-27`（`then` 字段恒不触发，与 blob 无关）；`P-06` 症状与因果同步修正、`P-07` 补实测；`self-check.md` §4 增补 `then` 自检项；`META.md` 已实测 15→16 条、排障条目 26→27

## 1.2.5（2026-09-03）

V-15 实测（详见 `docs/verify-lab-260903.yaml` §V-15），`F-07` 由「实战观察」升「已实测」并**重写**（推翻原断言）：

- **V-15 `F-07` 重写（推翻原「实战观察」断言）**：autoComplete 的 source 响应，`data` 为**直接数组** `[...]` 与**含 `options` 键的对象** `{options:[...]}` 在 amis 6.13.0 **都正常渲染**（各 3 项）。原规则称「`{options}` 嵌套会致下拉为空」**被实测推翻**——`{options}` 是合法形态。真正出错的形态是 CRUD 式对象（如 `{rows,items}`、`{count,total}`）：amis 会把对象的**值**当选项遍历，显示 `invalid label` / 数字（实测 4 项：`171 / 171 / invalid label / invalid label`）
- 同步修正 `P-11`（原「联想下拉为空=响应 data 嵌套 {options}」改为「联想下拉 invalid label/错乱=CRUD 式对象当 data」）、`self-check.md` F-07 自检项、`META.md` 已实测清单补 `F-07`（14→15 条）
- 归档验证配置 `_amis-lab/schemas/v15a-f07-autocomplete.json`（关键反例：wrap=options 形态）

## 1.2.4（2026-09-03）

V-14 实测三轮（详见 `docs/verify-lab-260903.yaml` §V-14），三条规则升「已实测」（11→14 条），其中一条**推翻 v1.2.2 的源码推断**：

- **V-14-A `F-01` 重写（重大）**：多选 select 提交值**恒为数组**。实测五种配置（默认 / `joinValues:true` / `+extractValue` / `+delimiter:"|"` / 仅 `extractValue`）提交值**全部是 `["a","b"]`**——v1.2.2 依据 select defaultProps `joinValues:!0` 推断「默认即逗号字符串」**被实测推翻**。真实结论：
  - **禁止 `joinValues: false`**（唯一有实质影响的配置，会让元素变成 `{label,value}` 对象）
  - `joinValues` / `extractValue` / `delimiter` 对提交值形态**无影响**，非必需
  - 要逗号字符串只能靠 `join` 过滤器：`"codes": "${field|join:','}"`（实测得到 `a,b`）
  - 同步修正 P-22（原写「默认 true 会拼成逗号分隔字符串」，与实测相反）
- **V-14-A `F-10` 成立 + 后果修正**：注入式对照（同一非标准响应，`adaptor` / `adapter` / 不写转换三组）——`adaptor` 组正常渲染注入值，`adapter` 组与「不写转换」组一致，均回退显示原始 value。**`adapter` 完全无效**。后果由「显示 invalid label」修正为「下拉为空 / 回退显示原始 value」（invalid label 实为 `labelField` 不匹配的表现）；`F-03` 排查链同步修正因果对应
- **V-14-B `D-03` 成立**：事件动作内 `target` 写法**零请求**（失效），`componentId` 与 `componentName` 均触发刷新（后者验证 v1.2.2 补入的等价写法成立）
- 未验证：`F-07`（需 autoComplete 交互场景，本次用 source 测属场景错配——source 的 `data.options` 是合法结构，不能证伪 F-07）
- lab 增强：mock 新增 `nonstd=1`（非标准业务码 + data 为数组）与 `wrap=options` 两个开关；修复非标准响应下日志 `KeyError: 'status'` 导致请求无响应的 bug

## 1.2.3（2026-09-03）

V-13 实测三轮（详见 `docs/verify-lab-260903.yaml`），四条规则由「实战观察」升「已实测」（7→11 条）：

- **V-13-A `D-06` 成立**：form 配 `onEvent.submit` 后接口**零请求**、`submitSucc` 不触发、弹层不关闭；基线组接口正常发出且弹层关闭。源码推断（事件动作须显式 `preventDefault:true`）被实测推翻——form 的 submit 事件是例外，规则补注「以实测为准」；后果描述由「loading 卡死」改为「弹层不关闭（点了没反应）」
- **V-13-B `A-01` 修正 + `D-09` 成立**：三层观测——`setValue` 不带 `componentId` 落在**按钮自身**数据域（Service / headerToolbar / 行内全读不到，比原描述更严格）；带 `componentId` 指向 Service 时 **Service 与 crud headerToolbar 可读**（`D-08`/`D-09` 方案成立），但 **crud columns 行内读不到**（拿初始快照）。`A-01` 重写为分层三态描述
- **V-13-C `C-04` 成立**：total=5 / perPage=10（单页）时 statistics **整个节点不渲染**，total=171 时正常渲染「1/18 共：171 项」；同期 tpl 替代方案在单页下正常渲染
- 归档验证配置 `_amis-lab/schemas/v13a-d06-submit.json`、`v13b-a01-scope.json`、`v13c-c04-statistics.json`

## 1.2.2（2026-09-02）

v1.2.1 全量审查后修复（审查报告 `docs/review-v121-260902.yaml`，21 项）：

- **事实错误修正（源码实证）**：`A-02` 删除「adapter 也能识别」括注——amis 6.13.0 源码只识别 `adaptor`，`sdk.js` 中 5 处 `adapter` 全是 axios 内部配置（与 `F-10` 的矛盾随之消解）；`F-01` 由「多选必带四件套」改为「保持 `joinValues` 为默认 true，`delimiter`/`extractValue` 按需」——select defaultProps 为 `joinValues:!0 / extractValue:!1 / delimiter:","`，原「不写就提交数组」的后果描述不成立，示例 `crud-base.json` 同步精简
- **元数据同步**：`SKILL.md` 规则总数 32→33；`META.md`「已实测」补 `D-12`/`F-02`（5→7 条），新增「据官方文档或源码」级别承载源码佐证规则；`INDEX.md` 行数声明对齐实际
- **SSOT**：reload 载体表三处（`META.md` / `crud.md §9` / `dialog-actions.md §3`）合一，仅保留 dialog-actions §3 为权威，另两处降级为引用（`D-05` 全文出现数 19→13）
- **来源升级为「据源码」**：`C-03`（crud defaultProps `syncLocation:!0`）、`D-03`（补 `componentName` 等价写法，源码 `componentId ? getComponentById : getComponentByName`）、`F-06`（措辞由「grid 布局」改为「form group 列宽比例」）、`A-02`、`F-01`
- **覆盖补齐**：`pitfalls.md` 新增 P-19～P-25（补 C-03/C-05/C-07/F-01/F-05/F-08 的排障入口 + F-02 的 ajax 跳过校验边界）；`data-source.md` 补 `patch`；`SKILL.md` 触发矩阵补 `META.md` 入口
- **示例层**：`dialog-confirm-loading.json` → `dialog-confirm.json`（`git mv` 保留历史，消除 loading 命名误导）；`INDEX.md` §2 补 `button-group` 包装片段，消除「三个按钮平铺→违反 C-08」的组合隐患；`dialog-form-edit.json` 两个 static 写法统一
- **命中率**：description 补触发场景（crud / 弹层 / 表单校验 / 字典联想 / 导入导出 / 刷新联动）；删除非标准字段 `disable`
- 终检：6 个 JSON 合法 / 16 文件全 CRLF / 33 条 ID 无跳号无悬空 / P-01～P-25 连续 / 规则层 656（≤800）/ 示例层 445（≤460）/ INDEX 声明行数与实际全对
- 未闭环，转入 V-13 实测：`D-06`（onEvent.submit 是否真拦截，源码 preventDefault 机制存疑，后果严重）、`A-01`（crud 内 setValue 不向外传播，D-09 唯一依据）、`C-04`（statistics 单页不渲染）

## 1.2.1（2026-09-01）

v1.2 收尾实测三组（V-10/V-11/V-12，详见 `docs/verify-lab-260901.yaml`）+ 规则落地：

- **V-11 required 校验链**：F-02 改写为「必填只写 `required:true`，勿双写 `validations.isRequired`（幂等无增强）」；实测边界修正源码推断——全空格串被拦截（源码推断不拦截）、ajax 按钮跳过提交前校验阻断（红字是 onChange 副作用）；新增 P-17（隐藏必填误拦截）/ P-18（combo 行内不校验）
- **V-12 close 缺省 form api reload**：D-11 升「已实测」（A 组新增 GET 生效 / B 组 close:false 不生效，V-2 复现）；与 D-05 形成对偶边界
- **V-10 按钮级 reload**：新增 D-12（两形态）——刷新专用按钮 `actionType:reload` 必须用 `target`（顶层 reload 无效）；业务按钮 ajax/submit 用顶层 `reload` 属性（close 不影响）；§3 表格三分、crud.md §9 与 META reload 载体总表同步
- 规则数量 32→33（D×11→D×12）；排障 16→18；META 可信度分级「已实测」行补 D-11
- 终检：权威形态唯一性 / 编号连续 / 悬空引用=0 / 全文 CRLF（见 `docs/verify-lab-260901.yaml` 末）
- 评审回执后补（`docs/review-v121-260901-in.yaml`，有条件通过）：SKILL.md version 同步 1.2.1（必修）；§2 决策表「刷新」行补 D-03/D-12/D-11/D-05；dialog-actions §3 表按钮级行拆两行；form-controls §2 F-02 补 P-18 引用。建议3（三表重叠）跳过（评审自述不强制）

## 1.2.0（2026-08-31）

SSOT 重构，四批次完成（评审文档见 `docs/`，基准 `docs/plan-iteration.md` §5.2）：

- 批次 1（5d3d67c + ee1a027）：规则 ID 体系冻结——32 条权威规则 = R-01 + C-01~C-08 + D-01~D-11 + F-01~F-10 + A-01~A-02，每条带「来源|状态|版本|违反后果」四要素
- 批次 2（ded35a5）：`pitfalls.md` 重编号 P-01~P-16 纯引用化（症状 + 错误写法 + ID 指向）；`SKILL.md` 索引化（59 行）
- 批次 3（135d383）：`crud-full.json` 拆 4 片段 + `examples/INDEX.md`（宿主依赖 / 覆盖规则 ID / 行数）
- 批次 4（a137700）：新增 `references/self-check.md`（6 组 33 项正向自检清单，覆盖 32 条规则，`C-02` 跨组复检，只引规则 ID）；`META.md` 参考文档计数更新；`SKILL.md` 触发矩阵补 self-check 入口
- 终检全部 PASS：权威形态唯一性（32 条各出现 1 次）/ 编号连续无跳号 / 悬空引用 = 0 / 全文 CRLF

## 1.1.0（2026-08-31）

止血修正（commit 7d1dea8；实测 V-1 / V-1-D / V-2 / V-3，详见迭代计划 §5.1）：

- 删除弹层提交 `loadingOn` 死配置（submit 按钮有内建 loading，实测三组对照均转圈）；导出 / download 按钮的 `loadingOn` 保留（实测等待下载完成，有效）
- 统一 `api.reload` 说法：`close: false` 下不生效且提交不默认刷新 CRUD，唯一写法是 `submitSucc` 显式 `componentId` reload（V-2 实测）
- 新增 `META.md`：amis 版本锚定（6.13.0）+ 适用边界 + 规则可信度分级
- `adaptor` 拼写统一为官方标准名；`data-source.md` 示例去 `//` 注释；修正 reload `target` 作用域（仅事件动作内失效）；删除不存在的 `columnsToggled`
- frontmatter 补 `amis-version` / `allowed-tools`

## 1.0.0

首发：SKILL.md + 5 references + 3 examples（957 行）。
