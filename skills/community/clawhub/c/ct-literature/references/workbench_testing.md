# 工作台标准检验流程（自动化测试 SOP）

> ⚠️ **已迁移至统一测试框架**：本文件保留作为历史参考。当前 ct-literature 的工作台测试已纳入 CT 系列统一的 `ctqa` 框架（位于 `ct-base/testing/ctqa/`），通过 `ctqa.config.json` 的 `legacy` 字段桥接 `workbench/_tests/test_static.py`。统一入口：`python -m ctqa run --skill ct-literature`。规范详见 `ct-base/references/workbench_ui.md` §23。
>
> 适用范围：`workbench/` 工作台页面（HTTP 服务 `server.py` + 前端 `app.js` / `wb-list.js` + 页面 `index.html` + 命令行 `scripts/ct_literature.py`）。
> 维护原则：legacy 桥接的 `test_static.py` 仍随 `python -m ctqa run --skill ct-literature` 执行。
>
> **legacy 保留文件**：`workbench/_tests/_support.py` 与 `workbench/_tests/test_static.py`（桥接到 W1 层），`tests/prompt_usage/_support.py` 与 `tests/prompt_usage/test_l6_coze.py`（桥接到 P5 层）。其余旧测试文件已清理至 `_ctqa_cleanup_backup/`。

---

## 1. 目录与文件

> **现状（2026-10-30 核对）**：`run_all.py`、`test_units.py`、`test_api.py`、`test_stream.py`
> **已于 2026-10-29 迁移时删除**，`units/api/stream` 三层改由 `ctqa` 的 W0/W1/W2B 层承担
> （含真实起服务的接口与浏览器交互检查）。下表为**当前实际留存**：

```
workbench/_tests/
├── _support.py       公共支撑：断言收集器 Report、node 调用、服务托管、HTTP 客户端
└── test_static.py    静态一致性：语法 / i18n / DOM id / 前后端事件协议四元核对（10 断言）
```

两者经 `ctqa.config.json` 的 `skill_tests` 以 **legacy 桥接**（`mode: module`）挂在 **W0** 层，
由 ctqa 统一调度；**没有独立的 `run_all.py`**。

> 该目录已加入 `workbench/publish-kit/build_publish.py` 的 `EXCLUDE_SEGMENTS`，**不会进入发布镜像**（详见 §6）。

---

## 2. 运行方式

```bash
# 在技能根目录执行（ctqa 位于 ct-base/testing，需加 PYTHONPATH）
cd <skill-root>

# 全量（推荐，CI / 发布前核对）
PYTHONPATH=../ct-base/testing C:/Tools/Anaconda3/python.exe -m ctqa run --skill ct-literature

# 只跑工作台相关层（快）
PYTHONPATH=../ct-base/testing C:/Tools/Anaconda3/python.exe -m ctqa run --skill ct-literature --layer W0 W1 W2B

# 诊断可测性（层是否可用 / playwright / node 是否就绪）
PYTHONPATH=../ct-base/testing C:/Tools/Anaconda3/python.exe -m ctqa doctor --skill ct-literature
```

**退出码约定（可挂 CI）：**
- `0` = 绿灯（无阻断项；WARN 不阻断，需人工判断）
- 非 `0` = 存在 FAIL / ERROR（必须修复后再发布）

**报告输出：** `tests/_ctqa_reports/` 下的 `report.html` / `report.json` / `junit.xml` / `summary.md`。

**环境要求：** Python 3（stdlib 即可，无需第三方包）；`node` 需在 PATH（`test_static` 用 `node --check` 校验 JS 语法、用 node 解析 `WB_T` i18n 表）；W2B 层需 playwright。

---

## 3. 四层测试设计

| 套件 | 是否起服务 | 覆盖重点 | 拦截的典型 bug |
|---|---|---|---|
| `static` | 否（纯静态分析） | JS/Py 语法、i18n zh/en 覆盖一致、DOM id 引用均有定义、前后端**事件协议四元核对** | 改了后端忘了前端、文案变 key、`$('#x')` 返回 null 后崩、死事件/不可达分支 |
| `units` | 否（import server） | `_json_event` 以 `\n` 结尾且为单行 JSON、路径沙箱、selection 读写与跨轮残留、`_count_pdfs`、限流 | NDJSON 缺换行致前端整条流无法解析、目录穿越、`skip` 残留静默吞掉下一轮篇目 |
| `api` | 是（真实起服务） | 全部 GET/POST 端点契约、`artifacts`+`selection` 状态一致性、`Host`/`Origin`/`null Origin` 护栏、静态黑名单、公网模式目录穿越 | 端点返回错码、外部 Host/Origin 放行（DNS rebinding / CSRF）、敏感文件泄露 |
| `stream` | 是（真实起服务，dry） | POST `/api/search` 的 NDJSON 流：合法 JSON、含起止事件、dry 不写状态、结束后 `_running` 复位 | 流中混入非 JSON 行、缺 `run_done` 终止事件、流结束后服务永久 409 |

> **当前实际执行情况（2026-10-30 核对）**：上表是**原始四层设计**，其中 `units` / `api` / `stream`
> 三层的独立脚本已删除，能力改由 `ctqa` 的 W0（静态）/ W1（静态代码分析）/ W2B（浏览器交互，
> 真实起服务）层承担。当前可执行的是：
>
> - W0 静态结构与契约：**14 断言**
> - W0 legacy 桥接 `test_static.py`：**10 断言**（事件协议四元核对即在此）
>
> 实测 `--layer W0` 合计 **24 条全绿**（PASS 24 / FAIL 0 / WARN 0）。历史上的"58 项断言全绿"
> 是四层套件并存时期的数据，已不适用于当前结构。

---

## 4. 核心防漂移检查：前后端事件协议四元核对

工作台事件分**两层分发**：

- **传输层**：后端 `_json_event(ev="progress", **ev)` → 前端 `ev.ev` 分支处理。
- **业务层**：CLI `ct_literature.py` 的 `_out(msg, "name")` 原生事件名 → 前端 `ev.event` 分支处理。

> ⚠️ **关键坑**：`_search` / `_batch_run` 对子进程事件**强制 `ev="progress"`**（`_json_event(ev="progress", **ev)`，CLI 事件名平铺进 `ev.event`）；而 `_coze_stream` 用 `_json_event(**ev)` **原生转发**。两侧不一致极易产生「后端发了但前端没接 / 前端接了但后端从不发」的漂移。

`test_static` 提取四组事件名并交叉核对：

1. 后端传输层 `_json_event(ev="xxx")` 集合 `b_outer`
2. 前端传输层 `ev.ev==="xxx"` 集合 `f_outer`
3. CLI 业务事件 `_out(msg, "name")` 集合 `cli_ev`
4. 前端业务层 `ev.event==="xxx"` 集合 `f_inner`

判定规则：
- `b_outer - f_outer` 非空 → **WARN**：后端事件前端未处理（被静默丢弃）
- `f_outer - b_outer` 且不在 `cli_ev` → **WARN**：前端不可达死分支（死代码）
- `cli_ev - f_inner` → **INFO**：CLI 事件无专属前端分支（落到通用 `progress` 显示 message，通常无害）

**改动任一侧事件协议，必须重跑 `static` 套件**（提取前先剥 JS 注释，避免注释中提及的代码被正则误判；CLI 事件正则支持嵌套括号以捕获 `_out(i18n.t("x", n=len(works)), "suggest_few")`）。

---

## 5. 已修缺陷清单（本套件建立过程中发现并修复）

| 类别 | 缺陷 | 处置 |
|---|---|---|
| 真实产品 bug | 后端发 `ev="artifacts"` 但前端全无消费（死事件） | 删除两处 `_json_event(ev="artifacts", dir=...)`，改由 `run_done→resultCard→finish()→artSetDir()` 对齐目录 |
| 真实产品 bug | `app.js` 外层 `ev.ev==="suggest_few"` / `"suggest_item"` 永不可达（真正处理在 `ev.event` 内层） | 删除 859–860 行不可达死分支 |
| 真实产品 bug | `_tests/` 会被打进发布镜像 | `build_publish.py` 的 `EXCLUDE_SEGMENTS` 增加 `_tests` |
| 测试自身（已内化） | `node -e` 直传大段代码超 Windows ~32k 命令行上限，静默报 "node not found" | `_support.run_node()` 改为**写临时 `.js` 文件**执行 |
| 测试自身（已内化） | `py_compile(cfile=os.devnull)` 在 Windows 报 "nul is a non-regular file" | 改为写到临时 `.pyc` 文件并删除 |
| 测试自身（已内化） | JS 注释中的代码被事件正则误判（残留 WARN） | 提取前先 `strip_js_comments()` 剥注释 |
| 测试自身（已内化） | `_norm_skip` 返回 dict 列表，断言误取整项 → 比对失败 | 断言取 `e.get("doi")` 字段 |
| 测试自身（已内化） | CLI 事件正则漏 `suggest_few`（嵌套括号） | 正则支持 `(?:[^()]|\([^()]*\))+` |

---

## 6. 发布前必检清单（gate）

1. **`PYTHONPATH=../ct-base/testing C:/Tools/Anaconda3/python.exe -m ctqa run --skill ct-literature`** 退出码必须为 `0`（W0/W1/W2B 无 FAIL；WARN 不阻断但需在提交说明中逐条确认「已知、无害」）。
2. 若本次改动涉及事件协议（任一侧 `_json_event` / `_out` / `ev.ev` / `ev.event`），**W0 legacy 桥接 `test_static.py`** 必须重新通过，并人工确认 §4 四元核对无新增 WARN。
3. 若改动 `server.py` 的沙箱 / 限流 / selection / 流格式，对应 **W1（静态代码分析）/ W2B（真实起服务浏览器检查）层必须重新通过**。
4. 确认 `_tests/` 已排除在 `build_publish.py` 的 `EXCLUDE_SEGMENTS` 之外（不进发布包）。
5. WARN 不阻断发布，但需在 PR/提交说明里逐条确认「已知、无害」；INFO 仅作规模提示。

---

## 7. 新增断言 / 套件的约定

- 新增纯函数逻辑 → 在 `workbench/_tests/test_static.py`（W0 legacy 桥接，import `server as S`，复用 `Report`）扩展；或以 `ctqa` 的 W1 静态分析层新增对应规则。
- 新增 HTTP 端点 → 在 `ctqa.config.json` 中挂接 **W2B** 层用例，对 `server.py` 端点做契约断言；新增安全护栏 → 加黑名单/Origin 用例。
- 新增流式语义 → 在 **W2B** 层加事件序列断言（优先用 dry 模式，避免联网）。
- 静态规则（i18n / DOM id / 事件协议）→ 在 `test_static.py` 的对应小节扩展；提取逻辑变动务必同步更新注释剥离与正则容忍规则。
- 所有断言用 `rep.check(name, cond, detail)`；仅在确认无害且需人工注意时用 `rep.warn()`；纯提示用 `rep.info()`。
