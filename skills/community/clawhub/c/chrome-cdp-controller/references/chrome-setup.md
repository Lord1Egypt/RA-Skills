# Chrome 远程调试设置

## 启动带远程调试的 Chrome

### macOS

```bash
# 关闭所有 Chrome 实例
killall "Google Chrome"

# 启动带远程调试的 Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &
```

或者创建别名:

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
alias chrome-debug='/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222'
```

### Windows

```cmd
# 关闭所有 Chrome 实例
taskkill /F /IM chrome.exe

# 启动带远程调试的 Chrome
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

### Linux

```bash
# 关闭所有 Chrome 实例
killall chrome

# 启动带远程调试的 Chrome
google-chrome --remote-debugging-port=9222 &
```

## 验证连接

打开浏览器访问: http://localhost:9222/json

如果看到 JSON 响应,说明远程调试已启动成功。

## 常见问题

### 端口被占用

如果 9222 端口被占用,可以使用其他端口:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9223 &
```

然后在使用 CDP 控制器时指定端口:

```bash
python scripts/cdp_controller.py --cdp-url http://localhost:9223
```

### 已有 Chrome 进程

必须先关闭所有 Chrome 进程,才能以调试模式启动。

### 权限问题

确保 Chrome 可执行文件有执行权限:

```bash
chmod +x /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome
```

## 自动化脚本

创建启动脚本 `start-chrome-debug.sh`:

```bash
#!/bin/bash
killall "Google Chrome" 2>/dev/null
sleep 1
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &
echo "Chrome 远程调试已启动 (端口 9222)"
```

使用:

```bash
chmod +x start-chrome-debug.sh
./start-chrome-debug.sh
```
