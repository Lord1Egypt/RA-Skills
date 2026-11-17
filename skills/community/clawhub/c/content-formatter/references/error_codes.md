# 错误码定义 - content-formatter

> 来源: SKILL.md§异常处理

## 错误码列表

| 错误码 | 描述 | 触发条件 | 处理方案 |
|:-------|:-----|:---------|:---------|
| UNKNOWN_PLATFORM | 未知平台 | platform不在29平台清单中 | 降级使用L1通用HTML排版，layer标记L1 |
| CONVERTER_NOT_FOUND | 专属排版器不可用 | format_converter.py文件不存在 | 降级到L1通用HTML，layer标记L1(fallback) |
| CONVERTER_FAILED | 专属排版器调用失败 | L2排版器超时或返回错误 | 降级到L1通用HTML，layer标记L1(fallback) |
| MARKDOWN_LIB_MISSING | markdown库未安装 | import markdown失败 | 使用简单正则替换进行基础转换，layer标记L1(基础) |
| FORMAT_ERROR | 排版引擎内部异常 | 未预期的Exception | 返回 {success:false, error, code} |
| CONTENT_EMPTY | 内容为空 | --content和--content-file均未提供或为空 | 返回错误，提示提供内容 |
| FILE_NOT_FOUND | 内容文件不存在 | --content-file指定的文件路径无效 | 返回错误，提示检查文件路径 |

## 降级行为

- L2排版失败 → 自动降级到L1通用HTML（不中断流程）
- markdown库缺失 → 使用正则替换基础转换（不中断流程）
- 未知平台 → 使用L1默认排版（不中断流程）
- 排版引擎内部异常 → 返回结构化JSON错误（中断流程）

## layer标记说明

| layer值 | 含义 |
|:--------|:-----|
| L0 | Markdown原文输出，无需转换 |
| L1 | 通用HTML转换成功 |
| L1(fallback) | L2失败后降级到L1 |
| L1(基础) | markdown库缺失，使用正则基础转换 |
| L2 | 平台专属排版成功 |
| L3 | 纯文本截断成功 |
