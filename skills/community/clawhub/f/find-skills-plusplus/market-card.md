# Find Skills++（技能发现 · 安全策展 · 生态治理）

**EN:** All-in-one AI-agent skill ecosystem tool — discovery, AST-level security curation, and full-lifecycle governance. Community supercharged fork of `find-skills` (MIT). 20 zero-dependency subcommands, 140 passing tests, end-to-end smoke self-proof.

## Description

技能生态的**发现 + 安全策展 + 全生命周期治理**工具。帮 AI agent 在多个技能注册中心
（宿主原生市场、SkillHub、ClawHub、Vercel Skills）里找技能、跨源合并去重、安装前做
AST 级安全审查、评估技能质量，并支持更新、卸载、冗余清理与安装历史追溯。

**与同类最关键的四点差异**：① 安装前用 **AST 语法树级扫描**（而非正则）做安全闸门，
能识破动态拼接的危险命令、base64 混淆执行、凭据目录窃取与 Agent 身份文件读取，
输出 EXTREME/HIGH/MEDIUM/LOW 四级风险与文件·网络·命令权限清单；
② `sync` 把在线目录同步到本地，**断网也能搜**；③ **引用完整性校验**，
识破"长得好看但引用了不存在工具"的假优技能；④ **全生命周期**（更新 / 卸载进回收站 /
重复安装清理），而同类只能装不能管。

附带**零依赖 Python CLI**（`findskills.py`，20 个子命令，含 `promote` 自我营销引擎、
`demo` 可录屏演示、`elevator` 电梯演讲），可脱离 agent 独立运行、可演示、
有完整 pytest 测试套件（140 项全绿），并带 `scripts/smoke.py` 端到端冒烟自证。

派生自 `guipi888/find-skills`（MIT，99.4 万下载），源头为 `vercel-labs/skills` 的
`find-skills`；共 **52 项实质增强**`。参考（非复制）`sandbaseai/workbuddy-skill`
的脚本化审查思路、对标 `skill-vetter`（31 万下载）的红旗清单。

## Publisher

何巍（成都）。本项目为**带完整署名的社区超级增强版**，**非官方替代品**。

## License / Terms of Use

- **MIT-0**（新增内容，见 NOTICE）。上游 `guipi888/find-skills` 经核实为 **MIT, Copyright (c) 2026 Kyle**，
  派生、修改、再分发均被明确允许；本仓库保留其 MIT 许可文本与署名。
- 源头 `vercel-labs/skills`；思路参考 `sandbaseai/workbuddy-skill`。
- 明确标注「基于 find-skills 修改」，不伪装成官方替代品。详见 `LICENSE` 与 `CHANGELOG.md`。

## Use Case

- 用户说"帮我找个能做 X 的技能"时，跨源搜索并给出排序后的中文卡片（含质量评级）
- 安装任何第三方技能前，做安全审查（AST 级 + 四级风险 + 权限清单）
- 本地已装技能太多、有重复或疑似冗余时，给出保留/清理建议
- 离线或注册中心 API 不可用时，仍能基于本地缓存与内置注册表推荐
- 需要向他人/市场介绍本技能时，一键生成推广素材（`promote`）与演示（`demo`）

## Deployment Geography for Use

Global。全部功能离线可用（内置 `registry.json` + 可选 `sync` 缓存），联网仅用于
主动拉取社区目录，非必需。

## Known Risks and Mitigations

**风险 1：安全扫描为静态分析，存在漏报。**
无法覆盖运行时行为、动态加载、条件触发的恶意逻辑；混淆得当的代码可能绕过检测。
> 缓解：扫描结果只作**分诊辅助**，明确标注"扫描干净 ≠ 安全保证"；四级风险中
> HIGH/EXTREME 一律要求人工批准；报告同时输出权限清单供人工核对。

**风险 2：安装社区技能本质上是执行第三方代码。**
> 缓解：安装前强制过扫描闸门；EXTREME 直接阻断；优先推荐宿主原生市场（经宿主审核）；
> 安装历史可追溯，卸载走回收站可还原。

**风险 3：卸载 / 清理操作可能误删。**
> 缓解：`uninstall` 与 `clean-dupes` 一律走**系统回收站**（Windows 原生 / `gio trash` /
> `trash-put`），非硬删除；支持 `--dry-run`；不可用时回落 `~/.workbuddy/.trash/`。

**风险 4：注册中心数据可能过时或被伪造（下载量、更新时间）。**
> 缓解：内置 `registry.json` 的 `downloads` 为 `null` 表示"未核实"，**不编造数据**；
> 用信誉分代替热度造假；综合分叠加时效衰减，长期未维护自动标记。

**风险 5：`sync` 会向第三方注册中心发起网络请求并缓存目录到本地。**
> 缓解：仅在用户显式执行 `sync` 时联网；`--offline` 可完全禁用网络；缓存带 TTL 24h；
> 不上传任何本地数据。

**风险 6：质量评级与冗余检测基于启发式信号，可能误判。**
> 缓解：明确标注为**静态信号**而非真实使用追踪；冗余检测用中文去停用字 + bigram
> 降误报；`prune` 为**只读建议**，不自动删除。

## 隐私

不收集、不上传、不外传任何本地数据。搜索请求仅发往用户主动指定的注册中心；
安装历史/缓存/注册表只写本地；安全扫描全本地静态分析，不上传被扫描内容。
