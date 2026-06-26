# 豆包链接爬取配置指南

## 问题现状

豆包（doubao.com）的内容需要登录才能查看完整内容。当前脚本已支持持久化浏览器上下文，但首次运行需要手动登录。

## 解决方案

### 方案 1：手动登录保存 Cookie（推荐，一劳永逸）

**第一次运行（需要手动登录）：**

1. 修改脚本第 93 行，将 `headless=True` 改为 `headless=False`
   ```python
   context = p.chromium.launch_persistent_context(
       user_data_dir=user_data_dir,
       headless=False,  # 第一次改为 False，显示浏览器
       # ... 其他配置
   )
   ```

2. 运行脚本抓取任意豆包链接
   ```bash
   python3 /root/openclaw/skills/amber-url-to-markdown/scripts/amber_url_to_markdown.py "https://www.doubao.com/thread/a6181c4811850"
   ```

3. 浏览器窗口会打开，手动登录豆包账号

4. 登录成功后，关闭浏览器（脚本会继续执行完成）

5. 修改回 `headless=True`，后续运行都会自动使用保存的 Cookie

**后续运行：** 全自动，无需手动干预

---

### 方案 2：直接注入 Cookie（无需显示浏览器）

**步骤：**

1. 浏览器打开 https://www.doubao.com 并登录

2. 按 F12 打开开发者工具 → 切换到「网络」面板

3. 刷新页面 → 找到第一个 doubao.com 的主请求

4. 复制「请求标头」中的完整 `Cookie` 值

5. 在脚本中添加 Cookie 到 headers：
   ```python
   extra_http_headers={
       "Cookie": "你复制的完整 Cookie 内容",  # 添加这行
       "Accept": "text/html,application/xhtml+xml...",
       # ... 其他 headers
   }
   ```

**注意：** Cookie 有有效期，失效后需要重新复制

---

### 方案 3：使用 API 接口（最稳定）

豆包的内容通过 API 返回，直接调用 API 更稳定：

1. 浏览器 F12 → 网络面板 → 筛选「Fetch/XHR」

2. 刷新豆包页面 → 找到名称带 `thread`/`detail` 的接口

3. 复制 API 地址，例如：
   ```
   https://www.doubao.com/api/thread/a6181c4811850
   ```

4. 用 API 地址替换原链接进行抓取

---

## 当前脚本配置

脚本已配置以下优化：

- ✅ 持久化浏览器上下文（保存登录状态）
- ✅ 完整的浏览器 Headers
- ✅ 自动滚动加载内容
- ✅ 反检测配置

**用户数据目录：** `/root/openclaw/skills/amber-url-to-markdown/doubao_user_data/`

Cookie 会保存在这个目录，首次登录后后续自动使用。

---

## 测试链接

可用测试链接：
- https://www.doubao.com/thread/a6181c4811850

---

## 注意事项

1. **合规使用**：仅限个人学习，禁止商用或二次分发
2. **账号安全**：不要泄露 Cookie
3. **频率控制**：避免短时间多次请求
4. **Cookie 有效期**：失效后重新登录即可

---

## 故障排查

**问题 1：内容仍为空（31 字符）**
- 原因：未登录或 Cookie 失效
- 解决：按方案 1 手动登录

**问题 2：浏览器无法启动**
- 原因：服务器环境不支持有头模式
- 解决：使用方案 2 直接注入 Cookie

**问题 3：提示需要验证码**
- 原因：请求频率过高
- 解决：等待 10-30 分钟后再试

---

更新时间：2026-03-26
