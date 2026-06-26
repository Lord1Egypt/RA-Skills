# Skill 抽取指南

将高价值经验抽取为独立可复用 skill 的完整流程。

## 抽取判定标准

满足以下任一条件即可视为可抽取：

| 标准 | 说明 |
|------|------|
| **Recurring** | 通过 `See Also` 关联到 2+ 相似问题 |
| **Verified** | 状态为 `resolved` 且修复已验证有效 |
| **Non-obvious** | 需要真实调试/排查才能发现 |
| **Broadly applicable** | 非项目特定，可跨代码库复用 |
| **User-flagged** | 用户明确说"把这个保存成 skill" |

## 抽取触发信号

**在对话中：**
- "把这个保存成一个 skill"
- "我总是遇到这个问题"
- "这个对其他项目也有用"
- "记住这个模式"

**在经验条目中：**
- 出现多个 `See Also` 链接（重复问题）
- 高优先级且已 resolved
- 分类为 `best_practice` 且可广泛复用
- 用户反馈明确认可方案质量

## 抽取流程

### 使用辅助脚本

```bash
# 预览将要创建的内容
./scripts/extract-skill.sh skill-name --dry-run

# 执行创建
./scripts/extract-skill.sh skill-name
```

### 手动创建

1. 创建 `skills/<skill-name>/SKILL.md`
2. 使用 `assets/SKILL-TEMPLATE.md` 模板
3. 遵循 [Agent Skills 规范](https://agentskills.io/specification)：
   - YAML frontmatter 至少含 `name` 和 `description`
   - name 必须与目录名一致
   - skill 目录内不要放 README.md

### 创建后

1. **定制 SKILL.md**：将模板替换为实际经验内容
2. **更新原经验**：状态改为 `promoted_to_skill`，补充 `Skill-Path`
3. **验证**：在新会话读取该 skill，确认其可独立理解

## Skill 质量门槛

抽取前检查：

- [ ] 方案已测试并可运行
- [ ] 脱离原上下文也能理解描述
- [ ] 代码示例可独立运行/阅读
- [ ] 不含项目特定硬编码值
- [ ] 命名符合规范（小写+连字符）

## 命名规范

- **Skill 名称**：全小写，单词间使用连字符
  - Good: `docker-m1-fixes`, `api-timeout-patterns`
  - Bad: `Docker_M1_Fixes`, `APITimeoutPatterns`

- **Description**：以动作动词开头，明确触发条件
  - Good: "Handles Docker build failures on Apple Silicon. Use when builds fail with platform mismatch."
  - Bad: "Docker stuff"

- **文件结构**：
  - `SKILL.md` - 必填，主文档
  - `scripts/` - 可选，可执行代码
  - `references/` - 可选，详细文档
  - `assets/` - 可选，模板资源
