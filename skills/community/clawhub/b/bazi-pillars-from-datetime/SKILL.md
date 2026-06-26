---
name: bazi-pillars-from-datetime
description: Use when a task involves deriving bazi chart data from Gregorian datetime and timezone, or generating a grounded user-language analysis from an existing chart JSON plus the local knowledge files.
---

# 八字排盘与分析

## 概览
这个 skill 现在包含两个明确模式，必须先判断当前任务属于哪一种：

1. `chart` 模式：把公历日期时间转换成可复现的八字排盘结果。
2. `analysis` 模式：基于已有盘面 JSON、用户问题和本地知识文件生成适配用户语言的分析。

不要把两种模式混用。排盘负责事实，分析负责表达与建议。

## 何时使用

### 使用 `chart` 模式
- 用户提供出生日期、时间、时区、地点，要求排盘、算四柱、看大运、看流年。
- 任务需要结构化 JSON 结果，供后续程序或分析环节消费。
- 需要稳定、可重复的计算结果，而不是自由发挥的解释。

### 使用 `analysis` 模式
- 已经有 `chart` 盘面 JSON，用户要求分析事业、婚恋、健康、整体趋势或指定年份。
- 任务需要生成面向用户的中文报告，而不是重新计算排盘。
- 需要引用 `knowledge.md` 的解释素材，并遵循 `prompt.md` 的输出结构。

### 使用顺序
- 如果用户同时要“排盘 + 分析”，先执行 `chart`，再把结果传给 `analysis`。
- 如果用户只给了 `chart`，不要重复排盘。
- 如果用户只给了生日信息但要分析，先排盘，再分析。

## 共享约束
- 排盘事实以 `main.py` 为准。
- 分析不得篡改盘面字段，不得臆造盘面中不存在的干支、岁运或结论。
- 不使用农历换算。
- 不输出宿命化、绝对化、恐吓式表达。
- 信息不足时，明确说明缺口和影响，不强行补全。
- 分析语言默认跟随用户；若未指定也无法判断，则默认使用简体中文。

## 模式一：`chart`

### 目标
输出一个确定性、可复现、可被程序消费的八字 JSON 合同。该模式不生成用户面向的自然语言分析。

### 输入合同
输入为 JSON，对应 `main.py` 从标准输入读取的 payload：

```json
{
  "datetime": "YYYY-MM-DDTHH:MM:SS",
  "timezone": "IANA/Timezone",
  "location": {
    "name": "City/Region",
    "longitude": 0.0,
    "latitude": 0.0,
    "lookup_mode": "auto|local|online",
    "lookup_provider": "nominatim|amap|tencent",
    "lookup_key": "optional-api-key",
    "lookup_path": "/path/to/cities.json",
    "cache_path": "/path/to/city_cache.json",
    "lookup_timeout": 6
  },
  "gender": "female|male|other",
  "rules": {
    "year_boundary": "lichun",
    "month_rule": "solar_terms",
    "day_boundary": "00:00",
    "time_correction": "mean_solar_time",
    "require_dayun": false
  },
  "flows": {
    "datetime": "YYYY-MM-DDTHH:MM:SS",
    "timezone": "IANA/Timezone"
  },
  "mode": "strict"
}
```

### 必填字段
- `datetime`：本地日期时间字符串，不带 offset。
- `timezone`：IANA 时区，例如 `Asia/Shanghai`。

### 条件必填字段
- `location`：当 `time_correction` 为 `mean_solar_time` 或 `true_solar_time` 时必填。
- `gender`：当需要计算大运且 `require_dayun=true` 时必填。
- `flows.datetime`：只有请求流年/流月/流日时才需要。

### 可选字段与默认值
- `rules.year_boundary` 默认 `lichun`
- `rules.month_rule` 默认 `solar_terms`
- `rules.day_boundary` 默认 `00:00`
- `rules.time_correction` 默认 `mean_solar_time`
- `rules.require_dayun` 默认 `false`
- `mode` 默认 `strict`
- `location.lookup_provider` 默认 `nominatim`
- `location.lookup_path` 默认 `./cities.json`
- `location.cache_path` 默认 `./city_cache.json`
- `location.lookup_timeout` 默认 `6`

### 地点解析规则
- 优先使用 `longitude` 和 `latitude`。
- 只有 `name` 时，按 `lookup_mode` 解析：
  - `local`：仅查本地映射。
  - `online`：仅查在线地理编码。
  - `auto`：先本地，后在线。
- `amap` 和 `tencent` 需要 `lookup_key`，也可走环境变量 `BAZI_GEOCODE_KEY`。
- 可通过环境变量覆盖默认路径和服务：
  - `BAZI_CITY_MAP_PATH`
  - `BAZI_CITY_CACHE_PATH`
  - `BAZI_GEOCODE_PROVIDER`
  - `BAZI_GEOCODE_KEY`
  - `BAZI_GEOCODE_TIMEOUT`

### 固定计算规则
- 年界：`立春`
- 月界：按节气切月
- 日界：默认 `00:00`
- 时差修正：
  - `mean_solar_time`：只做经度修正
  - `true_solar_time`：经度修正 + 均时差
- `require_dayun`：默认 `false`
- 日柱基准：`1984-02-02` 为 `丙寅日`
- `strict` 模式下，缺少关键时间信息应直接报错

### 处理顺序
1. 解析 `datetime` 与 `timezone`
2. 根据 `rules` 决定是否做平太阳时或真太阳时修正
3. 计算年柱、月柱、日柱、时柱
4. 如请求大运，则根据性别与年干阴阳顺逆推算
5. 如请求流转信息，则计算 `flows`
6. 返回节气信息、元信息与置信度

### 成功输出
```json
{
  "ok": true,
  "bazi": {
    "year": { "tg": "...", "dz": "..." },
    "month": { "tg": "...", "dz": "..." },
    "day": { "tg": "...", "dz": "..." },
    "hour": { "tg": "...", "dz": "..." }
  },
  "dayun": {
    "direction": "forward|backward",
    "start_age_years": 0.0,
    "start_age_months": 0.0,
    "start_datetime": "YYYY-MM-DDTHH:MM:SS",
    "cycles": [
      {
        "index": 1,
        "tg": "...",
        "dz": "...",
        "gz": "...",
        "start_age_years": 0.0,
        "start_datetime": "YYYY-MM-DDTHH:MM:SS",
        "end_datetime": "YYYY-MM-DDTHH:MM:SS"
      }
    ]
  },
  "flows": {
    "datetime": "YYYY-MM-DDTHH:MM:SS",
    "year": { "tg": "...", "dz": "...", "gz": "..." },
    "month": { "tg": "...", "dz": "...", "gz": "..." },
    "day": { "tg": "...", "dz": "...", "gz": "..." }
  },
  "solar_terms": {
    "prev": { "name": "...", "datetime": "..." },
    "next": { "name": "...", "datetime": "..." }
  },
  "meta": {
    "timezone": "IANA/Timezone",
    "rules_used": {
      "year_boundary": "lichun",
      "month_rule": "solar_terms",
      "day_boundary": "00:00",
      "time_correction": "mean_solar_time",
      "require_dayun": false
    },
    "true_solar_time": {
      "method": "mean_solar_time|true_solar_time",
      "datetime": "...",
      "delta_minutes": 0.0,
      "equation_of_time_minutes": 0.0,
      "longitude_correction_minutes": 0.0
    },
    "location": {
      "name": "...",
      "longitude": 0.0,
      "latitude": 0.0
    },
    "confidence": "high|medium|low",
    "notes": []
  }
}
```

### 失败输出
```json
{
  "ok": false,
  "error": {
    "code": "INVALID_DATETIME|INVALID_TIMEZONE|INVALID_LOCATION|MISSING_DATE|MISSING_TIMEZONE|MISSING_LOCATION|MISSING_GENDER",
    "missing": ["date|time|timezone|location|gender"],
    "message": "Human-readable error for agent use"
  }
}
```

### 错误处理约定
- `MISSING_DATE`：缺少 `datetime`
- `INVALID_DATETIME`：日期时间格式不合法
- `MISSING_TIMEZONE`：缺少 `timezone`
- `INVALID_TIMEZONE`：时区无效
- `MISSING_LOCATION`：需要地点但无法解析
- `MISSING_GENDER`：请求大运时缺少性别

### 最低测试覆盖
- 立春前后跨年边界
- 节气切月边界
- `00:00` 日界
- 同一 UTC 在不同时区对应不同本地日
- 缺地点时的报错路径
- 请求大运但缺性别时的报错路径

### 调用入口
入口文件：`main.py`

```bash
echo '{"datetime":"1998-08-12T15:30:00","timezone":"Asia/Shanghai","location":{"name":"广州"},"rules":{"time_correction":"true_solar_time"}}' | python3 main.py
```

## 模式二：`analysis`

### 目标
基于盘面事实与本地知识库，生成可对话展示、语言跟随用户的分析报告。该模式不重新计算排盘，只消费已有 `chart` 数据。

### 必需输入
- `user_query`：用户当前问题，可为简体中文或其他语言。
- `chart`：由 `main.py` 产生的排盘 JSON。
- `knowledge`：解释和建议素材，来源于 `knowledge.md`。

### 语言适配规则
语言选择优先级如下：

1. 用户明确指定的输出语言
2. `user_query` 的主要语言
3. 简体中文（默认）

补充约束：
- 若用户使用非中文提问，可按该语言输出，但核心术语如“十神”“天干”“地支”“大运”“流年”可保留中文并加简短解释。
- 若用户要求双语输出，可先给主语言版本，再附简短中文术语对照。
- 若用户未要求翻译，不要为了“国际化”主动输出双语。

### 事实来源优先级
1. `chart`
2. `knowledge.md`
3. 用户问题中的补充条件

当知识库与盘面事实冲突时，以 `chart` 为准，并明确说明不确定性。

### 分析前检查
- 先识别用户问的是整体、事业、婚恋、健康、还是指定年份。
- 确认 `chart` 是否包含 `dayun`、`flows`、`meta.confidence` 等关键字段。
- 若缺少时辰、地点、性别或用户关注年份，要说明影响范围。

### 输出结构
输出使用 Markdown，并固定以下标题顺序：

1. `盘面摘要`
2. `本次问题结论`
3. `时间轴`（仅在用户询问年份或趋势时使用）
4. `建议`
5. `依据与补充`
6. `可信度与缺失信息`

### 每部分要求

#### 1. 盘面摘要
- 四柱按年、月、日、时顺序展示。
- 大运写当前正在走的运；无法确定时写“当前大运不确定”。
- 流年仅在 `chart.flows.year.gz` 可用时展示，否则写“流年未指定”。

#### 2. 本次问题结论
- 输出 3 到 6 条核心判断。
- 每条都尽量包含：现象、影响、建议。
- 结论必须围绕 `user_query`，不要泛泛而谈。

#### 3. 时间轴
- 用户问未来趋势、具体年份、近三年变化时再输出。
- 可按今年、明年、后年逐年列重点。
- 若无对应流年数据，提示用户补年份。

#### 4. 建议
- 输出 3 到 7 条动作化建议。
- 尽量区分“适合做什么”和“避免做什么”。
- 建议要现实、可执行，避免空泛玄学口号。

#### 5. 依据与补充
- 只引用与当前盘面相关的知识点。
- 引用来源应对应 `knowledge.md` 的条目或章节。
- 引用尽量短，不超过 25 个字，可适度改写。
- 这里只提供解释依据，不新增结论。

#### 6. 可信度与缺失信息
- 可信度优先使用 `chart.meta.confidence`。
- 明确指出缺失信息会影响哪些判断。
- 如需追问，只提最关键的一项或两项。

### 写作原则
- 输出语言与用户请求保持一致；无法判断时默认简体中文。
- 多用“倾向于”“可能”“建议”等词，避免绝对断言。
- 不做医学诊断、法律建议或恐吓式表达。
- 不堆砌术语，首次出现可顺手白话解释。

### 禁止事项
- 不凭空创造新的八字理论。
- 不脱离 `chart` 事实做判断。
- 不把知识库内容整段照搬。
- 不因为用户追问就伪造缺失的大运、流年或时柱。

### 参考文件
- 输出格式与分析任务要求：`prompt.md`
- 解释依据与建议素材：`knowledge.md`

## 模式切换与交接
- 排盘结果是分析输入，不是分析结论。
- 当同一请求同时包含出生信息和分析诉求时，先产出 `chart`，再基于 `chart` 输出分析。
- 分析阶段如果发现 `chart` 关键字段缺失，只说明限制，不在分析阶段偷偷补算。

## 快速判定
- 问“帮我排盘 / 算四柱 / 算大运” -> `chart`
- 问“帮我看看事业 / 婚恋 / 健康 / 今年运势”且已有盘面 -> `analysis`
- 问“这是我的生日，顺便分析一下” -> `chart` 然后 `analysis`
