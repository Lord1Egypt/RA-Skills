# 文件下载

## 简介

用于根据文件ID和文件类型下载文件。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `-id` / `--file-id` | 是 | 文件ID。 |
| `-type` / `--file-type` | 是 | 文件类型。 |
| `-o` / `--output` | 否 | 输出文件路径；若不指定，则默认保存在gangtise工作目录下的 `files`（自动编号）；与环境变量GTS_SAVE_FILE无关，单独生效。|

## 调用示例

```bash
python3 scripts/get_file.py --file-id 1234567890 --file-type "研究报告"
```

指定输出路径（可选）：
```bash
python3 scripts/get_file.py --file-id 1234567890 --file-type "研究报告" -o "results/file.pdf"
```

## 返回说明

- **成功**：文件保存到指定路径或默认工作目录下的 `files`，返回说明文字中含保存路径。
- **失败**：返回错误信息（如「获取文件失败：...」）。

`file_type` 需与检索结果中的类型一致，如「研究报告」「公司公告」「会议纪要」等。
