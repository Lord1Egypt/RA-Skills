## v1.5.1 (2026-05-30)

### 修复
- audit --fix 自动修正

---

# everything-search-breadmemory 更新日志

## v1.2.0（2026-05-23）

**改写类型：skill-standardization 标准化改造**

### 更新内容

#### 结构改造（R-01~R-10 合规）
- 新增 `references/` 目录（渐进式 MD 体系）
  - `workflow.md`：完整工作流、自动化任务、跨平台调度指南
  - `agent-behavior.md`：Agent 行为规范
  - `data-storage.md`：数据存储结构说明
  - `script-reference.md`：脚本功能参考表
- SKILL.md 从 224 行精简到 **103 行**（≤200 ✅）
- 新增完整 YAML frontmatter（name/version/author/description/tags/references）

#### 修正内容
- 一级标题修正：移除"渐进式加载示范"示范用语
- 副标题改为真实描述（从 `description` 字段提炼）
- `description` 截断问题修正（R-04 审查时只取到前 60 字符，现完整）

#### 版本号同步
- SKILL.md `version:` `1.1.1` → `1.2.0`
- `_meta.json` `"version"` `1.1.1` → `1.2.0`

---

## v1.1.1（2026-05-22）

**类型：Bug 修复**

- 修复 `breadcrumb.py` 容灾备份脚本路径问题
- 修复 `ebbinghaus.py` 复习间隔计算错误（120 天应为第 8 次，非第 7 次）

---

## v1.1.0（2026-05-20）

**类型：Minor（新功能）**

- 新增拓扑甜甜圈关联引擎（`topology_donut.py`）
- 新增艾宾浩斯复习 + 拓扑扩展联动（`daily-review-expand`）
- 完善跨平台调度指南（Linux/macOS/Windows/WorkBuddy/GitHub Actions）

---

## v1.0.0（2026-05-18）

**类型：Major（初始版本）**

- 基于 Everything/es.exe 的本地文件搜索引擎
- 面包屑小本本（breadcrumb notebook）知识管理系统
- 艾宾浩斯遗忘曲线复习引擎
- 容灾备份机制（`breadcrumb_backup_01~09.bat/py`）
