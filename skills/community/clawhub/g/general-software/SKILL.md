---
name: general-software
description: 通用软件自动化技能，涵盖窗口管理、GUI自动化、批量文件处理、软件安装配置、系统设置、日志收集分析、截图取证等通用场景。触发场景：自动化点击、窗口操作、批量重命名、文件格式转换、软件批量安装、系统配置、日志分析、屏幕截图、GUI测试。
---

# General Software - 通用软件自动化

## 核心能力

### 窗口 & GUI 自动化
- 窗口查找、激活、最小化/最大化/关闭
- 鼠标点击、拖拽、滚轮操作
- 键盘输入、快捷键执行
- 表单自动填充
- 支持：Windows (PyAutoGUI/UIAutomation)、跨平台 (PyGuyy)

### 批量文件处理
- 批量重命名（支持正则、序号、日期插入）
- 格式转换（图片/音频/视频/文档）
- 文件批量压缩/解压
- 目录结构复制/同步
- 文件内容批量搜索替换

### 软件安装 & 配置
- 静默安装 / 卸载（MSI / EXE）
- 配置文件修改（INI / JSON / YAML / 注册表）
- 环境变量管理
- Windows 服务管理（启动/停止/重启）

### 日志收集 & 分析
- 多目录日志批量收集
- 按关键字 / 时间范围过滤
- 异常模式匹配（ERROR / Exception / Fatal）
- 日志汇总报告生成

### 系统 & 截图
- 系统信息采集（硬件/软件/网络）
- 屏幕截图 / 区域截图
- 多屏幕支持
- 截图标注和高亮

### 关键脚本
- `scripts/gui_auto.py` - PyAutoGUI Windows GUI 自动化
- `scripts/uiauto.py` - Windows UIAutomation 高级操作
- `scripts/batch_rename.py` - 批量文件重命名
- `scripts/file_convert.py` - 格式批量转换
- `scripts/soft_install.py` - 软件静默安装
- `scripts/log_collector.py` - 日志收集分析
- `scripts/screenshot.py` - 屏幕截图工具

### 参考资源
- `references/pyautogui-cheatsheet.md` - PyAutoGUI 速查表
- `references/windows-automation.md` - Windows 自动化进阶

## 工作流程

1. **描述任务**：用户描述需要自动化的软件操作
2. **判断类型**：GUI 自动化 / 文件处理 / 系统配置 / 日志分析
3. **执行脚本**：调用对应脚本，必要时先录制演示
4. **结果确认**：截图或输出文件确认效果

## 注意事项
- GUI 自动化前先了解目标软件的界面结构
- 批量文件操作先在测试目录验证
- 静默安装需要管理员权限
- 日志分析优先使用正则匹配关键模式
- 截图工具支持全屏/区域/窗口三种模式
