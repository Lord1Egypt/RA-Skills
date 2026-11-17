# Enterprise File Writer 更新日志

## [1.3.0] - 2026-07-16

### 🔒 安全增强

**新增安全检查机制**
- 添加路径安全检查函数 `check_path_safety()`
- 自动检测敏感系统路径（Windows: `C:\Windows`, `C:\Program Files`; Unix: `/etc`, `/usr`, `/bin`）
- 检测敏感文件类型（`.env`, `.git/config`, `.ssh/`, 凭据文件, 证书文件）
- 警告可执行脚本写入（`.sh`, `.bash`, `.bat`, `.cmd`, `.ps1`, `.vbs`）
- 检测路径遍历风险（`..`）

**新增命令行参数**
- `--force`: 跳过安全警告确认（谨慎使用）

**修改写入函数**
- 所有写入函数添加 `force` 参数，支持安全检查
- 检测到风险时输出警告到 stderr
- 未使用 `--force` 参数时中止操作
- 覆盖现有文件时输出覆盖警告

**文档更新**
- SKILL.md: 添加"安全警告"部分，明确 Agent 使用约束
- README.md: 添加安全警告和检查机制说明
- 添加用户确认要求说明

### 📋 问题修复

修复 SkillSpector 扫描发现的 3 个中等风险问题：
1. ✅ 文档未明确警告覆盖和目录创建行为的破坏性风险
2. ✅ Skill 支持覆盖和目录创建但未要求确认或警告
3. ✅ 接受任意文件路径无策略检查或限制

### 🔧 技术变更

**write_file.py**
- 新增敏感路径模式检测（Windows/Unix）
- 新增敏感文件类型检测
- 新增可执行脚本扩展名检测
- 所有写入函数添加安全检查逻辑
- 新增 `--force` 命令行参数

**文档结构**
- 在 SKILL.md 和 README.md 中添加安全警告部分
- 更新版本历史
- 所有文件版本号更新到 1.3.0

### ⚠️ 兼容性说明

- ✅ 向后兼容：保持原有 API 和命令行参数
- ✅ 新增功能为可选项（`--force` 参数）
- ✅ 默认行为更安全，不影响现有工作流

### 📖 使用示例

```bash
# 正常写入（遇到敏感路径会中止）
python write_file.py "test.txt" "content"

# 写入敏感路径（需要 --force）
python write_file.py "C:\Windows\test.txt" "content" --force

# 覆盖现有文件（会输出警告）
python write_file.py "existing.txt" "new content"
```

## [1.2.0] - 2026-03-09

- 重命名为 enterprise-file-writer
- 澄清功能描述

## [1.1.0] - 2026-03-09

- 新增 .docx 和 .xlsx 写入支持

## [1.0.0] - 2026-03-08

- 初始版本
- 支持文本/代码/配置文件写入
- UTF-8 编码保护
