# cad-file-reader 详细说明（由 SKILL.md 原样外移）

> 2026-11-10 瘦身：只搬未删。SKILL.md 保留硬规则、入口闸门、边界与口径摘要；命中下列主题时按需读取本文对应小节。

## 安装与依赖

- 完整包解压即用；SkillHub 轻量包一条命令：`bash scripts/setup.sh`（幂等，先自动补回下载包可执行位，再自动补齐依赖）。
- **运行时自动自举**：任意 `run_cad.sh` 入口启动时先调 `scripts/ensure_runtime.sh`，检测到 vendor 缺失自动补齐（默认公共 PyPI 零配置安装 ezdwg/ezdxf/fonttools/pyparsing/numpy；设置 `CAD_FILE_READER_REPO=<owner>/<repo>` 时改走 GitHub Release 完整包并做 SHA-256 校验，校验失败回退公共 PyPI；设 `CAD_AUTO_SETUP=0` 关闭并明确报错）；vendor 已存在则不联网、不重复下载。
- 依赖自检：`bash scripts/deps_check.sh --minimal`；缺 numpy 只影响梁线几何估算，其余功能降级为 review。
- **环境体检（只读，不自动安装）**：`bash scripts/doctor.sh` 一条命令输出分档结论（档0 当前哪几项可用/缺哪些，档1 每项缺失的最小修复命令，档2 DWG 缺 LibreDWG/ODA 转换后端时的下一步）。默认写 `doctor-report.json` + `doctor-report.md` 到当前目录，stdout 再打一份人类可读摘要；`--json-only` / `--md-only` / `--no-write` 供自动化或自测用。
- 30 秒样例：`bash scripts/demo.sh`；完整包用内置 `examples/sample_room.dxf`，SkillHub 轻量包若含 `.dxf` 则由 `scripts/generate_sample.py` 现场重建同一样例（跑识图→测量→契约校验）。

## 平台支持矩阵

支持 macOS / Windows 10–11 / Linux x86_64，核心能力一致；Windows SkillHub 轻量包无 `.cmd` 时改用同目录 `.py`，或装 GitHub 完整包。DWG→DXF 复扫、PDF OCR 属可选后端。完整矩阵与安装 FAQ 见 [README.md](README.md)。

## lis-skill-bus 契约联动（算量链必须安装）

- CAD 可独立识图；土建/安装/装饰/园林/钢结构算量链必须经 bus 复用 `cad-contract/v1`，bus 缺失时停止算量链并提示安装；已有契约输入时仍只消费契约，不自行解图。
- 最短入口：`scripts/cad_statesync.sh push ...` 发布，`scripts/cad_statesync.sh pull ...` 取最近契约。
- 安装、路径优先级、核心 section 和 Windows 用法见 `docs/bus-integration.md`。

## 五件套联动契约（qto-project/v1 可选）

本技能是土建/安装/装饰/园林四算量的**唯一共同底座**；四算量互不强依赖，只在同项目发现他专业输出时交叉核对，缺失即跳过并标占位。

- 主键三级：显式 `.qto/project.yaml` → 图内推断（`source=auto`+证据）→ 文件级回退（`source=file`，`review_required=true`）。
- 新输出 `qto-project/v1` 在 v0 上追加可选字段 `qto_spec/project_key/draft_type/specialty/producer/placeholder`，旧 v0 零改动。
- 工具：`scripts/qto_validate.sh`（校验）、`qto_project.py init|wrap|placeholder`、`qto_p1_link.py`、`qto_p2_summarize.py`、`qto_p3_clash.py`；P2/P3 只汇总与核对，不算量、不仲裁量值。
- 完整摘要与端到端示例：`docs/qto-linkage.md`；schema `schemas/qto-project-v1.schema.json`；slug 映射 `rules/skills-map.json`；样例 `examples/qto-sample/`。

## 结构/园林块几何上移（0.41.0）

- 结构：先 `cad_scan 结构图.dwg --with-mtext --with-insert --with-geom --with-geom-layer --with-block-expand --detail-json 结构详情.json`，再跑 `cad_structural_geometry`。详情 JSON 的 `block_geometry[].segments[]` 才带块内 LINE/LWPOLYLINE；结构输出追加 `category=raw_geometry` 行、`blocks[]`、`units`、`review[]`。未开 `--with-block-expand` 时只给 `block_geometry_unavailable` 复核项，不伪造块内几何。
- 园林：`cad_landscape_geometry --block-paving 景观图.dxf --block-refs 景观图.dxf --out-dir 园林识图` 可只读 DXF 直接生成块内铺装环与顶层块引用；也可与 cad_scan 详情 JSON 位置参数并用。块内铺装固定 P3/`confidence=0.4`、`final_quantity=false`、`review_note=块内推定`，面积只写 `area_drawing_units2`，不冒充 m²。
- 块内几何是复核候选，不替代设计确认、比例/单位核对、现场量测或专项算量；真实工程图默认只在本机只读处理；未经用户明确范围、字节与同意，不外发。

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

先用本机 `pdf-inspector` 分类：文本型取原生文字，扫描/混合型用 `pdftoppm` 渲染后调本地 `image-ocr`。结果只作识图/文字候选，一律进 `review_candidates` 并标 `missing_layer/missing_unit/missing_scale`，不输出测量数量。矢量 PDF 的 `pdf_meta.vector_text_items` 仅作证据，不参与测量；图签栏提取为版式优先 + 关键词兜底，需人工核对。公司图纸默认本机处理；未经用户明确范围、字节与同意，不把图纸字节交给云端模型、在线 OCR/转换或第三方服务。dpi 换算、缓存与全部命令见 `docs/pdf-pipeline.md`。

## 统一自测/回归闭环与发布预检

发布前必须跑 `bash scripts/run_preflight.sh`；它串起 `self_test`、契约样例校验和 `cad_release_scrub.py` 脱敏扫描，带真图清单时追加真实 DWG 回归。任一非跳过环节失败即禁止发布。完整命令、用例说明和跳过规则见 [README.md](README.md)。


## 快速读取

大图先 `scripts/cad_scan.sh 图.dwg --only 梁,板,柱,墙 --cluster 1500`；关键词与原文证据用 `--search`；要几何/详情加 `--with-mtext --with-geom`；同图重复查询加 `--cache-dir`，再按 `--roi` 或 `--sheet` 局部读；交付用 `--format all|xlsx|docx`。完整命令、缓存与 `--concise` 省 token 开关见 `docs/quick-scan.md`。

## 批量识图台账

`scripts/cad_batch.sh 图纸目录 --out 台账 --resume` 逐图写入 v0 契约、复核原因和失败台账，单图失败不中断。完整参数、输出与缓存说明见 `docs/batch-workbook.md`。

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

## 转换与规范辅助

- DWG 转 DXF / 批量转换：`scripts/convert_dwg.sh`（默认不覆盖已有输出，200MB 入口闸 + 内存看门狗）。
- 说明/构件规则初解：`scripts/cad_interpret.sh`；规范/图集元数据与输入缺口：`scripts/cad_normative.sh`——只出元数据与风险提示，不出条文符合性结论。
- 完整命令与参数见 `docs/conversion-and-normative.md`。

## 专业识图路由

所有专业包统一按 `pack-index.md`（默认入口表）选包：结构、塔吊布置、总图场地、给排水暖通、精装修/室内、幕墙、人防、预制装配、装饰、安装、电气、钢结构、市政、园林——每行给出脚本、`packs/<name>/SKILL.md` 与边界。完整对照表见 `docs/domain-routing-full.md`。

各专业只出识图证据，不输出面积/长度/数量/体积/材料量或造价；统一契约与置信分层见上文「统一候选契约」。本机真实回归用 `scripts/run_real_dwg_regression.sh --manifest 真图清单.json`（`kind=electrical|structural|site|hvac_plumbing|interior_finish|curtain_wall|civil_defense|precast`），发布前脱敏。

## 塔吊布置识图（crane-layout）

```bash
scripts/cad_crane_geometry.sh 图纸.dxf --drawing-unit mm --out-dir 塔吊识图
# 也可直接给 DWG；或给 cad_scan --detail-json 产物并加 --source-drawing 原图
```

- 总图场地包输出 `site_geometry[]`，含 `building_outline`（建筑屋顶/地下室外轮廓）、`site_boundary`、`road`、`retaining_wall` 等图层候选；轮廓是否为主楼、是否闭合仍要下游确认。
- 输出 `*.crane.json/md/csv`：`crane_layout[]`（兼容别名 `towers[]`）含 `crane_id`、块名/图层/句柄、`insert_xyz_mm`、`center_xy_m`、旋转/缩放、型号与臂长候选、圆旁证和证据坐标。
- `center_xy_m` 必须由 INSERT 仿射变换（块基点+平移+旋转+缩放）得到；DWG 直读拿不到块基点时保持 `null` 并进 review，优先用 DWG→DXF 副本或 `cad_scan --dwg-dxf-fallback --detail-json`，不伪造中心。
- 型号只认块名或塔吊图层/标签附近的明确文字；臂长只认“臂长/起重臂长”，排除“幅度/工作半径/R=”；圆只进 `radius_circles_m`，`used_as_jib_length=false`。
- 不选型、不验算、不判断覆盖/吊重/基础/附着/群塔防碰撞，不输出塔吊数量结论或施工方案；`final_quantity=false`。完整规则见 `packs/crane-layout/SKILL.md`。

## 跨图聚合 / 图纸关系 / 钢筋牌号

多图聚合、轴网核对和钢筋牌号回填按需读取 `packs/cross-drawing-aggregation/SKILL.md`。硬边界不变：牌号只来自本批图纸说明表，映射不跨项目；`bridged` 推断不得混作 `direct` 原文证据。

## 结构算量的归属

原 `cad-file-reader` 内的梁、板、柱、墙、楼梯、洞口、预制底板、混凝土分账和结构算量流水线已迁移到：

- `tujian-suanliang`
- 统一入口：在土建算量技能目录执行其 `run_qty.sh` 命令（高级模式或流水线模式）。
- 迁移脚本仍通过 `CAD_SKILL_DIR` 调用本技能的 `cad_scan`/`cad_interpret` 识图底座。

本技能不再提供 `cad_quantity_pipeline.sh`、梁板柱墙混凝土方量、轴线面积、构件体积或材料量输出。

## 工作流

1. 识别 DWG/DXF/DWT 和大小；大图禁止直接全量实体树解析。
2. `cad_scan` 建立文字/图层/块名/图框/几何候选索引，保留原文证据。
3. 说明与规范任务运行 `cad_interpret` + `cad_normative`；装饰/安装/电气/钢结构/市政/结构/塔吊布置/总图场地/给排水暖通/精装修幕墙人防预制识图读取对应 pack。
4. 需要算量时把识图结果交给 `tujian-suanliang`、`zhuangshi-suanliang`、`anzhuang-suanliang` 或对应专项 skill。
5. 同一张图重复查询优先复用已有 scan/detail/索引，不重复解析大图。

