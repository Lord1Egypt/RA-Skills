# URL 处理器架构说明

## 📁 目录结构

```
handlers/
├── __init__.py              # 包初始化，自动注册所有处理器
├── base_handler.py          # 基类，定义统一接口
├── general_handler.py       # 通用网页处理器
├── doubao_handler.py        # 豆包专用处理器
├── wechat_handler.py        # 微信公众号处理器
├── zhihu_handler.py         # 知乎处理器
├── juejin_handler.py        # 掘金处理器
└── README.md                # 本文档
```

## 🏗️ 架构设计

### 核心思想

**分类处理、互不影响、易于扩展**

每个网站类型有独立的处理器类，继承自统一的基类 `BaseURLHandler`。

### 类图

```
BaseURLHandler (抽象基类)
    │
    ├── GeneralHandler     → 通用网页（*）
    ├── DoubaoHandler      → 豆包（doubao.com）
    ├── WeChatHandler      → 微信公众号（mp.weixin.qq.com）
    ├── ZhihuHandler       → 知乎（zhihu.com）
    └── JuejinHandler      → 掘金（juejin.cn）
```

## 🚀 使用方法

### 基本用法

```python
from handlers import get_handler

# 根据 URL 自动获取对应处理器
handler = get_handler("https://www.doubao.com/thread/xxx")

# 抓取内容
result = handler.fetch(page)

# 获取结果
if result.success:
    print(f"标题：{result.title}")
    print(f"内容：{result.content[:500]}")
    print(f"图片：{len(result.images)}张")
else:
    print(f"失败：{result.error}")
```

### 在主脚本中使用

```python
# amber_url_to_markdown.py

from handlers import get_handler

# 创建处理器
handler = get_handler(url)

# 根据处理器配置启动浏览器
if handler.should_use_persistent_context():
    context = p.chromium.launch_persistent_context(...)
else:
    context = browser.new_context(...)

# 访问页面
page.goto(url)

# 使用处理器抓取
result = handler.fetch(page)

# 处理结果
if result.success:
    # 转换为 Markdown 并保存
    ...
```

## ➕ 如何添加新处理器

### 步骤 1：创建新的处理器类

创建 `handlers/github_handler.py`：

```python
from base_handler import BaseURLHandler, register_handler, FetchResult
from typing import Any, Dict, List

@register_handler
class GitHubHandler(BaseURLHandler):
    """GitHub 处理器"""
    
    SITE_TYPE = "github"
    SITE_NAME = "GitHub"
    DOMAIN = "github.com"
    
    config = {
        "needs_js": False,  # GitHub 静态内容多
        "wait_time": 2,
        "scroll_count": 0,
        "anti_detection": False,
        "use_persistent_context": False,
        "content_selectors": [
            ".markdown-body",  # GitHub README 容器
            "article",
            "body"
        ],
        "title_selectors": [
            "meta[property='og:title']",
            "h1",
            "title"
        ],
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
    }
    
    def fetch(self, page: Any) -> FetchResult:
        """抓取 GitHub 内容"""
        try:
            # 实现抓取逻辑
            title = self.extract_title(page)
            html, text = self.extract_content(page)
            images = self._extract_images(page)
            
            self.result.success = True
            self.result.title = title
            self.result.html = html
            self.result.content = text
            self.result.images = images
            
            return self.result
        except Exception as e:
            self.result.error = str(e)
            return self.result
    
    def _extract_images(self, page: Any) -> List[Dict]:
        """提取图片（GitHub 特殊处理）"""
        images = []
        # 实现图片提取逻辑
        return images
```

### 步骤 2：在 `__init__.py` 中导入

```python
# handlers/__init__.py

from .github_handler import GitHubHandler  # 添加这行

__all__ = [
    ...,
    'GitHubHandler',  # 添加这行
]
```

### 步骤 3：测试

```python
from handlers import get_handler, list_handlers

# 查看已注册的处理器
print(list_handlers())

# 测试新处理器
handler = get_handler("https://github.com/xxx/xxx")
print(handler)  # 应该输出：GitHub Handler (github)
```

## 📋 配置说明

### 处理器配置项

| 配置项 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `needs_js` | bool | 是否需要 JS 渲染 | `True` |
| `wait_time` | int | 基础等待时间（秒） | `3` |
| `scroll_count` | int | 滚动次数 | `5` |
| `scroll_delay` | float | 滚动间隔（秒） | `1.5` |
| `anti_detection` | bool | 是否启用反检测 | `True` |
| `use_persistent_context` | bool | 是否使用持久化上下文 | `True` |
| `content_selectors` | list | 内容选择器列表 | `["body", ".content"]` |
| `title_selectors` | list | 标题选择器列表 | `["title", "h1"]` |
| `headers` | dict | 自定义请求头 | `{"User-Agent": "..."}` |

### 配置优先级

1. **处理器配置** - 每个处理器有自己的默认配置
2. **URL 匹配** - 根据域名自动选择对应处理器
3. **后备方案** - 未匹配时使用 `GeneralHandler`

## 🔧 基类方法

### 必须实现的方法

```python
@abstractmethod
def fetch(self, page: Any) -> FetchResult:
    """抓取页面内容（核心方法）"""
    pass
```

### 可继承使用的方法

```python
def extract_title(self, page: Any) -> str:
    """提取页面标题"""

def extract_content(self, page: Any) -> Tuple[str, str]:
    """提取页面内容"""

def get_wait_timeout(self) -> int:
    """获取等待超时时间（毫秒）"""

def get_scroll_config(self) -> Dict:
    """获取滚动配置"""

def should_use_persistent_context(self) -> bool:
    """是否需要持久化上下文"""

def get_headers(self) -> Dict:
    """获取自定义请求头"""
```

## 📊 已注册处理器

| 处理器 | 域名 | 特殊功能 |
|--------|------|----------|
| GeneralHandler | * | 通用网页处理 |
| DoubaoHandler | doubao.com | 持久化上下文、多次滚动、消息容器选择器 |
| WeChatHandler | mp.weixin.qq.com | 代码块优化、图片防盗链 |
| ZhihuHandler | zhihu.com | 富文本处理、懒加载 |
| JuejinHandler | juejin.cn | 代码高亮、Markdown 渲染 |

## 🎯 最佳实践

1. **单一职责** - 每个处理器只处理一种网站类型
2. **配置集中** - 所有配置在类的 `config` 字典中
3. **方法复用** - 通用方法在基类实现，特殊方法在子类覆盖
4. **错误处理** - 所有异常在 `fetch` 方法中捕获并返回错误信息
5. **日志记录** - 关键步骤添加日志便于调试

---

更新时间：2026-03-26
