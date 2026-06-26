# CNINFO (巨潮资讯网) PDF 提取方法

## 问题

巨潮公告详情页中的 PDF 地址是 **动态生成 + 有时限** 的。直接构造 URL（如 `https://disc.static.szse.cn/download/...`）返回 404。通过静态 curl 抓取 HTML 也拿不到真实 PDF 链接（页面纯 JS 渲染）。

## 解决方案：用 Hermes browser 工具

Hermes 内置的 browser 工具（agent-browser 驱动）可以打开 JS 渲染的页面，与页面交互，获取真实下载链接。

### 前置条件：配置 Chrome

在 **国内服务器 / 无图形界面环境** 中：

#### ✅ 方案 A：复用 Playwright 已装的 Chrome（推荐，零下载）

```bash
# 检查是否存在
ls ~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome

# 设置环境变量（已注入 browser_tool.py，下次会话自动生效）
export AGENT_BROWSER_EXECUTABLE_PATH=~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome
export AGENT_BROWSER_ARGS="--no-sandbox"
```

**Hermes 补丁状态：** `browser_tool.py` 第1477-1484行已注入这两个环境变量。**需要重启 Hermes 会话才能生效**（当前会话已加载的旧代码不会看到补丁）。

#### ❌ 方案 B：agent-browser install（不推荐）

通过代理下载 Chrome 175MB，Vultr代理约需5-10分钟，且经常超时中断。**不推荐使用。**

### 已验证的操作流程

#### Step 1：打开公告列表页

```bash
export AGENT_BROWSER_EXECUTABLE_PATH=~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome
export AGENT_BROWSER_ARGS="--no-sandbox"

agent-browser open \
  "https://www.cninfo.com.cn/new/disclosure/stock?stockCode=002812&orgId=9900023446" \
  --session target
```

#### Step 2：等待页面加载并截图

```bash
agent-browser wait --load networkidle --session target
sleep 3  # 等JS渲染完成
agent-browser snapshot -i -c --session target
```

页面渲染后能看到完整的公告列表（含标题+日期），通过 `@eN` ref 定位目标公告。

#### Step 3：提取 announcementId（✅ 已验证可行）

用 `get attr` 直接拿公告链接的 `href`，无需点击跳转：

```bash
agent-browser get attr @eN href --session target
# 返回示例:
# /new/disclosure/detail?plate=szse&orgId=9900026450&stockCode=002812
#   &announcementId=1225304895&announcementTime=2026-05-14
```

**关键参数：** `announcementId=1225304895`

#### Step 4：打开详情页（✅ 已验证可行）

```bash
agent-browser open \
  "https://www.cninfo.com.cn/new/disclosure/detail?plate=szse\
   &orgId=9900026450&stockCode=002812\
   &announcementId=1225304895&announcementTime=2026-05-14" \
  --session detail
```

#### Step 5：点击"公告下载"按钮下载 PDF（✅ 已验证完整工作流）

详情页渲染成功后，可见：
- 公告名称（如"恩捷股份"）
- 股票代码显示（如 "002812"）
- **"公告下载"按钮**（`@e5`，文本 `<i class="iconfont icongonggaoxiazai"></i> 公告下载`）
- "全屏"链接

点击公告下载按钮应能获取真实 PDF 地址或触发下载。

**验证结果（2026-05-14 恩捷股份公告）：** 点击按钮后 PDF 自动保存到 `~/Downloads/恩捷股份：关于在自贡市投资建设锂电池隔离膜项目的公告.pdf`。文件为 PDF 1.7 格式，4页，137KB。可通过 `python3 -c "import fitz; doc = fitz.open('path/to.pdf'); [print(page.get_text()) for page in doc]"` 读取文字内容（需 `pip install pymupdf`）。

```bash
# 从PDF中提取文字（完整工作流）
agent-browser click @e5 --session detail      # 点击公告下载
# PDF 自动保存到 ~/Downloads/
ls -lh ~/Downloads/*.pdf
python3 -c "
import fitz
doc = fitz.open('~/Downloads/恩捷股份*.pdf')
for page in doc:
    print(page.get_text())
"
```

### 备选：纯 API 拿公告文本

不需要 PDF 原文，只需要标题+日期等元信息，直接用巨潮全文搜索 API：

```bash
curl -s "http://www.cninfo.com.cn/new/fulltextSearch/full" \
  -H "User-Agent: Mozilla/5.0" \
  -d "searchkey=002812&pageNum=1&pageSize=20&sortName=pubdate&sortType=desc"
```

返回 JSON 含 `announcementId`、`announcementTitle`、`announcementTime` 等。

### 注意事项

1. **Chrome 需要 --no-sandbox** — 服务器/Docker/VM 环境必须加此参数
2. **CDN 资源** — 巨潮用阿里云 CDN，国内访问一般很快 (~0.3s)
3. **announcementId 提取捷径** — 用 `get attr` 而非 `click`，避免页面跳转
4. **session 管理** — 用 `--session` 参数隔离不同任务，完成后 `agent-browser close --session X` 清理
5. **环境变量注入（代码补丁）** — Hermes 的 `tools/browser_tool.py`（browser_env 构造处，1477-1484行）已自动设置 `AGENT_BROWSER_EXECUTABLE_PATH` 和 `AGENT_BROWSER_ARGS`。补丁在下次 Hermes 会话重启后生效。**不支持 config.yaml 配置** — environment variables are injected directly into the subprocess env dict, not read from config.yaml.
6. **PDF 直链有时限** — 巨潮的 PDF 下载链接通常只在当天有效，跨天会过期
