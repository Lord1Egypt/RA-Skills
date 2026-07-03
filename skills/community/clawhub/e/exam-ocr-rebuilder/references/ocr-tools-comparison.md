# OCR工具对比与选择指南

## 可用OCR方案对比

| 维度 | tencent-docs OCR | 百度AI试卷切题 | 阿里云试卷切题 | PaddleOCR (本地) | DashScope多模态 |
|------|-----------------|---------------|---------------|-----------------|----------------|
| **连接状态** | 已连接MCP | 需API Key | 需API Key | 需本地安装 | 需API Key |
| **PDF直接支持** | 否（需转图片） | 是 | 否（仅图片） | 是 | 是 |
| **题型识别** | 否（纯文字OCR） | 是（5种题型） | 否（切题不分类） | 否（纯文字OCR） | 否（需LLM辅助） |
| **结构化输出** | 文本+坐标 | 题干/选项/答案 | 文本+坐标+切题 | 文本+版面分析 | 文本（LLM理解） |
| **数学公式** | 不支持 | 需自行解析 | 需自行解析 | PP-Structure支持 | LLM可识别 |
| **表格识别** | ocr.toexcel | 不支持 | 不支持 | PP-Structure支持 | LLM可识别 |
| **中英文** | 支持 | 支持中英混排 | 支持多学科 | 支持中英日韩 | 支持多语言 |
| **手写体** | 不确定 | 支持手写印刷混排 | 不支持 | 支持手写 | LLM可识别 |
| **图片限制** | 单张10MB | 10MB/8192px | 10MB/8192px | 无限制 | 依赖模型 |
| **批量处理** | 最多9张/次 | 逐页调用 | 逐页调用 | 支持批量 | 逐张调用 |
| **费用** | 腾讯文档额度 | 0.01-0.015元/次 | 0.01元/次 | 免费开源 | 0.008-0.12元/千token |
| **准确率** | 高（腾讯OCR） | 高（教育优化） | 高（教育优化） | 中高 | 取决于模型 |

## 推荐策略

### 首选方案：tencent-docs OCR（已连接）

**适用场景**：所有需要OCR识别的试卷

**流程**：
1. PDF → PyMuPDF转图片
2. 每页图片 → `ocr.extract`（accurate模式）
3. 合并文本 → LLM结构化解析

**优势**：
- 无需额外API Key，已连接可用
- 高精度OCR识别
- 支持位置信息（`with_positions: true`）
- 可直接生成Word文档（`ocr.toword`）

**调用方式**：
```
mcp__tencent-docs__ocr.extract
  extract_type: "accurate"
  image_base64: "<base64编码>"
  with_positions: true
```

### 增强方案：tencent-docs + 百度AI试卷切题

**适用场景**：需要自动题型识别的场景

**流程**：
1. PDF → 转图片
2. 图片 → 百度AI `paper_cut_edu` API（自动切题+题型识别）
3. 结构化结果 → LLM补充解析
4. 生成输出

**百度API调用**：
```python
import requests

url = "https://aip.baidubce.com/rest/2.0/ocr/v1/paper_cut_edu"
params = {
    "image": image_base64,
    "language_type": "CHN_ENG",
    "detect_direction": "true",
    "words_type": "handprint_mix",
    "splice_text": "true",
    "only_split": "false"
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(url, params=params, headers=headers)
```

### 快速方案：PDF直接导入腾讯文档

**适用场景**：只需快速提取文本，不需要精细结构化

**流程**：
1. `manage.pre_import` → 获取上传链接
2. curl上传PDF文件
3. `manage.async_import` → 触发导入
4. `manage.import_progress` → 轮询进度（每5秒）
5. `get_content` → 读取文本
6. LLM结构化解析

### 本地方案：PaddleOCR

**适用场景**：无网络或需要离线处理

**安装**：
```bash
pip install paddlepaddle paddleocr -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

**使用**：
```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="ch")
result = ocr.ocr("page_001.png", cls=True)
for line in result[0]:
    print(line[1][0])  # 文本内容
```

## PDF类型检测

在处理前先检测PDF类型，选择最优策略：

| PDF类型 | 检测方法 | 推荐策略 |
|---------|---------|---------|
| 文本型PDF | `page.get_text()` 有内容 | 直接提取文本，跳过OCR |
| 扫描型PDF | `page.get_text()` 为空 | 转图片 → OCR识别 |
| 混合型PDF | 部分页有文本 | 全部转图片 → 统一OCR处理 |

使用 `scripts/pdf_to_images.py --check` 检测PDF类型。

## 多页处理策略

1. **逐页OCR**：每页单独调用OCR，结果按页码合并
2. **批量OCR**：tencent-docs `ocr.toword` 支持最多9张图片
3. **并行处理**：多页PDF可并行调用OCR加速

## 错误处理

| 错误 | 处理方式 |
|------|---------|
| OCR识别不完整 | 提高DPI到400，重新转换图片 |
| 图片太大（>10MB） | 降低DPI或压缩图片 |
| API调用频率限制 | 增加请求间隔 |
| 手写体识别差 | 尝试百度AI的 `handwring_only` 模式 |
| 数学公式乱码 | 使用LLM重新理解和格式化公式 |
