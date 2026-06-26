slug: cn-diff-checker
name: 文本差异对比器
version: "1.0.0"
author: 千策

# 文本差异对比器


比对两个文本/文件的差异，支持逐行、逐词、逐字符比对。

## 功能

- 文本比对（字符串）
- 文件比对
- 逐行/逐词/逐字符模式
- 输出ANSI彩色差异

## 使用方法

```bash
# 比对两个字符串
python3 cn_diff_checker.py "Hello World" "Hello Python"

# 比对两个文件
python3 cn_diff_checker.py file1.txt file2.txt

# 逐词比对
python3 cn_diff_checker.py "这是测试文本" "这是示例文本" --word

# 逐字符比对
python3 cn_diff_checker.py "abc" "abd" --char
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `old` | 原始文本或文件 | 必填 |
| `new` | 新文本或文件 | 必填 |
| `--line` | 逐行比对 | 默认 |
| `--word` | 逐词比对 | False |
| `--char` | 逐字符比对 | False |
| `--output` | 输出到文件 | False |

## 示例

```bash
# 基本比对
python3 cn_diff_checker.py old.txt new.txt

# 只显示新增行
python3 cn_diff_checker.py old.txt new.txt | grep "^>"

# 只显示删除行
python3 cn_diff_checker.py old.txt new.txt | grep "^<"
```

## 依赖

- Python 3.x（内置difflib）

## 注意事项

- 自动检测文件输入（读取文件内容）
- 字符串输入直接比对
- Windows下ANSI颜色可能不显示

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
