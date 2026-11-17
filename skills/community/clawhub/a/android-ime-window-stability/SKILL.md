---
name: android-ime-window-stability
description: 修复 Android 输入法中候选区、预编辑编辑器或工具面板的测量变化导致的窗口跳动、闪烁或短暂消失；适用于原生输入法宿主的布局缺陷，需要补回归测试并在模拟器验收时使用。
---

# Android 输入法窗口稳定性

先确认问题是输入法窗口边界变化，而不是动画、重绘或宿主编辑器本身的问题。读取仓库的 `AGENTS.md`、`docs/ARCHITECTURE.md` 和 `.github/CONTRIBUTING.md`；在水杉输入法仓库中，产品宿主位于 `platforms/android`，不要启动或验收 Tauri 生成工程。涉及行为、布局层级或测试策略的修复要带 `.agents/notes/implemented/bug-fix/` 决策笔记，并先搜索已有的 Android 编辑器、候选区和窗口布局笔记。

## 定位

- 记录打开和关闭动作前后的 `AccessibilityWindowInfo.TYPE_INPUT_METHOD` bounds，连续采样确认是否出现底边、顶边或窗口存在状态变化。
- 沿着 `onCreateInputView` 的父子关系检查测量链。候选栏、工具栏和预编辑行放在纵向 `LinearLayout` 时，`GONE`/`VISIBLE` 会改变父项高度；这通常就是键盘抬起、回落或完成按钮导致闪烁的根因。
- 区分必须参与键盘主体测量的内容与临时覆盖内容。编辑器、放大拼写条和功能面板若只是覆盖顶部行，应放进键盘表面的 `FrameLayout`，使用包裹高度参数，并在候选区布局完成后按实际位置设置 `topMargin`。

## 修复

优先让临时编辑器成为覆盖层，而不是把它改成永久占位的 `INVISIBLE` 行。覆盖层可以继续用 `GONE`/`VISIBLE`，因为它不参与键盘主体测量；普通键盘不应为未打开的编辑器留下空白。对齐位置应跟随候选区实际的 `top`/`bottom`，并在旋转、换布局、候选行高度变化时重新对齐。检查 `FrameLayout` 子项顺序：编辑器应盖住它要编辑的顶部行，后加入的功能面板按产品设计决定是否覆盖它；隐藏覆盖层必须不拦截触摸和无障碍焦点。保持既有无障碍描述、编辑命令和完成按钮行为不变。

## 验证

在测试中同时覆盖打开和关闭路径，并断言输入法窗口在短时间采样内持续存在且 bounds 不变；测试输入只能使用合成值。对水杉输入法 Android 改动按仓库固定入口执行：

```sh
pnpm run verify-notes
git diff --check
ANDROID_SDK_ROOT=<SDK> bash platforms/android/check-host.sh
rbuild bash scripts/verify-local.sh --quick
bash platforms/android/tests/device/start-emulator.sh 28
MSIME_ANDROID_TEST_SERIAL=emulator-5566 bash platforms/android/tests/device/build-core-test.sh
MSIME_ANDROID_TEST_SERIAL=emulator-5566 bash platforms/android/tests/device/run-core-test.sh
```

界面相关改动还要在 API 35 专用模拟器运行相应的 device smoke。若未能构建当前分支的完整产品包或设备验收失败，报告确切命令、阶段和失败原因，不把 JVM、host 编译或 CI 说成设备验证。提交前遵守一 issue 一分支一 PR、中文 PR 正文和截图要求；不要把相同根因但不同 issue 合并到同一 PR。
