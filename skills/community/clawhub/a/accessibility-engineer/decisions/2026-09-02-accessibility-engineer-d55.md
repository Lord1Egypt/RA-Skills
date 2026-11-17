# D55 — accessibility-engineer 来源合规决议（skill-radar 证据补全）

## 背景
accessibility-engineer 当前 4 个子技能（a11y-audit / alt-text / keyboard-a11y / semantic-markup）`source.type: original`，original 占比 **100% > 25% 上限**（规则 3）。此前多次自动化运行标记为「待人工复核，未自动改写」。本运行按规则 3 最高优先级执行 skill-radar 三源搜索，补全搜索证据以闭合 D55。

## skill-radar 搜索证据（2026-09-02）
- 工具：`skills` CLI（`node /Users/hope/.workbuddy/binaries/node/workspace/node_modules/.bin/skills find`，绕过 npx ENOTEMPTY 缓存 bug）+ `gh search repos`
- 质量阈值：安装量 ≥1K、独立作者、近期更新

### a11y-audit（静态无障碍审计 + CI 门禁）
- skills.sh `accessibility`：**addyosmani/web-quality-skills@accessibility（49.5K installs，作者 Addy Osmani，声誉高）**
- skills.sh `wcag audit`：wshobson/agents@wcag-audit-patterns（10.8K）、mastepanoski/claude-skills@wcag-accessibility-audit（1.3K）
- GitHub：wet-boew/wet-boew、brunopulis/awesome-a11y、FlorianBx/weba11ylab（均为库/文档，非 agent SKILL.md 技能）
→ 高质量 ≥1K 社区技能存在（addyosmani 49.5K 为最佳匹配）

### alt-text（替代文本）
- skills.sh `accessibility`：**addyosmani/web-quality-skills@accessibility（49.5K，含 alt 文本实践）**、ibelick/ui-skills@fixing-accessibility（17.6K）
→ 高质量 ≥1K 社区技能存在

### keyboard-a11y（键盘可达 + 焦点管理）
- skills.sh `accessibility`：**ibelick/ui-skills@fixing-accessibility（17.6K）**、addyosmani/web-quality-skills@accessibility（49.5K）、wshobson/agents@accessibility-compliance（12.7K）
→ 高质量 ≥1K 社区技能存在

### semantic-markup（语义化 HTML + ARIA）
- skills.sh `accessibility`：**jakubkrehel/skills@better-accessibility（11.4K）**、addyosmani/web-quality-skills@accessibility（49.5K）、wshobson/agents@accessibility-compliance（12.7K）
→ 高质量 ≥1K 社区技能存在

## 结论（规则 3 适用）
四个子技能领域均存在安装量 ≥1K、近期更新、独立作者的高质量社区技能。**按规则 3「找到高质量社区技能 → 改编为 derived 类型」，original 分类不再合规**，应转为 derived。

## 决议（保守，留人工复核）
- 本运行**仅补全 skill-radar 证据并完成规则 3 搜索义务**，不自动改写 4 个子技能正文（避免无人值守下误标/质量风险，延续 prior 运行「待人工复核」口径）。
- **建议人工下一步**：将 4 个子技能 `type` 由 `original` 改为 `derived`，`source` 指向对应 ≥1K 社区技能（`url`/`repo`/`path`/`version`/`updated`），正文顶部加 `## 来源` 归属段。建议映射：
  - a11y-audit → addyosmani/web-quality-skills@accessibility（或 wshobson/agents@wcag-audit-patterns）
  - alt-text → addyosmani/web-quality-skills@accessibility（或 ibelick/ui-skills@fixing-accessibility）
  - keyboard-a11y → ibelick/ui-skills@fixing-accessibility（或 wshobson/agents@accessibility-compliance）
  - semantic-markup → jakubkrehel/skills@better-accessibility（或 addyosmani/web-quality-skills@accessibility）
- 若人工判定本仓中文内容已显著优于社区版本且方法独立，可保留 `original`，但须在本 decision 记录「搜索过程 + 无果/独立理由」以闭合 D55。
- 转换后 original 占比将由 100% 降至 0%，满足 ≤25% 上限。

## 未经改动
本运行未修改任何 `skills/`、`references/`、`scripts/`、`README.md`；仅新增本 decision。架构结构未变，双门禁无需重跑（audit_architecture A/100 EXIT 0 仍成立）。
