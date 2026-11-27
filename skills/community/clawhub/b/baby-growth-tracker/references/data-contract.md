# 数据契约

## 文件位置与格式

默认数据文件：`~/.workbuddy/baby-growth/data.json`（UTF-8、缩进 2 空格的 JSON）。覆盖方式：命令加 `--data 路径`，或设环境变量 `BABY_GROWTH_DATA`。

顶层字段与 App 备份格式保持一致，便于必要时互通：

| 键 | 类型 | 说明 |
|---|---|---|
| `app` | string | Skill 数据为 `baby_growth_skill`；`export --for-app` 时写 `baby_nutrition` |
| `formatVersion` | int | 当前为 1 |
| `exportedAt` | string | 最后写入时间，ISO 8601 |
| `babies` | array | 宝宝档案 |
| `meals` | array | 每餐记录 |
| `growthRecords` | array | 身高体重测量 |
| `favoriteCombos` | array | 常用食物组合，Skill 不维护，恒为空 |
| `reminders` | array | 提醒配置，保留迁移来的值，Skill 不触发通知 |
| `settings` | array | 键值对，目前只用 `activeBabyId` |

## 表结构

### babies

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | int | 主键，从 1 递增 |
| `name` | string | 昵称 |
| `gender` | string | `male` / `female`，只用于选 WHO 曲线 |
| `birthDate` | string | ISO 日期时间，如 `2025-01-30T12:00:00.000` |
| `heightCm` / `weightKg` | number | 最近一次测量值，录入成长记录时同步更新 |
| `allergies` | string | 过敏食物，逗号/顿号/空格分隔；只生成提醒文案 |
| `sizeStatus` | string | `small` / `normal` / `large`，影响推荐量 |
| `sizeStatusManual` | 0/1 | 为 1 时 `add-growth` 不自动覆盖 `sizeStatus` |
| `ironRisk` | 0/1 | 为 1 时铁的推荐量上调 20% |

月龄算法（与 App 一致）：`(目标年-出生年)*12 + 目标月-出生月`，若目标日的「日」小于出生日的「日」再减 1，负数归 0。

### meals

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | int | 主键 |
| `babyId` | int | 按宝宝隔离数据 |
| `mealType` | string | `breakfast` / `lunch` / `dinner` / `snack` |
| `date` | string | ISO 日期时间；查询按前 10 位日期匹配 |
| `foodsJson` | string | 内嵌 JSON 数组，元素为 `{"foodId":"rice","grams":100.0}` |
| `photoPath` | null | Skill 不存照片 |
| `note` | string | 备注 |
| `vitaminASupplement` / `vitaminCSupplement` | number | 额外补充剂，直接计入当日摄入 |

`foodId` 必须存在于 `assets/food_table.json`；未知 id 在计算时被跳过（不报错，避免脏数据导致崩溃）。

### growthRecords

`id`、`babyId`、`date`、`heightCm`、`weightKg`、`note`。按日期升序用于展示。

### reminders / settings

`reminders` 元素：`mealType`、`enabled`(0/1)、`hour`、`minute`。`settings` 元素：`{"key":"activeBabyId","value":"1"}`。

## ID 与写入规则

- 所有 `id` 用「当前最大值 + 1」生成，删除后不复用。
- 写入统一走 `save_doc()`：先把现有文件复制为同名 `.json.bak`，再写临时文件后原子替换。任何手工编辑都会绕过这层保护。
- 日期参数统一 `YYYY-MM-DD`；不传 `--date` 时取当天。指定日期的记录时间固定 12:00，今天的记录用当前时刻。

## 迁移与合并

`import-backup --file X` 从 App 导出的 JSON 备份迁移：

1. 校验顶层为对象且 `babies` 是数组；`app` 标识不是 `baby_nutrition` / `baby_growth_skill` 时只提示、不阻断。
2. 补齐缺失的 5 个数组键，`app` 统一改为 `baby_growth_skill`。
3. 目标文件不存在时直接写入；存在时默认按 `id` 合并（只追加不重复的记录，保留现有数据），加 `--replace` 才整库覆盖。
4. 无论哪种模式，写入前都生成 `.bak`。

`export` 输出 Skill 备份；`export --for-app` 把 `app` 改成 `baby_nutrition`，可被原 App 的「数据管理 → 导入」读取。注意该导入是整表清空重写，**不要在两边同时录入后直接覆盖**，否则会丢掉手机上新增的记录。

## 不做的事

- 不读写真机数据库、不调用 adb、不依赖 Flutter SDK。
- 不保存照片、不发送手机通知、不联网。
- 不自动合并「同一天同一餐次」的重复录入；`add-meal` 每次都新建一条，需要去重时用 `meals` 查后 `del-meal`。
