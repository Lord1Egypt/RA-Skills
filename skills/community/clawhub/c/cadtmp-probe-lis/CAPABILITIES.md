# CAD File Reader 能力总览（能力/边界矩阵）

> 完整命令与专业路由见 `pack-index.md`；本文件只列“能做什么 / 不能做什么 / 边界”。
> 所有输出固定 `final_quantity=false`，本技能只做识图、证据、语义/拓扑/变化候选和测量候选。

## 能力矩阵

| 能力域 | 能做什么 | 边界 |
|---|---|---|
| 读取/转换 | DWG/DXF/DWT 直接读取（大图低内存 `cad_scan`、小图实体树 `read_cad`）；`convert_dwg.sh` 转 DXF（依赖 ezdwg，已随包/由 install_vendor 补齐） | 大图禁止盲目全量实体树；内存/CPU 受看门狗限制 |
| 大图缓存 | SQLite 单文件按源 SHA-256 + 参数档隔离；`--roi`/`--sheet` 局部读取；`cad_cache_admin.sh` 盘点/清理 | 只缓存识图证据，不缓存工程量；corrupt/unknown 永不删除 |
| 标注/解释 | 平法集中标注、截面、箍筋、抗震等级、保护层、做法关键词；`cad_interpret.sh` 绑定图框/构件范围 | 自动推断标为候选/推测，保留原文与坐标，不冒充确认 |
| 规范/图集 | `cad_normative.sh` 匹配 `rules/standards.json` 元数据；输出索引状态、版本风险、资料入口 | 只做资料定位与风险提示，不复制全文、不判定条文合规 |
| 图层/块语义 | `cad_semantics.sh` 图层/块/实例关联；`cad_legend.sh` 图例词库匹配（14 组词、12 组符号指纹） | 缺失/低置信进 `review_candidates`；不引视觉模型 |
| 图纸对比 | `cad_compare.sh` 对比基准/目标详情，输出图层/块/文字/几何增删与移动 | 同图重复对比应 0 变化；不解释工程量变化 |
| PDF 识图 | 本机 `pdf-inspector` 分流（vector/raster/hybrid）→ 原生文字或本地 OCR 线性候选；`cad_pdf_vec.sh` 坐标复核 | 识别/OCRead 结果全部进 review；单位 PDF 点，不参与测量 |
| 统一契约 | `contract=cad-file-reader/v0`；候选分高置信（`confirmed_evidence`）、推断（`inferred_candidate`）与需复核（`review_required`）三档（阈值见 SKILL.md），可 `cad_validate.sh` 校验 | 候选固定 `final_quantity=false`；不含最终量/造价 |

## 专业识图包（17 个）

| 专业 | 入口脚本 | 说明 |
|---|---|---|
| 装饰 | `cad_descriptive_geometry.sh` | 房间/洞口/做法候选 |
| 安装/MEP | `cad_mep_geometry.sh` | 系统/路由/设备/立管/拓扑候选 |
| 电气（消防/弱点/智能化） | `cad_electrical_geometry.sh` | 回路/规格/防雷/领域分组候选 |
| 钢结构 | `cad_steel_geometry.sh` | 构件/截面/连接/材料候选 |
| 市政 | `cad_municipal_geometry.sh` | 道路/管网/桥隧/桩号/坐标候选 |
| 结构 | `cad_structural_geometry.sh` | 梁板柱墙/配筋/轴网候选；量交 tujian-suanliang |
| 总图/场地 | `cad_site_geometry.sh` | 红线/道路/挡墙/土方候选；量交市政/土建 |
| 给排水/暖通 | `cad_hvac_plumbing_geometry.sh` | 管/风管/设备/支吊架候选 |
| 精装修/室内 | `cad_interior_finish_geometry.sh` | 饰面/做法/标高/节点候选 |
| 幕墙 | `cad_curtain_wall_geometry.sh` | 立柱/面板/预埋/分格候选 |
| 人防 | `cad_civil_defense_geometry.sh` | 防护门/通风/电气候选 |
| 预制装配 | `cad_precast_geometry.sh` | 预制构件/预埋/连接候选 |
| 桥梁/隧道/道路 | `cad_bridge_tunnel_road_traffic.sh` | 桥墩/桥台/洞口/路线/交通设施候选 |
| 桩基/基坑/边坡 | `cad_pile_foundation_slope.sh` | 桩位/支护/锚索/挡墙/监测候选 |
| 门窗/楼梯/保温/防水 | `cad_doors_windows_stairs_insulation_waterproof.sh` | 门窗/楼梯/保温/防水候选 |
| 防火/无障碍/绿建 | `cad_fire_prevention_accessibility_green_energy.sh` | 防火分区/疏散/绿建候选 |
| 测量候选 | `cad_measure.sh` | 长度/面积/体积候选，保留计算式与证据 |

## 交付与复核

- Markdown / JSON / CSV / Excel / Word 报告；重要流水线带 manifest 和 SHA-256。
- 报告必须说明证据来源、自动推断、需回图项和授权全文核对项。
- 重复查询复用已有 scan/detail/索引，不改已有锁定基线。

## 硬边界

- 不替代翻样、下料、清单计价、结算、设计合规审查和规范条文解释。
- 不输出最终工程量、体积、面积、材料量、造价或结算量。
- 公司项目路径、内部结果和规范全文不得进入技能发布内容。
- 算量交给专项 skill（土建 → tujian-suanliang，装饰/安装 → 对应专项）。

- 园林景观识图：种植总平面/苗木表/铺装详图类型；苗木图例乔灌地被分类、植物名坐标证据；设计院图例快速校准（`cad_landscape_calibrate` 生成按院别 `plant_block_aliases` 覆盖）；对无意义块名做几何图例指纹兜底（大圆=乔木/多圆=灌木/条带=地被，`plant_block_fingerprints`）；硬景铺装图层闭合域轻量检测候选（含细缝尺度过滤、相邻环区块聚合与按区块复核锚点，独立环数/区块范围，final_quantity=false，不输出数量/面积/造价）；支持 `--with-block-geom` 块内几何指纹与 mm/m 单位自动归一；DWG 块名解码为空/乱码时可用 `--dwg-dxf-fallback` 自动转 DXF 复扫（含 cad_landscape_pdf.sh 园林 PDF 苗木文字+规格识别）。
