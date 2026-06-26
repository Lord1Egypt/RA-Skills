---
name: china-doc-ocr
description: 智能文档OCR识别与结构化提取。Use when the user has a complex document, PDF, scanned image, photo, invoice, receipt, ID card, table, or chart that needs to be recognized and converted to text or Markdown. Uses PaddleOCR-VL-1.5 and DeepSeek-OCR. 文档OCR、发票识别、证件识别。
version: 1.2.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["python3"], "env": ["SILICONFLOW_API_KEY"]}, "primaryEnv": "SILICONFLOW_API_KEY"}}
---

# 智能文档 OCR China Doc OCR

识别并提取复杂文档内容：PDF、图片、扫描件、发票、表格、证件等。
使用硅基流动 DeepSeek-OCR / PaddleOCR-VL，国内直连，无需翻墙。

模型选择与参数说明 → `references/models.md`
各场景提示词模板 → `references/prompts.md`

## 触发时机

- "帮我识别这个PDF/图片里的内容"
- "把这张发票/收据的信息提取出来"
- "将这份扫描合同转成可编辑文字"
- "这个表格里的数据帮我提取一下"
- "帮我把这张截图的文字识别出来"
- "这份报告转成 Markdown 格式"
- "识别这张身份证/营业执照的信息"

---

## 模型选择策略（优先OCR）

```
OCR优先级：
1. PaddleOCR-VL-1.5 (免费、快速、专业OCR)
2. DeepSeek-OCR (免费、效果好)
3. Qwen2.5-VL-72B (视觉语言模型，OCR效果一般但可补充)

默认使用 PaddleOCR-VL-1.5
如果识别效果不好，降级到 DeepSeek-OCR
如果仍然不好，降级到 Qwen2.5-VL-72B
```

---

## Step 0：环境检查

```bash
# 检查 API Key
if [ -z "$SILICONFLOW_API_KEY" ]; then
  echo "缺少 SILICONFLOW_API_KEY"
  echo "配置方法："
  echo "  1. 访问 cloud.siliconflow.cn 注册（国内直连）"
  echo "  2. 进入「API密钥」页面创建 Key"
  echo "  3. export SILICONFLOW_API_KEY='sk-xxxxxxxx'"
  exit 1
fi
```

---

## Step 1：识别内容类型，选择处理模式

```
用户提供文件路径或 URL → 判断类型：

文件扩展名/用户描述 → 处理模式：

.pdf                    → PDF 模式
.jpg/.jpeg/.png/.webp   → 图片模式
.bmp/.tiff/.gif         → 图片模式（先转换格式）
URL（http/https开头）   → URL 直接模式
用户粘贴了 base64       → 直接使用

用户意图 → 选择 Prompt 模式：

"转成文字/提取文字"     → 通用OCR
"转成Markdown/保留格式" → 文档转Markdown
"提取表格/表格数据"     → 图表解析
"发票/收据/单据"        → 发票识别
"身份证/证件/执照"      → 证件识别
"图表/图形/柱状图"      → 图表解析
未指定                  → 默认文档转Markdown
```

---

## Step 2：图片 OCR

### 本地图片文件

```bash
python3 scripts/ocr.py \
  --image "/path/to/image.jpg" \
  --prompt "Convert the document to markdown." \
  --model paddleocr
```

### 图片 URL

```bash
python3 scripts/ocr.py \
  --url "https://example.com/document.jpg" \
  --prompt "Convert the document to markdown." \
  --model deepseek
```

### 指定模型

```bash
# 使用 PaddleOCR（默认，推荐）
python3 scripts/ocr.py --image photo.jpg --model paddleocr

# 使用 DeepSeek-OCR
python3 scripts/ocr.py --image photo.jpg --model deepseek

# 使用 Qwen2.5-VL
python3 scripts/ocr.py --image photo.jpg --model qwen
```

---

## Step 3：PDF OCR

### 单页或少页 PDF

```bash
python3 scripts/ocr.py \
  --pdf "/path/to/document.pdf" \
  --prompt "Convert the document to markdown." \
  --model deepseek
```

### 多页 PDF

多页 PDF 需要分页处理。使用 Python 脚本：

1. 使用 pypdf 分页
2. 对每页分别调用 OCR
3. 合并结果

---

## Step 4：格式化输出

识别完成后根据用户需求输出：

### 文档转 Markdown（保留结构）

```
直接输出 Markdown 内容，保留：
  - 标题层级（# ## ###）
  - 列表（- * 1.）
  - 表格（| 列1 | 列2 |）
  - 代码块（```）
  - 加粗、斜体等格式
```

### 发票/证件识别（结构化输出）

```
发票识别结果
━━━━━━━━━━━━━━━━━━━━
发票类型：增值税专用发票
发票号码：XXXXXXXXXXXXXXXX
开票日期：2026年03月21日
购买方：[公司名称]
销售方：[公司名称]
商品/服务：[明细]
不含税金额：¥X,XXX.XX
税率：13%
税额：¥XXX.XX
价税合计：¥X,XXX.XX
```

### 表格数据（CSV 友好格式）

```
识别结果同时输出：
1. Markdown 表格（可读）
2. 询问用户是否需要 CSV 格式（方便导入 Excel）
```

---

## 输出文件保存

识别结果保存到工作区，长期保留。

---

## 错误处理

```
文件不存在           → 提示用户确认路径
文件过大（>10MB）    → 建议压缩或分页处理
图片分辨率过低       → 提示识别效果可能较差，建议重新拍摄
PDF 加密            → 提示需要先解密
识别结果为空         → 可能是纯图片型PDF，尝试截图后重新识别
401 错误            → API Key 失效，重新获取
429 错误            → 请求频率超限，等待后重试
```

---

## 注意事项

- 图片最小 56×56，最大 3584×3584 像素，超出会自动压缩
- PDF 支持 base64 编码输入
- 多页 PDF 需要安装 pypdf（用户需手动安装）
- detail=high 时按实际像素计费，detail=low 统一约256 token
- 发票/证件等隐私文件处理后请及时删除工作区临时文件