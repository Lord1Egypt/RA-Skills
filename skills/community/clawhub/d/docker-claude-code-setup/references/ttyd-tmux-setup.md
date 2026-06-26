# ttyd + tmux Web 终端配置

## 为什么用 ttyd + tmux

| 方案 | 组件数 | 会话持久化 | 中文支持 | 内存占用 |
|------|--------|-----------|---------|---------|
| VNC | 6+ | ❌ | 需配置 | 高 |
| ttyd | 1 | ❌ | ✅ 原生 | 极低 |
| ttyd + tmux | 2 | ✅ | ✅ 原生 | 极低 |

## 安装步骤

### 1. 安装 ttyd

```bash
# Debian/Ubuntu
apt-get update
apt-get install -y ttyd

# 或从源码编译
git clone https://github.com/tsl0922/ttyd.git
cd ttyd && mkdir build && cd build
cmake .. && make && make install
```

### 2. 安装 tmux

```bash
apt-get install -y tmux
```

### 3. 配置 tmux

创建 `~/.tmux.conf`:

```bash
# UTF-8 支持
set -g default-terminal "xterm-256color"
set -g utf8 on
set -g status-utf8 on

# 鼠标支持 (滚动、点击、调整大小)
set -g mouse on

# 更好的滚动体验
set -g terminal-overrides 'xterm*:smcup@:rmcup@'

# 状态栏美化 (可选)
set -g status-bg black
set -g status-fg green
```

### 4. 启动 ttyd + tmux

```bash
# 基本启动
ttyd -p 6080 -W tmux new -A -s main

# 带环境变量启动
ttyd -p 6080 -W bash -c "export LANG=zh_CN.UTF-8; export MY_VAR=value; tmux new -A -s main"
```

参数说明：
- `-p 6080`: 监听端口
- `-W`: 允许写入 (否则只能查看)
- `tmux new -A -s main`: 创建或附加到名为 main 的会话

## tmux 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+B D` | 断开会话 (保持后台运行) |
| `Ctrl+B C` | 新建窗口 |
| `Ctrl+B N` | 下一个窗口 |
| `Ctrl+B P` | 上一个窗口 |
| `Ctrl+B %` | 垂直分屏 |
| `Ctrl+B "` | 水平分屏 |
| `Ctrl+B 方向键` | 切换分屏 |

## 会话管理

```bash
# 列出所有会话
tmux ls

# 附加到会话
tmux attach -t main

# 杀死会话
tmux kill-session -t main

# 杀死所有会话
tmux kill-server
```

## 访问地址

- 本地: http://localhost:6080
- 外网: http://YOUR_IP:6080

**安全建议**: 在生产环境中，建议配合反向代理 (nginx) 使用 HTTPS。
