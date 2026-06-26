# 模板参数传递规范（给 agent）

本文件定义每个模板的参数清单、必填项和格式约束。调用 `scripts/send_feishu_card.py` 时，统一使用 `--var key=value` 传参。

---

## template: `movie-custom`

模板文件：`assets/templates/movie-custom.json`

### 必填参数

- `title`：电影标题（纯文本）
- `overview`：剧情简介（可多句）
- `rating`：评分文本（如 `8.3 / 10`）
- `runtime`：时长文本（如 `173 分钟`）
- `year`：上映日期/年份（如 `2023-01-22`）
- `genres`：类型列表文本（如 `科幻 / 灾难 / 冒险`）
- `country`：国家/地区（如 `中国` 或 `美国 / 英国`）
- `cast`：演员区块（Markdown 列表字符串）
- `director`：导演名
- `tagline`：一句话文案（可选；为空时自动不渲染该区块）
- `detail_url`：详情链接（TMDB 页面 URL，用于“查看详情”按钮）
- `tmdb_id`：TMDB 条目 ID（用于“立即订阅”回调）
- `media_type`：`movie`（可不传，规则默认补齐）
- `subscribe_disabled`：`true|false`（可选，控制“立即订阅”按钮禁用）
- `subscribe_button_text`：按钮文案（可选，默认“立即订阅”）

### 图片字段

- `poster_img_key`：飞书可用图片 key（`img_v3_...`），**必填**。
- 该字段用于模板中的海报渲染，不可直接传 URL。
- 若只有图片 URL/本地文件，可让脚本自动上传并注入：
  - `--poster-url <https://...jpg>`
  - `--poster-file </path/to/poster.jpg>`

### 重点：`cast` 参数样式（强约束）

`cast` 必须传 **Markdown 多行字符串**，每行一个演员，推荐格式：

```text
• **演员名** 饰 角色名
• **演员名** 饰 角色名
• **演员名** 饰 角色名
```

示例值：

```text
• **吴京** 饰 刘培强\n• **刘德华** 饰 图恒宇\n• **李雪健** 饰 周喆直
```

说明：
- 在 shell 里建议用单引号包裹整个值；换行用 `\n`。
- 不要传 JSON 数组，模板期望的是单个字符串。

### 一次完整示例

```bash
python3 scripts/send_feishu_card.py \
  --template movie-custom \
  --receive-id ou_xxx \
  --receive-id-type open_id \
  --account-id current \
  --var title='流浪地球2' \
  --var overview='太阳即将毁灭，人类启动数字生命与行星发动机双线计划。' \
  --var rating='8.3 / 10' \
  --var runtime='173 分钟' \
  --var year='2023-01-22' \
  --var genres='科幻 / 灾难 / 冒险' \
  --var country='中国' \
  --var cast='• **吴京** 饰 刘培强\n• **刘德华** 饰 图恒宇\n• **李雪健** 饰 周喆直' \
  --var director='郭帆' \
  --var tagline='爱是穿越一切的力量'
```

---

## cast 自动格式化工具

脚本：`scripts/format_cast.py`

用途：把演员 JSON 数组转换成 `cast` 字段要求的 Markdown 多行字符串。

### 输入示例

```json
[
  {"name": "吴京", "role": "刘培强"},
  {"name": "刘德华", "role": "图恒宇"},
  {"name": "李雪健", "role": "周喆直"}
]
```

### 用法

```bash
# 输出真实多行
python3 scripts/format_cast.py --input-file cast.json

# 输出 shell 友好的 \n 转义串（推荐给 --var cast=...）
python3 scripts/format_cast.py --input-file cast.json --escape-newline
```

## agent 执行规则（必须遵守）

1. 发送前先核对模板参数清单，缺失必填参数就先补齐。
2. `cast` 一律按上面的 Markdown 列表格式传。
3. 不要在参数值里注入未转义双引号；优先用单引号包裹 shell 值。
4. 失败时原样返回飞书错误码和 log_id，便于排障。
