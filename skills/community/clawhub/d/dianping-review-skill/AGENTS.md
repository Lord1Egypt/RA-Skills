# dianping-review-skill · 开发须知

> 本文件是运行时配置真源（每次开发会话都会重新加载）。Claude Code 用户见 CLAUDE.md 指针；
> Cursor / Codex / CodeBuddy 等直接读本文件。写给在本目录里干活的 Agent，不是项目说明书。

## 30 秒速览

- **产品**：大众点评评价/探店笔记写作 Skill（免费版，MIT-0）。终端用户 clone 后 symlink 进
  `~/.claude/skills/` 使用，不以本目录为 cwd 工作——本文件的读者基本只有开发会话。
- **技术栈**：纯 Python 3 标准库；Pillow 仅合成首图时用，可选。
- **运行时依赖**：hekouwang-writer-skill >= 1.1.0。`scripts/writer_bridge.py` 用子进程调它四个脚本的 `--json` 输出；它的 JSON 字段改了，这里要同步改。
- **新代码放哪**：确定性逻辑 → `scripts/`；写法规范 → `references/`；给模型的指令 → `SKILL.md`；回归 → `tests/`。

## 工作风格

- 先读后写：改任何文件前先通读它。
- 一次改一类、每类可回退；改完重跑测试，再动下一类。

## 跨会话记忆

- 任务前读 MEMORY.md，任务后写回新发现；宿主有自己的记忆机制时以它为准。
  长期约定进记忆文件，别堆在本文件。

## 铁律（改一边，必须同步另一边）

1. **`SKILL.md`「铁律」、`scripts/content_gate.py` 的 block 项、`references/style.md` 是同一份规矩的三处实现。**
   加/改一条拦截，三处一起改，并在 `tests/test_content_gate.py` 补对应用例。这是本项目最容易裂、
   且没有任何机械手段能发现的缝。
2. **不改用户评分、不编数字**：`test_content_gate.py` 有对应用例，别绕过。
3. **改完必跑** `python3 -m unittest discover -s tests`，挂了不提交。
4. **改了 `SKILL.md` frontmatter（description/结构）**：重跑 skill-doctor 的 `check.py`——
   description 是触发命脉，写不准等于 skill 永远不被唤醒。
5. **发布包默认输出 `./dist/<店名>-发布/`**，`dist/` 已在 .gitignore；别再改回 `~/Downloads`。

### Do NOT

- 不把 Pillow 提成硬依赖：写作和内容检查路径必须纯标准库。
- 不把 hekouwang-writer-skill 的脚本复制进本仓库：依赖它，不 fork 它，规则只在那边维护。
- 不给门禁加跳过写作规范的开关：依赖缺失就拦。
- 不提交 `dist/`、`__pycache__/`（.gitignore 已兜住，别 `git add -f`）。
- 不在 SKILL.md 教通用写法：只装模型推不出来的项目/平台私有事实。

## 关键事实表

| 事实 | 值 |
|---|---|
| 版本 | 1.2.0（CHANGELOG 与 SKILL.md frontmatter 同步改） |
| Python | 3.8+（`content_gate.py` 用了海象运算符） |
| 单测 | `python3 -m unittest discover -s tests`（写作规范相关用例需要 hekouwang-writer-skill 在同级目录或 `HEKOUWANG_WRITER_SKILL_DIR`；首图用例需要 Pillow） |
| 分发 | GitHub Pages（`docs/`）+ SkillHub（frontmatter 的 slug/displayName/summary 等字段是给它要的，运行时不用读） |

## 目录结构

见 README「目录结构」一节，不在这里重复。

## 延伸文档（用到再读）

- `references/style.md` / `templates.md` / `playbook.md` / `category_rules.json`：写法规范与品类规则
- `docs/`：GitHub Pages 主页
- `README.md` / `CHANGELOG.md`：面向人与维护者的说明

## 规划中功能（尚未落地，别假设已存在）

- Pro 版能力（Mac 代发、发布后复盘、经验库持续更新）不在本仓库；免费版口径见 SKILL.md「两件事」一节。
