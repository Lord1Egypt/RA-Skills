## A-SOUL 粉丝应援工具 — 一键签到 + 视频点赞

给嘉然、贝拉、乃琳、心宜、思诺的直播间签到和视频三连，一句话搞定。

基于 [OpenClaw](https://openclaw.ai) 的自动化 Skill，纯 Python 标准库，零依赖。

### 支持的功能

**直播间签到** — 给 5 位成员的直播间发弹幕签到，刷亲密度

**视频点赞** — 批量给成员指定月份的新视频点赞

**视频投币/收藏**（可选）— 需要明确指定，不会默认消耗硬币

### 安装

1. 先装 [OpenClaw](https://docs.openclaw.ai)（如果还没装的话，不清楚怎么安装的可以在B站搜索 OpenClaw 相关视频教程）

2. 安装本 Skill：

```bash
clawhub install asoul-support
```

3. 设置 B站 Cookie（只需一次）：

在 Chrome 打开 [bilibili.com](https://www.bilibili.com)（确保已登录），按 F12 → Application → Cookies → bilibili.com，找到 `SESSDATA` 和 `bili_jct` 两个值，然后告诉你的 OpenClaw：

> 帮我保存B站Cookie，SESSDATA是xxx，bili_jct是xxx

### 使用方式

直接用自然语言对话：

| 你说 | 它做 |
|------|------|
| 给asoul直播间签到 | 5个直播间全部签到 |
| 给asoul 3月视频点赞 | 给3月全部新视频点赞 |
| 给嘉然的视频三连 | 点赞+投币+收藏 |
| 给asoul最近的视频投币 | 最近7天视频投币 |

也可以只指定部分成员：

> 给嘉然和贝拉签到

### 示例输出

```
🌟 A-SOUL 直播间签到结果

  ✅ 嘉然  — 签到成功  💬「签到」
  ✅ 贝拉  — 签到成功  💬「签到」
  ✅ 乃琳  — 签到成功  💬「签到」
  ✅ 心宜  — 签到成功  💬「签到」
  ✅ 思诺  — 签到成功  💬「签到」

🎉 全部签到成功！(5/5)
```

### 搭配定时任务（每天自动签到）

**方式一：直接对话**

告诉你的 OpenClaw：

> 帮我设置一个定时任务，每天早上10:30自动给asoul直播间签到，然后给本月新视频点赞

OpenClaw 会自动帮你创建 cron 任务，之后每天到点自动执行，结果推送到你的聊天频道。

**方式二：命令行**

```bash
openclaw cron add --name "A-SOUL每日签到" --cron "30 10 * * *" --exact \
  --message "帮我给asoul直播间签到，然后给本月新视频点赞" \
  --timeout-seconds 300 --announce --channel discord --to 你的频道ID
```

### 源码

GitHub: https://github.com/XiaoYiWeio/asoul-support

---

不清楚如何安装 OpenClaw 的同学可以在B站搜索相关视频教程。使用过程中遇到任何问题或报错，欢迎在帖子下评论，我看到会竭力回复！
