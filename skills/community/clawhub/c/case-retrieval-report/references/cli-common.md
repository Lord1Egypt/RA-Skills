# deli-cli 通用前置

适用于 `case-retrieval-report@1.0.0`。命中本 skill 后，凡需要执行类案检索、相似案例匹配、报告候选案例获取、分页查看更多结果或调用后端能力时，先执行本文档步骤。

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
- 如果鉴权未完成，不得继续执行类案检索；先提示用户完成 CLI 初始化。

## 2. 发现当前 skill 命令

完成前置检查后，用当前 skill scope 发现命令：

```bash
npx @delilegal/deli-cli@latest cmds case-retrieval-report@1.0.0
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

- 类案报告可以围绕不同法院层级或争议焦点形成多次检索，但每次调用前都要有明确目的。
- 不自动机械扩词；无结果或结果不足时，先说明不足并给出建议检索式或补充事实。
- 案号、法院、裁判日期、裁判结果、指导性案例属性和裁判观点必须来自 CLI 返回结果、用户材料或后续人工核验，不得编造。
- 对拟作为主要参照的关键类案，应在报告中提示通过官方渠道复核。
