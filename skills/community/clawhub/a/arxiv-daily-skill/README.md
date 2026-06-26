# arXiv 每日论文推送 Skill

自动搜集 arXiv 上 LLM/RAG/Agent 等方向的最新论文，整理成结构化报告并通过飞书推送。

## 📁 文件结构

```
arxiv-daily-skill/
├── SKILL.md                    # Skill 定义
├── fetch_arxiv.py              # 核心脚本（获取 + 格式化 + 机构数据库）
├── deep_analyze.py             # 深度分析工具（详解单篇论文）
├── cron_run.sh                 # Cron 执行入口（带飞书推送）
├── run.sh                      # 手动测试脚本
├── test_affiliations.py        # 机构提取测试工具
├── affiliations_db.json        # 机构数据库（自动累积）
├── feishu_config.json.template # 飞书配置模板
└── README.md                   # 本文档
```

## 🚀 快速开始

### 1. 手动测试

```bash
cd /home/admin/.openclaw/workspace/skills/arxiv-daily-skill
python3 fetch_arxiv.py
```

### 2. 配置飞书推送

```bash
# 复制配置模板
cp feishu_config.json.template feishu_config.json

# 编辑配置文件，填入你的飞书 Webhook URL
vim feishu_config.json
```

**飞书 Webhook 获取步骤：**
1. 在飞书群聊中右键 → 添加机器人
2. 选择"自定义机器人"
3. 复制 Webhook 地址（形如 `https://open.feishu.cn/open-apis/bot/v2/hook/xxx`）
4. 粘贴到 `feishu_config.json` 的 `webhook_url` 字段

### 3. 设置定时任务

已配置 cron（工作日 9:00 AM）：

```bash
# 查看当前 cron 配置
crontab -l

# 如需手动添加：
echo "0 9 * * 1-5 /home/admin/.openclaw/workspace/skills/arxiv-daily-skill/cron_run.sh" | crontab -
```

## 📋 输出格式

### 目录（紧凑）
```markdown
## 📋 目录
1. Visual Preference Optimization with Rubric Rewards
2. Rethinking On-Policy Distillation of Large Language Models
...
```

### 详解（带机构信息）
```markdown
### 1. 论文标题
**arXiv**: 2604.13016v1 | 2026-04-14 | Tsinghua University + THUNLP
**作者**: Yaxuan Li, Yuxin Zuo, Bingxiang He et al.
**链接**: https://arxiv.org/abs/2604.13016v1

**中文摘要**:
> ...

**解决的问题**:
- ...

**核心创新**:
- ...

**为什么重要**:
- ...

**局限性**:
- ...
```

## 🔧 高级功能

### 深度分析单篇论文

```bash
python3 deep_analyze.py 2604.13016
```

或在对话中说：
- "详解第 3 篇"
- "分析 2604.13016 这篇论文"
- "用 ljg-paper 分析这篇"

### 机构数据库

机构信息自动累积在 `affiliations_db.json` 中：
- 首次运行时从 arXiv HTML 页面提取
- 自动保存到数据库
- 后续运行直接使用缓存

查看数据库：
```bash
cat affiliations_db.json | python3 -m json.tool
```

## 📊 搜索方向

当前配置的方向：
- **LLM**: Large Language Model
- **RAG**: Retrieval Augmented Generation
- **Agent**: AI Agent / Autonomous Agent
- **Transformer**: Transformer Architecture
- **Harness**: Agent Harness / Harness Engineering
- **Reasoning**: Language Model Reasoning

修改 `fetch_arxiv.py` 中的 `SEARCH_CONFIGS` 数组可自定义搜索方向。

## 🎯 使用场景

### 每日推送
- ⏰ 工作日 9:00 AM 自动执行
- 📤 飞书推送目录 + Top 5 详解
- 💾 完整报告保存到 `/tmp/arxiv_daily_YYYYMMDD.md`

### 主动查询
- "今天有什么新论文？"
- "看看今天的 arXiv 推送"
- "详解第 X 篇"

### 深度研究
- "用 ljg-paper 分析 2604.13016"
- "这篇论文的核心思想是什么？"
- "这篇论文值得精读吗？"

## 📝 更新日志

- **v5** (2026-04-16): 添加机构数据库自动累积、飞书推送、深度分析工具
- **v4** (2026-04-16): 优化机构信息提取、紧凑目录格式
- **v3** (2026-04-16): 基础版本（获取 + 格式化）

## 🤝 贡献

如需添加新的搜索方向或优化机构提取逻辑，请修改：
- `SEARCH_CONFIGS`（搜索方向）
- `extract_affiliations_from_html()`（机构提取）
- `top_institutions` 字典（知名机构列表）

---

**维护者**: OpenClaw Agent
**最后更新**: 2026-04-16
