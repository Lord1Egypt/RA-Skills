# Screen Control Node屏幕操控
# Node配对配置参考

## 配对步骤

### 方式1：命令行配对（推荐）
```bash
# 终端1 - 启动Gateway（如未运行）
openclaw gateway start

# 终端2 - 启动Node客户端
openclaw node run --host 127.0.0.1 --port 18789

# 终端3 - 查看并批准配对请求
openclaw nodes pending
openclaw nodes approve <requestId>
```

### 方式2：以管理员身份安装为服务
```powershell
# 以管理员身份运行PowerShell
openclaw node install --host 127.0.0.1 --port 18789
```

## 配对后的操作

配对成功后，Agent可以通过以下方式操控电脑：

1. **截图** — 获取屏幕实时画面
2. **pyautogui** — 移动鼠标、点击、键盘输入
3. **exec** — 运行本地脚本（文件操作、打开应用等）

## 屏幕控制脚本用法

```bash
# 截图
python scripts/screen_control.py screenshot

# 获取屏幕尺寸
python scripts/screen_control.py size

# 移动鼠标到坐标(500, 300)
python scripts/screen_control.py move 500 300

# 点击(500, 300)位置
python scripts/screen_control.py click 500 300 left

# 双击
python scripts/screen_control.py doubleclick 500 300

# 输入文字
python scripts/screen_control.py text "你好世界"

# 按键
python scripts/screen_control.py key enter
python scripts/screen_control.py key escape

# 组合键（使用pyautogui.hotkey）
python -c "import pyautogui; pyautogui.hotkey('ctrl', 'c')"

# 查找图片并点击
python scripts/screen_control.py locate button.png

# 查找文字位置
python scripts/screen_control.py findtext "确认"

# 查找并点击文字
python scripts/screen_control.py clicktext "提交"

# 滚动
python scripts/screen_control.py scroll -3

# 获取像素颜色
python scripts/screen_control.py color 100 200
```

## 注意事项

1. **Failsafe** — 将鼠标移到屏幕左上角可紧急停止
2. **权限** — 脚本需要管理员权限才能操作某些窗口
3. **Tesseract** — OCR功能需要安装Tesseract-OCR
   - 下载: https://github.com/UB-Mannheim/tesseract/wiki
   - 设置环境变量: TESSERACT_PATH
4. **分辨率** — 使用前先确认屏幕分辨率
