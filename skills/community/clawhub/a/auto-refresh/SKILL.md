---
name: auto-refresh
description: 自动刷新技能 - 定时刷新网页或执行任务
metadata:
  openclaw:
    emoji: "🔄"
---

# Auto Refresh 🔄

定时执行任务或刷新页面。

## 功能

- 定时刷新网页（通过浏览器快捷键 F5 或 Ctrl+R）
- 定时执行自定义命令
- 可配置间隔

## 使用方法

### 命令格式
```
auto-refresh --interval 30 --action refresh
```

### 参数
- `--interval`: 间隔时间（秒）
- `--action`: 操作类型 (refresh/click/key)
- `--x`: 鼠标 X 坐标（可选）
- `--y`: 鼠标 Y 坐标（可选）
- `--key`: 按键（可选）

## 示例

### 每30秒刷新一次页面
```
auto-refresh --interval 30 --action key --key F5
```

### 每分钟点击指定位置
```
auto-refresh --interval 60 --action click --x 100 --y 100
```

### 每20秒按一次空格键
```
auto-refresh --interval 20 --action key --key " "
```
