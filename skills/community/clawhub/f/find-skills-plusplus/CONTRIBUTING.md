# 贡献指南（CONTRIBUTING）

感谢你考虑为 **find-skills++** 做贡献。本仓库定位为「find-skills 的社区优化版」，欢迎在**不破坏署名与许可证边界**的前提下提交改进。

## 仓库底线（必读）

- 本仓库派生自 `vercel-labs/skills` 的 `find-skills`。**任何 PR 都不得删除顶部「派生自 vercel-labs/skills」的署名声明**，也不得宣称自己是官方替代品。
- 引用 `sandbaseai/workbuddy-skill` 的"脚本化安全审查"思路时，须保持"独立自研、非复制"的标注。
- 新增代码（脚本、文档）以 MIT-0 提供；上游代码权利归属上游，本仓库不做主张。

## 你可以贡献什么

1. **扩充离线注册表 `registry.json`**：把你在生态里验证过的好技能加入（见下方格式）。这是本项目相对竞品的核心差异点。
2. **改进 `scripts/security_scan.py` 的信号与误报控制**：新增危险模式识别，或降低误报。
3. **新增 CLI 子命令 / 推荐维度**：质量评级、语义匹配、冗余检测等（见 Roadmap）。
4. **修 bug、补文档、补测试**。

## 开发约定

- **零依赖**：`scripts/` 下的 Python 必须只用标准库，确保 Windows / Linux / macOS 通吃、无需 `pip install`。
- **渐进式披露**：`SKILL.md` 只放核心流程与 Quick Reference；长篇专题一律放 `references/`（`security.md` / `cli.md` / `ranking.md` / `enhancements.md` / `roadmap.md`），并在 SKILL.md 末尾用表格链接。目标：SKILL.md 控制在 ~200 行内。
- **frontmatter 规范**：必须含 `name` / `description` / `version`（语义化）/ `author` / `license` / `keywords`，以及 `metadata:` 块（`slug` / `displayName` / `category`）。改动行为时同步 bump `version`。
- **市场卡片**：行为或风险面变化时需同步更新 `market-card.md` 的 Known Risks and Mitigations。
- **新信号必须配测试**：往 `scripts/security_scan.py` 加任何检测项，都要在 `tests/` 里补「恶意样本命中 + 正常样本不误报」两个用例。
- **自查用 `--exclude-tests`**：`tests/` 内含大量恶意样本夹具，直接 `scan --path .` 会把自己判成 EXTREME。CI 已按此配置。审查**第三方**技能时绝不加该参数（payload 可能藏在测试目录）。
- **必须带测试**：改动 `security_scan.py` 或排序/去重逻辑，请在 `tests/` 下补 pytest 用例，并在本地跑通：
  ```bash
  python -m pytest tests/ -q
  ```
- **Python 版本**：兼容 3.8+（不依赖新语法特性）。
- **提交信息**：中文或英文均可，说明"为什么改"而非"改了什么"。

## registry.json 格式

```json
{
  "version": 1,
  "updated": "2026-09-19",
  "skills": [
    {
      "name": "react-performance",
      "displayName": "React Performance",
      "description": "优化 React 渲染性能",
      "sources": ["native", "clawhub"],
      "bestVersion": "1.0.0",
      "updatedAt": 1780000000000,
      "downloads": 2900,
      "trust": "official",
      "repo": "https://github.com/...",
      "tags": ["react", "frontend", "performance"]
    }
  ]
}
```

- `trust` 取值：`official`（知名官方源）/ `trusted`（可信作者、安装/星标达标）/ `caution`（未知作者、低星标，需谨慎）。
- 离线注册表是**缓存与兜底**，联网时仍以实时搜索为准。

## PR 流程

1. Fork → 建分支（`feat/xxx` 或 `fix/xxx`）。
2. 本地跑通测试与 `security_scan.py` 自测。
3. 提交 PR，描述改动动机与验证方式。
4. 维护者审查署名/许可证边界后合并。

---

*find-skills++ 欢迎务实、有主见的贡献。*
