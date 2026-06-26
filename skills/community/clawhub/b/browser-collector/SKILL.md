# Browser Collector Skill

**版本**: 1.3.0
**更新日期**: 2026-05-02
**状态**: 架构整合完成 ✅

---

## 简介

browser-collector 是基于 Playwright 的浏览器数据采集工具，提供反检测、代理池、验证码识别、批量采集等企业级功能。

## 快速入门

### 安装依赖
```bash
pip install -r requirements.txt
playwright install chromium
```

### 基本使用
```python
from collectors.adapters.builtin.cloud_docs.aliyun import AliyunDocAdapter
from collectors.adapters.extraction.spawait import wait_for_page_ready

# 创建适配器
adapter = AliyunDocAdapter()

# 使用
result = adapter.extract(page, "https://help.aliyun.com/document_detail/xxx")
print(result.title)
print(result.content)
```

### CLI 使用
```bash
# 采集文档
python3 collectors/cli.py collect --url "https://help.aliyun.com/document_detail/xxx"

# 使用指定适配器
python3 collectors/cli.py collect --url "xxx" --adapter aliyun_doc

# 批量采集
python3 collectors/cli.py batch --file urls.txt --workers 5
```

## 目录结构

```
browser-collector/
├── SKILL.md                          # 本文件
├── INTEGRATION_PLAN.md               # 集成方案文档
├── requirements.txt                  # Python依赖
├── spa_sites.json                    # SPA站点配置
├── collectors/
│   ├── __init__.py                   # 模块导出
│   ├── base.py                       # 数据结构定义（StructuredItem等）
│   ├── registry.py                   # 采集器注册表（CollectorRegistry）
│   ├── cli.py                        # 统一CLI入口
│   │
│   ├── captcha_solver.py             # 验证码识别（ddddocr + 滑块轨迹）
│   ├── tesseract_ocr.py              # Tesseract OCR优化
│   ├── batch_collector.py            # 批量采集 + 多进程Session隔离
│   ├── stealth.py                    # Playwright反检测（多级配置）
│   ├── proxy_pool.py                 # 代理池（抓取→验证→评分）
│   ├── cookie_db.py                  # SQLite Cookie持久化（加密）
│   │
│   ├── adapters/                    # 适配器系统（重构后）
│   │   ├── __init__.py              # 模块导出（自动注册所有内置适配器）
│   │   ├── base.py                  # 统一DocAdapter基类 + AdapterRegistry注册表
│   │   │
│   │   ├── builtin/                # 内置适配器
│   │   │   ├── cloud_docs/         # 云厂商文档
│   │   │   │   ├── aliyun.py       # 阿里云文档
│   │   │   │   ├── tencent.py      # 腾讯云
│   │   │   │   ├── volcengine.py   # 火山引擎
│   │   │   │   └── coze.py         # Coze扣子
│   │   │   ├── api_docs/           # API文档
│   │   │   │   ├── kimi.py         # Kimi API
│   │   │   │   └── minimax.py      # MiniMax API
│   │   │   └── social/             # 社交媒体
│   │   │       ├── github.py       # GitHub仓库/Issue/用户
│   │   │       ├── zhihu.py        # 知乎
│   │   │       ├── juejin.py       # 掘金
│   │   │       └── csdn.py        # CSDN
│   │   │
│   │   └── extraction/              # 提取能力模块
│   │       ├── __init__.py
│   │       ├── structure.py        # 结构化数据模型（DocumentItem等）
│   │       └── spawait.py          # 动态等待策略
│   │
│   └── builtin/                    # 兼容层（仅browser_collector.py）
│       └── browser_collector.py    # 通用浏览器采集器
```

## 核心功能

### 1. 通用浏览器采集器
```python
from collectors.builtin.browser_collector import BrowserCollector

collector = BrowserCollector(headless=True)
result = await collector.collect(url="https://example.com", wait_until="networkidle")
```

### 2. 文档适配器系统（★新增）
```python
from collectors.adapters import get_registry

# 获取适配器（自动注册所有内置适配器）
registry = get_registry()
adapter = registry.get_for_url('https://help.aliyun.com/doc')

# 提取完整文档结构
doc = adapter.extract(page, url)

# DocumentItem 包含：
# - toc: 嵌套目录结构
# - content: 正文内容
# - code_blocks: 代码块列表（带语言标记）
# - tables: 表格列表
# - images: 图片列表

# 输出格式
print(doc.to_json())      # JSON格式
print(doc.to_markdown())  # Markdown格式
```

### 3. 内置网站适配器
- **东方财富**: 股票数据、财经新闻
- **雪球**: 投资者社区、股票讨论
- **知乎**: 文章、问答
- **掘金**: 技术文章
- **CSDN**: 技术博客
- **GitHub**: 代码仓库信息
- **阿里云文档**: 云厂商文档（★重构）

### 4. 反检测功能
```python
from collectors.stealth import StealthConfig, apply_stealth

config = StealthConfig(level="high")  # low, medium, high
context = await browser.new_context()
apply_stealth(context, config)
```

### 5. 代理池
```python
from collectors.proxy_pool import ProxyPool

pool = ProxyPool()
proxy = await pool.get_proxy()  # 自动抓取、验证、评分
```

### 6. 验证码识别
```python
from collectors.captcha_solver import CaptchaSolver

solver = CaptchaSolver()
result = await solver.solve_captcha(image_bytes)
```

### 7. 批量采集
```python
from collectors.batch_collector import BatchCollector

collector = BatchCollector(max_workers=5)
results = await collector.run(urls=["url1", "url2", ...])
```

## CLI使用方式

```bash
# 通用采集（必填：--url）
python3 collectors/cli.py collect --url https://example.com

# 指定适配器采集
python3 collectors/cli.py collect --url https://help.aliyun.com/doc/xxx --adapter aliyun_doc

# 等待元素出现后采集
python3 collectors/cli.py collect --url https://platform.kimi.com/api/doc --wait-selector ".api-endpoint" --wait-time 5

# 东方财富数据
python3 collectors/cli.py eastmoney --stock 600519 --type basic

# 雪球数据
python3 collectors/cli.py xueqiu --symbol AAPL --type discussion

# 批量采集
python3 collectors/cli.py batch --file urls.txt --workers 5

# 代理池测试
python3 collectors/cli.py proxy --test
```

## 依赖安装

```bash
pip install -r requirements.txt
playwright install chromium
```

## 配置说明

### 反检测级别
| 级别 | 说明 |
|------|------|
| low | 基本隐身模式 |
| medium | 拦截 WebDriver 属性 |
| high | 完整反检测 + 随机UA |

### 代理池评分
- 分数 > 80: 优质代理
- 分数 50-80: 普通代理
- 分数 < 50: 低质代理（自动剔除）

## 注意事项

1. 反检测功能会修改 navigator 对象，慎用于需要真实信息的场景
2. 批量采集建议设置合理的 `max_workers` 避免被封
3. Cookie持久化支持多域名隔离
4. 验证码识别需要配置ddddocr模型

---

## 能力矩阵

### 适配器总览

| 适配器 | 支持站点 | 核心能力 | 状态 |
|--------|---------|---------|------|
| **云厂商文档** | | | |
| AliyunDocAdapter | help.aliyun.com | ✅ 文档结构化提取（标题/目录/正文/代码块/表格/图片/面包屑/元信息） | ✅ 已实现 |
| TencentDocAdapter | cloud.tencent.com | ✅ 文档结构化提取（标题/目录/正文/代码块/表格/图片/面包屑/元信息） | ✅ 已实现 |
| VolcengineDocAdapter | volcengine.com | ✅ 文档结构化提取（标题/目录/正文/代码块/表格/图片/面包屑/元信息） | ✅ 已实现 |
| CozeDocAdapter | coze.com, coze.cn | ✅ 文档结构化提取（标题/目录/正文/代码块/表格/图片/面包屑/元信息） | ✅ 已实现 |

| **API 文档** | | | |
| KimiApiAdapter | platform.kimi.com, api.moonshot.cn | ✅ API端点提取（路径/方法/参数/示例）、✅ 模型列表、✅ 代码示例 | ✅ 已实现 |
| MiniMaxApiAdapter | platform.minimaxi.com, api.minimax.chat | ✅ API端点提取（路径/方法/参数/示例）、✅ 模型列表、✅ 代码示例 | ✅ 已实现 |
| **社交媒体** | | | |
| GitHubAdapter | github.com | ✅ 仓库提取、✅ Issue提取、✅ 用户页、✅ README | ✅ 已实现 |

| ZhihuAdapter | zhihu.com | ✅ 文章提取、✅ 问答提取 | ✅ 已实现 |
| JuejinAdapter | juejin.cn | ✅ 技术文章提取 | ✅ 已实现 |
| CsdnAdapter | csdn.net | ✅ 技术博客提取 | ✅ 已实现 |
| **科技媒体** | | | |

| **通用采集** | | | |
| BrowserCollector | 通用网站 | ✅ 通用页面采集、✅ 反检测、✅ 代理池、✅ 验证码识别 | ✅ 已实现 |
| EastmoneyCollector | eastmoney.com | ✅ 股票数据、✅ 财经新闻 | ✅ 已实现 |
| XueqiuCollector | xueqiu.com | ✅ 投资者社区、✅ 股票讨论 | ✅ 已实现 |

### 适配器能力详情

#### 云厂商文档适配器

| 能力 | AliyunDocAdapter |
|------|------------------|
| 标题提取 | ✅ |
| 目录提取（侧边栏） | ✅ |
| 正文内容（Markdown） | ✅ |
| 代码块（带语言标记） | ✅ |
| 表格（格式保留） | ✅ |
| 图片（含Alt） | ✅ |
| 面包屑导航 | ✅ |
| 作者信息 | ✅ |
| 发布/更新时间 | ✅ |
| 版本标签 | ✅ |
| 标签提取 | ✅ |

#### 腾讯云/火山引擎文档适配器

| 能力 | TencentDocAdapter | VolcengineDocAdapter |
|------|-------------------|---------------------|
| 标题提取 | ✅ | ✅ |
| 目录提取（侧边栏） | ✅ | ✅ |
| 正文内容（Markdown） | ✅ | ✅ |
| 代码块（带语言标记） | ✅ | ✅ |
| 表格（格式保留） | ✅ | ✅ |
| 图片（含Alt） | ✅ | ✅ |
| 面包屑导航 | ✅ | ✅ |
| 作者信息 | ✅ | ✅ |
| 发布/更新时间 | ✅ | ✅ |
| 版本标签 | ✅ | ✅ |
| 标签提取 | ✅ | ✅ |

#### API文档适配器

| 能力 | KimiApiAdapter | MiniMaxApiAdapter |
|------|---------------|-------------------|
| API端点提取 | ✅ | ✅ |
| HTTP方法识别 | ✅ | ✅ |
| 参数列表（名称/类型/必填/描述） | ✅ | ✅ |
| 请求示例（JSON） | ✅ | ✅ |
| 响应示例（JSON） | ✅ | ✅ |
| 代码示例（curl/Python） | ✅ | ✅ |
| 模型列表 | ✅ | ✅ |
| 速率限制信息 | ✅ | ✅ |
| 认证方式 | ✅ | ✅ |
| 标签/分类 | ✅ | ✅ |
| 面包屑导航 | ✅ | ✅ |

#### 通用适配器

| 能力 | BrowserCollector | EastmoneyCollector | XueqiuCollector |
|------|------------------|---------------------|-----------------|
| 页面内容提取 | ✅ | ✅ | ✅ |
| 反检测（Playwright） | ✅ | ✅ | ✅ |
| 代理池 | ✅ | ✅ | ✅ |
| 验证码识别 | ✅ | ✅ | ✅ |
| 批量采集 | ✅ | ✅ | ✅ |
| Cookie持久化 | ✅ | ✅ | ✅ |

### 适配器选择建议

```python
from collectors.adapters import get_registry

registry = get_registry()

# 自动选择适配器（根据URL）
adapter = registry.get_for_url('https://help.aliyun.com/doc/12345')

# 手动指定适配器
adapter = registry.get('aliyun_doc')

# 列出所有适配器
all_adapters = registry.list_all()
for name in all_adapters:
    adapter = registry.get(name)
    print(f"{name}: {adapter.__class__.__name__}")
```