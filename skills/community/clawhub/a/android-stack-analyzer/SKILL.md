# Android Stack Analyzer - 安卓页面栈分析工具

## 简介
这个技能让你通过ADB命令快速查看安卓设备的页面栈信息，包括当前页面、Activity历史、Fragment等。适用于Android开发者、测试人员和逆向工程师。

## 功能特点
- 查看当前最上层页面
- 分析完整Activity页面栈
- 查看Fragment页面栈
- 监控页面切换
- 支持不同Android版本的命令兼容性

## 使用方法

### 1. 查看当前最上层页面

#### Windows:
```cmd
adb shell "dumpsys window | findstr mCurrentFocus"
```

#### Linux/macOS:
```bash
adb shell "dumpsys window | grep mCurrentFocus"
```
输出示例：
```
mCurrentFocus=Window{... u0 com.example.app/com.example.app.MainActivity}
```

### 2. 查看完整Activity页面栈

#### Windows:
```cmd
adb shell "dumpsys activity activities | findstr /R "Hist\|ResumedActivity\|mFocusedActivity"
```

#### Linux/macOS:
```bash
adb shell "dumpsys activity activities | grep -E 'Hist|ResumedActivity|mFocusedActivity'"
```
输出示例：
```
* Hist #3: ActivityRecord{... u0 com.example.app/.activity.MainActivity t533}
* Hist #2: ActivityRecord{... u0 com.example.app/.activity.SettingsActivity t533}
ResumedActivity: ActivityRecord{... u0 com.example.app/.activity.MainActivity t533}
```

### 3. 查看页面栈中的Fragment

#### Windows:
```cmd
adb shell "dumpsys activity <包名>"
```
示例：查看com.example.app的Fragment信息
```cmd
adb shell "dumpsys activity com.example.app"
```

#### Linux/macOS:
```bash
adb shell "dumpsys activity <包名>"
```
示例：查看com.example.app的Fragment信息
```bash
adb shell "dumpsys activity com.example.app"
```

### 4. 查看Activity任务栈树形结构

#### Windows:
```cmd
adb shell "dumpsys activity activities | findstr /R "TaskRecord\|ActivityRecord"
```

#### Linux/macOS:
```bash
adb shell "dumpsys activity activities | grep -E 'TaskRecord|ActivityRecord'"
```

### 5. 查看最近任务列表

#### Windows:
```cmd
adb shell "dumpsys activity recents"
```

#### Linux/macOS:
```bash
adb shell "dumpsys activity recents"
```

### 6. 实时监控当前页面切换

#### Windows:
```cmd
adb shell "while /l %%i in () do @echo [%time%] & adb shell "dumpsys window | findstr mCurrentFocus" & timeout /t 1 > nul"
```

#### Linux/macOS:
```bash
adb shell "while true; do echo "[$(date '+%H:%M:%S')] $(adb shell 'dumpsys window | grep mCurrentFocus')"; sleep 1; done"
```

### 7. 查看Activity生命周期状态

#### Windows:
```cmd
adb shell "dumpsys activity activities | findstr state="
```

#### Linux/macOS:
```bash
adb shell "dumpsys activity activities | grep 'state='"
```

## 高级用法

### 查看特定包名的详细Activity信息

#### Windows:
```cmd
adb shell "dumpsys activity a <包名>"
```

#### Linux/macOS:
```bash
adb shell "dumpsys activity a <包名>"
```

### 查看所有运行中的进程及对应的Activity

#### Windows:
```cmd
adb shell "dumpsys activity processes"
```

#### Linux/macOS:
```bash
adb shell "dumpsys activity processes"
```

### 查看Back Stack详细信息

#### Windows:
```cmd
adb shell "dumpsys activity activities | findstr /R "mResumedActivity\|mFocusedActivity"
```

#### Linux/macOS:
```bash
adb shell "dumpsys activity activities | grep -E 'mResumedActivity|mFocusedActivity'"
```

## 输出解析

### mCurrentFocus字段
- `u0` - 用户应用（User app）
- `s0` - 系统应用（System app）
- `com.example.app` - 包名
- `com.example.app.MainActivity` - Activity类名

### Activity历史栈
- `* Hist #3` - 历史记录中的第3个Activity（数字越大越新）
- `u0` - 用户应用
- `t533` - 任务ID
- `inHistory=true` - 在历史栈中
- `mStartingWindowState=STARTING_WINDOW_NOT_SHOWN` - 启动窗口状态

### Activity状态
- `INITIALIZING` - 初始化中
- `RESUMED` - 前台可见
- `PAUSED` - 暂停
- `STOPPED` - 停止
- `DESTROYED` - 已销毁

## 兼容性说明

### Windows平台
- 使用 `adb` 而不是 `adb.exe`（通常PATH中已配置）
- 使用 `findstr` 而不是 `grep`
- 使用 `findstr /R` 进行正则匹配
- 命令示例：
```cmd
adb shell "dumpsys window | findstr mCurrentFocus"
```

### Linux/macOS平台
- 使用 `adb` 命令
- 使用 `grep` 命令
- 支持正则表达式匹配
- 命令示例：
```bash
adb shell "dumpsys window | grep mCurrentFocus"
```

### Android版本差异
- Android 13+ 部分 `dumpsys` 输出格式有变化
- 如果命令不生效，可以先查看原始输出确认字段名
- 某些设备可能需要root权限才能获取完整信息

## 常见问题

### 1. findstr/grep命令不可用
某些设备上可能没有这些命令，可以：
- 使用 `adb shell dumpsys window` 然后手动查找
- 使用 `adb shell dumpsys activity activities` 然后手动查找

### 2. 输出太多信息
可以使用包名过滤：
```bash
adb shell "dumpsys activity activities | grep com.example.app"
```

### 3. 系统应用信息被隐藏
某些设备可能需要开启开发者选项中的"显示系统级应用"

### 4. 页面栈不准确
- 可能是WebView或Dialog/PopupWindow遮挡
- 可以使用 `dumpsys activity activities | grep ResumedActivity` 确认

## 实用脚本

### 自动化脚本示例
```bash
#!/bin/bash
# 获取当前页面
echo "=== 当前页面 ==="
adb shell "dumpsys window | grep mCurrentFocus"

# 获取页面栈
echo -e "\n=== 页面栈 ==="
adb shell "dumpsys activity activities | grep -E 'Hist|ResumedActivity'"

# 获取最近任务
echo -e "\n=== 最近任务 ==="
adb shell "dumpsys activity recents"
```

### 批量检查多个应用
```bash
#!/bin/bash
apps=("com.example.app1" "com.example.app2" "com.example.app3")

for app in "${apps[@]}"; do
    echo "=== 检查 $app ==="
    adb shell "dumpsys activity activities | grep $app"
    echo ""
done
```

## 注意事项
1. 确保设备已开启USB调试模式
2. 某些设备可能需要授权ADB连接
3. 系统应用信息可能需要root权限
4. 不同Android版本输出格式可能不同
5. 部分设备可能禁用了某些dumpsys命令

## 更新日志
- v1.0.0 - 初始版本，支持基本页面栈分析功能
- v1.1.0 - 添加Fragment查看功能
- v1.2.0 - 添加实时监控功能
- v1.3.0 - 添加跨平台兼容性支持