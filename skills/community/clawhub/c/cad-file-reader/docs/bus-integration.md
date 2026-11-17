# lis-skill-bus 契约联动

## lis-skill-bus 契约联动（CAD 单用可降级，算量链必须安装）

> 好处：同一张 CAD 图只解析一次，本技能与五件套、其它算量技能共享同一份项目状态与识图契约；图纸解析默认本地；仅首次缺依赖时联网取公共依赖，不上传图纸字节；图纸数据未经明确同意不交云端。
> 安装入口（跨平台）：先装 lis-skill-bus —— SkillHub slug：`lis-skill-bus`；GitHub：`lisong2003-lgtm/lis-skill-bus`。装完后运行安装器 `python install_py.py --apply`（只复制不注册 MCP：`SKIP_MCP_REG=1`）。
> **边界**：CAD 独立识图不依赖 bus；bus 缺失时只保留本机 state 兜底，便于安装后接续，但这不等于允许算量技能自行解图。进入土建/安装/装饰/园林/钢结构算量链时，bus 是必需的契约桥，缺失应停止并提示安装。

- 状态过滤：项目名/楼栋/楼层一致时，把本次解析的 `cad-contract/v1`（含 project_key / producer / source / contract）发布到本机 lis-skill-bus，供五件套后续直接取数，不再重复解图。
- 自动接线入口（推荐，不侵入解析核心）：
  - `scripts/cad_statesync.sh push --entry-file <cad-file-reader/v0.json> --project 项目 [--building 楼栋] [--floor 楼层] [--source-file 图纸.dwg] [--specialty 土建]`
    —— 自动把 cad-file-reader/v0 契约包装成 cad-contract/v1 并发布；`--detail-json <cad_scan --detail-json 产物>` 可直接包装详情。`--entry-file` 若已是 cad-contract/v1 则原样补全主键后推送。
  - `scripts/cad_statesync.sh pull --project 项目 [--building 楼栋] [--floor 楼层] [--out 落盘.json]`
    —— 拉取最近一次 cad 契约（供土建/安装/装饰/园林算量后续取数，命中即免重复解图）。
  - `--state-push` / `--resume` 分别为 push / pull 的别名；Windows 统一用 `python scripts/cad_statesync.py push/pull ...`（Windows SkillHub 版无 `.cmd`，直接走 py 入口，功能等价）。
- 兼容/降级：客户端按如下优先级定位 `skillbus_client.py`，正式路径存在时不回退 dev 副本：
① `SKILLBUS_HOME`（bus 目录）或 `SKILLBUS_CLIENT`（直接指向 client 文件）显式指定
② `$HOME/.codex/mcp_servers/lis-skill-bus/skillbus_client.py`（正式安装落点）
③ `$HOME/.codex/skills/lis-skill-bus/skillbus_client.py` / `$HOME/.codex/skills/.skillbus/skillbus_client.py`
④ 常见本机开发/临时副本目录（最后才回退）。
命中 dev/临时副本时 stderr 会输出告警行「bus 命中来源：<路径>（临时副本/dev，非正式安装）」，正式路径输出「（正式安装）」；找不到 bus 时不报错，直接写 `$HOME/.codex/skills/.skillbus/state.json`（与 bus 同构，后续装 bus 可无缝读取）。 无 MCP 不影响任何识图能力，核心解析与 cad-file-reader/v0 契约不变。
- 消费端必选核心口径（供接线核对，bus 内各专业自行判定）：土建 `text_records+geometry_segments`（默认启用）；安装 `circuits`/`route_segments`；装饰 `rooms`/`room_schedules`；园林 `plant_schedule_links`/`paving_closed_areas`。各专业 statesync `pull --require-core` 收紧为必选核心至少一命中；默认仍为宽松候选级命中，不改基础解析契约。

- Windows 接线：Windows SkillHub 版无 `.cmd`，统一用 `python scripts/cad_statesync.py push/pull ...`（功能一致）。Windows 未实机跑通，仅静态校验通过（CRLF 行尾；无 /Users、/bin/sh、python3 硬编码；py 启动器 + %PYTHON%/%CODEX_PYTHON% 回退；默认路径用 %USERPROFILE%\.codex）。
