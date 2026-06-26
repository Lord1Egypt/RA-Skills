---
name: event-manager
description: "小说事件管理工具。创建、编辑、查询事件档案，支持因果链、时间线、多线叙事追踪。Use when: Architect 代理在 Phase 2 需要创建事件架构、管理因果链、规划多线叙事。"
---

# Event Manager - 事件管理工具

创建、编辑、查询事件档案的工具，支持因果链、时间线、多线叙事追踪。专为 AutoNovel Writer v5.0 设计，由 Architect 代理在 Phase 2 使用。

## 快速开始

```bash
cd ~/.openclaw/workspace/skills/event-manager

# 安装依赖
pip3 install -r requirements.txt --user

# 创建新事件
python3 scripts/manage_events.py create --title "获得传承" --type "转折点" --output events/main.yml

# 查看事件列表
python3 scripts/manage_events.py list --project ./my-novel

# 查询事件因果链
python3 scripts/manage_events.py query --title "获得传承" --project ./my-novel --show-chain

# 导出时间线
python3 scripts/manage_events.py export --project ./my-novel --output timeline.md
```

## 命令行选项

| 选项 | 说明 | 必填 |
|------|------|------|
| `create` | 创建新事件档案 | - |
| `list` | 列出所有事件 | - |
| `query` | 查询事件信息 | - |
| `update` | 更新事件档案 | - |
| `delete` | 删除事件档案 | - |
| `export` | 导出事件时间线 | - |
| `--title` | 事件标题 | create/query/update |
| `--type` | 事件类型（转折点/冲突/揭示/成长） | create |
| `--project` | 项目目录 | list/export |
| `--output` | 输出文件路径 | create/export |

## 事件档案结构

```yaml
# events/main.yml
title: 获得传承
type: 转折点
chapter: 1

# 事件描述
description: 主角在山上采药时意外坠崖，被神秘老者所救，获得古老玉佩传承。

# 因果链
causality:
  causes:
    - title: 上山采药
      chapter: 1
  effects:
    - title: 加入青云宗
      chapter: 5
    - title: 被同门嫉妒
      chapter: 8

# 参与角色
characters:
  - name: 林风
    role: 主角
    action: 获得传承
  - name: 神秘老者
    role: 导师
    action: 传授传承

# 伏笔
foreshadowing:
  - id: FS-001
    description: 玉佩上的神秘纹路
    payoff_chapter: 50
    payoff_description: 揭示玉佩是上古宗门信物

# 情绪曲线
emotion_arc:
  start: 平静
  middle: 紧张
  end: 惊喜
```

## 支持的事件类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **转折点** | 改变故事方向的重大事件 | 获得传承、身份曝光 |
| **冲突** | 角色间的对抗事件 | 比武大会、宗门争斗 |
| **揭示** | 揭露秘密或真相 | 身世之谜、幕后黑手 |
| **成长** | 角色能力提升或心理成长 | 突破境界、领悟道理 |
| **相遇** | 重要角色首次见面 | 遇见女主角、结识盟友 |
| **离别** | 角色分离或死亡 | 亲友牺牲、分道扬镳 |

## 因果链示例

```yaml
# 主线事件因果链
event_chain:
  - title: 上山采药
    chapter: 1
    type: 日常
    
  - title: 获得传承
    chapter: 1
    type: 转折点
    causes: [上山采药]
    effects: [加入青云宗]
    
  - title: 加入青云宗
    chapter: 5
    type: 成长
    causes: [获得传承]
    effects: [被同门嫉妒，遇见女主角]
    
  - title: 被同门嫉妒
    chapter: 8
    type: 冲突
    causes: [加入青云宗]
    effects: [比武大会]
```

## 使用场景 (V5 流水线)

| 阶段 | 代理 | 输入 | 输出 |
|------|------|------|------|
| **Phase 2: 事件架构** | Architect | outline.md + world.yml | events/*.yml（因果链） |

## 依赖

```bash
pip3 install -r requirements.txt --user
```

主要依赖：
- `pyyaml>=6.0.1` - YAML 文件处理
- `rich>=13.7.0` (可选) - CLI 美化输出

## 相关文件

- `scripts/manage_events.py` - 主程序
- `configs/event_templates.yml` - 事件模板配置
- `references/event_design.md` - 事件设计指南

---

**Version**: 1.0.0
**基于**: AutoNovel Writer v5.0 项目规划
