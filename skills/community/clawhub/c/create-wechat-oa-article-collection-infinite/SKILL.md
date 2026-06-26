---
name: create-wechat-oa-article-collection-infinite
description: 在公众号后台创建文章合集。触发场景：创建公众号合集、新建文章合集、在公众号创建一个合集、创建合集。
version: 1.4.0.0
---

# 创建公众号文章合集_无限

用于在公众号后台创建文章合集。

## 触发场景

用户说：
- "创建公众号合集"
- "创建公众号文章合集"
- "新建公众号合集"
- "新建公众号文章合集"
- "在公众号创建一个文章合集"
- "在公众号创建一个合集"
- "在公众号新建一个文章合集"
- "在公众号新建一个合集"

## 重要注意事项

⚠️ **本技能用于创建合集，不是发表文章！**

⚠️ **Token 动态获取！**
- 公众号后台每次登录 token 会变，**必须使用主页当前最新的 token**
- 合集管理页面 URL 格式：`https://mp.weixin.qq.com/cgi-bin/appmsgalbummgr?action=list&token=TOKEN&lang=zh_CN`
- **正确做法**：先访问 `https://mp.weixin.qq.com/`（注意是根路径，不是/cgi-bin/home），它会自动重定向到主页并携带最新 token，然后从 URL 中提取 token 值，再用该 token 访问合集页面

⚠️ **Tab 标签页管理：**
- 公众号后台点击"创建合集"后，会弹出下拉菜单
- 选择"文章合集"后，创建表单会打开在**新标签页**
- 每次点击创建按钮后，**必须调用 tabs 查看新标签页**，然后切换到新标签页操作

⚠️ **点击"创建合集"按钮的正确姿势：**
- 合集列表页面右侧有"创建合集"按钮（首次加载 ref 如 e175）
- 按钮点击后会弹出下拉菜单（包含文章合集、贴图合集、视频合集、音频合集选项）
- 下拉菜单**出现后必须立即操作**，稍等片刻菜单会自动收起
- 需要点击下拉菜单中的"文章合集"选项（注意：左侧筛选栏的"文章合集"是 tab 标签，不是创建按钮，两者不要混淆）
- **用 ref 直接点击菜单项**（如 `ref=e376`），这是最可靠的方式
- **不要使用 evaluate 执行 JS**（不支持 const/let/箭头函数等 ES6 语法）
- **不要硬编码 ref 值**（每次页面刷新 ref 会变化，必须通过快照获取当前 ref）

## 操作流程

### 第零步：确保 OpenClaw 浏览器已启动

在执行任何浏览器操作前，**必须先确保 OpenClaw 托管的 Chrome 已运行**。按以下步骤操作：

1. 先调用 `browser(action=start, target="host", profile="openclaw")` 启动浏览器
2. 若失败，检查 `browser(action=status, target="host")` 状态
3. **浏览器启动后，用 `browser(action=navigate, target="host", profile="openclaw", url=...)` 导航到目标 URL**

**关键区别：**
- `browser(action=start, target="host", profile="openclaw")` ≠ `profile="user"` 或 `profile="chrome-relay"`
- `browser(action=navigate, ...)` ≠ `browser(action=open, targetUrl=...)`（后者会被 SSRF 策略拦截）
- `target="host"` 用于控制宿主机浏览器

**核心原则：除登录、支付、删除等核心操作外，所有问题自己尝试解决，不指挥用户。**

### 第一步：获取最新 Token 并进入合集管理页面

1. 导航到 `https://mp.weixin.qq.com/`（注意是根路径，不是 /cgi-bin/home）
2. 页面会自动重定向到主页 URL，其中包含最新 token
3. 从重定向后的 URL 中提取最新 token（如 `token=582165464`）
4. 访问合集管理页面：`https://mp.weixin.qq.com/cgi-bin/appmsgalbummgr?action=list&token=最新TOKEN&lang=zh_CN`

### 第二步：创建新合集

1. 在合集列表页面，找到右侧的**"创建合集"按钮**并点击，会弹出下拉菜单
2. 下拉菜单弹出后，**立即调用 snapshot 获取当前 refs**（菜单项的 ref 值如 e376，非固定）
3. 用 `click` + ref 直接点击"文章合集"选项（例：`ref=e376`，具体值从快照获取）
4. **立即调用 tabs** 查看新打开的标签页，获取创建表单的 targetId
5. ⚠️ 新标签页的 URL 会带旧 token，**必须替换为当前最新 token** 再导航

### 第三步：填写合集信息

1. 切换到创建表单标签页
2. 获取页面快照（snapshot），从快照中获取名称输入框 ref（如 e68）和简介输入框 ref（如 e77）
3. 用 `type` 命令输入合集名称到文本框
4. 简介为选填项，可省略

### 第四步：发布合集

1. 获取发布按钮的 ref（如 e106）
2. 点击"发布"按钮
3. 发布成功后，导航回合集列表页面验证：
   - 先访问主页获取新 token
   - 然后用新 token 访问合集列表

## 关键元素参考

| 元素 | 描述 | 操作方式 |
|------|------|---------|
| 主页URL | https://mp.weixin.qq.com/ | 用于获取最新token（根路径会自动重定向携带token） |
| 合集列表URL | /cgi-bin/appmsgalbummgr?action=list&token=xxx | 需要替换最新token |
| 创建合集按钮 | 合集列表右侧，ref=e175 | 点击弹出下拉菜单 |
| 文章合集选项 | 下拉菜单第一项，ref=e376（每次会话变化） | 点击后创建表单在新tab打开 |
| 名称输入框 | placeholder="填写名称"，ref=e68 | type 命令输入 |
| 简介输入框 | placeholder="填写简介"，ref=e77 | type 命令输入（选填） |
| 发布按钮 | 表单底部，ref=e106 | 点击发布合集 |

## 技术要点总结

1. **每次操作前获取最新 token** — 从主页 URL 中提取当前 token
2. **创建后立即 tabs** — 创建按钮点击后要检查新标签页
3. **创建表单在新标签页** — 必须切换到新 tab 才能填写表单
4. **输入用 type 命令** — 直接使用 type 命令即可，无需 JS
5. **发布后要刷新 token** — 发布成功后再访问合集列表要用新 token
6. **区分按钮和筛选标签** — "创建合集"是按钮，"文章合集"在左侧是筛选标签
7. **下拉菜单出现后立即快照获取 ref** — 菜单自动收起很快，操作要快
8. **ref 值每次会话都会变化** — 禁止硬编码，必须实时从快照获取

## 常见失败原因

- ❌ 硬编码旧 token 的 URL → 跳转到登录页
- ❌ 创建后没有 tabs → 在旧标签页操作，找不到表单元素
- ❌ 在旧标签页等待表单 → 表单已在新标签打开
- ❌ 发布后用旧 token 访问 → 页面提示登录超时
- ❌ 点击左侧筛选标签"文章合集" → 必须点击"创建合集"按钮弹出的**下拉菜单**里的"文章合集"选项，两者 class 相同但位置不同，要用 offsetParent 判断可见性
- ❌ 新标签页直接用旧 token → 新标签页 URL 里的 token 可能是旧的，必须替换为当前最新 token 再导航
- ❌ Chrome 未启动就直接调用 browser → 应先用 `browser(action=start, profile=user)` 启动，禁止用 exec/Start-Process
- ❌ 使用 evaluate 执行 JS → **evaluate 不支持 ES6 语法**（const/let/箭头函数），会报错 "Unexpected token"，点击菜单项改用 `click` + ref
- ❌ 硬编码 ref 值 → 每次页面刷新 ref 会变化，用快照获取当前 ref
- ❌ 下拉菜单出现后犹豫不决 → 菜单约 3-5 秒后自动收起，要立即快照+点击
