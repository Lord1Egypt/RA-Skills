# MarkItDown API 参考

本文档提供 MarkItDown 核心 API 的详细说明。

## 核心类

### MarkItDown

主要入口类，用于文件转换。

#### 初始化

```python
from markitdown import MarkItDown

# 默认：使用所有可用转换器
md = MarkItDown()

# 指定特定转换器
from markitdown import DocumentConverter
md = MarkItDown(converters=[MyCustomConverter()])

# 启用/禁用插件
md = MarkItDown(enable_plugins=True)
```

#### 方法

##### `convert(file_path: str, **kwargs) -> ConversionResult`

转换指定路径的文件。

**参数**:
- `file_path` - 要转换的文件路径（字符串）
- `**kwargs` - 传递给底层转换器的额外参数

**返回**: `ConversionResult` 对象，包含：
- `text_content` - 转换后的 Markdown 文本
- `metadata` - 文档元数据字典
- `encoding` - 文本编码

**示例**:
```python
result = md.convert("document.pdf")
print(result.text_content)
print(result.metadata.get('title'))
```

##### `convert_stream(file_stream, **kwargs) -> ConversionResult`

从文件流对象转换（适用于大文件或内存中的数据）。

**参数**:
- `file_stream` - 二进制文件类对象（如 `open('file.pdf', 'rb')`）
- `**kwargs` - 传递给底层转换器的额外参数

**示例**:
```python
with open("large.pdf", "rb") as f:
    result = md.convert_stream(f)
    print(result.text_content)
```

**注意**: 此方法需要二进制模式打开的文件，v0.1.0 版本起为强制要求。

### ConversionResult

转换结果对象。

#### 属性

- `text_content: str` - Markdown 格式的文本内容
- `metadata: dict` - 文档元数据（标题、作者、创建时间等）
- `encoding: str` - 返回文本的字符编码（通常是 'utf-8'）

### DocumentConverter (抽象基类)

自定义转换器的基类。

#### 需实现的属性和方法

##### `supported_extensions: List[str]`

返回此转换器支持的文件扩展名列表（小写，包含点号）。

```python
@property
def supported_extensions(self) -> List[str]:
    return ['.pdf', '.pdfa']
```

##### `convert(file_stream, **kwargs) -> ConversionResult`

实现具体的转换逻辑。

**参数**:
- `file_stream` - 二进制文件流
- `**kwargs` - 额外参数

**返回**: `ConversionResult` 实例

### 内置转换器类

MarkItDown 提供多个内置转换器，它们都继承 `DocumentConverter`：

| 转换器类 | 对应格式 | 扩展名 |
|----------|----------|--------|
| `PdfConverter` | PDF | .pdf |
| `DocxConverter` | Word | .docx |
| `PptxConverter` | PowerPoint | .pptx |
| `XlsxConverter` | Excel | .xlsx |
| `HtmlConverter` | HTML | .html, .htm |
| `TextConverter` | 纯文本 | .txt |
| `CsvConverter` | CSV | .csv |
| `JsonConverter` | JSON | .json |
| `XmlConverter` | XML | .xml |
| `ZipConverter` | ZIP | .zip |
| ` EpubConverter` | EPUB | .epub |
| `ImageConverter` | 图片 | .png, .jpg, .jpeg, .gif, ... |
| `AudioConverter` | 音频 | .mp3, .wav, .m4a, ... |
| `YoutubeConverter` | YouTube | (URL 以 youtube.com/youtu.be 开头) |

## 常见使用模式

### 批量转换

```python
from pathlib import Path
from markitdown import MarkItDown

md = MarkItDown()

input_dir = Path("./documents")
output_dir = Path("./markdown")
output_dir.mkdir(exist_ok=True)

for file_path in input_dir.rglob("*"):
    if file_path.is_file():
        try:
            result = md.convert(str(file_path))
            rel_path = file_path.relative_to(input_dir)
            output_file = output_dir / rel_path.with_suffix('.md')
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(result.text_content, encoding='utf-8')
            print(f"✓ {file_path.name}")
        except Exception as e:
            print(f"✗ {file_path.name}: {e}")
```

### 带进度显示的转换

```python
from tqdm import tqdm  # pip install tqdm

md = MarkItDown()
files = list(Path("./docs").rglob("*.pdf"))

for file_path in tqdm(files, desc="Converting"):
    result = md.convert(str(file_path))
    (output_dir / f"{file_path.stem}.md").write_text(result.text_content)
```

### 处理内存中的文件

```python
import io
from markitdown import MarkItDown

# 从数据库或网络获取文件内容
file_bytes = get_file_from_somewhere()  # bytes 对象

# 包装为 BytesIO
stream = io.BytesIO(file_bytes)
md = MarkItDown()
result = md.convert_stream(stream)
```

### 仅提取元数据

```python
md = MarkItDown()
result = md.convert("document.pdf")
print("标题:", result.metadata.get('title'))
print("作者:", result.metadata.get('author'))
print("创建时间:", result.metadata.get('creation_date'))
```

## 异常处理

```python
from markitdown import MarkItDown, UnsupportedFormatError, ConversionError

md = MarkItDown()

try:
    result = md.convert("unknown.xyz")
except UnsupportedFormatError:
    print("不支持的文件格式")
except ConversionError as e:
    print(f"转换失败: {e}")
except FileNotFoundError:
    print("文件不存在")
```

## 命令行工具

MarkItDown 安装后提供 `markitdown` 命令行工具：

```bash
# 查看帮助
markitdown --help

# 转换单个文件
markitdown input.pdf -o output.md

# 批量转换
markitdown ./docs/ --recursive -o ./output/

# 输出到标准输出
markitdown file.pdf
```

命令行工具返回码：
- `0` - 成功
- `1` - 转换失败
- `2` - 参数错误

## MCP 服务器

MarkItDown 提供 Model Context Protocol (MCP) 服务器，供 LLM 应用集成。

**启动**:
```bash
python -m markitdown.mcp
```

**配置 Claude Desktop**:
```json
{
  "mcpServers": {
    "markitdown": {
      "command": "python",
      "args": ["-m", "markitdown.mcp"],
      "env": {
        "MARKITDOWN_OPTIONS": "--verbose"
      }
    }
  }
}
```

MCP 服务器提供以下工具：
- `convert` - 转换单个文件
- `convert_batch` - 批量转换目录
- `list_formats` - 列出支持的格式

详情见 [MCP 官方文档](https://github.com/modelcontextprotocol/specification)。

## 性能建议

### 大文件处理

对于超过 100MB 的文件，建议使用流式 API：

```python
with open("huge_file.pdf", "rb") as f:
    result = md.convert_stream(f)  # 避免全文件加载到内存
```

### 并行处理

利用 `concurrent.futures` 加速批量转换：

```python
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

def convert_file(file_path):
    md = MarkItDown()  # 每个进程独立实例
    return md.convert(str(file_path))

files = list(Path("./docs").glob("*.pdf"))

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(convert_file, files))
```

注意：多进程时每个进程需独立创建 `MarkItDown` 实例。

### 缓存机制

对于重复转换的文件，可缓存结果：

```python
import hashlib
from pathlib import Path

def get_file_hash(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def cached_convert(md, file_path, cache_dir):
    file_hash = get_file_hash(file_path)
    cache_file = cache_dir / f"{file_hash}.md"

    if cache_file.exists():
        return cache_file.read_text(encoding='utf-8')

    result = md.convert(str(file_path))
    cache_file.write_text(result.text_content, encoding='utf-8')
    return result.text_content
```

## 版本兼容性

- **v0.1.0+**: `convert_stream()` 要求二进制流，API 稳定
- **v0.0.1**: 旧版 API 不兼容，建议升级

检查版本：
```bash
pip show markitdown
```

---
最后更新: 2026-03-09
参考版本: markitdown >= 0.1.0