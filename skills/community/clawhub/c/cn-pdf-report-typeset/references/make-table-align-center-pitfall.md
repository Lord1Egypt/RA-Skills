# make_table 对齐列签名坑（2026-08-31 实测）

## 现象
写新 PDF 脚本时调用 `make_table(data, widths, align_center_cols=[0])` 直接抛：
```
TypeError: make_table() got an unexpected keyword argument 'align_center_cols'
```

## 根因
`make_table` 的 `align_center_cols` 是**可选参数**。如果所用模板/脚本的函数签名里没定义它，传了就报错。签名应为：
```python
def make_table(data, widths, header_bg=C_BLUE, fontsize=13, align_center_cols=None):
    ...
    # 函数体内必须补这段才生效：
    if align_center_cols:
        for c in align_center_cols:
            style.append(("ALIGN", (c,1), (c,-1), "CENTER"))
```

## 修复
- 写脚本前先 grep 确认所用 make_table 签名带 `align_center_cols=None`
- 不带就手动补参数 + 那段 `if align_center_cols` 循环，再调用

## 可用参考
本目录 `scripts/gen_agent_kb.py` 是**已跑通**的完整示例：封面+多章节+大量表格，make_table 带正确签名（含 `align_center_cols`）。做"把一篇 md/知识笔记做成专业中文 PDF"时直接复制它的内容区再改数据即可。
