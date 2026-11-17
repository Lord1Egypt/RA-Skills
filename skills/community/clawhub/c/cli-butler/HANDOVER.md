# HANDOVER — cli-butler

## 0. 启动方式

在本目录（`~/Projects/cli-butler`）开新会话即可，交接模式已启用（`.agent-handoff.json`）。先读本文件与 `docs/REQUIREMENTS.md`。

## 1. 背景与去向

- 用户要做并**开源**一个 skill：让任意 agent 具备管理本地 CLI 工具的能力。名字 `cli-butler`（备选 toolbutler）。
- 2026-11-09 调研会话完成：线上搜证（skills.sh + GitHub，无对口方案，差异化=skill 形态+跨包管理器+来源追踪/引用链）、需求清单、批准计划、项目骨架。
- **实现与开源发布在本项目会话进行**；本 repo 尚未推送远端，发布时再建 GitHub repo（发布前名字查重：npm / GitHub / skills.sh）。

## 2. 目录地图

| 路径 | 内容 |
|------|------|
| `docs/REQUIREMENTS.md` | **需求真相源**：六功能详规、非目标、技术约束、验收标准 |
| `docs/provenance.md` | 渠道模型：渠道表、归属判定顺序、journal 格式、四条陷阱规则 |
| `docs/design.md` | 架构草案：布局、出口协议、容错与 dry-run 约定、实现顺序 |
| `docs/../SKILL.md` | agent 入口（英文，frontmatter 已含触发词） |
| `bin/*.sh` | 六功能入口 stub（exit 69 = 未实现占位） |
| `lib/common.sh` | 公共库：渠道清单、probe 容错、journal 读写（已有冒烟覆盖） |
| `tests/run.sh` + `tests/fixtures/` | 冒烟测试（fixtures 空待造） |
| `.github/workflows/ci.yml` | shellcheck + 冒烟 |

## 3. 数据口径与勿动约定

- **provenance 口径**：每个 CLI 归属恰好一个渠道；渠道是装/卸/升级唯一路由，禁止绕渠道直接 rm（细节见 `docs/provenance.md`）。
- journal：`~/.config/cli-butler/journal.tsv`（可用 `BUTLER_JOURNAL_DIR` 环境变量重定向，测试必须重定向）。
- 需求变更只改 `docs/REQUIREMENTS.md` 并在此文件登记一行变更记录；SKILL.md/README 同步。
- 2026-11-09 需求补充：F1 list 增加按渠道分组输出与每 CLI 一句话用途（desc，仅本地采集，禁逐包联网）；新增 `system` 分类（macOS SIP 系统自带 CLI 单列分组、显式标注不可卸载，F4 直接拒绝）。已同步 REQUIREMENTS / provenance / SKILL / README。

## 4. 已产出清单

- 骨架 + 首个 commit（5356e76）：REQUIREMENTS、provenance、design、六 stub、common.sh（journal 用 awk 首列匹配，勿改回 grep tab 方案）、SKILL.md、README、LICENSE(MIT)、CI、tests（本地绿；本机无 shellcheck，CI 里跑）。
- 需求来源：本计划曾两次驳回后批准（final：六功能完整版），全文誊入 REQUIREMENTS。

## 5. 可继续方向（实现顺序 F1→F5→F6→F3→F4→F2）

1. **F1 list**：逐渠道枚举（命令清单见 provenance.md 渠道表）+ PATH 无主二进制 + 合并去重 + 分组输出（组头渠道说明）+ desc 本地采集 + system 组标注；对数本机真实数据（docker=OrbStack 软链、node/nvm、dsh 残留 .off plist、homebrew 包、/usr/bin 系统自带）。
2. **F5 refchain**：五层输出 + zsh 历史 epoch 判活（mtime 不可信）；用 /usr/local/bin/docker 软链链与 ai.deepseek.dsh.web.plist.off 验证。
3. **F6 cap**：--help/-h/help 试探 + 顶层子命令提取。
4. **F3 install**：OS/渠道探测 → 路由 → journal 回写；代理检测（webget 在列时用之）；npm prefix 核对防劫持。
5. **F4 uninstall**：渠道路由 + manual 走 refchain→dry-run→确认；清扫残留。
6. **F2 manage**：info/outdated/upgrade 路由。
7. 收尾：真实 CLI 上跑通验收标准（见 REQUIREMENTS）→ fixtures 补齐 → CI 绿 → 名字查重 → 建 GitHub repo 开源发布。

## 6. 协作红线

- 渠道管理的二进制**永不直接 `rm`**。
- 卸载类操作**默认 dry-run**，显式确认才执行。
- launchd 停用须挪 plist（`.plist.off`），不能只 `launchctl bootout`。
- app 内嵌软链只备份挪链（`.bak`），不动 .app 内部。
- 删除、force push、改共享配置等危险操作须先确认（全局 AGENTS.md 规则）。
- 自动记录：钩子尚未接入具体 agent（用户未确认新会话用哪个），任务记录先手写 `tasks/` 目录（本 repo 暂无该目录，首个任务时建）。


## 2026-11-09 v0.1.0 发布完成（本次会话终态）

- 仓库已开源：https://github.com/kelegele/cli-butler （public，main @ 10d4d34 之后）
- Release v0.1.0：https://github.com/kelegele/cli-butler/releases/tag/v0.1.0
- 六命令全实现：list / install / uninstall / manage / refchain / cap；tests 79 绿（含 Ubuntu CI），shellcheck 0 警告
- 发布前查重（终查）：npm E404 ✓ / GitHub 无同名 ✓ / skills.sh 无同名 ✓
- 任务记录（含逐项验收证据）：tasks/2026-11-09-impl-publish.md
- 坑位备忘：CI 会 shellcheck tests/run.sh（本地曾只查 bin/lib）；Linux bash 5 set -u 要求 local 变量显式初始化（macOS bash 3.2 不报）；gh 需 HTTPS_PROXY=$(webget --proxy-url)
- 可继续方向：Linux SIP 等价体系（dpkg/rpm 系统目录）细化、outdated 扩展 pipx/uv/cargo、`npx skills add` 实装验证（已验证解析路径，未在本机实装避免污染 skill 目录）
