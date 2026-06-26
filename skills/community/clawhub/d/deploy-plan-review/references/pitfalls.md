# Python 中文 f-string 引号陷阱

## 症状

```python
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

执行或 lint `generate_review_report.py` 时，报错行是看起来完全合法的 f-string。

## 根因

Python 把**中文弯引号的左半部分 `"`（U+201C）按 ASCII 双引号 `"`（U+0022）处理**，造成字符串提前闭合。

### 错误示例

```python
# ✗ 报错 — "必须/必做" 的左右引号被 Python 视为字符串边界
f"模板中标记为"必须/必做"的操作步骤"

# ✗ 报错 — 同上
f"方案标题写"{num}台""

# ✗ 报错 — f"" 被解析为三引号开始
f""{wrong}" → "{correct}""
```

### 正确写法

```python
# ✓ 使用中文书名引号「」
f"模板中标记为「必须/必做」的操作步骤"

# ✓ 方案标题写「{num}台」
f"方案标题写「{num}台」"

# ✓ 单引号外包 f-string
f'「{wrong}」 → 「{correct}」'
```

## 检查方法

```bash
# 扫描文件中 f-string 内含中文引号的行
grep -n 'f".*[「」""].*"' scripts/*.py
```

## 涉及文件

- `generate_review_report.py` 第 53、70、74、343、394、443、565 行（均已修复）
- 任何含中文内容的 f-string 都有此风险
