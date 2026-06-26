<div align="center">

# 🍜 干饭.skill

> *"中午吃什么？晚上吃什么？—— 人类两大未解之谜"*

[License: MIT](LICENSE)
[Node.js](https://nodejs.org)
[Claude Code](https://claude.ai/code)

每天在工位上发呆 10 分钟想中午吃什么？  

开会开到 6 点，脑袋空空不知道晚上吃啥？  

好不容易想好了，到店发现排队 30 分钟？  

**装上这个 Skill，AI 饭搭子每天准时提醒，帮你 3 秒做决定。**

[安装](#-30-秒上手) · [使用](#-命令列表) · [定时提醒](#-定时提醒饭点自动推送) · [贡献](CONTRIBUTING.md)

[English](README_EN.md)

</div>

---

## ✨ 一句话介绍

装上 → 说"今天吃什么" → AI 先帮你选品类，再帮你找餐馆 → 你说"行"就去吃。

**不需要提前建餐馆库**，空库也能用——AI 自带美食知识，随机帮你选吃什么。有餐馆库推荐更精准，没有也不影响。

```
你：今天吃什么？

🎲 骰子在空中翻转...... 落地！

   🎯 今天的命运之味是——火锅！

   🍲 推荐点法：
     • 锅底：鸳鸯锅（一半番茄一半麻辣）
     • 必涮：毛肚、鸭肠、嫩牛肉、豆腐
     • 预算：人均 ¥60-80

   📍 你附近的火锅店：
     1️⃣ 海底捞（望京店）| 💰 ¥95 | 500m
     2️⃣ 小龙坎（来广营店）| 💰 ¥75 | 800m

犹豫就会败北，果断就能吃饱！
```

## 🚀 30 秒上手

### 方式一：复制粘贴（任何 AI 工具）

1. 复制 `[SKILL.md](SKILL.md)` 内容
2. 粘贴到 ChatGPT / Claude / 任何 AI 对话
3. 说：**今天吃什么？**

> 首次使用时 AI 会先聊几句了解你的口味、位置和预算，之后就能直接推荐了。不建餐馆库也能用。

### 方式二：安装到 AI 工具

**Claude Code：**

```bash
git clone https://github.com/funAgent/eat-skill.git ~/.claude/skills/eat-skill
cd ~/.claude/skills/eat-skill && npm install
```

**Cursor：**

```bash
git clone https://github.com/funAgent/eat-skill.git .cursor/skills/eat-skill
cd .cursor/skills/eat-skill && npm install
```

**OpenClaw：**

```bash
npx clawhub install eat-skill
```

### 方式三：我就想试试

直接在终端跑：

```bash
git clone https://github.com/funAgent/eat-skill.git
cd eat-skill && npm install
node schedule/nudge.mjs
```

## 🎮 命令列表

### 核心命令


| 命令              | 干什么        | 也可以直接说         |
| --------------- | ---------- | -------------- |
| `/eat`          | 看所有命令      | —              |
| `/eat-select`   | 帮你选今天吃什么   | "今天吃什么"        |
| `/eat-random`   | 骰子随机选      | "随便"、"别让我选了"   |
| `/eat-discover` | 搜附近餐馆      | "附近有什么吃的"      |
| `/eat-create`   | 创建餐馆 Skill | "帮我做个餐馆 Skill" |
| `/eat-navigate` | 怎么去那家店     | "怎么去眉州东坡"      |
| `/eat-pk`       | 两家店 PK     | "XX和YY哪个好"     |
| `/eat-list`     | 查看餐馆库      | "都有什么店"        |
| `/eat-nope`     | 换一个        | "这个不要"         |
| `/eat-review`   | 吃完评价       | "吃完了"          |


### 场景模式（这才好玩）


| 命令           | 场景      | 效果               |
| ------------ | ------- | ---------------- |
| `/eat-boss`  | 🤑 老板请客 | 推好的，难得有人请        |
| `/eat-broke` | 😭 月底吃土 | 严控预算，极限省钱        |
| `/eat-diet`  | 🥗 减肥中  | 低卡选项（但会温柔劝你别太极端） |
| `/eat-solo`  | 🧑 一个人吃 | 适合独食的店，语气温暖      |
| `/eat-date`  | 💕 约会   | 氛围好 + 避坑贴士       |
| `/eat-team`  | 👥 团建   | 品类多，众口难调终结者      |


## ⏰ 定时提醒（饭点自动推送）

**装上就自动开启**，到点提醒你吃饭。有餐馆库推荐具体的店，没有则随机推荐美食品类。

### 默认时间表


| 提醒           | 时间    | 频率  | 默认  |
| ------------ | ----- | --- | --- |
| 🥗 午餐        | 11:50 | 工作日 | ✅ 开 |
| 🍽️ 晚餐       | 17:45 | 工作日 | ✅ 开 |
| 🥐 周末 brunch | 10:00 | 周末  | ❌ 关 |
| 🌙 深夜投喂      | 22:00 | 每天  | ❌ 关 |


### 设置定时任务

#### Claude Code（推荐）

```bash
# 午餐提醒
claude schedule "每个工作日 11:50 提醒我吃午饭" \
  --command "node schedule/nudge.mjs --meal lunch"

# 晚餐提醒
claude schedule "每个工作日 17:45 提醒我吃晚饭" \
  --command "node schedule/nudge.mjs --meal dinner"

# 深夜投喂（混沌模式 — 更离谱的推荐）
claude schedule "每天 22 点问我要不要吃宵夜" \
  --command "node schedule/nudge.mjs --meal late_night --style chaotic"
```

#### OpenClaw

安装 Skill 时自动注册（读取 `schedule/eat-schedule.json` 配置）。
在 OpenClaw 设置页调整时间和开关。

#### 系统 Crontab（通用）

```bash
crontab -e

# 加入以下行（替换实际路径）
50 11 * * 1-5  cd /path/to/eat-skill && node schedule/nudge.mjs --meal lunch
45 17 * * 1-5  cd /path/to/eat-skill && node schedule/nudge.mjs --meal dinner
```

#### 自定义偏好

编辑 `schedule/eat-schedule.json`：

```json
{
  "preferences": {
    "avoidRepeat": true,
    "avoidRepeatDays": 3,
    "maxBudget": 50,
    "excludeCategories": ["快餐"],
    "locationHint": "五道口"
  }
}
```

## 🔍 附近餐馆发现（高德地图）

内置 [高德 LBS Skill](vendor/amap-lbs-skill/)，搜附近餐馆 + 路线导航。

### 设置 API Key（免费，一次就好）

```bash
# 1. 申请：https://console.amap.com/dev/key/app（选"Web服务"）
# 2. 设置
export AMAP_WEBSERVICE_KEY="你的key"
```

免费 5000次/天，个人用随便搜。

### 搜索 + 一键生成 Skill

```bash
# 搜附近餐馆
AMAP_KEY=$AMAP_WEBSERVICE_KEY node vendor/amap-lbs-skill/scripts/poi-search.js \
  --keywords="美食" --city="北京"

# 搜索结果 → 餐馆 Skill（骨架版）
AMAP_KEY=$AMAP_WEBSERVICE_KEY node vendor/amap-lbs-skill/scripts/poi-search.js \
  --keywords="烧烤" --city="北京" \
  | node generator/poi-to-skill.mjs --outdir restaurants/

# 路线规划
AMAP_KEY=$AMAP_WEBSERVICE_KEY node vendor/amap-lbs-skill/scripts/route-planning.js \
  --type walking --origin "116.338,39.992" --destination "116.345,39.995"
```

## 🏗️ 创建你的餐馆 Skill

三种方式，选最顺手的：

### 方法 1：对 AI 说（最快）

```
/eat-create

老王烤串，望京SOHO T1楼下，晚上5点到凌晨2点，
人均60，羊肉串8块，烤鱿鱼15，露天位夏天氛围好
```

### 方法 2：高德搜 + 自动转换

```bash
AMAP_KEY=$AMAP_WEBSERVICE_KEY node vendor/amap-lbs-skill/scripts/poi-search.js \
  --keywords="老王烤串" --city="北京" \
  | node generator/poi-to-skill.mjs --outdir restaurants/
# 骨架生成，手动补推荐菜
```

### 方法 3：填模板

```bash
cp templates/restaurant-info.yaml restaurants/laowang-bbq/restaurant-info.yaml
# 编辑填写
node generator/generate.mjs -i restaurants/laowang-bbq/restaurant-info.yaml \
  -o restaurants/laowang-bbq/SKILL.md
```

## 📋 已收录餐馆


| 餐馆                                                 | 城市    | 品类  | 人均  | 状态    |
| -------------------------------------------------- | ----- | --- | --- | ----- |
| [眉州东坡（北苑华贸店）](restaurants/meizhou-dongpo-beiyuan/) | 北京·朝阳 | 川菜  | ¥69 | 🟢 完整 |


> 🙋 你常去的店呢？[贡献一家 →](CONTRIBUTING.md)

## 📁 项目结构

```
eat-skill/
├── SKILL.md                         # 核心 Skill（加载这个就能用）
├── package.json
├── user-profile.json                # 用户画像（首次使用时 AI 自动生成）
│
├── schedule/                        # ⏰ 定时提醒
│   ├── nudge.mjs                    # 饭点提醒脚本（趣味消息+随机推荐）
│   └── eat-schedule.json            # 提醒配置（时间、偏好）
│
├── generator/                       # 🏗️ 餐馆 Skill 生成
│   ├── generate.mjs                 # 从 YAML/JSON 生成 SKILL.md
│   ├── poi-to-skill.mjs             # 高德 POI → 餐馆 SKILL.md 转换
│   └── skill-template.md            # 生成模板
│
├── vendor/
│   └── amap-lbs-skill/              # 🗺️ 高德 LBS Skill（POI/路线/地图）
│
├── templates/
│   ├── restaurant-info.yaml         # 餐馆信息填写模板
│   └── user-profile.example.json    # 用户画像示例
│
├── restaurants/                     # 🍽️ 社区餐馆集合（可选）
│   ├── README.md
│   └── meizhou-dongpo-beiyuan/
│
├── CONTRIBUTING.md
└── LICENSE
```

## 🧬 设计理念


| 原则       | 说明                    |
| -------- | --------------------- |
| **果断优先** | 宁可推错也不让你继续纠结          |
| **到点提醒** | 不用你问，饭点自动推            |
| **有趣味性** | 骰子、转盘、毒舌文案，每天不重样      |
| **可组合**  | 高德 Skill 搞定地图，我们搞定决策  |
| **社区驱动** | 越多人贡献餐馆，推荐越好          |
| **工具无关** | Markdown 文件，任何 AI 都能用 |


## 🎯 灵感


| 项目                                                                    | 启发了什么               |
| --------------------------------------------------------------------- | ------------------- |
| [金谷园饺子馆 Skill](https://github.com/JinGuYuan/jinguyuan-dumpling-skill) | 一家餐馆也能有自己的 AI Skill |
| [同事.skill](https://github.com/titanwings/colleague-skill)             | 人格化 Skill 的先行者      |
| [高德 LBS Skill](https://github.com/AMap-Web/amap-lbs-skill)            | 地图能力不用自己写           |


## 🤝 参与贡献

**最简单的贡献：把你常去的餐馆变成 Skill 提个 PR。**

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## License

[MIT](LICENSE) — 随便用，吃好喝好。

