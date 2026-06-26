# 打开 Agent 工作看板

## 方法 1：直接打开 HTML 文件

```bash
# 在 PowerShell 中执行
start "C:\Users\Xiabi\.openclaw\workspace\agents\dashboard.html"
```

## 方法 2：使用批处理脚本

```bash
# 在 PowerShell 中执行
& "C:\Users\Xiabi\.openclaw\workspace\agents\start-dashboard.bat"
```

## 方法 3：通过 OpenClaw 命令

在 OpenClaw 中说：
- "打开 Agent 看板"
- "显示工作看板"
- "查看 Agent 状态"

## 看板功能

- ✅ 实时显示 4 个 Agent 的工作进度
- ✅ 任务完成状态标记
- ✅ 进度条可视化
- ✅ 自动刷新（每 30 秒）
- ✅ 响应式设计，支持手机查看

## Agent 列表

1. 🏃 **健康顾问** - 绿色
2. 👶 **育儿顾问** - 橙色
3. 🚀 **创业顾问** - 蓝色
4. 📈 **投资顾问** - 紫色

---

**提示**: 可以将 `start-dashboard.bat` 添加到桌面快捷方式，方便快速访问！
