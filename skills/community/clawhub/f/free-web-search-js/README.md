# free-web-search-js

## 项目简介

free-web-search-js 是一个基于 Playwright和JS写 的免费网络搜索skill 可用于CC或者openclaw（clawhub install free-web-search-js），无需 API Key，支持国内和海外搜索，自动抓取搜索结果内容。

**Pure search — no rewriting, no filtering.** 噪音交给 AI 处理。使用真实浏览器（Playwright）处理 Bing CN 反爬，国际查询则使用 HTTP 加速。

- **免费**：零成本使用，无需 API Key
- **稳定**：根据网络环境自动切换搜索策略，提高可达性
- **快速**：首次搜索 3\~6 秒，后续复用浏览器更快
- **自动抓取**：搜索后自动抓取 top N 条结果内容
- **跨区域**：国内使用 Bing，海外使用 DDG

## 支持的搜索引擎

| 引擎       | 协议               | 区域 | 说明                                          |
| -------- | ---------------- | -- | ------------------------------------------- |
| Bing CN  | Playwright 搜索框提交 | 国内 | 先访问首页拿 cookie，再搜索框输入提交                      |
| DDG | Playwright 搜索框提交 | 海外 | 完整浏览器自动化                         |

## 安装

### 前置依赖

| 依赖            | 说明                     | 大小/耗时              |
| ------------- | ---------------------- | ------------------ |
| Node.js >= 18 | 运行时                    | —                  |
| cheerio       | HTML 解析                | 小，秒装               |
| commander     | CLI 参数解析               | 小，秒装               |
| iconv-lite    | GBK 编码转换               | 小，秒装               |
| playwright    | 浏览器自动化（Bing 搜索 + 抓取兜底） | \~50MB             |
| Chromium      | Playwright 专用浏览器       | **\~150MB，需几分钟下载** |

### 安装步骤

#### 一键安装

```bash
# Linux/macOS
bash scripts/setup.sh

# Windows
powershell -File scripts/setup.ps1
```

#### 手动安装

```bash
# 进入项目目录
cd free-web-search-js

# 安装依赖
npm install

# 安装 Playwright 浏览器
npx playwright install chromium    # ~150MB，需几分钟
```

### 国内镜像加速

```bash
# npm 镜像
npm install --registry=https://registry.npmmirror.com

# Playwright/Chromium 镜像
PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright npx playwright install chromium
```

### 验证环境

```bash
node scripts/check-env.js
```

## 用法

### 搜索（搜 + 自动抓内容）

```bash
# 基本搜索
node scripts/search.js "白银价格"

# 控制结果数量
node scripts/search.js "how to deploy docker" --max=5

# 指定区域
node scripts/search.js "xxx" --region=cn

# 控制抓取数量
node scripts/search.js "xxx" --fetch=5          # 抓前5条

# 只搜索不抓取
node scripts/search.js "xxx" --no-fetch

# 控制单页最大字符数
node scripts/search.js "xxx" --max-len=8000
```

### 单独抓取（给定 URL）

```bash
node scripts/fetch.js "https://example.com/page1" "https://example.com/page2"
```

## 性能优化：浏览器守护进程

搜索和抓取可复用浏览器守护进程，**提速约 70%**：

```bash
node scripts/browser-daemon.js &       # 启动
node scripts/browser-daemon.js --status # 状态
node scripts/browser-daemon.js --stop   # 停止
```

守护进程空闲 10 分钟自动退出。

## 架构

### 国内搜索流程

```
Playwright 打开 Bing → 首页拿 cookie → 搜索框提交 → 自动抓取 top N 页面内容
延迟：首次 3~6s（启动浏览器），后续复用更快
```

### 海外搜索流程

```
纯 HTTP → DDG HTML 解析 → 自动抓取 top N 页面内容
延迟：几百ms~1s
```

### 抓取模式

| 层级  | 方式                | 速度   | 说明             |
| --- | ----------------- | ---- | -------------- |
| 第1层 | 轻量 HTTP + cheerio | ⚡ 秒出 | 不启动浏览器         |
| 第2层 | Playwright headed | 🟡 慢 | 完整浏览器，支持 JS 渲染 |

## 区域检测

每次搜索时自动检测，三轮探测并行，谁先成功用谁：

| 轮次  | 探测服务                       | 逻辑      |
| --- | -------------------------- | ------- |
| 第1轮 | `myip.ipip.net` / `cip.cc` | 国内可达优先  |
| 第2轮 | `ipinfo.io` / `ipapi.co`   | 国际探测    |
| 第3轮 | 试连 `cn.bing.com`           | 能通大概率国内 |
| 兜底  | —                          | 默认国内    |

## 去重

智能去重：域名 + 路径主干（忽略 www/m 子域、tracking 参数、尾部斜杠、.html 后缀）。

Bing 跳转 URL（`bing.com/ck/`）自动解码为直链。

## 已知限制

- **国内首次搜索较慢**：需启动 Chromium（3\~6s），后续复用更快
- **Bing CN 即时答案不返回**：天气、计算器等即时卡片不走 `li.b_algo`，搜索结果为 0
- **搜狗 HTTP 不稳定**：无 cookie 纯请求结果可能为空（`--engine=sogou` 慎用）
- **部分站点 HTTP 抓不到**：需要 JS 渲染的页面——HTTP 失败会自动 headed 重试
- **部分站点海外不可达**：国内专属站点从海外访问可能超时
- **代理干扰 IP 检测**：出口 IP 走代理时可能误判区域，用 `--region=cn/intl` 手动指定
- **海外引擎国内不可达**：DDG 在国内被墙，国内策略不使用

## 许可证

MIT License
