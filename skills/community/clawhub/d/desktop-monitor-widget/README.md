# Desktop Monitor Widget - 桌面监控悬浮球

一个优雅的桌面监控悬浮球，实时显示系统资源状态。

## 功能特性

- 🎯 **悬浮球设计** - 透明悬浮窗，不干扰其他操作
- 📊 **实时监控** - CPU、内存、磁盘、温度
- 🎨 **贴边自动缩小** - 靠近屏幕边缘自动折叠 (Tkinter 版)
- 🖱️ **可拖动位置** - 随意放置在屏幕任意位置
- 🔄 **自动更新** - 每 2 秒刷新一次数据
- 👆 **双击切换** - 展开/折叠视图 (Tkinter 版)

## 安装依赖

```bash
# 安装 Python 依赖
pip3 install psutil

# 可选：Tkinter 版本需要 (如需使用桌面窗口模式)
sudo apt install python3-tk
```

## 使用方法

### 方式 1：Web 浏览器模式（推荐）

```bash
# 启动监控悬浮球
./scripts/start.sh

# 或直接运行
python3 scripts/widget-web.py
```

启动后会自动打开浏览器访问 `http://127.0.0.1:8765`

### 方式 2：Tkinter 窗口模式

```bash
python3 scripts/widget.py
```

## 操作说明

| 操作 | 效果 |
|------|------|
| 拖动窗口 | 移动位置 |
| 双击 | 展开/折叠 (Tkinter 版) |
| 靠近边缘 | 自动缩小 (Tkinter 版) |
| 鼠标悬停 | 显示完整内容 |

## 预览效果

```
┌─────────────────────────┐
│ 🖥️ 系统监控             │
├─────────────────────────┤
│ CPU       [████]  15%   │
│ 内存      [███]   42%   │
│ 磁盘      [█████] 65%   │
│ 温度      45°C          │
│ 运行时间  2 天 3 小时      │
│ 进程数    245           │
├─────────────────────────┤
│     ● 实时监控中        │
└─────────────────────────┘
```

## 文件结构

```
desktop-monitor-widget/
├── SKILL.md              # Skill 描述
├── README.md             # 使用说明
└── scripts/
    ├── widget-web.py     # Web 版本 (推荐)
    ├── widget.py         # Tkinter 版本
    └── start.sh          # 启动脚本
```

## 开机自启

### Linux (Systemd)

```bash
# 创建服务文件
sudo nano /etc/systemd/system/monitor-widget.service
```

内容：
```ini
[Unit]
Description=Desktop Monitor Widget
After=graphical.target

[Service]
Type=simple
User=your_username
ExecStart=/usr/bin/python3 /path/to/widget-web.py
Restart=always

[Install]
WantedBy=default.target
```

启用服务：
```bash
systemctl enable monitor-widget
systemctl start monitor-widget
```

## 故障排除

### 问题：无法启动，提示缺少 psutil
**解决：** `pip3 install psutil`

### 问题：端口 8765 已被占用
**解决：** 修改 `widget-web.py` 中的端口号

### 问题：浏览器无法打开
**解决：** 手动访问 http://127.0.0.1:8765

## 许可证

MIT License
