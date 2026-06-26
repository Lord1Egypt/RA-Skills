# OCR识别规则

## ⚠️ 核心原则

**OCR是必需步骤，不是可选功能！**

### 为什么必须使用OCR？

```
原因1：图表数据无法通过文本提取
- 行业分布、地区分布、信用评级分布通常以图表形式存在
- pdfplumber只能提取文本和表格，无法识别图表中的数据
- 不使用OCR会导致关键数据遗漏

原因2：避免信息丢失
- 文本提取可能遗漏图片中的关键信息
- 双重提取策略（文本+OCR）确保数据完整
- 宁可多识别，不可漏数据

原因3：用户期望
- 用户期望AI能提取所有可见数据
- 漏掉分布数据会导致用户需要手动补充
- 违背"自动化"的初衷
```

---

## 双重提取策略（强制执行）

### 流程图

```
PDF输入
    ↓
    ├─→ 方法A：文本提取（pdfplumber）
    │   - 提取文本内容
    │   - 提取表格数据
    │   - 识别字段名
    │
    ├─→ 方法B：OCR识别（pytesseract）★ 必须执行
    │   - PDF转图片（300 DPI）
    │   - 全页OCR识别
    │   - 提取图表数据
    │
    ↓
合并结果
    - 文本提取 + OCR识别 = 完整数据
    - 对比验证
    - 去重合并
    ↓
PDF信息Excel
```

### Python实现

```python
def extract_pdf_complete(pdf_path):
    """完整提取PDF数据（双重提取）"""
    
    # 方法A：文本提取
    text_data = extract_text(pdfplumber.open(pdf_path))
    
    # 方法B：OCR识别（必须执行！）
    images = convert_from_path(pdf_path, dpi=300)
    ocr_data = []
    for img in images:
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        ocr_data.append(text)
    
    # 合并结果
    complete_data = merge_results(text_data, ocr_data)
    
    return complete_data
```

---

## OCR流程（详细步骤）

### 步骤1：PDF转图片

```python
from pdf2image import convert_from_path

# 高分辨率转换（300 DPI）
images = convert_from_path(
    pdf_path,
    dpi=300,  # 高分辨率，确保图表清晰
    fmt='png',
    first_page=1,
    last_page=None  # 转换所有页
)
```

### 步骤2：OCR识别

```python
import pytesseract

# 配置
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
OCR_LANG = 'chi_sim+eng'  # 中文简体 + 英文
OCR_CONFIG = '--oem 3 --psm 6'  # 优化配置

# 识别每一页
for page_num, img in enumerate(images):
    # 全页OCR
    text = pytesseract.image_to_string(img, lang=OCR_LANG, config=OCR_CONFIG)
    
    # 处理识别结果
    lines = text.split('\n')
    for line in lines:
        # 查找关键数据
        if any(keyword in line for keyword in ['行業', '行业', '分布', '區域', '区域', '評級', '评级']):
            extract_distribution_data(line)
```

### 步骤3：数据提取

```python
import re

def extract_distribution_data(text):
    """从OCR文本中提取分布数据"""
    
    # 行业分布示例：周期性消费品 24.4%
    industry_pattern = r'(周期性消费品|金融|房地产|公用事业|工业|能源|政府|基本原料|通讯|其他|现金|非周期性消费品)\s+(\d+\.?\d*)\%'
    
    # 地区分布示例：中国内地 45.2%
    region_pattern = r'(中国内地|中国香港|美国|新加坡|英国|其他)\s+(\d+\.?\d*)\%'
    
    # 信用评级分布示例：AAA 10.2%
    rating_pattern = r'(AAA|AA\+|AA|AA-|A\+|A|A-|BBB\+|BBB|BBB-|BB|B|NR)\s+(\d+\.?\d*)\%'
    
    # 提取数据
    for pattern in [industry_pattern, region_pattern, rating_pattern]:
        matches = re.findall(pattern, text)
        for match in matches:
            name, value = match
            # 存储数据
            save_data(name, float(value) / 100)  # 转换为小数
```

---

## 重点识别对象

### 必须识别的数据

```
1. 行业分布（Industry Distribution）
   - 基本原料、通讯、周期性消费品、非周期性消费品
   - 能源、房地产、金融、工业、科技、公用事业
   - 政府、现金、其他

2. 地区分布（Geographic Distribution）
   - 中国内地、中国香港、中国澳门
   - 美国、新加坡、英国、印尼、韩国
   - 其他亚太、其他欧洲、其他地区

3. 信用评级分布（Credit Rating Distribution）
   - AAA、AA+、AA、AA-、A+、A、A-
   - BBB+、BBB、BBB-、BB、B、NR

4. 核心指标
   - 久期、组合久期、平均存续期
   - 到期收益率、YTM、孳息率
   - 基金规模、资产净值、AUM
```

---

## OCR准确度优化

### 提高识别准确度的方法

```python
# 方法1：高分辨率（300 DPI以上）
images = convert_from_path(pdf_path, dpi=300)

# 方法2：中英文混合识别
text = pytesseract.image_to_string(img, lang='chi_sim+eng')

# 方法3：图像预处理
import cv2

def preprocess_image(img):
    # 转灰度
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    
    # 二值化（增强对比度）
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # 去噪
    denoised = cv2.medianBlur(binary, 3)
    
    return denoised

# 方法4：对比验证
# OCR提取的数据，与文本提取的数据对比，确保一致性
```

---

## 数据校验

### 识别后必须校验

```python
def validate_ocr_data(field_name, value, all_values):
    """校验OCR识别的数据"""
    
    # 1. 范围校验
    if '久期' in field_name:
        if not (0 < value < 20):
            return False, "久期值异常"
    
    if '收益率' in field_name or 'YTM' in field_name:
        if not (0 < value < 1):  # 百分比形式（0.067 = 6.7%）
            return False, "收益率值异常"
    
    # 2. 分布数据总和校验
    if '分布' in field_name:
        total = sum(all_values)
        if not (0.95 < total < 1.05):  # 允许5%误差
            return False, f"分布数据总和异常：{total:.2%}"
    
    # 3. 与文本提取对比
    text_value = get_text_extracted_value(field_name)
    if text_value and abs(value - text_value) > 0.01:
        return False, f"OCR与文本提取不一致：OCR={value}, 文本={text_value}"
    
    return True, "校验通过"
```

---

## 特殊情况处理

### 情况1：饼图/环形图

```
问题：饼图的角度难以精确识别

处理策略：
1. 尝试OCR识别图例文字和百分比
2. 如果图例清晰，提取数据
3. 如果图例模糊：
   - 在Excel中标记"需手动输入"
   - 附注说明：饼图数据，OCR识别准确度低
```

### 情况2：复杂图表

```
问题：三维图表、渐变色图表难以识别

处理策略：
1. 尝试OCR识别
2. 如果识别失败：
   - 在Excel中预留空白单元格
   - 标记"图表复杂，需手动输入"
3. 提供图表截图位置，方便用户手动查看
```

### 情况3：表格图片

```
问题：表格以图片形式存在，pdfplumber无法提取

处理策略：
1. OCR识别整页
2. 从OCR文本中重构表格
3. 使用正则表达式提取行列数据
```

---

## 输出格式

### PDF信息Excel中标注数据来源

```
| 字段 | 值 | 数据来源 |
|------|-----|---------|
| 组合久期 | 2.3年 | 文本提取 |
| 平均最低孳息率 | 6.7% | 文本提取 |
| 周期性消费品 | 24.4% | OCR识别 |
| 金融 | 20.1% | OCR识别 |
| 房地产 | 12.9% | OCR识别 |
```

### 生成说明

```
AI生成Excel后，附带说明：

📊 数据提取报告：
- 文本提取字段：10个（准确度：高）
- OCR识别字段：15个（准确度：中）
- 需手动输入：0个

OCR识别详情：
- 行业分布：12项（来源：第1页图表）
- 地区分布：8项（来源：第1页图表）
- 信用评级分布：10项（来源：第1页图表）

建议：
- OCR识别准确度中等，建议对照PDF验证
- 所有分布数据已提取，无需手动补充
```

---

## 系统依赖（必须安装）

### Python包

```bash
pip install pdfplumber openpyxl pdf2image pytesseract Pillow
```

### 系统依赖

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim poppler-utils

# macOS
brew install tesseract tesseract-lang poppler

# Windows
# 1. 下载Tesseract：https://github.com/UB-Mannheim/tesseract/wiki
# 2. 下载Poppler：https://blog.alivate.com.au/poppler-windows/
# 3. 添加到系统PATH
```

### 检查安装

```python
import pytesseract
import pdf2image

# 检查Tesseract
try:
    version = pytesseract.get_tesseract_version()
    print(f"✅ Tesseract已安装：{version}")
except:
    print("❌ Tesseract未安装")

# 检查中文语言包
langs = pytesseract.get_languages()
if 'chi_sim' in langs:
    print("✅ 中文语言包已安装")
else:
    print("❌ 中文语言包未安装")
```

---

## 错误处理

### OCR识别失败

```
如果OCR完全失败：
1. 检查Tesseract是否安装
2. 检查中文语言包是否安装
3. 检查Poppler是否安装
4. 在Excel中标记所有分布字段为"OCR失败，需手动输入"
5. 向用户报告错误原因
```

### 数据不一致

```
如果文本提取与OCR识别结果不一致：
1. 优先使用文本提取结果（准确度更高）
2. 在Excel中用黄色标记不一致的字段
3. 附注说明：文本提取=X，OCR识别=Y
4. 让用户选择正确值
```

---

## 总结

**OCR识别三原则：**

1. **必须执行**：每次处理PDF都必须进行OCR识别
2. **双重提取**：文本提取 + OCR识别 = 完整数据
3. **宁多勿少**：宁可多识别一些数据，不可漏掉关键信息

**记住：漏掉分布数据 = 用户体验差 = 失败的自动化**
