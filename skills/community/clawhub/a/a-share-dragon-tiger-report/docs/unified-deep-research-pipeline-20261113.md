# 统一深度投研报告流水线 v4.0.2 · 2026-11-13 实跑基线

> 同步日期：2026-11-14　｜　发行版本：v4.0.5（4.0.4 引入四阶段流水线，4.0.5 安全加固）
> 同步目标：GitHub `yjkj999999/a-share-dragon-tiger-strategy`、ClawHub `a-share-dragon-tiger-report`、WorkBuddy 定时任务 `f0c0c53b-c8b3-4830-821f-f13c7ba32c44`
> 生成器：GitHub [`templates/unified/`](https://github.com/yjkj999999/a-share-dragon-tiger-strategy/tree/main/templates/unified)　｜　样本：[HTML](https://github.com/yjkj999999/a-share-dragon-tiger-strategy/blob/main/docs/unified-report-20261113.html) · [PDF](https://github.com/yjkj999999/a-share-dragon-tiger-strategy/blob/main/docs/unified-report-20261113.pdf)
> SOP 权威文本：`SKILL.md` **§18.12**

## 一、合并口径

原三条独立定时任务（18:00 主研判 / 19:15 预判核验 / 20:30 五大战法）合并为**一次触发、四阶段顺序执行、一份主交付**。三份原规格降级为内部取数与判定阶段，不再作为并列最终交付物。判定内核、四层漏斗、冻结阈值、情绪闸门六项阈值、W1–W5 定级、五条铁律、20 页 BII 页数机**一字未改**。

| 阶段 | 参考脚本 | 产物 |
|---|---|---|
| A 主研判 | `assemble_v4.py` | `data.json`（v4.0 / `selection_mode=limitup` / 三层旁路 14+23+25）、`predictions.json`、BII 双栏 20 页 HTML/PDF |
| B T−1 核验 | `build_verify.py` | `预判核验-由20261111报告.md / .csv`（原目录镜像，md5 一致） |
| C 五大战法 | `build_tactics.py` | 10 章单文件 HTML（11 内联 SVG） |
| D 统一报告 | `build_unified.py` + `charts.py` | **唯一主交付**：57 页 A4 PDF / 64 内联 SVG / 31 表 / 0 外部依赖 |

阶段 D 渲染：Chrome `--headless=new --no-pdf-header-footer --print-to-pdf=... --virtual-time-budget=90000 file://<URL 编码路径>`；交付前三重校验（HTMLParser 标签开合与外链、`pdfinfo`/`pdftotext -layout`/PyMuPDF 空白页与图号全命中、`pdftoppm` 目视抽查封面 / 图表密集页 / 表格密集页 / 末页）。

## 二、2026-11-13 实跑真值（仅作结构示例，禁止沿用为当期数据）

- **一句话定性**：广度崩塌 · 冰点日。上证 3634.35（−0.59%）、创业板 −3.32%；涨 765 / 跌 4748，上涨占比 13.71%；涨停 38 / 跌停 39；两市成交 16,556.68 亿。
- **四层漏斗**：L0 849 → L1 10/31 → L2 51 → L2.5 剔除 5 → L3 否决 38 → **过会 8 只**。
- **α 预算（7 亿机构口径，仅参考）**：上限 2.10 亿，阶段 II 已用 27.3%，剩余 1894.39 万；与 ¥100,000 实盘纪律分层隔离。
- **两套闸门**：冻结闸门覆盖 15/38 = 39.5%（`validate()` issues=0、自检 8/8）→ 部分覆盖；情绪闸门六项全数否决 → 实盘取更保守者，总仓位 ≤15%（¥15,000），条件 C 已满足，预备 0%。
- **五条预判**：目标日 2026-11-16，状态「登记·未核」，当期不可核验、未倒填命中率。
- **阶段 B 链路**：11-12 未产出主研判报告（如实登记缺口、不编造），回退补核 11-11 报告（目标日 11-12）：命中 2 / 未命中 2 / 不可核验 1，口径 A 40% / 口径 B 50%。
- **数据缺口**：21 类，见报告附录 B。
- **三重校验**：HTML 标签 0 错 / 0 外部依赖 / 64 图号唯一；PDF 57 页 A4、0 空白页、0 页眉残留、64 图号全命中；目视抽查通过。

## 三、口径修正：三链 5 / 20 日净额

`report_context.json` 的 `chain_d5 = +118.88 亿`、`chain_d20 = −318.66 亿` 只汇总了含 `d5` 子键的通信设备与半导体，**漏计元件分项**（5 日 −5.09 亿 / 20 日 −368.9 亿）。统一报告改用三链 `today_out.d5_yi / d20_yi` 全量求和：

| 口径 | 5 日 | 20 日 |
|---|---|---|
| 原落盘字段（两链） | +118.88 亿 | −318.66 亿 |
| **三链全量求和（采用）** | **+113.79 亿** | **−687.56 亿** |

差异已写入报告附录 B 与 `report_context.json` 的 `gaps`；两种口径下 20 日均为负，方向结论不变。

## 四、已实证的坑

| 现象 | 根因 | 修法 |
|---|---|---|
| 涨停源主池数量虚高 / 同股重复 | 龙虎榜同股多上榜原因被拆成多行 | 按股票代码聚合 `netBuyAmount`；准涨停单列 `watch`，不伪造成涨停 |
| 长表整表在 PDF 丢失、只剩表题 | `table` / `.card` 设了 `break-inside:avoid` | `table{break-inside:auto}` + `tr{break-inside:avoid}` + `thead{display:table-header-group}` |
| `heat_matrix(fmt="%.1f")` 报 `'str' object is not callable` | `fmt` 期待可调用对象 | 改 `fmt=lambda v: f"{v:.1f}"` |
| 市场概览为 T-1 滞后、分表为空 | 旧缓存未标注基准日 | westock `data_market_overview(date=报告日,type=all)` 实取并落盘 `raw/market_overview_YYYYMMDD.json` |
| 中文文件名 PDF 渲染失败 | `file://` 路径未转义 | `urllib.parse.quote` 后再拼 `file://` |

## 五、三处同步落点

| 目标 | 落点 |
|---|---|
| GitHub | `templates/unified/`（四脚本 + `charts.py` + 示例 JSON + README）、`docs/unified-report-20261113.html / .pdf`、`docs/unified-deep-research-20261113.md`；`skill/SKILL.md` 由旧短版同步为 v4.0.4 全量版并修正 homepage |
| ClawHub | slug `a-share-dragon-tiger-report`：**4.0.4**（§18.12 + 本文档 + README 修正）服务端已创建但公开版本列表暂未展示，疑为安全复核暂挂；**4.0.5** 在其基础上补 §18.13 权限边界、移除安装脚本 `rsync --delete`、示例数据快照化 |
| WorkBuddy 定时任务 | `f0c0c53b-c8b3-4830-821f-f13c7ba32c44` 阶段 D 参考实现改指向 `dragon-tiger-20261113/unified/build_unified.py` + `charts.py`，补入「实现基线与幂等」段落；跨阶段纪律九条不变；**状态保持 PAUSED，未擅自启用** |

> ClawHub 远端 4.0.3 版本级安全扫描结论为 `status=suspicious / hasWarnings=true / 73 issues / DO_NOT_INSTALL`，
> LLM 复核点名四项：安装脚本 `rsync --delete` 可能删除目标目录独有文件、固定 GitHub 远端整包发布超出报告生成范围、
> 未声明工具权限边界、示例硬编码数据可能被当作当期真值。4.0.5 已逐条处理：安装改为备份后逐文件覆盖、
> §18.13 显式声明权限边界、`templates/unified/*.example.json` 与样本报告标注为快照、发布命令明确为人工运维动作。
> 技能卡「Known Risks and Mitigations」同步登记。新版本能否解除标记由平台复核决定，本次**未绕过扫描、未删除任何风险说明**。

## 六、纪律与免责

本金 ¥100,000（2026-11-13 由 ¥7,000 变更）只改绝对金额；比例纪律、情绪闸门六项阈值、分母失真规则、W1–W5 定级、五条铁律、两套闸门分别判定原则不变。三层只读旁路无决策权，7+3 投行量化穿透字段一律标「数据缺口·待核」。跨市场 / 跨期数据逐项标注基准日，基准日不一致只做方向与结构比较。

> 本报告基于公开数据生成，属研究框架与决策辅助工具，不构成投资建议、收益承诺或操作指令；历史数据不代表未来表现。

---
**Author**：Wang Dongjie 王东杰 · Wdj_@163.com
