# lis-skill-bus 契约链路（完整版）

原 SKILL.md 章节，按需查阅。

## lis-skill-bus 强制契约链路

- 正式识图必须经过 `cad-file-reader -> cad-contract/v1 -> lis-skill-bus -> gangjiegou-suanliang`；本技能不读取图纸，也不在 bus 缺失时另开识图路径。
- 状态过滤：项目名/楼栋/楼层一致时，本技能与 `cad-file-reader` 及其它算量 skill 通过 lis-skill-bus 交换 `cad-contract/v1`；命中即复用，不再重复解图。
- 拉取（开工前）：`scripts/gangjiegou_statesync.sh pull --project 项目 [--building 楼栋] [--floor 楼层] [--out 落盘.json]`
  —— 命中且契约含本专业 section 字段（`members`、`sections`、`steel_geometry`、`connections`、`materials`、`finishes`）时返回 `hit=true usable=true`，可直接复用；未命中只触发一次新的 `cad-file-reader` 识图，不触发本技能本地解析。
- 发布（算量落盘后）：`scripts/gangjiegou_statesync.sh push --entry-file <本技能输出.json> --project 项目 [--building 楼栋] [--floor 楼层] [--specialty 钢结构]`，自动包装成 `cad-contract/v1` 后入 bus。
- 正式算量（主入口）：`python3 scripts/steel_tonnage.py --from-contract <contract_id> --project 项目 --out-prefix 钢结构吨位`，按 `contract_id` 从 bus 取契约；文件路径 `--steel` 必须配 `--allow-manual`，强制按 manual 降级，不是正式量。
- 对应接线脚本：`lis-skill-bus/integration/gangjiegou_pull_contract.sh` / `gangjiegou_publish_contract.sh`（薄壳，等价调用本技能 statesync）。
- 命中口径：`usable=true` 为本机状态里的「候选级命中」（`candidate_only=true`）；命中 section 内若有 `review_required`/P2/P3 项，statesync 只标 `review_flagged`，本技能的长度两档、米重公式、GB/T 706 查表、牌号分档与复核过滤仍按既有口径完成，不因 bus 命中而跳过滤；`--require-core` 可收紧为必选核心 section（`members`、`sections`）至少一个命中且非空。
- bus 路径变更：仅需设置 `SKILLBUS_HOME` 指向新 bus 目录，本技能任何文件无需改动。
- 安装前置：客户端按如下优先级定位 `skillbus_client.py`：① `SKILLBUS_HOME`/`SKILLBUS_CLIENT` 显式指定；② `$HOME/.codex/mcp_servers/lis-skill-bus/skillbus_client.py`（正式安装落点）；③ `$HOME/.codex/skills/lis-skill-bus/skillbus_client.py` / `$HOME/.codex/skills/.skillbus/skillbus_client.py`。找不到 bus 时 formal statesync 以退出码 2 停止并提示安装 `lis-skill-bus>=0.1.11`，不会降级为本地识图。
- Windows 接线：GitHub 完整包 `scripts/gangjiegou_statesync.cmd push|pull`（GitHub/ClawHub 含 .cmd，SkillHub 轻量包剔除 .cmd、Windows 改用同目录 .py 入口；macOS/Linux 用 `bash scripts/gangjiegou_statesync.sh` 等价调用）。Windows 未实机跑通，仅静态校验通过（CRLF 行尾；无 /Users、/bin/sh、python3 硬编码；%PYTHON%/%CODEX_PYTHON% 回退）。

