# mark-still-growing 升级工作流

## 版本规则
- 每次新增一个主题章节 → +0.0.1
- 满10次升级 → 合并推送一次 GitHub
- VERSION 是唯一真相源
- **版本同步四文件**：VERSION + SKILL.md frontmatter + CHANGELOG.md + 实际代码版本号

## 吸收 OpenClaw 代码工作流（2026-05-30 新增）

**适用场景**：从 OpenClaw 版本（如 `~/.jvs/.openclaw/skills/skills/still-growing/`）吸收代码到 mark-still-growing

**三阶段模式**：
1. **并发分析**（子任务）：同时分析 OpenClaw 源码 + mark-still-growing 现有代码，找出集成点
2. **顺序集成**：基于分析结果，依次执行代码集成
3. **代码审计并行**：集成同时运行代码审计（语法/安全/bug）

**关键发现**：OpenClaw still-growing 在 `~/.jvs/.openclaw/skills/skills/still-growing/`，与 `~/.hermes/skills/mark-still-growing/` 是两个独立技能

**示例**（v0.9.55-0.9.56）：
- 并行子任务1：分析 core_v2.py IntentEngine/EmotionAnalyzer → 集成方案报告
- 并行子任务2：代码审计 assessment.py → 发现 `--all` 遗漏严重Bug
- 顺序执行：修复Bug + 集成 EmotionAnalyzer → 版本→0.9.56

## 大型 SKILL.md（>2000行）插入模式

1. 找到最后一个主要章节和 `## 可运行工具` 之间的断点
2. 用 `patch` 工具插入新内容（不要用 write_file 覆盖全文）
3. 同步三处：
   - `VERSION` 文件
   - `SKILL.md` frontmatter `version:`
   - 检查其他引用处是否需要更新

## 插入点定位
```
# 在 SKILL.md 中搜索最后一个 ## 标题（如"## 📊 科学研究支撑"）
# 找到该章节末尾的空白行
# 下一行是 ## 可运行工具
# 在空白行和 ## 可运行工具之间插入
```

## 插件注意事项
- 心虫插件名：`heartflow-memory`（连字符，非下划线）
- 路径：`~/.hermes/plugins/heartflow-memory/`
- 启用命令：`hermes plugins enable heartflow-memory`

## 五个升级方向（已计划）
1. ✅ 离婚与单亲家庭（v0.9.23）
2. ✅ 多子女家庭（v0.9.23）
3. ✅ 祖辈育儿（v0.9.23）
4. ✅ 父母脆弱时刻（v0.9.23）
5. ⬜ 扩充学术研究（2024-2025最新数据）
