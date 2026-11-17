# VERIFICATION-selftest · cad-file-reader 0.34.0

本文件记录 0.34.0 发布回归底线与真实验证证据。

## 跨平台基线（历史稳定基线）

- 0.32.1 生成时间 2026-10-21，GitHub Actions 三 OS（ubuntu-latest / windows-latest / macos-latest）全部 success。
- self_test unit：265 tests，failures 0，errors 0。
- 样例回归：sample_room.dxf 三平台 `text_total=2 / layers=3`；Windows 中文 JSON 可读。

## 真实图纸回归基线（0.31.7）

- run_real_dwg_regression.py：真实 DWG 子集 20/20 通过。
- 覆盖候选门槛修复（缺省候选门槛改为“整套识图包至少产出一个领域候选”）。
- DWG 空解码自动复扫：reg-0169（R2007 section map 无条目）复扫后产出结构几何候选。
- schema/cad_validate 契约校验继续通过，`final_quantity=false` 未改动。

## 0.34.0 CI 实测（run 39914085728，2026-10-23）

- GitHub Actions run 39914085728：ubuntu-latest / windows-latest / macos-latest 全部 success（conclusion=success）。
- self_test unit：三 OS 均 265 tests、failures 0、errors 0；ubuntu/macos skipped=6，windows skipped=9。
- 样例回归：三 OS cad_scan 均为 `text_total=2 / layers=['0','TEXT','WALL']`。
- doctor --json-only：三 OS status=ok（os=linux / win / darwin）。
- lis-skill-bus 往返与降级断言（bus_schema=cad-contract/v1、downgrade projects=True、state_version=1）在三 OS 通过。
- ⚠️ 版本口径：该 run 对应 GitHub commit `92e536e46940458bcea0001ba18616f6ea39d21e`，其中 SKILL.md/manifest.json 为 **0.33.1**，doctor.py 不含 lis_skill_bus 检测；本次 0.34.0 本地内容（版本号、doctor bus 检测、VERIFICATION 文件、README 安装段）未进入该 run。0.34.0 的门禁验证在 s4 本地验证或后续 0.34.0 CI 补跑，不得以本 run 冒充 0.34.0 已通过。

## 0.34.0 回归动作（s1）

- 版本号 0.33.x → 0.34.0：SKILL.md frontmatter / manifest.json / CHANGELOG 同步。
- lis-skill-bus 联动文案由“可选试点”改为“推荐联动（不装自动降级）”，补齐跨平台安装入口。
- doctor.py 恢复只读 bus 检测；`python3 -m py_compile scripts/*.py` 全绿。
- 红线：契约 schema、cad_contract.py、wrap_v1/cmd_push/cmd_pull 与命令算法均未改动。

> 测试脚本按平台限制已在轻量包移除；完整可复跑代码在 GitHub 完整包。

## 0.34.0 本地验证（2026-10-23 s4，修复 doctor 平台测试后）

- self_test：summary ok=true，steps 5 pass / 1 skip（real_dwg_regression 无 manifest 跳过），unit 265 tests failures=0 errors=0 rc=0。
- 修复内容：v0.34 在 doctor.py tier0 新增第 7 项能力 lis_skill_bus；同步 scripts/tests（本机开发目录） 的 CAPABILITIES 断言由 6→7，并允许 bus 状态（已安装/未装/禁用）；doctor.py 标签统一为「联动总线（推荐）」。修复后 265/0 全绿。
- cad_validate：对 cad-file-reader/v0 契约样例 `ok=true, errors=[]`，exit=0。
- lis-skill-bus 往返（假 bus，SKILLBUS_HOME=/tmp/fakebus）：push cad-scan-detail（text_records+geometry_segments）→ pull 返回 schema=cad-contract/v1、spec=cad-file-reader/v0、contract.text_records/geometry_segments 命中；按 bus schemas/cad-contract-v1.schema.json 结构字段全通过。
- 降级路径：SKILLBUS_DISABLE=1 push/pull 无报错，写 $HOME/.codex/skills/.skillbus/state.json（13357B，含 floor=3、cad-contract/v1）。
- setup.py --dry-run exit=0（posix / python3.12.13 / vendor_present=True）。
- SkillHub 0.34.0 轻量包（163 文件）仍以 0.33.2 完整基线叠加：verify_package_refs.py exit=0 断链=0；check_release --skillhub --allow-sensitive problems=0。
