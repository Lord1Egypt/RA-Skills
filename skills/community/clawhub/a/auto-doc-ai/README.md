# Auto Doc AI

基于 AST 和 LLM 自动生成 Python 代码文档（Google Style docstring）

## 功能特性

- 🔍 基于 AST 解析代码结构
- 🤖 智能函数/类/方法分析
- 📝 生成 Google Style docstring
- 📁 支持单文件或整个目录批量处理
- 🔄 支持增量更新（跳过已有文档的函数）

## 安装

作为 OpenClaw Skill 使用:
```bash
clawhub install auto-doc-ai
```

或直接使用:
```bash
git clone https://github.com/kimi-claw/skill-auto-doc-ai.git
cd skill-auto-doc-ai
./bin/generate-docs --help
```

## 使用方法

### 为单个文件生成文档

```bash
/generate-docs /path/to/your_script.py
```

### 为整个目录生成文档

```bash
/generate-docs /path/to/src/ --recursive
```

### 强制更新已有文档

```bash
/generate-docs /path/to/src/ --overwrite
```

### 预览模式（不写入文件）

```bash
/generate-docs /path/to/your_script.py --dry-run
```

## 生成的文档格式示例

```python
def process_data(data, threshold=0.5):
    """处理输入数据并返回过滤后的结果。

    Args:
        data (list): 输入数据列表。
        threshold (float, optional): 过滤阈值，默认为 0.5。

    Returns:
        list: 过滤后的数据列表。

    Raises:
        ValueError: 如果数据格式无效。
    """
    pass
```

## 注意事项

- 仅支持 Python 3.7+ 的文件
- 建议先使用 `--dry-run` 预览生成的文档
- 使用 `--overwrite` 会替换所有现有 docstring

## License

MIT
