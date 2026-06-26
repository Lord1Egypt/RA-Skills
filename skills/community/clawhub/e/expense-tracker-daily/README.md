# expense-tracker-daily

> OpenClaw 智能记账 Skill — 用自然语言记账，AI 自动分类，多维度统计分析。

一句话记账，不用打开任何 App。对 AI 说"午饭花了35"，自动记录、自动归类。

## 特性

- 🗣️ **自然语言输入** — "午饭35"、"打车25块"、"昨天买衣服200" 都行
- 🏷️ **智能分类** — 9 大分类，100+ 关键词自动匹配
- 📊 **多维度统计** — 按日/周/月统计，按分类排行，每日趋势
- 🗑️ **完整 CRUD** — 添加、查询、删除，数据可控
- 💾 **纯本地存储** — 数据存本地 JSON，不联网、不传云端
- 📦 **零依赖** — 纯 Python 标准库，不需要安装任何第三方包

## 快速开始

### 前置要求

- [OpenClaw](https://github.com/nicepkg/openclaw) 已安装并运行
- Python 3.7+

### 安装

将整个 `expense-tracker-daily` 目录复制到 OpenClaw skills 目录：

```bash
cp -r expense-tracker-daily ~/.qclaw/skills/expense-tracker-daily
```

Windows:

```powershell
Copy-Item -Recurse expense-tracker-daily $env:USERPROFILE\.qclaw\skills\expense-tracker-daily
```

重启 OpenClaw Gateway 即生效。

### 使用

安装后直接用自然语言跟 AI 对话即可：

| 你说的 | AI 做的事 |
|--------|----------|
| 午饭花了35 | 记录：餐饮 ¥35.00 — 午饭 |
| 打车去公司25块 | 记录：交通 ¥25.00 — 打车去公司 |
| 昨天买衣服200 | 记录：购物 ¥200.00 — 买衣服（日期=昨天） |
| 本月花了多少 | 按月统计，分类排行 + 每日趋势 |
| 最近有什么餐饮支出 | 查询餐饮分类的记录列表 |
| 删掉刚才那笔 | 通过 id 删除指定记录 |
| 查一下所有分类 | 列出支持的 9 大分类 |

## 目录结构

```
expense-tracker-daily/
├── README.md                  ← 你正在看的文件
├── SKILL.md                   ← OpenClaw Skill 配置（AI 指令）
├── scripts/
│   └── expense_tracker.py     ← 核心引擎（数据存储 + 统计计算）
└── references/
    └── categories.md          ← 分类关键词映射表
```

### 文件说明

| 文件 | 作用 |
|------|------|
| `SKILL.md` | OpenClaw Skill 的入口文件，定义元数据、触发条件、处理流程。AI 读这个文件来知道怎么用这个 Skill |
| `scripts/expense_tracker.py` | Python CLI 工具，负责所有数据操作。AI 通过调用这个脚本来读写数据 |
| `references/categories.md` | 完整的分类关键词映射表，AI 用它来判断一句话属于哪个分类 |

## 数据存储

所有记账数据存储在本地：

```
~/.qclaw/workspace/expense-tracker-daily-data/
├── expenses.json    ← 所有支出记录
└── config.json      ← 用户配置（扩展分类等）
```

数据文件和 Skill 目录隔离——卸载 Skill 不会丢数据，重装 Skill 直接接着用。

### 数据格式（expenses.json）

```json
[
  {
    "id": 1,
    "amount": 35.0,
    "category": "餐饮",
    "description": "午饭",
    "date": "2026-04-09",
    "timestamp": 1775725459669
  }
]
```

## 支持的分类

| 分类 | 关键词示例 |
|------|-----------|
| 🍜 餐饮 | 午饭、外卖、火锅、奶茶、咖啡、烧烤... |
| 🚌 交通 | 打车、地铁、高铁、油费、停车... |
| 🛒 购物 | 超市、淘宝、买衣服、日用品、数码... |
| 🎮 娱乐 | 电影、游戏、演唱会、旅游、会员... |
| 🏠 住房 | 房租、水电、燃气、物业、宽带... |
| 🏥 医疗 | 看病、药、体检、挂号、保险... |
| 📚 教育 | 学费、培训、网课、教材、考试... |
| 🎁 人情 | 红包、份子、礼物、随礼、过节... |
| 📦 其他 | 无法匹配以上分类的支出 |

完整关键词表见 [`references/categories.md`](references/categories.md)。

## CLI 命令参考

`expense_tracker.py` 也支持直接命令行调用：

```bash
# 添加记录
python scripts/expense_tracker.py add --amount 35 --category 餐饮 --desc "午饭" --date 2026-04-09

# 查询记录
python scripts/expense_tracker.py list --limit 20
python scripts/expense_tracker.py list --category 餐饮 --from 2026-04-01 --to 2026-04-30

# 统计分析
python scripts/expense_tracker.py stats --period month
python scripts/expense_tracker.py stats --period week
python scripts/expense_tracker.py stats --period day --date 2026-04-09

# 全局总览
python scripts/expense_tracker.py summary --top 5

# 查看分类
python scripts/expense_tracker.py categories

# 删除记录
python scripts/expense_tracker.py delete --id 3
```

## 工作原理

```
用户: "午饭花了35块"
        │
        ▼
   ┌─────────────┐
   │  AI 解析层   │  ← SKILL.md 定义的规则
   │ 提取金额/    │     金额: 35
   │ 分类/日期    │     分类: 餐饮 (关键词匹配)
   └──────┬──────┘     日期: 今天
          │
          ▼
   ┌─────────────┐
   │ Python 引擎  │  ← expense_tracker.py
   │ 写入 JSON    │     纯本地，零依赖
   └──────┬──────┘
          │
          ▼
   ✅ 已记录：餐饮 ¥35.00 — 午饭 (2026-04-09)
```

AI 负责「理解人话」，Python 脚本负责「存数据」，各司其职。

## Roadmap

- [ ] CSV 导出（方便导入 Excel）
- [ ] 预算设置 + 超支提醒
- [ ] 多币种支持
- [ ] 云端同步（IMA / 腾讯文档 / Notion）
- [ ] 图表生成（支出趋势图）

## License

MIT
