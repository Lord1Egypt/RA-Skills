# FN Portrait Toolkit

金融财报 Portrait 生成工具 - 从 PDF 年报提取结构化数据，通过 LLM 智能分析，生成综合财务画像。

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```bash
export DEEPSEEK_API_KEY=sk-...
python scripts/fn_pipeline.py 688777 中控技术 --years 2023-2025 --plate 科创板
```

## 支持模型

- DeepSeek API（推荐）
- Moonshot API
- Ollama 本地模型
