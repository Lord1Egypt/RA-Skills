# 版本管理规范（v0.8.8）

## 核心原则

VERSION 文件是唯一真相源。所有版本引用都从这里同步。

## 文件结构

```
fu-mu-gong-ke/
├── VERSION              # 唯一版本真相源
├── SKILL.md            # frontmatter version 同步自 VERSION
├── VERSION_RULE.md      # 当前版本信息
└── scripts/
    └── version_sync.py  # 版本同步脚本
```

## 升级流程

```bash
# 1. 查看当前版本
python scripts/version_sync.py

# 2. 升级版本（自动同步所有引用）
python scripts/version_sync.py 0.8.9
```

version_sync.py 会同步：
- VERSION 文件
- SKILL.md frontmatter version
- VERSION_RULE.md 当前版本信息

## 版本号规则

| 变更类型 | 升级幅度 | 例子 |
|---------|---------|------|
| 错别字/格式调整 | +0.0.1 | 0.8.8 → 0.8.9 |
| 新增1-2个场景对话 | +0.0.1 | 0.8.9 → 0.8.10 |
| 新增1个AI prompt | +0.0.1 | |
| 重组章节/新增小节 | +0.1.0 | 0.8.x → 0.9.0 |
| 哲学框架重构 | +1.0.0 | 0.x.0 → 1.0.0 |

## 版本同步脚本技术要点

**教训（2026-05-28）：VERSION_RULE.md的版本号格式是`**当前版本：v0.8.8**`（单个`**`包住整句），regex必须是`**当前版本：v\d+\.\d+\.\d+\*\*`，不能用`**当前版本：**v...（在冒号后加分隔的双`**`）。**

运行验证：`python scripts/version_sync.py` 后必须检查所有三个位置是否同步。

## 升级工作流

1. 学术搜索论文（使用公开学术数据库）
2. 选定高引用论文（100+引用优先）提取核心发现
3. 写入SKILL.md新章节（内容在CHANGELOG之前）
4. 运行`python scripts/version_sync.py X.Y.Z`同步版本
5. 验证：VERSION / SKILL.md frontmatter / VERSION_RULE.md 三处一致

## 推送规则

升级10次，推送1次。保持Git历史整洁。

## 架构原则

**人性底层逻辑**作为系统基础层，融入每个模块，不是单独引擎。
- 父母的3层心理防御机制
- 孩子的3层发展需求
- 觉察→接纳→暂停→选择 解决路径
- 防御信号→看见→理解→接纳→改变 转化路径
