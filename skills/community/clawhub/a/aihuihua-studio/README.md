# aihuihua-studio v1.0.18 —— 在 Agent 里用 鼓鼓AI 生图、做视频、写歌

装上之后，在 Claude Code、Codex、WorkBuddy 这类 AI 工具里直接说「帮我画一张……」「把这张图做成视频」
「写首歌」，它就会用你在 鼓鼓AI（https://aihuihua.ai/）的账号调网站上的模型，按网站价格扣你的积分，
结果下载到本地。

- **登录**：第一次用时 Agent 给你一条授权链接，在浏览器里核对授权码、点「授权」就行，不用把密码交给 Agent；
- **模型**：GPT Image 2.5 Flare、GPT Image 2.5 Sunburst、GPT Image 2、Nano Banana Pro、GPT-4o 图片、即梦 Seedream 5.0、Midjourney、即梦 Seedance 2.5、即梦 Seedance 2.0、即梦 Seedance 2.0 Fast、即梦 Seedance 2.0 mini、即梦 Seedance 1.0 Pro、MiniMax H3、Suno 音乐、文字转语音，以及图片高清放大、AI 换脸、AI 抠图；
- **积分**：随时问「我还有多少积分」；不够了 Agent 会列出套餐，你选好后它生成微信支付二维码，扫码付款即可；
- **自动更新**：网站加了新模型、调了参数，技能会自己更新。

## 安装

把下面这句话发给你的 AI 工具：

```
安装并使用 鼓鼓AI AI 创作技能：https://oc.superx360.com/agent-skills/aihuihua-studio/aihuihua-studio.tar.gz
```

或者自己装（解到工具的技能目录，例如 `~/.claude/skills`）：

```bash
curl -fsSL https://oc.superx360.com/agent-skills/aihuihua-studio/aihuihua-studio.tar.gz | tar -xzf - -C ~/.claude/skills
```

要求 Node 20 以上，零依赖。

## 自己在命令行里用

```bash
S="node ~/.claude/skills/aihuihua-studio/scripts/studio.mjs"
$S login                     # 授权码登录
$S whoami                    # 余额
$S models                    # 全部模型、参数和价格
$S gen gpt-image-2.5-flare --prompt "一只戴墨镜的柴犬"
$S gen seedance-2.0-fast --prompt "海边日落延时" --duration 5
$S gen suno --prompt "轻快的夏日流行歌"
$S buy --list                # 充值套餐
$S history                   # 我的作品
```

详细说明见 `SKILL.md`。
