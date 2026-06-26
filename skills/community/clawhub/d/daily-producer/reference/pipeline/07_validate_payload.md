# 07 校验 JSON

## 脚本

```bash
python3 scripts/validate_payload.py output/daily/{date}.json
```

## 作用

校验 AI 生成的日报 JSON 是否符合渲染器契约。**必须在渲染 HTML 之前运行。**

校验分两层：
- **错误（error）**：结构、字段、URL 契约不合法，必须修改后重新校验
- **告警（warning）**：结构合法，但来源质量不足（例如单源过多、多源合并不充分），应优先让模型回头补源后再进入渲染

## 输入

- `output/daily/{date}.json` — AI 生成的日报 JSON

## 输出

- 完全通过：`✅ 校验通过` + 统计信息
- 通过但有质量告警：`⚠️ 校验通过，但有多源告警` + 告警列表
- 失败：`❌ 校验失败` + 具体错误列表

## 用法

```bash
# 基本校验（自动查找同日期 candidates.json 做 URL 交叉校验）
python3 scripts/validate_payload.py output/daily/{date}.json

# 指定 candidates 文件
python3 scripts/validate_payload.py output/daily/{date}.json --candidates output/raw/{date}_candidates.json
```

## 校验项

### meta（必需）

- `date`：非空，格式 YYYY-MM-DD
- `date_label`：非空
- `role`：非空

### left_sidebar（必需）

- `overview`：数组，至少 2 条，每条有 title + text
- `actions`：数组，至少 2 条，每条有 text + prompt，type 必须是 learn/try/watch/alert 之一
- `trends`：有 rising/cooling/steady（均为数组）+ insight（字符串）

### articles（必需）

- 数组，至少 5 条
- 每条必须有：id（唯一）、title、priority、source、url
- priority 必须是：major/notable/normal/minor
- summary 必须有 what_happened + why_it_matters
- relevance 非空
- tags 是数组
- url 以 http 开头

### data_sources（必需）

- 非空数组

## 失败处理

如果校验失败：

1. 阅读错误列表
2. 修改对应字段
3. 重新运行校验
4. 直到通过后才能进入渲染步骤

如果只是出现多源告警：

1. 阅读告警列表，定位哪些 article 只有单源或来源不足
2. 回到 `candidates.json` 重新查找同事件的官方 / 媒体 / 社区来源
3. 补全 `credibility.sources`、更新 `cross_refs`
4. 再次运行校验，尽量消除高优先级条目的单源告警
5. 若最终仍保留单源，应在 `evidence` 中说明是“未找到第二来源”，而不是遗漏合并

示例错误输出：

```
❌ 校验失败，3 个错误：
   [meta.date_label] 缺失或为空
   [articles[2].summary.why_it_matters] 缺失
   [articles[5].url] 格式错误: example.com/...
```

### URL 交叉校验（自动执行）

脚本自动加载 `output/raw/{date}_candidates.json`，检查：

- 每条 article 的主 `url` 必须在 candidates 中存在
- 每条 `credibility.sources[*].url` 必须在 candidates 中存在
- 不同 article 不能使用相同的主 URL
- 含 `/example` 的 URL 视为假 URL

### credibility 一致性

**错误（会导致校验失败）：**
- `cross_refs > 1` 时 `sources` 数组不能为空
- `sources` 中每个 URL 不能含 `/example`
- `cross_refs` 应与 `sources` 数组长度一致
- 主 `url` 应出现在 `credibility.sources` 中
- `sources` 中重复 URL 不能重复计数

**告警（不会导致校验失败）：**
- article 只有 1 个有效来源
- `major` 条目只有 1 个有效来源
- `notable` 条目只有 1 个有效来源
- 可疑的“多源合并不足”情况，应提示模型回到 candidates 重新找同事件来源
