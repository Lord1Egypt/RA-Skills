# 配置指南

> 如何配置人格修行系统

---

## 配置文件位置

用户配置文件应存放在 Obsidian vault 或指定工作目录：

```
your-vault/
├── daily-cultivation-config.yaml   # 主配置文件
├── virtue-status.md                 # 美德状态文件
├── quotes/                          # 语录库目录
│   ├── 段永平.md
│   ├── 富兰克林.md
│   └── ...
└── 每晚复盘/                       # 复盘存档（自动生成）
    ├── 2026-04-01-晚复盘.md
    └── ...
```

**建议**：将 `your-vault` 设为 Obsidian vault，方便搜索和分析。

---

## 配置项说明

### 基础配置

```yaml
# daily-cultivation-config.yaml

# 系统名称（可选，用于个性化）
system_name: "人格修行系统"

# 用户称呼
user_greeting: "朋友"  # 晨语/复盘中的称呼

# 时区
timezone: "Asia/Shanghai"

# Obsidian vault 路径（用于自动存档）
obsidian_vault: "D:/obisian/master"
```

---

### 晨间设置

```yaml
morning:
  enabled: true
  time: "08:00"          # 发送时间

  # 大师智慧配置
  wisdom:
    enabled: true
    masters:              # 最多6位
      - name: 段永平
        quotes_file: quotes/段永平.md
      - name: 富兰克林
        quotes_file: quotes/富兰克林.md
      - name: 万维钢
        quotes_file: quotes/万维钢.md
      - name: 冯仑
        quotes_file: quotes/冯仑.md
      - name: 乔布斯
        quotes_file: quotes/乔布斯.md
      - name: 吴军
        quotes_file: quotes/吴军.md
    daily_count: 6        # 每天显示几位大师的语录

  # 美德提醒
  virtue:
    enabled: true
    system: franklin      # franklin | custom
    status_file: virtue-status.md
```

---

### 美德体系配置

#### 方式一：使用富兰克林13美德（默认）

```yaml
morning:
  virtue:
    enabled: true
    system: franklin    # 使用富兰克林13美德
    status_file: virtue-status.md
```

#### 方式二：自定义美德体系

```yaml
morning:
  virtue:
    enabled: true
    system: custom     # 自定义美德
    virtues:           # 自定义美德列表
      - name: 专注
        definition: 全力投入当下之事，不分心
      - name: 勇气
        definition: 面对恐惧依然行动
      - name: 诚实
        definition: 对自己诚实，也对他人诚实
      - name: 感恩
        definition: 每天记录三件值得感恩的事
      # ... 可自由添加，建议 4-13 个
    status_file: virtue-status.md
```

#### 美德数量建议

| 数量 | 循环周期 | 适用场景 |
|:---:|:---|:---|
| 4 个 | 1个月 | 快速迭代，适合新手 |
| 6 个 | 1.5个月 | 平衡节奏 |
| 12 个 | 3个月 | 深度修炼 |
| 13 个 | 3个月 | 富兰克林经典 |

#### 美德设计建议

1. **选择真正想培养的品质** — 不要照搬，问自己想成为什么样的人
2. **定义清晰可执行** — 每个人对同一美德的定义不同
3. **数量不要太多** — 专注才能深入，4-6个也可以

---

### 晚间设置

```yaml
evening:
  enabled: true
  time: "22:00"           # 发送时间

  # 自我复盘
  reflection:
    enabled: true
    template: templates/evening.md

  # 美德践行
  virtue_check:
    enabled: true

  # 自动存档
  auto_save:
    enabled: true
    save_path: "每晚复盘"              # 相对于 vault 根目录
    filename_format: "{YYYY}-{MM}-{DD}-晚复盘.md"
```

---

### 晚复盘自动存档

**功能**：用户完成晚复盘后，自动保存到本地

**配置**：

```yaml
evening:
  auto_save:
    enabled: true
    save_path: "每晚复盘"
    filename_format: "{YYYY}-{MM}-{DD}-晚复盘.md"
```

**存档效果**：

```
your-vault/
└── 每晚复盘/
    ├── 2026-04-01-晚复盘.md
    ├── 2026-04-02-晚复盘.md
    ├── 2026-04-03-晚复盘.md
    └── ...
```

**结合 Obsidian 使用**：

1. 将 vault 设置为 Obsidian vault
2. 每日复盘自动保存
3. 可在 Obsidian 中：
   - 搜索历史复盘（Ctrl/Cmd + P）
   - 建立 `#复盘` 标签
   - 使用 Dataview 插件分析美德践行趋势
   - 追踪个人成长曲线

**示例：Dataview 查询**

```dataview
TABLE
  file.ctime as "日期",
  choice(contains(file.content, "美德打分：8"), "优秀", "良好") as "表现"
FROM "每晚复盘"
SORT file.ctime DESC
LIMIT 7
```

**形成修炼库的价值**：

| 功能 | 说明 |
|:---|:---|
| 回顾 | 翻看过去，发现成长 |
| 搜索 | 快速找到特定内容 |
| 分析 | 用插件统计美德得分趋势 |
| 分享 | 可导出分享给导师/朋友 |
| 传承 | 长期积累，成为人生财富 |

---

### 发送渠道

```yaml
channels:
  # 飞书
  - type: feishu
    target: "user:ou_xxx"    # 用户私聊
    # 或 group: "chat_xxx"   # 群聊

  # Discord（可选）
  - type: discord
    channel_id: "xxx"

  # Telegram（可选）
  - type: telegram
    chat_id: "xxx"
```

---

## 语录库格式

每位大师的语录文件格式：

```markdown
# [大师名]语录

> 来源说明

## 语录列表

1. **第一条语录内容。**（来源）
2. **第二条语录内容。**（来源）
...

## 已发送记录

| 日期 | 语录编号 |
|:---|:---:|
| 2026-04-14 | 1, 5, 8 |
```

---

## 美德状态文件

`virtue-status.md` 格式：

```markdown
# 美德状态

当前周：第10周
当前美德：整洁
美德定义：身体、衣服、住所保持清洁
时间范围：2026-04-13 至 2026-04-19

---

## 轮转历史

| 周次 | 美德 | 时间范围 |
|:---:|:---|:---|
| 1 | 节制 | 2026-01-06 至 2026-01-12 |
| ... | ... | ... |
```

---

## 定时任务配置

### OpenClaw Cron 格式

在 OpenClaw 配置中添加：

```yaml
cron:
  - name: morning-wisdom
    schedule: "0 8 * * *"      # 每天 08:00
    action: "发送晨语"
    skill: daily-cultivation

  - name: evening-reflection
    schedule: "0 22 * * *"     # 每天 22:00
    action: "发送晚复盘"
    skill: daily-cultivation
```

---

## 初始化流程

首次使用时，Agent 会引导用户：

1. **确认配置路径**
   - "你的配置文件想放在哪里？"
   - 建议：Obsidian vault

2. **选择大师**
   - "你想追随哪些大师的智慧？最多6位。"
   - 提供预设列表或自定义

3. **设置美德体系**
   - "使用富兰克林13美德，还是自定义？"
   - 如果自定义，引导用户定义美德名称和定义

4. **配置定时**
   - "晨语几点发送？（默认08:00）"
   - "晚复盘几点发送？（默认22:00）"

5. **选择渠道**
   - "发送到哪个平台？"

6. **自动存档**
   - "晚复盘自动保存到本地吗？"
   - 确认保存路径
