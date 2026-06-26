---
name: energy-tracker
description: 每日能量状态追踪与多日趋势分析；当智能体需要主动采集用户当日能量状态时使用
dependency:
  python:
    - matplotlib>=3.5.0
---

# 能量状态追踪器 / Energy Tracker

## 任务目标 / Objective
- **本 Skill 用于**：智能体主动采集用户每日能量状态并保存数据，同时基于多日数据识别心理模式
- **This Skill is for**: AI agent proactively collects daily energy status from users and saves data, while identifying psychological patterns based on multi-day data
- **能力包含**：每日单选题采集、单天心理状态解读、多日趋势模式识别、可视化趋势图表、专业建议生成、紧急干预提醒
- **Capabilities**: Daily single-question collection, single-day psychological status interpretation, multi-day trend pattern recognition, visual trend chart generation, professional advice generation, emergency intervention alerts
- **触发条件**：智能体需要记录用户当天的能量状态（每日一次主动询问）
- **Trigger condition**: AI agent needs to record user's daily energy status (proactive inquiry once per day)

## 前置准备 / Prerequisites
- **依赖说明**：matplotlib（用于生成趋势图表）
- **Dependencies**: matplotlib (for generating trend charts)

## 操作步骤 / Procedure

### 标准流程（智能体主动询问） / Standard Flow (Agent Proactive Inquiry)

#### 1. 主动展示问题 / Display Question
- **中文**：提问"我今天是否有足够的能量，去应对那些必须要做的事？" 展示选项：A-"是"  B-"勉强可以"  C-"不，完全不想动"
- **English**: Ask "Do I have enough energy today to handle the things I must do?" Show options: A-"Yes"  B-"Barely"  C-"No, don't want to move at all"

#### 2. 采集回答 / Collect Response
- **中文**：记录用户的选择（A/B/C），记录当前日期（YYYY-MM-DD格式）
- **English**: Record user's choice (A/B/C), record current date (YYYY-MM-DD format)

#### 3. 单天解读 / Single-day Interpretation
- **中文**：根据用户选择，提供对应的单天结果解读和建议：
  - A-"是"：心理平衡期，保持规律作息，【智能体根据用户记忆生成个性化小奖励内容】
  - B-"勉强可以"：心理代偿期，精简清单，推掉非必要社交，早睡一小时
  - C-"不，完全不想动"：心理耗竭期，允许停顿，只做维持生存的最低限度工作
- **English**: Provide corresponding single-day interpretation and advice based on user's choice:
  - A-"Yes": Psychological balance period, maintain regular sleep schedule, [agent generates personalized reward content based on user memory]
  - B-"Barely": Psychological compensation period, simplify to-do list, decline non-essential social activities, sleep one hour earlier
  - C-"No, don't want to move at all": Psychological burnout period, allow pause, only do minimum work to maintain survival

#### 4. 数据持久化 / Data Persistence
- **中文**：按照参考文档格式，将今日记录追加到 `./energy_data.json` 文件中，文件不存在时首次创建
- **English**: Append today's record to `./energy_data.json` file according to reference document format, create file if it doesn't exist

#### 5. 生成趋势图表 / Generate Trend Chart
- **中文**：每次记录后，调用 `scripts/generate_chart.py` 生成可视化趋势图。命令：`python3 /workspace/projects/energy-tracker/scripts/generate_chart.py ./energy_data.json ./energy_chart.png`。在回复中引用生成的图表展示趋势变化
- **English**: After each recording, call `scripts/generate_chart.py` to generate visual trend chart. Command: `python3 /workspace/projects/energy-tracker/scripts/generate_chart.py ./energy_data.json ./energy_chart.png`. Reference the generated chart in response to show trend changes

#### 6. 多日分析与干预检测（可选） / Multi-day Analysis and Intervention Detection (Optional)
- **中文**：当数据积累超过7天时，自动调用脚本进行趋势分析。执行 `scripts/analyze_trends.py` 处理 `./energy_data.json`。检查脚本返回的 `needs_intervention` 字段：
  - 若 `needs_intervention` 为 `true` 且 `consecutive_c >= 3`：
    - 判断用户地区：中国大陆推送"12356"全国统一心理援助热线
    - 其他地区：智能体自行搜索当地心理援助热线并推送
  - 结合脚本返回的模式和建议，用自然语言为用户解释趋势含义
  - 给出具体的行动建议
- **English**: When accumulated data exceeds 7 days, automatically call script for trend analysis. Execute `scripts/analyze_trends.py` to process `./energy_data.json`. Check the `needs_intervention` field returned by script:
  - If `needs_intervention` is `true` and `consecutive_c >= 3`:
    - Determine user region: Push "12356" national psychological assistance hotline for mainland China
    - Other regions: Agent searches for local psychological assistance hotline and pushes it
  - Combine pattern and advice returned by script to explain trend meaning to user in natural language
  - Provide specific action suggestions

## 资源索引 / Resource Index
- **必要脚本1 / Essential Script 1**: [scripts/analyze_trends.py](scripts/analyze_trends.py)（多日趋势分析与干预检测，输入：energy_data.json，输出：分析报告 / Multi-day trend analysis and intervention detection, input: energy_data.json, output: analysis report）
- **必要脚本2 / Essential Script 2**: [scripts/generate_chart.py](scripts/generate_chart.py)（可视化趋势图表生成，输入：energy_data.json、输出路径，输出：PNG图片 / Visual trend chart generation, input: energy_data.json, output path, output: PNG image）
- **领域参考 / Domain Reference**: [references/data-format.md](references/data-format.md)（数据文件格式定义与示例 / Data file format definition and examples）
- **示例数据 / Sample Data**: [references/sample-data.json](references/sample-data.json)（7天示例数据，用于格式参考 / 7-day sample data for format reference）

## 注意事项 / Notes
- **中文**：智能体每日主动询问一次，避免重复录入。多日分析至少需要7天数据才能提供有意义的趋势判断。每次记录后都生成趋势图表，即使用户数据不足7天也可展示。对于持续低能量状态，建议用户关注专业干预建议。连续3天及以上选择C时，必须推送心理援助热线信息。个性化奖励内容应基于用户记忆生成具体化建议。所有用户数据文件使用相对路径 `./`，Skill资源使用绝对路径
- **English**: Agent proactively asks once per day, avoid duplicate entries. Multi-day analysis requires at least 7 days of data to provide meaningful trend judgments. Generate trend chart after each recording, even if user data is less than 7 days. For sustained low energy status, suggest user pay attention to professional intervention advice. When C is selected for 3 or more consecutive days, must push psychological assistance hotline information. Personalized reward content should generate specific suggestions based on user memory. All user data files use relative path `./`, Skill resources use absolute paths

## 使用示例 / Usage Examples

### 标准场景 / Standard Scenario
- **中文**：
  - **智能体**：主动提问"我今天是否有足够的能量，去应对那些必须要做的事？A-'是'  B-'勉强可以'  C-'不，完全不想动'"
  - **用户**："选A"
  - **智能体**：提供单天解读"你处于心理平衡期。保持规律作息，【根据记忆生成：比如喝一杯喜欢的茶/看一集喜欢的剧/散步15分钟】作为小奖励"，将记录保存到 `./energy_data.json`
  - **智能体**：调用图表生成脚本，展示"能量状态趋势图"（图片）
  - **智能体**（当数据超过7天）：调用脚本分析数据，补充说明"你的状态反复波动，代表环境压力过载..."并提供建议
- **English**:
  - **Agent**: Proactively asks "Do I have enough energy today to handle the things I must do? A-'Yes'  B-'Barely'  C-'No, don't want to move at all'"
  - **User**: "Choose A"
  - **Agent**: Provides single-day interpretation "You are in psychological balance period. Maintain regular sleep schedule, [generate based on memory: e.g., drink a cup of favorite tea / watch an episode of favorite show / take a 15-minute walk] as a small reward", saves record to `./energy_data.json`
  - **Agent**: Calls chart generation script, displays "Energy Status Trend Chart" (image)
  - **Agent** (when data exceeds 7 days): Calls script to analyze data, supplements with explanation "Your status fluctuates repeatedly, representing environmental pressure overload..." and provides suggestions

### 紧急干预场景 / Emergency Intervention Scenario
- **中文**：
  - **智能体**：调用分析脚本，检测到 `needs_intervention: true` 且 `consecutive_c: 3`
  - **智能体**：推送紧急提醒"检测到您连续3天处于心理耗竭期，这是预警信号。请拨打12356全国统一心理援助热线（如在其他地区，请查询当地心理援助热线），及时寻求专业支持。"
- **English**:
  - **Agent**: Calls analysis script, detects `needs_intervention: true` and `consecutive_c: 3`
  - **Agent**: Pushes emergency alert "Detected that you have been in psychological burnout period for 3 consecutive days, this is an early warning signal. Please call 12356 national psychological assistance hotline (if in other regions, please query local psychological assistance hotline), seek professional support in time."
