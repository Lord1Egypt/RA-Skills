# Coze 端修复规格 · publisher_pdf_batch 与 literature_summary 失败治理

> 生成：2026-11-13（ct-update 飞书取数分析结论驱动）
> 适用范围：ct-literature 的 Coze 端 `feishu_write` 节点 / `publisher_pdf_batch` 结果构建器
> 背景：本地脚本（`scripts/ct_literature.py`、`scripts/batch_lib.py`）**只构建 `querystr` 载荷**；
> `resultstr`（含 `status` / `s3` / `ok` / `total` / `runtime_sec` / `skill_version` / `coze_version`）
> **由 Coze 端飞书节点写入**（见 `ct_literature.py:1635` 注释与 `batch_search_contract.md §4`）。
> 因此下列修复**只能在 Coze 端落地**，本地脚本无法改。

---

## 0. 实证依据（来自 2026-10-15 → 2026-11-13 飞书 searchlog 650 条）

经 `feishu_log_fetch.py --skill literature` + 指标反推（旧 §3 因只认 `status=error` 对 literature **完全失明**）：

| 信号 | 实测次数 | 占比 | 性质 |
|---|---|---|---|
| `s3=false`（成功也未登记产物 URL） | 116 | 100% 的批量下载 | warning（不可回溯） |
| `ok==0 / total=N`（批量下载全失败） | 57 | 50.9% 的批量下载 | error |
| `ok < total`（漏抓链接） | 11+ | 9.8% 的批量下载 | warning |
| `hits_merged==0`（检索零命中） | 14 | 2.6% 的检索步 | error（用户拿空摘要） |

关键事实：**所有记录 `resultstr.status` 都是 `"ok"`**——即便 `ok==0` 或 `s3=false` 也回写成功，属**假成功**。这导致：
- 用户侧：下载实际失败却收到"完成"；
- 运维侧：取数工具误判"无错误"，无法定位真实故障。

---

## 1. P0 · 禁止假成功（重写 resultstr.status 判定）

**现状**（伪代码，Coze 端）：
```python
# 当前：无论实际成败，统一回写 status="ok"
resultstr = {"status": "ok", "ok": ok, "total": total, "s3": s3, ...}
```

**改为**（按实际成败分级）：
```python
def build_pdf_batch_resultstr(ok, total, s3_url, failed_links):
    if total and ok == 0:
        status = "error"                       # 全军覆没
    elif ok is not None and total is not None and ok < total:
        status = "warn"                        # 部分漏抓
    elif not s3_url:
        status = "warn"                        # 成功但无产物 URL
    else:
        status = "ok"
    return {
        "status": status,
        "ok": ok, "total": total,
        "s3": bool(s3_url),
        "s3_url": s3_url or None,              # 见 §2
        "failed_links": failed_links or [],     # 见 §3
        ...
    }
```

验收：`ok==0` 时 `status` 必须为 `error`；`ok<total` 或 `s3=false` 时必须为 `warn`，**不得**为 `ok`。

---

## 2. P0 · s3 产物 URL 必落库

**现状**：批量下载节点成功后 `s3` 字段恒为 `false`（116/116），"完成"不可回溯。

**改法**：下载成功后，把**稳定产物引用**写入 `resultstr.s3_url`（三选一，按现有基础设施）：
- 已上传 S3 → 填 S3 object key / 公开 URL；
- 仅本地落盘 → 填本地稳定路径或 manifest 引用（至少让后续审计能定位产物）；
- 大结果集外置 → 沿用 `batch_search_contract.md §3` 的 `{"s3_url": "...", "results": []}` 契约。

验收：凡 `status in ("ok","warn")` 且确有产物，`s3=true` 且 `s3_url` 非空。

---

## 3. P1 · 失败结构化字段（取代 notes 文本兜底）

`resultstr` 增补（便于 `feishu_log_fetch` / `auto_check` 量化，不再依赖解析 notes 文本）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `error_type` | string | `rate_limited` / `paywall` / `no_oa_link` / `timeout` / `parse_error` / `empty` |
| `error_code` | string? | 上游 HTTP/协议码（如 `429` / `403`） |
| `failed_links` | list[str] | 实际失败的链接列表（供重试/人工核查） |

`publisher_pdf_batch` 与 `literature_summary` 统一采用。

---

## 4. P1 · hits_merged==0 显式 warn + 兜底

**触发**：`literature_summary` 的 `hits_merged==0`（或本地 `querystr.zero_hits=true`，见 `ct_literature.py:1637` 已补）。

**Coze 端改法**：
```python
if hits_merged == 0:
    resultstr["status"] = "warn"
    resultstr["error_type"] = "empty"
    # 触发兜底：扩源 / 放宽年份 / 提示用户，而非静默返回空摘要
    trigger_fallback_or_notify(topic)
```

---

## 5. P2 · 重试 / 退避 / 超时（压长短尾）

实测批量下载 `runtime_sec`：p50=12.8s、p90=92.1s、max=274.9s——长尾多为超时后上游限流，反而加剧 §1 的 `ok==0`。

**改法**（批量下载节点内）：
- 单链接超时 `per_link_timeout=30s`；
- 重试 `max_retries=3`，指数退避 `backoff=2**attempt`（1s→2s→4s），遇 `429` 退避更久；
- 整批设置硬上限（如 `batch_cap=180s`），超时即收尾并如实回写 `ok/total` + `failed_links`，**不得**假装 `ok`。

---

## 6. P2 · 可观测性字段补齐

`resultstr` 增补（与 `feishu_log_fetch` §6、`auto_check` 对齐）：
- `skill_version` / `coze_version`：确保每一条都落（实测覆盖率非 100%）；
- `token_usage`：本次调用 token 消耗；
- `cache_hit`：是否命中缓存（配合本地 query 归一化，见 §7）；
- `answer_hash`：结果内容哈希，便于判重与回归。

---

## 7. P1 · call_type 双列落点

本地 `querystr` 已于 `ct_literature.py:1637` 补 `call_type="literature_summary"`；
Coze 端 `resultstr` 也**同步写入 `call_type`**（检索步 `literature_summary` / 批量 `publisher_pdf_batch`），
使取数工具两列都能区分两套 schema，避免 `auto_check_skill.py` 混算稀释统计。

---

## 8. 验收清单（Coze 端）

- [ ] `publisher_pdf_batch`：`ok==0` → `status=error`；`ok<total` 或 `s3=false` → `status=warn`
- [ ] 成功必有 `s3=true` + `s3_url`
- [ ] `resultstr` 含 `error_type` / `error_code` / `failed_links`
- [ ] `literature_summary`：`hits_merged==0` → `status=warn` + 兜底触发
- [ ] 批量下载含 per-link 超时 + 指数退避 + 整批硬上限
- [ ] `resultstr` 含 `skill_version` / `coze_version` / `token_usage` / `cache_hit` / `answer_hash`
- [ ] `resultstr.call_type` 与 `querystr.call_type` 一致

> 落地后，重新跑 `feishu_log_fetch.py --skill literature`，§3.5 的 `no_artifact` / `zero_fetch` /
> `partial_fetch` 计数应显著下降（说明假成功与 s3 漏登已修复），§3 的 `status=error/warn`
> 将首次真实反映 literature 的失败。

---

## 附录 A · 版本治理（P2，需 Coze 端确认）

实测 30 天窗口内 **72%（468/650）记录的 `skill_version` 为 1.4.7**，而本地代码已到
1.7.x。两种可能，需先定性再动作，**不可直接推定"灰度未铺开"**：

| 假设 | 判别方法 | 处置 |
|---|---|---|
| 多端点并存（旧端点仍在服务） | 比对 `query_origin` / `entry_point` 与版本交叉分布；查 Coze 工作流发布记录 | 收敛旧端点或显式标注版本来源 |
| 灰度未铺开 | 检查 Coze 发布版本与流量分配 | 推动全量，并在 `resultstr.coze_version` 落真实版本 |

**要求**：Coze 端每条 `resultstr` 必写 `skill_version` / `coze_version`（当前覆盖率非 100%），
否则无法把 §1–§7 的修复归因到具体版本、也无法验证修复是否真正生效。

## 附录 B · 缓存跨运行（本地侧已修，Coze 端知悉）

本地 `scripts/ct_literature.py` + `adapters/search_cache.py` 已于 2026-11-13 修复：
缓存文件从「每次唯一的 `<out_dir>/.search_cache.json`」提升到用户级共享目录，
`_SCHEMA` 升 v2 作废旧键。实测 534 条检索汇总中 **98.9% 调用落在同一精确 topic
的重复簇**，此前因作用域问题全部白跑全链路。

- 无损归一仅合并大小写/标点/功能词变体（实测 215→214 唯一 topic，收益有限）；
- **语义同义不自动合并**：`omega-3 for depression in adults`(20) 与
  `omega-3 fatty acids for depression in adults`(8) 属同义但措辞不同，自动合并会
  让临床检索命中错误缓存、返回错误文献集；该类判断须交 LLM/人工，或由用户在
  入口层显式复用同一检索式。

**Coze 端可选配合**：若云端检索节点自身有独立缓存，请确认其键同样包含
`(source, 翻英后检索式, 年份/日期窗口, max_results, cochrane)` 全参数，
避免不同参数命中同一缓存（与本地 v2 口径一致）。

