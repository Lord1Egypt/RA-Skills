# Landscape Geometry / 园林景观识图中间数据包

本包把园林/景观施工图（种植总图、苗木表、铺装、硬景、水景、家具图纸）读成“园林专项可复核”的识图候选。

只做识图和证据提取，不输出苗木数量、铺装面积、土方量、材料量、造价或结算量；`contract.final_quantity=false`。

## 触发
- 需要识别园林图纸类型：种植总平面、苗木表、景观总平面、铺装平面/详图、景墙/坐凳/花钵/廊架/亭详图。
- 需要苗木图例候选：乔/灌/地被/其他植物名带坐标证据。
- 需要硬景铺装闭合域候选：铺装图层几何闭环检测候选。
- 需要水景、家具等硬景构件候选。

## 快速审计
## 设计院图例快速校准（用户提供不同设计院图纸）
用户拿到某设计院新图纸后，不需要人工改整个词库，只跑两条命令即可生成该院覆盖：

```bash
# 1) 扫描该院图纸（必须 --with-insert --with-blocks，块名才是来源）
scripts/cad_scan.sh 该院图纸.dwg --with-mtext --with-insert --with-blocks   --detail-json 该院校准输入.json --format json -o 扫描

# 2) 自动建议 block 名→乔/灌/地被/其他 覆盖，并写 institutes/<该院>.json
scripts/cad_landscape_calibrate.sh 该院校准输入.json --institute 该院 --write-override

# 3) 之后园林识图按院别复用
scripts/cad_landscape_geometry.sh 该院详情.json --institute 该院 --out-dir 园林识图
```

校准产物：
- `校准输出/*.calibrate.json`：逐块名建议（含实例数、置信度、证据、status）。
- `packs/landscape-geometry/institutes/<该院>.json`：只写“块名→分类”覆盖，运行时可被 `--institute` 合并进词库。
- 人工只需复核自动建议；`suggested_category=""` 的块名需补写后再 `--write-override`。

```bash
scripts/cad_scan.sh 景观图.dwg --with-mtext --with-insert --with-geom --with-geom-layer \
  --detail-json 景观详情.json --format json -o 景观扫描
scripts/cad_landscape_geometry.sh 景观详情.json --out-dir 园林识图
```

输入必须是 `cad_scan --with-geom --with-geom-layer` 的详情 JSON（带图层原图效果最佳；t3 精简版图层名为空时苗木图例仍可识别，铺装闭合域降级为 review）。需要块定义内部几何时加 `--with-block-geom`（DXF 优先，DWG 需先转 DXF）。

## 识别范围
- 图纸类型：种植总平面、苗木表、景观总平面、铺装平面/详图、硬景详图。
- 系统：种植、铺装、水景、家具。
- 苗木图例候选：按植物名/图层命中分乔木、灌木、地被、其他，带原文、图层（若有）与坐标证据。
- 块/图例植物候选：按块名与 `plant_block_aliases`/`plant_block_tokens` 将设计院图例代号映射到乔/灌/地被/其他，带引用次数证据（`plant_block_aliases` 可按具体设计院继续校准）。
- 几何图例指纹候选：块名映射不命中时优先使用 `--with-block-geom` 提取的块定义内部几何，其次对多次插入的同名块吸收其附近几何做形状指纹（大圆+中心点→乔木，多圆团簇→灌木，连续长条带→地被/绿篱）；按 `plant_layer_tokens` 做图层闸门性能保护，单位/mm-m 自动归一化阈值；多个实例投票、支持度不足降级 review，结果写入 `plant_block_fingerprints`（需 `--with-insert --with-geom --with-geom-layer`）。
- 铺装闭合域候选：对 `景观铺地/铺装/园路/波打/收边` 等图层几何做轻量闭环检测，闭合成功标 candidate；细缝/装饰小环按尺度过滤进 `filtered_ring_candidates`，相邻合规环聚合成带 `review_label`/`anchor_center` 的 `region_candidates` 便于按区块复核；缺图层或无法成环标 review（`incomplete_geometry`/`missing_layer`）。
- 硬景构件候选：景墙、坐凳、花钵、廊架、亭、汀步、台阶、水景、雕塑等文字候选。

## PDF 输入
PDF 图纸可用同一套园林识图入口，但只有“文字候选 + 矢量几何 review 证据”：

```bash
# 矢量/混合/扫描 PDF（本机 cad_pdf_ocr 分流）
scripts/cad_landscape_pdf.sh 景观图纸.pdf --out-dir 园林识图pdf
# 只处理部分页，避免大 PDF 资源占用
scripts/cad_landscape_pdf.sh 景观图纸.pdf --pages 1,3-5 --out-dir 园林识图pdf
# 复用已有 cad_pdf_ocr json（不重复 OCR）
scripts/cad_landscape_pdf.sh 已有.pdf识图.json --out-dir 园林识图pdf
```

- 矢量 PDF 用 `pdf_meta.vector_text_items` 坐标出苗木图例/系统/图纸类型；扫描/混合页回落 OCR bbox 中心。
- 矢量几何量由 `cad_pdf_geometry.py`（pdfminer）以 `pdf_geometry_candidates` 输出，固定 `status=review`、`review_reason=pdf_no_layer_geometry`；无图层语义，**不参与铺装/绿地闭合域、不参与算量**。
- 全链路输出 `final_quantity=false`。

## 苗木图例清洗与字符兜底
- 苗木/植物图例文字自动拆成 植物名 + 规格：`苗木图例 1-10 香樟 φ15cm` → 香樟 + φ15cm；没拆出种名时保留原文。
- 英文/ASCII 图例词兜底（`plant_english_aliases`）：tree/shrub/groundcover/lawn/grass 等按乔/灌/地被候选，海外或转码丢中文的图纸也可复核。
- 硬景构件词库含铺装材料（透水砖/花岗岩/青石板/木平台/防腐木/艺术地坪等）。

## PDF 批量
`cad_landscape_pdf` 支持多个 PDF/JSON 或目录：`scripts/cad_landscape_pdf.sh 目录 --out-dir 园林识图pdf` 会递归收 PDF，多文件按 `<茎>.landscape.*` 分开输出并生成 `_batch_summary.json`；单文件用法不变。

## 扫描版 PDF
位图/扫描 PDF 走同一条 `cad_landscape_pdf`：`cad_pdf_ocr` 渲染+本地 OCR，OCR 文字行 bbox 中心转 PDF 点坐标后进 landscape；错字属 OCR 固有噪声，标 missing_layer 进入 review，`final_quantity=false`（无矢量几何，`pdf_geometry_candidates=0`）。

## 文字图例校准闭环
`cad_landscape_calibrate` 会把未分类植物词（`audit.top`）初判为乔/灌/地被/其他并给 `text_word_suggestions`；`--write-text-words` 只把 conf≥0.8 的植物名词自动并入该院 `plant_trees/shrubs/groundcover/other`，配合 `--verify` 一轮完成“审计→提词→写入→复验”，不确定词仍进 review。

## 快速校准复验
`cad_landscape_calibrate --write-override --verify` 会在写入 `institutes/<院>.json` 后自动用该院覆盖复验，输出 `calibrate_verify.json`（before/after 分类变化），免手工二次识图。

## 词库覆盖审计
输出的 `audit.unclassified_legend_words` / `audit.top` 列出“带种植/图例上下文但没分到类”的候选词频（如新设计院植物名），方便补 `rules.json` 或按 `cad_landscape_calibrate` 校准；只审计词库覆盖，不算量。

## 边界
- 不计算苗木数量、铺装面积、土方量、水景面积、材料量、造价或结算量。
- 闭环检测是轻量几何候选，不替代设计复核、放线、点数和现场核对。
- 缺几何、缺图层、无法成环时进入 `review`，不输出到默认汇总主线。
