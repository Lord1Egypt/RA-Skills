# Published Application (ct-safety workbench)

> 本文件是 **部署 / 重发布操作的单一事实源**（2026-11-08 建立）。执行任何 deploy / re-publish 前先加载本文件。
> 建立动因：此前「最近一次发布」只写在 `SKILL.md` 的一句正文里，与 `CHANGELOG.md` 的多条
> 「线上仍待重新部署」长期冲突；页脚版本又另有 6 处锚点，没有一张对照表。
> 与 `ct-registry` / `ct-literature` 的同名文件对齐（三技能统一）。

## Registry

| Item | Value |
|---|---|
| Share link | `https://ct-safety.app.workbuddy.host/` |
| appId | `wbapp_GyOm0cdJ1qHoaQxlFZOVwl` |
| domainPrefix | `ct-safety` |
| **Publish bundle** | **`workbench/publish/`** — `build_publish.py:26` 的 `DST = WORKBENCH / "publish"`；与 `app.config.json` 一致（本技能**没有** `publish-dist`） |
| Publish infra | `workbench/publish-kit/` — `.wbapp_*.genie` 标记 + `install_genie.py` + `build_publish.py` |
| Ownership marker | `workbench/publish-kit/.wbapp_GyOm0cdJ1qHoaQxlFZOVwl.genie` |
| Deployed as | Python HTTP service（`workbench/app.py` → `workbench/server.py`，`PORT` 默认 8791） |
| Backend | `GET /api/config /api/health /api/localize /api/runs /api/source-health /api/task/<id> /api/download`；`POST /api/search /api/bug-report /api/run-delete` |
| Deploy metadata | `workbench/app.config.json` |
| **Last deployed** | ⚠️ **线上版本未核实**。`SKILL.md` 旧文自陈 `2026-09-26`，但 `CHANGELOG.md` v0.10.6 / v0.10.7 标「线上应用仍待重新部署」。部署后必须回写本行并补 `app.config.json` 的 `deployedAt`。 |

> **本技能没有犯 ct-registry 的错**：`publishDir` 在 SKILL.md、构建脚本、`app.config.json` 三处都是
> `workbench/publish`。ct-literature 用 `publish-dist` 是它自己的病史（跨 workspace 误绑），不要照抄。

## Version anchors（2026-11-15 统一到 1.0.0）

| 位置 | 值 |
|---|---|
| `SKILL.md` front-matter `version` | `1.0.0` |
| `CHANGELOG.md` 首条 | `v1.0.0 — 2026-11-15 正式版（0.10.x 线收口）` |
| `workbench/workbench.config.json` `version` | `1.0.0` — **页脚主来源**（`/api/config` 直读本文件） |
| `workbench/app.config.json` `version` | `1.0.0` |
| `workbench/index.html` 内嵌 `WB_CFG.version` | `1.0.0`（后端不可达时的兜底配置） |
| `workbench/index.html` `wbRenderFooter()` fallback | `1.0.0`（连内嵌配置都没有时的最后兜底） |

> 页脚版本链路：`wbRenderFooter()` → `WB_CFG.version` → `/api/config` → `workbench.config.json`。
> 2026-11-08 之前 4 处写死 `0.1.0`，用户天天看到 `v0.1.0` 而技能已到 0.10.7。
> 六处锚点由 `workbench/capability_parity.py` 第 1 条强制一致。

## Re-publishing protocol（ct-base §13.5 Scheme B）

1. **能力对齐检查**（发布检查单硬关卡）：
   `python workbench/capability_parity.py` → 必须 PASS（版本 / i18n / DOM / CLI flag /
   **架构↔文案事实一致性**五条全绿）。`ctqa.config.json` 的 W0 层已接入同一脚本。
2. **辅助检查**：`python workbench/check_i18n.py`（已改为相对路径，可独立运行）；
   `py_compile workbench/server.py scripts/ct_safety.py`；内联 JS `node --check`。
3. **重建载荷**：`python workbench/publish-kit/build_publish.py`（whitelist + prune，不做 bulk delete）。
   脚本已排除 `_bak*`、`__pycache__`、`runs/`、`publish-kit/`、`.genie`、`.env`。
4. **安装归属标记到当前 workspace 根目录**：
   `python workbench/publish-kit/install_genie.py`（可加 `--dry-run`）。
5. **覆盖发布**：`directory = <skill>/workbench/publish`，`appId = wbapp_GyOm0cdJ1qHoaQxlFZOVwl`，
   `domainPrefix = ct-safety`。**绝不 `createNewApp`** —— 复用 appId 是保住同一链接的唯一手段。
6. **断言返回值**：`shareLink` 必须等于 `https://ct-safety.app.workbuddy.host/`（§13.5 dirty-binding 红线）。
7. **回写**：更新 `app.config.json` 的 `deployedAt`、本表 `Last deployed`、CHANGELOG 去掉「待部署」标记。

## 待部署欠账（部署后逐条验证并销账）

| 条目 | 部署后必验 |
|---|---|
| v0.10.7 阶段 2 交付契约 + 空报告结构 | `report.xlsx` 中文四表、空结果也有完整结构 |
| v0.10.6 工作台 Excel 语言对齐 + 脚本层 auto 回退 | 页面下载的 xlsx 不再是全英文 |
| 2026-11-08 页脚版本 `0.1.0 → 0.10.7` | 线上页脚显示 `v0.10.7` |
| 2026-11-08 数据流表述 + 出站披露 | 数据源页写明 `ct-search.coze.site`，无「恒开直连」 |
| 2026-11-08 综合信号评分卡 / 源健康面板 | 单事件检索后可见 0–100 分与 T1–T4；数据源页有真实产物清单 |
| v0.10.8 工作台合规整改（品牌 ct-tier-a / 侧栏折叠 / C7 返回钮 / 披露收口） | 顶栏为 tier-a 渐变；侧栏单击空白折叠并记忆；顶栏最右有「CT 首页」；表单底部无出站横幅 |
| v0.10.9 视觉审查整改（A 组规范硬项 / B 组可用性） | 表单 label 13px；未选数据源卡不再半透明；顶栏状态胶囊按 §19.2 color-mix 冻结配方（深底白字四态可辨，非白底+语义色）；内容区居中限宽 1280；SOC 条形图可见 |
| v0.10.10 数据源页语义纠正（源说明 / 产出核对分离） | 数据源页先列 5 个源（主源+附加源）与判定口径；产出核对按抓取/分析/导出分组，未勾选项显示「未启用」而非「未产出」；失联运行只显示一条失败摘要+异常行 |
| v0.10.11 数据源清单核实 + 侧栏提示沉底 | 数据源表下有一行脚注说明「5 个即全部，佐证源 3 个与阻断源 6 个不在本页链路」；侧栏「单击空白折叠」贴在侧栏最底部而非紧跟导航项 |
| v0.10.12 Top-N 截断 / 覆盖率说明 / 器械语义 / PSUR 补列 | *Top 事件数* 填 6 时候选池真的只有 6；多事件表出现覆盖率说明与被剔除项清单；MAUDE 模式标题为器械语义；PSUR 信号表含 IC 与证据分级列 |
| v1.0.0 正式版（版本号收口，无功能改动） | 线上页脚显示 `v1.0.0`；`/api/config` 返回 `version = 1.0.0`；载荷须用 `publish-kit/build_publish.py` 重新构建 |

> ⚠️ 这些改动**只重建了本地载荷，尚未执行线上覆盖发布**。

## 部署后冒烟清单

- `/api/config` → `version = 1.0.0`；页脚 `v1.0.0`
- `/api/health` → `ok: true`；`/api/source-health` → `has_run` 与 9 项产物（含 group / applicable 字段）
- 首页含 `wb-cthome`（返回 CT 首页钮）/ `wb-plan-mount` / `wb-src-health`；出站端点信息在 `srcLockTip` 悬停提示（含 `ct-search.coze.site`），无独立披露横幅；无 `maode`、无「恒开直连」
- 单事件检索（如 `osimertinib` + `pneumonitis`）→ 结果卡出现评分卡；多事件检索 → 出现「需填写聚焦事件」说明而非伪造分数
- 下载 `report.xlsx` 为中文表头；DISCLAIMER 与免责声明完整
