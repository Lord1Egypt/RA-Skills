# Feishu Power Skill 🦅

飞书深度自动化 Skill，让 AI Agent 像飞书重度用户一样操作飞书。

飞书官方 MCP 只做文档读写。我们做的是：**多维表格自动化 + 跨文档工作流 + 智能报告生成 + 零售运营审计**。

## 兼容平台

| 平台 | 入口文件 | 说明 |
|------|---------|------|
| [OpenClaw](https://github.com/openclaw/openclaw) | `SKILL.md` | 放到 `~/.openclaw/skills/feishu-power-skill/` 自动加载 |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | `CLAUDE.md` | 放到项目目录，Claude Code 自动读取 |

同一套代码，两个入口，各自按自己的协议发现能力。

## 功能

| 模块 | 脚本 | 能力 |
|------|------|------|
| Bitable 引擎 | `bitable_engine.py` | 批量创建/更新、跨表 JOIN、数据快照、统计摘要、CSV/JSON 导入 |
| 文档工作流 | `doc_workflow.py` | 模板引擎 + Bitable 数据→飞书文档一步生成 |
| 零售审计 | `retail_audit.py` | YAML 配置化规则、门店健康评分、异常诊断、报告自动发布 |
| 定时报告 | `report_generator.py` | 日/周/月调度、多报告类型、YAML 配置、状态跟踪 |
| API 封装 | `feishu_api.py` | Token 自动管理、Bitable/Docx/Wiki/Drive 全覆盖 |

## 快速开始

### 1. 配置飞书凭证

```bash
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx
```

需要一个飞书自建应用，开通 Bitable 和 Docx 相关权限。

### 2. 安装（推荐）

```bash
bash install.sh
```

自动检测环境、安装依赖、链接到 OpenClaw/Claude Code、运行冒烟测试。

也可以手动：`pip install requests pyyaml`

### 3. 使用

**Bitable 批量操作：**

```bash
# 批量创建记录
python3 scripts/bitable_engine.py batch-create --app <app_token> --table <table_id> --data records.json

# 跨表 JOIN
python3 scripts/bitable_engine.py join --app <app_token> --left <table1> --right <table2> --on "字段名"

# 统计摘要
python3 scripts/bitable_engine.py stats --app <app_token> --table <table_id>
```

**Bitable 数据 → 飞书文档：**

```bash
python3 scripts/doc_workflow.py generate \
  --app <app_token> --table <table_id> \
  --template templates/data_summary.md \
  --title "周报标题"
```

**零售运营审计：**

```bash
# Demo（50家模拟门店）
python3 scripts/retail_audit.py demo --output report.md

# 真实数据审计 + 发布到飞书
python3 scripts/retail_audit.py audit \
  --app <app_token> --sales-table <table_id> \
  --config configs/retail_default.yaml \
  --publish
```

**定时报告调度：**

```bash
# 运行所有到期任务
python3 scripts/report_generator.py run --schedule configs/schedule.yaml

# 列出任务状态
python3 scripts/report_generator.py list --schedule configs/schedule.yaml

# 强制运行指定任务
python3 scripts/report_generator.py run --schedule configs/schedule.yaml --job daily_audit --force
```

## 模板语法

```
{{变量名}}                    — 简单替换
{{#each 列表}}...{{/each}}   — 循环
{{#if 条件}}...{{/if}}       — 条件判断
{{TODAY}} {{NOW}}             — 内置日期变量
```

## 审计规则配置

YAML 配置化，按行业切换阈值：

```yaml
rules:
  sell_through_high:
    enabled: true
    level: critical
    thresholds:
      sell_through_min: 0.85
      days_left_max: 3
```

内置：`retail_default.yaml`（服装）、`fmcg.yaml`（快消）。复制一份改阈值即可适配其他行业。

## 项目结构

```
feishu-power-skill/
├── SKILL.md                 # OpenClaw 入口
├── CLAUDE.md                # Claude Code 入口
├── scripts/
│   ├── feishu_api.py        # 飞书 API 封装
│   ├── bitable_engine.py    # 多维表格引擎
│   ├── doc_workflow.py      # 文档工作流
│   ├── retail_audit.py      # 零售审计引擎
│   └── report_generator.py  # 定时报告生成器
├── templates/               # 文档模板
│   ├── weekly_report.md
│   └── data_summary.md
└── configs/                 # 审计规则
    ├── retail_default.yaml
    └── fmcg.yaml
```

## License

MIT
