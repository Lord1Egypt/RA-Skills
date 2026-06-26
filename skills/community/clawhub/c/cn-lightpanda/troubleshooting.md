# 故障排查

## 安装问题

---

### 问题 1：下载的二进制无法执行

**难度：** 低

**症状：** `Permission denied` 或 `cannot execute binary file`

**解决方案：**
```bash
# 检查并添加执行权限
ls -la lightpanda
chmod a+x ./lightpanda
./lightpanda version
```

如果在 Alpine Linux 或 musl 系统上：
```bash
# Lightpanda 依赖 glibc，不支持 musl
# 改用 glibc 系统（Debian/Ubuntu）或 Docker

docker run --rm lightpanda/browser:nightly lightpanda version
```

---

### 问题 2：macOS 安全警告（`Apple 无法验证`）

**难度：** 低

**症状：** `"lightpanda" cannot be opened because the developer cannot be verified`

**解决方案：**
```bash
# 方式一：在终端中右键打开一次（选择"打开"）

# 方式二：移除隔离属性
xattr -d com.apple.quarantine ./lightpanda
./lightpanda version
```

---

### 问题 3：Linux 缺少系统库

**难度：** 中

**症状：** `error while loading shared libraries: libXXX.so.X`

**排查步骤：**
```bash
ldd ./lightpanda | grep "not found"
```

**解决方案：**
```bash
# Ubuntu/Debian 安装常见依赖
sudo apt-get update
sudo apt-get install -y libcurl4 libssl3

# 如果仍有缺失，使用 Docker 镜像
docker run -d --name lightpanda \
  -p 127.0.0.1:9222:9222 \
  lightpanda/browser:nightly
```

---

## 使用问题

---

### 问题 4：CDP 服务器连接失败

**难度：** 中

**症状：** `WebSocket connection failed` 或 `ECONNREFUSED 127.0.0.1:9222`

**排查步骤：**
```bash
# 确认服务器正在运行
ps aux | grep lightpanda

# 检查端口监听
netstat -tlnp | grep 9222
# 或
lsof -i :9222

# 测试 HTTP 端点
curl http://127.0.0.1:9222/json/version
```

**解决方案：**
```bash
# 确保先启动 CDP 服务器
./lightpanda serve --host 127.0.0.1 --port 9222 &
sleep 1

# 等待服务就绪后再连接
until curl -s http://127.0.0.1:9222/json/version; do sleep 1; done
echo "Lightpanda ready"
```

---

### 问题 5：Puppeteer 脚本连接超时

**难度：** 中

**症状：** `TimeoutError: Timeout exceeded while waiting for connect response`

**常见原因：**
- Lightpanda 还未完全启动（概率 50%）
- 使用了 `browserWSEndpoint` 而非等待服务就绪（概率 30%）
- Lightpanda 崩溃（Beta 阶段概率 20%）

**解决方案：**
```javascript
import puppeteer from 'puppeteer-core';

// 增加连接超时
const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222",
  timeout: 30000,  // 30 秒
});

// 如果还是失败，检查 Lightpanda 进程状态
// ps aux | grep lightpanda
```

---

### 问题 6：页面 JS 渲染结果不完整

**难度：** 中

**症状：** 动态加载的内容没有出现在提取结果中

**常见原因：**
- 没有等待页面 JS 执行完成（概率 60%）
- 依赖的 Web API 在 Lightpanda Beta 中尚未实现（概率 40%）

**解决方案：**
```bash
# CLI：使用等待选项
./lightpanda fetch --dump html \
  --wait-until networkidle \
  --wait-selector "#dynamic-content" \
  https://spa-app.com

# 或增加等待时间
./lightpanda fetch --dump html \
  --wait-ms 3000 \
  https://slow-spa.com
```

```javascript
// Puppeteer：等待具体元素
await page.goto(url, { waitUntil: 'networkidle0' });
await page.waitForSelector('.dynamic-content', { timeout: 5000 });
const content = await page.textContent('.dynamic-content');
```

如果仍不工作，该功能可能依赖 Lightpanda Beta 尚未实现的 Web API，检查 GitHub Issues：https://github.com/lightpanda-io/browser/issues

---

## 网络/环境问题

---

### 问题 7：Docker 容器内无法访问宿主机网络

**难度：** 中

**症状：** Docker 容器中的爬虫无法访问 `localhost` 上的目标服务

**解决方案：**
```bash
# 使用宿主机 IP 替代 localhost
docker run -d --name lightpanda \
  -p 127.0.0.1:9222:9222 \
  --add-host host.docker.internal:host-gateway \
  lightpanda/browser:nightly

# 爬取宿主机服务时使用 host.docker.internal
./lightpanda fetch --dump html http://host.docker.internal:3000
```

---

### 问题 8：并发过高导致崩溃（Beta 限制）

**难度：** 中

**症状：** 高并发时 Lightpanda 崩溃或产生乱码输出

**说明：** Lightpanda 当前处于 Beta 阶段，极高并发下可能不稳定。

**解决方案：**
```javascript
// 限制并发数量
const CONCURRENCY = 5;  // 从 5 开始测试，根据稳定性调整

async function crawlWithLimit(urls) {
  const results = [];
  for (let i = 0; i < urls.length; i += CONCURRENCY) {
    const batch = urls.slice(i, i + CONCURRENCY);
    const batchResults = await Promise.all(batch.map(crawl));
    results.push(...batchResults);
  }
  return results;
}
```

如果发现崩溃，请在 GitHub Issues 报告，附上复现步骤。

---

## 通用诊断

```bash
# 检查版本和基本功能
./lightpanda version
./lightpanda fetch --dump markdown https://example.com | head -10

# 检查 CDP 服务器健康状态
curl -s http://127.0.0.1:9222/json/version | python3 -m json.tool

# 查看详细日志
./lightpanda serve \
  --log-format pretty \
  --log-level debug \
  --host 127.0.0.1 \
  --port 9222
```

**注意：** Lightpanda 处于 Beta 阶段，部分网站可能遇到问题。如有 Bug，请在 GitHub 提交 Issue 并附带能复现的具体 URL。

**GitHub Issues：** https://github.com/lightpanda-io/browser/issues

**Discord：** https://discord.gg/K63XeymfB5

**文档：** https://lightpanda.io/docs
