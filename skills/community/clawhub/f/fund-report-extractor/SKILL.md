# 基金定期报告投资策略提取Skill

## 功能
自动提取公募基金定期报告中"投资策略和运作分析"部分的全文。

## 适用场景
- 提取基金经理管理的基金定期报告
- 需要获取"报告期内基金的投资策略和运作分析"原文
- 按时间正序整理汇总

## 使用方法

### 1. 获取基金代码
如果不知道基金代码，需要先搜索：
- 基金名称 → 天天基金网搜索
- 或使用AKShare搜索

### 2. 运行提取脚本
```bash
python 基金报告提取.py --code 基金代码 --name "基金名称"
```

## 技术要点

### 1. 数据获取：AKShare
```python
import akshare as ak
df = ak.fund_announcement_report_em(symbol='基金代码')
```
- 获取基金全部历史公告列表
- 包含公告ID，可构建PDF下载链接

### 2. PDF下载链接格式
```
http://pdf.dfcfw.com/pdf/H2_{报告ID}_1.pdf
```

### 3. PDF解析方案

#### 方案A：PyMuPDF（文本型PDF）
```python
import fitz
import re

doc = fitz.open(stream=pdf_content, filetype='pdf')
full_text = ''
for page in doc:
    html = page.get_text('html')
    # 提取Unicode中文
    codes = re.findall(r'&#x([0-9a-fA-F]+);', html)
    for c in codes:
        full_text += chr(int(c, 16))
```

#### 方案B：pdfplumber（扫描版PDF）
```python
import pdfplumber

with pdfplumber.open(pdf_file) as pdf:
    all_text = ''
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            all_text += text + '\n'
```

### 4. 关键词定位
不同基金公司/报告类型关键词位置不同：

**文本型PDF（景顺长城）：**
- "报告期内基金的投资策略和运作分析"
- "管理人对报告期内基金的投资策略和业绩表现的说明"
- "管理人对宏观经济、证券市场及行业走势的简要展望"

**扫描版PDF（中泰星元）：**
- "4.4 报告期内基金的投资策略和运作分析"
- 内容通常在Page 7-9
- 需要逐页搜索关键词

### 5. 内容提取模板
```python
# 提取投资策略部分
if '报告期内基金的投资策略和运作分析' in full_text:
    idx1 = full_text.find('报告期内基金的投资策略和运作分析')
    idx2 = full_text.find('报告期内基金的业绩表现', idx1)
    if idx2 == -1:
        idx2 = idx1 + 2500
    content = full_text[idx1:idx2]
```

## 常见问题

### Q: PDF是扫描版文字提取不到？
A: 使用pdfplumber替代PyMuPDF，并精确定位Page 7/8/9

### Q: 关键词匹配不到？
A: 检查关键词是否有空格差异，尝试不同变体

### Q: 报告数量不全？
A: 东方财富只保留最近4年报告，更早的报告需要其他渠道

### Q: 网络请求失败？
A: 添加延时time.sleep(1-2)，避免被限流

## 输出文件
- `reports_{基金代码}/` - 原始报告文件
- `{基金名称}_投资策略汇总.txt` - 完整汇总

## 依赖库
```bash
pip install akshare pymupdf pdfplumber pandas requests
```

---

**Created**: 2026-03-08
**Author**: 有才
