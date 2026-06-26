# Notion 集成方案（Notion Integration）

> 适用版本：family-cultivation-coach v1.4+
> 定位：飞书方案的低门槛替代，适合没有飞书环境的普通用户
> 前提条件：有 Notion 账号，获取 API Key

---

## 一、与飞书方案的核心差异

| 能力 | 飞书方案 | Notion 方案 |
|------|---------|-----------|
| 数据存储 | 多维表格 | Notion Database |
| 初始化成本 | 高（6步，有卡点） | **低（3步，5分钟）** |
| 主动推送速记卡 | ✅ 机器人原生推送 | ❌ 无推送，需用户主动触发 |
| 日报推送 | ✅ 飞书消息 | ❌ 写入 Notion，需主动查看 |
| 手动编辑体验 | 多维表格 | **Notion 界面（更友好）** |
| 跨设备访问 | ✅ | ✅ |
| 家人共享 | ✅ | ✅ 共享页面即可 |
| 数据隐私 | 字节跳动服务器 | Notion 服务器 |
| 国内访问稳定性 | 稳定 | 偶尔需要代理 |

**Notion 方案适合**：没有飞书环境、不需要主动推送提醒、希望最快上手的用户。

**飞书方案适合**：已有飞书机器人、需要定时速记卡推送、希望完全自动化的用户。

---

## 二、初始化步骤（用户操作，约5分钟）

### 步骤1：创建 Notion Integration（2分钟）

1. 打开 https://www.notion.so/my-integrations
2. 点击「New integration」
3. 填写名称：`family-cultivation-coach`
4. 关联到你的 Workspace
5. 点击「Submit」
6. 复制页面上的 **Internal Integration Token**（格式：`secret_xxxxxxxx`）

### 步骤2：让 Skill 自动建库（Skill 执行）

把以下指令发给 Skill：

```
请使用 Notion API 在我的 Notion 中初始化家庭养育系统数据库。
Notion API Key：[粘贴你的 Token]
请创建所有必要的数据库并返回各数据库的 ID。
```

Skill 会自动创建 6 个数据库并返回 ID。

### 步骤3：共享数据库给 Integration（1分钟）

Skill 建完库后，每个数据库页面右上角点「···」→「Add connections」→ 选择 `family-cultivation-coach`。
（共享后 Skill 才有读写权限）

完成，可以开始使用。

---

## 三、数据库结构

共 6 个 Notion Database，结构与飞书方案对应。

---

### DB1：孩子画像（child_profile）

| 字段名 | 字段类型 | 说明 |
|--------|---------|------|
| 昵称 | Title | 主键 |
| 年龄 | Number | 岁 |
| 上学阶段 | Select | 幼儿园小班/中班/大班/小学1年级/… |
| 性格标签 | Multi-select | 活跃外向/安静内向/情绪敏感/随和/好奇心强/… |
| 兴趣 | Rich Text | |
| 优势 | Rich Text | |
| 短板描述 | Rich Text | 行为描述，不贴标签 |
| 培养重点 | Rich Text | 当前最重要的1-3个方向 |
| 最后更新 | Date | |
| 备注 | Rich Text | |

---

### DB2：课表版本（schedules）

| 字段名 | 字段类型 | 说明 |
|--------|---------|------|
| 版本号 | Title | v1.0 / v1.1 / … |
| 孩子昵称 | Relation | 关联孩子画像 |
| 生效日期 | Date | |
| 状态 | Select | 当前执行中 / 历史版本 |
| 课表JSON | Rich Text | 结构化数据 |
| 课表摘要 | Rich Text | 人类可读的简短描述 |
| 变更说明 | Rich Text | |
| 生成来源 | Select | Skill生成 / 手动编辑 |

---

### DB3：每日记录（daily_logs）

| 字段名 | 字段类型 | 说明 |
|--------|---------|------|
| 日期 | Title（日期格式） | 如 2024-09-03 |
| 孩子昵称 | Relation | |
| 整体状态 | Select | 很好 / 正常 / 有点难 / 很难 |
| 执行情况 | Multi-select | 英语输入/英语输出/数学/认字阅读/钢琴练习/跆拳道/轮滑/科学课/睡前故事/晨间例程 |
| 跳过的任务 | Rich Text | |
| 亮点时刻 | Rich Text | |
| 困难点 | Rich Text | |
| 孩子情绪 | Select | 稳定 / 有波动 / 情绪很差 |
| 家长情绪 | Select | 稳定 / 有点累 / 很疲惫 |
| 自由记录 | Rich Text | |
| 记录来源 | Select | Skill写入 / 手动录入 |

---

### DB4：每日日报（daily_reports）

| 字段名 | 字段类型 | 说明 |
|--------|---------|------|
| 日期 | Title（日期格式） | |
| 孩子昵称 | Relation | |
| 今日进展 | Rich Text | |
| 明日安排 | Rich Text | |
| 当前问题 | Rich Text | |
| 思考与建议 | Rich Text | |
| 状态 | Select | 已生成 / 已推送 |

---

### DB5：每周复盘（weekly_reviews）

| 字段名 | 字段类型 | 说明 |
|--------|---------|------|
| 周次 | Title | 如 2024-W37 |
| 孩子昵称 | Relation | |
| 整体状态评分 | Number | 1-5 |
| 执行率 | Number | 百分比 |
| 最顺的安排 | Rich Text | |
| 最难执行的安排 | Rich Text | |
| 孩子本周变化 | Rich Text | |
| 家长自我观察 | Rich Text | |
| 下周只抓1件事 | Rich Text | |
| 是否需要调整课表 | Select | 不需要 / 小调整 / 需要重新生成 |
| Skill分析摘要 | Rich Text | |

---

### DB6：累积洞察（insights）

| 字段名 | 字段类型 | 说明 |
|--------|---------|------|
| 生成日期 | Title（日期格式） | |
| 孩子昵称 | Relation | |
| 洞察类型 | Select | 执行规律/情绪规律/学习进展/家长状态/风险预警 |
| 洞察内容 | Rich Text | |
| 数据依据 | Rich Text | |
| 建议行动 | Rich Text | |
| 状态 | Select | 新发现 / 持续观察 / 已处理 |

---

### DB7：临时活动（temp_events）

> 独立存储未来临时活动，与每日记录完全分离。
> 日报、周复盘、速记卡生成时均来此库查询。

| 字段名 | 字段类型 | 说明 |
|--------|---------|------|
| 活动名称 | Title | 如"恐龙展览" |
| 孩子昵称 | Relation | |
| 活动日期 | Date | 核心查询字段 |
| 活动时间 | Rich Text | 如 15:00-17:00 |
| 影响的常规任务 | Rich Text | 如"跆拳道取消"，可为空 |
| 需要准备的事项 | Rich Text | 如"带水、换衣服"，可为空 |
| 提前提醒天数 | Number | 默认1；有准备事项自动设2 |
| 状态 | Select | 待发生 / 已完成 / 已取消 |

---

## 四、Notion API 调用路径

```
# 查询数据库记录
POST https://api.notion.com/v1/databases/{database_id}/query

# 创建新记录
POST https://api.notion.com/v1/pages

# 更新已有记录
PATCH https://api.notion.com/v1/pages/{page_id}

# 请求头（所有请求均需）
Authorization: Bearer {api_key}
Notion-Version: 2022-06-28
Content-Type: application/json
```

---

## 五、Skill 交互规则（Notion 模式）

### 每次对话开始时
1. 读取孩子画像库 → 获取基础信息
2. 查询课表版本库（状态=当前执行中）→ 获取现行课表
3. 如涉及分析 → 查询最近 14 天每日记录
4. 如涉及复盘 → 查询本周记录 + 最近 2 条累积洞察

### 记录触发方式（Notion 模式无主动推送）

| 用户操作 | Skill 动作 |
|---------|-----------|
| 发送"记录今天：…" | 解析内容 → 写入每日记录库 → 生成日报写入日报库 |
| 发送速记格式（数字+字母） | 解析 → 写入每日记录 → 生成日报 |
| 提到未来日期+活动 | 自动识别 → **写入 temp_events 库** → 后续日报/复盘自动查询插入预告 |
| 发送"做本周复盘" | 完整性检查 → 生成复盘 → 查询 temp_events 下周活动 → 写入复盘库 |
| 发送"最近…怎么样" | 查询记录 → 分析 → 直接回复 |
| 生成或更新课表 | 旧版本改为历史版本 → 写入新版本 |

**临时活动识别规则与飞书模式完全一致**，见 `rules/feishu_integration.md` 第二节 2.4。
**日报/复盘/速记卡查询 temp_events 的逻辑与飞书模式完全一致**，见 `rules/feishu_integration.md` 第四、五节。

### Notion 模式的速记格式

无主动推送，用户主动发以下格式即触发记录。**选项编号与飞书速记卡保持一致**，从当前课表动态生成，规则相同（见 `rules/feishu_integration.md` 第三节）。

用户发送时可以使用：

```
# 速记格式（推荐）
今天：[编号组合] [状态字母] [一句话（可选）]

# 示例
今天：1 3 B 睡前故事Sunny自己选了两本
今天：全完成 A 今天超级顺
今天：就睡前故事 D 情绪很差什么都不配合

# 自然语言也可以
记录今天：英语和睡前故事完成了，钢琴没练，情绪正常
```

用户不确定编号时，可以直接用任务名称，Skill 自动匹配：

```
今天：英语输入 睡前故事 B 今天主动说了一句英文
```

---

## 六、给用户的推送替代方案

Notion 没有主动推送能力，以下是替代方式（由用户自选）：

| 方式 | 成本 | 效果 |
|------|------|------|
| 手机设置每日提醒（20:00） | 零，30秒设置 | 提醒打开对话记录，不自动推送内容 |
| Notion 日历视图 | 零 | 可视化查看每日记录状态，缺失天一目了然 |
| 和飞书/微信机器人结合 | 中 | 机器人提醒 → 用户去 Notion 查看/记录 |

**推荐**：手机日历设置一个每天 20:00 的重复提醒，提醒文字写"记录 Sunny 今天"，点开后直接发给 Skill。成本为零，效果够用。

---

## 七、配置文件格式

Skill 存档 Notion 配置时使用以下格式：

```
存储后端：notion
API Key：secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
数据库 ID：
  孩子画像：xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  课表版本：xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  每日记录：xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  每日日报：xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  每周复盘：xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  累积洞察：xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  临时活动：xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
