# 专业识图路由（完整表，原 SKILL.md 内容）

## 装饰/安装/电气/钢结构/市政识图路由

专业识图统一入口见 `pack-index.md`（默认入口表）；各专业只输出识图候选，选量交给专项 skill。

| 专业 | 脚本 | 方法/边界 |
|---|---|---|
| 装饰 | `scripts/cad_descriptive_geometry.sh 详情.json --out-dir 描述几何` | `packs/descriptive-geometry/SKILL.md`；房间/洞口/做法候选，不直接出量 |
| 安装 | `scripts/cad_scan.sh 安装图.dwg ... --detail-json 安装详情.json` + `scripts/cad_mep_geometry.sh 安装详情.json` | `packs/mep-geometry/SKILL.md`；系统/路由/设备/立管候选，选量给 anzhuang-suanliang |
| 电气 | `scripts/cad_scan.sh 电气图.dwg ... --detail-json 电气详情.json` + `scripts/cad_electrical_geometry.sh` | `packs/electrical-geometry/SKILL.md`；回路/规格/防雷/消防/弱点候选；不展开芯数线长/负荷/照度 |
| 钢结构 | `scripts/cad_scan.sh 钢结构图.dwg ... --detail-json 钢结构详情.json` + `scripts/cad_steel_geometry.sh` | `packs/steel-geometry/SKILL.md`；构件/截面/连接/材料候选；重量涂装交专项 |
| 市政 | `scripts/cad_scan.sh 市政图.dwg ... --detail-json 市政详情.json` + `scripts/cad_municipal_geometry.sh` | `packs/municipal-geometry/SKILL.md`；道路/管网/桥梁/桩号/标高候选；0.39.0+ 提取圆实体（井圈/阀门/消火栓，`--with-geom` 自动，标注层/图例区/微圆三层剔除） |

## 结构/塔吊布置/总图场地/给排水暖通/精装修/幕墙/人防/预制装配识图路由

| 专业 | 脚本 | 方法/边界 |
|---|---|---|
| 结构 | `scripts/cad_scan.sh 结构图.dwg ... --detail-json 结构详情.json` + `scripts/cad_structural_geometry.sh` | `packs/structural-geometry/SKILL.md`；梁板柱墙/配筋/节点/轴号候选 + **几何轴网**（`axis_nets`，给跨专业核对用）；方量钢筋交 tujian-suanliang |
| 塔吊布置 | `scripts/cad_crane_geometry.sh 图纸.dxf --drawing-unit mm --out-dir 塔吊识图`（也可给 DWG 或 `cad_scan --detail-json` 产物） | `packs/crane-layout/SKILL.md`；INSERT 仿射回转中心、型号/臂长候选；圆只作旁证，不选型/验算 |
| 总图场地 | `scripts/cad_scan.sh 总图.dwg ... --detail-json 总图详情.json` + `scripts/cad_site_geometry.sh` | `packs/site-geometry/SKILL.md`；红线/道路/停车/挡墙/土方候选；量交市政/土建 |
| 给排水暖通 | `scripts/cad_scan.sh 给排水图.dwg ... --detail-json 给排水详情.json` + `scripts/cad_hvac_plumbing_geometry.sh` | `packs/hvac-plumbing-geometry/SKILL.md`；管/风管/设备/支吊架候选；量交 anzhuang-suanliang |
| 精装修/室内 | `scripts/cad_interior_finish_geometry.sh` | `packs/interior-finish-geometry/SKILL.md` |
| 幕墙 | `scripts/cad_curtain_wall_geometry.sh` | `packs/curtain-wall-geometry/SKILL.md` |
| 人防 | `scripts/cad_civil_defense_geometry.sh` | `packs/civil-defense-geometry/SKILL.md` |
| 预制装配 | `scripts/cad_precast_geometry.sh` | `packs/precast-geometry/SKILL.md` |

各专业只做识图证据，不输出面积/长度/数量/体积/材料量或造价；统一契约与置信度分层见上文“统一候选契约”。本机真实回归用 `scripts/run_real_dwg_regression.sh --manifest 真图清单.json`，清单可写 `kind=electrical|structural|site|hvac_plumbing|interior_finish|curtain_wall|civil_defense|precast`，发布前脱敏。
