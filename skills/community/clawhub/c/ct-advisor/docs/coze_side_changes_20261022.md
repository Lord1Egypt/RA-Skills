# Coze 侧配套改动说明 · ct-advisor v1.3.17（2026-10-22）

> 本文档是 **Coze 部署侧** 的配套改动说明，由本地侧（entry.py / workbench proxy / session_store / scope_guard / UI）完成的「适用范围扩大 + 会话上下文 + 缓存去重」改造所对应的云端契约。
> **红线：本技能本地仓库绝不触碰 `adapters/coze/`**。所有本地改动已在 `scripts/` 与 `workbench/` 落盘并离线自测通过；本文档只描述 Coze 工作流侧 **应当接受 / 可选优化** 的请求字段与返回约定，供云端维护者对齐。

---

## 1. 背景（来自飞书 advisorlog 近 30 天诊断）

| 实测痛点 | 数据 | 根因 |
|---|---|---|
| 多轮承接靠用户手工复述 | 18% 提问含「承接上一轮 / 继续调研」回指 | `context_stitch` 算出的 history 从未被主链路（entry.py / proxy）注入 Coze payload |
| 重复发送白烧云端 | 21%（11 个重复簇） | `answer_cache` / `dedup_guard` 只接在 `refine_answer.py` CLI 路径，entry.py / proxy 直连 Coze 时完全绕开 |
| 高频能力域被误判超范围 | 47% 提问为写作/大纲/模板类，旧版一律前置免责转介 | 旧 `scope_guard` 把 `medical_writing` 当超范围 tag |
| 进度无反馈、长问题焦虑 | p50 68.7s，无阶段/计时 | workbench UI 缺进度态 |

目标：尽量扩大适用范围（仅明确非医药/生命科学语境才转介），并把上下文/缓存/去重做成跨入口一致的本地能力。

---

## 2. 本地已完成的改动（不依赖 Coze 改动即可生效）

| 模块 | 改动 | 是否需 Coze 配合 |
|---|---|---|
| `scripts/scope_guard.py` | 重写为 domain 路由（多标签）；writing/ops/compliance 升为在范围核心域 | 否（仅写 payload 提示） |
| `scripts/session_store.py` | 新建统一存储：history + 跨 session 答案缓存 + 同 session 近窗去重 | 否 |
| `scripts/entry.py` | `--session` 注入 `conversation_history`；所有路径走 cache/dedup 短路 | 否 |
| `workbench/ct-advisor-proxy.py` | `_inject_session` 注入上下文 + 写 `scope_hint`/`domain_hint`；命中短路返回本地伪 task；新增 `/api/history` `/api/turn` `/api/feedback` | 否（端点全本地） |
| `workbench/index.html` | 进度阶段 + 计时 + 附件引导 + `output_format` 选择 + 历史 + 👍/👎 满意度 | 否（前端） |

> **结论：本地侧改造对 Coze 是「payload 富化 + 前置短路」，旧的 `/run` `/async_run` `/task/{id}` 端点契约不变即可工作。** 以下字段为「建议接受」级别；不实现也不会报错，只是少一层上下文/优化。

---

## 3. Coze 请求字段契约（建议接受）

本地代理在转发前向 body 注入以下字段（已存在则保留前端值，仅当缺省时补）：

| 字段 | 类型 | 含义 | 优先级 |
|---|---|---|---|
| `conversation_history` | `array<{question, answer_summary}>` | 历史轮次（含摘要，非全量原文），用于消解回指 | **建议接受**（直接拼进系统提示/上下文） |
| `scope_hint` | `string` | 仅超范围时为 `"non_medical"`；命中后本地已前置转介声明 | 可选（引擎可据其强化边界语气） |
| `domain_hint` | `array<string>` | 多标签 domain，如 `["compliance","ops"]` | **建议接受**（优化检索/兄弟技能路由） |
| `query_meta.output_format` | `string` | `auto|doc|outline|table|ppt`，期望答案形态 | 可选（引擎尽量遵循） |
| `session_id` | `string` | 稳定 per-machine id（镜像 `query_origin`） | 可选（引擎侧做跨轮记忆时可复用） |

`/stream_run` 路径：代理只注入上下文，不做短路（流式无法本地伪 task），其余字段同。

---

## 4. Coze 返回字段约定（保持不变 + 建议增量）

- **不变**：`final_answer` / `answer` 双键、`need_tool` / `params` / `message` 透出。（注：本地侧完整性信封自 v1.3.21 起**不再使用 base64**——标记 `<<<CT_ANSWER_END>>>` + `checksum` 由 `entry._emit_plain` 在出口产生，Coze 返回体本身无需任何编码约定。）
- **建议增量**（非必须）：出参可附 `skill_version` + `coze_version`（已在 §20.13 落地），便于 §22.5 审计对齐；`domain_hint` 命中时可在 `basis` 中标注所依据的知识库 topic。

---

## 5. 可选优化（云端侧，非阻断）

1. **`domain_hint` 路由增强**：用 `compliance/ops/writing` 等标签在知识库检索阶段偏置（如 writing → 方案/CSR 模板库；ops → SOP/预算库），降低泛化检索噪声。
2. **`output_format` 渲染**：`table`/`ppt` 时直接产出结构化块（表格 / 幻灯片大纲），前端 `outFmt` 选择已就位。
3. **长任务进度**：本地 proxy 已加「已提交，云端分析中…（已 Ns）」轮询计时；云端若能在 `/task/{id}` 轮询返回 `progress` 阶段字段，可进一步点亮阶段进度条（前端已预留 `_progTimer`）。

---

## 6. 部署红线与检查清单

- ❌ **不修改 `adapters/coze/`**：本地仓库零改动，所有逻辑在 `scripts/` + `workbench/`。
- ✅ 本地自测已通过：`scope_guard --selftest`（15/15）、`session_store` 内嵌自测（ALL PASSED）、`entry.py --help`、`proxy` 语法检查、`index.html` 内联 JS `node --check`。
- ✅ 旧 `/run` `/async_run` `/task/{id}` 端点契约未变，线上零成本兼容。
- ⏳ 正式发布 workbench 应用需重新打包上传（用户授权后执行 `publish-kit/build_publish.py` + 重发应用）。
- ⏳ 若云端要启用 §3/`domain_hint`/`output_format` 优化，单独排期，不影响本次本地发布。
