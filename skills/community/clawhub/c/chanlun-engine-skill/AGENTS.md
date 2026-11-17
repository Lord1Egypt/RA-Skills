# chanlun-engine-skill

本仓库是一个 Agent Skill：用确定性脚本计算 A 股缠论结构（分型/笔/线段/中枢/买卖点/背驰），
输出四态操作判定（买入候选/持有/卖出减仓/等待观察）与失效价位。

**规则入口：读 [SKILL.md](SKILL.md) 并严格遵守其中的硬性禁令与新手引导流程。**
核心纪律：脚本算一切结构与判定，你只解读转述；禁止自己看K线心算缠论。

常用命令（在仓库根目录）：

```bash
python scripts/setup_env.py --recommended        # 环境自检+装免费行情源
python scripts/get_data.py --symbol 600519 --out k.csv   # 取日K(自动选数据源)
python scripts/chan_engine.py --symbol 600519.SH --csv k.csv   # 结构+判定 JSON
```

Codex 用户安装为技能：把本仓库放入 `.agents/skills/chanlun-engine-skill/`（项目级）
或 `~/.agents/skills/chanlun-engine-skill/`（用户级），或用 `$skill-installer install <本仓库URL>`。
