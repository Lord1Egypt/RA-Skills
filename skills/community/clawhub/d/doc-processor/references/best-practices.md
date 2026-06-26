# 文档处理最佳实践

## 1. 依赖管理

### 系统依赖
```bash
# PDF 处理（必需）
sudo apt install poppler-utils      # Linux
brew install poppler                # macOS
```

### Python 依赖
```bash
# 使用虚拟环境
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. 性能优化

### 大文件处理
```python
# Excel 分块读取
for chunk in pd.read_excel('large.xlsx', chunksize=1000):
    process(chunk)

# PDF 限制页数
content = processor.read('large.pdf', pages='1-10')
```

### 内存管理
```python
# 使用 read_only 模式
load_workbook('large.xlsx', read_only=True)

# 及时关闭文件
with pd.ExcelWriter('output.xlsx') as writer:
    df.to_excel(writer)
```

## 3. 错误处理

```python
try:
    content = processor.read('file.docx')
except DependencyError as e:
    print(f"依赖缺失：{e}")
    print("请运行：pip install python-docx")
except FileNotFoundError as e:
    print(f"文件不存在：{e}")
except FormatError as e:
    print(f"格式不支持：{e}")
```

## 4. 安全注意事项

### 文件验证
```python
# 检查文件是否存在
if not Path(file_path).exists():
    raise FileNotFoundError(file_path)

# 检查文件类型
if path.suffix.lower() not in SUPPORTED_FORMATS:
    raise FormatError(f"不支持的格式：{path.suffix}")
```

### 路径安全
```python
# 解析绝对路径
path = Path(file_path).resolve()

# 限制在 workspace 内
if not str(path).startswith(workspace):
    raise SecurityError("路径超出工作区")
```

## 5. 测试建议

```python
# 单元测试
def test_read_word():
    processor = DocumentProcessor()
    content = processor.read('test.docx')
    assert content.type == 'word'
    assert len(content.data['paragraphs']) > 0

# 集成测试
def test_convert_word_to_csv():
    processor = DocumentProcessor()
    output = processor.convert('input.docx', 'output.csv')
    assert Path(output).exists()
```

## 6. 扩展开发

### 添加新格式支持
```python
def _read_newformat(self, path: Path) -> DocContent:
    """读取新格式"""
    # 实现读取逻辑
    return DocContent(type='new', format='text', data=content)

# 注册到 read() 方法
elif ext == '.new':
    return self._read_newformat(path)
```

### 添加新操作
```python
def compare(self, file1: str, file2: str) -> Dict:
    """比较两个文档"""
    content1 = self.read(file1)
    content2 = self.read(file2)
    # 实现比较逻辑
    return diff_result
```
