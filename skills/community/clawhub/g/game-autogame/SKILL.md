# 游戏自动化 - 向僵尸开炮

基于OCR的微信小程序游戏自动化脚本，自动刷关+智能选技能。

## 功能

- 自动检测"开始游戏"并点击
- 自动检测技能弹窗 → OCR识别技能 → 关键词智能选择
- 自动检测"返回" → 循环刷关
- 支持普通关/精英关

## 技能选择逻辑

1. **优先**：技能名称含"连"、"齐"
2. **其次**：技能名称含"子弹"（排除属性弹）
3. **默认**：选择中间技能

## 使用方法

### 1. 安装依赖
```bash
cd C:\Users\HQY\.openclaw\workspace\skills\game-autogame
pip install -r requirements.txt
```

### 2. 运行
```bash
python start.py
```

### 3. 停止
按 `Ctrl+Q` 停止程序

## 文件说明

| 文件 | 说明 |
|------|------|
| start.py | 主入口，循环执行 |
| GameControl.py | 游戏控制逻辑 |
| rapidocrhelper.py | OCR识别辅助 |
| win32helper.py | 窗口操作辅助 |
| requirements.txt | 依赖库 |

## 依赖

```
pywin32
rapidocr
onnxruntime
pyautogui
loguru
keyboard
```

## 注意事项

- 运行时会占用鼠标
- 需要提前打开微信小程序并选中要刷的关卡
- 游戏窗口标题必须是"向僵尸开炮"
