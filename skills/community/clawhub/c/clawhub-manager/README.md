# ClawHub 管理技能

简化和自动化 ClawHub 技能的管理操作。

## 功能

- 🔍 **查询技能** - 查看技能详细信息和统计数据
- 🔎 **搜索技能** - 在 ClawHub 上搜索技能
- 📦 **发布技能** - 将本地技能发布到 ClawHub
- 🗑️ **删除技能** - 从 ClawHub 删除已发布的技能
- 📋 **列出技能** - 列出本地已安装的技能

## 使用方法

### 查询技能

```bash
bash scripts/inspect.sh feishu-voice
bash scripts/inspect.sh feishu-voice --json
```

### 搜索技能

```bash
bash scripts/search.sh "feishu"
bash scripts/search.sh "pdf" --limit 20
```

### 列出本地技能

```bash
bash scripts/list.sh
```

### 发布技能

```bash
bash scripts/publish.sh /path/to/skill --version 1.0.0
bash scripts/publish.sh /path/to/skill --version 1.0.0 --changelog "首次发布"
```

### 删除技能

```bash
bash scripts/delete.sh my-skill
```

## 依赖

- `clawhub` CLI 工具
- `jq` (JSON 处理，用于 --json 输出)

## 作者

franklu0819-lang

## 许可证

MIT
