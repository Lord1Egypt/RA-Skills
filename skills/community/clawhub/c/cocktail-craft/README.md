# Cocktail Craft 🍸

给 AI Agent 用的鸡尾酒配方与研发技能包。收录 IBA 官方配方、五大网站精选、世界顶级酒吧签名酒、品牌配方库、比赛获奖配方，以及完整的技法参考和自制材料指南。

## 内容

| 文件 | 内容 |
|------|---------|
| `references/iba-cocktails-web.csv` | IBA 102 款官方配方（精确用量） |
| `references/iba-cocktails.json` | IBA 89 款配方（Wiki 完整版） |
| `references/web-cocktail-db.md` | 五大网站 80+ 款精选：Difford's Guide / Liquor.com / PUNCH / Imbibe / Food & Wine |
| `references/brand-recipes.md` | 品牌官方配方：Campari、Aperol、Chartreuse、Bacardi、Tanqueray 等 |
| `references/famous-bar-signatures.md` | 15 家世界顶级酒吧签名酒（Death & Co / PDT / Connaught / Sips / Handshake 等） |
| `references/competition-recipes.md` | Diageo World Class + Bacardi Legacy 获奖配方 |
| `references/cocktail-classics.md` | 30+ 款经典鸡尾酒起源与历史 |
| `references/recipe-design.md` | 配方设计方法论：六根配方 / 风味平衡 / 开发流程 / 常见错误 |
| `references/techniques.md` | 进阶技法：奶洗 / 慢煮 / 浸泡 / 澄清 / 脂肪洗涤 |
| `references/homemade-ingredients.md` | 自制材料：Bitters / Tinctures / Shrubs / Cordials / Oleo / Vermouth |
| `references/glassware-garnish-ice.md` | 杯具选型 / 装饰技法 / 冰处理 |
| `references/online-sources.md` | 五大鸡尾酒网站的搜索策略 |
| `references/top-bars.md` | World's 50 Best Bars 榜单与概览 |

## 一键安装

将以下内容直接发给 AI Agent（Claude Code / Codex CLI / Cursor / OpenClaw 等），Agent 将自动完成安装：

```
请安装 Cocktail Craft skill：

# 下载
curl -L -o cocktail-craft.zip https://github.com/makishimatouri/COCKTAIL/archive/refs/heads/main.zip

# 解压
unzip cocktail-craft.zip -d /tmp/cocktail-craft

# 移动到 skills 目录（按你的平台调整路径）
# OpenClaw:
mv /tmp/cocktail-craft/COCKTAIL-main ~/.openclaw/workspace/skills/cocktail-craft

# Claude Code / Cursor:
mv /tmp/cocktail-craft/COCKTAIL-main ~/.claude/skills/cocktail-craft

# Codex CLI:
mv /tmp/cocktail-craft/COCKTAIL-main ~/.codex/skills/cocktail-craft

安装完成后确认 references/ 目录下有 13 个参考文件即可。
```

或者用 ClawHub 一键安装（需要 clawhub CLI）：

```
请帮我安装 Cocktail Craft skill。

如果 ClawHub 上还没有，就从 GitHub 安装：
git clone https://github.com/makishimatouri/COCKTAIL.git ~/.openclaw/workspace/skills/cocktail-craft
```

## 用法

兼容 OpenClaw、Claude Code、Cursor、Codex CLI 等所有支持 SKILL.md 格式的 AI Agent。

把 `cocktail-craft/` 目录放到 Agent 的 skills 文件夹即可。当用户讨论鸡尾酒配方、调酒技法、酒款历史等问题时自动触发。

## 数据来源

- International Bartenders Association (IBA) 官方配方
- Campari Academy、Chartreuse Diffusion、Bacardi、Tanqueray 等品牌官网
- Difford's Guide、Liquor.com、PUNCH、Imbibe Magazine
- Diageo World Class 全球调酒师大赛
- Bacardi Legacy 全球鸡尾酒大赛
- Death & Co、PDT、Connaught Bar、Sips、Handshake Speakeasy 等世界顶级酒吧

## 许可

MIT
