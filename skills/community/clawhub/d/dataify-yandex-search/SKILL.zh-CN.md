---
name: dataify-yandex-search
description: "当用户想搜索 Yandex 时，使用此 skill。"
---

# Dataify Yandex Search

## 工作流程

1. 读取用户的请求并将其映射到以下 API 字段。
2. 仅从参数描述中获取默认值。不要将示例 YAML body 作为默认值来源。
3. 每次调用 API 前，使用内置脚本以 `--preview` 运行并向用户展示完整表格：

```bash
python3 scripts/yandex_search.py --text "<search query>" --preview
```

4. 询问用户是否需要修改参数。用户确认前不要调用 API。
5. 如果用户要求修改，调整参数，再次展示完整的预览表格并请求确认。
6. 确认后，检查 token。如果用户未提供 token 且 `DATAIFY_API_TOKEN` 不可用，停止操作并要求用户提供 Dataify API token 或前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 注册。
7. 使用已确认的参数调用 API：

```bash
python3 scripts/yandex_search.py --text "<search query>" --token "<token>"
```

8. 将脚本的标准输出直接返回给用户。不要对 API 响应进行解析、总结、翻译、过滤、重新格式化或其他处理。

## 预览表格

每次调用 API 前必须展示完整的字段列表。不要在表格中包含 `Authorization`。表格只能包含以下列：

- `参数名`
- `当前值`
- `默认值`
- `说明`

内置脚本通过以下方式生成此表格：

```bash
python3 scripts/yandex_search.py --text "<search query>" --preview
```

## 默认值

当用户未指定某个字段时，使用以下文档化默认值：

- `engine`: `yandex`
- `json`: `1`
- `yandex_domain`: `yandex.com`
- `lang`: 当 `yandex_domain` 为 `yandex.com` 时为 `en`
- `family_mode`: `1`
- `fix_typo`: `true`
- `groups_on_page`: `20`
- `no_cache`: `false`

无文档化默认值：

- `text`: 必须从用户请求中获取。
- `lr`: 除非用户指定，否则留空。
- `p`: 除非用户指定，否则留空；指定时页码从 `0` 开始。

来自 API 示例 body 的重要修正：

- 不要将示例中的 `family_mode: "0"` 当作默认值。描述中的默认值为中等，因此使用 `1`。
- 不要将示例中的 `no_cache: "true"` 当作默认值。描述中说明 `false` 是默认值。

## 字段映射

- `--json`: 输出格式。使用 `1` JSON，`2` JSON+HTML，`3` HTML，或 `4` Light JSON。
- `--yandex-domain`: Yandex 域名，如 `yandex.com`、`yandex.ru`、`ya.ru`、`yandex.kz`、`yandex.com.tr` 或其他支持的域名。
- `--lang`: 搜索语言，例如 `en`、`ru`、`tr`。
- `--lr`: 国家或地区 ID。
- `--p`: 页码，从 `0` 开始。
- `--family-mode`: 安全搜索模式。使用 `0` 关闭，`1` 中等，`2` 严格。
- `--fix-typo`: `true` 或 `false`。
- `--groups-on-page`: 每页最大结果组数。
- `--no-cache`: `true` 跳过缓存，`false` 使用缓存。
- `--params-json`: 用于非常规请求的原始字段覆盖 JSON 对象。使用 `null` 省略已有默认值的字段。

需要完整字段列表时，请查阅 `references/api_fields.md`。

## 示例

预览普通搜索的参数：

```bash
python3 scripts/yandex_search.py --text "OpenAI latest news" --preview
```

用户确认后调用 API：

```bash
python3 scripts/yandex_search.py --text "OpenAI latest news" --token "$DATAIFY_API_TOKEN"
```

预览俄语 Yandex、第 2 页、HTML 输出：

```bash
python3 scripts/yandex_search.py --text "artificial intelligence news" --yandex-domain yandex.ru --lang ru --p 1 --json 3 --preview
```
