---
name: 选妃
description: 每日 AI Girl 选妃 - 从指定目录（目录里要有图片）随机选择 3 张 AI 女孩图片，让用户选择一个最喜欢的，自动保存为新头像并记录偏好。使用场景：(1) 每日早晨执行选妃任务，(2) 需要更新 AI 助手形象时，(3) 需要随机选择图片用于展示或测试
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "install": [],
      },
  }
---

# 选妃 - Daily AI Girl Portrait Selection

## 功能概述

每日随机从指定目录选择 3 张 AI Girl 图片，让你选择最喜欢的一个作为新头像。适合需要更新 AI 助手形象的场景。

# 效果展示

## 预览界面示例

![预览界面](assets/demo1.png)

**说明**: 上图展示了选妃任务生成的精美 HTML 预览页面，包含 3 张 AI Girl 图片的卡片式布局。

## 其他截图

![第二张截图](assets/demo2.png)

## 使用方法

### 基本用法

只需说：
- **"选妃"** - 直接执行选妃任务
- **"开始选妃"** - 同上

### 工作流程

1. 从 `/Volumes/info/sex/picture/AI girls/` 目录随机选取 3 张图片
2. 发送给你展示，并提供清晰的预览
3. 等待你选择（说"选 1"、"选 2"、"选 3"或文件名）
4. 自动保存你选择的图片作为新头像
5. 记录你的偏好到 `.learnings/AI-GIRL-PREFERENCES.md`
6. 更新头像文件 `~/.openclaw/workspace/avatars/mimi-today.png`

### 配置路径

- **图片源目录**: `/Volumes/info/sex/picture/AI girls/` (可修改)
- **头像保存位置**: `~/.openclaw/workspace/avatars/mimi-today.png`
- **偏好记录文件**: `.learnings/AI-GIRL-PREFERENCES.md`

## 脚本工具

脚本位于 `scripts/ai-girl-selection.sh`，支持：

- ✅ 随机选择 3 张图片
- ✅ 自动保存到预览目录
- ✅ 创建精美的 HTML 预览页面
- ✅ 记录选择偏好
- ✅ 自动更新头像

## 示例对话

```
用户：选妃
Mimi: 🌹 选妃时间 - Daily AI Girl Selection
      随机选取了 3 张 AI Girl 图片，请选一个你喜欢的：
      1. 20250725_002805.jpg
      2. 20250716_000913.jpg
      3. 00004-145824367.png

      告诉我你的选择吧！(直接说 "选 1/2/3") 😏
```

## 输出格式

- **成功**: 保存选择，更新头像，记录偏好
- **错误**: 目录不存在、没有图片、选择无效等

## 注意事项

- 确保源目录存在且有 JPG/PNG/WebP 图片
- 选择的图片将保存为 `mimi-today.png` 作为当日头像
- 偏好记录包含日期、时间、选择的文件名
- 支持旋转头像（可根据需要添加）