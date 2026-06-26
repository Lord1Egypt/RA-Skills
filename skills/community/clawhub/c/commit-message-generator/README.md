# 📝 Git 提交信息生成器

根据代码变更内容，自动生成符合 Conventional Commits 规范的 Git 提交信息。

## 📌 功能简介

本 Skill 帮助开发人员快速生成规范的 Git 提交信息，确保团队提交历史清晰、可读，便于生成变更日志和自动化版本发布。

## 🎯 解决什么问题

- ❌ 提交信息随意写，历史难以阅读
- ❌ 不符合团队规范，被要求重写
- ❌ 忘记关联 Issue 号，难以追溯
- ❌ 不清楚 Conventional Commits 规范

## ✨ 核心功能

1. **自动分类** - 智能识别变更类型（feat/fix/docs/refactor 等）
2. **范围提取** - 从代码变更中识别影响模块
3. **规范输出** - 符合 Conventional Commits 标准
4. **Issue 关联** - 自动提取并关联需求号

## 🚀 使用方式

### 触发词

- `生成提交信息`
- `提交信息`
- `commit message`
- `git commit`
- `生成 commit 信息`

### 使用示例

**输入：**
```
生成提交信息：新增缓冲液单人份配置功能，支持精确计算消耗量，需求号 234
```

**输出：**
```
feat(algorithm): 增加缓冲液单人份独立配置

- 新增配置项"单人份缓冲液量"
- 修改稀释逻辑，支持按实际人份计算

Closes #234
```

**输入（带 git diff）：**
```
生成提交信息
diff --git a/src/core/algorithm.py b/src/core/algorithm.py
+ def calculate_reagent_volume():
+     """计算试剂用量"""
+     pass
```

**输出：**
```
feat(core): 新增试剂用量计算函数

- 新增 calculate_reagent_volume 函数
- 实现试剂用量计算逻辑
```

## 📁 技能结构

```
commit-message-generator/
├── SKILL.md                          # 技能主文档
├── package.json                      # ClawHub 发布配置
├── README.md                         # 使用说明
├── scripts/
│   └── generate_commit_message.py    # 提交信息生成脚本
└── references/
    ├── conventional-commits.md       # Conventional Commits 完整规范
    └── commit-examples.md            # 提交信息示例集合
```

## 🏷️ 适用场景

- 日常代码提交
- Bug 修复提交
- 版本发布
- 团队协作开发
- 开源项目贡献

## 📊 变更类型说明

| 类型 | 说明 | 版本影响 |
|------|------|----------|
| feat | 新功能 | 次版本号（minor） |
| fix | 修复 Bug | 修订号（patch） |
| docs | 文档更新 | 无 |
| style | 代码格式 | 无 |
| refactor | 重构 | 无 |
| perf | 性能优化 | 修订号（patch） |
| test | 测试相关 | 无 |
| chore | 杂项 | 无 |

## 🔗 相关资源

- [Conventional Commits 规范](references/conventional-commits.md)
- [提交信息示例](references/commit-examples.md)

## 📝 更新日志

### v1.0.0 (2026-03-29)
- 初始版本发布
- 支持自动生成提交信息
- 智能识别变更类型和范围
- 包含完整规范和示例文档

## 👨‍💻 作者

Leo

## 📄 许可证

MIT
