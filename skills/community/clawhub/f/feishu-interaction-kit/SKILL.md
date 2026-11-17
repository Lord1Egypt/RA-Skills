---
name: feishu-interaction-kit
slug: feishu-interaction-kit
version: 1.0.0
category: integration
author: 九品锦锂e
license: MIT
platforms: [any]
displayName: 飞书机器人卡片·思考折叠流式战果卡
summary: 零依赖飞书卡片 CLI：思考折叠卡 + 战果独立卡 + 打字机流式 + 状态行，probe 四步自检不发消息。
description: "智能体接飞书，思考过程与结论糊一条消息刷屏、长按复制全是噪音。方案：思考折叠卡+战果独立卡，长按整卡复制=干净答复，打字机流式+状态行。零依赖纯标准库CLI，任何能执行shell的智能体可调，probe四步自检不发消息。内置绕开99992402/300317/11310实测坑。飞书机器人/飞书卡片/CardKit/流式消息/打字机/消息卡片"
---

# 飞书 AI 交互套件（零依赖 · 平台无关）

## 一、它解决什么

智能体接飞书，默认体验通常很难看：思考过程、工具调用、最终答复全糊在一条消息里刷屏；
长按复制，拿到的是带一堆思考噪音的混合文本。

本套件把交互固定成一套 **两卡版式**，任何智能体都能照做：

- **卡 1 · 思考卡**：折叠面板装"思考和工具调用过程"，面板外只留一行实时窗。整卡可直接跳过。
- **卡 2 · 战果卡**：最终答复独立成卡，标题「🏆 战果」。**长按整卡复制，拿到的就是干净答复。**
- 正文以打字机流式输出；卡尾自动追加一行状态（耗时 / token / 模型）。
- 卡片整体走**琥珀金双色**（琥珀金＝数字与关键指标，咖啡＝小标签），一段话最多两处颜色。

**关键设计**：正文不放在思考卡里 —— 这是"复制干净"和"不刷屏"两个诉求的唯一同时解。

## 二、5 分钟接入

### 第 1 步：飞书后台开权限并发布

需要的权限（开发者后台 → 权限管理）：

- `im:message`（发消息）
- `im:message:send_as_bot`（以应用身份发消息）
- `cardkit:card:write`（建卡与更新卡 —— 不用 CardKit 老卡片可不开）

然后 **创建版本并发布**（企业内部应用需管理员审核）。详见 `references/权限与配置清单.md`。

### 第 2 步：跑一次自检

```sh
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx

python scripts/feishu_card.py probe          # 只建卡、不发消息、不打扰人
```

四步全 `true` 就说明账号、权限、网络、以及三个经典的坑都不存在了：

```
{"action":"probe","ok":true,"steps":[
  {"step":"1_create_card","ok":true},
  {"step":"2_typewriter","ok":true},
  {"step":"3_append_status_line","ok":true},
  {"step":"4_close_stream","ok":true}]}
```

失败时错误码会打印排查提示（见 `references/错误码对照表.md`）。

### 第 3 步：接进你的智能体

只要你的智能体**能执行 shell 命令**（Hermes / Claude Code / Codex / QwenPaw 等），就能接。典型一轮交互：

```sh
# 1) 建思考卡并发出，拿到卡 1 的 card_id
python scripts/feishu_card.py think-card --receive-id oc_xxx
#    → {"card_id":"c_1","message_id":"om_1"}

# 2) 思考过程中，实时刷面板里的全量日志 + 面板外的实时窗
python scripts/feishu_card.py update --card-id c_1 --element-id think_log --text "正在检索资料…"
python scripts/feishu_card.py update --card-id c_1 --element-id think_live --text "💭 正在核对数据源"

# 3) 正文开始 → 另建战果卡（卡 2）
python scripts/feishu_card.py result-card --receive-id oc_xxx
#    → {"card_id":"c_2","message_id":"om_2"}

# 4) 打字机更新正文
python scripts/feishu_card.py update --card-id c_2 --text "第一段结论…"

# 5) 收尾：思考卡定格 ✅（重新用 think_log 写完整日志），两张卡都关流式
python scripts/feishu_card.py update --card-id c_1 --element-id think_title --text "<font color='cus-1'>**思考和工具调用过程**</font> ✅"
python scripts/feishu_card.py close --card-id c_1 --summary "查看完整思考过程"
python scripts/feishu_card.py close --card-id c_2 --summary "第一段结论…"
```

**更新频率**：`update` 由调用方自行节流到 **≥0.5 秒一次**（在自己的循环里控制间隔），
太频繁既没必要、也更容易撞上 `sequence` 问题。

**sequence 怎么处理**：默认**不传**（单写者场景最省心，飞书不做乐观锁校验）。
只有在"多个进程/协程并发写同一张卡"时才需要自己发号，且必须**串行递增**——传错顺序会报 `300317`。
本套件默认不传，就是为了让接入方少踩这个坑。

## 三、命令速查

| 命令 | 作用 | 关键参数 |
|---|---|---|
| `token` | 只验凭据能否换到 `tenant_access_token` | — |
| `chats` | 列出机器人所在的群（拿 `chat_id` 最省事） | `--page-size` |
| `probe` | 四步自检（建卡→打字机→追加状态行→关流式），**不发消息** | `--theme` |
| `send` | 发静态卡片（1.0 老版，**不需要 CardKit 权限**） | `--receive-id`、`--text`、`--title` |
| `think-card` | 建思考卡（可同时发出） | `--receive-id`、`--title` |
| `result-card` | 建战果卡（可同时发出） | `--receive-id`、`--title`、`--text` |
| `update` | 更新某个元素内容（打字机） | `--card-id`、`--element-id`、`--text` |
| `append` | 在某元素后插入新元素（状态行） | `--card-id`、`--after-element-id`、`--text` |
| `close` | 关流式并设置收起摘要 | `--card-id`、`--summary` |

- 所有命令输出**一行 JSON**，成功 `{"ok":true}`，失败 `{"ok":false,"code":…,"msg":…}` 且退出码 1。
- 凭据可用环境变量：`FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_RECEIVE_ID` / `FEISHU_RECEIVE_ID_TYPE`。
- 主题：`--theme amber`（琥珀金，默认）｜ `--theme neutral`（中性蓝灰，脱敏用）。

**元素 id 约定**（模板见 `references/cards/`）：

- `think_title` 折叠面板标题（可塞 spinner 帧）
- `think_log` 面板内全量思考日志
- `think_live` 面板外一行实时窗
- `result_title` 战果标题
- `streaming_content` **正文**（打字机就更新它；状态行靠 `insert_after` 它追加）

## 四、三个必踩的坑（都已在代码里绕开）

1. **`99992402 field validation failed`** —— 追加元素接口少传了必填 `type`（须 `insert_after`／`insert_before`／`append`）；
   且 `elements` 必须是 **JSON 字符串**，传数组会报 `9499`。SDK 的类型提示不靠谱，它说 `str` 也别信一半。
2. **`300317 sequence number compare failed`** —— 同一张卡被并发写，序号乱了。要么别传 `sequence`，要么**每卡一把锁**串行发号。
   （实测：三路并发写同卡，3 分钟丢 4 次更新，全是这个码。）
3. **`11310`（自定义色）** —— 自定义色必须**明暗两套都写**，缺一套就报错。琥珀金主题里 `cus-0`＝琥珀金、`cus-1`＝咖啡。

还有一个最容易漏的：**`settings` 接口是 `PATCH`，写成 `PUT` 会 404**（本套件已踩过并修好）。

## 五、长内容怎么发（C 方案）

飞书卡片是整体渲染单元，长文塞进去会被挤成"一行一个字"。规矩：

- **卡片＝摘要**（≤15 行，手机一屏看完）
- **全文走文件或云文档链接**（`.md` / `.docx` 附件、云文档链接）

## 六、降级路径（没有 CardKit 权限也能用）

`send` 命令发的是 1.0 老版静态卡片（`msg_type=interactive`，content 直接内嵌卡片 JSON），
**不需要 `cardkit:card:write`**。代价是没有打字机与流式更新，适合只想"发张好看点的卡"的场景。

## 七、文件说明

```
feishu-interaction-kit/
├── SKILL.md                        # 本文件（给智能体读的说明书）
├── scripts/feishu_card.py          # 零依赖 CLI（纯标准库）
└── references/
    ├── 权限与配置清单.md            # 后台要开什么权限、怎么拿 chat_id
    ├── 错误码对照表.md              # 报错 → 根因 → 修法
    ├── 接入示例.md                  # shell / Python / Node / 伪代码四种接法
    └── cards/
        ├── think_card.json          # 思考卡模板（可直接改）
        └── result_card.json         # 战果卡模板（可直接改）
```

---

*初版沉淀自 QwenPaw 飞书渠道线上实测（原作者：膺战），经通用化改造与维护：九品锦锂e ｜ 版本 1.0 ｜ 三个真缺陷均在生产环境复现并修复后沉淀。*

---

## 🙋 关于作者

**九品锦锂e** ｜ 把踩过的坑封装成"拿来就能跑"的 skill，不写教科书。这个 skill 是我自己每天在用的版本。

**微信：ly5419495**（加时备注「SkillHub」，我优先通过）
**公众号：初五Agent**（微信搜一搜，复盘和方法都写在那儿，不加微信也能读）

我另外做的几个能直接跑的工具，都放在这个货架页（复制到浏览器打开）：
https://skillpay.alipay.com/public/jiupinjinli

用的时候卡住了、或者有别的场景想让我封装成 skill，按上面任意方式找我就行。

![九品锦锂e 微信二维码](https://jinli-vault-1372591613.cos.ap-guangzhou.myqcloud.com/skillhub/hook-wechat-jiupinjinlie.png)
