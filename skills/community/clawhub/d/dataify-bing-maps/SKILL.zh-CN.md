---
name: dataify-bing-maps
description: "当用户使用 Bing Maps 搜索地点或查看地图时，执行此 skill。"
---

# Bing Maps

## 概述

使用此 skill 将自然语言 Bing Maps 请求转换为 Dataify Bing Maps API 字段，通过 `scripts/bing_maps.py` 调用固定的 Dataify 端点，并将 API 响应直接返回给用户，不进行总结、解析或后处理。

源 API 文档汇总在 `references/api.md` 中。当字段行为或响应结构不明确时请查阅该文件。

## 工作流程

1. 识别用户的地图/地点查询并将可选需求映射到 API 字段：
   - `q`: Bing Maps 搜索关键词。必填。
   - `json`: 输出格式。用户未指定输出格式时默认使用 `1`；`2` 表示 JSON+HTML，`3` 表示 HTML。
   - `cp`: 查询中心点 GPS 坐标，格式为 `纬度~经度`。仅当用户提供坐标时传入。
   - `setlang`: 两位语言/地区值，例如 `us`、`de`、`gb`。仅当用户要求语言/地区时传入。
   - `place_id`: Bing Maps 地点唯一引用。仅当用户提供地点 ID 时传入。
   - `first`: 本地结果偏移量。参数说明写明默认值为 `0`，因此用户未指定时使用 `0`。
   - `count`: 每页建议返回结果数量。最大值为 `30`，但最大值不是默认值。仅当用户要求结果数量时传入。
   - `no_cache`: `true` 表示跳过缓存，`false` 表示使用缓存。参数说明写明默认值为 `false`，因此用户未指定时使用 `false`。
2. 用户明确提供的字段值优先于推断值。
3. 当用户未指定某个值时，使用参数描述中的默认值：
   - `engine`: `bing_maps`
   - `json`: `1`
   - `first`: `0`
   - `no_cache`: `false`
   - `q`、`cp`、`setlang`、`place_id` 或 `count` 无默认值。
4. 切勿将文档示例当作默认值。不要添加坐标、`setlang=us` 或 `count=30` 等示例值，除非用户明确请求了该字段。
6. 使用 `python3` 运行内置 Python 脚本。通过 `--prompt` 传递完整的用户请求，仅在覆盖自动解析时添加显式标志。
7. 在实际调用前确保认证：
   - 从当前环境读取 `DATAIFY_API_TOKEN`。
   - 当 token 不包含 `Bearer ` 前缀时，脚本会自动添加。
   - 如果没有可用的 token，脚本会以中文提示退出；请要求用户输入 Dataify API token 或前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 注册。
9. 当需要机器可读的解析输出而不调用 API 时，运行 dry run：

```bash
python3 scripts/bing_maps.py --prompt "JiangSu" --dry-run
```

预期的 dry-run 负载：

```json
{
  "engine": "bing_maps",
  "q": "JiangSu",
  "json": "1",
  "first": "0",
  "no_cache": "false"
}
```


```bash
```

11. 将脚本输出直接返回给用户。不要总结地图结果、提取字段、重新格式化 JSON、解析嵌入的 JSON 字符串或处理返回的 HTML，除非用户另行要求处理。

## 脚本使用

脚本支持自动解析加显式覆盖：

```bash
python3 scripts/bing_maps.py \
  --prompt "搜索JiangSu，并返回 JSON 和 HTML" \
  --json 2
```

可用标志：

- `--q`、`--json`、`--cp`、`--lat`、`--lon`、`--setlang`、`--place-id`、`--first`、`--count`、`--no-cache`
- `--field key=value` 用于任何支持的 API 字段
- `--body-format form|json`，默认 `form`
- `--params-table` 打印所需的调用前 Markdown 参数表格并跳过网络/认证检查
- `--dry-run` 打印解析后的负载并跳过网络/认证检查

如果实际调用因 `DATAIFY_API_TOKEN` 缺失而失败，请要求用户提供 token 或前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 注册。

## 结果呈现

- 默认返回精简、可直接使用的结果：最相关的标题、链接和垂类关键字段，并在必要时说明数量或截断情况。
- 普通流程不暴露传输细节、固定引擎字段、任务内部状态或完整响应包装。
- 只有用户明确要求原始输出时才返回 raw JSON 或 HTML。
- 保留来源链接，区分字段缺失与空值，不得编造数据。

## 参数交互策略

- 当请求意图明确、只读、低风险且成本较低时，使用安全默认值直接执行。可以用一句话说明执行内容，但不要暂停等待确认。
- 只在缺少必填输入、存在会明显改变结果的歧义、大批量或多页采集、媒体下载、会明显增加积分消耗、不可逆操作，或用户明确要求查看参数时询问。
- 必须确认时，只展示会影响目标、范围、输出或成本的用户参数。优先使用一句简短说明；只有三个及以上关键值确实需要比较时才使用精简表格。
- 不要展示固定字段、空的可选字段、未修改的默认值、凭据或内部实现参数，例如引擎选择、响应格式开关、偏移量、spider ID 和文件名模板。
- 默认隐藏高级筛选项，除非用户主动询问或需要它们消除歧义。不得用文档示例值代替用户缺失的必填输入。
- 先返回首个结果，再提供相关的细化选项，不要在首次执行前强迫用户决定所有可选项。

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts receive 50 free credits. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
