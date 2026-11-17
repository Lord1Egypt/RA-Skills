# 强依赖底座契约（cad-file-reader）

原 SKILL.md 内嵌说明，完整保留于此，供按需查阅。

本技能采用**识图与算量分离**的固定架构，`cad-file-reader` 是**强依赖底座**，不是可选增强：

- **为什么必须强依赖**：DWG/DXF/DWT/PDF 的解析、图层/文字/块/图框/几何提取、识图候选和测量候选全部集中在底座完成，一次解图、全项目复用，保证证据坐标与契约一致。本技能只做本专业口径的量算、扣减、损耗、分账和台账，不重复解析图纸。
- **分工**：底座输出 `final_quantity=false` 的识图/测量候选；本技能输出本专业概算底稿/物资计划草稿（`final_quantity=true` 仅本专业口径）。
- **版本约束**：底座最低版本以各技能 `SKILL.md`「前置/依赖」写的 `>=x.y.z` 为准；缺底座或版本不够时明确报错，不静默用错误数据。
- **安装**：先装底座（`cad-file-reader` 的 `scripts/setup.sh`），再装本技能；运行时底座可在 `SKILL_NO_BASE=1` 下退化为只读已有扫描/候选/表格输入，但精度受限并必须在结果标注。
- **联动**：装有 lis-skill-bus 时，底座与各算量技能通过 `cad-contract/v1` 共享契约，同一张图只解一次；不装 bus 时各技能自动降级为各自 `state/`，功能不丢失。

## 强依赖底座（cad-file-reader，不做弱化）

`cad-file-reader` 是强依赖底座，不是可选增强：DWG/DXF/DWT/PDF 解析、图层/文字/块/图框/几何与测量候选全部由底座完成，一次解图、全项目复用，保证证据坐标与契约一致；本技能只做本专业口径的量算、扣减、损耗、分账和台账，不重复解析图纸。底座输出 `final_quantity=false` 的候选，本技能输出概算底稿/物资计划草稿（`final_quantity=true` 仅本专业口径）。缺底座或版本不足必须明确报错，不静默用错数据。装 `lis-skill-bus` 时按 `cad-contract/v1` 共享契约，否则降级到各自 `state/`。完整说明与安装/降级细节见 `references/base-contract.md`。



- 底座 `cad-file-reader >= 0.28.1` 是本技能的**显式依赖**：运行首次会自动检测，缺失时自动下载安装底座并补齐 vendor（联网，下载包做 SHA-256 完整性与版本校验，校验失败拒绝安装）；已装则直接复用，不重复下载。
- 独立/离线场景可设 `SKILL_NO_BASE=1`：不再自动安装底座，仅使用已有扫描 JSON、测量候选或表格输入（精度受限并在结果中标注）。
- 可设 `CAD_AUTO_SETUP=0` 关闭底座内部的 vendor 自动下载；手动安装用 `scripts/setup.sh` 或 `scripts/ensure_base.sh`。

- 依赖 `cad-file-reader >= 0.25.0`；扫描结果会记录底座版本和测量候选兼容状态。
- 可用 `cad_measure.sh` 先生成长度/面积/体积识图候选，再通过 `mep_plan.py --cad-measurement` 导入“CAD测量候选核对”工作表；候选固定 `final_quantity=false`，不参与本技能算量。

- `cad-file-reader` 负责全部 DWG/DXF/PDF 识图并产出 MEP 契约；`mep_scan.sh --contract` 只消费契约 JSON，不再打开 DWG。找不到时设置 `CAD_SKILL_DIR=/path/to/cad-file-reader`。
- `mep_plan.py` 只读 `.scan.json`，不依赖 CAD 解析。
- Python ≥3.10；openpyxl 生成 xlsx。

