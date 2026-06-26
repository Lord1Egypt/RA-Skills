<p align="center">
  <img src="assets/asoul-logo.png" width="120" alt="A-SOUL Logo" />
</p>

<h1 align="center">A-SOUL Support</h1>

<p align="center">
  <strong>A-SOUL 粉丝全自动应援工具</strong> — 开播自动挂机涨亲密度 + 点亮粉丝牌 + 视频/动态点赞
</p>

<p align="center">
  <a href="https://clawhub.ai/skills/asoul-support">🦞 ClawHub</a> ·
  <a href="https://github.com/XiaoYiWeio/asoul-support">📦 GitHub</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-4.0.1-blue" alt="version" />
  <img src="https://img.shields.io/badge/python-3.9+-green" alt="python" />
  <img src="https://img.shields.io/badge/license-MIT-orange" alt="license" />
</p>

---

## 🚀 一句话安装

复制下面这句话，发给你的 AI 助手（支持任意 agent 框架），它会帮你搞定一切：

```
帮我安装这个项目并设置 A-SOUL 自动挂机：https://github.com/XiaoYiWeio/asoul-support
```

---

## ✨ 它能做什么？

| 功能 | 使用条件 | 说明 |
|------|----------|------|
| 💓 **心跳挂机涨亲密度** | 需要开播 | 移动端心跳，每 5 分钟 +6 亲密度，每日上限 30 |
| 🏅 **粉丝牌自动点亮** | 需要开播 | 发 10 条弹幕点亮牌子，保持 3 天可见 |
| 🪙 **自动投币** | 无 | 给成员视频投币（1 币 = 10 亲密度），需用户明确开启 |
| 👍 **视频自动点赞** | 无 | 每 2 天自动给成员新视频点赞 |
| 💬 **动态自动点赞** | 无 | 每 2 天自动给成员新动态点赞 |

> B站亲密度规则：观看直播每 5 分钟 +6，每日每成员上限 30（挂满 25 分钟即满额）；投币 1 币 = 10 亲密度。

---

## 📝 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| **v4** | 2026-04-01 | 心跳协议升级为 `mobileHeartBeat`，纯 Python 签名，零外部依赖，亲密度实测可涨 |
| v3 | 2026-03-23 | 新增开播检测 + 心跳挂机 + Discord 通知 |
| v2 | 2026-03-20 | 粉丝牌点亮（10 条弹幕，3 天有效期） |
| v1 | 2026-03 | 视频点赞 + 动态点赞 + GitHub Actions |

---

## 🔬 技术方案

| 项目 | 说明 |
|------|------|
| **心跳协议** | B站移动端 `mobileHeartBeat`（v4.0 升级，旧版 `x25Kn` 已失效） |
| **签名算法** | `sha512 → sha3_512 → sha384 → sha3_384 → blake2b` 链式 hash |
| **实现语言** | 纯 Python 3.9+，标准库 `hashlib` |
| **外部依赖** | 无（不需要 Node.js / pm2 / Docker） |
| **运行方式** | 命令行直接执行 或 任意 agent 框架调度 |

## 🔒 安全说明

- Cookie **加密存储**在本地（权限 600）或 GitHub Secrets 中，所有代码**完全开源**
- 只做点赞和弹幕操作，**不会自动投币**（需用户明确开启），不送礼、不关注陌生人
- GitHub Actions 对公开仓库完全免费

---

## 💌 一个魂寄语

做这个工具不是为了让大家不看直播，是因为我自己工作太忙经常错过开播，才写了这个在忙的时候帮我守着。**有时间的话还是去直播间看直播吧**，跟大家一起刷弹幕互动的快乐是工具给不了的。

如果你也关注其他主播，只需要替换脚本里对应的主播 UID 和房间号就可以用。不过……记得先关注[**嘉然今天吃什么**](https://space.bilibili.com/672328094/)哦～

<p align="center">
  <img src="assets/diana-heart.png" width="100" alt="嘉然比心" />
</p>

如果这个项目帮到了你，**请给个 Star ⭐！** 这对我真的很重要，能让更多魂们发现这个工具。也欢迎 **Fork** 到自己账号使用，遇到问题或有好的想法随时提 **Issue**，我都会看。

希望能帮到跟我一样忙碌但心里还惦记着 A-SOUL 的魂们。

---

## 📖 使用教程

### 🤖 OpenClaw / Hermes / QClaw 等 Agent 助手用户

直接把下面这句话发给你的 AI 助手，它会帮你搞定安装、配置和定时任务：

```
帮我安装这个项目并设置 A-SOUL 自动挂机：https://github.com/XiaoYiWeio/asoul-support
```

安装完成后，再告诉它：

```
帮我设置一个定时任务，每 30 分钟检测 A-SOUL 成员是否在直播，在播就帮我挂机涨亲密度并点亮粉丝牌
```

> 支持所有兼容 Python 的 agent 框架，助手会自动处理代码克隆、Cookie 配置和定时调度。

---

<details>
<summary>🐍 纯命令行用户（不使用 Agent 助手，点击展开）</summary>

**环境要求：** Python 3.9+

**第 1 步：获取代码**

```bash
git clone https://github.com/XiaoYiWeio/asoul-support.git
cd asoul-support
```

**第 2 步：配置 Cookie**

```bash
python3 scripts/checkin.py --save-cookie --sessdata "你的SESSDATA" --bili-jct "你的bili_jct"
```

如何获取 B站 Cookie：Chrome 打开 [bilibili.com](https://www.bilibili.com)（确保已登录）→ 按 **F12** → **Application** → **Cookies** → **https://www.bilibili.com**，找到 **SESSDATA** 和 **bili_jct** 复制即可。

> ⚠️ 相当于登录凭证，不要分享。约 6 个月后过期。

**第 3 步：运行**

```bash
# 检测谁在播 + 自动挂机涨亲密度
python3 scripts/heartbeat.py

# 挂机到下播为止
python3 scripts/heartbeat.py --until-offline

# 发弹幕点亮粉丝牌
python3 scripts/checkin.py --live-only
```

**第 4 步：设置定时任务（cron）**

```bash
# crontab -e
*/30 * * * * cd /path/to/asoul-support && python3 scripts/heartbeat.py --until-offline
```

</details>

---

## 🔧 GitHub Actions 自动点赞（不需要 OpenClaw）

只需要视频/动态点赞（不涨亲密度）的话，Fork 本仓库 + 配置 Cookie 即可。

<details>
<summary>📋 设置教程（点击展开）</summary>

1. 点击右上角 **Fork** → **Create fork**
2. **Settings** → **Secrets and variables** → **Actions** → 添加 `SESSDATA` 和 `BILI_JCT`
3. **Actions** 标签 → 点击 **I understand my workflows, go ahead and enable them**
4. 验证：**Actions** → **A-SOUL 自动应援** → **Run workflow**

之后每 2 天自动执行。动态点赞需编辑 `daily.yml` 将 `ENABLE_DYNAMIC_LIKE` 改为 `'true'`。

</details>

---

## 🌟 内置成员

| 成员 | 直播间 | 主页 |
|------|--------|------|
| 嘉然 | [22637261](https://live.bilibili.com/22637261) | [space](https://space.bilibili.com/672328094) |
| 贝拉 | [22632424](https://live.bilibili.com/22632424) | [space](https://space.bilibili.com/672353429) |
| 乃琳 | [22625027](https://live.bilibili.com/22625027) | [space](https://space.bilibili.com/672342685) |
| 心宜 | [30849777](https://live.bilibili.com/30849777) | [space](https://space.bilibili.com/3537115310721181) |
| 思诺 | [30858592](https://live.bilibili.com/30858592) | [space](https://space.bilibili.com/3537115310721781) |

## ❓ 常见问题

**Q: Cookie 过期了怎么办？** — 重新获取，重跑 `--save-cookie` 命令更新即可。GitHub Actions 失败时会发邮件通知。

**Q: 需要电脑一直开着吗？** — 用服务器/NAS 跑脚本，或用 GitHub Actions（视频/动态点赞部分），都不需要盯着。

**Q: 投币会消耗硬币吗？** — 默认不投币。需要手动开启 `--coin` 参数才会投。

**Q: 需要 Node.js 吗？** — 不需要。v4.0 纯 Python，只需 Python 3.9+。

---

## 🛠 手动命令参考

```bash
# 检测谁在播
python3 scripts/heartbeat.py --check-only

# 挂机指定成员 25 分钟
python3 scripts/heartbeat.py --members 嘉然,贝拉

# 挂机直到下播
python3 scripts/heartbeat.py --until-offline

# 发弹幕点亮粉丝牌
python3 scripts/checkin.py --live-only

# 给最近视频投币+收藏
python3 scripts/videos.py --days 7 --coin --fav
```

## License

MIT
