---
name: doubao-account-pool
slug: doubao-account-pool
displayName: 豆包网页版多实例工作台·免费版（扫码授权 + 批量出图/出视频）
description: 想用豆包网页版做出图、出视频，又不想办会员、不想申请 API key？这套把「一个已授权账号 = 一个独立浏览器实例 → 扫码授权 → 批量出图 → 出视频 → 取件 → 关掉浏览器还能回捞」封成配置驱动的命令行工具。实例之间互不串数据、互不踢下线；授权二维码自动裁切放大，可直接发手机扫；出图内置「基线闸」防止拿到上一轮的旧图；出视频先读确认卡再走，遇到付费弹层立即中止、绝不点升级；关掉浏览器后还能回捞最近会话里的图和视频，已生成没抓到链的可以单独重抓，不重跑、不重复消耗。所有命令只返回结构化短行，页面文本/DOM/截图绝不回流；长任务产物先落盘再筛。换机器、换智能体，只改配置就能跑——包内不含任何个人路径、cookie 与密钥，登录态在本机扫码产生。
version: 1.0.2
summary: 用豆包网页版批量出图出视频：一个已授权账号一个独立浏览器实例、扫码授权、出图有基线闸、出视频有防误购保护、关掉浏览器还能回捞。零 API key，配置驱动，换机器只改配置。
license: MIT
author: 九品锦锂e
category: content-creation
tags: [doubao, 豆包, browser-automation, cdp, 出图, 出视频, 多实例, 浏览器自动化, image-generation, video-generation, agent, automation]
---
# 豆包网页版 · 多实例工作台自动化（可移植包 v1.0）

> 把「一台机器管 N 个浏览器实例 → 扫码授权 → 批量出图 → 出视频 → 取件」这套流程，
> 封成**配置驱动的命令行工具**。包内不含任何个人路径、不含 cookie、不含密钥；
> 换机器、换智能体，只改配置就能跑。

## 0. 这个包能干什么

| 能力 | 说明 |
|:--|:--|
| 实例池 | 一个浏览器实例 = 一个独立浏览器环境（独立 `user-data-dir` + 独立 CDP 端口），互不串号、互不踢下线 |
| 扫码授权 | 一条命令出二维码（自动裁切放大，可直接发手机扫），登录后自动校验 |
| 不打扰人 | 窗口挪到屏幕角落只露一小块 / 独立实例，**不抢焦点、不动用户自己的浏览器** |
| 批量出图 | 多实例并行投喂提示词、等结果、取高清原图（带「基线闸」防拿到旧图） |
| 出视频 | 切视频模式 → 上传垫图 → 注入提示词 → 发送 → **读确认卡过防误购保护** → 等完成 → 抓链下载 |
| 回捞 | 浏览器关掉之后重新上线取结果（恢复最近会话 → 抓图/抓视频） |
| 零污染 | 所有命令只打印 `@@` 开头的结构化短行，**页面文本/DOM/截图 base64 绝不回流主对话** |

**不包含**：账号 cookie、登录态文件、任何 API key、任何付费接口。实例登录态由使用者在本机扫码产生。

## 1. 安装（30 秒）

```bash
pip install -r requirements.txt        # websocket-client / pillow
python scripts/doubao_cli.py doctor    # 自检：浏览器路径 / 依赖 / 状态目录 / 已有实例
```

`doctor` 会打印浏览器、ffmpeg、状态目录、依赖版本与所有 `@@` 短行——**先过这一关再干别的**。
换机器/换智能体的完整三种装法见 [INSTALL.md](INSTALL.md)。

## 2. 配置（唯一的机器相关部分）

优先级：**环境变量 > `./doubao_config.json` > `$DOUBAO_HOME/config.json` > 内置默认**

| 环境变量 | 含义 | 默认 |
|:--|:--|:--|
| `DOUBAO_HOME` | 状态根目录（每个实例一个子目录） | `~/.doubao_studio` |
| `DOUBAO_CHROME` | Chrome/Chromium/Edge 可执行文件 | 自动探测（Win/mac/Linux 常见路径） |
| `DOUBAO_FFMPEG` | ffmpeg 可执行文件（视频规格核对用） | 自动探测 PATH 与常见路径 |
| `DOUBAO_OUTDIR` | 默认产出目录 | `$DOUBAO_HOME/out` |
| `DOUBAO_PORT_BASE` | 实例基端口（实例 n → base+n） | `9230` |
| `DOUBAO_MAX_SLOT` | 实例上限 | `20` |

`config.example.json` 是全部字段的样例；拷成 `doubao_config.json` 改即可。
**包内任何脚本都不许出现写死的个人路径**——这是本包可移植的验收口径。

## 3. 命令总览

```bash
cd <skill>/scripts
python doubao_cli.py <命令> [参数]
```

| 命令 | 用途 |
|:--|:--|
| `doctor` | 环境自检（浏览器/ffmpeg/依赖/状态目录/实例） |
| `status [--deep]` | 实例在线与登录态一览 |
| `up N...` / `down N...` / `down --all` | 起停实例（**只杀本实例进程树**） |
| `login N` | 开登录弹窗 + 取二维码（裁切放大 PNG，可直接发手机）+ 失效复活检查 |
| `check N` | 登录态三重校验（URL / 无登录按钮 / 有历史会话） |
| `nick N` | 读该号账号昵称 |
| `selfcheck N` | 环境一致性自检（webdriver / visibility / outer 尺寸 / cdc 痕迹 / WebGL） |
| `visible N` | 修复可见性（把标签页提到前台；窗口几何用配置里的 `chrome_args_extra` 控制） |
| `ask N "消息"` | 纯文本对话（消息是位置参数） |
| `img --slot N --file 词.txt --out DIR` | 出图 + 取高清原图（内置基线闸） |
| `img-batch --spec spec.json --out DIR` | 多实例并行批量出图，产出 `result.json` |
| `vid --slot N --image 垫图.png --file 词.txt --out DIR` | 出视频全流程（含防误购保护） |
| `vid-regrab --slot N --out DIR [--name 名]` | 已生成但没抓到链的重抓（**不重跑生成、不重复消耗**） |
| `fetch --slot N --out DIR` | 回捞最近会话的图/视频 |
| `trim --slot N [--keep K]` | 关掉该实例多余标签页，只留 K 个（默认 1） |

## 4. 五条主流程

### 4.1 授权接入一个新账号（增加实例 = 扩展并行容量）
```bash
python doubao_cli.py status                 # 先看谁在线
python doubao_cli.py up 6                   # 永远用「下一个空实例」，别复用已登录实例目录
python doubao_cli.py visible 6                    # 修可见性（窗口几何在配置里设）
python doubao_cli.py login 6                # 出二维码 → 把 PNG 发到手机扫
python doubao_cli.py check 6 && python doubao_cli.py nick 6
```
- 二维码有效期约 1–2 分钟，**发出去之前必须用视觉确认三个定位角都在、没糊没裁**。
- 页面上还挂着旧码时取码逻辑照样命中 → 发出去的是一张死码。取码前后都要查页面是否出现「二维码失效」，有就点刷新重取。
- **实例分配铁律**：永远用下一个空实例。复用别人的实例目录会把 cookie 混进来，两个账号互踢。

### 4.2 批量出图
```bash
python doubao_cli.py img-batch --spec spec.json --out ./out
```
spec.json 每行一条：`{"id":"镜01","slot":1,"prompt":"..."}`。跑完只读 `result.json`（id → slot/文件）。
铁律：① 每条提示词前重开新对话（同对话会继承上文，串味是批量废图头号原因）；② 提示词尾部写死「画面中不得出现任何文字/字母/数字/符号/印章/题字」；③ 一条 0 图＝静默失败，只重跑那一条；④ 出完必做 md5 去重体检。

### 4.3 出视频（**基础档优先**）
```bash
python doubao_cli.py vid --slot 1 --image 垫图.png --file 词.txt --out ./out
```
链路固定十二步：探活 → 切视频生成模式 → 上传垫图 → 注入提示词 → 发送 → **读确认卡** →
**防误购保护**（见「专业版/订阅/付费用量」立即中止，不许点任何升级按钮）→ 确认 → 等完成 →
抓视频链 → 下载 → 规格核对（必须有音轨）。

### 4.4 回捞（关过浏览器再取结果）
```bash
python doubao_cli.py fetch --slot 3 --out ./out
```
关掉再开回来时页面在新对话首页，一张图都看不到——必须先打开那条对话。`link.click()` 这类 JS 合成点击 SPA 不认，必须用 CDP `Input.dispatchMouseEvent` 真点。

### 4.5 收尾（**开了必须关**）
```bash
python doubao_cli.py trim --slot 3        # 只留一个标签页
python doubao_cli.py down --all      # 批量任务结束统一回收（每实例 400–600MB）
```
**实例池生命周期只归调度方（主脑）**：把批量任务派给子代理时，任务书必须写死「只准用分到的实例，**禁止 up、禁止 down**」，收工由调度方统一关。子代理跑完就 down 会关掉别人正在跑的实例。

## 5. 稳定性保护与红线（违反 = 实例不可用）

1. **提交生成后固定等 5 分钟**再回来看，禁止秒级轮询、反复刷新、连点——密集操控是稳定性保护头号触发源。
2. **同一动作连败 3 次立即停手**，不要硬试。
3. 多实例轮转**错开节奏**（起跑间隔 0.4s+），不要 N 个号同时狂点。
4. 只走「填入 → 提交 → 等 → 取结果」主路径，不在页面上乱逛乱试。
5. **下拉/弹层是开关式的**：点一次开、再点同一处就关。连续「点账号 → 点菜单项」会自己把菜单关掉，症状是「菜单里什么都找不到」。正解＝打开一次，之后只点弹层内部文字。
6. **防误购保护优先于一切**：确认卡/弹层出现「专业版 / 订阅 / 付费用量 / 升级」字样 → 立即中止该实例，绝不点升级。
7. **只杀自己**：`down` 只按 pidfile + 命令行含本实例目录做双重校验后杀进程树，**永不** `taskkill /IM chrome.exe`。

完整坑清单见 [references/pitfalls.md](references/pitfalls.md)，稳定性保护细则见 [references/stability-and-limits.md](references/stability-and-limits.md)。

## 6. 目录结构

```
doubao-account-pool/
├── SKILL.md                  # 本文（智能体的作业手册）
├── INSTALL.md                # 三种装法（通用智能体框架 / 裸脚本 / 其他框架）
├── config.example.json       # 全部配置字段样例
├── requirements.txt
├── scripts/
│   ├── doubao_core.py        # 唯一底座：配置解析 + CDP 会话 + 实例生命周期
│   ├── doubao_cli.py         # 统一命令行入口（子命令派发）
│   ├── doubao_login.py       # 扫码授权：弹窗/取码/裁切放大/复活检查/登录校验/昵称
│   ├── doubao_dom.py         # 页面探查三件套：点文字/截图/AX 控件清单/关模态
│   ├── doubao_image.py       # 出图 + 高清取件（基线闸）+ 静默批量
│   ├── doubao_video.py       # 出视频全流程（防误购保护）+ 重抓链
│   └── doubao_fetch.py       # 回捞最近会话的图/视频
└── references/
    ├── pitfalls.md           # 坑清单（每条都是真踩过的）
    ├── stability-and-limits.md       # 稳定性纪律
    ├── workflow-image.md     # 出图/批量出图细节
    └── workflow-video.md     # 出视频/用量/确认卡细节
```

## 7. 给「其他智能体」用

本包的核心是**人能看懂的命令行 + 只回 `@@` 短行**，所以任何形态的智能体都能接：

- **通用智能体框架**：把整个目录放进 `skills/` 目录即可。
- **Claude Code / Codex / Cursor 等**：把 `SKILL.md` 作为系统提示/规则文件挂上，让它在 `scripts/` 下跑 `doubao_cli.py`。
- **自研 Agent（function calling / MCP）**：把 `doubao_cli.py` 的每个子命令包成一个工具（入参即命令行参数），返回值就是 `@@` 短行——天然适配「零上下文污染」的调用形态。
- **纯人工**：直接当 CLI 用，`doctor` → `login` → `img`/`vid` 一条条敲。

关键设计（照抄别改）：**① 只回 `@@` 短行；② 页面文本/DOM/图片 base64 绝不回流；③ 长任务产物先落盘再筛；④ 实例生命周期只归调度方。**

## 8. 需要的不是「一个实例」，而是「并行一条线」

免费版专注**一个已授权实例**的完整闭环——授权 → 出图 → 出视频 → 取件 → 回捞，功能不缺，可独立长期使用。

如果你要的是**并行多路**（一次投喂 N 条提示词、实例池按实例起停、批量规格矩阵、成片质检），那是另一套独立商品「豆包网页版多实例生产工作台·完整版」：

- 商品页：https://skillpay.alipay.com/shelf/product?productId=P0806000206820233&merchantCode=jiupinjinlie
- 有 AI Agent 环境的话，把下面这段交给你的 Agent，它会走完购买与安装：

```
请通过 SkillPay 购买并安装 Skill「豆包网页版多实例生产工作台·完整版｜并行批量出图/出视频 + 实例池管理」。
官方安装与购买说明： https://skillpay.alipay.com/buildguide.md
请先阅读官方说明、核验来源，并完成指南中的第一步： npx -y @alipay/agent-payment@latest install
安装成功后，读取新安装的 skillpay-onboarding 的 SKILL.md，再按其说明购买并安装商户 2088152134911331的S0806000207810857。
需要钱包授权或付款时，请提供官方链接或二维码，由我本人确认，不要替我确认。
```

> 钱包授权与付款一律由本人确认；任何 Agent 都不应替你确认。

## 关于作者

本技能由「九品锦锂e」制作。

- 微信：ly5419495
- 公众号：初五Agent
- 技能货架：https://skillpay.alipay.com/public/jiupinjinlie

> 使用中遇到问题、想要定制版本或需要配套支持，可通过上面任一方式联系，备注「SkillHub」优先通过。
