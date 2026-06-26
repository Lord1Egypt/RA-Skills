# 豆包链接爬取成功方案

## 🎉 最终解决方案

经过多轮测试，已成功实现豆包链接的自动化爬取！

### 核心技术方案

**1. 持久化浏览器上下文** - 保存浏览器状态
```python
context = p.chromium.launch_persistent_context(
    user_data_dir="./doubao_user_data",
    headless=True,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    # ... 其他配置
)
```

**2. 完整浏览器 Headers** - 伪装真实用户
```python
extra_http_headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.doubao.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
}
```

**3. 智能等待 + 滚动加载** - 确保动态内容完全加载
- 等待 `networkidle` 状态（15 秒超时）
- 多次滚动页面（每次 600px，共 5 次）
- 每次滚动后等待 1.5 秒
- 验证内容长度（目标：>1000 字符）

**4. 精准内容选择器** - 提取豆包消息容器
```python
# 使用 [class*='message'] 选择器定位内容
message_el = page.query_selector("[class*='message']")
content_html = message_el.inner_html()
```

## 📊 测试结果

**测试链接：** https://www.doubao.com/thread/a6181c4811850

**抓取结果：**
- ✅ 内容长度：4,590 字符
- ✅ HTML 长度：30,282 字符
- ✅ 格式：完整 Markdown
- ✅ 耗时：~42 秒

**输出文件：** `/root/openclaw/urltomarkdown/Personify_Memory_项目评估与优化_-_豆包.md`

## 🚀 使用方法

直接发送豆包链接，Hook 会自动抓取：

```
https://www.doubao.com/thread/a6181c4811850
```

系统会自动：
1. 检测豆包链接
2. 启动持久化浏览器
3. 等待内容加载
4. 滚动页面触发动态加载
5. 提取消息容器内容
6. 转换为 Markdown
7. 保存到 `/root/openclaw/urltomarkdown/` 目录

## 📁 输出目录

- **文件位置：** `/root/openclaw/urltomarkdown/`
- **图片目录：** `/root/openclaw/urltomarkdown/images/knowledge_时间戳/`
- **用户数据：** `/root/openclaw/skills/amber-url-to-markdown/doubao_user_data/`

## ⚠️ 注意事项

1. **首次运行** - 可能需要更长时间建立浏览器配置
2. **Cookie 有效期** - 豆包 Cookie 会过期，如抓取失败需重新访问链接
3. **频率控制** - 避免短时间内多次抓取同一链接
4. **内容长度** - 豆包内容有字数限制，长对话可能被截断

## 🔧 故障排查

**问题 1：内容长度为 0 或很少**
- 原因：页面未完全加载
- 解决：检查日志中的"内容长度"，应 >1000 字符

**问题 2：提示找不到消息容器**
- 原因：豆包页面结构可能变化
- 解决：检查 `[class*='message']` 选择器是否仍然有效

**问题 3：浏览器启动失败**
- 原因：服务器资源不足
- 解决：检查系统内存，关闭其他占用资源的进程

## 📝 技术细节

### 为什么这个方案有效？

1. **持久化上下文** - 保存了浏览器指纹和状态，降低被检测风险
2. **完整 Headers** - 模拟真实浏览器的所有请求特征
3. **智能等待** - 确保 SPA 应用的动态内容完全渲染
4. **滚动加载** - 触发豆包的懒加载机制
5. **精准选择器** - 直接定位包含内容的消息容器

### 与其他方案对比

| 方案 | 状态 | 说明 |
|------|------|------|
| 静态 HTTP 请求 | ❌ 失败 | 只能获取空 HTML |
| Scrapling | ❌ 失败 | 无 JS 执行能力 |
| Playwright（无优化） | ❌ 失败 | 内容未加载完成 |
| **Playwright（持久化 + 滚动）** | ✅ 成功 | 本方案 |
| API 接口 | ❌ 失败 | 需要认证（401） |

## 📚 参考资料

- 原始方案文档：`/root/openclaw/豆包聊天记录 url 爬取优化及自动化内容整理方案.md`
- 脚本路径：`/root/openclaw/skills/amber-url-to-markdown/scripts/amber_url_to_markdown.py`
- URL 处理器：`/root/openclaw/skills/amber-url-to-markdown/scripts/url_handler.py`

---

更新时间：2026-03-26
状态：✅ 生产就绪
