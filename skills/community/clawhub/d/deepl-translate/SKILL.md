---
name: deepL-translate
description: 当用户明确要求使用 DeepL 官方 API 时使用，适用于文本翻译、文档翻译、语言与用量查询，以及 glossary v2/v3 管理。仅连接 DeepL 官方 API 域名，使用环境变量中的 DEEPL_API_KEY，不读取其他凭证。
---

# DeepL 翻译与 API 工具

当用户明确要求使用 DeepL 官方 API 时，使用这个 skill，而不是普通翻译能力。

## Prerequisites

- 需要可用的 `python3` 运行环境。
- 需要在环境变量中设置 `DEEPL_API_KEY`。
- 如果使用 DeepL Free，可额外设置 `DEEPL_API_BASE_URL=https://api-free.deepl.com`。
- 脚本仅依赖 Python 标准库，不需要安装额外三方包。

## 安全边界

- 仅允许请求 `https://api.deepl.com` 或 `https://api-free.deepl.com`。
- 仅使用环境变量 `DEEPL_API_KEY` 进行认证，不读取其他凭证、token 或本地账号配置。
- 不执行 shell、不会下载或运行外部脚本、不会启动子进程。
- 只有在用户显式提供 `--text`、`--file`、`--stdin`、`--entries-file` 或文档翻译文件时，才会读取对应本地内容。
- 读取到的文本、词汇表条目或文档文件，只会发送到 DeepL 官方 API，不会转发到其他域名。

## 能力范围

当前脚本尽量覆盖 DeepL OpenAPI 中常用且公开的接口能力：

- 核心能力：
  - 文本翻译：`/v2/translate`
  - 语言查询：`/v2/languages`
  - 用量查询：`/v2/usage`
  - 文本润色 / 改写：`/write/rephrase`
- 扩展能力：
  - 文档翻译
  - glossary v2 / v3 管理
- 文本翻译：`/v2/translate`
- 语言查询：`/v2/languages`
- 用量查询：`/v2/usage`
- 文本润色 / 改写：`/write/rephrase`
- 文档翻译：
  - 上传：`/v2/document`
  - 状态查询：`/v2/document/{document_id}`
  - 结果下载：`/v2/document/{document_id}/result`
  - 一键闭环：脚本封装的 `document-translate`
- glossary v2：
  - 列表、详情、条目、创建、删除
  - 语言对查询：`/v2/glossary-language-pairs`
- glossary v3：
  - 列表、详情、条目查询
  - 创建 glossary
  - PATCH 更新 glossary / 合并字典
  - PUT 替换指定语言对字典
  - 删除指定字典
  - 删除 glossary

## 快速开始

1. 设置 `DEEPL_API_KEY`。
2. 默认基础地址为 `https://api.deepl.com`。
3. 如果使用 DeepL API Free，可设置：

```bash
export DEEPL_API_BASE_URL=https://api-free.deepl.com
```

只允许以上两个 DeepL 官方基础地址，其他地址会被脚本拒绝。

4. 调用脚本：

```bash
cd <skill-directory>
python3 scripts/deepl_translate.py <子命令> ...
```

其中 `<skill-directory>` 表示当前 skill 的安装目录。

也可以不切换目录，直接执行：

```bash
python3 /path/to/deepL-translate/scripts/deepl_translate.py <子命令> ...
```

为兼容旧用法，如果不写子命令、直接传 `--text --target-lang` 这类参数，脚本会自动按 `translate` 处理。

## For Agents

- 默认优先使用核心能力：`translate`、`rephrase`、`languages`、`usage`。
- 只有在用户明确要求上传文档或管理 glossary 时，再使用扩展能力。
- 如果只是改写语气、商务化表达、同语种润色，优先用 `rephrase`，不要误用跨语种翻译。
- 需要结构化结果时使用 `--json`。

## For Humans

- 示例命令中的 `<skill-directory>` 表示当前 skill 的安装目录。
- 如果宿主平台已经帮你切换到 skill 目录，可直接执行 `python3 scripts/deepl_translate.py ...`。
- 如果宿主平台以绝对路径调用脚本，也可以直接使用 `/path/to/.../scripts/deepl_translate.py`。

## 常用命令

文本翻译：

```bash
cd <skill-directory>
python3 scripts/deepl_translate.py translate \
  --source-lang EN \
  --target-lang ZH \
  --text "Hello, world"
```

兼容旧写法：

```bash
cd <skill-directory>
python3 scripts/deepl_translate.py \
  --source-lang EN \
  --target-lang ZH \
  --text "Hello, world"
```

查询支持语言：

```bash
cd <skill-directory>
python3 scripts/deepl_translate.py languages --type target --json
```

查询账户用量：

```bash
cd <skill-directory>
python3 scripts/deepl_translate.py usage --json
```

文本润色 / 同语种变体改写：

```bash
cd <skill-directory>
python3 scripts/deepl_translate.py rephrase \
  --target-lang EN-US \
  --writing-style business \
  --text "please send me the report soon"
```

文档翻译闭环：

```bash
cd <skill-directory>
python3 scripts/deepl_translate.py document-translate \
  --file ./input.docx \
  --target-lang DE \
  --output-file ./output_de.docx
```

创建 v2 glossary：

```bash
cd <skill-directory>
python3 scripts/deepl_translate.py glossary-v2-create \
  --name demo-v2 \
  --source-lang EN \
  --target-lang DE \
  --entries-file ./entries.tsv
```

创建 v3 glossary：

```bash
cd <skill-directory>
python3 scripts/deepl_translate.py glossary-v3-create \
  --name demo-v3 \
  --dict EN:DE:./en_de.tsv:tsv \
  --dict EN:FR:./en_fr.tsv:tsv
```

## 使用建议

- 短文本翻译优先使用 `translate`。
- 如果只是英文变体、美化语气、商务化表达，优先使用 `rephrase`，不要误用跨语种翻译。
- UI 文案、短句、多义词，尽量传 `--context`。
- 需要完整返回结构时加 `--json`。
- 需要 glossary 时，先确认是旧的 v2 单语言对，还是新的 v3 多语言词汇表。
- 文档翻译如果只想拆步骤排查，可分别使用 `document-upload`、`document-status`、`document-download`。

## 已知约束

- `translate` 单次最多 50 个 `text` 项，请求体总大小不能超过 128 KiB。
- `glossary_id` 依赖 `source_lang`。
- 文档翻译为异步流程，必须先上传，再轮询状态，最后下载结果。
- 文档翻译、`--file`、`--stdin`、`--entries-file` 会把用户明确提供的内容发送到 DeepL 官方服务。
- 脚本尽量覆盖官方公开接口，但某些新接口字段可能随 DeepL 文档演进而变化。

## 常见错误

- `未设置 DEEPL_API_KEY。`
  - 需要先导出 `DEEPL_API_KEY` 再调用命令。
- `DEEPL_API_BASE_URL 仅允许配置为 ...`
  - 只支持 `https://api.deepl.com` 和 `https://api-free.deepl.com`。
- `未提供输入文本。请使用 --text、--file 或 --stdin。`
  - `translate` 和 `rephrase` 必须显式提供输入内容。
- `--glossary-id 需要同时提供 --source-lang。`
  - glossary 翻译调用时，必须同时指定源语言。
- `文档翻译失败：...`
  - 文档翻译由 DeepL 异步处理，失败原因以返回的错误信息为准。

## 参考资料

- 若需要接口摘要、端点列表和字段说明，读取 [references/deepl_api.md](references/deepl_api.md)。
