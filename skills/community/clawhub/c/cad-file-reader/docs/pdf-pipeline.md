# PDF 图纸流水线（识图候选）

原 SKILL.md 章节，按需查阅。

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

输出为 `*.pdf识图.json`（cad-file-reader/v0 契约）与同名 Markdown；可用 `scripts/cad_validate.sh 输出.json` 校验。公司图纸默认本机处理；未经用户明确范围、字节与同意，不把图纸字节交给云端模型、在线 OCR/转换或第三方服务。

