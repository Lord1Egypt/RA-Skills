# Amber Url to Markdown V3.0 - 重构更新日志

## 📅 更新时间

**2026-03-24** - V3.0 正式发布

---

## 🎯 重构目标

根据代码评估报告，从"能用"到"好用"，重点强化：
- **健壮性** - 全量异常处理
- **兼容性** - 动态页面支持
- **合规性** - robots.txt 协议
- **可维护性** - 模块化设计
- **可测试性** - 单元测试覆盖

---

## ✨ 新特性

### 1. 模块化代码结构

**重构前：**
```
amber_url_to_markdown.py (单文件，600+ 行)
```

**重构后：**
```
scripts/
├── amber_url_to_markdown.py    # 主入口（协调各模块）
├── fetcher.py                  # URL 请求模块（~200 行）
├── parser.py                   # HTML 解析模块（~200 行）
├── utils.py                    # 工具函数模块（~250 行）
└── url_handler.py              # URL 类型识别（保持不变）
```

**优势：**
- 单一职责原则
- 易于测试和维护
- 代码复用性高

---

### 2. 强化错误处理

#### fetcher.py - 全量异常捕获

```python
def fetch_url_content(url, timeout=30, headers=None):
    """抓取 URL 的 HTML 内容，包含异常处理与浏览器 UA 模拟"""
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
        
    except Timeout:
        print(f"[ERROR] ❌ 请求{url}超时（{timeout}秒）")
        return None
        
    except HTTPError as e:
        print(f"[ERROR] ❌ {url}返回 HTTP 错误：{e.response.status_code}")
        return None
        
    except ConnectionError as e:
        print(f"[ERROR] ❌ 连接{url}失败：{str(e)[:80]}")
        return None
        
    except RequestException as e:
        print(f"[ERROR] ❌ 请求{url}失败：{str(e)[:80]}")
        return None
```

**覆盖场景：**
- ✅ 网络超时
- ✅ HTTP 错误（4xx/5xx）
- ✅ 连接失败
- ✅ 未知异常

---

### 3. 合规性检查

#### robots.txt 协议遵循

```python
def is_allowed_by_robots(url, user_agent="amber-url-to-markdown"):
    """判断是否允许爬取目标 URL（遵循 robots.txt 协议）"""
    
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    
    parser = RobotFileParser()
    parser.set_url(robots_url)
    parser.read()
    
    return parser.can_fetch(user_agent, url)
```

**功能：**
- ✅ 自动检查目标网站 robots.txt
- ✅ 禁止爬取时跳过并提示
- ✅ 无法获取时默认允许（可配置）

---

### 4. 批量请求限流

```python
def batch_fetch_urls(urls, timeout=30, check_robots=True, random_delay=True):
    """批量抓取 URL 内容，含限流与合规检查"""
    
    for i, url in enumerate(urls, 1):
        # robots.txt 检查
        if check_robots and not is_allowed_by_robots(url):
            continue
        
        # 抓取内容
        content = fetch_url_content(url, timeout)
        
        # 随机延迟（降低反爬风险）
        if random_delay and i < len(urls):
            delay = random.uniform(1, 3)
            time.sleep(delay)
```

**特性：**
- ✅ 批量抓取支持
- ✅ 随机延迟 1-3 秒
- ✅ 降低封 IP 风险

---

### 5. 优化 Markdown 转换

#### parser.py - 自定义转换规则

```python
def html_to_markdown(html, heading_style="ATX", bullets="-"):
    """自定义 HTML 转 Markdown 规则，提升格式准确性"""
    
    # 优化 HTML
    html = optimize_html_for_markdown(html)
    html = optimize_for_tables(html)
    html = clean_html(html)
    
    # 转换为 Markdown
    markdown_text = md(
        html,
        heading_style=heading_style,      # 标题用 #
        bullets=bullets,                  # 无序列表用 -
        convert_ol=True,                  # 保留有序列表
        image_alt_text=True,              # 保留图片 alt 文本
        linkify=True,                     # 自动识别纯文本链接
        strip=['script', 'style'],        # 剔除脚本/样式
        escape_underscores=False,         # 禁用下划线转义
        escape_misc=False,                # 禁用其他字符转义
        code_language='text',             # 代码块默认语言
    )
    
    # 后处理
    markdown_text = re.sub(r'```\s*\n\s*```', '', markdown_text)
    markdown_text = re.sub(r'\n{4,}', '\n\n', markdown_text)
    
    return markdown_text
```

**优化点：**
- ✅ 表格格式优化
- ✅ 代码块正确处理
- ✅ 图片路径下划线不转义
- ✅ 移除多余空行

---

### 6. 时间戳一致性保证

**问题：** 之前在不同位置生成时间戳，导致图片目录名和 MD 文件引用不一致。

**解决：** 在函数开始时就生成时间戳，后续所有地方都使用同一个。

```python
def fetch_with_playwright(url, output_dir, download_images=True):
    """Playwright 方案"""
    
    # 【重要】在开始处理时就生成时间戳，后续所有地方都使用同一个时间戳
    timestamp = format_timestamp()
    log(f"时间戳：{timestamp}", "INFO")
    
    images_dir = os.path.join(output_dir, "images", f"knowledge_{timestamp}")
    
    # 后续所有图片引用都使用这个 timestamp
    relative_path = f"images/knowledge_{timestamp}/{filename}"
```

**效果：**
- ✅ 图片目录名 = MD 文件引用路径
- ✅ 图片可以正常显示
- ✅ 避免 404 错误

---

### 7. 单元测试覆盖

#### tests/test_amber_url_to_markdown.py

**测试覆盖：**

| 模块 | 测试项 | 状态 |
|------|--------|------|
| fetcher | 正常 URL 请求 | ✅ |
| fetcher | 404 页面请求 | ✅ |
| fetcher | 超时场景 | ✅ |
| fetcher | 无效 URL | ✅ |
| fetcher | robots.txt 检查 | ✅ |
| fetcher | 批量抓取 | ✅ |
| parser | HTML 转 Markdown | ✅ |
| parser | 空 HTML 处理 | ✅ |
| parser | 标题提取 | ✅ |
| parser | 代码块优化 | ✅ |
| utils | 标题清理 | ✅ |
| utils | 特殊字符处理 | ✅ |
| utils | 长度限制 | ✅ |
| utils | 时间戳格式 | ✅ |
| utils | 目录创建 | ✅ |
| url_handler | 微信 URL 识别 | ✅ |
| url_handler | 知乎 URL 识别 | ✅ |
| url_handler | 掘金 URL 识别 | ✅ |

**运行测试：**
```bash
./run_tests.sh
# 或
pytest tests/ -v
```

---

### 8. 代码规范与配置

#### pyproject.toml

```toml
[tool.black]
line-length = 120
target-version = ["py38", "py39", "py310", "py311", "py312"]

[tool.flake8]
max-line-length = 120
exclude = ["__pycache__", "venv"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

**工具链：**
- ✅ black - 代码格式化
- ✅ flake8 - 语法检查
- ✅ pytest - 单元测试

---

## 📊 对比总结

| 维度 | V2.x | V3.0 | 改进 |
|------|------|------|------|
| **代码结构** | 单文件 | 模块化 | ⭐⭐⭐⭐⭐ |
| **错误处理** | 基础 | 全量异常捕获 | ⭐⭐⭐⭐⭐ |
| **合规性** | 无 | robots.txt 检查 | ⭐⭐⭐⭐⭐ |
| **限流机制** | 无 | 随机延迟 | ⭐⭐⭐⭐ |
| **测试覆盖** | 无 | 完整单元测试 | ⭐⭐⭐⭐⭐ |
| **代码规范** | 无 | black + flake8 | ⭐⭐⭐⭐ |
| **时间戳** | 多处生成 | 统一生成 | ⭐⭐⭐⭐⭐ |
| **可维护性** | 低 | 高 | ⭐⭐⭐⭐⭐ |

---

## 🚀 升级指南

### 安装依赖

```bash
# 安装核心依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 运行测试

```bash
# 验证安装
./run_tests.sh
```

### 使用方式

**无变化** - 保持向后兼容：

```bash
# 命令行
python3 scripts/amber_url_to_markdown.py <URL>

# Python 调用
from amber_url_to_markdown import fetch_url_to_markdown
result = fetch_url_to_markdown("https://...")
```

---

## 📝 后续计划

### 短期（V3.1）

- [ ] 增加更多网站类型支持
- [ ] 优化动态页面抓取（Selenium 备选）
- [ ] 增加缓存机制

### 中期（V3.2）

- [ ] GUI 界面（Tkinter/PyQt）
- [ ] 批量处理 Web 界面
- [ ] 导出格式扩展（PDF、EPUB）

### 长期（V4.0）

- [ ] 分布式抓取支持
- [ ] AI 内容摘要生成
- [ ] 多语言支持

---

## 🙏 致谢

感谢代码评估报告提供的专业建议，使这次重构更加系统和专业！

**核心优化思路：** 从"能用"到"好用"，重点强化**健壮性、兼容性、合规性**，同时提升代码可维护性。

---

**版本**: V3.0  
**创建时间**: 2026-03-24  
**作者**: 小文
