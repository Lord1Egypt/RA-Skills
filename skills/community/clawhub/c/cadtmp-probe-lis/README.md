# CAD 图纸识图与证据提取（cad-file-reader）

> **[English](./README.en.md) | [中文](./README.md)**


本地运行的 CAD **识图与证据提取** Skill：直接解析 DWG/DXF/DWT 与 PDF 图纸，不需要 AutoCAD，全部本机处理、图纸字节不上传。

定位：识图与证据工具，不替代设计审查、清单计价、翻样下料、结算或规范条文解释。
身份透明：这是 AI 助手调用的工具型 Skill，不伪装成任何人物或外部产品。

## 能做什么

- **流式解析** DWG/DXF/DWT：图层、文字、块、图框、几何、构件编号、关键词。
- **专业识图候选**（17 个专业包）：建筑、结构、总图场地、安装、电气（含消防/弱点/智能化）、钢结构、市政、给排水暖通、精装修、幕墙、人防、预制装配、桥梁隧道道路、桩基基坑边坡、门窗楼梯保温防水、防火无障碍绿建。
- **园林景观识图**：苗木图例/乔灌地被候选、铺装闭合域轻量候选、设计院图例快速校准、DWG 块名净化与 `--dwg-dxf-fallback` 自动转 DXF 复扫；全部 `final_quantity=false`。
- **长度/面积/体积测量候选**：每条 `final_quantity=false`，不冒充工程量。
- **规范/图集元数据定位**、图层/块语义、图纸变化对比、PDF 识图（本机类型分流 + 本地 OCR）。
- **大图低内存扫描**、证据缓存、局部解析；Markdown / JSON / CSV / Excel / Word 输出。
- **统一候选契约** `cad-file-reader/v0`：证据坐标、置信度分层（confirmed/inferred/review）、复核原因。

## 安装（三平台一条命令）

依赖：Python 3.10+；解析库随完整包自带，或由轻量包一条命令补齐到本包 `vendor/`，不污染系统环境。

macOS：

```bash
cd "$CODEX_HOME/skills/cad-file-reader"
bash scripts/setup.sh --dry-run   # 先看平台/依赖清单
bash scripts/setup.sh             # 缺 vendor 时用公共 PyPI 补齐到 vendor/
```

Windows（PowerShell 或 CMD 均可，内部统一转发 Python）：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_windows.ps1 -DryRun   # 只检测
powershell -ExecutionPolicy Bypass -File scripts\setup_windows.ps1           # 安装+doctor 摘要
```

Windows SkillHub 轻量包（无 .cmd / .ps1，用纯 Python 安装入口）：

```bat
python scripts\setup_win.py --dry-run   # 只检测
python scripts\setup_win.py             # 安装/校验 vendor + 后端指引
```

Linux (Debian/Ubuntu 优先，fedora/dnf 已备注等价包)：

```bash
cd "$CODEX_HOME/skills/cad-file-reader"
bash scripts/setup_linux.sh --dry-run   # 只打印，不安装系统包
bash scripts/setup_linux.sh             # 缺系统依赖时用 apt 安装后补齐 vendor
# 已有系统依赖时可跳过 apt：SKIP_APT=1 bash scripts/setup_linux.sh
```

完整包（已内置 vendor，macOS/Linux 通常无需执行安装器）：

```bash
cp -R cad-file-reader "$CODEX_HOME/skills/"
# 可选：普通环境缺 numpy 时
python3 -m pip install numpy
# 可选（内存看门狗平台回退，Windows 主路径）：缺少时内存闸降级为协作式超时
python3 -m pip install psutil
```

SkillHub 轻量包（纯文本合规包，不含二进制 vendor）：

```bash
cd "$CODEX_HOME/skills/cad-file-reader"
bash scripts/setup.sh   # 等价旧路径；内部转发 scripts/setup.py，缺依赖用公共 PyPI 补齐
```


### lis-skill-bus 推荐联动（可选装，不装自动降级）

先装 lis-skill-bus（SkillHub slug：`lis-skill-bus`；GitHub：`lisong2003-lgtm/lis-skill-bus`），
装完运行安装器 `python install_py.py --apply`；Windows SkillHub 版无 `.cmd` 时统一用
`python scripts/cad_statesync.py push/pull`。不装自动降级到
`$HOME/.codex/skills/.skillbus/state.json`，五件套仍各自可用。

## Windows 使用（新增 .cmd 入口）


Windows 用户请先运行：

```bat
scripts\setup.cmd        # 依赖自举：检查/提示补齐 vendor
scripts\deps_check.cmd   # 依赖自检（复用 pyboot 检查）
scripts\doctor.cmd       # 环境体检，一条命令看能力分档
```

之后即可像 macOS/Linux 一样使用（内部统一转发到 `scripts/run_cad.py`）：

```bat
scripts\cad_scan.cmd   图纸.dwg --only 墙,柱 --format json -o 扫描结果
scripts\read_cad.cmd   图纸.dwg
scripts\convert_dwg.cmd 图纸.dwg --out 图纸.dxf
scripts\cad_validate.cmd 候选.json
scripts\cad_batch.cmd   图纸目录 --out 台账 --recursive
scripts\demo.cmd        # 简明演示（扫描内置样例）
```

已提供的 .cmd：`setup / deps_check / doctor / cad_scan / read_cad / convert_dwg /
cad_validate / demo / cad_batch`，以及 17 个专业识图入口
（`cad_descriptive_geometry / cad_structural_geometry / cad_site_geometry /
cad_mep_geometry / cad_electrical_geometry / cad_steel_geometry /
cad_municipal_geometry / cad_hvac_plumbing_geometry /
cad_interior_finish_geometry / cad_curtain_wall_geometry /
cad_civil_defense_geometry / cad_precast_geometry /
cad_bridge_tunnel_road_traffic / cad_pile_foundation_slope /
cad_doors_windows_stairs_insulation_waterproof /
cad_fire_prevention_accessibility_green_energy / cad_landscape_geometry`）。

这些 .cmd 只做薄转发、不替换现有 `*.sh`；macOS/Linux 继续用 `.sh`。

## 平台支持矩阵

支持 macOS / Windows 10 及 11 / Linux x86_64，功能一致由统一 Python 入口承接；差异仅在启动脚本后缀（macOS/Linux 用 `scripts/*.sh`，Windows 用 `scripts/*.cmd`）与可选后端安装命令。

| 能力 | macOS | Windows 10/11 | Linux x86_64 |
|---|---|---|---|
| DXF / DWT 流式解析 | ✅ 直接支持 | ✅ 直接支持 | ✅ 直接支持 |
| DWG 流式解析（ezdwg） | ✅ 随包/补齐 | ✅ 随包/补齐 | ✅ 随包/补齐 |
| DWG→DXF 复扫（LibreDWG/ODA） | ⚠️ 可选后端（dwg2dxf/ODAFileConverter） | ⚠️ 可选后端（ODAFileConverter） | ⚠️ 可选后端（dwg2dxf/ODA） |
| PDF 矢量文字坐标（pdftoppm） | ⚠️ 可选 `poppler` | ⚠️ 可选 `poppler`/conda | ✅ 系统包或 `poppler-utils` |
| PDF 扫描 OCR（tesseract / ocr_image / pdf-inspector） | ⚠️ 可选 OCR 引擎 | ⚠️ 可选 OCR 引擎 | ⚠️ 可选 OCR 引擎 |
| 17+1 类专业识图候选 | ✅ | ✅ | ✅ |
| 测量候选（长度/面积/体积） | ✅ | ✅ | ✅ |
| qto-project/v1 五件套联动 | ✅ | ✅ | ✅ |
| 批量识图台账（Excel） | ✅ | ✅ | ✅ |
| 内存看门狗 | ✅ `resource`+psutil 回退 | ✅ psutil 主路径 | ✅ `resource`+psutil 回退 |
| 统一自检 `self_test` | ✅ | ✅ | ✅ |
| 环境体检 `doctor` | ✅ | ✅ | ✅ |

> `⚠️` 表示该平台需要额外安装可选后端才能完整开启对应档位；缺后端时不影响其余能力，`scripts/doctor.cmd|doctor.sh` 会给出该项最小修复命令。三平台 CI（`.github/workflows/cad-xplatform.yml`）在 GitHub Actions 上持续跑 setup→lint→pycompile→self_test→doctor。

### 安装步骤对比

1. **macOS**：`bash scripts/setup.sh`（缺 vendor 时自动补齐）；默认后端 LibreDWG/ODA 可选装。
2. **Windows 10/11**：PowerShell 执行 `powershell -ExecutionPolicy Bypass -File scripts\setup_windows.ps1`，或 SkillHub 轻量包用 `python scripts/setup_win.py`；日常入口用 `.cmd`。
3. **Linux x86_64**：`bash scripts/setup_linux.sh`（apt/dnf/yum 自动适配；已有系统依赖可用 `SKIP_APT=1`）。

### 常见问题（FAQ）

- **Q：Windows 命令提示符没有 bash，能用吗？**
  A：能。Windows 全部提供 `.cmd` 入口（`scripts\cad_scan.cmd` 等），内部统一转发到 `python scripts/run_cad.py`，不需要 Git Bash 或 WSL。
- **Q：Windows 打印中文 JSON 乱码（cp1252）？**
  A：入口已切换为 Python + UTF-8；若仍遇终端编码问题，在 `cmd` 执行 `chcp 65001` 或设置 `PYTHONUNBUFFERED=1`/`PYTHONIOENCODING=utf-8`。
- **Q：三平台 `self_test` 内容一样吗？**
  A：是同一套脚本与样例，CI 在 ubuntu/windows/macos-latest 各跑一遍；平台噪声（内存峰值、路径分隔符、时间戳）有白名单，核心字段一致。
- **Q：Linux glibc 或 macOS 架构限制？**
  A：macOS 支持 Intel 与 Apple Silicon（纯 Python + 可选后端按平台探测）；Linux 面向 x86_64 主流发行版，Python 3.10+。
- **Q：装不上 psutil 会坏吗？**
  A：不会。内存看门狗自动降级为协作式超时，并在 doctor 中提示。
- **Q：完整包自带 vendor 吗？**
  A：GitHub 完整包与轻量包都**不含** vendor 二进制以规避平台差异；首次使用运行 `scripts/setup.sh`（macOS/Linux）或 `scripts\setup.cmd`（Windows）即可补齐到本包 `vendor/`，可离线校验 SHA-256。

## 环境体检（doctor，只读）

一条命令看当前机器能直接处理哪些、缺哪些（DXF/DWG/PDF 矢量/扫描 OCR/测量/算量联动
分别分档为 可用 / 需外部转换 / 需OCR引擎 / 不可用），并把每项缺失的最小修复命令与
DWG 转换后端说明一并给出。**只读，不自动安装、不联网。**

```bash
bash scripts/doctor.sh --out-dir .      # 写 doctor-report.json + doctor-report.md 并打印摘要
bash scripts/doctor.sh --json-only       # 机器可读 JSON 打到 stdout
bash scripts/doctor.sh --md-only         # 人类可读 Markdown 打到 stdout
```

- 档 0：当前机器可用/缺失能力分档。
- 档 1：每项缺失的最小修复命令（优先本技能自带 `scripts/setup.sh`、`install_vendor.sh`、`ensure_runtime.sh`）。
- 档 2：DWG 缺少 LibreDWG(dwg2dxf)/ODAFileConverter 转换后端时的下一步（可用 `cad_scan.sh --dwg-dxf-fallback` 先试）。

## 统一自测/回归闭环（scripts/self_test.sh）

一条命令把「环境体检 + 全量自测 + schema/契约校验 + 样例与坏文件回归」跑完，
输出 doctor / self_test / 回归三合一报告（JSON + Markdown）；带 `--manifest` 时
再串起真实 DWG 回归。

```bash
bash scripts/self_test.sh                              # 三合一报告写到当前目录
bash scripts/self_test.sh --manifest 真图清单.json      # 加真实 DWG 回归
bash scripts/self_test.sh --out-dir /tmp/cad-selftest --report-json r.json
bash scripts/self_test.sh --json-only --skip-unit      # 快速跑，JSON 打到 stdout
```

- 第 1 段：`doctor.py` 环境体检（档 0/1/2 能力与最小修复命令）。
- 第 2 段：`unittest discover` 全量自测（现 205 项）。
- 第 3 段：`schemas/*.schema.json` 轻量 JSON Schema 校验（随包内置，不依赖
  jsonschema）对 `examples/qto-sample` 样例做正/负向不变量校验，并用
  `cad_validate.sh` 校验全部 v0 契约样例。
- 第 4 段：`examples/sample_room.dxf` 实际 `cad_scan` → contractize →
  `cad_validate.sh` 契约校验。
- 第 5 段：坏文件不变量（空文件 / 坏魔数快速失败 <5s）。
- 第 6 段：可选真实 DWG 回归（`run_real_dwg_regression.py`），缺清单则记
  `skipped`，不影响其它段结论。
- 任一非跳过段失败时退出码为 1，禁止发布。

## 跨平台 CI 与不可回归 lint

- GitHub Actions：`.github/workflows/cad-xplatform.yml` 在 ubuntu / windows / macos 三个平台跑
  setup（含可选 psutil）→ `scripts/pyboot.py --version` → `scripts/lint_cross_platform.py`
  （含 vendor 探测）→ py_compile → `self_test --json-only` → `doctor --json-only`。
- 本地复现：`python3 scripts/lint_cross_platform.py scripts/`（退出码 0 = 无 ERROR；
  WARN 仅提示）。`--vendor-check` 允许仓库存在 darwin `.so`，其它平台缺 darwin 二进制不报错。
- 约束：业务脚本出现 `/opt/homebrew`、`/Applications`、`.venv/bin`、`brew`、`osascript`、
  `setrlimit/RLIMIT_*`、裸 `resource.getrusage`、`SIGALRM`、`SIGKILL` 且没有平台分支保护
  会被判 ERROR；跨平台 helper（pyboot/platform_paths/safe_timeout/mem_guard）命中为 WARN。
- 改动边界：不改 `cad-file-reader/v0` / `qto-project/v1` 契约，不重写解析与算量逻辑。

## 批量识图台账（scripts/cad_batch.sh）

按目录批量扫图，输出候选级识图台账 Excel（黄底标出需人工复核行）+ `自检汇总.md`。
复用现有 `cad_scan` 做单图解析，不新写整套引擎；每张图独立运行，单图失败/缺输入只记入台账，不中断整批。

```bash
# 批量扫图：默认输出 outdir/识图台账.xlsx + outdir/自检汇总.md
scripts/cad_batch.sh 图纸目录 --out 输出目录 --glob "*.dwg;*.dxf" --recursive

# 断点续跑：按源文件 SHA-256 跳过已成功图
scripts/cad_batch.sh 图纸目录 --out 输出目录 --glob "*.dwg;*.dxf" --resume

# 单目录/多文件混合、配缓存
scripts/cad_batch.sh 图纸A.dwg 图纸目录/ --out 台账 --glob "*.dxf" --recursive --cache-dir /tmp/cad-cache
```

- Excel `识图台账` sheet：每候选一行，含 `复核原因 / 证据坐标 / 来源文件` 列；`review_required`、置信度<0.5、复核原因非空的行黄底。
- 每张图一个 `汇总·图名` sheet 与一个 `图纸汇总` sheet：列出 候选人 / 复核人（需复核数）/ 缺口。
- `自检汇总.md`：逐图列出 可交付 / 需人工复核 / 失败跳过 / 缺输入，并附 sha256 与契约文件路径。
- 每图契约写入 `outdir/_contract/<图名>.json`（`cad-file-reader/v0`，逐候选 `final_quantity=false`），可继续用 `scripts/cad_validate.sh` 校验。

## 可靠性策略

- **快速失败**：`cad_scan / read_cad / convert_dwg` 先跑 `scripts/cad_preflight.py` 预检。
  空文件、<1KB、魔数错误（非 AC#### / DXF-SECTION / %PDF-）<5 秒直接跳过并写明原因，不假装转换成功；
  DWG 版本不在支持列表时报“不支持的 DWG 版本”。
- **批量跳档**：`cad_batch.sh` 单图失败只写 `自检汇总.md` / `_state.json` 的缺口/失败原因，不中断整批；
  加密 DWG、不支持版本、超时、内存看门狗终止都会被明确翻译后记录。
- **PDF 复核截图**：`cad_pdf_ocr.sh --out-dir 输出` 会把可疑 PDF 页/OCR 失败页/低置信区块截图
  输出到 `输出/_review/<图名>-p<页码>.png`，并生成 `_review/index.json`。可用 `--no-review` 关闭。
- 保持 `cad-file-reader/v0` 契约不变，`scripts/cad_validate.sh` 校验继续通过。

## 快速开始（30 秒见结果）

```bash
bash scripts/demo.sh                       # 用内置样例 DXF 跑一次完整识图，展示首屏 JSON
scripts/cad_scan.sh 图纸.dwg --only 梁,板,柱,墙 --cluster 1500 --format md -o 图纸扫描
scripts/cad_scan.sh 图纸.dwg --with-mtext --with-geom --detail-json 详情.json --format all -o 图纸扫描
scripts/cad_measure.sh 详情.json --out-dir 测量候选
```

SkillHub 轻量包不含 `.dxf` 样例，`scripts/demo.sh` 会用 `scripts/generate_sample.py` 现场还原内置样例后继续。

## 五件套联动端到端示例（qto-project/v1）

在同一个项目目录里跑「识别 → P1 → P2 → P3 → 校验」，**不要求五件全装**；缺专业会占位，不阻断体系。

```bash
# 1) 建联动项目，--recognized 支持一次多个量算专业（已识别/要接入的）
SKILL_DIR/cad-file-reader/scripts/qto_project.py init 项目A \
  --project 示例项目 --building 1#楼 \
  --recognized tujian-suanliang anzhuang-suanliang zhuangshi-suanliang yuanlin-suanliang

# 2) 把你的识图结果包装进各专业识别层（base + 各量算专业）
SKILL_DIR/cad-file-reader/scripts/qto_project.py wrap 1#楼识图.json \
  --specialty cad-file-reader --project 示例项目 --building 1#楼 \
  --out 项目A/识别/cad-file-reader/1#楼__cad-file-reader__20261019.json
# …量算专业同理（--specialty tujian-suanliang / …）

# 缺识图但已登记的专业可补占位：
SKILL_DIR/cad-file-reader/scripts/qto_project.py placeholder 项目A \
  --specialty zhuangshi-suanliang --project 示例项目 --note "本轮未出图，待装饰识图"

# 3) P1 算量联动登记：有既有量算结果用 --quantity 附着（仅登记，final_quantity=false）
SKILL_DIR/cad-file-reader/scripts/qto_p1_link.py --project-dir 项目A \
  --specialty tujian-suanliang --quantity 土建量算.json --draft-type 物资计划
SKILL_DIR/cad-file-reader/scripts/qto_p1_link.py --project-dir 项目A --specialty anzhuang-suanliang

# 4) P2 汇总 + P3 交叉核对
SKILL_DIR/cad-file-reader/scripts/qto_p2_summarize.sh --project-dir 项目A
SKILL_DIR/cad-file-reader/scripts/qto_p3_clash.sh --project-dir 项目A

# 5) 项目级校验：qto 契约 + 识别层完整性 + regression_pass/precision_note 分开统计
SKILL_DIR/cad-file-reader/scripts/qto_validate.sh 项目A --report-json 项目A/validate-report.json
```

产物落在：`.qto/project.yaml`、`识别/<专业slug>/`、`算量/<专业slug>/`、`汇总/<key>__汇总__<date>.json|csv`、`汇总/<key>__交叉核对__<date>.json|csv`。全链路只登记与汇总，不计算最终工程量。

## 使用指引

- 全部命令入口与专业路由见 `pack-index.md`（默认入口表）。
- 能力边界矩阵见 `CAPABILITIES.md`。
- 版本变更见 `CHANGELOG.md`。

## 边界

- 只输出识图、证据、语义/拓扑/变化候选和测量候选（固定 `final_quantity=false`）。
- 不做设计合规审查、清单计价、结算审计或规范条文解释。
- 不输出最终工程量、材料量、造价或结算量。
- 自动提取不能替代设计单位、翻样、清单编制和正式授权规范全文。
- 算量交给专项 skill（土建 → tujian-suanliang，装饰/安装 → 对应专项）。
- 公司项目路径、内部结果和规范全文不得进入技能发布内容。

## 许可

本包文档与脚本采用 CC BY-NC-SA 4.0。第三方解析库许可见 `NOTICE.md`。
