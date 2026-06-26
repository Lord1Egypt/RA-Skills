# UI自动化测试模块使用指南

## 📖 概述

UI自动化测试模块基于 **Playwright** 框架，提供现代化的浏览器自动化测试解决方案：
- 支持多浏览器（Chromium、Webkit、Firefox）
- Headless模式和有界面模式切换
- 自动截图和Trace回放
- 异步批量执行
- 元素智能定位
- 多视口测试

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install playwright pytest-asyncio
playwright install
```

### 2. 创建UI测试脚本

**基础登录测试示例：**

```python
import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio
class TestLogin:
    """登录页面UI测试"""

    async def test_login_success(self):
        """测试登录成功"""
        async with async_playwright() as p:
            # 启动浏览器（配置会自动注入）
            browser = await p.chromium.launch(headless=TEST_CONFIG["headless"])
            context = await browser.new_context(
                viewport=TEST_CONFIG["viewport"]
            )
            page = await context.new_page()

            # 导航到登录页面
            await page.goto("http://localhost:3000/login")

            # 填写表单
            await page.fill('#username', 'admin')
            await page.fill('#password', 'password123')

            # 点击登录按钮
            await page.click('#login-btn')

            # 验证跳转到首页
            await expect(page).to_have_url("http://localhost:3000/dashboard")

            # 截图
            await page.screenshot(path=f"{SCREENSHOT_DIR}/login_success.png")

            # 清理
            await context.close()
            await browser.close()

    async def test_login_invalid_password(self):
        """测试密码错误"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto("http://localhost:3000/login")
            await page.fill('#username', 'admin')
            await page.fill('#password', 'wrong_password')
            await page.click('#login-btn')

            # 验证错误提示
            error_msg = await page.locator('.error-message').text_content()
            assert "密码错误" in error_msg

            # 截图
            await page.screenshot(path=f"{SCREENSHOT_DIR}/login_fail.png")

            await browser.close()
```

**通过API创建脚本：**

```bash
POST http://localhost:8000/api/ui/script
Authorization: Bearer your_auth_code

{
  "name": "登录页面UI测试",
  "content": "import pytest\nfrom playwright.async_api import async_playwright\n...",
  "type": "ui"
}
```

### 3. 配置浏览器

```bash
POST http://localhost:8000/api/ui/browser/config
Authorization: Bearer your_auth_code

{
  "script_id": 1,
  "browser_type": "chromium",
  "headless": true,
  "viewport": {
    "width": 1920,
    "height": 1080
  },
  "slow_mo": 100
}
```

**参数说明：**
- `browser_type`: 浏览器类型（chromium/webkit/firefox）
- `headless`: 是否无头模式（true=无界面）
- `viewport`: 视口大小（模拟不同屏幕尺寸）
- `slow_mo`: 操作延迟（毫秒，用于演示或调试）

### 4. 执行测试

**执行单个脚本：**

```bash
POST http://localhost:8000/api/ui/execute
Authorization: Bearer your_auth_code

{
  "script_id": 1,
  "browser_config": {
    "browser_type": "chromium",
    "headless": true
  },
  "timeout": 600
}
```

**批量执行：**

```bash
POST http://localhost:8000/api/ui/execute/batch
Authorization: Bearer your_auth_code

{
  "script_ids": [1, 2, 3],
  "browser_config": {
    "browser_type": "chromium",
    "headless": true
  },
  "timeout": 1200
}
```

### 5. 查询执行进度

```bash
GET http://localhost:8000/execute/progress/{task_id}
```

### 6. 获取截图和Trace

**获取截图：**

```bash
GET http://localhost:8000/api/ui/screenshot/1/login_success.png
Authorization: Bearer your_auth_code
```

**获取Trace文件（用于回放）：**

```bash
GET http://localhost:8000/api/ui/trace/1
Authorization: Bearer your_auth_code
```

## 📝 完整示例

### 示例1：用户管理页面测试

```python
import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio
class TestUserManagement:
    """用户管理页面测试"""

    @pytest.fixture(autouse=True)
    async def setup(self):
        """每个测试前的初始化"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=TEST_CONFIG["headless"]
        )
        self.context = await self.browser.new_context(
            viewport=TEST_CONFIG["viewport"]
        )
        self.page = await self.context.new_page()

        # 登录
        await self.page.goto("http://localhost:3000/login")
        await self.page.fill('#username', 'admin')
        await self.page.fill('#password', 'admin123')
        await self.page.click('#login-btn')
        await self.page.wait_for_url("**/dashboard")

    async def teardown_method(self):
        """清理资源"""
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

    async def test_create_user(self):
        """测试创建用户"""
        # 导航到用户管理页面
        await self.page.click('text=用户管理')
        await self.page.click('text=新建用户')

        # 填写表单
        await self.page.fill('#username', 'newuser')
        await self.page.fill('#email', 'newuser@example.com')
        await self.page.select_option('#role', 'user')
        await self.page.click('button:has-text("保存")')

        # 验证创建成功
        await expect(self.page.locator('.success-message')).to_be_visible()

        # 截图
        await self.page.screenshot(path=f"{SCREENSHOT_DIR}/create_user_success.png")

    async def test_delete_user(self):
        """测试删除用户"""
        await self.page.click('text=用户管理')

        # 找到要删除的用户行
        row = self.page.locator('tr:has-text("testuser")')
        await row.locator('button:has-text("删除")').click()

        # 确认删除
        await self.page.click('button:has-text("确认")')

        # 验证删除成功
        await expect(self.page.locator('.success-message')).to_contain_text("删除成功")

        # 截图
        await self.page.screenshot(path=f"{SCREENSHOT_DIR}/delete_user_success.png")

    async def test_search_user(self):
        """测试搜索用户"""
        await self.page.click('text=用户管理')

        # 输入搜索关键词
        await self.page.fill('#search-input', 'admin')
        await self.page.press('#search-input', 'Enter')

        # 等待搜索结果
        await self.page.wait_for_selector('.user-table')

        # 验证搜索结果
        rows = await self.page.locator('tbody tr').count()
        assert rows > 0

        # 截图
        await self.page.screenshot(path=f"{SCREENSHOT_DIR}/search_user.png")
```

### 示例2：多浏览器测试

```python
import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
@pytest.mark.parametrize("browser_type", ["chromium", "webkit", "firefox"])
async def test_cross_browser(browser_type):
    """跨浏览器测试"""
    async with async_playwright() as p:
        # 根据参数选择浏览器
        browser = await getattr(p, browser_type).launch(headless=True)
        page = await browser.new_page()

        # 执行测试
        await page.goto("http://localhost:3000")
        title = await page.title()
        assert "首页" in title

        # 截图（文件名包含浏览器类型）
        await page.screenshot(path=f"{SCREENSHOT_DIR}/homepage_{browser_type}.png")

        await browser.close()
```

### 示例3：响应式设计测试

```python
import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
@pytest.mark.parametrize("viewport", [
    {"width": 1920, "height": 1080},  # 桌面
    {"width": 1366, "height": 768},   # 笔记本
    {"width": 768, "height": 1024},   # 平板
    {"width": 375, "height": 667}     # 手机
])
async def test_responsive_design(viewport):
    """测试响应式设计"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport=viewport)
        page = await context.new_page()

        await page.goto("http://localhost:3000")

        # 检查导航菜单
        if viewport["width"] < 768:
            # 移动端：检查汉堡菜单
            hamburger = page.locator('.hamburger-menu')
            await expect(hamburger).to_be_visible()
        else:
            # 桌面端：检查完整导航
            nav = page.locator('.nav-menu')
            await expect(nav).to_be_visible()

        # 截图
        await page.screenshot(
            path=f"{SCREENSHOT_DIR}/responsive_{viewport['width']}x{viewport['height']}.png"
        )

        await context.close()
        await browser.close()
```

## 🔧 API 接口列表

### 脚本管理

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/ui/script` | POST | 创建UI测试脚本 |
| `/api/ui/script/list` | GET | 获取脚本列表 |
| `/api/ui/script/{id}` | GET | 获取脚本详情 |
| `/api/ui/script/{id}` | PUT | 更新脚本 |
| `/api/ui/script/{id}` | DELETE | 删除脚本 |

### 浏览器配置

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/ui/browser/config` | POST | 配置浏览器参数 |
| `/api/ui/browser/config/{script_id}` | GET | 获取浏览器配置 |

### 测试执行

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/ui/execute` | POST | 执行单个UI脚本 |
| `/api/ui/execute/batch` | POST | 批量执行UI脚本 |
| `/execute/progress/{task_id}` | GET | 查询执行进度 |
| `/api/ui/screenshot/{script_id}/{name}` | GET | 获取截图文件 |
| `/api/ui/trace/{script_id}` | GET | 获取Trace文件 |

## 💡 最佳实践

### 1. 元素定位策略

**优先级从高到低：**

```python
# 1. 使用语义化选择器
await page.get_by_role('button', name='登录')
await page.get_by_label('用户名')

# 2. 使用文本选择器
await page.locator('text=登录')

# 3. 使用CSS选择器
await page.locator('#login-btn')
await page.locator('.submit-button')

# 4. 使用XPath（最后选择）
await page.locator('xpath=//button[@type="submit"]')
```

### 2. 等待策略

```python
# 等待元素出现
await page.wait_for_selector('.element')

# 等待元素消失
await page.wait_for_selector('.loading', state='hidden')

# 等待导航完成
await page.wait_for_load_state('networkidle')

# 使用expect断言自动等待
await expect(page.locator('.message')).to_be_visible()
```

### 3. 截图策略

```python
# 每个重要步骤都截图
await page.screenshot(path=f"{SCREENSHOT_DIR}/step1_initial.png")
await page.click('#btn')
await page.screenshot(path=f"{SCREENSHOT_DIR}/step2_after_click.png")

# 失败时自动截图（在teardown中）
try:
    await expect(page.locator('.result')).to_be_visible()
except:
    await page.screenshot(path=f"{SCREENSHOT_DIR}/failure.png")
    raise
```

### 4. Trace录制

```python
# 开始录制
context = await browser.new_context()
await context.tracing.start(screenshots=True, snapshots=True)

# ... 执行测试 ...

# 停止并保存
await context.tracing.stop(path=f"{TRACE_DIR}/trace.zip")
```

## ⚠️ 注意事项

1. **执行环境**
   - 确保Playwright已安装：`playwright install`
   - 浏览器驱动已下载
   - 目标网站可访问

2. **超时设置**
   - UI测试较慢，建议600秒以上
   - 批量执行时间=脚本数量×单脚本时间

3. **资源消耗**
   - 浏览器实例消耗内存较大
   - 避免同时执行过多脚本
   - 及时关闭浏览器和context

4. **截图管理**
   - 定期清理旧截图
   - 截图文件可能较大
   - 考虑压缩或存储策略

## 🐛 故障排查

### Playwright未安装

```bash
# 安装Playwright
pip install playwright

# 安装浏览器
playwright install chromium
playwright install webkit
playwright install firefox
```

### 元素定位失败

**原因：**
1. 页面未完全加载
2. 元素选择器错误
3. 元素被遮挡或不可见

**解决方法：**
```python
# 增加等待
await page.wait_for_selector('#element', timeout=10000)

# 使用更精确的选择器
await page.locator('button:has-text("登录")')

# 强制等待
await page.wait_for_timeout(1000)
```

### 截图为空白

**原因：**
1. headless模式下渲染问题
2. 页面未完全加载

**解决方法：**
```python
# 等待网络空闲
await page.wait_for_load_state('networkidle')

# 或等待特定元素
await page.wait_for_selector('.loaded')
```

## 📊 Trace回放

**查看Trace：**

```bash
# 下载Trace文件后，使用Playwright查看
playwright show-trace trace.zip
```

这将打开一个交互式界面，可以：
- 查看每一步操作
- 检查页面快照
- 查看网络请求
- 分析性能指标

---

**版本：** v1.0.0
**更新时间：** 2026-03-23
