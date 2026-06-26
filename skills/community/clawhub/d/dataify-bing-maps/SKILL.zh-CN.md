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
5. 每次实际调用 API 前，向用户展示包含完整字段列表（除 `Authorization` 外）的 Markdown 表格。表格只能包含以下列：`参数名`、`当前值`、`默认值`、`说明`。`说明` 列必须为中文。询问用户是否需要修改。用户确认前不要调用 API。
6. 使用 `python3` 运行内置 Python 脚本。通过 `--prompt` 传递完整的用户请求，仅在覆盖自动解析时添加显式标志。
7. 在实际调用前确保认证：
   - 从当前环境读取 `DATAIFY_API_TOKEN`。
   - 如果用户在任务中提供了 token，使用 `--token` 传递或在调用脚本前设置 `DATAIFY_API_TOKEN`。
   - 当 token 不包含 `Bearer ` 前缀时，脚本会自动添加。
   - 如果没有可用的 token，脚本会以中文提示退出；请要求用户输入 Dataify API token 或前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 注册。
8. 在实际调用前生成确认表格：

```bash
python3 scripts/bing_maps.py --prompt "JiangSu" --params-table
```

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

10. 仅在 token 可用且用户确认参数表格后才运行实际调用。添加 `--confirmed`；脚本在没有该标志时拒绝实际调用：

```bash
python3 scripts/bing_maps.py --prompt "JiangSu" --confirmed
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
- `--token` 提供当前运行的 token
- `--body-format form|json`，默认 `form`
- `--params-table` 打印所需的调用前 Markdown 参数表格并跳过网络/认证检查
- `--dry-run` 打印解析后的负载并跳过网络/认证检查
- `--confirmed` 允许在用户确认参数表格后进行实际 API 调用

如果实际调用因 `DATAIFY_API_TOKEN` 缺失而失败，请要求用户提供 token 或前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 注册。
