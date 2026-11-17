# 故障处理索引（Troubleshooting Index）

> **这是索引，不是教程。** 先看 §0 定位症状，跳到对应小节照「修复」跑命令，
> 最后回 §11 做回归。自愈不了再按 §10 上报——别一上来就问人。
>
> 所有命令在 skill 根目录执行。个人数据目录默认 `~/.im-standin/`（可用 `IM_STANDIN_DIR` 改）。
>
> **在 DSH 插件壳里（首轮载荷带「运行形态：DSH 插件壳」）不要跑 `doctor.py` / `bootstrap.py`
> / 监听脚本**：它们会写 `~/.im-standin/states`，壳内沙箱会拒。体检改用面板「体检」
> 页，或只读命令（`lark-cli auth status` / `wecom-cli auth show` / `dws auth status`）。
> 媒体下载失败先在 prompt 里看是否标了「未适配 / 下载失败」，再按对应 `references/` 试。

<a id="triage"></a>

## 0. 30 秒分诊表

| 你看到的 | 最可能原因 | 第一条命令 | 跳 |
|---|---|---|---|
| `command not found` / `CLI not found: xxx` | CLI 没装或不在 PATH | `which lark-cli wecom-cli dws` | [A](#a-cli-缺失-版本漂移命令改名字段消失) |
| `unrecognized subcommand` / `unknown flag` | CLI 升级后命令改名 | `lark-cli update --check` / `dws upgrade --check` | [A](#a-cli-缺失-版本漂移命令改名字段消失) |
| `SCHEMA_MISMATCH keys: ...` | 返回字段路径变了 | `python3 scripts/bootstrap.py --probe <平台>` | [C](#c-schemamismatch返回字段路径漂移) |
| `ERROR: 无法获取本人 ID` | 未登录 / 授权过期 / whoami 改字段 | `lark-cli doctor` / `dws doctor` / `wecom-cli auth show` | [B](#b-授权到期-未登录要引导用户授权) |
| 体检报 `tokenStatus` 非 `valid`、`authenticated:false`、`Status: unauthorized` | 授权到期 | 见 §B.2 重新授权 | [B](#b-授权到期-未登录要引导用户授权) |
| 授权同意页出现你**没用过**的权限（如「妙搭」） | 续期命令漏了 `--scope`，默认 `--domain all` 全量申请 | `python3 scripts/reauth.py feishu --show-scope` 核对，应为「新增 0」 | [B.3](#b3-权限范围只续期不扩权自适应所有人) |
| 进程活着但一直不唤醒 | 目标/发送者过滤写错、水位超前、CLI 拉空 | 看水位文件 + 手动跑一条拉取 | [E](#e-命中行为不对该唤醒没唤醒-反复唤醒) |
| 拉取成功但消息是空的 | 时间窗、权限、限流、消息类型 | `--lookback-min 120` 再试；看是否 429 | [D](#d-拉取成功但拿不到消息) |
| 同一条消息被唤醒多次 | 水位没推进（无 ID 平台指纹抖动） | 看 `~/.im-standin/states/*.pos` | [E](#e-命中行为不对该唤醒没唤醒-反复唤醒) |
| 发出去了但对方没收到 / 报错 | 平台发送参数不同（企微 text 是 JSON） | 见 §G 对应行 | [G](#g-发不出去回复失败) |
| 值守中途彻底没动静 | 单发唤醒处理完没重挂；后台进程被回收 | `ps aux \| grep listen_cli` | [F](#f-值守进程没在跑-中途消失) |
| `env.json` 解析失败 / 报 KeyError | 配置被写坏 | `python3 scripts/doctor.py --repair-state` | [I](#i-配置-状态损坏) |
| 命中内容涉及资金/承诺/外部群 | 合规硬停 | **停手上报，不自动回** | [H](#h-内容与合规硬停不绕过) |

## 1. 先体检，别猜

```bash
python3 scripts/doctor.py                          # 全平台体检：CLI/版本/授权/配置/水位
python3 scripts/doctor.py feishu --chat-id oc_xxx  # 附带 3 秒真实通路自检
python3 scripts/doctor.py --check-update           # 额外查各 CLI 是否有新版
python3 scripts/doctor.py --json                   # 机器可读，便于 agent 决策
```

`doctor.py` 每一项失败都会打印 `→ 修复:` 一行，可直接照抄。

CLI 自带的体检（**优先用它们，它们知道自己的检查项**）：

| CLI | 命令 | 说明 |
|---|---|---|
| 飞书 | `lark-cli doctor` | JSON：`cli_version` / `cli_update` / `config_file` / `app_resolved` / `bot_identity` / `user_identity` / 连通性 |
| 钉钉 | `dws doctor --json` | 每项带 `hint` 字段（如「运行 dws auth login 进行登录」），照着做即可 |
| 企业微信 | ❌ 无 `doctor` | 用 `wecom-cli auth show` + 手动跑一条 `chat messages list` 代替 |

<a id="a"></a>

## A. CLI 缺失 / 版本漂移（命令改名、字段消失）

**症状**：`CLI not found`、`unrecognized subcommand`、`unknown flag`、昨天还能跑今天报参数错。

**为什么会这样**：三个 CLI 都在高频迭代（飞书 `lark-cli update --check`、钉钉
`dws upgrade --check` 都能自查），子命令和返回字段随时可能改。这个 skill 的设计前提就是
**不假设命令永久有效**——所以别改代码，先升级再重新发现。

### A.1 确认装了什么、装的哪个

```bash
which lark-cli wecom-cli dws
lark-cli --version ; wecom-cli --version ; dws version
```

装的位置也能说明升级方式：`~/.nvm/.../bin/` 或 `~/.workbuddy/binaries/...` = npm 装的
（用 npm 升级）；独立二进制 = 用 CLI 自带 `update`/`upgrade`。

### A.2 查最新版（三个平台来源不同，别用错）

```bash
lark-cli update --check            # 飞书：官方更新源，自动识别 npm/pnpm/独立安装
dws upgrade --check                # 钉钉：官方更新源
npm view @wecom/cli version        # 企微：只能查 npm
```

⚠️ npm 上的 `lark-cli`、`dws`、`dws-cli` 是**无关包**，别照着装。飞书包名是
`@larksuite/cli`，钉钉是 `dingtalk-workspace-cli`，企微是 `@wecom/cli`。

### A.3 升级

```bash
lark-cli update                    # 飞书（--json 可给 agent 解析）
dws upgrade                        # 钉钉；独立安装会自动备份，可 dws upgrade --rollback 回滚
npm install -g @wecom/cli          # 企微
```

### A.4 升级后：重新发现命令（**不要凭记忆写命令**）

| CLI | 发现入口 | 查参数契约 |
|---|---|---|
| 飞书 | `lark-cli <domain> --help`（`+shortcut` 优先于原始 API） | `lark-cli schema im.message.list` |
| 钉钉 | `dws <service> --help` → `dws <path> --help` | `dws schema --cli-path "<path>" --compact -f json` |
| 企微 | `wecom-cli <cmd> --help` | `wecom-cli <cmd> --schema`（输出 JSON schema） |

```bash
# 飞书：看 IM 域有哪些快捷命令
lark-cli im --help | grep "^  +"
# 钉钉：看 chat 服务下的命令
dws chat --help
# 企微：看消息列表的真实参数与返回结构
wecom-cli chat messages list --schema | head -c 2000
```

### A.5 升级后必做回归（4 步，缺一步都可能带病上岗）

```bash
python3 scripts/bootstrap.py                                   # 重新探测 → 刷新 self_id
python3 scripts/bootstrap.py --probe <平台> --chat-id <目标>    # 看真实输出，必要时写 override
python3 scripts/bootstrap.py --selftest <平台> <目标>           # 3 秒通路自检
python3 tests/run_tests.py                                     # 引擎回归（不碰真实账号）
```

改名了但功能还在？**只改 `~/.im-standin/env.json` 的 `overrides`，不改代码**（见 [C](#c-schemamismatch返回字段路径漂移)）。

<a id="b"></a>

## B. 授权到期 / 未登录（要引导用户授权）

**症状**：`无法获取本人 ID`、`authenticated: false`、`Status: unauthorized`、
请求返回 401 / token invalid、昨天能跑今天全空。

### B.1 先判断是「过期」还是「没配」

| 平台 | 查状态 | 判定 |
|---|---|---|
| 飞书 | `lark-cli auth status` | 看 `identities.user.tokenStatus`；`expiresAt` 是 access token（约 2 小时），`refreshExpiresAt` 是刷新凭证（约 7 天）。**refresh 也过了就必须重新扫码** |
| 企业微信 | `wecom-cli auth show` | 文本 `Status: authorized` + `Bot ID: ...`；其它状态即未授权 |
| 钉钉 | `dws auth status` | JSON `authenticated: true/false`，`message` 直接写「未登录」。**false 有两种**：真没登过；登录被组织闸门拒（见 B.2 末），后者只能从登录输出认出来 |

```bash
lark-cli auth status | python3 -c "import json,sys; u=json.load(sys.stdin)['identities']['user']; print(u['tokenStatus'], u.get('expiresAt'), u.get('refreshExpiresAt'))"
```

### B.2 重新授权（不要扫码，也不要卡住用户）

**飞书 —— 一条命令：把授权按钮发到你的飞书里**

```bash
python3 scripts/reauth.py feishu              # 需要时才发，发完等你在飞书点（至多 10 分钟）
python3 scripts/reauth.py feishu --detach     # 发完立即返回；点完再 --complete 收尾
python3 scripts/reauth.py feishu --complete <device_code>
python3 scripts/reauth.py feishu --no-send    # 不发卡片，只打印链接（纯终端场景）
```

它做的事：`auth login --no-wait --json --scope "<现有权限>"` 拿设备码 → 以 **bot 身份**发一张交互卡片到你的私聊
（按钮直链授权页，URL 已带 `user_code`）→ 你点一下确认 → `--device-code` 收尾 → 校验状态。

**为什么这能成立**（这也是为什么它比扫码更可靠）：

- bot 身份用 `app_id/app_secret`，是**长期凭证**；user token 是另一套。user token 过期时
  bot 照样能给你发消息 —— 否则就死锁了。
- 卡片按钮打开的是设备流授权页，**不需要本机回调端口**，所以 agent/远端机器也能用。
- 仍然需要你「点一下确认」：OAuth 授权是用户本人的意思表示，第三方应用不能代签。
  能省掉的是**扫码**和**回终端贴 code**，不是那次点击。

手动等价流程（不想用卡片时）：

```bash
# ★ --scope 不能省：不带它等于 --domain all，会把应用开通的所有业务域都申请一遍
SC=$(lark-cli auth status --json | python3 -c "import json,sys;print(json.load(sys.stdin)['identities']['user']['scope'])")
lark-cli auth login --no-wait --json --scope "$SC"   # 立刻返回 verification_url + device_code，不阻塞
lark-cli auth qrcode                        # 需要二维码时（--ascii / --output 出 PNG）
lark-cli auth login --device-code <code>    # 用户确认已授权后收尾
```

> 设备码 **10 分钟**过期，且等同于一次登录凭证 —— 卡片不要转发。
> 若卡片发不出去（bot 未开通与你单聊 / 应用可用范围不含你），脚本会自动退化为文本消息，
> 再失败就打印链接让你手动开。

**钉钉 —— 先分清「没登录」和「组织没开」**

`dws auth login --device` 给出短链接 + `user_code`，本人点确认后流程不会立刻成功，
还要过 Step 4「检查组织 CLI 授权状态」。组织没开 CLI 数据访问时这一步直接拒：

```
⚠️  您暂无 CLI 数据访问权限
   当前组织未授权您通过 CLI 访问个人数据。
   组织主管理员：<姓名>
   管理员操作入口：https://open-dev.dingtalk.com/fe/old#/developerSettings
```

退出码 2，**token 不落盘**：`dws auth status` 回到 `authenticated: false`，
`dws profile list` 空数组，与「从没登录过」在状态上无法区分。闸门按**组织**走，
换号只有在目标号所在组织已开通（或本人就是该组织主管理员）时才有用，重跑设备码
是同一个结果。

处理：把这段输出原文与主管理员名字交给用户，请其开通后再 `dws auth login`。
这是组织侧开关，脚本不申请、不绕过（同 §B.3 的「不扩权」）。

<a id="b3"></a>
### B.3 权限范围：只续期、不扩权（自适应所有人）

**坑**：`lark-cli auth login` 在**不带 `--scope`／`--domain`／`--recommend` 时，等价于 `--domain all`**。
续期会顺手把应用已开通的全部业务域都申请一遍，同意页上就会冒出你从没用过的权限
（本项目实测多出的是妙搭 `spark:app:*`）。在别人机器上这叫「越权申请」，哪怕最后没授予也很吓人。

**规则不看具体账号，只看策略**（脚本已实现，`scripts/reauth.py`）：

| 策略 | 触发方式 | 申请范围 |
|---|---|---|
| `keep`（默认） | 直接跑 | 有历史授权 → `auth status` 的 `scope` **原样照搬**，新增恒为 0；无历史授权 → 落到必需集 |
| `minimal` | `--policy minimal` | 「必需集 ∩ 应用已开通」，首次安装或主动收窄时用 |
| `explicit` | `--scope "a b c"` | 你给什么申请什么（仍要过闸门） |
| 扩权 | `--add <scope> --allow-add` | 缺了这两项就 `[block]`，不会静默加 |

**三种边界情况**（脚本自动处理，不用人记）：

| 情况 | 行为 |
|---|---|
| 应用没开通某必需权限 | 取交集跳过 + 报 `lack_on_app`，说明哪个功能会受限（硬塞会让 OAuth 整体失败） |
| 应用列表里没有、但历史上授予过 | `keep` 保留并提示；若登录报 scope 错，改 `--policy minimal` 收窄重试 |
| 平台基础 scope（如 `auth:user.id:read`） | 永远带上、不告警（它不由应用权限列表控制） |

自查命令：

```bash
python3 scripts/reauth.py feishu --show-scope    # 只演练：本次会申请几项、新增几项（应恒为 0）
python3 scripts/doctor.py feishu                 # 含 scope 能力项：必需项是否齐备
lark-cli auth scopes --json                      # 应用侧开通了哪些（多于你授予的属正常）
lark-cli auth status --json                      # 你实际授予了哪些（以此为准）
```

**已发出去的卡片要撤回**（撤回是高危写操作，需本人确认）：

```bash
lark-cli im +messages-search --as user --query "重新授权" --chat-type p2p   # 取 message_id
lark-cli im messages delete --message-id <om_xxx> --as bot --yes            # 需本人点头后再执行
```

判据：`auth status` 的 `grantedAt` 没变 = 那次授权**没完成**，权限范围没有被扩大。

**企业微信 —— 没有授权卡片，免扫码路径是「手填凭证」**

企微用的是**机器人凭证**（Bot ID + Secret），不是 OAuth，所以不存在"点一下就授权"的卡片；
扫码只是领取凭证的便捷方式。

```bash
wecom-cli auth init --manual        # 免扫码：让管理员直接粘贴 Bot ID + Secret（可复用）
wecom-cli auth init --noninteractive --output-qrcode /tmp/wecom-qr.png   # 远程时把图发给人扫
```

**钉钉 —— 用设备流短链，不发卡片**

dws 未登录时本机没有可用的 bot 通道 —— "用 bot 发卡片"在这里是死锁，所以走设备流：

```bash
dws auth login --device     # 输出 user_code + 短链，浏览器打开输码即可，无需扫码
dws auth login              # 本机有浏览器：起 127.0.0.1 回调，授权后自动完成
dws auth login --token <token>   # 已有 token 直接导入（换机最快）
dws auth status             # 确认 authenticated: true
```

多账号/多组织：`lark-cli auth list` 看已登录身份；钉钉用 `dws profile list` 选
`--profile corpId:userId`。

### B.3 授权成功后收尾（漏了会继续报同一个错）

```bash
python3 scripts/bootstrap.py                        # 刷新 self_id（防回环依赖它）
python3 scripts/bootstrap.py --selftest <平台> <目标>
```

### B.4 授权相关的坑

| 现象 | 原因 | 处理 |
|---|---|---|
| 授权了还是没权限 | token 有效但 scope 不够 | `lark-cli auth check --scope im:message:readonly`；`lark-cli auth scopes` 看应用开了哪些 |
| 以 bot 身份发的消息 | 没带 `--as user` | 读/发都要显式 `--as user` |
| 钥匙串相关报错（macOS） | 凭证存在 Keychain，被锁/换机 | `dws auth migrate-keychain`；`lark-cli doctor` 看 `dpopKeyStatus` |
| 换机器后全部失效 | Keychain 不随文件迁移 | 重新 `auth login`（钉钉可 `auth export` / `auth import` 迁移） |

> **安全**：token、Bot Secret、`extra_identity_context` 都是凭据。**不要贴进聊天、
> 不要写进日志、不要进 git。** 排查时只贴状态字段，不贴值。

<a id="c"></a>

## C. SCHEMA_MISMATCH（返回字段路径漂移）

**症状**：退出码 2，stderr 里有 `SCHEMA_MISMATCH keys: {...}`，或监听能跑但
`content` 永远是空、`sender` 永远是 `None`。

引擎按 ADAPTER 的候选路径取字段，全不命中就报这个错——**这是设计好的可诊断状态**，
不是 bug。修复分三步：

```bash
# 1. 打印真实形态：候选命令逐条试跑，标 [hit] 的那条就是可用命令
python3 scripts/bootstrap.py --probe wecom --chat-id <目标>

# 2. 按真实 JSON 写 override（改配置，不改代码）
#    编辑 ~/.im-standin/env.json，overrides.<平台> 可覆盖/新增任意键
# 3. 复测
python3 scripts/bootstrap.py --selftest wecom <目标>
```

`overrides` 示例（字段挪了一层 + 命令改名，一次搞定）：

```json
{
  "overrides": {
    "wecom": {
      "cmd_list": ["chat", "messages", "list", "--chat-id", "{chat_id}",
                   "--begin-time", "{begin_time}", "--end-time", "{end_time}"],
      "f_items": [["data", "messages"], ["messages"]],
      "f_content_list": [["text", "content"], ["content"]]
    }
  }
}
```

| 成因 | 表现 | 改哪个键 |
|---|---|---|
| 多包了一层信封 | `{"code":0,"data":{"messages":[...]}}` | `f_items`: `[["data","messages"]]` |
| 字段改名 | `text.content` → `content.text` | `f_content_list` 候选顺序 |
| 消息 ID 没了 | 水位不动 / 反复唤醒 | `f_msg_id_compose`（复合指纹） |
| 一条命令失效 | `rc≠0` 或 `unrecognized` | `cmd_list_chain`（给多条候选，命中后缓存） |
| 空结果被当字段错 | 会话真没消息却报 mismatch | 配 `f_count` / `f_has_more` |

⚠️ **不要用「猜字段」代替 probe**：`dig()` 候选路径命中空字符串也会返回，
看起来"成功"但内容是空——这是最隐蔽的一种误判。

<a id="d"></a>

## D. 拉取成功，但拿不到消息

| 现象 | 原因 | 修复 |
|---|---|---|
| 企微永远返回空 | **必须带时间窗，且只能拉最近 7 天** | `--lookback-min 120`；超 7 天的历史拿不到（API 限制，不是 bug） |
| 刚发的消息看不到 | `--lookback-min` 太小 / 本机时钟偏差 | 加大看窗；`date` 对时 |
| 群消息空、单聊正常 | 群目标参数用错 | 钉钉群用 `--chat-id/--group`，单聊用 `--user`；飞书群是 `oc_` 开头 |
| 企微私聊查不到 | 单聊 `chat_id` **就是对方 userid** | `--user-id <userid>`，不要去查会话列表 |
| 只有群列表没有私聊 | 企微会话列表只回群 | 用 `contact users search` 拿 userid 直接监听 |
| 间歇性空 + 偶发 429 | 触发限流 | 降频（`--interval 60+`）、禁止全量拉、飞书加 `--page-limit` |
| 消息在但正文为空 | 富文本/卡片/系统消息，正文路径不同 | probe 看该条原文字段；飞到 `cmd_mget` 补全 |
| 只能看到 bot 消息 | 用了 bot 身份 | 全部读写加 `--as user` |

<a id="e"></a>

## E. 命中行为不对（该唤醒没唤醒 / 反复唤醒）

水位文件在 `~/.im-standin/states/<平台>_<目标>.pos`，内容 `{"last_id": "...", "ts": ...}`。
**它是唯一真相**，先看它。

| 现象 | 原因 | 修复 |
|---|---|---|
| 一直不唤醒 | `--sender` 写错（应为对方 ID，不是名字） | 去掉 `--sender` 先验证，再逐字比对 ID |
| 一直不唤醒 | `self_id` 识别错 → 把对方当成自己过滤掉 | `doctor.py` 看「self_id」项；`bootstrap.py` 重新探测 |
| 一直不唤醒 | `--init latest` 把现有消息设为基线 | 想立刻验证用 `--init zero` |
| 一直不唤醒 | 水位超前（手动改过 / 时钟乱） | 见下表「重置水位」 |
| 反复唤醒同一条 | 平台无消息 ID，复合指纹抖动（同秒同人同文变化） | `f_msg_id_compose` 去掉易变字段（如毫秒） |
| 反复唤醒同一条 | states 目录不可写（`save_watermark` 静默失败） | 检查 `~/.im-standin/states` 权限 |
| 把自己的回复当新消息 | 绕过引擎直接发送且 `self_id` 不准 | 修 `self_id`；别手改水位 |
| 一次来多条只叫醒一次 | **设计如此**（避免连唤醒 N 次） | 读 `pending_in_burst`，拉一次上下文看全 |

重置水位（会重放窗口内消息，慎用）：

```bash
mv ~/.im-standin/states/<平台>_<目标>.pos /tmp/pos.bak   # 备份后删除 = 重新以最新为基线
python3 scripts/doctor.py <平台>                          # 确认状态文件正常
```

<a id="f"></a>

## F. 值守进程没在跑 / 中途消失

本 skill 是**单发唤醒**，不是常驻服务：命中 → 退出 → agent 处理 → **必须重挂**。
"没人理我"十次有九次是忘了重挂。

```bash
ps aux | grep -c "[l]isten_cli"     # 0 = 没在挂；>1 = 挂重了（会双回复）
```

| 退出码 | 含义 | 处理 |
|---|---|---|
| `0` | 命中（stdout 单行 JSON） | 处理完重挂 |
| `3` | 到点未命中 | 正常，重挂 |
| `2` | 参数/环境/schema 错误 | 看 stderr → 走 [B](#b-授权到期-未登录要引导用户授权) 或 [C](#c-schemamismatch返回字段路径漂移) |
| `127` | CLI 不在 PATH | 走 [A](#a-cli-缺失-版本漂移命令改名字段消失) |

其他坑：

- **后台进程随会话结束被回收** → 表现是"挂了但一直没消息"。重挂前先 `ps` 确认没有残留。
- **重复挂载**：两个进程盯同一会话，对方会收到两条一样的回复。挂之前先数进程。
- **别忘了 `--timeout`**：不设就是不限时；设了到点退出 3，反而更安全（不会静默死掉）。
- 重挂不会漏消息：水位在文件里，重启从上次位置继续。

<a id="g"></a>

## G. 发不出去（回复失败）

先把内容写进文件，再用 `$(cat ...)` 传——**引号、换行、表情是发送失败第一大原因**。

```bash
printf '%s' "回复正文" > /tmp/reply.txt
```

| 平台 | 发送命令 | 坑 |
|---|---|---|
| 飞书 | `lark-cli im +messages-send --chat-id <id> --msg-type text --as user --text "$(cat /tmp/reply.txt)"` | 缺 `--as user` 会变成 bot 说话；`text` 里不能塞 JSON |
| 企业微信 | `wecom-cli message send --chat-id <id> --msg-type text --text '{"content":"..."}'` | **`--text` 是 JSON 对象**，裸字符串必失败；`chat_id` 传对方 userid 或群会话 ID |
| 钉钉 | 单聊 `dws chat +messages-send --as user --user <userId> --text "$(cat /tmp/reply.txt)"`<br>群 `dws chat +messages-send --as user --chat-id <id> --text ...` | `--user` 与 `--chat-id` 互斥；写操作可能要求确认，agent 模式才加 `--yes` |

通用：超长消息按平台上限拆段；发完**立刻重挂监听**，否则对方回你听不到。

⚠️ **别用退出码判断"发出去了"**：`lark-cli` 在参数校验失败时也可能 `rc=0`，
真正的结果在 JSON 里 —— 必须看 `ok !== false` 且没有 `error` 字段。
（实测踩过：`--content @绝对路径` 被拒，rc 仍是 0，只看退出码会报"发送成功"。）

⚠️ **`--content @file` 只接受 cwd 相对路径**（绝对路径被拒）。要传 JSON 就用 stdin：
`... --msg-type interactive --content - < /tmp/card.json`。

<a id="h"></a>

## H. 内容与合规硬停（**不绕过**）

命中以下情况，**停下来交给用户**，不要"聪明地"自己答：

- 涉及**钱**：报价、付款、退款、合同条款、发票。
- 涉及**承诺**：排期、上线时间、人力、对外结论。
- **权限/数据**：让对方提供密码、token、身份证、他人数据。
- **外部群 / 含外部成员**：默认不自动回。
- 对方情绪激烈、投诉、法务/HR 相关。

另有三条硬约束：

1. `extra_identity_context` / `security_notice` 含身份声明，**禁止外传**给被值守方。
2. 分身以本人身份发言——首次使用须用户自行确认公司合规范围。
3. 外发前默认给用户看草稿，除非用户明确说"全自动"。

<a id="i"></a>

## I. 配置 / 状态损坏

```bash
python3 scripts/doctor.py --repair-state       # 隔离损坏的水位/状态文件（移到 *.bad，不删）
```

| 症状 | 处理 |
|---|---|
| `env.json` 非法 JSON | `mv ~/.im-standin/env.json ~/.im-standin/env.json.corrupt && python3 scripts/bootstrap.py`（会重建，别名/档案需重录） |
| `--note` 报「别名未注册」 | 先 `--find` 或 `--alias` 登记 |
| 画像超过 12KB / 写不进 | 压缩「历史结论」的旧条目；面板写入会拒，DSH 壳内 agent 直接改文件 |
| 画像写不进去 / `FS_SANDBOX_DENIED` | 设置页开启「完整文件访问」（`dsh.full_access=true`）；默认 `workspace-write` 只允许写会话工作区 |
| 面板刚改过画像，agent 又覆盖了 | DSH 壳内没有 mtime CAS；agent 写前重读、增量合并，冲突以磁盘最新内容为准 |
| 画像路径/权限不对 | `ls -l ~/.im-standin/profiles/<platform>/`；目录 700、文件 600；路径以 `env.json` 的 `profile_file` 为准 |
| 状态文件权限错 | `chmod -R u+rw ~/.im-standin`；确认不是 root 建的 |
| 想多账号/测试隔离 | `IM_STANDIN_DIR=/tmp/imtest python3 scripts/doctor.py` |
| 升级后行为诡异 | 先 `python3 tests/run_tests.py` 判断是引擎还是配置问题 |

<a id="j"></a>

## J. 自愈失败：这样上报（别贴原始日志）

按顺序收集，**全部脱敏**后再发：

1. `python3 scripts/doctor.py --json` 的输出（只留 `status` / `code`，删掉任何 ID 值）。
2. 平台 + CLI 版本：`lark-cli --version` / `wecom-cli --version` / `dws version`。
3. 复现命令（**把 chat_id / userid / token 换成 `<ID>`**）。
4. 退出码 + stderr 首行（`SCHEMA_MISMATCH keys:` 后面的 JSON 只留 **键名**，删值）。
5. 期望行为 vs 实际行为，一句话。
6. 是否刚升级过 CLI / 换过账号 / 换过机器。

脱敏检查：`grep -nE "ou_|oc_|aib|Bearer|token" /tmp/report.txt` —— 命中就删。

<a id="k"></a>

## K. 回归清单（改配置 / 升级 CLI / 换账号后）

```bash
python3 scripts/doctor.py                        # 1 全平台体检，全绿再往下
python3 scripts/bootstrap.py --probe <平台> --chat-id <目标>   # 2 确认真实字段没变
python3 scripts/bootstrap.py --selftest <平台> <目标>          # 3 真跑 3 秒
python3 tests/run_tests.py                       # 4 引擎回归
# 5 手动发一条测试消息给自己，确认监听能唤醒（--init zero 验证存量命中）
```

四项都过再上岗。**只过 1、2 就挂上去 = 大概率静默失效**（能拉取但字段空 → 永不命中）。
