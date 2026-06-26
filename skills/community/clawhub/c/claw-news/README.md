# Claw-News Skill

智能每日新闻简报生成工具，已完整接入 OpenClaw。

## 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/claw-news
pip install -r requirements.txt
```

### 2. 配置 API Keys

```bash
cp .env.example .env
# 编辑 .env 文件，添加你的 API Keys
```

### 3. 测试运行

```bash
# 查看关注列表
python scripts/newsman.py --mode list

# 搜索测试
python scripts/newsman.py --mode search -q "人工智能"

# 生成简报（预览模式）
python scripts/newsman.py --mode digest --dry-run
```

## OpenClaw 使用方式

### 用户交互命令

在 Slack 中直接发送消息：

```
@claw newsman add <关键词>              # 添加关注
@claw newsman add <人名> --type person  # 添加人名关注
@claw newsman remove <id>               # 删除关注
@claw newsman list                      # 查看关注列表
@claw newsman run                       # 立即执行简报生成
```

### Cron 定时任务

添加每日 9:00 定时简报：

```bash
openclaw cron add \
  --name "claw-news-daily" \
  --schedule "0 9 * * *" \
  --timezone "Asia/Shanghai" \
  --sessionTarget isolated \
  --payload '{"kind": "agentTurn", "message": "运行 claw-news skill 生成每日简报: python ~/.openclaw/workspace/skills/claw-news/scripts/newsman.py --mode digest", "model": "kimi-coding/k2p5"}'
```

或使用 cron 工具：

```python
cron.add(
    name="claw-news-daily",
    schedule="0 9 * * *",
    timezone="Asia/Shanghai",
    payload={
        "kind": "agentTurn",
        "message": "python ~/.openclaw/workspace/skills/claw-news/scripts/newsman.py --mode digest",
        "model": "kimi-coding/k2p5"
    }
)
```

## 项目结构

```
claw-news/
├── SKILL.md                    # Skill 主文档
├── README.md                   # 本文件
├── requirements.txt            # Python 依赖
├── .env.example               # 环境变量示例
├── scripts/                   # 核心脚本
│   ├── newsman.py            # 主入口
│   ├── interest_manager.py   # 兴趣管理
│   ├── search_engine.py      # 多 API 搜索
│   ├── result_aggregator.py  # 结果聚合
│   ├── digest_generator.py   # 简报生成
│   └── config.py             # 配置管理
├── references/               # API 文档
│   ├── kimi_api.md
│   ├── minimax_api.md
│   └── claude_api.md
├── assets/                   # 资源文件
│   └── digest_template.md   # 简报模板
├── data/                    # 数据文件
│   ├── interest_list.json   # 关注列表
│   └── search_cache.json    # 搜索缓存
└── output/                  # 输出目录
```

## 已实现功能

- [x] 多 API 搜索轮询 (Kimi → MiniMax → Claude)
- [x] 智能去重和结果聚合
- [x] Markdown 简报生成
- [x] 关注列表管理 (添加/删除/查看)
- [x] 优先级分类
- [x] 文件缓存和输出
- [x] 配置管理

## 待优化

- [ ] Slack 消息推送集成
- [ ] 更智能的摘要生成 (LLM 优化)
- [ ] 相似度去重算法优化
- [ ] Web UI 管理界面
