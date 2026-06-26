---
name: fn-ime-voice-switch
description: macOS 上用 Hammerspoon 实现按住 Fn 切到豆包语音输入、松开切回默认输入法的自动化方案。用户说「设置 Fn 切换输入法」/「Fn 切到豆包语音」/「按 Fn 切豆包」/「macOS 输入法 Fn 自动化」/「Hammerspoon 切输入法」/`/fn-ime-voice-switch` 时触发。包含权限设置、输入法 ID 查找、微信输入法 Fn 拦截绕过、init.lua 模板。
---

# Fn 键一键切换默认输入法和豆包语音输入

在 macOS 上让"打字默认 IME + 语音用豆包"的两难变成一个键：按住 Fn 切到豆包并触发语音，松开自动切回默认 IME。整套流程不需要模拟按键，只切输入法。

## 触发条件

当用户说以下任意一种时启动：

- `/fn-ime-voice-switch`
- "设置 Fn 切换输入法"
- "Fn 切到豆包语音"
- "按 Fn 切豆包"
- "macOS 输入法 Fn 自动化"
- "Hammerspoon 切输入法"

## 关键洞察

**豆包输入法本身允许把"语音输入快捷键"设为「长按 Fn」**。所以用户态程序只要把当前输入法切到豆包，豆包会自然响应那个 Fn 长按、开始录音。整套方案：

```
按住 Fn → Hammerspoon 监听到 flagsChanged → 切到豆包 → 豆包响应 Fn 长按开始录音
松开 Fn → Hammerspoon 监听到 flagsChanged → 切回原 IME
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| 默认输入法 | ✅ | 用户日常打字用的 IME（微信、搜狗、系统拼音等） |
| 豆包是否已装 | ✅ | 必须先装豆包输入法 PC 版 |
| 默认 IME source ID | ❌ | 不确定时通过 `hs.keycodes.methods(true)` 查 |

## 执行流程

### Phase 1 — 环境准备检查

按顺序检查并引导用户：

1. **确认两个输入法已装并加入系统**
   - 默认 IME（微信/搜狗/系统拼音任选）
   - 豆包输入法（豆包官网 PC 版）
   - 确认在 系统设置 → 键盘 → 文本输入 → 输入法 中两者都存在

2. **安装 Hammerspoon**（用户目录方案，避开 sudo）

   ```bash
   brew install --cask --appdir=$HOME/Applications hammerspoon
   open ~/Applications/Hammerspoon.app
   ```

   说明：`--appdir=$HOME/Applications` 把 app 装到用户目录。brew cask 默认要 sudo 拷到 `/Applications`，没法弹密码的环境会失败。装到 `~/Applications` 一样能用，菜单栏有图标，brew 一样能升级。

3. **授权 TCC 权限**

   去 系统设置 → 隐私与安全性，在以下两处都勾上 Hammerspoon：
   - **辅助功能**（Accessibility）
   - **输入监控**（Input Monitoring）⚠️ 漏勾的话脚本能加载但完全监听不到 Fn

### Phase 2 — 关掉默认 IME 自己的 Fn 快捷键（关键，决定成败）

**这是整套方案最容易踩的坑。**

**如果默认是微信输入法**：它出厂就绑了「长按 Fn = 语音输入」，并且是在**系统底层**装钩子把 Fn 事件全部吃掉。任何用户态 eventtap 都收不到——表现就是按 Fn 微信自己的录音条出来，Hammerspoon 半点反应没有。

  **必须先关它**：进微信输入法偏好设置 → 语音输入/快捷键 → 把「长按 Fn」改成别的或直接关掉。一关 Fn 立马正常下发。

**如果默认是搜狗、系统拼音、其他**：实测不抢 Fn，可以跳过。但保险起见，看一眼那个输入法的快捷键面板，确认没有把 Fn 绑给它自己就行。

**排查思路**：在 init.lua 里加事件计数器，按 Shift 看数字涨不涨，再按 Fn 比对。Shift 涨、Fn 不涨就是被某个高优先级钩子抢了，99% 是某个输入法自己。

### Phase 3 — 设置豆包的语音快捷键

豆包菜单栏图标 → 偏好设置 → 语音输入 → 快捷键 → 选「**长按 Fn**」。

### Phase 4 — 写 init.lua

把模板放到 `~/.hammerspoon/init.lua`：模板见 [templates/init.lua](templates/init.lua)。

需要替换的占位符：
- `{{DEFAULT_INPUT}}` → 用户默认 IME 的 source ID

常见 IME source ID 速查：

| 输入法 | source ID |
|--------|-----------|
| 微信输入法 | `com.tencent.inputmethod.wetype.pinyin` |
| 搜狗输入法 | `com.sogou.inputmethod.sogou.pinyin` |
| 系统拼音 | `com.apple.inputmethod.SCIM.ITABC` |
| 豆包输入法 | `com.bytedance.inputmethod.doubaoime.pinyin` |

不确定就跑：

```bash
hs -c "hs.keycodes.methods(true)"
```

⚠️ **不要信 `defaults read com.apple.HIToolbox AppleEnabledInputSources`**——这份 plist 是缓存，与系统不实时同步，列表里可能根本没有刚装的输入法但实际能用。靠它判断会误判。`hs.keycodes.methods(true)` 走系统 API 拿真实可用列表。

### Phase 5 — Reload + 测试

```bash
hs -c 'hs.reload()'
```

或者 Hammerspoon 菜单 → Reload Config。

切到默认输入法，找个文本框按住 Fn 测试：屏幕右上角弹出"切到豆包"，开始录音；松开切回默认。

### Phase 6 — 故障诊断

如果按 Fn 没反应：

1. **测试基础 eventtap 是否工作**：在回调里加计数器，按 Shift/Cmd 看是否涨。涨说明权限 OK，flagsChanged 通路正常。
2. **再按 Fn 比对**：若 Shift 涨、Fn 不涨 → 被高优先级钩子抢了 → 回去 Phase 2 关默认 IME 的 Fn 快捷键。
3. **检查 TCC**：辅助功能 + 输入监控两处都得勾，缺一个 Fn 就收不到。
4. **检查 `AppleFnUsageType`**：如果 macOS 系统设置里把 Fn 设成"什么都不做"或"显示 Emoji"，可能影响事件下发。改回"开始听写"或类似选项。

调试小技巧：Hammerspoon 装好后会软链 CLI 到 `/opt/homebrew/bin/hs`，可以从外部直接发命令验证：

```bash
hs -c 'hs.keycodes.currentSourceID("com.bytedance.inputmethod.doubaoime.pinyin")'
hs -c 'hs.keycodes.currentSourceID()'
hs -c 'hs.reload()'
```

切输入法、读当前状态、reload 配置全不用动鼠标。

## 输出

完成后，用户体验：
- 默认输入法打字一切照旧
- 按住 Fn → 切到豆包并开始录音
- 松开 Fn → 切回默认 IME 继续打字
- 全过程一个键，没有可感知的延迟

## 已知限制

- 仅支持 macOS（依赖 `hs.eventtap` 和 `hs.keycodes`）
- 必须装豆包输入法 PC 版（语音引擎绑定在豆包内）
- 微信输入法用户必须先关它的 Fn 快捷键（系统级钩子无法绕过）
- Touch Bar Mac 上 Fn 行为不同，未测试

## 参考资料

- 完整公众号文章：[wechat-articles/claude-code-fn-ime-switch/article.md](https://github.com/I501579/fn-ime-voice-switch)（如已发布）
- Hammerspoon 文档：https://www.hammerspoon.org/docs/
- `hs.keycodes` API：https://www.hammerspoon.org/docs/hs.keycodes.html
- `hs.eventtap` API：https://www.hammerspoon.org/docs/hs.eventtap.html
