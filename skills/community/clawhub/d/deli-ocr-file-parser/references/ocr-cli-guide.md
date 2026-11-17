# OCR 文件解析 CLI 场景指南

本指南承接 `deli-ocr-file-parser` 的可变命令示例、参数组织和结果映射。使用前必须先执行 [cli-common.md](./cli-common.md) 中的前置检查和命令发现步骤。

## 一、CLI 命令使用原则

1. 先用 `npx @delilegal/deli-cli@latest cmds deli-ocr-file-parser@1.0.0` 获取本次 `RUN id`、命令名和参数。
2. 后续调用必须采用当次返回的 `npx @delilegal/deli-cli@latest run_... <command> [options]` 形态。
3. 不在本指南中固化真实命令名；以下示例中的 `parse-file`、`ocr-file`、`pdf-to-markdown`、`image-ocr` 仅表示可能的命令类型，实际以 `cmds` 输出为准。
4. 文件路径、输出目录、语言、任务类型、是否保存原始响应等参数必须以当次 `cmds` 返回的 `usage` 和 `params` 为准。
5. 不把大段解析结果作为命令行参数传给其他工具；先保存为 Markdown 或文本文件，再交给其他 skill 或 Agent 分析。

示例 `cmds` 返回后，实际调用可能形如：

```bash
npx @delilegal/deli-cli@latest run_a1b2c3d4e5f6 parse-file --input "D:\case\合同扫描件.pdf" --output-dir "D:\case\parsed"
npx @delilegal/deli-cli@latest run_a1b2c3d4e5f6 image-ocr --input "D:\case\付款回单.png" --output-dir "D:\case\parsed" --lang "zh-cn+en"
npx @delilegal/deli-cli@latest run_a1b2c3d4e5f6 pdf-to-markdown --input "D:\case\法院文书扫描件.pdf" --output-dir "D:\case\parsed"
```

以上仅为参数组织示例。正式执行时必须替换为当次 `cmds` 返回的 `run_...`、命令名和参数。

## 二、调用前判断

只有出现以下情况才调用 OCR：

- 扫描版 PDF、图片、OFD 或票据图片无法被当前 Agent 原生解析。
- 原生解析结果为空、缺页、乱码、版式严重错乱，或表格、票据、印章、案号、金额等关键信息无法识别。
- 用户明确要求“用得理 OCR”“调用 OCR”“扫描版识别一下”“这个文件 agent 解析不了”。

不要调用 OCR 的情况：

- 文本、Markdown、HTML、CSV、JSON 可直接读取。
- PDF 或 Office 文件已被原生解析为可用文本。
- 图片内容可由平台视觉模型准确识别，且用户未要求得理 OCR。

## 三、支持格式判断

常见支持格式包括：

| 类型 | 扩展名 |
|------|--------|
| 文档 | `.pdf`、`.docx`、`.doc`、`.docm`、`.dotm`、`.rtf`、`.txt`、`.ofd` |
| 表格 | `.xlsx`、`.xls` |
| 图片 | `.png`、`.jpeg`、`.jpg`、`.gif`、`.bmp`、`.img` |
| 网页 | `.html` |

如果文件格式不支持，先提示用户转换格式，不调用 OCR。

## 四、场景化参数组织

### 1. 扫描版 PDF 转 Markdown

适用：合同扫描件、法院文书扫描件、证据材料 PDF。

参数应包含：

- 输入文件路径
- 输出目录
- 是否需要保存原始响应
- 语言，如 `zh-cn+en`
- 任务类型，如当前 `cmds` 支持 PDF 转 Markdown 或通用文件解析时按返回参数选择

输出建议：

```text
parsed/
├── 合同扫描件.md
└── raw_response/
```

### 2. 图片、票据或回单 OCR

适用：付款回单、发票、收据、身份证件、现场照片、截图。

参数应包含：

- 输入图片路径
- 输出目录
- 语言
- 是否需要保留原始响应，便于核对金额、日期、票号和账号

### 3. 批量文件处理

适用：目录中有多份合同、票据、扫描材料。

处理规则：

1. 逐个判断文件是否已能原生解析。
2. 只对原生解析失败或明显不可用的文件调用 OCR。
3. 输出到单独目录，不覆盖原始文件。
4. 建议按原文件名生成 `.md` 或 `.txt`，并保留文件对应关系。

### 4. 后续交给其他 skill

OCR 输出完成后：

- 合同扫描件：将 Markdown 交给合同审查、法律意见书或证据整理流程。
- 票据、回单、发票：交给证据整理或财务证据结构化流程。
- 法院文书：交给案例分析、法律意见或诉讼策略流程。

## 五、结果映射

最终交付时至少说明：

- 原始文件名
- 输出 Markdown 或文本文件路径
- 是否保存原始响应
- 解析是否完整
- 需要人工复核的字段

重点提醒人工复核：

- 金额
- 日期
- 姓名和主体名称
- 案号、合同编号、发票号码
- 银行账号和付款流水号
- 印章、签名、手写内容

## 六、失败处理

出现以下情况时，不要改用旧本地脚本或直接请求接口：

- `cmds` 未返回可用 OCR 命令
- 文件格式不支持
- CLI 鉴权未完成
- 上传或解析失败
- 输出结果为空或明显乱码

处理方式：

- 标注“命令不可用”“格式不支持”“解析失败”或“结果待复核”。
- 给出下一步建议，例如转换为 PDF/PNG、提供更清晰扫描件、拆分大文件或改用原生文本版本。
