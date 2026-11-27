---
name: baby-growth-tracker
description: 维护 1-3 岁宝宝的喂养与成长数据：记录每餐食物与克重、身高体重测量，计算当日营养摄入与全天推荐量达成率，生成营养建议、WHO 生长曲线判型和 7/30 天报告，并导出 JSON 备份。This skill should be used when 用户要记一餐、查今天营养够不够、加成长记录、看生长曲线、生成宝宝营养报告、维护宝宝档案或迁移备份，尤其涉及宝宝成长信息、辅食记录、营养缺口、身高体重等中文请求时。
agent_created: true
compatibility: Requires Python 3.8+ and a host with filesystem access and code execution; no network or third-party packages.
---

# 宝宝成长数据维护

## 用途

把原本 Flutter App 里的数据层与计算引擎独立成本 Skill：不依赖 App、不联网、不需要手机、不需要 adb。所有数据落在一个本地 JSON 文件，所有计算由 `scripts/baby.py` 完成，AI 通过命令行直接维护宝宝成长信息。

## 何时使用

- 「记一下今天中午吃了米饭 80g 和鸡蛋」「加了维C 补充剂 20mg」
- 「今天营养够吗」「缺铁吗」「蛋白质多少」「维A 都从哪些食物来的」
- 「量了身高 81.5、体重 10.4」「看看生长曲线正不正常」
- 「出一份近 7 天 / 30 天报告」「导出备份」「新建一个宝宝档案 / 切到另一个宝宝」

## 数据位置

默认 `~/.workbuddy/baby-growth/data.json`。用 `--data 路径` 或环境变量 `BABY_GROWTH_DATA` 覆盖。每次写入前自动把旧文件复制为 `.json.bak`。**禁止直接手改 JSON，一律走 CLI**，否则 ID、日期格式、`.bak` 保护都会失效。

分发包只含能力，**不含任何个人数据**；新用户拿到的是空库，必须按下方「首次使用」初始化。安装与分发步骤见 `INSTALL.md`。

下文命令均以本 Skill 目录为基准执行：`python scripts/baby.py <子命令> [参数]`。

## 工作流

### 0. 首次使用

先执行 `status` 确认数据文件状态。若提示数据文件不存在，二选一：

```
python scripts/baby.py init                       # 建空库，再用 add-baby 建档
python scripts/baby.py import-backup --file "备份.json" --replace   # 或导入已有备份
python scripts/baby.py add-baby --name 宝宝 --birth 2025-01-30 --height 80 --weight 10
```

备份须为含 `babies` 数组的 JSON，兼容原 App 导出的备份格式。默认按 id 合并、不覆盖已有记录；`--replace` 才整库替换（旧数据仍会先备份）。

### 1. 记录前先确认

1. 执行 `status` 看当前宝宝。多宝宝时执行 `babies` 核对，必要时 `switch --id N` 切换。
2. 用 `foods --search 关键词` 或 `foods --category 分类` 查到准确食物 id，**不要凭名称猜 id**。
3. 克重单位是克（g），营养值按每 100g 折算；`--food ID:克重` 可重复传多次。

### 2. 记录一餐

```
python scripts/baby.py add-meal --type lunch --food rice:100 --food egg:50 --vc 20 --note "胃口不错"
```

- `--type`：`breakfast` / `lunch` / `dinner` / `snack`
- `--date YYYY-MM-DD`：默认今天；`--va` 维生素A μg、`--vc` 维生素C mg 为额外补充剂
- 至少要有一种食物或补充剂；未知食物 id、克重小于等于 0 会被拒绝
- 反悔用 `del-meal --id N`；查看用 `meals --date YYYY-MM-DD`

### 3. 查询营养与建议

```
python scripts/baby.py intake
python scripts/baby.py advice
python scripts/baby.py sources --nutrient iron
```

`intake` 输出 6 项摄入 / 目标 / 达成率，`advice` 输出偏低、达标、偏高的建议文案，`sources` 只统计**今日实际吃过的食物**（含补充剂单列）。默认查今天，可用 `--date YYYY-MM-DD` 指定日期。向用户转述时必须说明：**目标值是全天总量，不是累计到当前时刻**；60%~130% 都算达标。

### 4. 记录成长数据

```
python scripts/baby.py add-growth --height 81.5 --weight 10.4
python scripts/baby.py growth
```

录入后自动按 WHO 0-36 月 P3/P97 判型，并在未手动锁定个头时回写档案的 `sizeStatus`、`heightCm`、`weightKg`。`growth` 显示月龄、参考区间、判型与最近 10 次测量。

### 5. 报告与备份

```
python scripts/baby.py report --days 7 --out "报告.md"
python scripts/baby.py export --out "备份.json"
```

`report` 输出 Markdown（日均达成率表 + 每日热量明细），可直接转述或写成文件。`export --for-app` 才输出成原 App 可导入的格式；本 Skill 正常运作**不需要**该选项。

## 命令速查

| 命令 | 作用 |
|---|---|
| `status` / `babies` / `switch --id N` | 数据概览 / 档案列表 / 切换当前宝宝 |
| `add-baby --name --birth --height --weight` | 建档（可选 `--gender` `--allergies` `--iron-risk` `--size-status` `--manual-size`） |
| `foods [--category X] [--search X]` | 查食材表与 id |
| `add-meal` / `meals` / `del-meal --id N` | 记一餐 / 查某日餐次 / 删餐次 |
| `intake` / `advice` / `sources --nutrient X` | 摄入对比 / 建议 / 今日食物来源 |
| `add-growth` / `growth` | 记录测量 / WHO 判型 |
| `report --days 7|30` / `export` | 报告 / 备份 |
| `init` / `import-backup --file X` | 建空库 / 迁移备份 |

完整子命令参数用 `python scripts/baby.py <子命令> --help` 查看。

## 规则要点

- 6 项营养素：热量 kcal、蛋白质 g、铁 mg、钙 mg、维生素A μg、维生素C mg。
- 推荐量按 24 月龄分两档，再按个头、体重、缺铁风险微调；**过敏只产生提醒文案，不改数值；性别只影响 WHO 曲线，不影响推荐量**。
- 达成率小于 0.6 提示补充，大于 1.3 提示减量，中间达标；超过 100% 时显示超出百分比。
- WHO 数据仅 P3/P97，适用于足月儿 0-36 月龄；身高曲线在 24 月处约有 0.7cm 断层属正常。

精确系数、文案、字段与合并策略见 `references/nutrition-rules.md` 与 `references/data-contract.md`。

## 约束与安全

1. **纯本地**：不联网、不上传、不调用任何模型或后端处理儿童健康数据。
2. **写入保护**：每次写操作自动生成 `.bak`；执行 `import-backup --replace` 或 `del-meal` 前先向用户说明影响，不要在未确认时整库覆盖。
3. **不维护的东西**：照片（`photoPath` 恒为 null）、常用组合、手机本地通知。需要三餐提醒时改用 WorkBuddy 的定时自动化任务，不要在 Skill 里假装已设置通知。
4. **健康合规**：所有建议是内置规则生成，转述时保留免责声明，避免「诊断 / 治疗 / 必须补充」等医疗化措辞。
5. **数值口径**：食物营养值为每 100g 近似值；报告「有记录天数」只按热量/蛋白质/铁/钙判断，与纯补充剂记录无关。

## 资源

| 文件 | 内容 |
|---|---|
| `INSTALL.md` | 面向接收方的安装（zip / 项目级 / Git clone）、初始化、验证与隐私说明（分享时一起给） |
| `UNIVERSAL.md` | 跨 Agent / 跨模型接入：各宿主技能目录、AGENTS.md 片段、工具化包装、兼容性注意 |
| `scripts/baby.py` | 数据 CRUD、营养计算、WHO 判型、报告生成（唯一执行入口） |
| `references/data-contract.md` | JSON 数据契约、字段单位、ID 与日期规则、迁移合并策略 |
| `references/nutrition-rules.md` | 推荐量分档、定制系数、阈值文案、WHO 标准、免责与数据出处 |
| `assets/food_table.json` | 30 种常见食材每 100g 营养值 |
| `assets/growth_standards.json` | WHO 0-36 月男女身高体重 P3/P97，8 组各 37 个点 |
