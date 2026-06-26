---
name: screen-control
description: "屏幕控制技能 - 通过OpenClaw Node + pyautogui实现电脑屏幕识别和鼠标键盘操控。功能：(1) 截图获取屏幕画面，(2) OCR文字识别定位，(3) 图片匹配定位，(4) 鼠标移动/点击/拖拽，(5) 键盘输入/快捷键，(6) 基于视觉信息的自动化操作。Use when: (1) 需要远程操电脑屏幕，(2) 需要自动操作桌面应用（非浏览器），(3) 需要批量处理电脑上的文件或软件，(4) 需要通过视觉识别自动化操作。Triggers: '操作电脑', '屏幕控制', '自动点击', '截图识别', '桌面自动化', '远程操控', '操控鼠标', '屏幕识别'。"
---

# Screen Control — 屏幕操控技能

## 概述

通过 OpenClaw Node + pyautogui + OCR，实现对电脑屏幕的识别和鼠标键盘操控。

## 架构

```
用户指令 → Agent → screen_control.py (pyautogui + OCR) → 屏幕操作
                    ↕
              OpenClaw Node (截图/远程执行)
```

## 前置条件

1. **OpenClaw Node** — 需配对成功（见 references/setup-guide.md）
2. **Python依赖** — pyautogui, pillow, mss, pytesseract（如需OCR）
3. **Tesseract-OCR** — 如需文字识别功能（安装指引见 setup-guide.md）

## 工作流程

当用户要求操控电脑时：

### Step 1：确认屏幕状态
```bash
python {baseDir}/scripts/screen_control.py screenshot
python {baseDir}/scripts/screen_control.py size
```
获取当前屏幕画面和分辨率，AI识别画面内容。

### Step 2：分析画面 + 定位目标
AI分析截图，确定需要操作的坐标或内容。

- 如果目标基于**图片**：`locate <image_path>`
- 如果目标基于**文字**：`clicktext "确定"`
- 如果目标基于**坐标**：`click 500 300`

### Step 3：执行操作
```python
# 打开浏览器
press_key("win") + type_text("chrome") + press_key("enter")

# 打开网页
type_text("douyin.com\n")  # \n = enter

# 拖动
mouse_drag(100, 100, 500, 500)

# 复制粘贴
hotkey("ctrl", "c")
hotkey("ctrl", "v")
```

### Step 4：验证结果
再次截图确认操作结果。

## 脚本命令速查

| 命令 | 参数 | 说明 |
|------|------|------|
| screenshot | 无 | 截图保存到文件 |
| size | 无 | 获取屏幕分辨率 |
| move | x y | 移动鼠标 |
| click | x y [button] | 点击（按钮: left/right/middle） |
| doubleclick | x y | 双击 |
| text | "文字" | 键盘输入文字 |
| key | key_name | 按键（enter/esc/tab等） |
| locate | image_path | 查找图片位置 |
| findtext | "文字" | 查找文字位置 |
| clicktext | "文字" | 查找并点击文字 |
| scroll | clicks | 滚动（正=上，负=下） |
| color | x y | 获取像素颜色 |

## 常用场景

### 1. 自动登录平台后台
```
截图 → 定位登录框坐标 → 输入账号密码 → 点击登录按钮
```

### 2. 批量操作抖音/小红书后台
```
截图 → 找到发布按钮 → 点开 → 上传视频/图片 → 填写标题 → 发布
```

### 3. 打开特定软件/文件
```
按Win键 → 搜索程序名 → 回车打开
```

### 4. 文件整理/批量重命名
```
打开文件夹 → 选中文件 → 执行操作
```

## 安全注意

1. 操作前先截图给用户确认
2. 任何破坏性操作（删除文件、修改配置）需用户确认
3. 使用 pyautogui.FAILSAFE=True（左上角急停）
4. 不要在用户未授权的情况下操作浏览器密码/支付页面
