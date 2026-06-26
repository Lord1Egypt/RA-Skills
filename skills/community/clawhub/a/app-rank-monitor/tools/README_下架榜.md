# 下架榜实现状态说明

> **更新时间**: 2026-03-16 22:32  
> **状态**: ⚠️ 需要调整方案

---

## 📊 当前状态

### 已完成

1. ✅ **创建脚本** - `diandian_removed_apps.py`
2. ✅ **浏览器自动化** - 可以访问下架监控页面
3. ✅ **Cookie 设置** - 成功设置点点数据 Cookie
4. ✅ **页面加载** - 页面可以正常加载（HTML 725KB）

### 遇到的问题

**问题**: 下架监控页面的数据是**动态加载**的（JavaScript 渲染）

**表现**:
- ✅ 页面 HTML 已加载（725KB）
- ❌ 应用列表数据在 JavaScript 中，不在初始 HTML
- ❌ 需要等待 API 请求完成或执行 JavaScript

**尝试的方案**:
1. ❌ 直接提取 HTML - 数据不在 HTML 中
2. ❌ 等待选择器 - 动态加载，选择器不确定
3. ❌ 简单 evaluate - 需要正确的数据提取逻辑

---

## 💡 解决方案

### 方案 1: 拦截 API 请求（推荐）

**原理**: 
- 点点数据页面会调用 API 获取下架应用
- 拦截 API 响应，直接获取 JSON 数据

**实现**:
```python
# 监听 API 响应
async with page.expect_response("**/api/rank/*") as response_info:
    await page.click("下架监控按钮")
response = await response_info.value
data = await response.json()
```

**优点**:
- ✅ 直接获取 JSON 数据
- ✅ 数据准确完整
- ✅ 不需要解析 HTML

**缺点**:
- ⚠️ 需要知道正确的 API 端点
- ⚠️ 可能需要触发页面交互

---

### 方案 2: 执行 JavaScript 提取数据

**原理**:
- 点点数据使用 Nuxt.js/Vue.js
- 数据可能在 `window.__NUXT__` 或 Vue 实例中

**实现**:
```python
data = await page.evaluate("""
    () => {
        // 尝试从 Nuxt 状态获取
        if (window.__NUXT__) {
            return window.__NUXT__.data;
        }
        return null;
    }
""")
```

**优点**:
- ✅ 直接获取前端数据
- ✅ 不需要等待 API

**缺点**:
- ⚠️ 需要了解前端框架
- ⚠️ 数据结构可能复杂

---

### 方案 3: 使用点点数据 API（最简单）

**原理**:
- 直接调用点点数据 API
- 使用 Cookie 认证

**API**:
```
GET https://app.diandian.com/api/rank/offline
参数：platform=ios, limit=100
```

**问题**:
- ❌ 之前测试返回 302 重定向
- ❌ 可能需要额外的 headers 或参数

**解决**:
```python
headers = {
    'Cookie': token,
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://app.diandian.com/',
    'Accept': 'application/json',
}
# 使用 Session 保持 Cookie
session = httpx.Client(cookies=cookie_jar)
response = session.get(url, headers=headers)
```

---

## 🎯 建议

### 立即执行：方案 3（API 调用）

**原因**:
1. ✅ 最简单
2. ✅ 已有 Cookie
3. ✅ 只需要正确的 headers

**实现代码**:
```python
import httpx

# 创建 CookieJar
cookie_jar = httpx.Cookies()
for item in token.split(';'):
    if '=' in item:
        name, value = item.split('=', 1)
        cookie_jar.set(name.strip(), value.strip(), domain='.diandian.com')

# 使用 Session
with httpx.Client(cookies=cookie_jar) as client:
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://app.diandian.com/',
        'Accept': 'application/json',
    }
    response = client.get(
        'https://app.diandian.com/api/rank/offline',
        params={'platform': 'ios', 'limit': 100},
        headers=headers
    )
    data = response.json()
```

---

### 备选方案：方案 1（API 拦截）

如果方案 3 失败，使用 Playwright 拦截 API：

```python
async with async_playwright() as p:
    browser = await p.chromium.launch()
    page = await browser.new_page()
    
    # 监听 API 响应
    async with page.expect_response("**/api/rank/offline*") as response_info:
        await page.goto("https://app.diandian.com/rank/line-1-1-0-75-0-3-0")
    
    response = await response_info.value
    data = await response.json()
```

---

## 📝 下一步

1. [ ] 测试方案 3（API 调用 + Session）
2. [ ] 如果失败，实施方案 1（API 拦截）
3. [ ] 集成到主脚本
4. [ ] 配置定时任务

---

**预计完成时间**: 30 分钟  
**实现难度**: ⭐⭐（中等）
