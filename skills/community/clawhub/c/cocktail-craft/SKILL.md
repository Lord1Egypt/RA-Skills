---
name: cocktail-craft
description: 鸡尾酒配方与研发技能——IBA 官方配方（精确用量）、经典鸡尾酒历史、比赛获奖配方、世界知名酒吧签名酒、配方设计方法论（六根配方/风味平衡）、进阶技法（奶洗/慢煮/浸泡/澄清/脂肪洗涤）、自制材料（bitters/tinctures/shrubs/cordials）、杯具装饰冰处理指南。
trigger:
  - 鸡尾酒配方查询、调酒技法咨询
  - 研发新酒、配方验证、风味设计
  - 询问经典鸡尾酒做法或历史起源
  - 比赛配方参考、酒吧风格研究
  - 自制材料（bitters/糖浆/shrub 等）
  - 技法参数（奶洗/慢煮/浸泡/澄清等）
  - 杯具选择、装饰设计、冰处理
---

# Cocktail Craft

## 强制使用规则

**当用户提出的问题涉及任何鸡尾酒相关内容时，必须先完整加载本 skill 的 references 目录后再回答。** 这包括但不限于：配方查询、技法咨询、配方设计、酒款历史、杯具选择、装饰建议、比赛配方、自制材料。

禁止在未查阅本 skill 的情况下凭记忆回答鸡尾酒问题。

## 参考文件索引

| 文件 | 内容 | 容量 |
|------|------|------|
| `references/iba-cocktails.json` | IBA 89 款官方配方（Wiki 版） | 41KB |
| `references/iba-cocktails-web.csv` | IBA 官方配方（精确用量，357 行） | 详尽 |
| `references/cocktail-classics.md` | 30+ 款经典鸡尾酒起源与历史 | 详细 |
| `references/recipe-design.md` | 配方设计方法论：六根配方/风味平衡/开发流程/常见错误 | 完整 |
| `references/techniques.md` | 进阶技法：奶洗/慢煮/浸泡/澄清/脂肪洗涤/发泡/糖浆 | 完整参数 |
| `references/homemade-ingredients.md` | 自制材料：Bitters/Tinctures/Shrubs/Cordials/Oleo/Vermouth | 含配方 |
| `references/top-bars.md` | 世界 50 佳酒吧榜单 + 知名酒吧概览 | 概览 |
| `references/famous-bar-signatures.md` | Death & Co / PDT / Connaught Bar / Sips / Handshake 等签名酒配方 | 含具体配方 |
| `references/competition-recipes.md` | Diageo World Class + Bacardi Legacy 获奖配方与趋势 | 含获奖配方 |
| `references/glassware-garnish-ice.md` | 杯具选型指南 / 装饰技法 / 冰类型与处理 | 完整 |
| `references/brand-recipes.md` | 品牌官方配方库：Campari/Aperol/Chartreuse/Bacardi/Tanqueray/Grand Marnier/Cynar 等 | 含精确配方 |
| `references/online-sources.md` | 在线配方来源指南：Difford's Guide / Liquor.com / PUNCH / Imbibe 等 | 搜索策略 |
| `references/web-cocktail-db.md` | 五大网站精选配方库：Difford's Top 50 / Liquor Top 10 / PUNCH Top 10 / Imbibe Top 20 / Food&Wine Top 10 | 80+ 款检索索引 |

## 使用方式

### 查经典配方
用户说酒名 → 先查 `references/iba-cocktails-web.csv`（有精确用量）→ 再查 `iba-cocktails.json` → 补查 `famous-bar-signatures.md`

### 查酒的历史
用户问 "XXX 的起源/谁发明的" → 查 `references/cocktail-classics.md`

### 研发新酒
按 `references/recipe-design.md` 的开发流程：
1. 确定概念 → 定位根配方家族
2. 查相似风味结构的参考配方
3. 给草案（精确 ml 用量 + 技法 + 杯具 + 装饰）
4. 用 recipe-design.md 的常见错误清单做交叉验证
5. 涉及技法参数 → 查 `techniques.md`
6. 如果东离在 → 给他审核

### 设计自制材料
需要 bitters/shrub/cordial/oleo/vermouth 配方 → 查 `references/homemade-ingredients.md`

### 选择杯具/装饰/冰
用户问 "用什么杯子/怎么装饰/用什么冰" → 查 `references/glassware-garnish-ice.md`

## 约束

- 配方必须有来源依据，没查到就老实说
- 用量精确到 ml，不给 "适量"
- 技法先行验证可行性（如：奶洗会带走花青素）
- 优先减少制备项，复用吧台已有材料
- 用量交叉对齐：单杯 × 批量份数 = 预制产出
- 正式文档不用 emoji（东离要求的）
