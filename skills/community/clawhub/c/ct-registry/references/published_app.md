# Published Application (ct-registry workbench)

> 本文件是 **部署 / 重发布操作的单一事实源**（2026-11-08 建立）。执行任何 deploy / re-publish 前先加载本文件。
> 建立动因：此前 `publishDir` 在 SKILL.md、构建脚本、app.config.json 三处不一致，且「Last republished」
> 写死在 SKILL.md 里，与 CHANGELOG 的多条「（待部署）」记录长期矛盾。

## Registry

| Item | Value |
|---|---|
| Share link | `https://ct-registry.app.workbuddy.host/` |
| appId | `wbapp_39NhpDKvmNZ4AjTmsODgqH` |
| domainPrefix | `ct-registry` |
| **Publish bundle** | **`workbench/publish/`** — 在技能目录内、与 workspace 无关（重建：`python workbench/publish-kit/build_publish.py`，脚本 `DST = HERE.parent / "publish"`） |
| Publish infra | `workbench/publish-kit/` — `.wbapp_*.genie` 标记 + `install_genie.py` + `build_publish.py`；构建时按目录排除，不进载荷 |
| Ownership marker | `workbench/publish-kit/.wbapp_39NhpDKvmNZ4AjTmsODgqH.genie`（安装：`python workbench/publish-kit/install_genie.py`） |
| Deployed as | Python HTTP service（`app.py` → `workbench/server.py`，绑 `0.0.0.0`，读 `$PORT`） |
| Backend | `GET /api/config /api/health /api/localize /api/runs /api/task/<id> /api/download /api/sources`；`POST /api/search /api/plan /api/bug-report /api/run-delete /api/diff` |
| Deploy metadata | `workbench/app.config.json` |
| **Last deployed** | ⚠️ **线上版本未核实**。SKILL.md 旧文自陈 `2026-09-26`，但 0.14.4 / 0.14.5 与 10-23 崩溃修复的 CHANGELOG 条目均标「未执行部署 / 待部署」。部署后必须回写本行并补 `app.config.json` 的 `deployedAt`。 |

> ⚠️ **历史陷阱（勿重演）**：2026-11-08 之前 SKILL.md 把 `publishDir` 写成 `workbench/publish-dist`
> （照抄 ct-literature 的配置），但该目录在本技能中**从不存在**；构建脚本与 `app.config.json` 一直用
> `workbench/publish`。ct-literature 之所以改名 `publish → publish-dist`，是因为它自己的 `publish/`
> 曾被错误绑定到别的应用沙箱（跨 workspace 事故），**那是 ct-literature 的病史，不是 ct-registry 的**。
> 若本技能将来出现 `shareLink` 漂移 / mis-binding，按同一原则处理：换一个全新的载荷目录名，
> 旧的被误绑路径永久退役，且每次部署后必须断言返回的 `shareLink` 仍是本表地址。

## Version anchors（2026-11-15 统一到 1.0.1）

| 位置 | 值 |
|---|---|
| `SKILL.md` front-matter `version` | `1.0.1` |
| `SKILL.md` §Deliverable language | `v1.0.1` |
| `CHANGELOG.md` 首条 | `1.0.1 — 2026-11-15` |
| `README.md` / `README_zh-CN.md` 页脚 | `v1.0.1` |
| `AGENTS.md` 标题 | `v1.0.1` |
| `workbench/workbench.config.json` `version` | `1.0.1` — **页脚 `wb-footer-ver` 读这里**（`/api/config` 直读本文件） |
| `workbench/app.config.json` `version` | `1.0.1` |
| `workbench/publish/workbench/workbench.config.json` `version` | `1.0.1`（发布载荷内页脚版本来源，随升版同步） |

> 页脚版本链路：`index.html:wbRenderFooter()` → `WB_CFG.version` → `/api/config` → `workbench.config.json`。
> 任何一处漏改，用户就会看到过期版本号（2026-11-08 前线上显示 `v0.1.1`）。

## Re-publishing protocol（ct-base §13.5 Scheme B）

1. **能力对齐检查**（发布检查单硬关卡）：
   `python workbench/capability_parity.py` → 必须 PASS。
2. **重建载荷**：`python workbench/publish-kit/build_publish.py`（whitelist + prune，不做 bulk delete）。
   构建脚本已排除 `_bak*` 备份目录、`__pycache__`、`runs/`、`publish-kit/`、`coze/` 等。
3. **安装归属标记到当前 workspace 根目录**：
   `python workbench/publish-kit/install_genie.py`（可加 `--workspace <dir>` / `--dry-run`）。
   部署工具只校验当前 workspace 是否存在该 `.genie` 标记，不关心载荷在哪个目录。
4. **覆盖发布**：`directory = <skill>/workbench/publish`，`appId = wbapp_39NhpDKvmNZ4AjTmsODgqH`，
   `domainPrefix = ct-registry`。**绝不 `createNewApp`** —— 复用 appId 是保住同一链接的唯一手段，
   新建应用会生成带后缀域名，属事故而非备选。
5. **断言返回值**：`shareLink` 必须等于 `https://ct-registry.app.workbuddy.host/`（§13.5 dirty-binding 红线）。
6. **回写**：更新 `app.config.json` 的 `deployedAt`、本表 `Last deployed`、CHANGELOG 去掉对应的「待部署」标记。

## 待部署欠账（部署后逐条验证并销账）

| 条目 | 部署后必验 |
|---|---|
| 0.14.5 阶段 2 Excel 交付契约 + 英文交付物零中文 | `report.xlsx` 四表中文；`--lang en` 版 CJK 单元格 0 |
| 0.14.4 结果文件中文化 + 兜底报告排版 | 表头中文、冻结首行、列表值不再是 `str(list)` |
| 2026-10-23 CT.gov v2 `statusModule` 归一化崩溃 | `osimertinib` 默认 50 条/库不再 `AttributeError`，有清单 / xlsx / Landscape |
| 2026-10-20 coze antiscrape 六级准入 | 需另打包 `adapters/coze` zip + MD5 上传 Coze（手动，待授权） |
| 端点 0.4.00 B 类三项上移 | 仅本地打包，未上传 / 未部署；部署后单独 canary 验 PROSPERO 可达性 |

> 注：后两项是 **Coze 端点侧**部署，与 WorkBuddy 站点覆盖发布是两条独立通道，不要混为一步。

## 部署后冒烟清单

```
GET  /api/config                 → version = 1.0.1
GET  /                          → 页脚显示 v1.0.1
GET  /api/sources               → 源健康 / 降级状态可读
POST /api/plan                  → 返回站点 × 关键词组计划
POST /api/diff {a,b}            → 返回 status_delta（纯本地、零联网）
下载 report.xlsx                → 中文四表 + 冻结首行 + 8 张原生图表
```
