# deli-cli 通用前置

适用于 `deli-ocr-file-parser@1.0.0`。命中本 skill 后，凡需要调用得理 OCR、文件解析、PDF 转 Markdown、图片 OCR、OFD 解析或后端能力时，先执行本文档步骤。

## 1. 检查 CLI 与鉴权

先运行：

```bash
npx @delilegal/deli-cli@latest check
```

如提示未配置 API Key，引导用户前往以下地址创建：

```text
https://open.delilegal.com/personal/keys
```

然后写入本机 CLI 配置：

```bash
npx @delilegal/deli-cli@latest init --apikey "你的 API Key"
```

CLI 配置保存位置：

```text
~/.deli/cli/config.json
```

注意：

- 不读取、不创建、不提示用户配置 skill 目录下的旧 `config.json`。
- 如果鉴权未完成，不得继续调用 OCR 或文件解析命令；先提示用户完成 CLI 初始化。

## 2. 发现当前 skill 命令

完成前置检查后，用当前 skill scope 发现命令：

```bash
npx @delilegal/deli-cli@latest cmds deli-ocr-file-parser@1.0.0
```

必须解析本次 `cmds` 输出中的以下字段：

- `RUN id`
- `usage`
- `commands`
- `params`
- `description`

后续调用必须使用当次返回的 `run_...` 入口、命令名和参数形态，不得假设固定命令或固定参数一定存在。

## 无可用命令时的执行边界

如 `cmds` 返回为空、未提供可执行命令、未暴露当前任务需要的工具，或当前 skill scope 没有后端 MCP/工具服务，不视为 skill 失败。此时不再尝试通过 CLI 调用 MCP；Agent 应直接依据本 `SKILL.md`、本地 `references/`、`assets/` 和用户材料完成本 skill 的主体工作。

在无可用命令时，外部法规/案例/地方口径/动态数据/后端计算等无法由 CLI 核验的内容必须标注“检索受限”“命令不可用”或“需人工复核”；不得编造 CLI 未返回的依据、案例、数值或结论。

## 3. 调用约束

- 原生解析成功时，不调用 OCR。
- 每个文件先判断是否确需 OCR，再按文件逐个调用，避免重复解析。
- 命令、参数、输出路径、是否保存原始响应等均以 `cmds` 当前输出为准。
- 命令不可用、文件格式不支持或解析失败时，先说明原因和下一步建议，不自行改用旧脚本或直接请求接口。
