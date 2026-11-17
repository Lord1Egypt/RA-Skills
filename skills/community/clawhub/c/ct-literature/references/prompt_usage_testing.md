# 提示词使用方式 · 标准检验流程（自动化测试 SOP）

> ⚠️ **已迁移至统一测试框架**：本文件保留作为历史参考。当前 ct-literature 的 Coze 信封脱敏测试（`test_l6_coze.py`）已纳入 CT 系列统一的 `ctqa` 框架，通过 `ctqa.config.json` 的 `legacy` 字段桥接。统一入口：`python -m ctqa run --skill ct-literature`。规范详见 `ct-base/references/workbench_ui.md` §23。
>
> 适用范围：ct-literature 技能的**提示词 / 上下文使用方式**全链路。
> 维护原则：legacy 桥接的 `test_l6_coze.py` 仍随 `python -m ctqa run --skill ct-literature` 执行。

---

## 1. 目录与文件

```
tests/prompt_usage/
├── run_all.py         总入口：汇总七层，退出码 0=无FAIL / 1=有FAIL
├── _support.py        公共支撑：断言收集器 Report、CLI preview 子进程托管
├── test_l1_spec.py    规格/参数构造纯函数（_build_search_topic / _build_lane_plan）
├── test_l2_injection.py 注入 / SAFE PREVIEW 闸门（单测 monkeypatch + 子进程）
├── test_l3_continuity.py 跨轮连贯 merge_spec（ct-base 共享权威副本）
├── test_l4_batch.py   批量规格 parser（行列表 / YAML / key=value / concepts）
├── test_l5_triage.py  触发/triage 弱断言（静态规则 + dry-run 冒烟）
├── test_l6_coze.py    Coze 信封 11-key 脱敏 + 真实白名单发送 e2e
└── test_l7_e2e.py     E2E dry-run 流水（英/特殊/超长/中文）
```

该目录已加入 `workbench/publish-kit/build_publish.py` 的 `EXCLUDE_SEGMENTS`（连同整个 `tests/`），**不会进入发布镜像**。

---

## 2. 运行方式

```bash
# 进入测试目录
cd tests/prompt_usage

# 只打印失败/告警（Coze e2e 默认跳过）
C:/Tools/Anaconda3/python.exe run_all.py

# 打印全部断言（推荐，CI / 发布前核对）
C:/Tools/Anaconda3/python.exe run_all.py -v

# 只跑指定层
C:/Tools/Anaconda3/python.exe run_all.py l1 l4 l6

# 含真实白名单 Coze 发送 e2e（用户已授权；默认不跑，避免每次发真实报告）
CT_COZE_E2E=1 C:/Tools/Anaconda3/python.exe run_all.py l6
```

**退出码约定（可挂 CI）：** `0` = 无 FAIL；`1` = 存在 FAIL。

**环境要求：** Python 3（stdlib 即可，无需第三方包；批量 YAML 解析需 PyYAML，但本套件经 dict 直传规避）。`ct-base` 须与本技能同级（`../ct-base/scripts/merge_spec.py`）以覆盖 L3。

---

## 3. 七层测试设计

| 层 | 是否联网 | 覆盖重点 | 拦截的典型 bug |
|---|---|---|---|
| `l1` | 否（纯函数） | `_build_search_topic` 概念 AND 拼接+去重、`_build_lane_plan` 维度分轨 | 概念重复/漏拼、safety lane 缺失、深度救援轨逻辑错 |
| `l2` | 否（单测）+ 子进程英文 | **SAFE PREVIEW 闸门**（monkeypatch `run()` 证明不进 fetch）+ 恶意 topic 注入 | 缺 `--run` 仍联网、`$()`/反引号/多行注入被执行、topic 被当 CLI flag |
| `l3` | 否（纯函数 + 脚本） | `merge_spec.merge`：cur 覆盖 prev、继承审计、required 校验 | 跨轮字段污染、未改字段被静默覆盖、必填空缺未报 |
| `l4` | 否（纯函数） | `batch_lib.parse_linelist/parse_yaml/_parse_kv_tokens/_normalize_concepts` | `#` 误吞、含空格值丢失、`safety=false` 误展开、YAML 嵌套错、畸形输入崩溃 |
| `l5` | 否（dry-run） | dialogue.md 四桶分类 + §12 网关（静态）；多形态输入 preview 冒烟（弱断言） | triage 规则缺失、多样输入下 preview 崩溃 |
| `l6` | 否（单测）+ 可选真发 | `bug_report.sanitize_report` 11-key 硬白名单；`send_to_endpoint` e2e | 非白名单键泄露原始数据、description 被吞、类型不符 |
| `l7` | 否（英文）/ 中文允许 | `ct_literature.py` E2E dry-run：exit 0 + `[PREVIEW]` + 不进 fetch | 长/特殊字符主题崩溃、中文翻译后未回 PREVIEW |

当前状态：**108 项断言全绿（0 FAIL / 0 WARN）**；真实 Coze e2e 发送返回 `status=ok`（信封端到端可达）。

---

## 4. 核心防漂移检查

- **SAFE PREVIEW 闸门（最关键）**：`main()` 在缺 `--run` 时必须于 preview 分支直接 `return`，绝不调用 fetch 管线 `run()`。L2 单测 monkeypatch `ct_literature.run`，断言：无 `--run` → `run()` 调用次数 0；带 `--run` → `run()` 被调用（证明闸门逻辑正确）。**任何修改 preview 路径或 `run()` 触发条件的改动，必重跑 L2。**
- **Coze 信封 11-key 硬白名单**：`sanitize_report` 仅保留 `REPORT_SCHEMA` 键，任何用户原始数据键（受试者表/原始输入）一律剔除；`description` 为唯一自由文本字段，空串省略键。L6 单测断言剔除与保留；e2e 验证端到端可达。**改 `REPORT_SCHEMA`/`sanitize_report` 必重跑 L6。**
- **跨轮连贯 merge_spec**：cur 覆盖 prev、未提及字段无损继承、required 缺失必报。L3 覆盖纯函数与 `merge_spec.py` stdin 接口。**改合并逻辑必重跑 L3。**

---

## 5. 已踩坑（测试设计教训）

- **死代理断言法不可用**：曾用 `HTTPS_PROXY=http://127.0.0.1:1` 覆盖代理来「证明不联网」，但 skill 的 PREVIEW 路径会对**非英文主题做在线翻译**（合法网络调用），死代理使其永久阻塞 → 整批测试卡死。
  → 改为：preview 子进程用**正常环境**；英文主题不触发翻译（零网络、确定性）；「未进 fetch」改由 **L2 单测 monkeypatch `run()`** 确定性证明，而非依赖死代理。
- **跨套件顺序无关**：曾误判「l2 在 l1 之后卡死」，实为 zh 翻译联网耗时 + 轮询过早；`l1+l2` 与 `l3–l7` 分组均可在 ~2–3 分钟内通过，整批约 4–6 分钟（含 2 个中文翻译联网 case）。CI 超时须 > 8 分钟或排除中文 case。
- **ct-base 路径**：`merge_spec.py` 是 `ct-base/scripts/` 的家族唯一权威副本（非本技能内），L3 从其导入；若 ct-base 不在同级，L3 退化为 WARN 不阻断。
- **concept flag 名**：CLI 是 `--concept TYPE=VALUE`（可重复 append），**不是** `--concepts`；用错 flag 会 argparse `rc=2`。

---

## 6. 发布前必检清单（gate）

1. `cd tests/prompt_usage && C:/Tools/Anaconda3/python.exe run_all.py -v` 退出码必须为 `0`（无 FAIL）。
2. 若改动 SAFE PREVIEW 闸门 / `run()` 触发 → L2 必过；改动 Coze 信封 → L6 必过；改动 merge_spec → L3 必过；改动 batch parser → L4 必过；改动主题构造 → L1 必过。
3. 真发 e2e（可选，用户授权场景）：`CT_COZE_E2E=1 ... run_all.py l6` 返回 `status=ok` 即信封端到端可达。
4. 确认 `tests/`（含 `prompt_usage/`）已排除在 `build_publish.py` 的 `EXCLUDE_SEGMENTS` 之外（不进发布包）。
5. WARN/INFO 不阻断发布，但需在提交说明里逐条确认「已知、无害」。

---

## 7. 与工作台测试套件的关系

- `workbench/_tests/`（static/units/api/stream）覆盖**工作台 Web UI / 服务 / 事件协议**；本套件覆盖**技能提示词/规格/CLI/Coze 使用方式**。两者共同构成技能的完整标准检验流程。
- 发布前两者都应跑；详见 [workbench_testing.md](workbench_testing.md) 与本文档。

---

## 8. 新增断言 / 套件的约定

- 纯函数逻辑（L1/L3/L4/L6 单测）→ 直接 import 对应模块（`ct_literature` / `ct-base/scripts/merge_spec` / `batch_lib` / `adapters/bug_report`）断言。
- 需真实运行 CLI 的场景（L2/L5/L7）→ `run_cli_preview(topic, extra)` 起子进程走 PREVIEW；**英文主题零网络、确定性**；中文主题允许联网翻译（放宽超时）。
- 安全闸门类断言优先用 **monkeypatch 单测**（如 L2 的 `run()` 拦截）而非依赖环境变量。
- 所有断言用 `rep.check(name, cond, detail)`；仅无害且需人工注意用 `rep.warn()`；纯提示用 `rep.info()`。
