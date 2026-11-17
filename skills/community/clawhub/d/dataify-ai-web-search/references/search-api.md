# AI Web API Search 静态参数契约

本文件是数据库 AI Web 配置的静态快照，不是运行时动态生成。

- 接口：`POST https://aiwebapi.dataify.com/search`（可用 `AI_WEB_API_BASE_URL` 覆盖）
- 鉴权：`Authorization: Bearer <DATAIFY_API_TOKEN>`
- 请求体：`application/json`
- `time_range`：网页搜索和新闻搜索支持；购物搜索和学术搜索不支持。
- 购物搜索不接收输入 `url`。
- `extract_options` 及其子参数仅在 `extract_content=true` 时发送。

## 网页搜索

- unique_id：`search_web`
- source：`web`

| 参数名 | key | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 搜索词 | `query` | string | 是 | -- | 去除首尾空格后长度 1～256 字符 |
| 结果类型 | `source` | enum | 否 | web | 固定为 web |
| 结果数量 | `max_results` | integer | 否 | 10 | 1～100 |
| 结果时间范围 | `time_range` | enum | 否 | -- | hour、day、week、month、year |
| 结果来源国家 | `country` | string | 否 | US | 两位大写国家码 |
| 结果页面语言 | `language` | string | 否 | en | 界面语言代码 |
| 是否内容提取 | `extract_content` | boolean | 否 | False | 是否继续提取每条结果的正文 |
| 内容提取设置 | `extract_options` | object | 否 | -- | 仅当 extract_content=true 时可传 |
| 结果格式 | `formats` | array<string> | 否 | markdown | markdown、raw_html、clean_html、links |
| 保留标签 | `include_tags` | array<string> | 否 | -- | 最多 50 项，每项最长 2048 UTF-8 字节 |
| 排除标签 | `exclude_tags` | array<string> | 否 | -- | 最多 50 项，每项最长 2048 UTF-8 字节 |
| 是否只保留主体 | `only_main_content` | boolean | 否 | True | true 只保留正文，false 保留更多内容 |
| 采集策略 | `advanced_mode` | boolean | 否 | True | false 使用无渲染 HTTP；true 使用自动解锁链路 |
| 页面请求限制 | `timeout_ms` | integer | 否 | 60000 | 1000～120000 毫秒 |
| 页面加载限制 | `wait_for_ms` | integer | 否 | 0 | 0～30000 毫秒，且不得超过 timeout_ms 的一半 |
| 页面缓存限制 | `max_age_ms` | integer | 否 | 172800000 | 0～172800000 毫秒；0 表示强制回源 |

## 购物搜索

- unique_id：`search_shopping`
- source：`shopping`
- 不支持 `time_range`，不接收输入 `url`。

| 参数名 | key | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 搜索词 | `query` | string | 是 | -- | 去除首尾空格后长度 1～256 字符 |
| 结果类型 | `source` | enum | 否 | shopping | 固定为 shopping |
| 结果数量 | `max_results` | integer | 否 | 10 | 1～100 |
| 结果来源国家 | `country` | string | 否 | US | 两位大写国家码 |
| 结果页面语言 | `language` | string | 否 | en | 界面语言代码 |
| 是否内容提取 | `extract_content` | boolean | 否 | False | 是否继续提取每条结果的正文 |
| 内容提取设置 | `extract_options` | object | 否 | -- | 仅当 extract_content=true 时可传 |
| 结果格式 | `formats` | array<string> | 否 | markdown | markdown、raw_html、clean_html、links |
| 保留标签 | `include_tags` | array<string> | 否 | -- | 最多 50 项，每项最长 2048 UTF-8 字节 |
| 排除标签 | `exclude_tags` | array<string> | 否 | -- | 最多 50 项，每项最长 2048 UTF-8 字节 |
| 是否只保留主体 | `only_main_content` | boolean | 否 | True | true 只保留正文，false 保留更多内容 |
| 采集策略 | `advanced_mode` | boolean | 否 | True | false 使用无渲染 HTTP；true 使用自动解锁链路 |
| 页面请求限制 | `timeout_ms` | integer | 否 | 60000 | 1000～120000 毫秒 |
| 页面加载限制 | `wait_for_ms` | integer | 否 | 0 | 0～30000 毫秒，且不得超过 timeout_ms 的一半 |
| 页面缓存限制 | `max_age_ms` | integer | 否 | 172800000 | 0～172800000 毫秒；0 表示强制回源 |

## 新闻搜索

- unique_id：`search_news`
- source：`news`
- 支持 `time_range`。

| 参数名 | key | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 搜索词 | `query` | string | 是 | -- | 去除首尾空格后长度 1～256 字符 |
| 结果类型 | `source` | enum | 否 | news | 固定为 news |
| 结果数量 | `max_results` | integer | 否 | 10 | 1～100 |
| 结果时间范围 | `time_range` | enum | 否 | -- | hour、day、week、month、year |
| 结果来源国家 | `country` | string | 否 | US | 两位大写国家码 |
| 结果页面语言 | `language` | string | 否 | en | 界面语言代码 |
| 是否内容提取 | `extract_content` | boolean | 否 | False | 是否继续提取每条结果的正文 |
| 内容提取设置 | `extract_options` | object | 否 | -- | 仅当 extract_content=true 时可传 |
| 结果格式 | `formats` | array<string> | 否 | markdown | markdown、raw_html、clean_html、links |
| 保留标签 | `include_tags` | array<string> | 否 | -- | 最多 50 项，每项最长 2048 UTF-8 字节 |
| 排除标签 | `exclude_tags` | array<string> | 否 | -- | 最多 50 项，每项最长 2048 UTF-8 字节 |
| 是否只保留主体 | `only_main_content` | boolean | 否 | True | true 只保留正文，false 保留更多内容 |
| 采集策略 | `advanced_mode` | boolean | 否 | True | false 使用无渲染 HTTP；true 使用自动解锁链路 |
| 页面请求限制 | `timeout_ms` | integer | 否 | 60000 | 1000～120000 毫秒 |
| 页面加载限制 | `wait_for_ms` | integer | 否 | 0 | 0～30000 毫秒，且不得超过 timeout_ms 的一半 |
| 页面缓存限制 | `max_age_ms` | integer | 否 | 172800000 | 0～172800000 毫秒；0 表示强制回源 |

## 学术搜索

- unique_id：`search_scholar`
- source：`scholar`
- 不支持 `country` 或 `time_range`。

| 参数名 | key | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 搜索词 | `query` | string | 是 | -- | 去除首尾空格后长度 1～256 字符 |
| 结果类型 | `source` | enum | 否 | scholar | 固定为 scholar |
| 结果数量 | `max_results` | integer | 否 | 10 | 1～100 |
| 结果页面语言 | `language` | string | 否 | en | 界面语言代码 |
| 是否内容提取 | `extract_content` | boolean | 否 | False | 是否继续提取每条结果的正文 |
| 内容提取设置 | `extract_options` | object | 否 | -- | 仅当 extract_content=true 时可传 |
| 结果格式 | `formats` | array<string> | 否 | markdown | markdown、raw_html、clean_html、links |
| 保留标签 | `include_tags` | array<string> | 否 | -- | 最多 50 项，每项最长 2048 UTF-8 字节 |
| 排除标签 | `exclude_tags` | array<string> | 否 | -- | 最多 50 项，每项最长 2048 UTF-8 字节 |
| 是否只保留主体 | `only_main_content` | boolean | 否 | True | true 只保留正文，false 保留更多内容 |
| 采集策略 | `advanced_mode` | boolean | 否 | True | false 使用无渲染 HTTP；true 使用自动解锁链路 |
| 页面请求限制 | `timeout_ms` | integer | 否 | 60000 | 1000～120000 毫秒 |
| 页面加载限制 | `wait_for_ms` | integer | 否 | 0 | 0～30000 毫秒，且不得超过 timeout_ms 的一半 |
| 页面缓存限制 | `max_age_ms` | integer | 否 | 172800000 | 0～172800000 毫秒；0 表示强制回源 |

## 响应说明

- search 的 `outputs` 通常是数组，无结果可能为 `null`。
- 购物和新闻结果中的 `url` 可能是 Google 搜索页或跳转地址，不一定是最终来源 URL。
- `snippet` 可能为 `null`。