# 深知写作助手（Clawhub Public 版）

这是深知写作助手的 Clawhub 分发版本。功能逻辑与自用版保持一致，但不内置深知搜索 API Key；首次使用前需要用户自行通过 Clawhub 渠道注册链接获取并配置 API Key。

## 能力范围

- 深知可信搜索：通过 `scripts/dkag_search.py` 调用搜索接口获取政策、数据和案例素材。
- 公文写作流程：由 `SKILL.md` 进行任务路由，按任务复杂度选择直接生成、追问、搜索、审查或严格流水线。
- 搜索策略：`reference/search_policy.md` 保留深知搜索逻辑、素材四分类和来源限制。
- 任务路由：`reference/task_router.md` 定义简单任务、常规任务、复杂任务和高风险任务的处理方式。
- 质量审查：`reference/review_checklist.md` 定义公文内容、素材来源、文种专项和 Word 输出检查项。
- Word 排版：通过 `scripts/format_document.py` 生成普通格式 `.docx`。
- 红头文件：通过 `scripts/template_generator.py` 代码化生成红头和表尾，不依赖 `templates/` 中的 Word 模板。

## 依赖

```bash
pip3 install python-docx requests
```

## 配置深知搜索 API Key

1. 访问 Clawhub 渠道注册链接：

```text
https://platform.dknowc.cn/auth/#/register?channel=2787E171-B0E5-4328-9946-47AC52434D1F&type=6
```

2. 注册并登录深知平台
3. 获取深知可信搜索 API Key
4. 将 `config.ini.example` 复制为 `config.ini`
5. 填入你的 API Key：

```ini
[dkag]
api_key=your_api_key_here
```

搜索接口固定为：

```text
https://open.dknowc.cn/dependable/search/
```

不要把包含真实 API Key 的 `config.ini` 上传或公开分享。

## 版本说明

当前 Clawhub Public 版基于 `3.0.20`。

## 常用测试

语法检查：

```bash
python3 -m py_compile scripts/dkag_search.py scripts/merge_search_results.py scripts/format_document.py scripts/template_generator.py
```

普通 Word 生成：

```bash
python3 scripts/format_document.py official-docs/input/dknowc-test.md --output dknowc-test.docx
```

红头 Word 生成：

```bash
python3 scripts/template_generator.py 通知 --input dknowc-test.docx --org "广东省政务服务和数据管理局" --doc-number "粤政数〔2026〕1号" --output dknowc-test-red.docx
```

搜索结果保存：

```bash
python3 scripts/dkag_search.py "留学人才来粤服务政策" --area 广东省 --clean --output result_gd.json
```

多次搜索合并：

```bash
python3 scripts/merge_search_results.py result_gd.json result_bj.json --output merged.json
```

## Public 版说明

- 本版本不内置 API Key。
- 用户通过 Clawhub 渠道注册链接获取 API Key。
- 深知搜索、素材分类、Word 生成、异常处理等功能逻辑与自用版一致。
- 如搜索失败或提示 API Key 未配置，请先检查 `config.ini` 是否存在且 `api_key` 是否有效。
