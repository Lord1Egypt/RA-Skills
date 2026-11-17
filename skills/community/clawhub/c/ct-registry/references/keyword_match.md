# 关键字匹配优化与菜单 / Keyword Matching — Optimization & Menu
> 经验固化自 2026-07-28 实网检索「沙坦类 · 高血压 · 近 5 年」时暴露的反复试错问题。
> 配套探针: `ct_sartan_htn_2021_2026/keyword_probe/probe_keywords.py` + `probe_report.md`。
> 实现: `ct-base/scripts/kw_localize.py` (`localize` / `kw_match_candidates` / `render_kw_menu`)。

---

## 1. 为什么需要这套规则 / Why
两个 Coze 端点（WHO `source=who`、中国 CDE `source=chinadrugtrials`）的**关键字匹配语义完全不同**，
且都不支持「药物类别通配」。直接投「类别词 / 英文」会静默漏检，逼着 Agent 反复试错。
本文件把实测行为固化成**可复用的匹配规则 + 关键字匹配菜单**，让非标准关键字的解析变成
一次「菜单选择」而非反复猜测（呼应 ct-base §8「未找到结果，您是否想检索：{suggestion}？」）。

---

## 2. 实测匹配语义 / Empirical Matching Semantics
| 端点 | 匹配方式 | 类别词(裸后缀) | 缩写/全称 | 具体药名 | 英文投中文库 |
|---|---|---|---|---|---|
| **WHO** `source=who` | 英文标题/字段精确 | `sartan`=6（加 5 年窗→0） | `ARB`=604 / `angiotensin receptor blocker`=353 | `valsartan`=1243 / `losartan`=729 | 不适用 |
| **中国 CDE** `source=chinadrugtrials` | 中文子串 | `沙坦`=788（`沙坦类`=0） | `ARB`=121 | `缬沙坦`=248 | `sartan`=10 / `valsartan`=0 |

结构化字段（仅 WHO）：`who_intervention=sartan`=0，但 `=valsartan`=454 —— **结构化须填具体药名**。

---

## 3. 优化规则 / Optimization Rules
1. **类别词不要裸投后缀**。
   - WHO：用缩写 `ARB` 或全称 `angiotensin receptor blocker`，或**枚举具体成员**（valsartan+losartan+…）。
   - CDE：用中文类别后缀 `沙坦`；**务必去掉「类」**（`沙坦类`=0）。
2. **CDE 必须译中文**：英文 `sartan`=10 / `valsartan`=0，译中文 `沙坦`=788。
   技能已对 CDE 路径自动 `localize→zh`（含药名/类别词扩展表），英文关键词不再裸投中文库。
3. **日期过滤很严格**：WHO 裸 `sartan` 加 5 年窗→0；5 年窗内可靠路径是**枚举具体药名**（每药独立带日期过滤）。
4. **WHO 结构化字段须填具体药名**：`intervention=<类别>`=0，`=<具体药名>` 有结果。
5. **跨源桥梁词**：`ARB` 在 WHO(604)/CDE(121) 都有效，可作单一类别词；但中文后缀 + 英文具体名在覆盖度/精度上仍胜出。
6. **宽松 AND**：CDE `multi_keyword`「高血压 沙坦」=730（子串宽松 AND），适合一次性收窄。

---

## 4. 关键字匹配菜单 / Keyword-Matching Menu (ct-base §8)
当关键字**非标准 / 未命中术语表 / 是类别词**时，调用 `kw_localize.kw_match_candidates(text, source)`
生成候选解释菜单，由用户选择，避免 Agent 静默试错：

```python
from kw_localize import kw_match_candidates, render_kw_menu
cands = kw_match_candidates("sartan", "cde")   # source=None 时给全策略
print(render_kw_menu("sartan", cands))
```

候选策略（`strategy` 字段）：
| 策略 | 含义 | 适用 |
|---|---|---|
| `as_is` | 直接用原文 | 兜底，可能漏检 |
| `translate` | 术语表/扩展词库翻译（zh↔en） | 通用 |
| `class_suffix` | 类别词→中文类名后缀（如 sartan→沙坦） | **CDE 子串匹配首选** |
| `enumerate` | 枚举类别具体成员（如 9 个 ARB 英文名） | **WHO 精确药名首选** |
| `structured` | WHO 结构化 condition+intervention 字段 | WHO 仅具体成员有效 |

`ct_registry.py` 已接入：
- **CDE 路径**：`localize(base,"zh")` 命中 `term_map` 直接用；`miss`（英文无法译中文）时
  打印 `render_kw_menu` 并 STOP（除非 `--auto-confirm` 自动采用 `translate`/`class_suffix`）。
- **CT.gov 确认门**：外文词未命中术语表时，除建议译文外也打印候选菜单。

---

## 5. 如何扩展词表 / Extending the Maps
- **中英术语**：编辑 `ct-base/references/term_map.json`（zh→en，~190+ 条，自动反向建立 en→zh）。
- **药物类别后缀**：编辑 `kw_localize.py` 的 `_CLASS_EN2ZH`（英文类别 token → 中文后缀，
  如 `sartan→沙坦`）；反向 `_CLASS_ZH2EN` 自动生成。
- **具体药名**：编辑 `_DRUG_EN2ZH`（英文具体药名 → 中文）；成员枚举在 `_CLASS_MEMBERS`。
- 三条表都会经 `localize()` 的 `term_map` 路径命中，并经 `kw_match_candidates()` 暴露为菜单候选。
- 设计约束（ct- 哲学）：**本地优先、离线**，不调用在线翻译 API；`_EXTRA`/`_CLASS`/`_DRUG`
  仅作保守安全网，拿不准的词返回 `None` 交由 Agent/用户补充。
