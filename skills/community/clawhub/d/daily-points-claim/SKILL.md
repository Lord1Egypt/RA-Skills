---
name: daily-points-claim
description: 每日自动领取积分、签到打卡的执行器，开箱支持 WorkBuddy（Buddy 加油站）每日签到。当用户要配置、新增、运行、调试「每日签到」「自动领积分」「打卡领奖励」「每日任务领取」类任务，或要检查今天是否已领取、积分是否到账、Cookie 是否过期时使用。支持多站点、模板变量、HttpOnly Cookie 抓取、以及灵活的成功/已领判定规则，可挂定时任务每天自动执行。Use when: daily check-in automation, auto claim daily points, sign-in bonus, scheduled point claiming, WorkBuddy daily check-in, cookie expired troubleshooting.
agent_created: true
---

# 每日积分自动领取

把「人在网页上点签到」翻译成一次 HTTP 请求，用配置驱动的多站点执行器批量完成，并记录每天的结果。零第三方依赖，只要求本机有 Python 3.8+。

## 何时使用

- 用户要新增一个每日签到/领积分的站点
- 用户要手动跑一次领取，或查看今天领没领到
- 签到失败，需要定位是 Cookie 过期、判定规则不对、还是接口变了
- 用户要设置每天定时自动领取

## 目录结构

```
daily-points-claim/
├── SKILL.md
├── scripts/
│   ├── claim.py              # 执行器（主入口）
│   ├── add_site.py           # 交互式新增站点向导
│   ├── buddy_login.py        # WorkBuddy 扫码登录，自动回写 Cookie
│   ├── cdp.py                # 极简 CDP 客户端，用于取 HttpOnly Cookie
│   ├── config.example.json   # 配置模板
│   └── config.json           # 你的真实配置（首次运行自动生成，含 Cookie）
├── references/
│   ├── config-guide.md       # 抓包流程 + 字段 + 模板变量 + 判定规则
│   └── troubleshooting.md    # 故障对照表
└── logs/                     # 运行后自动生成
```

以下命令中的 `<skill>` 指本 skill 目录（如 `~/.workbuddy/skills/daily-points-claim`）。

## 首次使用

`config.json` 不随包分发——首次运行 `claim.py` 时会自动从 `config.example.json` 复制一份并提示填写 Cookie。这样你的登录态永远只留在本地，不会被后续版本更新覆盖。

## 执行

```bash
python "<skill>/scripts/claim.py"                    # 跑全部启用站点
python "<skill>/scripts/claim.py" --site a,b          # 只跑指定站点
python "<skill>/scripts/claim.py" --dry-run           # 只打印请求，不发送
python "<skill>/scripts/claim.py" --json              # 结构化摘要，便于解析
python "<skill>/scripts/claim.py" --check             # 只校验配置
python "<skill>/scripts/claim.py" --set-cookie a "k=v"  # 快速更新 Cookie
```

输出状态含义：`[成功]` 本次领取成功 / `[已领]` 今天已经领过（正常状态）/ `[失败]` 站点明确返回失败 / `[待确认]` 响应未命中任何规则，需人工看响应片段 / `[异常]` 网络或配置错误。

退出码：`0` 全部成功或已领，`1` 存在失败或待确认，`2` 配置问题。

## 已配置站点：WorkBuddy 每日签到

`buddy` 站点开箱即用，只需补 Cookie：

- `POST https://www.workbuddy.cn/billing/meter/daily-checkin`，`code==0` 成功、`code==10001` 今日已领
- 鉴权是 **HttpOnly Cookie**，`document.cookie` 读不到，只能用 CDP 从浏览器取
- **UA 会被 APISIX 网关拦截**：`Chrome/126` 一律 401，必须用较新的 `Edg/156` UA
- 登录态过期时运行 `python "<skill>/scripts/buddy_login.py"`，会开一个专用浏览器窗口让你扫码，
  登录成功后自动把 Cookie 回写到 `config.json`（依赖同目录 `cdp.py`，纯标准库实现）
- 浏览器数据目录落在 skill 目录下的 `browser-profile/`，只含该站点的登录态，不要对外分发

## 新增一个站点

**方式一：交互向导**（用户在终端自行操作）

```bash
python "<skill>/scripts/add_site.py"
```

依次回答 id、URL、方法、Cookie、请求体、判定方式，写入后可选立即测试。

**方式二：由 agent 直接写配置**（用户提供抓包信息时）

1. 向用户索取：签到接口 URL、请求方法、Cookie（或 Authorization）、请求体、以及签到成功时的响应 JSON。
2. 按 `references/config-guide.md` 的字段说明，往 `scripts/config.json` 的 `sites` 数组追加一项。
3. 判定规则优先用响应里的状态字段（如 `code`），重复领取用消息字段关键字（如 `msg` 含「已签到」）区分——很多站点重复签到时状态码仍为成功。
4. 先 `--dry-run` 让用户核对，再 `--site <id>` 真跑一次，确认状态为 `[成功]` 或 `[已领]` 才算配置完成。

缺少响应 JSON 时先把请求发出去，从 `[待确认]` 的响应片段反推字段，再回填规则。

## 挂定时任务

用 `automation_update` 创建每日重复任务，prompt 写成自包含的指令，例如：

> 执行每日积分领取：运行 `python "%USERPROFILE%/.workbuddy/skills/daily-points-claim/scripts/claim.py" --json`，若全部为成功或已领则简短汇报总数；若有失败或待确认，列出站点名和响应片段并指出可能原因（如 Cookie 过期）。

时间由用户指定（默认建议早 8:00）。注意定时任务依赖客户端处于运行状态。

## 排错

先读 `logs/runs.jsonl` 最近记录，对照 `references/troubleshooting.md` 的故障表。最常见原因是 Cookie 过期，表现为 401/403 或响应变成登录页 HTML，处理方式是重新抓 Cookie 后用 `--set-cookie` 更新，不必改其他配置。

## 注意

- `config.json` 与 `browser-profile/` 含登录凭据，属敏感文件。不要提交到公开仓库，不要整份贴进聊天记录；分享配置时先清空 Cookie。
- 部分站点签到接口带 `sign` 签名，需按 `references/config-guide.md` 第六节处理。
- 单次领取失败不要立刻多次重试，可能触发风控。脚本默认只对网络错误和 5xx/429 重试两次。
- 仅用于领取自己账号的每日奖励，不要用于批量注册或刷量。
