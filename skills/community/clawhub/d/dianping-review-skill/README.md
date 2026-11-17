# dianping-review-skill · 大众点评评价助手（免费版）

**把你刚拍的店铺照片和一句话口述，整理成一条真实、不编造、别人愿意看完的大众点评评价或探店笔记。**
写完还能把照片按上传顺序编号、文案存成文件，你在点评 App 里照着发就行。写作只需要 Python 3 和 [hekouwang-writer-skill](https://github.com/huiyonghkw/hekouwang-writer-skill)（内容检查按它的写作规范把关）；合成带标题的首图时再装 Pillow。

主页：[huiyonghkw.github.io/dianping-review-skill](https://huiyonghkw.github.io/dianping-review-skill/) · 公众号：会勇禾口王的AI笔记

## 适合谁

| 适合 | 不适合 |
|---|---|
| 吃完、玩完想发点评，但懒得组织文字的普通用户 | 商家后台、门店主页、团购、推广通等商家运营 |
| 想让评价有信息量（价格、时长、避雷），被更多人看到 | 刷好评、代写虚假评价、冒充顾客 |
| 同一家店既想发评价、又想发笔记，且两篇不重复 | 美团、小红书等其他平台的文案 |

## 它做两件事

| 你说 | 它做 | 你拿到 |
|---|---|---|
| 「刚吃完帮我写个点评」「把这几张图整理成笔记」 | **写** | 可直接复制的正文、标签、首图文字、图片顺序；评价带星级，笔记带标题 |
| 「帮我整理好，我自己发」 | **整理手动发布包** | `./dist/<店名>-发布/` 下的带标题首图、按上传顺序编号的原图、`文案.txt` |

## 一次完整的流程

1. **问一次**：只问缺的几项（店名、人均、最满意和最想吐槽的点、和谁去、几星），一次问完，整理成**事实卡**。
2. **定类型**：评价写给「已经想去、在做决定的人」，笔记写给「还在找去处的人」。两篇都要时，开头卖点不能重复。
3. **按品类写**：每个品类有读者最关心的必写项，缺了会提醒。
4. **过内容检查**：正文里每个数字都要在事实卡里找得到；拦截极限词、站外联系方式、网感堆砌词。
5. **整理发布包**（你要时）：先合成一张带标题的首图（白字写 `<地点 · 名称>`，下面几行只写事实卡里有的），再把原图编号、文案存文件，你在 App 里手动发。

## 支持的品类

| 品类 | 例子 | 必写项（缺了会提醒） |
|---|---|---|
| 餐饮 | 火锅、烧烤、日料、咖啡、茶饮、甜品 | 价格、口感或味道、排队或位置 |
| 亲子体验 | 遛娃、陶艺、手工 DIY、研学、农场、科技馆 | 适合年龄或人群、费用、时长或节奏、交通或停车、配套（吃饭/休息/厕所） |
| 美容美发 | 美甲、理发、烫染、皮肤管理、SPA | 价格、是否推销、时长或预约 |
| 休闲娱乐 | 密室、剧本杀、骑行、露营、景点、公园 | 价格、时长、预约或人数 |
| 酒店民宿 | 酒店、民宿、客栈 | 隔音、水压或卫浴、早餐、位置或交通 |

规则在 [references/category_rules.json](references/category_rules.json)，可以自己加品类。

## 快速开始

装进 Claude Code、Cursor、Codebuddy 等支持 Skill 的 AI 工具：

```bash
git clone https://github.com/huiyonghkw/dianping-review-skill.git
git clone https://github.com/huiyonghkw/hekouwang-writer-skill.git
ln -s "$PWD/dianping-review-skill" ~/.claude/skills/dianping-review-skill
ln -s "$PWD/hekouwang-writer-skill" ~/.claude/skills/hekouwang-writer-skill
```

ClawHub 用户：`clawhub install dianping-review-skill && clawhub install hekouwang-writer-skill`。

然后把照片发给 AI，说「帮我写个点评」。内容检查依赖 hekouwang-writer-skill（>= 1.1.0），没装会直接拦下并提示安装；除此之外只要 Python 3。要合成带标题的首图时，再装一次 Pillow：

```bash
python3 -m pip install pillow
```

## 它怎么保证内容是真的

| 环节 | 做法 |
|---|---|
| 收集 | 一轮访谈 + 照片识别，整理成**事实卡**：只有你说过的、照片里看得到的 |
| 生成 | 评价写给「在做决定的人」，笔记写给「在找灵感的人」，结构、字数和开头卖点各不相同 |
| 内容检查 | 正文里**每个数字都必须在事实卡里找得到**；正文人均必须和人均栏一致；拦截广告法极限词、站外导流、网感堆砌词、AI 套话、硬推销和商家口吻；提醒品类必写项、行动信息和不适合谁 |
| 写法 | 用「点什么、几点去、怎么去、适合和不适合谁」带读者去消费，不喊口号；交付前按 [references/style.md](references/style.md) 去 AI 味自查 |
| 照片 | 首图叠上标题和几行事实，方便在信息流里被看懂；拍到手机号、二维码的必须删；拍到陌生人或别家孩子正脸的标出来，由你决定 |

## 免费版和 Pro 的区别

| 能力 | 免费版 | Pro |
|---|---|---|
| 写评价和笔记、内容检查、品类必写项 | ✅ | ✅ |
| 手动发布包：照片编号 + 文案文件 | ✅ 任何系统 | ✅ |
| 带标题的首图（需 Pillow） | ✅ | ✅ |
| 写作经验库 | 基础版 | 持续更新版：带真实复盘数据和证据 |
| 手机交接：iCloud 相册 + 备忘录文案，发完一条命令清理 | — | ✅ macOS |
| 通过 Mac 微信小程序代发：搜店核对、填写、预览确认、核对是否发出 | — | ✅ macOS |
| 复盘：发布 3 天后采集浏览、点赞、评论，经验回写 | — | ✅ macOS |

两个版本的 Skill 名都是 `dianping-review-skill`，升级时把整个文件夹换成 Pro 即可。
Pro 版 ¥49（含一年更新），购买方式见[主页「Pro」一节](https://huiyonghkw.github.io/dianping-review-skill/#buy)，或关注公众号「会勇禾口王的AI笔记」。

## 目录结构

```
├── SKILL.md                  # 给 AI 的指令：两件事怎么选、铁律、写作流程
├── references/
│   ├── templates.md          # 分品类正文骨架、行动段、笔记骨架、极限词替换、差评写法
│   ├── style.md              # 引导消费与去 AI 味的写法、改写自查
│   ├── category_rules.json   # 各品类读者最关心的必写信息
│   └── playbook.md           # 写作经验（基础版）
├── scripts/
│   ├── content_gate.py       # 内容检查
│   ├── manual_package.py     # 手动发布包：内容检查 + 首图叠字 + 照片编号 + 文案
│   ├── cover_card.py         # 首图：3:4 拼图，白字标题，浅黄事实行
│   └── textmatch.py          # 文本容错匹配
├── tests/                    # python3 -m unittest discover -s tests
├── dist/                     # 发布包交付物（manual_package.py 默认输出这里，已 gitignore）
└── docs/                     # GitHub Pages 主页
```

## 红线

1. 只写你说过的和照片里看得到的，不编数字、不编感受。
2. 不改你的评价：你说「一般」就写「一般」，可以写得更具体，不会改成夸奖；星级必须是你自己给的分。
3. 不代写虚假好评，不刷评，不冒充顾客，不帮商家写好评。
4. 不用广告法极限词，不留手机号、微信号、二维码等站外联系方式。
5. 差评只写事实和感受，不攻击商家。
6. 不承诺流量、优质评价或审核通过。

## 依赖

- [hekouwang-writer-skill](https://github.com/huiyonghkw/hekouwang-writer-skill)（>= 1.1.0，必装）：中文文档写作规范。内容检查调用它的锯末词、长句、敏感信息、算术对账规则，点评正文同时要过它的规范。点评以外的文档（办事指南、方案、报告、邮件、长篇攻略）也交给它。

## License

[MIT-0](LICENSE)：随便用、随便改、可商用，不需要署名。
