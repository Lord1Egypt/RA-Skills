# 军事招投标全周期追踪系统

集成企业微信（WeCom）的招投标全生命周期管理工具，基于 OpenClaw LLM 框架运行。

## 快速上手

### 环境要求

- Python 3.10+
- SQLite3
- 企业微信（WeCom）账号（用于接收通知）

### 安装

```bash
# 1. 克隆项目
git clone <repo-url>
cd bidding-tracker

# 2. 初始化数据库
python3 scripts/init_db.py
# 输出：数据库初始化完成：data/bids.db

# 3. 配置（可选）
cp .env.example .env
# 编辑 .env，设置 DB_PATH 等参数
```

### 初始化管理员

```bash
# 首位用户自动注册为系统总监
python3 scripts/manage_users.py \
  --bootstrap --user-id <wecom_userid> --name "张三"
```

### 注册新项目

```bash
python3 scripts/register_project.py \
  --json '{"project_name":"网络安全设备采购","budget":500000,"bid_agency":"军采中心","bid_opening_time":"2026-04-10T14:00:00"}' \
  --manager-name "李经理" \
  --travel-days 2
```

### 查询项目

```bash
# 总监查看全部活跃项目
python3 scripts/query_projects.py --user-id <wecom_userid> --active-only

# 经理查看本人项目
python3 scripts/query_projects.py --user-id <wecom_userid>

# 按关键词搜索
python3 scripts/query_projects.py --user-id <wecom_userid> --keyword "2026"
```

### 记录投标结果

```bash
python3 scripts/record_result.py \
  --project-id 1 \
  --our-price 480000 \
  --winning-price 490000 \
  --winner "我方" \
  --won true
```

### 统计分析

```bash
# 全局统计
python3 scripts/stats.py

# 按负责人分组
python3 scripts/stats.py --by-manager

# 按月度趋势
python3 scripts/stats.py --by-month

# 指定季度
python3 scripts/stats.py --by-month --period 2026-Q1
```

### Cron 提醒设置

系统支持定时提醒（在开标前1天、截标前2天、文件购买截止前3天自动推送）。

```bash
# 查看当前定时任务
python3 scripts/reminder_check.py
```

## 项目状态说明

```
registered → doc_pending → doc_purchased → preparing → sealed → opened → won/lost/cancelled
```

## 目录结构

```
scripts/          Python CLI 工具脚本
tools/            OpenClaw Tool 函数（鉴权网关）
tests/            pytest 测试套件
data/             SQLite 数据库（gitignored）
docs/             技术文档与接口规格
```

## 运行测试

```bash
DB_PATH=/tmp/test_bids.db python3 -m pytest tests/ -v
```

## 相关文档

- [技术设计文档](docs/technical-design.md)
- [接口规格文档](docs/api-interfaces.md)
- [文件结构说明](docs/file-structure.md)
