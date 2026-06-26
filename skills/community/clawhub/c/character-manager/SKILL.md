---
name: character-manager
description: "小说角色管理工具。创建、编辑、查询角色档案，支持角色关系网络、情感弧光、动机追踪。Use when: Architect 代理在 Phase 3 需要创建角色档案、管理角色关系、追踪角色成长轨迹。"
---

# Character Manager - 角色管理工具

创建、编辑、查询角色档案的工具，支持角色关系网络、情感弧光、动机追踪。专为 AutoNovel Writer v5.0 设计，由 Architect 代理在 Phase 3 使用。

## 快速开始

```bash
cd ~/.openclaw/workspace/skills/character-manager

# 安装依赖
pip3 install -r requirements.txt --user

# 创建新角色
python3 scripts/manage_characters.py create --name "林风" --role "主角" --output characters/linfeng.yml

# 查看角色列表
python3 scripts/manage_characters.py list --project ./my-novel

# 查询角色关系
python3 scripts/manage_characters.py query --name "林风" --relation "盟友"

# 导出角色档案
python3 scripts/manage_characters.py export --project ./my-novel --output characters_export.md
```

## 安全说明

**重要**: `--project` 参数用于指定项目目录，工具会读取和写入该目录中的 YAML 文件。

**安全建议**:
- ✅ 仅指向小说项目目录（如 `./my-novel`）
- ✅ 使用相对路径或工作区内的绝对路径
- ❌ 不要指向系统目录（如 `/etc`, `/home`, `~/.ssh`）
- ❌ 不要指向包含敏感数据的目录

**示例**:
```bash
# ✅ 安全
python3 scripts/manage_characters.py list --project ./my-novel
python3 scripts/manage_characters.py export --project /home/user/workspace/novels/my-book

# ❌ 危险 - 不要这样做
python3 scripts/manage_characters.py list --project /etc
python3 scripts/manage_characters.py list --project ~/.ssh
```

## 命令行选项

| 选项 | 说明 | 必填 |
|------|------|------|
| `create` | 创建新角色档案 | - |
| `list` | 列出所有角色 | - |
| `query` | 查询角色信息 | - |
| `update` | 更新角色档案 | - |
| `delete` | 删除角色档案 | - |
| `export` | 导出角色档案 | - |
| `--name` | 角色名称 | create/query/update |
| `--role` | 角色类型（主角/配角/反派） | create |
| `--project` | 项目目录 | list/export |
| `--output` | 输出文件路径 | create/export |

## 角色档案结构

```yaml
# characters/linfeng.yml
name: 林风
role: 主角
age: 16
gender: 男

# 外貌特征
appearance:
  height: 175
  build: 清瘦
  features:
    - 剑眉星目
    - 气质出尘
  clothing_style: 朴素青衣

# 性格特征
personality:
  traits:
    - 坚韧不拔
    - 重情重义
    - 聪明机智
  flaws:
    - 有时冲动
    - 不愿示弱
  mbti: ENFP

# 背景故事
background:
  origin: 青石镇普通少年
  family: 父母早逝，与爷爷相依为命
  key_events:
    - chapter: 1
      event: 获得神秘玉佩传承
    - chapter: 10
      event: 加入青云宗

# 能力体系
abilities:
  cultivation:
    current_realm: 练气三层
    max_realm: 未知
    skills:
      - 基础剑法
      - 青木诀
  special:
    - 玉佩空间
    - 快速学习

# 人际关系
relationships:
  - name: 苏媚
    type: 女主角
    status: 暧昧
    description: 青云宗圣女，对林风有好感
  - name: 萧炎
    type: 竞争对手
    status: 亦敌亦友
    description: 同门师兄，天赋异禀

# 情感弧光
emotional_arc:
  start: 平凡少年，渴望力量
  midpoint: 发现身世之谜，陷入迷茫
  end: 接受使命，成长为强者

# 动机追踪
motivation:
  surface_goal: 成为强者，保护重要的人
  deep_goal: 寻找父母失踪真相
  internal_conflict: 力量与本心的平衡
```

## 支持的角色类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **主角** | 故事核心人物 | 林风 |
| **女主角** | 感情线核心 | 苏媚 |
| **重要配角** | 推动剧情的关键配角 | 导师、盟友 |
| **配角** | 一般配角 | 同门、路人 |
| **反派** | 对立面角色 | 宿敌、BOSS |
| **中立** | 立场不明确的角色 | 商人、情报贩子 |

## 关系类型

| 类型 | 说明 |
|------|------|
| 盟友 | 站在主角一方的角色 |
| 敌人 | 对立面角色 |
| 竞争对手 | 亦敌亦友的关系 |
| 师徒 | 师傅/徒弟关系 |
| 亲人 | 父母、兄弟姐妹 |
| 暧昧 | 感情线未明确 |
| 恋人 | 确定的恋爱关系 |

## 使用场景 (V5 流水线)

| 阶段 | 代理 | 输入 | 输出 |
|------|------|------|------|
| **Phase 3: 角色档案** | Architect | outline.md + world.yml | characters/*.yml (≥3 个主角) |

## 依赖

```bash
pip3 install -r requirements.txt --user
```

主要依赖：
- `pyyaml>=6.0.1` - YAML 文件处理
- `rich>=13.7.0` (可选) - CLI 美化输出

## 相关文件

- `scripts/manage_characters.py` - 主程序
- `configs/character_templates.yml` - 角色模板配置
- `references/character_design.md` - 角色设计指南

---

**Version**: 1.0.0
**基于**: AutoNovel Writer v5.0 项目规划
