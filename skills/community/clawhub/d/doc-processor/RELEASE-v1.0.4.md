# doc-processor v1.0.4 发布

## 修复内容

### ✅ Bug 1: Excel 直接写入失败 (P0)
**问题:** `At least one sheet must be visible`

**原因:** `_write_excel` 方法未正确处理 `{'sheet_name': '...', 'data': [...]}` 格式参数

**修复:** 添加特殊处理逻辑，识别该格式并使用指定的 sheet_name 和 data

**测试场景:**
```python
processor.write('test.xlsx', {
    'sheet_name': '数据表',
    'data': [['姓名', '年龄'], ['张三', 25]]
})
# ✅ 成功
```

### ✅ Bug 2: Word 文档合并失败 (P2)
**问题:** `Package not found at 'part1.docx'`

**原因:** `_merge_word` 方法中文件路径未解析为绝对路径

**修复:** 在打开文件前调用 `_resolve_path()` 和 `_validate_file()` 确保路径正确

**测试场景:**
```python
processor.merge(['part1.docx', 'part2.docx'], 'merged.docx')
# ✅ 成功
```

## 验证结果

两个 Bug 均已通过测试验证，功能恢复正常。

## 已验证功能清单

- ✅ PDF 读取
- ✅ Word 读写
- ✅ Excel 读写 (含自定义 sheet_name)
- ✅ CSV 读取/写入
- ✅ Word 文档合并
- ✅ Excel 文档合并
- ✅ 格式转换
- ✅ 文档信息获取

---
**版本:** v1.0.4  
**日期:** 2026-03-25  
**状态:** ✅ 已发布
