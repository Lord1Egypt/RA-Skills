---
name: douyin-web-control
description: Use this skill when the user wants an Agent to operate Douyin web through the douyin-web CLI, including launching or focusing Douyin, login checks, feed navigation, search, current video info, playback control, comments, likes, following the current author, favorites, sharing, danmaku, screenshots, or screen/audio recording. Prefer the CLI over direct browser automation for Douyin control. Do not use it for video-watching strategy, recommendation guidance, persona behavior, or video creation ideas.
---

# 抖音网页版控制

`douyin-web` 是抖音网页版的底层动作库。这个 skill 的职责是指导 Agent 正确调用 CLI：执行动作、读取 JSON、查看截图、记录限制。它不负责“该看什么视频”“为什么点赞”“怎么做内容创作”等策略问题。

CLI 项目地址：

```text
https://github.com/billwang233/douyin-web-cli
```

如果系统里还没有安装 CLI，先安装：

```bash
python3 -m pip install "git+https://github.com/billwang233/douyin-web-cli.git"
python3 -m playwright install chromium
douyin-web --help
```

## 先决策

使用本 skill 的场景：

- 用户要 Agent 操作抖音网页版。
- 用户要测试、验证、扩展 `douyin-web` CLI。
- 用户要打开抖音、检查登录、控制播放器、截图、录制、点赞、关注当前视频作者、收藏、分享、评论或弹幕。

不要用本 skill 的场景：

- 制定刷视频策略。
- 做推荐判断或内容偏好分析。
- 生成视频创意、脚本、选题。
- 处理创作者中心的完整发布流程。

## 命令入口

优先使用 skill 自带包装脚本：

```bash
skills/douyin-web-control/scripts/douyin-web --json COMMAND
```

包装脚本会按顺序寻找 CLI：

- `$DOUYIN_WEB_CLI`
- `$DOUYIN_CLI_ROOT/bin/douyin-web`
- 当前工作区或父目录下的 `bin/douyin-web`
- 已安装到 `PATH` 的 `douyin-web`
- 已安装到 `PATH` 的 `cli-anything-douyin-web`

如果需要指定浏览器会话目录，用：

```bash
--home ${DOUYIN_WEB_HOME}
```

如果没有指定，CLI 会使用自己的默认 home。测试时可以用隔离的临时 home：

```bash
--home ${DOUYIN_WEB_HOME:-/tmp/douyin-web-home}
```

并行多个项目时，优先使用全局 `--profile`，并且后续每条命令都带同一个 profile：

```bash
douyin-web --profile project-a --json launch
douyin-web --profile project-a --json open recommend
douyin-web --profile project-a --json current

douyin-web --profile project-b --json launch
douyin-web --profile project-b --json open jingxuan
douyin-web --profile project-b --json current
```

`--profile NAME` 会把会话、截图和浏览器数据隔离到 `~/.douyin-web-cli/profiles/NAME/`。不要在同一条命令里混用 `--profile` 和 `--home`。

## 工作原则

- 优先通过 CLI 操作抖音，不要绕过 CLI 直接点网页；只有调试 CLI 实现时才直接检查 DOM 或页面。
- 并行项目必须全程使用各自的 `--profile`；如果后续命令漏掉 profile，会回到默认会话。
- 页面动作默认截图。读取 JSON 里的 `data.screenshot.path` 做视觉确认。
- 如果弹出登录页、验证码、滑块验证、短信验证、账号风控或任何真人验证，不要尝试绕过、自动识别或自动填写。立即停下来提示用户人工处理；用户确认完成后，再运行 `douyin-web --json status` 或 `douyin-web --json wait-login --timeout 300` 确认状态，然后继续后续动作。
- 对账号有影响的动作，例如 `like`、`follow-author`、`favorite`、`share`、`comment --submit`、`danmaku-send --submit`，执行前确认用户允许。
- 对视觉状态不稳定的动作，例如 `danmaku off`、`loop`、点赞/收藏高亮状态，只报告 CLI 结果和截图，不要声称绝对确认。
- 如果用户要求“测试 CLI”，必须用 `douyin-web` 命令执行测试。

## 常用工作流

登录、验证码和风控处理：

```bash
douyin-web --json status
douyin-web --json wait-login --timeout 300
```

如果 `status` 显示未登录，或者截图里出现验证码/登录/验证页面，停止当前自动化流程，向用户说明需要人工登录或验证。不要继续点击、不要尝试破解验证码。用户确认处理完成后，再重新运行 `status` 或 `wait-login`。

检查会话和登录：

```bash
douyin-web --json state
douyin-web --json status
douyin-web --json wait-login --timeout 300
```

打开页面：

```bash
douyin-web --json launch
douyin-web --json open recommend
douyin-web --json open jingxuan
douyin-web --json open ai-search
douyin-web --json open follow
douyin-web --json open friends
douyin-web --json open mine
douyin-web --json open live
douyin-web --json open vs
douyin-web --json open series
```

查看当前状态：

```bash
douyin-web --json current
douyin-web --json info
douyin-web --json screenshot /tmp/douyin-current.png
```

播放器控制：

```bash
douyin-web --json play state
douyin-web --json play pause
douyin-web --json play resume
douyin-web --json play toggle
douyin-web --json next
douyin-web --json prev
douyin-web --json seek --seconds 30
douyin-web --json seek --percent 50
douyin-web --json rate 1.25
douyin-web --json volume 0.8
douyin-web --json sound on
douyin-web --json sound off
```

修改倍速或音量后，测试结束时尽量恢复：

```bash
douyin-web --json rate 1
douyin-web --json volume 1
```

显示和沉浸控制：

```bash
douyin-web --json clean
douyin-web --json fullscreen
douyin-web --json danmaku off
douyin-web --json loop
douyin-web --json prepare
douyin-web --json dismiss
douyin-web --json press Escape
```

搜索和互动：

```bash
douyin-web --json search "关键词"
douyin-web --json search "关键词" --no-submit
douyin-web --json comments open
douyin-web --json comments close
douyin-web --json comment "评论草稿" --no-submit
douyin-web --json danmaku-send "弹幕草稿" --no-submit
douyin-web --json like
douyin-web --json follow-author
douyin-web --json favorite
douyin-web --json share
```

录制：

```bash
douyin-web --json devices
douyin-web --json record /tmp/douyin-record.mp4 --duration 15 --video-index VIDEO_INDEX --audio-index AUDIO_INDEX --verify
```

录制注意事项：

- 系统音频优先用 `BlackHole 2ch`。
- 默认拒绝非 BlackHole 音频，避免误录麦克风。
- 每次录制前先跑 `devices`，因为 AVFoundation 设备编号可能变化。
- 桌面自动化环境可能把前台窗口切回工具本身，所以 MP4 生成成功不一定代表画面就是抖音；需要截图、抽帧或人工验证。

## 测试建议

自动测试：

```bash
cd ${DOUYIN_CLI_ROOT}/agent-harness
python3 -m pytest -q -rs
```

真实 CLI 测试：

- 一次测试一个动作，或只做小批量连续动作。
- 查看 JSON 的 `ok`、`message` 和关键 `data` 字段。
- 查看 `data.screenshot.path`。
- 如果失败，优先修 CLI 或记录为 CLI 限制，不要用直接浏览器操作掩盖失败。

## 功能矩阵

需要完整功能范围、适合/不适合 CLI 化的边界、下一批待补命令时，读取：

```text
references/feature-matrix.md
```
