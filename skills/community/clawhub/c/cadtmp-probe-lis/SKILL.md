---
name: cadtmp-probe-lis
slug: cadtmp-probe-lis
displayName: CAD Tmp Probe
version: 0.0.2
license: CC-BY-NC-SA-4.0
author: lis
i18n: true
locale: zh-CN
locales: [zh-CN, en-US]
description: 本地读取 AutoCAD DWG/DXF/DWT/PDF 图纸：DWG/DXF 走流式解析，PDF 走本机分流+本地 OCR。提取图层、文字、块、图框、几何、建筑/结构/总图场地/安装/电气/钢结构/市政/给排水暖通/精装修/幕墙/人防/预制装配/园林景观（苗木图例、乔灌地被候选、铺装闭合环、设计院校准、DWG块名净化与自动转DXF复扫）识图候选、系统拓扑、长度/面积/体积测量候选及规范图集元数据，均保留证据坐标与复核原因。仅输出识图与测量候选（final_quantity=false），不计算最终工程量、材料量、造价或结算量；算量交给专项技能。内置 P0–P5 优化：统一候选契约/置信度分层、大图缓存与局部解析、图层/块语义、MEP 拓扑增强、图纸对比。
---

# CAD 图纸识图与证据提取（cad-file-reader）

本技能只做**识图、证据提取、候选解释和测量候选**，可输出长度、面积、体积的识图候选值、计算式和复核边界；不把候选值冒充最终工程量、清单量、材料量、造价或结算量。结构混凝土/钢筋算量已迁到 `tujian-suanliang`（本机目录 `shangwu-suanliang`），装饰、安装、钢结构、市政算量分别交给对应专项 skill。

## 安装与依赖

- 完整包解压即用；SkillHub 轻量包一条命令：`bash scripts/setup.sh`（幂等，先自动补回下载包可执行位，再自动补齐依赖）。
- **运行时自动自举**：任意 `run_cad.sh` 入口启动时先调 `scripts/ensure_runtime.sh`，检测到 vendor 缺失自动补齐（默认公共 PyPI 零配置安装 ezdwg/ezdxf/fonttools/pyparsing/numpy；设置 `CAD_FILE_READER_REPO=<owner>/<repo>` 时改走 GitHub Release 完整包并做 SHA-256 校验，校验失败回退公共 PyPI；设 `CAD_AUTO_SETUP=0` 关闭并明确报错）；vendor 已存在则不联网、不重复下载。
- 依赖自检：`bash scripts/deps_check.sh --minimal`；缺 numpy 只影响梁线几何估算，其余功能降级为 review。
- **环境体检（只读，不自动安装）**：`bash scripts/doctor.sh` 一条命令输出分档结论（档0 当前哪几项可用/缺哪些，档1 每项缺失的最小修复命令，档2 DWG 缺 LibreDWG/ODA 转换后端时的下一步）。默认写 `doctor-report.json` + `doctor-report.md` 到当前目录，stdout 再打一份人类可读摘要；`--json-only` / `--md-only` / `--no-write` 供自动化或自测用。
- 30 秒样例：`bash scripts/demo.sh`；完整包用内置 `examples/sample_room.dxf`，SkillHub 轻量包若含 `.dxf` 则由 `scripts/generate_sample.py` 现场重建同一样例（跑识图→测量→契约校验）。

## 平台支持矩阵

支持 macOS / Windows 10 及 11 / Linux x86_64，功能一致；差异仅在启动脚本与可选后端：
macOS/Linux 用 `scripts/*.sh`，Windows 用 `scripts/*.cmd`（GitHub 完整包才有全部 `.cmd`；SkillHub 轻量包剔除 `.cmd`，Windows 请改用同目录 `scripts/*.py`，或装 GitHub 完整包）。三平台 CI 见 `.github/workflows/cad-xplatform.yml`。

| 能力 | macOS | Windows 10/11 | Linux x86_64 |
|---|---|---|---|
| DXF / DWT 流式解析 | ✅ | ✅ | ✅ |
| DWG 流式解析 | ✅ | ✅ | ✅ |
| DWG→DXF 复扫 | ⚠️ 可选后端 | ⚠️ 可选后端 | ⚠️ 可选后端 |
| PDF 矢量 / 扫描 OCR | ⚠️ 可选后端 | ⚠️ 可选后端 | ⚠️ 可选后端 |
| 专业识图候选 | ✅ | ✅ | ✅ |
| 测量候选 | ✅ | ✅ | ✅ |
| qto 五件套联动 | ✅ | ✅ | ✅ |
| 批量台账 Excel | ✅ | ✅ | ✅ |
| 内存看门狗 | ✅ | ✅（psutil 主路径） | ✅ |
| self_test / doctor | ✅ | ✅ | ✅ |

平台安装与 FAQ 见 `README.md`“平台支持矩阵”。

## 执行原则

- 先用低内存 `cad_scan` 读文字、图层、块名、图框和几何候选；确需实体树/渲染时再用 `read_cad`。
- 自动结果必须带证据坐标、图框、图层、口径和复核边界；缺输入时列缺口，不编造数量或合规结论。
- 规范/图集资料只做元数据与版本风险提示，不复制全文、不输出条文符合性结论。
- 命令均相对技能根目录执行；输出文件写入当前项目工作目录，不写系统目录。
- 大图先扫描、按需局部展开；高内存/高 CPU 立即暂停。
- 首次扫描可用 `--cache-dir` 建立本机证据缓存；同图重复查询命中缓存。缓存只保存识图证据，不保存最终工程量。

## 可靠性策略（快速失败 / 批量跳档 / 复核截图）

- **入口快速失败**：`cad_scan / read_cad / convert_dwg` 先跑 `scripts/cad_preflight.py` 的轻量预检
  （<5 秒，只读前 4KB，不调解析器）。空文件、<1KB、魔数不是 AC####/DXF-SECTION/%PDF 的头会立即标
  “快速失败”并跳过，不假装转换成功；DWG 版本不在支持列表时直接报“不支持的 DWG 版本”。
- **批量不中断**：`cad_batch.sh --out 台账` 对坏图/加密图/不支持版本逐图记录
  “缺口/失败原因”（`自检汇总.md` 与 `_state.json`），单图失败不影响其它图继续跑。
  - 加密 DWG（ezdwg 报 `encrypted/password`）记为“加密 DWG：需密码或人工解锁”。
  - 不支持版本记为“不支持的 DWG 版本”。
- **超时与内存看门狗**：单图沿用 `--budget` 阶段预算和 `--cap-mb` 内存闸；批量层对整条
  `cad_scan` 再加硬超时（超时 rc=124），退出码 -9/内存闸关键词被翻译成“内存看门狗终止”，原因写入台账。
- **PDF 复核截图**：`cad_pdf_ocr.sh --out-dir 输出` 自动把可疑页面截图写到
  `输出/_review/<图名>-p<页码>.png`，并写 `_review/index.json`（每页原因 + 图片相对路径）。
  - 触发条件：OCR 失败页、扫描页 OCR 无有效文字、整页平均置信 <60%、出现单行置信 <40% 的低置信区块。
  - 截图对应的候选项带 `review_image` 字段；`--no-review` 可关闭截图输出。
- 以上改动保持 `cad-file-reader/v0` 契约不变，`scripts/cad_validate.sh` 校验仍需通过。

## 统一候选契约（cad-file-reader/v0）

装饰、安装、钢结构、市政和测量候选 JSON 会额外写入 `contract`：

- `candidates[]` 只放 `confirmed_evidence` 和 `inferred_candidate`；`review_candidates[]` 只放 `review_required`。
- `confirmed_evidence`：有直接文字、图层、几何、块或标注证据，且置信度 ≥ 0.90。
- `inferred_candidate`：由邻近关系、图层语义、块内容或规则推断，置信度 0.50–0.89。
- `review_required`：低置信、缺比例/单位/图层/块定义、文字绑定不明、几何冲突、重复、图框外或几何不完整；不进入默认汇总主线。
- `review_reasons[]` 使用标准英文词表，`review_notes` 保留中文说明；`source_schema` 固定为 `cad-file-reader/v0`，`final_quantity` 固定为 `false`。
- 交付或交接前可校验：`scripts/cad_validate.sh 输出.json`。
- **输出深度（用户可选）**：默认完整输出；追加 `--concise` 使用精简契约省 Token（候选只保留主干字段 id/类别/图层/文本/置信度/复核原因/来源文件）；`--full` 或 `--with-evidence` 恢复完整证据。环境变量 `CAD_CONCISE=1` 可全局设为精简默认。

## lis-skill-bus 推荐联动（不装自动降级）

> 好处：同一张 CAD 图只解析一次，本技能与五件套、其它算量技能共享同一份项目状态与识图契约；完全本地、不联网、不上云。
> 安装入口（跨平台）：先装 lis-skill-bus —— SkillHub slug：`lis-skill-bus`；GitHub：`lisong2003-lgtm/lis-skill-bus`。装完后运行安装器 `python install_py.py --apply`（只复制不注册 MCP：`SKIP_MCP_REG=1`）。
> **不装自动降级**：找不到 bus 时自动写 `$HOME/.codex/skills/.skillbus/state.json`，先跑通工作流，装好后无缝读取；五件套仍各自可用，功能不丢。

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

## 五件套联动契约（qto-project/v1 可选）
## 五件套联动契约（qto-project/v1 可选）

`cad-file-reader` 是五件套（土建/安装/装饰/园林算量）联动体系的**唯一共同底座**。联动契约、schema、校验器与目录约定都放本技能；四算量 skill 之间互不强依赖，只在同项目发现其他专业输出时做交叉核对，缺失即跳过并标占位，不要求五件全装。

- 主键三级来源：显式（`.qto/project.yaml`）→ 图内推断（`source=auto` + 证据）→ 文件级回退（`source=file`，置 `review_required=true`）。
- 项目目录约定：`.qto/project.yaml`、`识别/<专业slug>/`、`算量/<专业>/`（P1）、`汇总/`（P2）。
- 新输出为 `qto-project/v1`：在 `cad-file-reader/v0` 之上追加可选顶层字段 `qto_spec/project_key/draft_type/specialty/producer/placeholder`；旧 v0 输出零改动。
- 校验器：`scripts/qto_validate.sh <项目目录> [--report-json 报告.json]`，旧 v0 只 warning 不 fail，`regression_pass` 与 `precision_note` 分开统计。
- 生成/包装/占位工具：`scripts/qto_project.py init|wrap|placeholder`；`init --recognized` 支持一次多专业（例如 `--recognized tujian-suanliang anzhuang-suanliang`）。
- 端到端示例见 `README.md#五件套联动端到端示例`（识别→P1→P2→P3→validate 一条链）。
- P1 登记工具：`scripts/qto_p1_link.py`；P2 汇总工具：`scripts/qto_p2_summarize.py`（+`.sh`），只汇总各专业状态/候选数与缺口，不计算量。
- P3 交叉核对工具：`scripts/qto_p3_clash.py`（+`.sh`），按部位出同专业/多专业覆盖缺口与需人工核对清单，不计算量、不仲裁量值。
- 详细契约见 `docs/qto-linkage.md`；schema 见 `schemas/qto-project-v1.schema.json`；slug 映射见 `rules/skills-map.json`；自绘简化样例见 `examples/qto-sample/`。

## 图层/块语义与图纸对比

在 `cad_scan` 详情 JSON 上生成图层语义、块语义、块实例关联、MEP 端点/设备/立管关联候选和图纸变化候选；低置信或冲突项只进入 `review_candidates[]`，不进入默认汇总主线，也不改写工程量。

```bash
# P2/P3：图层与块语义候选；匿名/无语义块会标 missing_block_definition 或低置信推断
scripts/cad_semantics.sh 图纸详情.json --out-dir 语义识图 \
  --max-layers 2000 --max-blocks 2000 --max-instances 2000 --link-radius 3000

# 图例知识表候选（轻量词库：块名/图层/文字关键词匹配，不引视觉模型）
scripts/cad_legend.sh 图纸详情.json --out-dir 图例识图 --max-matches 2000

# P4：安装专业管段端点、设备、立管和系统冲突关联候选
scripts/cad_mep_geometry.sh 安装详情.json --out-dir 安装识图

# P5：同图重复对比应返回 0 变化；不同图输出图层/块/文字/几何增删与移动候选
scripts/cad_compare.sh 基准详情.json 目标详情.json \
  --out-dir 图纸对比 --tolerance 1.0 --max-changes 5000
```

图例候选沿用统一契约：`legend_matches` 输出专业、语义、命中关键词、块/图层/文字证据和 `discipline_refs`；`rules/legends.json` 内置 14 组关键词与 12 组符号指纹，块引用优先走符号指纹匹配，同名文本不重复抢占。语义与变化候选沿用统一契约：`semantic_layers`、`semantic_blocks`、`block_instances`、`mep_relations`、`drawing_changes`。候选可带可选 `rotation`（文字旋转角）、`confidence_scores`（证据子项强度）和 `discipline_refs`（跨专业视角），全部固定 `final_quantity=false`；专用技能必须自行核对后再做算量。旋转角参与位置分桶（0-180°按 5° 归一）：同一图框内同位置但旋转不同会拆为独立标注位置，旋转相同则按原规则合并。

## PDF 图纸（识图候选，本机分流 + 本地 OCR）

PDF 图纸先用本机 `pdf-inspector` 分类：文本型取原生文字，扫描/混合型用 `pdftoppm` 渲染后调本地 `image-ocr` 出线性文字候选。全部结果只作识图/文字候选，一律进 `review_candidates` 并标 `missing_layer/missing_unit/missing_scale`，不输出测量数量。

扫描/混合页候选的 OCR 像素框按渲染 dpi（默认 200，1in=72pt）换算成 `page_bbox`（PDF 点），并在候选上保留 `source_bbox_px` 供追溯。

矢量 PDF（`source_format=pdf_vector`）额外输出 `pdf_meta.vector_text_items`：原生文字 `x/y/width/height/font/font_size/page` 坐标候选，单位为 PDF 点，**仅作证据与分流，不参与测量**；可单独用 `scripts/cad_pdf_vec.sh 图纸.pdf --json vec.json` 复核。

图签栏提取为**版式优先 + 关键词兜底**：`pdf_meta.title_block` 优先扫描右下角图签栏区域（x>页面宽45%、y<页面高55%）命中字段，未命中字段再回退全量关键词；`page_bbox` 记录证据坐标，仅作元数据锚点，需人工核对。

```bash
# 分类 + 输出文字识图候选（文本型 / 扫描型 PDF 均可）
scripts/cad_pdf_ocr.sh 图纸.pdf --out-dir 图纸PDF识图

# 只分类不 OCR（先看是什么类型）
scripts/cad_pdf_ocr.sh 图纸.pdf --classify-only

# 扫描页并行数（默认3，建议≤CPU核心数）
scripts/cad_pdf_ocr.sh 图纸.pdf --workers 4 --out-dir 图纸PDF识图

# 自定义缓存目录；两级缓存（文件级 pdf 元数据 + 页面级 OCR 行结果）
scripts/cad_pdf_ocr.sh 图纸.pdf --cache-dir /tmp/pdf-cache --out-dir 图纸PDF识图

# 强制重新解析/渲染，忽略缓存
scripts/cad_pdf_ocr.sh 图纸.pdf --force --out-dir 图纸PDF识图
```

输出为 `*.pdf识图.json`（cad-file-reader/v0 契约）与同名 Markdown；可用 `scripts/cad_validate.sh 输出.json` 校验。公司图纸字节全程本机处理，不上云。

## 统一自测/回归闭环与发布预检

日常/CI 用 `scripts/self_test.sh` 跑“三合一”闭环（doctor 环境体检 → 全量
unittest → `schemas/*.schema.json` + `cad_validate.sh` 契约校验 → 样例 DXF 回归 →
坏文件快速失败不变量 → 可选真实 DWG 回归），输出 JSON + Markdown 报告：

```bash
bash scripts/self_test.sh                                    # 无真图时跑闭环，回归段记 skipped
bash scripts/self_test.sh --manifest <本地真图清单.json>      # 带真实 DWG 回归
bash scripts/self_test.sh --out-dir 报告输出目录 --json-only
```

发布前仍跑 `scripts/run_preflight.sh`：依次执行全量 self-test、契约样例校验、`cad_release_scrub.py` 脱敏扫描；带真图清单时加 `--manifest <本地真图清单.json>` 跑真实图纸回归。任一环节失败即视为未通过，禁止发布（本机自测现 205 项）。



## 快速读取

```bash
# 大图优先：构件编号、图层、关键词、图框
scripts/cad_scan.sh 图纸.dwg --only 梁,板,柱,墙 --cluster 1500 --format md -o 图纸扫描

# 关键词与原文证据
scripts/cad_scan.sh 图纸.dwg --search "板厚|C30|抗震等级|保护层|22G101"

# 需要识图几何和详情时
scripts/cad_scan.sh 图纸.dwg --only 梁,板,柱,墙 --with-mtext --with-geom \
  --cluster 1500 --detail-json 图纸详情.json --format all -o 图纸扫描

# 大图首次全量扫描并建本机证据缓存
scripts/cad_scan.sh 图纸.dwg --with-geom --with-geom-layer \
  --cache-dir /tmp/cad-file-reader-cache --format all -o 图纸扫描

# 同图重复查询：命中缓存后按图面矩形局部读取
scripts/cad_scan.sh 图纸.dwg --with-geom --with-geom-layer \
  --cache-dir /tmp/cad-file-reader-cache --roi 0,0,30000,20000 --format json -o 局部读取

# 省 Token：精简输出（默认完整；显式 --concise 精简候选主干，--full/--with-evidence 恢复完整）
scripts/cad_scan.sh 图纸.dwg --concise --format json -o 图纸精简

# 交付常用：同一结果同时导出 Markdown/JSON/CSV/Excel/Word
scripts/cad_scan.sh 图纸.dwg --only 梁,板,柱,墙 --cluster 1500 \
  --detail-json 图纸详情.json --format all -o 图纸扫描
# 单独导出 Excel 或 Word（需 --out 指定前缀）
scripts/cad_scan.sh 图纸.dwg --only 梁,板,柱,墙 --format xlsx -o 图纸扫描
scripts/cad_scan.sh 图纸.dwg --only 梁,板,柱,墙 --format docx -o 图纸扫描
# 同图重复查询：命中缓存后按图框编号局部读取
scripts/cad_scan.sh 图纸.dwg --with-geom --with-geom-layer \
  --cache-dir /tmp/cad-file-reader-cache --sheet 1 --format json -o 图框读取
```

## 批量识图台账（scripts/cad_batch.sh）

批量扫图输出候选级台账，复用 `cad_scan` 引擎：

```bash
scripts/cad_batch.sh 图纸目录 --out 台账 --glob "*.dwg;*.dxf" --recursive
scripts/cad_batch.sh 图纸目录 --out 台账 --resume        # 按 SHA-256 断点续跑
scripts/cad_batch.sh 图纸A.dwg 图纸目录 --out 台账 --glob "*.dxf" --cache-dir /tmp/cad-cache
```

- 输出 `<out>/识图台账.xlsx`：`识图台账` sheet 每候选一行，含 `复核原因 / 证据坐标 / 来源文件` 列，
  `review_required` / 置信度<0.5 / 复核原因非空的行黄底；每图一个 `汇总·图名` sheet 与整体 `图纸汇总` sheet
  （候选人 / 复核人 / 缺口）。
- 输出 `<out>/自检汇总.md`：逐图列出 可交付 / 需人工复核 / 失败跳过 / 缺输入。
- 单图失败不中断整批；`--resume` 用 `_state.json` 按源文件 SHA-256 跳过已成功图。
- 每图写入 `_contract/<图名>.json`（cad-file-reader/v0，逐候选 `final_quantity=false`），可 `scripts/cad_validate.sh 校验`。
- 大图仍走 `cad_scan` 的 `mem_guard`/时间预算；`--budget` 可调单图时间预算。

缓存键使用源文件 SHA-256 和影响证据内容的扫描参数档；`--roi`、`--sheet` 只做查询过滤。ROI 几何使用预归一化 bbox 索引，缓存写入先批量落库、延后建索引。JSON 的 `cache.hits/misses` 记录命中情况。局部结果只返回命中范围内的证据，不混入整图块统计。
缓存只保存识图证据，不保存最终工程量、扣减、材料量、造价或结算量。
JSON 汇总输出 `cache.read_ms/write_ms/db_files/db_bytes`；每个文件输出 `cache_read_ms/cache_write_ms/cache_bytes`。
缓存盘点/清理用 `scripts/cad_cache_admin.sh 缓存目录`：默认只读盘点；`--cleanup` 生成计划，`--apply` 才删除。temp/legacy 默认进入计划；corrupt/unknown 永不删除；current 默认保留，必须显式 `--include-current` 且提供 `--max-age-days` 或 `--max-total-mb`。

口径：`原文次数`不是根数；`--count-by auto`优先平法集中标注，缺集中标注退回标注位置去重。
`--with-geom`提供图面几何候选和证据；需要长度/面积/体积候选时再用 `cad_measure`，输出始终带 `final_quantity=false`。

## 测量候选（长度 / 面积 / 体积）

从 `cad_scan` 详情或装饰/安装/钢结构/市政识图 JSON 生成可追溯测量候选：

```bash
scripts/cad_measure.sh 描述几何/图纸详情.descriptive.json --out-dir 测量候选

# 显式覆盖比例/单位；缺比例或单位时保留图面值并转 review
scripts/cad_measure.sh 安装识图/安装详情.mep.json   --scale 1:100 --unit mm --coordinate-space model --out-dir 测量候选

# 已有面积候选且设计明确厚度时，生成待复核体积候选
scripts/cad_measure.sh 描述几何/图纸详情.descriptive.json --thickness-m 0.10 --out-dir 测量候选
```

输出 `cad-measurement-candidates.json/md/csv`，每条包含 `kind/value/unit/value_drawing_units/scale/space/basis/method/formula/status/confidence/review_reason/evidence/source_schema/source_id/final_quantity=false`。闭合多边形用鞋带公式，显式文字测量值可直接采用，外接框面积只作证据；MEP/钢结构/市政单段长度只作识图证据。方法、比例单位规则和专项交接见 `packs/measurement-candidates/SKILL.md`。

本层不输出最终工程量；扣减、重叠、做法、损耗、分账、清单量和材料量由专项算量 skill 负责。

## 装饰/安装/电气/钢结构/市政识图路由

专业识图统一入口见 `pack-index.md`（默认入口表）；各专业只输出识图候选，选量交给专项 skill。

| 专业 | 脚本 | 方法/边界 |
|---|---|---|
| 装饰 | `scripts/cad_descriptive_geometry.sh 详情.json --out-dir 描述几何` | `packs/descriptive-geometry/SKILL.md`；房间/洞口/做法候选，不直接出量 |
| 安装 | `scripts/cad_scan.sh 安装图.dwg ... --detail-json 安装详情.json` + `scripts/cad_mep_geometry.sh 安装详情.json` | `packs/mep-geometry/SKILL.md`；系统/路由/设备/立管候选，选量给 anzhuang-suanliang |
| 电气 | `scripts/cad_scan.sh 电气图.dwg ... --detail-json 电气详情.json` + `scripts/cad_electrical_geometry.sh` | `packs/electrical-geometry/SKILL.md`；回路/规格/防雷/消防/弱点候选；不展开芯数线长/负荷/照度 |
| 钢结构 | `scripts/cad_scan.sh 钢结构图.dwg ... --detail-json 钢结构详情.json` + `scripts/cad_steel_geometry.sh` | `packs/steel-geometry/SKILL.md`；构件/截面/连接/材料候选；重量涂装交专项 |
| 市政 | `scripts/cad_scan.sh 市政图.dwg ... --detail-json 市政详情.json` + `scripts/cad_municipal_geometry.sh` | `packs/municipal-geometry/SKILL.md`；道路/管网/桥梁/桩号/标高候选 |

## DWG 转 DXF

```bash
scripts/convert_dwg.sh 图纸.dwg --out 图纸.dxf
scripts/convert_dwg.sh 图纸目录 --recursive --out 输出目录
```

默认输出已存在不覆盖；大文件有 200MB 入口闸和内存看门狗，必要时才显式放开。

## 说明、规范与图集辅助

```bash
# 1. 抽取说明文字、标注和图纸参数
scripts/cad_scan.sh 图纸.dwg --with-mtext --with-geom \
  --detail-json 图纸详情.json --format json -o 图纸扫描

# 2. 解读构件规则、引用目录和缺失输入
scripts/cad_interpret.sh --scan 图纸扫描.json --detail 图纸详情.json \
  --rules rules --format all -o 图纸解读

# 3. 定位规范/图集元数据、版本风险、参数冲突和资料入口
scripts/cad_normative.sh --scan 图纸扫描.json --detail 图纸详情.json \
  --rules rules --format all -o 规范辅助
```

规范辅助输出：已索引/未索引编号、现行/旧版/待确认状态、知识库相对路径或在线入口、缺少的设计输入、多参数冲突。`rules/standards.json`只保存编号、名称、专业、状态和资料入口元数据；条文适用性以图纸指定版本和授权全文为准。

## 结构/总图场地/给排水暖通/精装修/幕墙/人防/预制装配识图路由

| 专业 | 脚本 | 方法/边界 |
|---|---|---|
| 结构 | `scripts/cad_scan.sh 结构图.dwg ... --detail-json 结构详情.json` + `scripts/cad_structural_geometry.sh` | `packs/structural-geometry/SKILL.md`；梁板柱墙/配筋/节点/轴网候选；方量钢筋交 tujian-suanliang |
| 总图场地 | `scripts/cad_scan.sh 总图.dwg ... --detail-json 总图详情.json` + `scripts/cad_site_geometry.sh` | `packs/site-geometry/SKILL.md`；红线/道路/停车/挡墙/土方候选；量交市政/土建 |
| 给排水暖通 | `scripts/cad_scan.sh 给排水图.dwg ... --detail-json 给排水详情.json` + `scripts/cad_hvac_plumbing_geometry.sh` | `packs/hvac-plumbing-geometry/SKILL.md`；管/风管/设备/支吊架候选；量交 anzhuang-suanliang |
| 精装修/室内 | `scripts/cad_interior_finish_geometry.sh` | `packs/interior-finish-geometry/SKILL.md` |
| 幕墙 | `scripts/cad_curtain_wall_geometry.sh` | `packs/curtain-wall-geometry/SKILL.md` |
| 人防 | `scripts/cad_civil_defense_geometry.sh` | `packs/civil-defense-geometry/SKILL.md` |
| 预制装配 | `scripts/cad_precast_geometry.sh` | `packs/precast-geometry/SKILL.md` |

各专业只做识图证据，不输出面积/长度/数量/体积/材料量或造价；统一契约与置信度分层见上文“统一候选契约”。本机真实回归用 `scripts/run_real_dwg_regression.sh --manifest 真图清单.json`，清单可写 `kind=electrical|structural|site|hvac_plumbing|interior_finish|curtain_wall|civil_defense|precast`，发布前脱敏。

## 结构算量的归属

原 `cad-file-reader` 内的梁、板、柱、墙、楼梯、洞口、预制底板、混凝土分账和结构算量流水线已迁移到：

- `tujian-suanliang`（本机目录 `shangwu-suanliang`）
- 统一入口：在土建算量技能目录执行其 `run_qty.sh` 命令（高级模式或流水线模式）。
- 迁移脚本仍通过 `CAD_SKILL_DIR` 调用本技能的 `cad_scan`/`cad_interpret` 识图底座。

本技能不再提供 `cad_quantity_pipeline.sh`、梁板柱墙混凝土方量、轴线面积、构件体积或材料量输出。

## 工作流

1. 识别 DWG/DXF/DWT 和大小；大图禁止直接全量实体树解析。
2. `cad_scan` 建立文字/图层/块名/图框/几何候选索引，保留原文证据。
3. 说明与规范任务运行 `cad_interpret` + `cad_normative`；装饰/安装/电气/钢结构/市政/结构/总图场地/给排水暖通/精装修幕墙人防预制识图读取对应 pack。
4. 需要算量时把识图结果交给 `tujian-suanliang`、`zhuangshi-suanliang`、`anzhuang-suanliang` 或对应专项 skill。
5. 同一张图重复查询优先复用已有 scan/detail/索引，不重复解析大图。

## 边界

- 不做设计合规审查、施工方案判断、清单计价、结算审计或规范条文解释。
- 测量候选不是最终工程量；专项算量 skill 必须继续完成扣减、重叠、做法映射、损耗、分账和台账。
- 不输出最终工程量、材料量、造价或结算量；只输出识图候选、几何证据、测量候选（`final_quantity=false`）和复核原因。
- 自动提取不能替代设计单位、翻样、清单编制和正式授权规范全文。
- 不把公司内部路径、项目结果或规范全文写入技能发布内容。

<!-- temp publish probe 2026-10-23: 仅用于诊断，发布后删除 -->
