# Fuck-ClawHub

## 目录 / Contents

- [🇨🇳 中文](#zh)
  - [一、背景](#zh-background)
  - [二、功能与意义](#zh-features)
  - [三、技术简介](#zh-tech)
  - [四、相关链接](#zh-links)
- [🇬🇧 English](#en)
  - [Background](#en-background)
  - [Features & Purpose](#en-features)
  - [Technical Overview](#en-tech)
  - [Related Links](#en-links)

---

<a id="zh"></a>
# 🇨🇳 中文

> 把 ClawHub 的链接一把薅过来，换成 [skillhub](https://skillhub.cn) 的——顺便替你骂醒那套只会砍人的审查。

[🌐 切换到 English](#en)

<a id="zh-background"></a>
## 一、背景

如果你也在 ClawHub 上被那套越来越离谱的"安全审查"折磨过，你一定熟悉这种滋味：兴冲冲写好、或好不容易扒到一个清清白白、毫无风险的 skill，点下提交，然后眼睁睁看它在某个根本看不懂技能、却手握生杀大权的审核员手里被一刀剁了。rnm

理由永远冠冕堂皇——"合规""安全""风险评估"。翻译过来就一句话：宁可错杀一千，绝不放过一个能用的。

就ClawHub这个审核强度，就相当于是用浏览器的搜索栏都是有危险的。

ClawHub 的审查，他们就不知道什么叫"安全把关"，而是一场"宁可错杀一片"的行为艺术：把一帮看不懂技能的人凑在一块儿，学着三国时期某著名曹老板，比赛谁更擅长把正常的作品摁死。审着审着，能用的全审没了，留下一地鸡毛，和一群被消音的开发者。

所以，与其跪着求审，不如另起炉灶。[skillhub](https://skillhub.cn) 就是那个不拿"合规"当遮羞布的替代品——同样做安全审计，却不会随手把正经东西埋进土里。这个 skill 存在的唯一意义，就是帮你把 ClawHub 的链接拽过来，换成 skillhub 的，顺便在 skillhub 上替你找到更靠谱的同类。

<a id="zh-features"></a>
## 二、功能与意义

- **搜得到**：想找个做某件事的 skill？它优先去 skillhub 搜，按相关度排好，挑最契合的 3–5 个递到你面前——而不是让你在 ClawHub 的严审名单外干瞪眼。
- **看得清**：每条结果都老老实实列出 **名称 / 版本号 / 作者 / 更新日期 / 简介**，装不装你说了算，不糊弄。
- **转得动**：扔给它一个 ClawHub 链接，它自动去 skillhub 找同名/同功能的替代并做对比；要是 skillhub 真没有，它会替你狠狠吐槽 ClawHub 的离谱审查，再问你要不要干脆从 ClawHub 装。

意义就一句话：把选择权还给你，而不是交给那套只会砍人的审核机器。

<a id="zh-tech"></a>
## 三、技术简介

- **数据源**：SkillHub 公开列表接口 `https://api.skillhub.cn/api/skills`（免鉴权）。通过 `keyword` 分词搜索 + `sortBy=score` 实现相关度排序。
- **执行脚本**：`scripts/search_skillhub.py`，两种模式：
  - `search "<关键词>" [--category 分类] [--limit N]` —— 搜索并格式化输出；
  - `convert "<clawhub链接>"` —— 解析 ClawHub 链接、在 skillhub 搜同名候选并判断是否匹配。
- **字段映射**：`name`→名称、`version`→版本号、`ownerName`→作者、`updated_at`（毫秒时间戳）→更新日期、`description_zh`→简介。
- **安装**：经 SkillHub CLI `skillhub install <slug> --dir <skills目录>`；WorkBuddy 用户级目录为 `~/.workbuddy/skills`。
- **触发**：当用户搜索 skill、给出 `clawhub.ai` 链接、或想绕开 ClawHub 审查时自动启用。

<a id="zh-links"></a>
## 四、相关链接

想摆脱 ClawHub 那套"刀法"？直接上 [skillhub](https://skillhub.cn) 看看——同样是技能社区，却不会拿"合规"当借口把正常技能摁死。

---

<a id="en"></a>
# 🇬🇧 English

> Yank your ClawHub link over and swap it for [skillhub](https://skillhub.cn)'s — and rip into that axe-happy review while we're at it.

[🌐 切换到中文 / Switch to Chinese](#zh)

<a id="en-background"></a>
## Background

If you've ever been ground down by ClawHub's ever-more-absurd "security review," you know the taste: you finally write — or scrape up — a perfectly clean, utterly harmless skill, hit submit, and watch it get axed by some reviewer who clearly can't tell a skill from a screenshot, yet holds your fate in their hands.

The excuse is always solemn — "compliance," "security," "risk assessment." Translated, it's one line: better safe than sorry, even if you bury a thousand innocent ones.

At ClawHub's review standards, you'd think even typing a query into a browser's search bar counts as a hazard.

ClawHub's review stopped being "security vetting" long ago. It's performance art titled "better kill them all" — a lineup of people who don't understand skills, competing to see who can squash the most legitimate work. They review and review until everything usable is gone, leaving a pile of feathers and a crowd of silenced developers.

So instead of kneeling and begging for approval, we start elsewhere. [skillhub](https://skillhub.cn) is the alternative that doesn't use "compliance" as a fig leaf — it audits for safety too, but won't casually bury decent work in the dirt. The only point of this skill is to yank your ClawHub link over, swap it for skillhub's, and find you a saner equivalent there.

<a id="en-features"></a>
## Features & Purpose

- **Findable**: Want a skill that does something? It searches skillhub first, ranks by relevance, and hands you the 3–5 best matches — instead of leaving you gaping outside ClawHub's ever-shrinking approved list.
- **Transparent**: Every result plainly lists **Name / Version / Author / Update date / Description**. Install or not, your call — no hand-waving.
- **Convertible**: Toss it a ClawHub link and it hunts skillhub for a same-name / equivalent alternative and compares them. If skillhub genuinely has none, it rips into ClawHub's absurd review for you, then asks whether you'd rather just install from ClawHub.

The point in one line: give the choice back to you, not to a machine that only knows how to swing the axe.

<a id="en-tech"></a>
## Technical Overview

- **Data source**: SkillHub's public list API `https://api.skillhub.cn/api/skills` (no auth). Tokenized `keyword` search + `sortBy=score` for relevance ranking.
- **Script**: `scripts/search_skillhub.py`, two modes:
  - `search "<keyword>" [--category cat] [--limit N]` — search and format output;
  - `convert "<clawhub link>"` — parse the ClawHub link, search skillhub for same-name candidates, judge the match.
- **Field mapping**: `name`→Name, `version`→Version, `ownerName`→Author, `updated_at` (ms timestamp)→Update date, `description_zh`→Description.
- **Install**: via SkillHub CLI `skillhub install <slug> --dir <skills dir>`; WorkBuddy user-level dir is `~/.workbuddy/skills`.
- **Trigger**: activates when the user searches for a skill, pastes a `clawhub.ai` link, or wants to dodge ClawHub's review.

<a id="en-links"></a>
## Related Links

Want to escape ClawHub's knife work? Go straight to [skillhub](https://skillhub.cn) — a skill community that, unlike ClawHub, won't use "compliance" as an excuse to squash normal skills.
