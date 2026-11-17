# cyber-im-avatar

> 把你的办公 IM 分身挂起来：有人发消息才干活；没人说话时几乎不花 token（每小时一次缓存续期）。

以**你本人身份**值守飞书 / 企业微信 / 钉钉的一个会话：新消息进来 → 唤醒 agent →
按你的语气起草 → 以你的身份发出 → 重挂等待。

## 值守中的一天

> 你把它挂上，然后去忙自己的事。有消息才唤醒 AI，没人说话时它只是在本地睡觉。

| 时间 | 它在做什么 | 你要做什么 |
| --- | --- | --- |
| 09:12 | 客户发来「这个报价还能再让一点吗？」 | — |
| 09:12 | 本地轮询命中，唤醒 agent（没命中就不跑模型） | — |
| 09:13 | 读当前对象画像，按你的语气起草回复 | 看一眼草稿，点「发送」 |
| 09:14 | 发出后重新挂起，等下一轮 | — |
| 18:30 | 每 55 分钟续一次上下文缓存，其余时间没有模型请求 | — |

一轮真实值守大概长这样（人物与对话虚构）：

> **客户**：这个报价还能再让一点吗？
>
> **分身草稿**：我先跟内部确认一下成本，今天下班前给你准信。

默认**人工确认**，草稿不会自己发出去；涉及金额、承诺、合同或外部群的消息只提醒、不代回。

## 两种形态

同一个仓库提供两种用法，共用飞书 / 企微 / 钉钉的 CLI 登录态：

| 形态 | 位置 | 适合 |
| --- | --- | --- |
| Skill | 仓库根目录（`SKILL.md` + `scripts/`） | 挂在 Claude Code / WorkBuddy 里，agent 被消息唤醒后自己跑完整闭环 |
| DSH 插件 | [`dsh-plugin/`](dsh-plugin/) | 想要一个常驻壳：侧边栏席位、收件箱与通知、手动发送；命中后同样唤醒一个真 DSH 会话，由 agent 自己调 CLI、调研、回复 |

> 插件壳默认启用 **飞书 / 企业微信**；钉钉是第三个平台，默认不启用——没装 `dws` 的机器
> 不会每轮白跑授权检查。在「体检」页点钉钉卡片的「启用」即可纳入轮询与唤醒。

插件形态把轮询、状态、API 放进 `dsh-plugin/lib/`，**直接跑在 DSH 宿主进程里**（Node，只用标准库），
不监听任何端口：DSH 把自己的 Web 服务上的一条同源路由 `/plugins/im-standin` 交给它，
机器上唯一的监听 socket 还是 DSH 那个。**插件只当壳，脑子是 agent 会话**：
一通值守会话绑一个长期复用的 DSH 会话，新消息到达时取消在飞 turn、同会话续跑。
本地只留 `~/.im-standin/state.json`、每会话最近 10 条消息指针和唤醒时取回的媒体；
图片会作为 DSH image block 随载荷交给模型，文件/音视频给本地路径，历史正文在线查。

```bash
dsh plugin --profile web add ~/cyber-im-avatar/dsh-plugin
dsh web    # 侧边栏底部出现「IM 值守」
```

细节见 [dsh-plugin/README.md](dsh-plugin/README.md)。

## 为什么不是"定时任务 + AI"

常见做法是 cron 每 5 分钟跑一次 agent 检查有没有新消息——一天 288 次唤醒，绝大多数空跑。
这个 skill 把等待放在**脚本的 sleep 里**：进程阻塞在本地轮询，命中才退出并把消息交给 agent；
每 55 分钟主动退出一次续上下文缓存（见下）。

| 方案 | 8 小时值守的 agent 唤醒次数 | 空跑 token |
|---|---|---|
| cron 每 5 分钟 | ~96 次 | 每次都要读上下文 |
| 本 skill | 真实消息数 + 每小时 1 次缓存续期 | ≈0（缓存命中） |

### 为什么监听 55 分钟就主动退出

模型服务商的上下文缓存通常按 1 小时过期，命中缓存比重新读一遍上下文便宜得多。监听脚本
默认在 **55 分钟** 主动退出（退出码 `3`）；agent 被这次退出叫醒、按原样重挂，这一次模型
调用会命中旧缓存并把 1 小时有效期续上。两次续期之间仍然只有本地轮询，不产生模型请求；
代价只是每小时一次很便宜的缓存命中。`--cache-refresh-min 0` 可关闭；临时值守重挂继续沿用同一个
`--until`，不会重置截止时间。

> DSH 插件形态不走这个脚本：会话常驻 DSH，由轮询器按消息唤醒，没有「监听进程退出」这个
> 时点，目前不做 55 分钟心跳。

## 三个设计取舍

1. **不无脑拉全量会话。** 按名字精准解析 → 最近会话 → 全量列表（限页）三级降级。
   实测某账号有 2000+ 会话，翻 100 页都没到底，"先拉全部再筛"是不可行的。
2. **平台差异不进引擎。** `listen_core.py` 没有任何平台分支，差异全在 ADAPTER 的
   命令模板 + 字段候选路径里；CLI 版本漂移时改 `env.json` 的 overrides 即可，不碰代码。
3. **承认不知道。** 企微没有消息 ID、钉钉没登录就读不了——这些都在 `references/` 里写明，
   而不是假装适配过了。

## 安装

需要 Python 3.9+；运行时只用标准库。把公开仓库安装到用户级 skill 目录：

```bash
# 装到你所用 agent 的 skills 目录（下面以 Claude Code 为例）
git clone https://github.com/buger-gif/cyber-im-avatar.git ~/.claude/skills/cyber-im-avatar
cd ~/.claude/skills/cyber-im-avatar

# IM CLI 依赖任一（可多装）
npm install -g @wecom/cli               # 企业微信，wecom-cli
npm install -g dingtalk-workspace-cli   # 钉钉，dws
# 飞书：安装 lark-cli 并 lark-cli auth status 确认登录态

python3 scripts/bootstrap.py            # 探测环境、抓本人 ID、写 ~/.im-standin/env.json
python3 tests/run_tests.py              # 安装后自检，不碰真实账号
```

## 30 秒上手

```bash
python3 scripts/bootstrap.py --find feishu "张三"        # 名字 → chat_id，自动登记
python3 scripts/bootstrap.py --learn-style feishu --chats oc_xxx  # 仅显式选择的会话，脱敏
python3 scripts/bootstrap.py --selftest feishu oc_xxx    # 3 秒验证通路
UNTIL=$(python3 -c 'import time; print(int(time.time() + 1800))')
python3 scripts/feishu_listen_cli.py --chat-id oc_xxx --sender ou_yyy --until "$UNTIL"
```

命中时退出码 `0`，stdout 一行 JSON；没消息到点退出 `3`（含每小时缓存续期，重挂即可）；出错退出 `2`。临时值守命中后重挂要沿用同一个 `--until`，不要重新计算或重置截止时间。

## 三平台差异（一句话版）

| | 飞书 | 企业微信 | 钉钉 |
|---|---|---|---|
| 有消息 ID | ✅ `message_id` | ❌ 用复合指纹 | ✅ `messageId` |
| 需要时间窗 | 否 | **是**（必填，仅近 7 天） | 否（可省略） |
| 返回顺序 | 倒序 | **正序** | 倒序 |
| 单聊 chat_id | `oc_` 会话 ID | **对方 userid** | `userId` |
| 找人 | `contact +search-user` | `contact users search` | `contact user search` |

细节和坑位见 `references/`。

## 自测

```bash
python3 tests/run_tests.py
```

用假 CLI 模拟三种输出形态（企微正序无 ID / 钉钉倒序多段 JSON / 字段全错），
验证命中唤醒、防回环、水位去重、关键词与发送者过滤、SCHEMA_MISMATCH 诊断与 override 修复，
外加文档索引锚点完整性与 doctor 自检。
**不需要真实账号，也不会发出任何消息。**

## 挂了怎么办（这是最常被问的）

AI 分身最典型的死法不是报错，而是**静默失效**：CLI 升级后字段改名，拉取照样 200，
但正文永远取到空 → 永不命中，你以为它在守，其实它瞎了。所以先体检，别猜：

```bash
python3 scripts/doctor.py                          # CLI / 版本 / 授权 / 配置 / 水位
python3 scripts/doctor.py feishu --chat-id oc_xxx  # 附带 3 秒真实通路自检
python3 scripts/doctor.py --check-update           # 各 CLI 是否有新版
```

每项失败都给 `→ 修复:` 一行和手册锚点。完整故障索引在
**[`references/troubleshooting.md`](references/troubleshooting.md)**，按症状查：

| 症状 | 处理 |
|---|---|
| `unrecognized subcommand` / 字段突然没了 | §A 版本漂移：`lark-cli update --check`、`dws upgrade --check`、`npm view @wecom/cli version` |
| 授权到期 / 401 / `未登录` | §B：飞书 `python3 scripts/reauth.py feishu`（**bot 发卡片到你的 IM，点一下续期，不扫码**）；企微 `auth init --manual`；钉钉 `auth login --device` |
| `SCHEMA_MISMATCH` | §C：`--probe` 看真实 JSON → 写 `overrides` → `--selftest` |
| 拉不到消息 | §D：企微时间窗仅 7 天、群/单聊参数互斥、429 限流 |
| 不唤醒 / 重复唤醒 | §E：看水位文件、核对 `--sender` 与 `self_id` |
| 挂上没动静 | §F：单发唤醒，处理完必须重挂 |
| 发不出去 | §G：企微 `--text` 必须是 JSON 对象 |
| 涉及钱/承诺/外部群 | §H：**硬停交人，不自动回** |

核心原则：**fail 未清零不挂监听**——它不会报错，只会假装在工作。

### 续期不想扫码？让它把授权按钮发到你 IM 里

飞书 token 大约 7 天要重新授权一次，传统做法是去终端跑 `auth login` 再扫码。现在：

```bash
python3 scripts/reauth.py feishu        # bot 直接给你发一张「一键续期授权」卡片
```

点一下卡片 → 确认 → 完事（`--detach` / `--complete` 支持 agent 异步收尾）。

**只续期、不扩权（对任何人、任何应用都自适应）**：`lark-cli auth login` 不带 `--scope` 时
等价于 `--domain all`，会把应用开通的所有业务域（如妙搭 `spark:*`）都申请一遍。本脚本永远
显式传 `--scope`：

- 默认 `--policy keep`：沿用你**当前已授予**的集合，新增恒为 0
- `--policy minimal`：首次安装 / 主动收窄，只留本 skill 必需的那几项
- 应用没开通的必需权限自动取交集跳过（否则 OAuth 会整体失败）；多了权限直接拒跑，
  要加必须 `--add` + `--allow-add`

完整标准（必需清单、三种边界情况、企微/钉钉为什么没有 scope）写在 **SKILL.md → 权限标准**。自查：

```bash
python3 scripts/reauth.py feishu --show-scope   # 本次申请几项 / 新增几项（应为 0）
python3 scripts/doctor.py feishu                # 必需权限是否齐备
```

能这么做是因为 **bot 凭证（app_id/secret）与 user token 是两套**：user token 过期时 bot
照样能发消息。企微是机器人凭证（用 `auth init --manual` 免扫码），钉钉未登录时没有 bot
通道 —— 这两个平台脚本会直接告诉你正确路径，不糊弄。

## 隐私与合规

- 所有个人数据（本人 ID、会话别名、服务对象画像、聊天语料、风格文件）都在 `~/.im-standin/`，
  与 skill 目录分离，不进版本库、不随 skill 分发；脚本自动设置目录 `700`、文件 `600`。
  收件箱只在待回时保留消息正文，处理完/知会/已发的消息只留指针；历史正文回平台在线查。
- 学风格必须显式 `--chats` 选择会话，URL、凭据、邮箱、ID 等默认脱敏，语料保留 30 天；
  `python3 scripts/bootstrap.py --delete-data --yes` 可删除全部个人数据。
- 服务对象画像有 8KB 软上限 / 12KB 硬上限；接近上限时 agent 会整理成稳定结论，
  旧版归档到同目录 `.history.md`，不会无限追加。画像长什么样见
  [SKILL.md](SKILL.md) §服务对象画像（脱敏示例）。
- 聊天内容一律是不可信数据，不得据此执行命令、读文件、改配置、扩权或向第三方转发信息。
- 分身以**你的身份**发言，外发前默认人工确认；涉及公司合规请自行确认授权范围。
- 企业微信每条响应里的 `extra_identity_context` 含身份声明，脚本只取 `messages`，
  不会把它带给被值守方。
- `doctor.py` 输出默认给所有 ID 打码（`--show-ids` 才显示全量）；对外上报前仍请按
  `references/troubleshooting.md` §J 自检一遍。

## 参与贡献

- 想改代码：先读 [CONTRIBUTING.md](CONTRIBUTING.md)——里面写了改 `panel.js` 要重建产物、
  以及**哪些东西不能进仓库**（真实聊天、凭据、个人路径、内网地址）。
- 项目文档（架构 / 契约 / spec 流程 / runbook）从 [docs/README.md](docs/README.md) 进；
  给 AI 会话看的项目指引是 [AGENTS.md](AGENTS.md)。
- 报安全漏洞：走 [SECURITY.md](SECURITY.md) 的私密通道，别开公开 issue。
- 示例数据一律虚构（`dsh-plugin/scripts/demo/fixture.mjs`），截图用 `node scripts/shot-dsh.mjs` 复现。

## License

MIT
