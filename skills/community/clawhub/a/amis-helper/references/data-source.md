# API 与数据源

规则 ID 前缀 `A-xx`，元数据四要素：`来源|状态|版本|违反后果`。

## §1 api 配置三种写法

1. 字符串简写（GET）：`"api": "/XXX/XXXX/list"`
2. 方法前缀简写：`"api": "put:/XXX/XXXX/reset/${id}"`
3. 对象（推荐，可控制 data/headers）：

```json
{
  "api": {
    "method": "post",
    "url": "/XXX/XXXX/page",
    "data": { "current": "${page}", "size": "${perPage}" }
  }
}
```

支持的 method：get/post/put/delete/patch。

## §2 响应结构转换（`A-02`）

- **`A-02`** 非 amis 标准响应用 `adaptor` 把业务码转成 `status`（**必要性在「失败判定」**）；**`adapter` 是常见误拼，6.13.0 写了完全无效**（源码只识别 `adaptor`；`sdk.js` 里出现的 `adapter` 全是 axios 内部配置，与 amis 无关）
  `来源:实战观察+amis源码(2026-09-02)+V-20实测(2026-09-08)|状态:已实测|版本:6.13.0|后果:不转换时后端业务失败被当成功（submitSucc 误触发、弹层照关）；adapter 拼法静默失效`
  实测（V-20，判据：是否渲染 + 提交后 `submitSucc` 是否触发）：

  | 场景（响应体） | 不写 adaptor | 写 adaptor |
  |---|---|---|
  | select `{code:200,data:[...]}` | **渲染 3 项** | 3 项（无差异） |
  | crud `{code:200,data:{records:[...]}}` | **照样渲染 10 行**（amis 会遍历 `data` 的值找数组） | 10 行 |
  | 提交 `{code:500,msg:"..."}` | **submitSucc 触发**（后端失败当成功）+ 仍 toast msg | submitSucc 不触发，正确走失败分支 |

  - 「不转换就渲染不出数据」**不成立**（过严）：无 `status` 字段时 amis 视为成功，字段名也有宽容兜底
  - **真正的必要性是失败判定**：业务码失败不转换 → 成功分支照走（`D-01` 的 closeDialog、刷新等都会误执行）
  - 字段/结构映射仍建议写 `adaptor`（行为可控，不依赖 amis 兜底）

amis 标准响应：`{ "status": 0, "data": { "items": [...], "total": n } }`。两个转换位置：

```json
{ "api": { "method": "post", "url": "/XXX/XXXX/page",
  "adaptor": "return { ...payload, data: { items: payload.data.rows, total: payload.data.total } };" } }
```

```json
{ "source": { "url": "/XXX/XXXX/dict/list?type=Country",
  "adaptor": "return { status: payload.code === 200 ? 0 : payload.code, data: payload.data };" } }
```

常见转换：后端分页字段 `rows/total` → `items/total`；业务码 `code:200` → `status:0`；adaptor 是 JS 片段，可用 `return { ...payload, ... }` 展开原 payload。

## §3 变量取值

| 变量 | 来源 |
|------|------|
| `${page}` / `${perPage}` / `${total}` | crud 数据域 |
| `${行字段名}` | 行上下文（operation 列按钮、弹层 title） |
| `${term}` | autoComplete 搜索词 |
| `${selectedItems}` / `${selectedItems.length}` / `${selectedItems\|pick:字段}` | crud 选中行 |
| `${file}` | input-file |
| `${ENV.xxx}` / `${LC_LOCALE}` | 环境变量 |

## §4 表达式条件显隐

- `visibleOn: "${xxx == 'a'}"` 控制显隐（`visible` 直接布尔）
- `disabledOn: "!${selectedItems.length}"` 控制禁用
- `sendOn` 控制联想请求触发条件（位置规则 → references/form-controls.md §3 `F-04`）

## §5 CRUD 与 Service 数据域（`A-01`）

- **`A-01`** 状态变量一律声明在外层 Service 的 `data`，且 `setValue` 的 `componentId` 指向 Service（写法 → references/dialog-actions.md §4 `D-09`）。实测作用域（V-13-B，2026-09-03）：
  - `setValue` **不带 `componentId`** → 落在**按钮自身**数据域，Service / crud headerToolbar / 行内**全部读不到**
  - `setValue` 带 `componentId` 指向 Service → Service 与 **crud headerToolbar 可读**（故 `D-08`/`D-09` 的 loadingOn 方案成立），但 **crud columns 行内读不到**（拿到的是初始快照值）
  `来源:实战观察+V-13-B实测(2026-09-03)|状态:已实测|版本:6.13.0|后果:状态变量读不到 → loadingOn 恒 false；行内若依赖 Service 变量会拿到过期初始值`
