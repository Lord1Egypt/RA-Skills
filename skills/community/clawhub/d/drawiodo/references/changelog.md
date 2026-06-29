## [2.6.1] - 2026-06-19

### 修复
- 修复: drawio_agent.py 硬编码钩子调用(PRE_THINK/POST_THINK/PRE_ITERATE/POST_ITERATE) + 版本自动备份集成

---

## [2.6.0] - 2026-06-19

### 修复
- refactor: drawiodo

---

## [2.5.0] - 2026-06-19

### 修复
- refactor: drawiodo

---

## 2.4.1 (2026-06-10)

### 修复
- 修复FAQ排错章节格式 + changelog反斜杠引用清理

---


## 2.4.0 (2026-06-10)

### 新增
- **钩子系统强制约束**：12 个内置钩子全部 Python 端执行，0 个依赖 LLM 自觉
  - `preview_trigger` 钩子：直接调用 subprocess.Popen 打开 draw.io 预览
  - `shortcut_detector` 钩子：快捷模式时直接清除 confirm_options，LLM 无法 AskUserQuestion
  - `auto_backup` 钩子：迭代前直接调用 VersionManager.save_version() 自动备份
  - `limit_checker` 钩子：版本超限时直接删除最旧版本
- 新增 `references/hooks.md`：钩子系统完整参考文档

### Changed
- 输出路径标准化：`{workspace}` → `skills/.standardization/drawiodo/outputs/`（铁律 4）
- 创建 outputs/ 和 temp/ 标准化目录
- SKILL.md 正文冗余路径清理（删 8 行）
- 生成图表章节拆分到 `references/generation.md`（247→194 行）

### 修复
- trigger 字段反斜杠损坏修复：--fix 将触发词中的 `draw.io` 反复转义为大量反斜杠，已恢复
- 版本号三端一致：SKILL.md = _meta.json = changelog = 2.4.0
- _meta.json description 与 SKILL.md frontmatter 同步

---

## 2.3.2 (2026-06-10)

### 标准化
- skill-standardization v2 全量审计（R-01~R-26），25/25 PASS，0 ERROR 0 WARN
- 修复 R-10：三端版本号一致（SKILL.md = _meta.json = changelog = 2.3.2）
- 修复 R-17：生成图表章节拆分到 references/generation.md，SKILL.md 从 247 行降至 196 行
- 修复 _meta.json description 与 SKILL.md frontmatter 不一致
- 修复 changelog.md 旧版 v 前缀
- 更新 `references/generation.md`：从 SKILL.md 拆分，保持渐进加载
## 2.3.0 (2026-06-10)

### 新增
- **钩子系统**：在 Think→Confirm→Iterate→VC 四阶工作流中植入 8 个 Hook Point
- 新增 `scripts/drawio_hooks.py`：钩子引擎（注册/注销/执行/历史/自检），含 12 个内置钩子
- 新增 `references/hooks.md`：钩子系统完整参考文档
- `pre_think` 钩子：输入校验 + 上下文补全
- `post_think` 钩子：分析输出完整性校验
- `pre_confirm` 钩子：选项校验 + 快捷模式检测
- `post_confirm` 钩子：用户选择解析
- `pre_iterate` 钩子：文件存在性检查 + 备份触发
- `post_iterate` 钩子：输出校验 + 自动预览触发
- `pre_vc` 钩子：版本上限检查
- `post_vc` 钩子：版本状态报告
- 反模式新增：跳过钩子校验、篡改钩子注册表

### 强制约束机制
- **`auto_backup` 钩子**：迭代更新前直接调用 `VersionManager.save_version()` 自动备份，**不依赖 LLM 自觉**
- **`output_validator` 钩子**：首次生成后直接调用 `VersionManager.init()` 自动初始化版本管理，**不依赖 LLM 自觉**
- **`limit_checker` 钩子**：版本数超限时直接删除最旧版本目录，**不依赖 LLM 自觉**
- **`preview_trigger` 钩子**：直接调用 `subprocess.Popen()` 打开 draw.io 预览，**不依赖 LLM 自觉**（升级前为 flag 模式）
- **`shortcut_detector` 钩子**：快捷模式时直接清除 `confirm_options`，LLM 无法展示 AskUserQuestion（升级前为 flag 模式）
- `file_checker` 钩子：输出目录不存在时自动 `os.makedirs()` 创建
- 废弃 `backup_trigger`（flag 模式），替换为 `auto_backup`（Python 执行模式）
- 所有相关文档同步更新：hooks.md/SKILL.md/guide.md/antipatterns.md

---

## 2.2.2 (2026-06-04)

### 修复
- audit --fix 自动修正: frontmatter_fields, h1, version, external_data_dir
- 修复 H1 不含技能名（# drawiodo: draw.io 自动做图 Skill）
- 补充 frontmatter trigger 字段（4 条触发规则）
- 修复 _meta.json description 与 SKILL.md 不一致
- 修复 SKILL.md data_dir 路径与 _meta.json 统一
- 修复 changelog.md 旧版本 v 前缀（v2.2.1 → 2.2.1）
- 删除 drawio.py 硬编码 LIB_DIR 路径，改用脚本所在目录
- 修复 drawio_templates.py import math 在文件末尾问题

---

## 2.2.1 (2026-05-30)

### 修复
- audit --fix 自动修正
