# 数据文件解析技能 (Data File Parser)

## 技能描述
智能解析各种数据文件格式(CSV/JSON/XLSX/Parquet/SQL)，自动检测编码、修复常见问题、提取结构化数据。

## 支持格式

### 1. CSV (逗号分隔值)
**常见问题及修复:**
- 编码问题: 自动尝试 UTF-8 → GBK → GB2312 → Latin1
- 标题行数: 自动检测 (常见: 1行、2行、混合单元格表头)
- 数字格式: 处理逗号千分位 (如 "1,234.56")、中文数字 (如 "３")
- 空值: 处理 "-", "—", "null", "None", 空字符串
- 换行符: 处理 CSV 内嵌换行 (需引号包裹)

**自动检测:**
```python
# 检测标题行数
def detect_header_lines(content):
    lines = content.split('\n')[:10]
    for i, line in enumerate(lines):
        if '合约代码' in line or '交易代码' in line or 'symbol' in line.lower():
            return i
    return 1  # 默认1行
```

### 2. JSON (JavaScript Object Notation)
**常见问题及修复:**
- BOM头: 移除 `\ufeff`
- 尾部逗号: `{"a": 1,}` → `{"a": 1}`
- 单引号: `{'a': 1}` → `{"a": 1}`
- Python注释: 移除 `#` 注释
- 数值精度: 处理科学计数法

**修复函数:**
```python
def fix_json(text):
    # 移除BOM
    text = text.replace('\ufeff', '')
    # 修复尾部逗号
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    # 单引号转双引号
    text = re.sub(r"'([^']*)'", r'"\1"', text)
    # 移除注释
    text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'#.*$', '', text, flags=re.MULTILINE)
    return text
```

### 3. XLSX (Excel)
**常见问题及修复:**
- 损坏文件: "File is not a zip file" → XLSX本质是ZIP，需重新保存
- 合并单元格: 读取时需处理 `merged_cells` 范围
- 空行: 跳过全为 None 的行
- 日期格式: 转换为标准 ISO 格式
- 公式: 使用 `data_only=True` 读取计算值

**检测XLSX是否损坏:**
```python
import zipfile
import openpyxl

def is_valid_xlsx(path):
    try:
        # 方法1: 检查ZIP有效性
        with zipfile.ZipFile(path, 'r'):
            pass
        # 方法2: 尝试用openpyxl打开
        wb = openpyxl.load_workbook(path, data_only=True)
        wb.close()
        return True
    except:
        return False
```

### 4. Parquet (列式存储)
**特点:** 高压缩率、适合大数据分析
```python
import pyarrow.parquet as pq

def read_parquet(path):
    table = pq.read_table(path)
    return table.to_pandas()
```

### 5. SQL脚本
**常见问题:**
- 字符集声明: `CHARSET=utf8mb4`
- 批量插入: 处理 `INSERT INTO ... VALUES (...), (...), ...`
- 转义字符: 处理 `\'` → `'` 或 `''`

---

## 核心工具函数

### 自动编码检测
```python
import chardet

def detect_encoding(path):
    with open(path, 'rb') as f:
        raw = f.read(10000)  # 读取前10KB
    result = chardet.detect(raw)
    return result['encoding'] or 'utf-8'
```

### 智能读取CSV
```python
import pandas as pd
import chardet

def smart_read_csv(path, **kwargs):
    # 1. 检测编码
    enc = detect_encoding(path)
    
    # 2. 尝试读取
    try:
        df = pd.read_csv(path, encoding=enc, **kwargs)
    except:
        # 备用编码
        for alt_enc in ['gbk', 'gb2312', 'utf-8-sig', 'latin1']:
            try:
                df = pd.read_csv(path, encoding=alt_enc, **kwargs)
                break
            except:
                continue
    
    return df
```

### 智能读取XLSX
```python
def smart_read_xlsx(path):
    """带自动修复的XLSX读取"""
    
    # 检查文件是否有效
    if not is_valid_xlsx(path):
        print(f"警告: {path} 可能损坏")
        return None
    
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    
    # 读取为列表
    data = []
    for row in ws.iter_rows(values_only=True):
        # 跳过全空行
        if not any(row):
            continue
        data.append(list(row))
    
    wb.close()
    return data
```

---

## 使用示例

### 解析任何数据文件
```python
from data_parser import parse_file

# 自动识别格式并解析
data = parse_file("data.csv")      # 返回 DataFrame/List
data = parse_file("data.json")     # 返回 dict/List
data = parse_file("data.xlsx")     # 返回 List[List]
data = parse_file("data.parquet")  # 返回 DataFrame
```

### 批量转换
```python
from data_parser import convert_folder

# 将文件夹内所有XLSX转为CSV
convert_folder(
    input_dir="D:/data/xlsx",
    output_dir="D:/data/csv",
    output_format="csv"
)
```

---

## 依赖安装
```bash
pip install pandas openpyxl chardet pyarrow
```

## 注意事项
1. XLSX文件如果显示"File is not a zip file"，说明文件损坏，需重新从源头获取
2. CSV编码问题最常见，优先检测编码
3. 大文件用 Parquet 格式更高效
4. 读取XLSX时用 `data_only=True` 获取计算值，否则得到公式