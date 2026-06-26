# 快速开始

## 适用场景

- 用 AI 调试前端页面的 JavaScript 报错
- 分析页面性能瓶颈
- 检查网络请求和 API 响应
- 执行浏览器自动化操作

---

## 基础工作流：调试前端 Bug

典型的 AI 调试会话流程：

1. **告诉 AI 访问页面**
   ```
   请打开 http://localhost:3000，截图并检查控制台是否有报错
   ```

2. **AI 返回截图 + 控制台消息**，通常包含带源码映射的完整错误堆栈

3. **深入检查**
   ```
   查看页面所有网络请求，找出失败的 API 调用
   ```

4. **执行交互**
   ```
   点击"Submit"按钮，然后截图表单提交后的状态
   ```

---

## 截图

```
请截图 https://www.example.com 的首屏效果
```

```
截图 http://localhost:3000/dashboard，确认侧边栏是否正确显示
```

AI 会返回图片供直接查看，无需手动操作浏览器。

---

## 控制台调试

```
打开 http://localhost:3000，读取控制台的所有错误和警告
```

chrome-devtools-mcp 会返回：
- 错误消息文本
- 源码映射后的真实文件名和行号（不是 bundle.js:1）
- 完整调用堆栈

---

## 网络请求检查

```
访问 http://localhost:3000/api-test，检查所有网络请求，
特别关注失败的请求（4xx/5xx）
```

AI 可以看到：
- 请求 URL 和方法
- 响应状态码
- 请求/响应头
- 响应体内容

---

## 性能分析

```
录制 https://example.com 的页面性能，找出主要性能瓶颈
```

AI 会：
1. 录制 DevTools Performance Trace
2. 提取关键指标（FCP、LCP、TBT 等）
3. 结合真实用户数据（CrUX）对比实验室数据
4. 给出可操作的优化建议

禁用 CrUX 真实用户数据（隐私敏感场景）：
```json
"args": ["-y", "chrome-devtools-mcp@latest", "--no-performance-crux"]
```

---

## 浏览器自动化

```
在 http://localhost:3000/login 填写用户名 "test@example.com"
和密码 "password123"，点击登录，截图登录结果
```

```
在搜索框输入 "Claude Code"，点击搜索按钮，截图结果页面
```

Puppeteer 底层确保每次操作都等待执行完成，比简单的 `setTimeout` 更可靠。

---

## 执行 JavaScript

```
在当前页面执行 document.title，返回页面标题
```

```
执行 window.localStorage.getItem('user_token')，查看当前存储的 token
```

---

## 完成确认检查清单

- [ ] 成功截图本地开发服务器页面
- [ ] 读取到控制台错误消息（含源码映射堆栈）
- [ ] 检查到网络请求列表
- [ ] 执行了至少一次自动化点击/填写操作

---

## 下一步

- [高级用法](03-advanced-usage.md) — 连接已有浏览器、Slim 模式、CI 无头模式
