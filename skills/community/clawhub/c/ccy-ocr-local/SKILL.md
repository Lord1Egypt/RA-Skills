---
name: ccy-ocr-local
description: 本地 OCR / 图表识别技能。对本机图片做离线文字识别，支持截图、文档图片、扫描件、表格/图表图片中的中英文文本与图表数据提取；默认不上传文件、不依赖外部 API。
---

# ccy-ocr-local

本技能用于**本地离线 OCR 与图表结构化识别**。默认只处理本机文件，不上传图片，不调用外部 API。

## 什么时候使用

- 用户给出本机图片、截图、扫描件，要求识别文字
- 用户给出图表图片，要求提取标题、标签、数值或粗略结构化数据
- 需要批量 OCR 多张图片，并保存 txt/json/tsv 结果

## 快速路径

技能目录：`skills/ccy-ocr-local/`

### 普通 OCR

```bash
python3 skills/ccy-ocr-local/scripts/local_ocr.py <image_path> --lang chi_sim+eng
```

常用参数：

- `--json`：输出内容和元数据
- `--format tsv`：输出带坐标/置信度的 TSV
- `--autorotate`：自动尝试方向
- `--doc-hint label`：标签、票据、短文本图片优先用这个
- `--multi-variant`：多预处理候选搜索，慢一些但更稳
- `--mode accurate`：更适合追求准确率的单张图片
- `--batch --out-dir <dir>`：目录批处理并生成 `manifest.json`

JSON 输出会包含 `avg_conf`、`low_conf_words`、`quality_warning` 和 `suggestions`，用于判断是否需要重跑或人工复核。

示例：

```bash
python3 skills/ccy-ocr-local/scripts/local_ocr.py image.png --lang chi_sim+eng --autorotate --json
python3 skills/ccy-ocr-local/scripts/local_ocr.py images/ --batch --recursive --out-dir ocr-out --lang chi_sim+eng
```

### 图表识别

```bash
python3 skills/ccy-ocr-local/scripts/chart_ocr.py <image_path> --chart-type auto --json
```

支持 `auto | pie | bar | line | table | dashboard`。

示例：

```bash
python3 skills/ccy-ocr-local/scripts/chart_ocr.py chart.png --chart-type dashboard --json
python3 skills/ccy-ocr-local/scripts/chart_ocr.py chart.png --chart-type bar --extract-numbers --extract-labels --json
python3 skills/ccy-ocr-local/scripts/chart_ocr.py chart.png --chart-type auto --visualize --visualize-output chart_debug.png --json
```

`--visualize` 会生成调试标注图：灰框为候选区域，橙/红框为选中图表或 dashboard 子图区域。

## 依赖

- Python 3
- Tesseract 可执行文件
- Python 包：`pillow pytesseract opencv-python numpy`
- 中文识别需要 Tesseract 语言包 `chi_sim`；英文只需 `eng`

检查语言包：

```bash
tesseract --list-langs
```

如果 tesseract 不在 PATH，可用：

```bash
python3 skills/ccy-ocr-local/scripts/local_ocr.py image.png --tesseract-cmd /path/to/tesseract
```

或设置 `TESSERACT_CMD` 环境变量。

## 输出与判断

- 普通 OCR 输出以 Tesseract 结果为准；图片质量、字体、分辨率、语言包会显著影响效果。
- 图表识别是“OpenCV 结构线索 + OCR 文本”的规则/启发式提取，适合常见饼图、柱状图、折线图、表格和 dashboard 粗提取；不要把结果当作人工校验后的精确数据。
- 图表 JSON 会包含 `quality_notes`；如果提示低置信，优先查看 `--visualize` 调试图，并考虑裁剪图表主体或手动指定 `--chart-type`。
- 若结果差，优先尝试：`--autorotate`、`--multi-variant`、`--mode accurate`、提高图片分辨率、换 `--psm`、确认语言包。

## 持续提升准确率

如果要让这个技能在真实业务图片上越来越准，按下面顺序迭代。不要只凭单张样例调参，先建样本和评测。

### 1. 建真实样本集

把实际会遇到的图片按类型放到固定目录，例如：

```text
skills/ccy-ocr-local/assets/eval/
├── text/          # 普通文档、截图、票据、标签
├── label/         # 短文本标签、产品标签、物流标签
├── chart-bar/     # 柱状图
├── chart-line/    # 折线图
├── chart-pie/     # 饼图
└── dashboard/     # 多图表看板
```

每张图片旁边放一个同名 `.expected.json`，记录人工校验后的期望结果。建议字段：

```json
{
  "type": "text",
  "lang": "chi_sim+eng",
  "expected_text": "人工校验后的完整文字",
  "important_terms": ["供应商", "数量", "软头镊子"],
  "expected_numbers": [123, 45.6]
}
```

图表样本建议记录：

```json
{
  "type": "chart-bar",
  "chart_type": "bar",
  "title": "月度产量",
  "labels": ["1月", "2月", "3月"],
  "values": [120, 160, 150]
}
```

### 2. 固定评测指标

普通 OCR 建议看：

- 字符准确率：人工文本 vs OCR 文本
- 关键字段命中率：`important_terms` 是否识别出来
- 数字准确率：金额、数量、型号等是否识别正确
- 平均置信度：JSON 里的 `avg_conf`、`low_conf_words`

图表识别建议看：

- 图表类型准确率：`bar / line / pie / table / dashboard`
- 标题/图例命中率
- 数值误差：提取值和期望值的绝对/相对误差
- 区域检测是否正确：结合 `--visualize` 调试图人工抽检

### 3. 用质量字段决定是否重跑

普通 OCR 的 JSON 会输出：

- `avg_conf`：平均置信度，低于 55 通常要复核
- `low_conf_words`：低置信词数量，越多越不稳
- `quality_warning`：低质量原因
- `suggestions`：建议重跑参数

低质量时优先重跑：

```bash
python3 skills/ccy-ocr-local/scripts/local_ocr.py image.png \
  --lang chi_sim+eng \
  --autorotate \
  --multi-variant \
  --mode accurate \
  --json
```

标签、票据、短文本图片加：

```bash
--doc-hint label
```

### 4. 按类型调参，不要全局乱改

推荐调参顺序：

1. 确认语言包：中文图片必须有 `chi_sim`，中英混排用 `chi_sim+eng`
2. 尝试 PSM：常用 `6`、`7`、`11`、`3`
3. 尝试预处理：`--multi-variant`、`--sharpen`、提高 `--min-edge`
4. 尝试旋转：`--autorotate --autorotate-strategy full`
5. 对稳定错字加入领域纠错：编辑 `DOMAIN_CORRECTIONS`
6. 对某类图片固定最佳参数：在调用侧按目录/文件名选择 `--doc-hint`、`--psm`、`--mode`

### 5. 图表准确率提升路径

图表识别优先这样做：

1. 先用 `--visualize` 确认图表区域是否选对
2. 区域错了：优化 `_find_chart_regions` / `_classify_region`
3. 类型错了：补关键词、线条/圆形/表格判定规则
4. 文本错了：优化标题、坐标轴、图例 OCR 配置
5. 数值错了：优先做几何反推，而不是只依赖 OCR
   - 柱状图：检测柱子矩形高度 + 坐标轴刻度映射
   - 折线图：检测折线点位 + 坐标轴刻度映射
   - 饼图：检测扇区角度 + 图例/百分比匹配

### 6. 每次提升后都跑回归

修改代码或参数后至少运行：

```bash
python3 skills/ccy-ocr-local/scripts/regression.py
python3 skills/ccy-ocr-local/scripts/test_chart_ocr.py
```

如果增加了真实样本集，建议再补一个专门的 eval 脚本，输出每次修改前后的准确率变化。只有评测变好，才算真正提升准确率。

## 回归验证

```bash
python3 skills/ccy-ocr-local/scripts/regression.py
python3 skills/ccy-ocr-local/scripts/test_chart_ocr.py
```

## 目录导航

- `scripts/local_ocr.py`：通用离线 OCR CLI
- `scripts/chart_ocr.py`：图表识别 CLI 与 `ChartOCR` API
- `scripts/regression.py`：OCR 样例回归
- `scripts/test_chart_ocr.py`：图表识别回归
- `assets/`：样例图片
- `OCR-CONFIG.md` / `ROADMAP-*.md`：更细的配置与路线说明，需要时再读

## Python API

```python
from scripts.chart_ocr import ChartOCR

chart_ocr = ChartOCR(lang="chi_sim+eng")
result = chart_ocr.extract_chart_data("chart.png", ["auto"])
print(result)
```
