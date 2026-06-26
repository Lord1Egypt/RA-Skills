# Step Contract 标准

用于创建、审查或修补 `plans/step-NN-name.md`。

## 必需结构

每个 Step Contract 必须自包含，并包含以下 section：

```md
# Step NN: [Name]

## 输入
[明确文件、API、用户上下文，或写“无”]

## 任务
[命令或受限语义指令；一个 step 只做一类工作]

## 输出
[精确产物路径、对象结构、状态文件或可见结果]

## 验证命令
[可执行命令、schema 检查、断言、清单或人工门禁]

## 验证失败处理
[重试次数、跳过/降级/停止/人工复核，以及失败记录位置]

## 下一步
`plans/step-NN-next.md` 或 `TERMINAL`
```

## 拆分规则

如果一个 step 同时抓取、分类、渲染、通知，应该拆开。

大型渲染 step 可以内部拆成多个 block，但每个 block 都要有验证，通过后才能继续。

## 命令可移植性

生成 Step Contract 时，不要默认使用某一种 shell 方言。

- 如果目标环境没有明确是 Bash，避免直接写 `mkdir -p`、`rm -f`、`test -d`、heredoc 等 Unix shell 写法。
- 如果目标环境没有明确是 PowerShell，避免直接写 PowerShell 专用命令作为唯一验证。
- 默认优先把清理、转换、验证写成 `scripts/*.py` 这类跨平台脚本，再在 step 中调用 `python scripts/name.py`。
- 如果必须使用 shell 命令，在 step 的输入或任务里明确运行环境，例如 `shell: bash` 或 `shell: PowerShell`。
- 验证命令必须能在目标环境真实执行，不要只写概念性检查。

## 复查清单

最终定稿前检查：

- runtime `SKILL.md` 是否足够薄。
- 业务细节是否都在 `plans/`，而不是塞在引擎里。
- 每个 step 是否都有 输入 / 任务 / 输出 / 验证命令 / 验证失败处理 / 下一步。
- 每个 step 是否只做一类工作。
- 验证是否检查结构和内容，而不是只检查文件存在。
- raw/source 字段是否被保护，避免 Agent 改写。
- LLM 判断是否被限制在枚举、小摘要和授权字段里。
- 失败策略是否有边界。
- 是否存在 `TERMINAL`。
- 是否写明隐藏依赖：cwd、凭据、当前时间、登录态、外部工具、定时任务。
- 命令是否匹配目标 shell；不确定时是否改为跨平台脚本。
- 不可逆动作是否有人工或外部门禁。
- 执行 Agent 是否避免读取未来 step。
