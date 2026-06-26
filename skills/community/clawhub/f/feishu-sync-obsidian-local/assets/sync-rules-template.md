# SYNC-RULES.md — 飞书同步规则

> 本文件定义飞书 Wiki 到本 vault 的同步规范。
> 安装 feishu-sync-obsidian Skill 后，如无 SYNC-RULES.md，
> 小墨会生成默认版本，用户确认后写入。
>
> **核心**：编辑本文件即可修改同步行为，无需修改 Skill 代码。

---

## 数据源

> 格式：`| Wiki 名称 | Space ID | 目标路径 |`
> sync.py 启动时从本段读取配置，不再硬编码。
> 如需新增/修改 Wiki，直接编辑此表后重新同步即可。

| Wiki 名称 | Space ID | 目标路径 |
|-----------|---------|---------|
| 个人成长 | 7619963059842419643 | 02WIKI/00原料池/飞书文档 |
| openclaw知识库 | 7617330356886178745 | 02WIKI/00原料池/飞书文档 |

**Space ID 获取方式**：
打开飞书 Wiki 知识库，复制浏览器 URL 中的 space ID。
例如：`https://vcndmev90kwz.feishu.cn/wiki/xxxxx` → `xxxxx` 是节点 token，不是 space ID。
Space ID 需要从飞书开放平台或 API 文档获取。

---

## frontmatter 规范

### 基础字段（必含）

```yaml
---
date: YYYY-MM-DD           # 创建日期
lastmod: YYYY-MM-DD        # 最后修改
draft: false               # 是否草稿
categories: []              # Hugo FixIt 分类
tags: []                    # 标签
feishu_doc_token: xxx       # 飞书文档 token（去重，必填）
feishu_wiki: xxx            # 来源 Wiki 名称
feishu_node_token: xxx      # 节点 token
---
```

### 已有 vault 的 frontmatter

如果 vault 已有其他 frontmatter 规范（定义在 AGENTS.md 或 converter.py），
**优先使用已有规范**，飞书扩展字段（feishu_doc_token / feishu_wiki / feishu_node_token）
**无条件追加**到已有字段之后。

### feishu 扩展字段说明

| 字段 | 用途 | 说明 |
|------|------|------|
| `feishu_doc_token` | 去重 | 飞书文档 token，已存在则跳过同步 |
| `feishu_wiki` | 来源追踪 | Wiki 名称（与数据源表中的 Wiki 名称一致） |
| `feishu_node_token` | 来源追踪 | 节点 token |

---

## 同步策略

### 目录结构保留
同步时**保留飞书 Wiki 的目录层级**，按 `parent_node_token` 递归构建路径：
```
飞书：个人成长/2026-03/学习计划.md
同步后：02WIKI/00原料池/飞书文档/个人成长/2026-03/学习计划.md
```

### 去重
按 `feishu_doc_token` 去重。vault 中已有相同 token 的文档跳过。

### 增量
支持中断后重新同步。已完成写入的文件不受影响。
同步状态记录在 `/tmp/feishu-sync-obsidian/sync_state.json`。

### 目录自动创建
目标路径不存在时，自动创建目录。
例如：`02WIKI/00原料池/飞书文档` 会自动创建。

### 非 docx 类型处理

| 类型 | 处理方式 |
|------|---------|
| sheet | 写入链接占位符，不拉内容 |
| bitable | 写入链接占位符，不拉内容 |
| mindnote | 写入链接占位符，不拉内容 |
| docx | 完整同步内容 |

---

## 同步触发

- **手动**：告诉小墨"同步飞书"
- **自动**：每周日 00:00（systemd timer）

---

## 路由规则（可选）

> 以下为**可选**的高级功能。默认不使用路由表，所有文档同步到数据源指定的目标路径。
> 如需启用路由规则（按关键词分发到不同目录），在下方定义。

<!--
## 路由规则

| Wiki | 关键词 | 目标路径 |
|------|--------|---------|
| 个人成长 | 软考 | 01务实之道/软考 |
| 个人成长 | 英语 | 01务实之道/英语 |
| 个人成长 | 默认 | 05进思斋 |
| openclaw知识库 | 默认 | 03藏珍之库/工具 |

**匹配逻辑**：按顺序首个命中即终止，未命中使用「默认」路径。
如需启用，删除上面的 HTML 注释包裹，并删除数据源表中的目标路径列。
-->
