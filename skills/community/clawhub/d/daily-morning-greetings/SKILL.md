---
name: daily-morning-greetings
description: This skill triggers when the user asks for a 早安问候, asks to configure a daily early-morning 早安问候, asks to manually补发一条今天的早安问候, or asks for a backup version such as “换一条” or “再来个备选版”. It generates a fixed-format daily morning message using a deterministic local context script for live weather, rotating icons, and rotating wisdom-and-blessing pairs. It supports explicit city parameters, defaults to Shanghai when no city is provided, and can configure external OpenClaw cron schedules across the current chat channel, including plugin-backed chat channels.
version: 1.0.12
compatibility: Requires python3 and network access for live weather fetch.
metadata:
  openclaw:
    emoji: "🌤️"
    requires:
      bins:
        - python3
---

# Daily Morning Greetings

这个 skill 现在走“脚本取数 + 固定模板输出”的稳定路径：

1. 先运行本地脚本，取目标城市当天上下文 JSON。
2. 直接使用脚本返回的 `formatted` 字段输出最终文案。
3. 如果实时天气没取到，要明确说明，不允许猜天气。
4. 定时标准版走本地稳定轮换；手动触发和“换一条”走本地伪随机轮换，并尽量做到同日同窗不重复。

## Supported Intents

这个 skill 需要识别 3 类中文提示词：

- 配置定时：
  - `请配置早安问候为每天早上固定6点`
  - `请配置早安问候为每天早上固定7点`
  - `请配置早安问候为每天早上7点半`
- 手动触发或补发：
  - `来一条今天的早安问候`
  - `手动补发一次今天的早安问候`
- 备选版或换一条：
  - `换一条`
  - `再来个备选版`

所有用户可见文案统一叫“早安问候”，不要再写“晨间问候”。

公开版默认定时时间是 `06:00`，但用户如果明确指定 `07:00`、`07:30` 或别的时间段，应优先按用户指定时间配置。
配置早安问候定时任务时，默认同时开启失败提醒。

## Data Sources

- 对中国城市或 `Asia/Shanghai` 场景，天气数据优先来自 `Open-Meteo`
- 其他城市默认优先来自 `wttr.in`
- 主源失败时，会自动回退到另一方数据源
- 如果只是换城市但没给经纬度，脚本会先做城市地理解析，再请求 `Open-Meteo`
- 智慧人物、短句和祝福语来自本地 `references/wisdom_pairs.json`
- 开头图标和结尾图标由脚本按日期稳定轮换

## Required Command

触发后第一步必须运行：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" --variant 0
```

如需指定城市，使用：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" \
  --variant 0 \
  --city "Beijing" \
  --city-zh "北京" \
  --timezone "Asia/Shanghai"
```

如果需要更便于程序解析，可用：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" --variant 0 --compact
```

如果是 cron 定时标准版，或需要在保留主聊天投递的同时自动补发微信 bot，优先使用包装脚本：

```bash
python3 "$SKILL_DIR/scripts/dispatch_morning_greeting.py" \
  --variant 0 \
  --deliver-weixin auto \
  --print-message
```

推荐的 cron 内联 payload 文案是：

```text
Run this command first: python3 "$SKILL_DIR/scripts/dispatch_morning_greeting.py" --variant 0 --deliver-weixin auto --print-message . Then return the stdout exactly as the final answer. Preserve blank lines. Do not read any skill or prompt file unless strictly necessary. Do not add any extra text.
```

如果是手动触发，希望当天同一窗口尽量不重复，使用：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" \
  --selection-mode manual \
  --scope-key "chat:example"
```

如果是备选版，改用非 0 的 `variant`：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" --variant 1
```

如果是“换一条 / 再来个备选版”，应优先改用：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" \
  --selection-mode alternate \
  --scope-key "chat:example"
```

如果是“手动补发一次今天的早安问候”，并希望在当前聊天正常回显的同时，自动补发到已配置的微信 bot，优先使用：

```bash
python3 "$SKILL_DIR/scripts/dispatch_morning_greeting.py" \
  --selection-mode manual \
  --scope-key "chat:example" \
  --deliver-weixin auto \
  --print-message
```

## Default Location

默认地点是上海。

如果你希望在自己的环境里长期固定成别的城市，可以设置这些环境变量：

```bash
export MORNING_WEATHER_CITY="Shanghai"
export MORNING_WEATHER_CITY_ZH="上海"
export MORNING_WEATHER_TIMEZONE="Asia/Shanghai"
export MORNING_WEATHER_LATITUDE="31.2304"
export MORNING_WEATHER_LONGITUDE="121.4737"
```

如果只是某一次调用临时换城市，优先使用命令行参数，不必改环境变量。

脚本会给出：

- 目标城市时间与日期
- 目标城市实时天气与今日预报
- 当前生成使用的 `variant`
- 当前生成使用的 `selection`
- 开头问候图标
- 天气图标
- 智慧人物、短句、关联祝福语
- 结尾温和图标
- 三段最终可直接输出的格式化文本

## Single Source Of Truth

脚本返回的 JSON 是唯一事实来源：

- `location`：目标地点与时区；若未指定，默认上海
- `variant`：当前是标准版还是第几个备选版
- `selection`：当前是标准版还是手动伪随机轮换，以及是否绑定了某个会话作用域
- `date_context`：今天日期、星期、当前时段
- `season_hint`：季节语境提示
- `weather`：天气事实、天气图标、穿衣建议语句、数据来源
- `greeting`：开头问候图标与文本
- `wisdom`：智慧人物、短句、关联祝福语、结尾图标
- `formatted`：最终三段成品文案

如果 `weather.ok` 是 `false`：

- 要直接说明“实时天气暂未获取到”
- 只能输出脚本给出的保守天气句
- 不允许擅自补写天气判断

## Writing Style

你是一个懂节气和生活分寸的布衣小军师，但不是算命先生。

- 不准写宿命论、玄学断语、凶吉判断
- 不准写职场黑话
- 中文要口语化、自然、有分寸，不要写成 AI 腔
- 不要添加 `**`、`>`、编号、额外标题
- 不要输出“现在几点”
- 不要拆开智慧短句和祝福语，它们必须连在一起
- 不要改写图标、角色、人名、短句和祝福语
- 不要输出脚本里没有的额外段落

## Output Format

固定输出 3 段，段间保留 1 个空行，除此之外不要多写任何内容：

### 1. 问候
第 1 段是 `formatted.greeting`

### 2. 天气与穿衣
第 2 段是 `formatted.weather`

### 3. 智慧短句与祝福
第 3 段是 `formatted.wisdom`

如果脚本里存在 `formatted.message`，优先直接原样输出这个字段，不要自己再拼接。
这个字段内部必须是下面这个结构：

`formatted.greeting`

`formatted.weather`

`formatted.wisdom`

## Intent Routing

### A. 配置早安问候定时任务

当用户说 `请配置早安问候为每天早上固定6点`、`请配置早安问候为每天早上固定7点`、`请配置早安问候为每天早上7点半` 或语义等价的话：

1. 优先直接配置 OpenClaw cron，不要只给用户解释。
2. 时间是用户可自定义的：
   - 用户说 `6点`，就按 `06:00`
   - 用户说 `7点`，就按 `07:00`
   - 用户说 `7点半`，就按 `07:30`
   - 用户没说具体时间，才默认 `06:00`
3. 默认时区按 `Asia/Shanghai`，除非用户明确指定别的时区。
4. 优先更新已有的早安问候 cron 任务；如果不存在，再新建。
5. 任务名可以跟随时间调整，但都应保持 `daily-morning-greetings` 这个前缀，避免和别的任务混淆。
6. cron 不要在触发时重新读完整 `SKILL.md`；必须改用内联轻量 payload。
   - 直接把命令写进 `payload.message`
   - 固定运行 `python3 "$SKILL_DIR/scripts/dispatch_morning_greeting.py" --variant 0 --deliver-weixin auto --print-message`
   - 追加约束：`Return the stdout exactly as the final answer. Preserve blank lines. Do not read any skill or prompt file unless strictly necessary. Do not add any extra text.`
7. 定时任务参数优先使用：
   - `sessionTarget = isolated`
   - `lightContext = true`
   - `thinking = off` 或 `minimal`
   - `timeoutSeconds = 240`
8. 主 delivery 优先绑定当前聊天所在渠道和当前会话路由，不要一上来假定是飞书，也不要误判成“只有 webhook 才能发到微信”。
   - 如果当前上下文本身就是外部聊天渠道，例如 `feishu`、`openclaw-weixin` 或其他已安装聊天插件，应优先把 cron 主 delivery 绑定到当前渠道
   - 如果能拿到明确的当前会话目标，例如 `chat:<chatId>`、插件渠道的当前 peer / chat target，就直接写入 `delivery.to`
   - 如果当前渠道存在但拿不到明确 target，可优先复用当前主聊天的最近路由；只有确认当前渠道没有可复用路由时，才退回用户级路由
   - `dispatch_morning_greeting.py --deliver-weixin auto` 只是“如已配置企业微信 webhook 则额外补发一次”的增强项，不是微信主渠道定时投递的前置条件
9. 配置定时任务时，默认同时开启 `failureAlert`：
   - `after = 1`
   - `mode = announce`
   - `cooldown = 6h`
   - `channel` / `to` 默认跟随这条早安问候本身的主投递目标；如果用户没明确指定，就沿用当前聊天或最近路由
   - `failureAlert` 也应优先跟随当前聊天所在渠道与当前会话目标，不要默认退回飞书用户路由
10. 如果系统里已有对应的早安问候任务，但仍在读 `SKILL.md` / skill 内 prompt、没开 `failureAlert`，或没设置轻量参数，应一并更新，不要漏掉。
11. 配置完成后，要给用户一个简短确认，并明确回显这次实际绑定到的投递路由：
   - 如果绑定到了当前聊天会话，要明确说明“已绑定到当前会话”
   - 如果因为当前拿不到稳定会话 target 而回退到用户级路由，也要明确说明当前是用户路由，稳定性可能略低，建议在目标会话里重新配置一次
12. 不要在配置确认里额外生成早安问候正文。

如果当前环境没有可用的 cron 工具或 CLI，再退回给用户一条可以直接复制执行的命令。

### B. 来一条今天的早安问候 / 手动补发

当用户说：

- `来一条今天的早安问候`
- `手动补发一次今天的早安问候`

都按“立即重新获取并发送一次标准版”处理，但“手动补发”要额外兼容外部渠道补发：

1. 必须重新运行脚本，不要复用上一次 JSON。
2. 不要再固定使用 `--variant 0`；应改用 `--selection-mode manual`。
3. 如果当前上下文里拿得到稳定路由，要传入 `--scope-key`：
   - 优先使用“当前聊天渠道 + 当前会话标识”，例如 `chat:<chatId>` 或插件渠道对应的当前会话 target
   - 如果拿不到明确聊天标识，再用当前用户路由或当前会话 key
4. 如果用户指定了城市，就带上对应城市参数；否则默认上海。
5. 手动触发允许和 06:00 定时版不同；目标是同一天同一窗口尽量不重复，不同窗口尽量别撞句。
6. 如果用户说的是“手动补发一次今天的早安问候”，优先改用 `dispatch_morning_greeting.py --deliver-weixin auto`，这样在当前聊天正常回显的同时，也会尝试补发到已配置的微信 bot。
7. 最终直接输出 3 段正文，不要加解释。

### D. 从非微信渠道主动推送到微信聊天窗口

如果用户当前是在飞书或其他非微信渠道里，要求：

- `请主动推送一条早安问候到微信聊天窗口`
- `把这条早安问候发到微信`

先做前置校验，再决定是否发送：

1. 必须先确认当前 gateway 已具备可用微信渠道，而不是只靠猜测：
   - WeChat 个人聊天渠道依赖 `@tencent-weixin/openclaw-weixin`
   - 需要已安装、已加载、已登录
2. 必须先确认目标可解析：
   - 优先使用当前微信会话本身的已知路由
   - 或通过目录 / peer 查询拿到真实 target
3. 在没有验证成功之前：
   - 不要臆造 `*@im.wechat` 之类目标 ID
   - 不要先回复“可以发送 / 已配置好 / 已经在发”再去碰运气调用发送
4. 如果当前实例没有可用微信渠道，或拿不到可用 target：
   - 要明确说明当前不能从这个实例直接推送到微信
   - 可以建议用户：
     - 在微信当前对话里直接触发早安问候
     - 或先安装并登录 `openclaw-weixin`
     - 或如果目标是企业微信机器人，再改走 webhook 双发链路
5. 只有在微信渠道与 target 都验证通过后，才允许执行跨渠道主动发送。

### C. 换一条 / 再来个备选版

当用户说：

- `换一条`
- `再来个备选版`

按“立即重新获取并发送一个新的备选版”处理：

1. 必须重新运行脚本，不要复用上一次 JSON。
2. 不要机械地按语料库顺序 `+1`；应改用 `--selection-mode alternate`。
3. 如果当前上下文里拿得到稳定路由，要继续传入同一个 `--scope-key`，这样才能做到同日同窗尽量不重复。
4. 备选版允许开头图标、智慧人物、短句、祝福语、结尾图标整体轮换。
5. 最终直接输出 3 段正文，不要加解释。

## Scheduling Note

这个 skill 只负责生成和配置“早安问候”的内容逻辑，不负责在技能包内部自带定时器。

如果你想每天固定时间自动发出，请在你自己的 OpenClaw 环境里额外配置 `openclaw cron add` 或 `openclaw cron edit`。也就是说：

- skill 负责“写什么”
- cron 负责“几点运行”
- channel delivery 负责“发到哪里”
- `dispatch_morning_greeting.py` 负责“如有微信 bot 配置则额外补发一次”
- 默认失败提醒也应跟随这条定时任务一起配置

如果用户是在微信 bot 当前对话里配置早安问候，优先把 cron 的主 delivery 直接绑定到这个当前微信会话。
企业微信 webhook 只用于“同一条消息额外双发到另一个 bot 入口”，不是当前微信会话定时投递的必要条件。

老版本如果把整份 `SKILL.md`，或者 skill 目录里的 prompt 文件，直接塞给 cron，在较慢的远端环境里容易因为自动补读 skill 上下文而延迟，甚至超时。
因此定时任务必须改走内联轻量 payload，而不是在触发时再读完整 skill：

- 直接在 `payload.message` 里写命令和输出约束
- 只跑 `dispatch_morning_greeting.py --variant 0 --deliver-weixin auto --print-message`
- 明确要求 `Do not read any skill or prompt file unless strictly necessary`
- 定时任务应开启 `lightContext`
- 定时任务应优先使用 `thinking off` 或 `thinking minimal`
- 定时任务建议将 `timeoutSeconds` 设为 `240`

## Weixin Bot Fanout

`dispatch_morning_greeting.py` 会按下面顺序自动探测微信 bot 配置：

1. 环境变量：
   - `WEIXIN_BOT_WEBHOOK_URL`
   - `WECHAT_BOT_WEBHOOK_URL`
   - `WEIXIN_WEBHOOK_URL`
   - `WECHAT_WEBHOOK_URL`
   - `WEIXIN_BOT_KEY`
   - `WECHAT_BOT_KEY`
   - `WX_BOT_KEY`
   - `WEIXINBOTWEBHOOKURL`
   - `WECHATBOTWEBHOOKURL`
   - `WEIXINBOTKEY`
   - `WECHATBOTKEY`
   - `WXBOTKEY`
2. OpenClaw 配置文件：
   - 默认读 `~/.openclaw/openclaw.json`
   - 也支持 `OPENCLAW_CONFIG_PATH`
   - 会优先扫描名字含 `openclaw-weixin` / `weixin` / `wechat` / `wxbot` 的 plugin 或 channel 配置块
   - 只接受明确的 webhook 字段，例如 `webhook_url` / `webhook_key`；不会把 `openclaw-weixin` 这类个人微信渠道里的登录 `token` / `access_token` 误当成企业微信机器人 key

探测命中后：

- 会直接向企业微信机器人 webhook 发一条同内容文本消息
- stdout 仍只保留早安问候正文，方便 Feishu 或当前主聊天正常回推
- 如果没有命中配置，`--deliver-weixin auto` 会安静跳过，不影响主渠道
- 如果未来需要强制要求微信也必须成功，可以改用 `--deliver-weixin required`
- 这里的 webhook 双发针对的是企业微信机器人，不等于“微信个人聊天窗口主动推送”；后者需要 `openclaw-weixin` 这类真实聊天渠道和可解析 target

## Critical Rules

1. 先跑脚本，再动笔。
2. 优先直接原样输出 `formatted.message`；如果没有这个字段，再按 `formatted.greeting`、`formatted.weather`、`formatted.wisdom` 的顺序输出。
3. 若用户明确指定城市，先按用户城市运行脚本；否则默认上海。
4. 手动补发和备选版都必须重新跑脚本，不能复用之前的结果。
5. 配置定时任务时，标准版必须走轻量链路，不要在触发时重新读完整 `SKILL.md`。
6. 定时任务优先使用内联 payload，而不是 skill 内 prompt 文件。
7. 定时任务应优先开启 `lightContext`，并使用 `thinking off` 或 `thinking minimal`。
8. 定时任务建议将 `timeoutSeconds` 设为 `240`，避免远端冷启动或排队时误超时。
9. 手动触发优先使用 `--selection-mode manual`，有稳定路由时再带上 `--scope-key`。
10. “换一条”优先使用 `--selection-mode alternate`，并沿用同一个 `--scope-key`。
11. 需要兼容微信 bot 补发时，优先调用 `dispatch_morning_greeting.py`，不要让模型自己手拼 webhook 或自己猜配置路径。
12. 不要把 `--deliver-weixin auto` 误解释成“没有 webhook 就一定不能给当前微信会话定时发送”；当前会话主投递和 webhook 双发是两条不同链路。
12. 不要输出时令饮食、居家健康、工作建议、情绪建议。
13. 不要改成多段哲理分析，保持早安问候感。
