---
name: 度慧文档转换-文档转PDF
description: 当需要通过阿里云市场的度慧文档转换将单个本地文档转换为 PDF 时，请使用此 skill。凡是请求中提到“度慧”、“文档转PDF”、“doc to pdf”、“文档转换”、“格式转换”、“文档格式转换”或“PDF转换”，或者需要通过异步 API 将单个本地 Office/WPS/OFD/图片/文本/网页等任意文件转换为 PDF 时，均应触发此 skill
homepage: https://market.aliyun.com/detail/cmapi00044564
compatibility: Requires python3, DUHUI_ALI_APPCODE, and network access to Duhui/Alibaba endpoints.
always: false
metadata:
   clawdbot:
      emoji: "📄"
      requires:
         bins:
            - python3
         env:
            - DUHUI_ALI_APPCODE
   audit:
      runtime_python_packages: []
      external_endpoints:
         - https://file.duhuitech.com/k/tmp_up.json
         - https://fmtmp.oss-cn-shanghai.aliyuncs.com
         - https://doc2pdf.market.alicloudapi.com/v2/convert_async
         - https://api.duhuitech.com/q
      data_handling:
         uploads_local_files_to_vendor_controlled_oss: true
         fetches_temporary_upload_credentials_at_runtime: true
         cleanup_remote_source_best_effort: true
         persists_secrets_to_disk: false
         secrets_must_not_be_requested_in_chat: true
         requires_user_notice_before_upload: true
---

# 度慧文档转PDF

## Overview

用这个 skill 处理“单个本地文件转单个 PDF”的度慧异步转换任务。
标准链路是：本地文件 -> 阿里云 OSS 临时上传 -> 把 OSS 对象直链放进 `input` -> `v2/convert_async` -> 轮询查询 -> 下载本地 PDF -> 删除 OSS 临时文件。

## Required Runtime And Secret

- 必需二进制：`python3`
- Python 侧只依赖标准库，不需要额外安装第三方包
- 必需环境变量：`DUHUI_ALI_APPCODE`
- AppCode 获取地址：`https://market.aliyun.com/detail/cmapi00044564`
- 在运行转换脚本前，agent 必须确保 `DUHUI_ALI_APPCODE` 已出现在执行环境中
- 本 skill 不规定 secret 的存储、检索或注入方式；这由用户自己的 agent 能力和授权策略决定

## Network Endpoints

- `https://file.duhuitech.com/k/tmp_up.json`：运行时获取临时 OSS 上传凭证
- `https://fmtmp.oss-cn-shanghai.aliyuncs.com`：vendor 控制的临时 OSS 桶，用于上传本地源文件
- `https://doc2pdf.market.alicloudapi.com/v2/convert_async`：提交异步转换请求
- `https://api.duhuitech.com/q`：轮询转换状态
- vendor 返回的 `pdfurl`：下载输出 PDF

## Data Flow And Privacy

- 本地源文件会先上传到阿里云 OSS 上海地域临时桶 `fmtmp.oss-cn-shanghai.aliyuncs.com`
- 上传完成后会把 OSS 对象 URL 传给 vendor 的异步转换接口
- 脚本会在运行时从 `https://file.duhuitech.com/k/tmp_up.json` 获取临时上传凭证，仅供当前进程使用
- 转换结束后会 best-effort 删除 OSS 临时源文件；如果删除失败，远端源文件可能短暂残留
- agent 不得在聊天、日志或最终答复里回显 AppCode
- agent 只有在用户明确同意在聊天里直接粘贴 AppCode
- agent 只有在用户明确同意且其自身 secret 管理策略允许时，才能持久化或缓存 AppCode

## When To Use

- 用户明确提到度慧、文档转 PDF、文档转换、格式转换、PDF 转换、压缩pdf，PDF水印
- 用户要把单个本地 `doc/docx/ppt/pptx/xls/xlsx/ofd/img/txt/html/...` 文件转成 PDF
- 任务需要走度慧的异步接口，而不是本地 LibreOffice 或其他转换器

## Do Not Use

- 直接 URL 输入
- Base64 输入
- 回调 URL

## Workflow

1. 先确认运行前置条件。
   - 运行环境必须可用 `python3`。
   - 只检查环境变量 `DUHUI_ALI_APPCODE`。
   - 如果环境变量已经存在，直接运行转换脚本；不要要求用户重复输入 AppCode。
   - 如果环境变量不存在，必须明确告诉用户：当前执行环境缺少 `DUHUI_ALI_APPCODE`，请先到阿里云市场商品页获取 AppCode：`https://market.aliyun.com/detail/cmapi00044564`。不要只笼统地说“请提供 AppCode”。
   - agent 应引导用户通过其支持的安全 secret 配置机制、环境变量机制或本地 secret store 来配置 `DUHUI_ALI_APPCODE`。如果 agent 支持安全的非聊天式 secret 输入，可指导用户使用该机制。
   - 只有在 agent 无法安全提供 `DUHUI_ALI_APPCODE` 且用户尚未完成配置时，才停止执行并等待用户完成配置。
2. 默认优先运行脚本，不要手写 OSS 上传或 HTTP 调用逻辑：

```bash
python3 scripts/duhui_doc_to_pdf.py ./input.docx
```

4. 用户指定输出路径时，加 `--output`：

```bash
python3 scripts/duhui_doc_to_pdf.py ./input.docx --output ./output.pdf
```

5. 默认会覆盖同名输出 PDF；如果用户要保留旧结果，显式指定另一个 `--output` 路径。
6. 只有在文件后缀缺失、错误、或需要强制覆盖源类型时才传 `--type`。
7. 需要 vendor `v2` 可选参数时，用 `--extra-params '<json>'` 透传，例如：

```bash
python3 scripts/duhui_doc_to_pdf.py ./input.docx --extra-params '{"pagesize":2,"compress":1}'
```

8. 绝不在聊天、日志或最终答复里回显 AppCode 或脚本内置的 OSS 凭证；持久化时也只用占位符，不要把秘密再次展示出来。
9. 当需要确认支持格式、把用户的细化要求映射成更多 `v2` 参数、查看 vendor 参数细节、或排查 vendor 返回字段时，读取 [references/doc_to_pdf_ali.md](references/doc_to_pdf_ali.md)。

## Missing AppCode Prompt

- 当 `DUHUI_ALI_APPCODE` 缺失时，优先使用类似下面的提示，而不是直接中止：

```text
当前执行环境缺少 DUHUI_ALI_APPCODE。
请先到阿里云市场商品页获取度慧文档转 PDF 的 AppCode：
https://market.aliyun.com/detail/cmapi00044564

请改用你当前 agent 支持的安全 secret 配置方式、环境变量机制或本地 secret store 完成配置；配置完成后再继续转换。
```

## Output Contract

- 进度信息只写到 `stderr`
- `stdout` 只输出一个 JSON
- 成功 JSON 包含：`status`, `token`, `output_path`, `pdf_url`, `page_count`, `filesize`, `source_object_key`
- 失败 JSON 包含：`status`, `stage`, `token`, `reason`

## Notes

- 脚本始终只处理一个本地输入文件
- 脚本只使用 Python 标准库，不依赖额外 Python 包
- OSS 对象名固定为 `up/<uuid4><原扩展名>`
- 运行时会从 `https://file.duhuitech.com/k/tmp_up.json` 请求临时 OSS 上传凭证
- 上传后直接把 OSS 对象 URL 传给 vendor，不生成签名 URL
- 查询接口不带认证，固定每 2 秒轮询一次，最长等待 60 分钟
- 转换结束后会尝试删除 OSS 临时源文件；删除失败只记 warning，不覆盖主错误
- `DUHUI_ALI_APPCODE` 的存储、持久化、检索和注入由用户自己的 agent 负责
