# browser-collector 完整集成方案

**版本**: 1.1.0
**更新日期**: 2026-04-18
**状态**: 已实现

---

## 一、整体架构

```
browser-collector/
├── SKILL.md                          # 技能定义文档 [已有]
├── collectors/
│   ├── __init__.py                   # 模块导出 [已有]
│   ├── base.py                       # 数据结构定义 [已有]
│   ├── registry.py                   # 采集器注册 [已有]
│   ├── cli.py                        # 统一CLI [已增强]
│   │
│   ├── captcha_solver.py             # ✅ 新增：验证码识别（ddddocr + 预处理 + 滑块轨迹）
│   ├── tesseract_ocr.py              # ✅ 新增：Tesseract OCR优化
│   ├── batch_collector.py            # ✅ 新增：批量采集 + 多进程Session隔离
│   ├── stealth.py                    # ✅ 新增：Playwright反检测（多级配置）
│   ├── proxy_pool.py                 # ✅ 新增：免费代理池（抓取 → 验证 → 评分）
│   ├── cookie_db.py                  # ✅ 新增：SQLite Cookie持久化（加密 + 多域名）
│   │
│   └── builtin/
│       ├── browser_collector.py      # ✅ 新增：通用浏览器采集器（一站式整合）
│       ├── eastmoney.py              # [已有]
│       ├── xueqiu.py                 # [已有]
│       └── akshare.py                # [已有]
│
└── browser/
    ├── __init__.py                   # [已有]
    ├── playwright.py                 # [已有]
    ├── captcha.py                    # [已有]（旧版验证码，现已升级）
    └── login.py                       # [已有]
```

---

## 二、模块详细设计

### 2.1 captcha_solver.py — 验证码识别模块

**文件路径**: `collectors/captcha_solver.py`
**职责**: 提供文字验证码识别和滑块验证码轨迹生成
**依赖**: `ddddocr`, `opencv-python`, `numpy`, `Pillow`

#### 关键类

| 类名 | 职责 | 核心方法 |
|------|------|----------|
| `CaptchaSolver` | 文字验证码识别（主引擎ddddocr + Tesseract fallback） | `solve_image(bytes)`, `solve_with_preprocess(path)`, `solve_as_item()` |
| `SliderCaptchaSolver` | 滑块验证码缺口检测 + 人类轨迹生成 | `detect_gap(path)`, `generate_track(ratio, width)`, `solve_slider(path)` |
| `CaptchaResult` | 识别结果（兼容StructuredItem） | 继承`StructuredItem`，含`captcha_type`, `confidence`, `processing_time_ms` |

#### API设计

```python
# 文字验证码
solver = CaptchaSolver(beta=False)
result = solver.solve_image(image_bytes)                          # bytes → str
result = solver.solve_with_preprocess('captcha.png')            # 文件 → str（带预处理）
item = solver.solve_as_item(image_bytes, platform='github')      # → CaptchaResult(StructuredItem)

# 滑块验证码
slider = SliderCaptchaSolver()
gap_ratio = slider.detect_gap('bg.png')                           # 0.0-1.0
track = slider.generate_track(gap_ratio, total_width=300)        # [(x,y,delay_ms), ...]
steps = slider.solve_slider('bg.png')                             # → [{'x', 'y', 'delay'}, ...]

# 在Playwright中执行轨迹
solve_slider_with_playwright(page, '[class="slider"]', track)
```

#### 与 base.py 兼容性

- `CaptchaResult` 继承 `StructuredItem`
- `content` 字段 = 识别文字
- `quality_score` = 识别置信度（0-1）
- `platform` = 目标站点

---

### 2.2 tesseract_ocr.py — Tesseract OCR优化模块

**文件路径**: `collectors/tesseract_ocr.py`
**职责**: 通用OCR识别，适合长文本、文档、混合语言（与ddddocr互补）
**依赖**: `pytesseract`, `opencv-python`, `tesseract-ocr`（系统包）

#### 关键类

| 类名 | 职责 | 核心方法 |
|------|------|----------|
| `TesseractOCR` | Tesseract OCR识别器 | `preprocess_for_tesseract(path)`, `recognize(path)`, `get_confidence(path)` |

#### API设计

```python
ocr = TesseractOCR(lang='eng+chi_sim', psm=7)

# 预处理后识别
img = ocr.preprocess_for_tesseract('doc.png')   # → PIL.Image
text = ocr.recognize('doc.png')                  # → str

# 带置信度
text, conf = ocr.get_confidence('doc.png')       # → (str, 0-100)

# StructuredItem格式
item = ocr.recognize_as_item('doc.png', platform='doc')
```

#### 预处理流程

```
灰度化 → 非局部均值去噪 → 锐化卷积 → 自适应二值化 → 边框干扰去除 → PIL.Image
```

---

### 2.3 batch_collector.py — 批量采集 + 多进程隔离

**文件路径**: `collectors/batch_collector.py`
**职责**: 支持大规模URL批量采集，多进程隔离避免Session冲突
**依赖**: `playwright`, `concurrent.futures`

#### 关键类

| 类名 | 职责 | 核心方法 |
|------|------|----------|
| `SessionManager` | 多进程Session隔离（每域名独立Context） | `get_session(domain)`, `save_session(domain)`, `close_all()` |
| `BatchCollector` | 线程池批量采集（控制并发） | `collect_urls(urls, handler, progress)`, `collect_urls_as_items()` |
| `ProcessBatchCollector` | 多进程批量采集（真正进程隔离） | `start()`, `submit_task(url)`, `iter_results()`, `stop()` |
| `CollectTask` | 采集任务数据结构 | — |
| `CollectResult` | 采集结果（可转StructuredItem） | `to_item()` |

#### API设计

```python
# 线程池模式（适合中小规模）
batch = BatchCollector(max_workers=2, max_per_domain=50)
items = batch.collect_urls(urls, progress_callback=lambda d,t: print(f'{d}/{t}'))

# StructuredItem版本
items = batch.collect_urls_as_items(urls, handler=my_handler)

# 多进程模式（适合大规模）
collector = ProcessBatchCollector(max_workers=2)
collector.start()
for url in urls:
    collector.submit_task(url)
for result in collector.iter_results():
    print(result)
collector.stop()

# 自定义handler（返回StructuredItem兼容dict）
def my_handler(page, url):
    page.goto(url)
    return {'title': page.title(), 'url': url, 'platform': 'test'}
```

#### 性能设计

- **Session隔离**: 按域名独立Context，防止Cookie跨域污染
- **LRU缓存**: `max_contexts`控制Context数量，超出后LRU淘汰
- **请求限速**: `request_interval`控制同域名请求间隔
- **多进程**: `ProcessBatchCollector`用独立进程+Queue，真正隔离

---

### 2.4 stealth.py — Playwright反检测模块

**文件路径**: `collectors/stealth.py`
**职责**: 完整的浏览器指纹隐藏和反检测能力
**依赖**: `playwright`（纯JS注入）

#### 关键类

| 类名 | 职责 | 核心方法 |
|------|------|----------|
| `StealthConfig` | 反检测配置（preset + 可扩展） | `get_combined_script()` |
| `StealthScripts` | JS脚本库（11种脚本） | — |

#### 反检测级别

| 级别 | 脚本 | 说明 |
|------|------|------|
| `basic` | webdriver_hide, chrome_object, plugins, languages | 基础必备 |
| `medium` | basic + canvas_randomize, webgl_spoof, permissions_api | 推荐默认 |
| `aggressive` | medium + audio_context, connection_info, device_memory, hardware_concurrency, platform | 最高隐蔽 |

#### 可用脚本清单

```
webdriver_hide       # 隐藏navigator.webdriver
chrome_object        # 伪造window.chrome对象
plugins              # 伪造navigator.plugins
languages            # 伪造navigator.languages
canvas_randomize     # Canvas指纹随机化
webgl_spoof         # WebGL厂商/渲染器伪装
audio_context       # AudioContext指纹处理
permissions_api      # Permissions.query伪造
connection_info      # Network Information API
device_memory        # navigator.deviceMemory
hardware_concurrency # navigator.hardwareConcurrency
platform             # navigator.platform
```

#### API设计

```python
# 独立使用
config = StealthConfig(level='medium', randomize=True)
apply_stealth(context, config)

# 创建Context时自动注入
context = stealth_context(browser, level='aggressive')

# CLI
python collectors/stealth.py --list  # 列出所有脚本
python collectors/stealth.py --level medium  # 输出合并后的脚本
```

---

### 2.5 proxy_pool.py — 免费代理池

**文件路径**: `collectors/proxy_pool.py`
**职责**: 从公开源抓取代理 → 验证 → 评分 → 按需分配
**依赖**: `aiohttp`, `playwright`

#### 关键类

| 类名 | 职责 | 核心方法 |
|------|------|----------|
| `ProxyInfo` | 代理信息 dataclass | `score`（综合评分0-1） |
| `ProxyPool` | 异步代理池 | `fetch_all()`, `verify_all()`, `get_working_proxy()`, `auto_maintain()` |
| `SyncProxyPool` | 同步封装（用于Playwright） | `get_proxy()`, `refresh()` |

#### 代理源

```python
FREE_PROXY_SOURCES = {
    'github_1': 'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'github_2': 'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'github_3': 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'proxyscan': 'https://www.proxyscan.io/api/proxy?limit=20&type=http',
    'free-proxy-list': 'https://free-proxy-list.net/',
    'ssl-proxy': 'https://sslproxies.org/',
}
```

#### 评分算法

```
综合评分 = 成功率×0.5 + (1 - 归一化延迟/5000ms)×0.3 + (1 - 失败次数/10)×0.2
```

#### API设计

```python
# 异步使用
pool = ProxyPool()
stats = asyncio.run(pool.refresh_and_verify())
proxy = pool.get_working_proxy()  # 返回最优代理

# 同步使用（Playwright）
sync_pool = SyncProxyPool()
proxy_url = sync_pool.get_url()   # → 'http://1.2.3.4:8080'
page.set_proxy(proxy={'server': proxy_url})

# CLI
python collectors/cli.py proxy --refresh
python collectors/cli.py proxy --test --limit 10
python collectors/cli.py proxy --status
```

---

### 2.6 cookie_db.py — SQLite Cookie持久化

**文件路径**: `collectors/cookie_db.py`
**职责**: SQLite存储、加密、分域隔离、自动清理
**依赖**: `sqlite3`（内置）

#### 关键类

| 类名 | 职责 | 核心方法 |
|------|------|----------|
| `CookieRecord` | Cookie记录 dataclass | `is_expired`, `to_dict()` |
| `CookieDatabase` | SQLite存储核心 | `save_cookies()`, `get_cookies()`, `delete_expired()` |
| `MultiDomainCookieManager` | 多域名Cookie管理 | `get_all_cookies_for_request(url)`, `sync_to_context()` |

#### API设计

```python
# 基础使用
db = CookieDatabase('./data/cookies.db')
db.save_cookies(playwright_cookies, 'github.com')  # 批量保存
cookies = db.get_cookies('github.com')             # 获取（Playwright格式）
context.add_cookies(cookies)                       # 注入到Context

# 多域名管理
manager = MultiDomainCookieManager()
cookies = manager.get_all_cookies_for_request('https://api.github.com/repos/...')
# 自动包含 github.com + api.github.com + gist.github.com 的Cookie

# CLI
python collectors/cli.py cookie --status
python collectors/cli.py cookie --export --domain github.com
python collectors/cli.py cookie --delete-expired
```

---

### 2.7 builtin/browser_collector.py — 通用浏览器采集器

**文件路径**: `collectors/builtin/browser_collector.py`
**职责**: 一站式整合所有模块，提供通用Playwright采集能力
**依赖**: `playwright`, `captcha_solver`, `cookie_db`, `stealth`, `proxy_pool`

#### 关键类

| 类名 | 职责 | 核心方法 |
|------|------|----------|
| `BrowserCollector` | 通用浏览器采集器 | `collect(url)`, `solve_captcha()`, `batch()`, `save_screenshot()` |
| `BatchCollectorWrapper` | BatchCollector便捷包装 | `collect_urls(urls)` |

#### API设计

```python
# 基本使用
collector = BrowserCollector()
item = collector.collect('https://github.com/microsoft/vscode')
print(item.title, item.content[:200])

# 带代理
collector = BrowserCollector(proxy_pool=ProxyPool())

# 批量采集
with collector.batch(max_workers=2) as batch:
    items = batch.collect_urls(urls, progress_callback=lambda d,t: print(f'{d}/{t}'))

# 验证码处理
result = collector.solve_captcha(page)              # 自动截取验证码图片
collector.solve_slider_captcha(page, 'bg.png')      # 处理滑块

# 自定义适配器
collector.register_adapter('github', MyGitHubAdapter())
item = collector.collect('https://github.com/microsoft/vscode', adapter='github')

# CLI
python collectors/cli.py collect --url https://github.com/microsoft/vscode --adapter github
python collectors/cli.py batch --file urls.txt --workers 2
```

#### 内置适配器映射

```python
DEFAULT_ADAPTERS = {
    'github.com': 'github',
    'zhihu.com': 'zhihu',
    'juejin.cn': 'juejin',
    'csdn.net': 'csdn',
    'aliyun.com': 'aliyun',
    'help.aliyun.com': 'aliyun',
}
```

---

## 三、CLI命令完整清单

### 新增命令

```bash
# 浏览器采集
python collectors/cli.py collect --url URL [--adapter NAME] [--wait-selector SEL] [--json]
python collectors/cli.py collect --url https://github.com/microsoft/vscode --adapter github

# 批量采集
python collectors/cli.py batch --file urls.txt --workers 2 [--output results.json]
python collectors/cli.py batch --url URL1 --url URL2 --workers 2

# 验证码识别
python collectors/cli.py captcha recognize captcha.png [--preprocess] [--beta]
python collectors/cli.py captcha number captcha.png
python collectors/cli.py captcha chinese captcha_zh.png
python collectors/cli.py captcha test

# 滑块验证码
python collectors/cli.py slider detect gap.png
python collectors/cli.py slider solve gap.png

# 代理池
python collectors/cli.py proxy refresh
python collectors/cli.py proxy test --limit 10
python collectors/cli.py proxy status

# Cookie管理
python collectors/cli.py cookie status
python collectors/cli.py cookie export --domain github.com
python collectors/cli.py cookie delete-expired
```

### 原有命令（保持兼容）

```bash
python collectors/cli.py --list
python collectors/cli.py --collector eastmoney --action quote 600000
python collectors/cli.py --collector eastmoney --action limit-up --limit 50
python collectors/cli.py --collector xueqiu --action hot --limit 20
```

---

## 四、与 base.py StructuredItem 的兼容性

所有新增模块的返回值均为 `StructuredItem` 或其子类：

```python
# captcha_solver.py
CaptchaResult(StructuredItem)
  - content: str          = 识别文字
  - quality_score: float = 置信度 0-1
  - platform: str         = 目标站点
  - captcha_type: str     = 'image' | 'slider'
  - confidence: float     = 置信度
  - processing_time_ms: float

# tesseract_ocr.py
StructuredItem (via recognize_as_item)
  - content: str          = 识别文字
  - quality_score: float  = 置信度/100
  - platform: str          = 指定平台

# batch_collector.py
CollectResult
  - to_item() → Optional[StructuredItem]

# cookie_db.py
CookieRecord (dataclass风格)
  - to_dict() → Playwright格式Cookie列表
```

---

## 五、测试验证方案

### 单元测试

```bash
# captcha_solver
python -c "from collectors.captcha_solver import CaptchaSolver, SliderCaptchaSolver; s=SliderCaptchaSolver(); print(s.detect_gap('test.png'))"

# tesseract_ocr
python collectors/tesseract_ocr.py test

# stealth
python collectors/stealth.py --list

# proxy_pool
python collectors/proxy_pool.py refresh  # 需要网络

# cookie_db
python collectors/cookie_db.py status

# CLI集成测试
python collectors/cli.py --list
python collectors/cli.py captcha test
python collectors/cli.py proxy status
python collectors/cli.py cookie status
```

### 集成测试

```bash
# 1. 浏览器采集测试
python collectors/cli.py collect --url https://www.github.com --visible

# 2. 批量采集测试（创建测试文件）
echo "https://github.com" > /tmp/test_urls.txt
echo "https://baidu.com" >> /tmp/test_urls.txt
python collectors/cli.py batch --file /tmp/test_urls.txt --workers 1

# 3. 完整流程测试
python -c "
from collectors.builtin.browser_collector import BrowserCollector
from collectors.cookie_db import CookieDatabase
from collectors.captcha_solver import CaptchaSolver

# 测试采集器初始化
c = BrowserCollector()
print('BrowserCollector initialized')

# 测试Cookie持久化
db = CookieDatabase()
stats = db.get_statistics()
print(f'Cookie DB: {stats}')

# 测试验证码
s = CaptchaSolver()
print('CaptchaSolver initialized')

c.close()
print('All tests passed')
"
```

---

## 六、依赖清单

```txt
# Python依赖（pip install）
playwright>=1.40.0
ddddocr>=1.4.11
opencv-python>=4.8.0
numpy>=1.24.0
Pillow>=10.0.0
pytesseract>=0.3.10
aiohttp>=3.9.0

# 系统依赖
# - Tesseract OCR: apt install tesseract-ocr
# - Playwright浏览器: playwright install chromium

# Node.js依赖（Playwright需要）
# Node.js >= 16
```

---

## 七、文件清单（新增/修改）

| 文件 | 状态 | 行数 | 说明 |
|------|------|------|------|
| `collectors/captcha_solver.py` | ✅ 新增 | ~500 | 验证码识别 |
| `collectors/tesseract_ocr.py` | ✅ 新增 | ~300 | Tesseract优化 |
| `collectors/batch_collector.py` | ✅ 新增 | ~700 | 批量采集 |
| `collectors/stealth.py` | ✅ 新增 | ~450 | 反检测 |
| `collectors/proxy_pool.py` | ✅ 新增 | ~500 | 代理池 |
| `collectors/cookie_db.py` | ✅ 新增 | ~450 | Cookie持久化 |
| `collectors/builtin/browser_collector.py` | ✅ 新增 | ~600 | 通用采集器 |
| `collectors/cli.py` | ✅ 增强 | ~550 | 新增6个子命令 |

**总计新增代码**: ~4050 行

---

## 八、已知限制

1. **免费代理质量**: 免费代理成功率 <20%，关键业务不建议依赖
2. **ddddocr中文识别**: 对某些复杂字体识别率有限，建议配合Tesseract fallback
3. **滑块验证码**: 依赖背景图缺口明显程度，极端情况可能失败
4. **多进程Cookie**: 多进程写入同一SQLite需注意并发（已用Lock保护）
5. **Tesseract依赖**: 需要系统安装`tesseract-ocr`命令
