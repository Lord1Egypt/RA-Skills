# 故障排查指南

## 1. 端口相关错误

### 错误: "No available ports found"

**症状**:
```
Error: No available ports found
    at getPort (/path/to/remotion/renderer/dist/get-port.js:53:11)
```

**原因分析**:
Remotion 在检测端口时会同时测试多个网络接口:
- `::1` (IPv6 loopback)
- `127.0.0.1` (IPv4 loopback)
- `::` (IPv6 any)
- `0.0.0.0` (IPv4 any)

如果所有接口的端口检测都失败，就会报这个错误。

**解决方案**:

1. **检查 IPv6 loopback 是否存在**:
   ```bash
   ip -6 addr show lo | grep ::1
   ```

2. **如果不存在，手动添加**:
   ```bash
   ip -6 addr add ::1/128 dev lo
   ```

3. **清理残留的 Chrome 进程**:
   ```bash
   pkill -f chrome-headless
   ```

4. **强制指定端口**:
   ```tsx
   const composition = await selectComposition({
     serveUrl: bundled,
     id: 'MyVideo',
     port: 3400,  // 强制端口
     preferIpv4: true,
   });
   ```

### 错误: "Port XXX is already in use"

**解决方案**:
```bash
# 查看端口占用
ss -tuln | grep LISTEN

# 查找并杀掉占用进程
lsof -i :3000
kill -9 <PID>
```

## 2. 浏览器相关错误

### 错误: "Failed to launch the browser process! EACCES"

**原因**: Chrome 可执行文件没有执行权限

**解决方案**:
```bash
# 查找 Chrome 路径
find node_modules -name "chrome-headless-shell" -type f

# 添加执行权限
chmod +x /path/to/chrome-headless-shell
```

### 错误: "Failed to launch the browser process! spawn ENOENT"

**原因**: 找不到 Chrome 可执行文件

**解决方案**:
1. 检查 Remotion 是否已下载 Chrome:
   ```bash
   ls node_modules/.remotion/chrome-headless-shell/
   ```

2. 手动指定浏览器路径:
   ```tsx
   const browserExecutable = '/path/to/chrome-headless-shell';
   
   await renderMedia({
     composition,
     serveUrl: bundled,
     codec: 'h264',
     outputLocation: './out/video.mp4',
     browserExecutable,
   });
   ```

### 错误: "Chromium failed to start"

**可能原因**:
- 缺少系统依赖库
- 内存不足

**解决方案**:
```bash
# 检查依赖 (Ubuntu/Debian)
ldd /path/to/chrome-headless-shell | grep "not found"

# 安装缺失依赖
apt-get install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2
```

## 3. 渲染相关错误

### 错误: "Could not play video with Chrome"

**原因**: 视频编解码器不支持

**解决方案**:
1. 使用支持的编码器:
   ```tsx
   await renderMedia({
     composition,
     serveUrl: bundled,
     codec: 'h264',  // 或 'vp8', 'vp9'
     outputLocation: './out/video.mp4',
   });
   ```

2. 检查 FFmpeg:
   ```bash
   ffmpeg -codecs | grep h264
   ```

### 错误: "FATAL:zone allocated memory"

**原因**: 内存不足

**解决方案**:
1. 减少并发:
   ```tsx
   await renderMedia({
     composition,
     serveUrl: bundled,
     codec: 'h264',
     outputLocation: './out/video.mp4',
     concurrency: 1,  // 减少并发数
   });
   ```

2. 降低分辨率:
   ```tsx
   <Composition
     id="MyVideo"
     component={MyVideo}
     width={1280}   // 降低分辨率
     height={720}
     fps={30}
     durationInFrames={150}
   />
   ```

## 4. TypeScript 相关错误

### 错误: "Cannot find module 'remotion'"

**解决方案**:
```bash
npm install remotion @remotion/cli @remotion/player react react-dom
```

### 错误: "Module resolution failed"

**检查 tsconfig.json**:
```json
{
  "compilerOptions": {
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx"
  }
}
```

## 5. 常见运行时错误

### 错误: "Composition not found"

**检查项**:
1. Composition ID 是否正确
2. `registerRoot` 是否已调用
3. 入口文件路径是否正确

### 错误: "Props mismatch"

**解决方案**:
确保 `defaultProps` 和组件 props 类型匹配:
```tsx
interface MyVideoProps {
  title: string;
  count: number;
}

<Composition
  id="MyVideo"
  component={MyVideo}
  defaultProps={{
    title: 'Hello',
    count: 42,
  }}
/>
```

## 快速诊断命令

```bash
# 1. 检查网络配置
ip addr show lo
ip -6 addr show lo

# 2. 检查端口状态
ss -tuln | grep LISTEN

# 3. 检查残留进程
ps aux | grep -E "(chrome|remotion|node)" | grep -v grep

# 4. 检查磁盘空间
df -h

# 5. 检查内存
free -h

# 6. 测试 Chrome
/path/to/chrome-headless-shell --version
```
