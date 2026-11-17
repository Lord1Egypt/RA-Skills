# PROSPERO API 访问申请与对接指南

> 适用范围：ct-literature 技能 P1 升级（PROSPERO 注册检索）的收口依据
> 整理时间：2026-08-12
> 维护人：小龙（Wintone AI 伙伴）
> **决策（2026-08-12）**：PROSPERO 维持「保留接口 / reserved source」定位 — 默认降级跳过、不主动申请 token、不转正。本指南作为将来若需启用的申请参考保留。

---

## 0. 结论先行（TL;DR）

1. **PROSPERO 官方 REST API 已经加了鉴权网关。** 现在任何对 `/api/` 端点的请求，无论是否带 token，都会被前置网关拦截并返回 `{"status":"error","errormessage":"Error code: header value undefined"}`。
2. **正确的鉴权 header 名没有在任何公开文档里出现。** 我们试过 `User-Agent`、`PROSPERO-TOKEN`、`PROSPERO-ACCESS-TOKEN`、`X-API-KEY` 全部无效。
3. **不存在公开的"申请 API key"表单。** PROSPERO 主站只有"注册系统评价"的流程，没有"申请 API 访问"的页面。
4. **当前最优解**：把 PROSPERO 在 ct-literature 里保持为 **UNVERIFIED 降级源**（无 token 时优雅跳过，不声称可用），等拿到官方认可的 header 名 + token 再转正。
5. 如果你其实想问"怎么注册一个 PROSPERO 账号/注册自己的系统评价"——那是另一套免费标准流程，见文末附录，与 API 访问是两件事。

---

## 1. 真实探测证据（2026-08-12 实测）

三个 case 全部返回**相同的错误体、相同的 ETag**，说明是同一道网关在拦所有 `/api/` 请求，而不是路径或大小写问题：

```
=== A. 小写路径 /prospero/api/search/ ===
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
X-Powered-By: Express
Access-Control-Allow-Origin: *
X-Powered-By: ARR/3.0
ETag: W/"4b-Q35T1btJfnfTn7nlWLtPp9x6qB4"
{"status" : "error", "errormessage" : "Error code: header value undefined"}

=== B. 大写路径 /PROSPERO/api/search/ ===
ETag: W/"4b-Q35T1btJfnfTn7nlWLtPp9x6qB4"   （与 A 完全相同）
{"status" : "error", "errormessage" : "Error code: header value undefined"}

=== C. 大写路径 + 试带 PROSPERO-ACCESS-TOKEN: test ===
ETag: W/"4b-Q35T1btJfnfTn7nlWLtPp9x6qB4"   （与 A/B 完全相同）
{"status" : "error", "errormessage" : "Error code: header value undefined"}
```

**关键推断**：
- 后端是 Express（`X-Powered-By: Express`），前面挂了 IIS 的 ARR/3.0 反向代理（`X-Powered-By: ARR/3.0`）。
- `Error code: header value undefined` 是 Express 应用层抛的——代码读了某个**固定 header 名**，但取到的值是 `undefined`（即"你没传我要的那个 header"）。我们传的 `PROSPERO-ACCESS-TOKEN` 它根本没读，所以还是 undefined。
- ETag 恒定 → 不是后端业务在判断，是**网关层统一拒绝**，所有 `/api/` 调用目前都进不去。

---

## 2. 鉴权机制真相（基于第三方逆向 + 服务器指纹）

社区项目 **PROSPERO-MCP**（himcp.ai / glama.ai 可查）是目前唯一公开对接过 PROSPERO 自动化接口的实现，它暴露的线索：

| 环境变量 | 说明 |
|---|---|
| `PROSPERO_BASE_URL` | 默认 `https://www.crd.york.ac.uk/PROSPERO/api/` |
| `PROSPERO_ACCESS_TOKEN` | 可选，默认空串 |
| `PROSPERO_AUTH_TOKEN` | 可选，默认每请求用时间戳动态生成 |
| `PROSPERO_USER_DATA_DIR` | 持久化 Chrome/Edge profile，用于 PROSPERO 网站登录 |

它的 **setup 流程（`npm run setup:prospero`）是用浏览器打开 PROSPERO 做网站登录（website login）**，再校验 public / authenticated 访问。

**这意味着什么**：
- PROSPERO 的"令牌"很可能来自**登录网站后的 session**，不是独立申请的 API key。
- PROSPERO-MCP 的公开发现工具（`prospero_search_protocols` 等）底层大概率是**scrape 公开 HTML 页面**（`view_record` 的文档原话就是 "fetch and parse the full public PROSPERO record page by accession number"），而非纯 REST 调用——因为纯 REST 现在被网关挡死了。
- 换句话说，连第三方都没拿到"官方 API 文档"，大家都在试错或降级到页面爬取。

---

## 3. 拿到 PROSPERO 数据的三条路径（对比）

| 路径 | 做法 | 可行性 | 对 ct-literature 的适配成本 | 风险评估 |
|---|---|---|---|---|
| **A. 申请官方 API 访问** | 联系 CRD/York，说明用途，索取 header 名 + token | 最正统，但无公开表单，需邮件沟通，周期不确定 | 拿到后只需在 `fetch_prospero.py` 接上 header 名即可转正 | 低；合规、稳定、可溯源（反幻觉策略友好） |
| **B. 账号登录 + session 调** | 注册免费账号，浏览器登录取 session/cookie，再调 `/api/` | 不确定能绕过网关（网关可能仍要特定 header） | 需引入浏览器/登录态管理，偏离"纯 API、零浏览器"设计 | 中；session 易失效，运维重 |
| **C. 直接 scrape 公开页** | 不走 `/api/`，解析 `crd.york.ac.uk/PROSPERO/` 网站搜索结果 HTML | 现在可用（公开页无需 token） | 需新增 `fetch_prospero_scrape.py` + HTML 解析器，且 HTML 结构会变 | 高；非结构化、脆弱、违反反幻觉/结构化契约 |

**我的建议**：优先走 **A**，B 作为备选，C 不推荐（除非官方接口长期不可用且你确实急需）。

---

## 4. 申请官方 API 访问的具体步骤（路径 A）

PROSPERO 由 **University of York · Centre for Reviews and Dissemination (CRD)** 运营，受 NIHR 资助。官方没有公开 API 申请页，标准做法是走网站的 **Contact / Help** 表单或支持渠道说明需求。

### 4.1 操作清单
1. 打开 PROSPERO 主站：https://www.crd.york.ac.uk/PROSPERO/
2. 滚到底部找 **Contact us / Help / Enquiries** 入口（通常是表单或邮箱）。
3. 说明你是做系统评价的文献检索自动化，请求 API 程序化访问权限（一个 API token 或正确的 Authorization header 规范）。
4. 重点强调：**合规用途、仅检索公开注册记录、不写不爬、用于科研文献聚合**。
5. 等 CRD 回复，拿到两样东西：
   - 正确的 **header 名**（如 `PROSPERO-ACCESS-TOKEN` 或别的）
   - 你的 **token 值**
6. 把这两样发给我，我立刻在 `fetch_prospero.py` 接上、去掉降级、把源从 UNVERIFIED 转正，并补一段 `tests/scenario` 真实验证（用你的 token 跑一次 `--with-prospero`）。

### 4.2 邮件/表单模板（中英文）

**中文版**
```
主题：申请 PROSPERO REST API 程序化访问权限

尊敬 PROSPERO 团队：

我是[机构/姓名]，正在开发一套面向系统评价（systematic review）的
文献检索自动化工具（ct-literature）。该工具聚合 OpenAlex、Europe PMC 等
公开学术源，希望把 PROSPERO 注册库作为系统评价协议（protocol）的检索补充。

我们注意到 PROSPERO 的 REST API（/PROSPERO/api/）当前要求一个 Authorization
header，但未在公开文档中说明具体名称与申请方式。恳请告知：
  1) 程序化访问所需的 API token 申请流程；
  2) 请求时应使用的 header 名称与格式。

用途说明：仅检索公开注册记录、只读、不写入、不批量爬取，用于科研文献聚合与去重。
如需要可签署使用条款或提供机构信息。

期待回复，谢谢。
```

**English version**
```
Subject: Request for PROSPERO REST API programmatic access

Dear PROSPERO team,

I am [name/institution] building ct-literature, a tool that aggregates public
scholarly sources (OpenAlex, Europe PMC, etc.) for systematic-review literature
retrieval. We would like to include PROSPERO as a supplementary source for
registered review protocols.

We observed that the PROSPERO REST API (/PROSPERO/api/) now requires an
Authorization header, but the exact header name and the token-issuance process
are not documented publicly. Could you please advise:
  1) how to apply for a programmatic-access API token;
  2) the exact request header name/format to use.

Use case: read-only retrieval of public registry records, no writes, no bulk
scraping — for research literature aggregation and de-duplication. We are happy
to provide institutional details or accept usage terms if needed.

Looking forward to your reply. Thank you.
```

---

## 5. 对接 ct-literature 的落地状态与下一步

**当前代码状态（v0.6.0）**
- `scripts/fetch_prospero.py`：已实现，结构化为 unified schema（`type="systematic-review-protocol"`、`source="PROSPERO"`、`prospero_status`）。
- 鉴权模型：**key-gated 优雅跳过**。无 token 时 `fetch()` 返回 `None` 并 WARN，不写文件、不声称可用（同 Semantic Scholar 无 key 行为）。
- CLI：`--with-prospero` / `--prospero-token` / `--prospero-header`，已接线到 `run()`。
- 源在 SKILL.md / README / CHANGELOG 中标注为 **UNVERIFIED**。

**你拿到 header 名 + token 后，我做的三件事**
1. 在 `fetch_prospero.py` 把 `DEFAULT_HEADER` 改成官方名，去掉降级分支，改为真实请求。
2. 跑一次真实 `--with-prospero` 端到端，复核 `_parse_response()` 的 JSON/XML 双解析器（当前是 best-effort stub，需真数据校准字段映射）。
3. 把 SKILL.md / README 的 PROSPERO 标签从 UNVERIFIED 改为已验证可用，bump 到 0.6.1。

---

## 6. 附录：如果你其实是想"注册自己的系统评价"

这与"API 访问"是两件事。PROSPERO 注册**免费、公开、标准**：

1. **注册账号**：https://www.crd.york.ac.uk/PROSPERO/#joinuppage
2. **资格问卷**：回答系统会判断你的研究是否符合 PROSPERO 注册标准（系统评价/快速评价/伞评价/诊断准确性/预后/方法学评价可注册；**Scoping review 不可注册**）。
3. **填写注册表**：在线填结构化字段（PICO、纳入排除、检索策略、合成方法、团队/资助/利益冲突、预计起止时间、通讯作者）。
4. **审核**：CRD 编辑审核，通过后发 **CRD 编号**（如 `CRD420251181863`）——期刊/审稿人用它核对"发表的方案是否和注册一致"。
5. **时限**：方案确定后、最好文献筛选前注册；最晚数据提取完成前仍可审。**已完成的系统评价不接受注册**。
6. **费用**：免费。Cochrane 评价不应单独在 PROSPERO 注册。

> 提示：注册前先在 PROSPERO 搜一遍同名主题，避免重复（这正是我们做 API 检索的初衷之一）。

---

## 7. 参考链接
- PROSPERO 主站：https://www.crd.york.ac.uk/PROSPERO/
- 注册入口：https://www.crd.york.ac.uk/PROSPERO/#joinuppage
- PROSPERO-MCP（社区逆向参考）：https://himcp.ai/server/prospero-mcp
- ct-literature 代码：`scripts/fetch_prospero.py`（`fetch()` / `_parse_response` / `_map_review`）
