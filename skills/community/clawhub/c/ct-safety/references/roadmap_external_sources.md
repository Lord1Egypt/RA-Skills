# 规划中数据源 — T1 三件套（加 / 日 / 澳）

> **状态：规划中，未实现。** 2026-09-01 用户决定暂缓接入，先把可行性结论与架构决策落到文档，未来再实现。
> 代码骨架 `scripts/fetch_canada.py` 已创建（header 自适应 alias 解析），但因无数据未验证、未接入引擎。

---

## 一、为什么是这三个（价值排序，实测 2026-09-01）

当前 ct-safety 已覆盖：FAERS / FDA Label / DailyMed / RxClass / openFDA Enforcement（全美国源）+ cdr-adr.org.cn（中国）+ drugoffice.gov.hk（香港，Coze 节点已写待部署）。
**国外尚未实现**：欧盟 EMA、英国 MHRA、澳大利亚 TGA、加拿大 Health Canada、日本 PMDA、WHO/UMC。

选 T1 三件套的理由（价值 = 报告体量 × 人群多样性 × 可否做失配比）：

| 源 | 访问模型 | 体量（核实） | 可程序化 | 对 ct-safety 的增量价值 |
|---|---|---|---|---|
| **Health Canada（加）** | 开放数据门户整库下载 | ZIP 299 MB（实际 313,578,432 B），含 demo/drug/reac/outc/link/ther 等 11+ 表 ASCII | ✅ Open Government Licence，完全开放 | 第二个**独立北美**报告流 → 交叉验证 FAERS、抵消美国报告偏倚 |
| **PMDA JADER（日）** | 整库 4 表 CSV，但下载页有图片验证码 | demo/drug/reac/hist，~96 万例（2004–） | ⚠️ 公开但 `CsvDownload.jsp` 含 `captchaText`；需浏览器/Coze 通道或手动落盘 | **亚洲人群遗传学差异**（如 HLA 相关 DILI、卡马西平 SJS）→ 最能补 FAERS 短板 |
| **TGA DAEN（澳）** | **非整库**，微软 Power Pages (Dataverse) 后端 Web 应用 | 按药名检索，导出上限 15 万行 xlsx / 3 万行 csv | ⚠️ 无官方公开 API（需逆向 Power Pages 匿名 Web API 端点，常受 WAF/CORS 限制） | 大洋洲人群；体量最小(~40–50万)、价值最低，**不建议优先** |

> 未入选（本轮评估）：WHO VigiBase（公共 VigiAccess 仅汇总、无 2×2、无批量；VigiLyze 仅限 PIDM 成员国机构——中国 1998 已加入，或可经 NMPA/CDR 拿权限，若有则是量级碾压 4000 万，优先级置顶）；EudraVigilance（>3100 万，但仅门户 line listing 无干净 API，自动化=门户爬取，成本高）；MHRA（脱欧后独立、与 EudraVigilance 重叠高，边际价值低）。

---

## 二、关键纠正（推翻前期 Blocked 表错误结论）

SKILL.md `### Blocked / excluded sources` 第 110 行原记 **"Health Canada — 本机不可达（health-products.canada.ca API 连续 ReadTimeout）"** 是**测错端点**的结论，已推翻：

- ❌ 旧结论针对的是 `health-products.canada.ca` 的 **Canada Vigilance Online 网页 API**（确实 ReadTimeout）。
- ✅ 实际可用通道是 **`open.canada.ca` CKAN 开放数据门户**（dataset `9cbaef00-b52c-4a70-9fed-d9aa8263ab74`），提供**整库 ZIP 下载**，Open Government Licence，本机直连可达。
- 实测（2026-09-01）：沙箱需 `dangerouslyDisableSandbox:true` 才放行进网；连通后 API 正常返回，下载 URL 有效，文件 313,578,432 B。下载本身可行，只是**本机→open.canada.ca 带宽仅 ~41 KB/s**，299 MB 全量需 ~2 小时。

→ Health Canada 不应再列在"不可达"里，已移至本规划文档并标注"可整库下载，规划中"。

PMDA JADER 验证码确认属实，但前期 Blocked 表漏记"可经浏览器/Coze 通道或手动落盘整库 4 表 CSV 绕过"——也已补入本规划。

---

## 三、架构决策（已定，待实现时落地）

| 源类型 | 归属 | 理由 |
|---|---|---|
| 批量源（Canada / Japan） | **本地批量入库** | 整库文件物化到本地磁盘（放 skill 包外 `CT_SAFETY_DATA_DIR`，默认 `~/ct-safety-data`），解析→建全局 2×2 索引→喂现有 PRR/ROR/IC/EBGM 引擎。Coze `/run` 是无状态请求-响应、无持久化 GB 级存储、其 RAG 知识库给不了精确计数，故**批量源不能上 Coze**。不依赖 Coze 部署，守住发布红线。 |
| 实时检索源（TGA DAEN） | **Power Pages / Dataverse 后端，无官方 API** | TGA 是 Power Pages 站点（非官方 API），归实时检索源但**不能直接套 FAERS 适配器**：需逆向其匿名 Web API 端点（实体名未知），且本机直连受 WAF/CORS 风险高；被拦则外发 Coze（新建 `tga_node`，**成本高于 FAERS**，且触发部署红线）。 |

> 这与用户"所有 safety 检索外发 Coze"指令**不冲突**——该指令针对*实时检索*；批量入库+重本地计算是另一类，本就本地运行。

**调用点零改动**：复用 `FaersShim` 同款垫片/注册模式。批量源适配器提供 `fetch_counts(drug, event) -> result dict`，`result` 含 `source` + `drug_total`/`grand_total`/`event_total` + `counts={a,b,c,d,...}`，失配比引擎（PRR/ROR/IC/EBGM）零改动复用。

---

## 四、环境坑（未来实现必看，已实测）

1. **沙箱拦出网**：本环境 Bash 默认沙箱会阻断出网（curl 无输出即死）。下载/外网请求需 `dangerouslyDisableSandbox:true`。
2. **curl `-o` 写盘报 `(23) client returned ERROR on write of 16384 bytes`**：本环境 curl 写文件会失败，但管道到 stdout 正常。解决：用 **shell 重定向** `curl ... > file`（已验证通过），不要 `-o file` / `-o /dev/null`。
3. **带宽**：本机→open.canada.ca ~41 KB/s，299 MB 需 ~2 小时。建议后台跑（`run_in_background`）或手动在高速网络落盘后拷入 `CT_SAFETY_DATA_DIR/canada/`。

---

## 五、未来实现步骤（checklist）

### Health Canada（最优先，真·整库）
1. 下载 `https://open.canada.ca/data/dataset/9cbaef00-b52c-4a70-9fed-d9aa8263ab74/resource/2e736909-ef1f-4d60-bfb6-f15b3be3b1fa/download/extract_extrait.zip`（299 MB）→ `CT_SAFETY_DATA_DIR/canada/`。
2. 解压，看真实字段：分隔符是 **`$` 且字段带引号**（非 FAERS 的管道符）；确认 report-id 连接键、`DRUGNAME`/`ACTIVE_INGREDIENT`/`ROLE_COD`（药角色：疑似/合并/相互作用及其编码）、`PT_NAME`/`REAC_OD`（MedDRA 反应术语）。
3. 完善 `scripts/fetch_canada.py`：流式解析 11 表 → 按 caseid 聚合「疑似药物集合 + 反应集合」→ 建全局索引（N_total、每药 case 数、每反应 case 数、药×反应 case 数）→ `fetch_counts` 返回**同构 FAERS dict**。
4. `ct_safety.py` 加 `--source canada`，失配比引擎零改动。
5. 已知药（如 二甲双胍）自测 → 同步 SKILL.md 数据源表 + CHANGELOG（version bump）。

### PMDA JADER（价值最高，人种多样性）
1. 浏览器/Coze 通道过 `CsvDownload.jsp` 验证码 → 落盘 4 表 CSV（demo/drug/reac/hist）→ `CT_SAFETY_DATA_DIR/jader/`。
2. 解析四表，按 caseid 聚合疑似药物+反应 → 同构 2×2 接入。

### TGA DAEN（实时检索，但为 Power Pages / Dataverse 后端，**非**官方 API）
1. 探明 `daen.tga.gov.au` 的 Power Pages 匿名 Web API（Dataverse OData 实体端点，需逆向实体名）；评估 WAF/CORS/匿名权限。
2. **不可直接套 `fetch_faers`**（FAERS 有 openFDA 官方 API，TGA 没有）；若本机可达则写定制实时检索适配器；被 WAF/地域拦则外发 Coze（需新建 `tga_node` 并部署，发布红线）。

---

## 六、复用接口契约（来自 fetch_faers.fetch_counts）

```python
# 返回 result dict，加拿大/日本适配器需返回同构结构，引擎零改动复用：
result = {
    "source": "HEALTH_CANADA",          # 或 "PMDA_JADER"
    "drug_total": ...,                  # 含该药的报告数
    "grand_total": ...,                 # 全库报告数 N
    "event_total": ...,                 # 含该事件的报告数
    "counts": {
        "a": drug_event_pairs,          # 药 × 事件
        "b": drug_minus_a,              # 药 − a
        "c": event_minus_a,             # 事件 − a
        "d": grand_total - a - b - c,   # 其余
        # ... 其他引擎所需字段同 FAERS
    },
}
```
