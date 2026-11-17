# ct-advisor 改进实施记录 — 连续提问诊断落地（2026-09-23）

> 来源：《Ct-Advisor_连续提问诊断报告》（2026-09-23）5 项改进建议的落地。
> 范围：**本地技能侧**为主；Coze 端只给**可选、向后兼容**补丁，默认零改动。

---

## 0. 结论先行：大文档上传是否需要 Coze 端较大改动？

**不需要。** 采用「本地分块 + 检索、只传相关片段」路线，Coze 端 **零改动** 且 **与老版本完全兼容**。

论据（基于代码事实，非推测）：

| 事实 | 依据 |
|---|---|
| Coze 端 = **你自控、可部署**的 LangGraph 镜像（打包 zip 上传 + 重启镜像生效），非黑盒 SaaS | `adapters/coze/`、`coze_modification_guide.md` |
| 外发契约只有 4 个字段：`query_meta / original_question / draft_answer / conversation_history` | `adapters/refiner.py::to_payload` |
| 大文档片段**内联进 `original_question`**（核心契约字段）→ 老/新 Coze 都认 | 本次 `doc_memory.compact_large_question` |
| 新增字段一律 `default_factory`/缺省；Coze 端 `GraphInput` 为 pydantic `extra='ignore'` | `coze_cache_policy.md §7/§10`、`refiner.py` |
| 响应兼容：`final_answer`（新）/ `answer`（老）双键回退 | `refiner.py::refine` |

**只有**当你要「整本文档进 Coze 知识库做跨会话**语义**检索」时，才需要 Coze 端中等以上改动（节点接 KB 查询 + 受 Coze 平台 KB 文件大小/格式约束）。**跨会话文档记忆默认落在本地**即可满足需求。

---

## 1. 改进映射（诊断建议 → 落地状态）

| 编号 | 诊断建议 | 落地方式 | 状态 |
|---|---|---|---|
| A | 会话上下文 + 文档记忆 | 文档记忆：`doc_memory`（大文档入库+检索）；无状态调用由 `conversation_history`（既有）+ 本地去重/压缩协同缓解 | ✅ 本地侧完成 |
| B | 重复提交检测/去重 | `dedup_guard`（同 origin 近似去重 + 本地答案短路）+ `refine_answer` 串行路径接入 | ✅ 完成 |
| C | 范围路由与明确转介 | `scope_guard`（医学写作/综述类且弱试验信号 → 超范围转介声明，后置注入） | ✅ 完成 |
| D | 质量稳定性 | 由 Coze 端作答契约（C1/C3）+ 缓存四闸既有机制覆盖；本次未改 | ⚪ 既有机制 |
| E | 大文档/上传能力 | 本地分块+检索（`doc_memory`），片段内联外发；Coze 端可选补丁见附录 | ✅ 本地侧完成 |

---

## 2. 新增/修改文件

### 新增（本地守卫）
| 文件 | 作用 |
|---|---|
| `scripts/doc_memory.py` | 大文档内容哈希入库、分块（~600 字重叠窗口）、关键词重叠检索；`compact_large_question()` 把超长问题压成「指令头 + 相关片段」 |
| `scripts/dedup_guard.py` | 按 `query_origin` 记录近期问题/答案；`quick_ratio≥0.90` 判重；命中且存过答案→本地短路复用 |
| `scripts/scope_guard.py` | 强写作意图 ∩ 无试验运营信号 → 超范围；产出转介声明（`apply_referral` 前置注入） |
| `scripts/forward_guards.py` | 三守卫编排；`apply_guards(req, mode)`；fire_only/collect 直接 no-op |
| `scripts/test_local_guards2.py` | 离线单测（monkeypatch 隔离存储，无网） |

### 修改
| 文件 | 改动 |
|---|---|
| `scripts/refine_answer.py` | `req.validate()` 后注入守卫调用（防御式，异常跳过）；串行路径支持去重短路；ship/forward/serial 三个收尾点注入范围声明 + 回写去重库 |
| `adapters/refiner.py` | `RefineRequest` 增可选字段 `doc_context` / `scope_hint`（默认空、normalize 归一、**不随契约外发**，与 `tone_profile` 同策略） |
| `adapters/coze/coze_modification_guide.md` | 追加 §六「可选增强：doc_context / scope_hint（向后兼容，非必改）」 |

---

## 3. 关键设计约束（与既有纪律一致）

- **race 硬闸门**：`fire_only` / `collect` 路径 **零本地检索**（`apply_guards` 直接返回 no-op），绝不「先本地检索再发 Coze」。
- **防御式**：所有守卫 `try/except` 兜底，任何异常仅写 stderr 后跳过，**绝不阻断主流程**（与 `context_stitch` 打包失败同策略）。
- **零 Coze 改动即可受益**：大文档片段内联 `original_question`；去重短路在本地完成；范围声明本地注入。
- **向后兼容**：新增字段缺省 + `extra='ignore'` + 双键回退，老本地/老 Coze 双向共存。

---

## 4. 测试

- `route.py --self-test`：29/29 = 100%（无回归）。
- `test_local_guards.py`：**ALL PASS**（doc_memory / dedup_guard / scope_guard / forward_guards，含 fire_only no-op 断言）。
- `test_local_doc_payload.py`：**32/32 PASS**（本地→Coze 大文档载荷外发契约，跨端用 Coze 解析器反解本地载荷）。
- **端到端接线验证**（真实跑 `refine_answer.py`，不触网）：预置去重记录 → 串行模式命中短路，stdout 输出复用答案，stderr `forward_guards: dedup:hit(0m)`。✅

---

## 5. 已知事项 / 后续

1. ~~环境文件锁~~ **【已于 2026-09-23 第二轮全部解决】**：锁释放后已完成——
   - `scripts/dedup_guard.py::_store_path()` 修正落盘：`CT_ADVISOR_DATA_ROOT` 一律视为**目录根**、文件名固定拼接（与 `doc_memory` 语义一致）；生产路径 `ROOT/config/dedup_store.json` 不变。
   - 测试文件已合并：`test_local_guards.py` 保留为唯一版本，冗余的 `test_local_guards2.py` 已移出仓库。
2. **未动**：`workbench/index.html` 渲染层对缓存/去重来源的提示条（可选优化）。

---

## 6. Coze 端落地（2026-09-23 第二轮，v1.21）

本地守卫解决「问题文本」层面的浪费；**文档本体**的处理已按用户要求落到 Coze 端（不再追求「零改动」）：

- 新增入口节点 `doc_ingest`（`doc_ingest → cache_check → …`）：解析 `doc_context` → 服务端文档库落盘 → 按指令检索证据块；
- 新增 `src/doc/`：`doc_router`（分块 + 梳理型覆盖/问答型相关度排序）、`doc_store`（SQLite 文档库）、`payload`（契约真源）；
- `full_analysis`：文档依据**前置为最高优先级** + 「文档优先原则」6 条硬约束；文档在线时**抑制**「KB 缺席」误报免责、**跳过**联网补充；
- 缓存键纳入**文档指纹**；文档场景 `generate_organized_problems` 改用 `instruction` 判难度/组织问题；
- 飞书信封追加 `doc_id/doc_chars/doc_chunks/doc_fp/doc_mode`（不新增列）；
- 本地侧：`doc_memory.build_doc_payload()` 构造结构化载荷 → `forward_guards` 写入 → `refiner.to_payload()` 非空才外发。

设计与算法规格：`adapters/coze/docs/doc_pipeline.md`；部署清单：`adapters/coze/coze_modification_guide.md §六`（v1.21 **必改**）。
部署包：`adapters/coze/ct-advisor_coze_v1.21_20260923.zip`（107 文件，md5 `b8ab0e985aaa186879482bb5cbc30774`）。

---

## 7. 建议的下一步（可选）

- 部署 v1.21 包后按 §6.5 做 4 条线上验收（梳理型覆盖 / 问答型命中 / 重复请求命中缓存 / 无文档回归）。
- 观察线上 advisorlog：重复提交是否下降、`scope:medical_writing` 转介是否按预期触发、`doc_*` 信封字段是否落地。
- 可选延迟优化：启用「追问只传 `doc_id`」（服务端已就绪，见 guide §6.7）。
