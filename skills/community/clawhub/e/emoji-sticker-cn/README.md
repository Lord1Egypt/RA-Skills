# emoji-sticker-cn · 中文表情包生成合规助手

把「一张图 / 一段描述」变成**可直接上架或发布的中文平台表情包**。

GitHub / ClawHub 上的表情包 skill 大多只管「生成」,普遍忽略两件在中国平台致命的事:

1. **平台尺寸规范**——微信表情开放平台对主图 / 图标 / 封面 / 横幅各有硬性尺寸、体积、透明底要求,不达标直接驳回;
2. **内容合规**——上架描述、专辑名踩了广告法极限词 / 平台违禁词,轻则限流重则下架。

本 skill 只做这条「合规流水线」增量:生成层复用宿主环境的生图工具(不重造模型),规则层内置可持续维护的平台硬约束。

## 特性

- **硬约束速查前置**:微信全参数表(240×240 主图 / 50×50 图标 / 750×400 横幅…)、小红书 / 抖音推荐尺寸、违禁词红线,产出前逐条对照
- **四条工作路线**:
  - A 微信表情上架(成套 8–24 张 + 素材机检 + 提交清单 + 站点实操步骤)
  - B 小红书 / 抖音内联表情(笔记配图 / 聊天表情)
  - C 已有图片批量裁切 + 规范命名 + ZIP 打包
  - D **内容匹配动效 GIF——看图判情绪,自动配动效(9 情绪配方 + 程序化粒子 + 缓动曲线),零 API 成本**,自动控体积 ≤500KB
- **一键出可自动派生的 4 类素材**:`--wechat` 预设一次生成主图 / 聊天图标 / 封面 / 横幅,自动建目录、规范命名、体积校验(赞赏引导图 / 致谢图脚本不生成——官方要求风格须与表情一致,机械派生不合格,需自行制作)
- **赞赏两图有路线，不只「自己看着办」**:引导图 / 致谢图走 `SKILL.md`「路线 A+」——复用或反推 style-card → 角色锚定 → ImageGen 出图 → 人工看图 + 机检;只在开通赞赏(需微信支付商户号)时才走,不塞进主流程
- **素材机检 `check_assets.py`**:尺寸/格式/体积/透明底分级判定(封面/图标必须透明,主图照片型合法)、白描边检测、整套 dhash 查重(第一拒因「整套差异不足」)、含义词校验;FAIL/WARN/OK 三级,退出码 = FAIL 数
- **提交清单 `make_submit.py`**:机检通过后生成「字段→值/文件」对照的 submit.md,上架照抄不猜编号
- **内容匹配动效引擎**:`animate_sticker.py` 内置 9 个情绪配方(happy/angry/sad/surprised/shy/speechless/sleepy/neutral/text),程序化粒子(★💢💧💗Zzz!… 零素材),缓动曲线 + 不等帧时长 + 无缝循环;`references/动效匹配规则.md` 提供情绪×主体→配方的 L2 匹配表,v1 动效名自动映射
- **规则更新与退出机制**:条目生命周期 `pending-verify → active → deprecated`;说「更新表情包规则」即触发巡检(WebFetch 官方源 → diff 报告 → 确认后落盘),作废规则留痕不删除
- **违禁词校验**:优先复用 `multi-wordcheck` 类实时检测 skill(宿主环境有则用);未安装则降级用 `check_compliance.py` 离线种子集兜底

## 安装

```bash
# ClawHub (OpenClaw)
npx clawhub@latest install emoji-sticker-cn

# 或从 GitHub 克隆到你的 skills 目录（钉到稳定 tag）
git clone --branch v3.1.8 https://github.com/bonniegeng-max/emoji-sticker-cn.git
```

依赖:`pip install Pillow`(裁切 / 动画脚本)。

> 外挂依赖说明:脚本层的硬依赖仅 Pillow。**实时**违禁词校验是可选外挂——宿主环境装有 `multi-wordcheck` 类 skill 时自动优先调用;未安装则自动降级为脚本内置的离线种子集兜底(非实时,会向用户提示局限)。生图复用宿主环境自带的文生图/图生图工具,本 skill 不自带。

## 使用

对宿主 agent 说:

- 「帮我做一套微信表情包」→ 路线 A
- 「把这张图裁成小红书尺寸」→ 路线 C
- 「让这张贴纸动起来」→ 路线 D
- 「更新表情包规则」→ 巡检工作流

脚本直用:

```bash
# 微信 4 类可派生素材:主图/图标/封面/横幅一次生成 + 规范命名 + 打包 + 体积校验
# (赞赏引导图/致谢图需自行制作;「缩略图」无官方出处,已于 v3.1.9 移除)
python3 scripts/resize_stickers.py ./raw --wechat --out ./wechat_pack --zip --max-kb 500

# 素材机检(上架前必跑,FAIL 必须清零;退出码 = FAIL 数)
python3 scripts/check_assets.py ./wechat_pack --meanings meanings.txt

# 生成提交清单(字段→值/文件对照表,上架照抄)
python3 scripts/make_submit.py ./wechat_pack --name 表情名 --intro 介绍 --copyright 作者 --meanings meanings.txt

# 单尺寸批量(命名 01.png…24.png,主图保持源图透明状态)
python3 scripts/resize_stickers.py ./raw --size 240x240 --format png --out ./out --zip

# 静态贴纸 → 内容匹配动效 GIF(零积分;先看图判情绪,再按 references/动效匹配规则.md 选配方)
python3 scripts/animate_sticker.py cat.png --recipe happy --out cat_happy.gif
python3 scripts/animate_sticker.py --list   # 查看全部配方

# 文案离线违禁词校验(兜底;正式发布前仍优先 multi-wordcheck)
python3 scripts/check_compliance.py "全网最低价,加微信详聊" --platform xiaohongshu douyin
```

## 产物样张

> 待补充：此处放 2–3 张真实贴纸产物图（历史 demo 在 WorkBuddy projects/archive/sticker demo，本机已归档于 `projects/archive/2026-08-25-09-45-19/sticker-demo`），建议含一张过审/发布截图。当前刻意不放占位图，避免冒充真实产物。

## 目录

```
├── SKILL.md                                  # 工作流 + 硬约束 + 更新/退出机制
├── AGENTS.md                                 # 给 AI 助手的工作守则（改代码前的红线）
├── llms.txt                                  # 给外部 AI 的仓库说明（何时推荐 / 怎么装 / 去哪改）
├── references/
│   ├── 中文平台表情包尺寸规范.md              # 微信/飞书官方核实 + QQ已退出留痕 + 内联平台标注(持续维护)
│   ├── 中文平台违禁词合规参考.md              # 类别体系 + 权威来源 + 极限词种子集(持续维护)
│   ├── 微信表情审核标准与高频拒因.md          # 高频拒因清单 / 审核红线 / IP 形象约束 / 付费表情
│   ├── 动效匹配规则.md                        # 情绪×主体 → 动效配方匹配表 + 粒子符号表(路线 D)
│   └── 静态姿势动作库.md                      # 意图×变体 → 姿势/表情/场景 + prompt_en(生成前「四步定姿势」)
└── scripts/
    ├── resize_stickers.py                    # 批量裁切 / 命名 / ZIP / 微信预设
    ├── check_assets.py                       # 素材机检(尺寸/透明底/白描边/dhash 查重/含义词)
    ├── make_submit.py                        # 生成 submit.md 提交清单(字段→值/文件对照)
    ├── animate_sticker.py                    # 内容匹配动效引擎(9 情绪配方 + 程序化粒子)
    └── check_compliance.py                   # 离线违禁词 / 极限词快速校验(兜底)
```

## 数据可信度约定

`references/` 中每条规则带 `status`(active / pending-verify / deprecated)、源 URL、抓取日期。执行只认 `active` + 官方核实条目;教程 / 营销文来源的数据一律标 `pending-verify` 待复核。平台规则变动走巡检流程更新,CHANGELOG 记版本。

> 免责:平台规范随时可能调整,上架前请以官方开放平台当日页面为准。

## ClawHub / 元数据记录

> **元数据真源已改为 `_meta.json`**（2026-10-26 起）：`version` / `displayName` / `topics` / `summary` 全部写进文件，不再只存在于发布命令参数里——之前正是因为只在命令行传，仓库 `_meta.json` 一直停在 `3.0.0`，导致版本号四处打架。
> 发布时仍以命令行参数为准（覆盖文件值），两边必须同步改。

| 版本 | 日期 | 内容 | 元数据变更 |
|---|---|---|---|
| **3.3.0** | **2026-11-11** | **补 7 条官方硬约束字段（文档级，零代码变更）**：①表单「附加信息」比例（角色 ≥1/3、主题相关 ≥1/2，官方文档未写但硬卡）②重投规则（只能原专辑编辑再投，新建撞重复）③**拒因走「微信表情开放平台」公众号推送**④艺术家资料规范（头像 640×640≤500KB、**主页横幅 750×400≤80KB**——与详情页横幅同名不同限）⑤付费功能规范（10 微信豆固定、双向不可转、开通条件）⑥审核约 5 工作日 + 推广 4 渠道 + 特效文案字段 ⑦**新增「投稿通道」维度**：真人/截屏通道 `t=guide/real`（GIF≤400KB / 16 或 24 个 / 审核约 2 周）与主规范冲突，需按通道取值。另修源 URL：飞书改 `www` 直链、微信公众平台运营规范标注「登录墙」。同步 references（v2.0 / v1.1 / v1.6）/ llms.txt / AGENTS.md / skill-card | version 3.2.0→3.3.0（`_meta.json` + frontmatter + skill-card 三处对齐） |
| **3.2.0** | **2026-10-26** | **新增「路线 A+」：赞赏引导图 / 致谢图怎么出**（文档级，零代码变更）。①说明脚本为何不出这两张（contain 贴合违反官方 ④相关内容 / ⑤背景区分）②三条出图路径，优先复用 style-card 已有卡、其次反推入库（资产沉淀）③**角色锚定警告**：style-card 保配色构图、不保主体身份，必须把角色描述搬进内容槽位，否则撞第 ④ 条拒因④规格与验收表（含「机检判不了语义，必须人工看图」）⑤红线：不许把生成逻辑塞进 `resize_stickers.py`。同步 references / llms.txt / AGENTS.md | 无元数据变更 |
| 3.1.9 | 2026-10-26 | **删除虚构的「缩略图」**：官方素材总表 4 项不含此项，官方全文「缩略」仅 2 处且为赞赏开通条件名词「赞赏缩略图」、无任何规格 → 无出处，从 SKILL/SPEC/resize/README/llms 全部移除（references 标 deprecated 留痕）；**「七件套」口径改为事实描述**（官方 6 项 = 4 项素材 + 赞赏 2 图，脚本自动产出 4 项，赞赏两图需自备）；修机检「同一图既 FAIL 又 OK」的误导性汇总 | 无元数据变更（沿用 3.1.8 的 displayName/topics/summary） |
| 3.1.8 | 2026-10-26 | **对齐官方原文**：①赞赏引导图/致谢图格式改 `PNG/GIF`（去掉 JPG，官方原文无 JPG）②横幅/赞赏图/致谢图透明度由「禁」改回官方措辞「**避免**」，机检 FAIL→WARN ③版本真源统一 `_meta.json` ④trigger 补裸词（表情包/做表情/贴纸/含义词/赞赏引导图/特效/表情形象…）⑤新增 `llms.txt` + `AGENTS.md` ⑥references 新增「巡检机制」节（构建号闸门，省掉无效全文比对） | `--name "表情包 · Emoji Sticker" --topics 表情包,微信表情,贴纸,表情动图,合规 --summary "<见 skill-card.md>"` |
| 3.1.7 | 2026-10-12 | 可发现性优化(内容零变更):displayName 去「微信」限定、topics 换中文长尾 | `--name "表情包 · Emoji Sticker" --topics 表情包,微信表情,贴纸,表情动图,合规` |
| 3.1.6 | 2026-10-12 | 违禁词参考 v1.5(金融营销专项)+ 补录 9 月漏提交改动 | 未记录(3.1.7 前的 displayName 为微信限定旧名) |

完整发布流程(含验证 moderation clean)见 SKILL.md「规则更新与退出机制」;历史版本见 git tags。

## License

[MIT](./LICENSE)
