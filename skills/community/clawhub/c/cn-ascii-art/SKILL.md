slug: cn-ascii-art
name: ASCII艺术生成器
version: "1.0.0"
author: 千策

# ASCII艺术生成器


将文本转换为ASCII艺术，支持多种字体和样式。

## 功能

- 文本转大写ASCII艺术
- 多种字体样式
- 支持中英文

## 使用方法

```bash
# 基本转换
python3 cn_ascii_art.py "Hello"

# 指定字体
python3 cn_ascii_art.py "你好" --font banner

# 窄字体
python3 cn_ascii_art.py "Test" --font narrow

# 块字体
python3 cn_ascii_art.py "OK" --font block
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `text` | 要转换的文本 | 必填 |
| `--font` | 字体样式 | standard |

## 字体样式

- standard - 标准
- banner - 横条
- narrow - 窄体
- block - 块体

## 示例

```bash
# 生成签名
python3 cn_ascii_art.py "Hello World"

# 中文测试
python3 cn_ascii_art.py "测试"
```

## 依赖

- Python 3.x（内置pyfiglet）
- pyfiglet (pip install pyfiglet) - 如无会自动降级

## 注意事项

- 中文字符可能显示不完整（ASCII艺术主要针对英文）
- 建议字体：standard, banner, narrow

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
