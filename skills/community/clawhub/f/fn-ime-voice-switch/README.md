# fn-ime-voice-switch

> Claude Code skill：在 macOS 上用 Hammerspoon 实现「按住 Fn 切到豆包语音输入，松开切回默认输入法」的全自动方案。

## 解决的问题

**中文输入法的两难**：打字想用一个输入法（微信/搜狗/系统拼音，看中词库或生态），语音又想用豆包（识别准、标点准）。手动来回切是日常噪音，一天几十次。

**这个 skill 让 Fn 键替你切**：
- 按住 Fn → 自动切到豆包并触发豆包的语音输入
- 松开 Fn → 自动切回默认 IME

整套流程不需要模拟按键，只需要切输入法。豆包输入法本身允许把"语音输入快捷键"设为「长按 Fn」，所以程序只要把当前输入法切到豆包，豆包会自然响应那个 Fn 长按、开始录音。

## 安装

### 方式 1：作为 Claude Code skill 使用（推荐）

```bash
mkdir -p ~/.claude/skills/fn-ime-voice-switch
git clone https://github.com/I501579/fn-ime-voice-switch.git /tmp/fn-ime-voice-switch
cp -r /tmp/fn-ime-voice-switch/* ~/.claude/skills/fn-ime-voice-switch/
```

然后在 Claude Code 里说「设置 Fn 切换输入法」或「Fn 切到豆包语音」，Claude 会按 SKILL.md 的步骤一步步带你配置。

### 方式 2：手动套用

直接抄 [`templates/init.lua`](templates/init.lua) 到 `~/.hammerspoon/init.lua`，按里面的注释改一行 source ID。详细步骤见 [SKILL.md](SKILL.md)。

## 前置条件

- macOS（依赖 `hs.eventtap` 和 `hs.keycodes`）
- 默认 IME（微信、搜狗、系统拼音任选一个）
- 豆包输入法 PC 版（语音引擎绑定在豆包内）
- Homebrew

## 三个最容易踩的坑

1. **TCC 权限两处都要勾**：辅助功能 + 输入监控。漏勾输入监控，脚本能加载但完全监听不到 Fn。

2. **微信输入法用户必须先关它的 Fn 快捷键**：微信输入法在系统底层装钩子把 Fn 事件全部吃掉，任何用户态 eventtap 都收不到。搜狗等其他输入法实测不抢，可以跳过这步。

3. **输入法 source ID 别信 `defaults read`**：那份 plist 是缓存，与系统不实时同步，列表里可能根本没有刚装的输入法但实际能用。用 `hs -c "hs.keycodes.methods(true)"` 走系统 API 拿真实可用列表。

## 文件结构

```
fn-ime-voice-switch/
├── SKILL.md              # Claude Code skill 主文件（触发条件 + 完整流程）
├── README.md             # 这个文件
└── templates/
    └── init.lua          # Hammerspoon 配置模板
```

## 相关链接

- Hammerspoon：https://www.hammerspoon.org/
- 豆包输入法：https://www.doubao.com/chat/ime
- 公众号文章：[鱼和熊掌都要：Fn 一键切换默认输入法和豆包语音输入](https://mp.weixin.qq.com/s/...)（待发布）

## License

MIT

## 作者

宁静致远GC
