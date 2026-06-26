---
name: desktop-automation
description: |
  桌面智能体自动化技能。执行需要操作电脑的多步骤任务时激活。

  能力：屏幕截图、视觉分析、浏览器自动化、桌面键鼠控制、文件shell操作、跨域握手协议。

  触发场景：
  - "帮我自动完成XXX（需要操作电脑）"
  - "打开XX应用/网页，然后..."
  - "把桌面上的文件自动整理到..."
  - "自动登录XX网站并填入..."
  - "批量重命名/移动/处理文件"
  - 任何涉及点击、拖拽、填写表单的任务
---

# 桌面智能体自动化

macOS 专用桌面自动化，执行看→想→做→验证循环完成任务。

## 双域架构

```
【浏览器域】→ browser 工具（网页操作）
【桌面域】  → screencapture + osascript + cliclick（系统操作）
```

## 核心循环（每步必须走完）

```
看 → 想 → 做 → 验证
```

## 浏览器域工具

使用 `browser` 工具：
- `browser navigate url="..."` — 导航
- `browser snapshot` — 获取DOM快照
- `browser screenshot` — 截图
- `browser click ref="A7"` — 按ref点击元素
- `browser type ref="..." text="..."` — 输入文本
- `browser evaluate script="..."` — 执行JS

## 桌面域工具

### 截图
```bash
screencapture -x /tmp/screen.png
```
然后用 `image` 工具分析截图内容。

### 点击（坐标）
```bash
cliclick p  # 先获取当前鼠标位置
cliclick c:500,300  # 点击坐标(500,300)
cliclick dc:500,300  # 双击
```

### 点击（图像匹配）
```bash
cliclick fi:/tmp/button.png  # 找图点击（全屏搜索）
```

### 键盘输入
```bash
# 文本粘贴法（推荐）
osascript -e 'set the clipboard to "要输入的文本"'
osascript -e 'tell application "System Events" to keystroke "v" using command down'

# 直接按键
osascript -e 'tell application "System Events" to keystroke "return"'
osascript -e 'tell application "System Events" to keystroke "g" using {command down, shift down}'
```

### 文件对话框（万能路径法）
```bash
# macOS打开/保存对话框输入路径
cliclick kd:cmd,shift:g  # Cmd+Shift+G
osascript -e 'set the clipboard to "/Users/macmini/Desktop/目标文件.txt"'
osascript -e 'tell application "System Events" to keystroke "v" using command down'
osascript -e 'tell application "System Events" to keystroke "return"'
```

### 文件操作（shell，禁用Finder）
```bash
mv /源路径 /目标路径
cp /源路径 /目标路径
mkdir -p /目录路径
curl -o /保存路径 "https://url"
```

## 跨域握手协议

浏览器域→桌面域切换时必须：
1. **离开前快照**：browser screenshot → 记录状态
2. **切换执行**：在桌面域完成操作
3. **回归前验证**：切回浏览器，browser screenshot → 确认状态变化

**五个触发信号**：点击无响应超过2秒 | 出现macOS对话框 | 涉及文件保存/打开/下载 | 对话框消失 | 焦点切换到桌面应用

## 七条铁律

1. **每步先看后做**：每个动作前必须先截图/快照
2. **坐标只在当前截图有效**：页面变化后必须重新获取坐标
3. **系统弹窗用键盘**：Cmd+Shift+G 输路径是万能招式
4. **文件操作用shell**：mv/cp/mkdir，不开Finder
5. **跨域切换必须握手**：离开前→执行→回归前验证
6. **连续失败2次停下**：问用户，不盲目继续
7. **里程碑输出状态**：[已完成] [当前] [下一步]

## 任务栈维护

执行复杂任务时维护任务栈：
```
主任务：用户任务描述
  [浏览器域] 步骤1      ✓ 完成
  [浏览器域] 步骤2      ● 进行中
    ├─ [浏览器域] 子步骤2a  ✓ 完成
    └─ [桌面域] 处理对话框    ● 当前位置
  [浏览器域] 步骤3        ○ 待执行
```

## 权限要求

桌面域需要 macOS Accessibility 权限：
- 系统设置 → 隐私与安全性 → 辅助功能 → 允许「终端」或「OpenClaw」

## 常用任务模板

### 飞书发消息
```
1. browser navigate → feishu网页版
2. browser snapshot → 找到输入框
3. browser click → 点击输入框
4. browser type → 输入内容
5. browser click → 发送按钮
```

### 批量文件整理
```
1. exec → mkdir -p ~/目标目录
2. exec → for f in ~/源目录/*.csv; do mv "$f" ~/目标目录/; done
3. exec → ls ~/目标目录/ | wc -l → 验证数量
```

### 下载并保存文件
```
1. browser navigate → 目标页面
2. browser evaluate → 获取下载链接
3. exec → curl -o ~/保存路径 "URL"
4. exec → ls ~/保存路径 → 验证
```
