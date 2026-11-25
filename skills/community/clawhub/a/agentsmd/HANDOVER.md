# 项目交接

## 当前目标与用户决定

- 2026-11-08：用户决定为本项目开启多 Agent 交接模式（`.agent-handoff.json` enabled=true）。
- 任务：为 Flitnut（飞栗 AI）公众号写长文投稿推荐 agentsmd skill；读者定位 AI 编程工具用户；交付 Markdown 稿 + 公众号排版 HTML。
- 2026-11-09：用户指出稿件此前未投到任何位置；已按 project-handoff-skill 的投稿目录惯例归档至 `docs/articles/`。
- 2026-11-09：用户决定写作类事项（标题终选、排版风格、配图、发布跟进等）不在本项目处理；稿件产物原地保留不再跟进，后续写作在他处进行。
- 2026-11-09：用户决定把 skill 收录进主流 Skills Hub（official Hermes/Nous、lobehub、skills.sh、clawhub）；browse.sh 核实定位不符（只收网站自动化技能）跳过；发布全程带 GitHub 仓库与 kelegele.com 引流；接受 ClawHub MIT-0 条款。
- 2026-11-09：用户决定 skill 包与 README 全面英文默认，中文参考译文收 `docs/zh-CN/`；frontmatter `description` 双语（英文主句 + 中文触发短语）；随即发 v1.5.2 并重推 ClawHub、同步 Hermes PR。规范已写入项目 AGENTS.md。

## 当前任务、状态和记录入口

- 公众号长文投稿稿：`docs/articles/2026-11-09-flitnut-wechat-article.md`（含投稿头注释、3 个备选标题、摘要、正文约 3300 字、配图建议；目录惯例对齐 project-handoff-skill 同系列投稿）
- 公众号 HTML（notion 风，已过静态检查，可直接全选复制粘贴公众号后台）：`docs/articles/2026-11-09-flitnut-wechat-article-notion.html`
- 已提交内容仓 inbox（2026-11-09 01:06，commit 5d85160）：`kelegele/flitnut.ai` → `Topics/inbox/20261109-0106-agentsmd-wechat-article.md`（全文自包含，待 harvest-topics 加工/发布流程跟进）
- 规则固化（2026-11-09，用户批准）：AGENTS.md Gotchas 新增「对外交付类指令落点不明先查 env/惯例/问用户，不得默默降级」；memory `delivery-instruction-clarify-target` 已在库并索引
- 交接模式搭建：`scripts/agent_hook.py`（冒烟测试通过）、`.zcode/config.json`（--agent ZCode，python3=/usr/local/bin/python3）、`AGENTS.md` 已并入「多 Agent 交接」规则
- README 特性升格（2026-11-09，用户批准）：记忆同步卖点（表格末行 + 七事⑥ + FAQ personal agent 条目）；CHANGELOG 加 Unreleased 条目；README 仓库结构加注
- 真正的投稿动作：粘贴公众号后台仍需用户执行（agent 无法操作后台）
- work 场景归集放宽（2026-11-18，用户批准）：SKILL.md v1.5.2→v1.6.0，三桶 `docs/ data/ references/` 降为 coding 缺省，work 可按类型自定顶层子文件夹（优先沿用既有惯例；批准后把归档约定写入 AGENTS.md 固化）；README 四处、zh-CN 双语、CHANGELOG 同步；本地安装副本 ~/.agents/skills/agentsmd 已从旧中文 v1.5.0 直接覆盖为仓库最新版（v1.6.0）；已 commit 未 push/发版，ClawHub/LobeHub/skills.sh 随下次发版流程同步
- Skills Hub 收录（2026-11-09，任务记录 docs/execution/agent-runs/ZCode-df77f481ba25efc238e6/handover.md）：
  - skills.sh 已收录（此前自动上榜）：https://www.skills.sh/kelegele/agentsmd-skill
  - ClawHub 已公开 agentsmd@1.5.1：https://clawhub.ai/kelegele/agentsmd（MIT-0，同步出现在 Hermes 市场 clawhub/ 来源）
  - Hermes 官方 Hub PR 待审核：NousResearch/hermes-agent#151512（optional-skills/software-development/agentsmd，英文版，已 align 上游 v1.5.2）
  - v1.5.2 已发版（英文默认 + 双语 description；release v1.5.2；ClawHub v1.5.2 过审后自动切 latest）
  - LobeHub 已上架：https://lobehub.com/skills/kelegele-agentsmd-skill （v1.5.2，标识锚定 GitHub 仓库）

## 未完成事项与下一步

- [x] 交接基础设施已纳入 git（2026-11-09 用户批准后提交；`.v2c/`、`.video_agent/`、`out/`、`*.lock` 已 gitignore，README 仓库结构已加注）
- Codex / QwenWork 钩子配置未安装（本会话仅确认使用 ZCode），需要时按模板补
- 自动记录需新会话真实验证：本会话（2026-11-09 启动检查已完成，历史 2 条）结束时检查 `docs/execution/agent-runs/` 是否新增记录
- 文章发布后：在本文件登记发布日期与标题终选
- LobeHub ✅ 已完成（2026-11-09）：市场自动抓取入库后 `lhm skill claim kelegele-agentsmd-skill` 认领 + CLI 推 v1.5.2；卡片 https://lobehub.com/skills/kelegele-agentsmd-skill 。README 安装链接已改为该 URL（随下次发版进包）。无「新建技能」网页入口，/publish 不存在
- ClawHub v1.5.2 提交后偶发需人工复核：过审后卡片 latest 应显示 1.5.2（双语 description），未切换则查 /dashboard 扫描状态
- Hermes PR #151512 有结果后：登记 merge 或被拒原因；被拒则评估改投（如社区推广渠道）
- 后续版本发布时：ClawHub（clawhub skill publish）、LobeHub（lhm skill publish，创建后可用）、skills.sh（随 GitHub 自动）三处随 CHANGELOG 同步升级
