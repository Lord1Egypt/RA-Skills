# bailian-usage Skill | 百炼用量查询

**中文**：自动查询阿里云百炼 Coding Plan 套餐用量、剩余额度、有效期信息，支持自动登录和数据提取。
**English**: Auto-query Alibaba Cloud Bailian Coding Plan usage, quota, and expiration. Supports automated login and data extraction.

---

## 模型配置 | Model Configuration

**默认模型：** qwen3.5-plus（如需更换，可在调用时通过 `--model` 参数指定）

## 触发条件 | Trigger Words

用户提到以下关键词时激活 | Activate when user mentions:
- "查百炼套餐" / "Check Bailian package"
- "百炼用量" / "Bailian usage"
- "百炼额度" / "Bailian quota"
- "阿里云百炼" / "Alibaba Cloud Bailian"
- "Coding Plan"
- "看看套餐情况" / "Check package status"

## 执行流程

### 主链路：openclaw browser tool + evaluate 直接提取

1. **启动浏览器**（如未运行）
   ```bash
   openclaw browser start
   ```

2. **打开百炼控制台** → 导航到 `https://bailian.console.aliyun.com/cn-beijing/?tab=coding-plan#/efm/detail`

3. **检查登录态** → 通过 aria snapshot 检查是否有邮箱、"主账号"等登录标识

4. **必要时登录**：
   - 点击右上角"登录"按钮
   - 填写账号密码（从 `TOOLS.md` 读取）
   - 点击"立即登录"按钮
   - 等待登录完成并刷新页面

5. **提取数据** → 用 `evaluate` 执行 JS 直接读取 DOM 文本

6. **返回结果** → 格式化输出套餐信息

## 输出格式

```markdown
## 📊 百炼 Coding Plan 套餐详情

**套餐状态：** ✅ 生效中 | 剩余 **xx 天**（YYYY-MM-DD 到期）  
**自动续费：** ❌ 未开启 / ✅ 已开启

**用量消耗：**
- 最后统计时间：YYYY-MM-DD HH:mm:ss
- 近 5 小时：**xx%**（YYYY-MM-DD HH:mm:ss **重置**）
- 近一周：**xx%**（YYYY-MM-DD HH:mm:ss **重置**）
- 近一月：**xx%**（YYYY-MM-DD HH:mm:ss **重置**）

**可用模型：** 千问系列 / 智谱 / Kimi / MiniMax

---

### 💡 用量分析
- ✅ 用量充足 / ⚠️ 用量紧张 / ❌ 用量不足
- 到期提醒（如适用）
```

## 登录流程详解

### 自动化登录（默认）

**主链路**：点击登录按钮 → 填写账号密码 → 点击立即登录

**账号信息**自动从 `TOOLS.md` 读取，无需用户干预。

**账号信息**存储在 `TOOLS.md` 中（示例）：
```markdown
## 🔐 阿里云百炼账号
- **网址**: https://bailian.console.aliyun.com/cn-beijing/?tab=coding-plan#/efm/index
- **账号**: your-email@example.com
- **密码**: your-password
```

⚠️ **注意**: 请勿将真实账号密码提交到版本控制系统。此处的示例仅用于说明格式。

### 🔐 安全说明

- **凭证存储**：账号密码仅存储在用户本地 `TOOLS.md` 文件中，不提交到 Git/版本控制
- **凭证使用**：脚本读取凭证后仅在内存中使用，不在日志中输出或传输到外部
- **浏览器会话**：登录态保存在本地浏览器 Profile 中，不上传到任何服务器
- **网络请求**：所有请求直接发往 `bailian.console.aliyun.com`，无第三方中转

### 人工验证（备选）

如果自动登录触发滑块/短信验证：
1. 脚本会提示"可能需要人工完成验证"
2. 用户在浏览器窗口中完成验证
3. 验证成功后，继续执行查询

## 数据提取逻辑（优化版 v2 - 2026-03-17）

使用 `evaluate` 执行 JS 直接读取 `document.body.innerText`，通过**按行分割 + 精准定位**提取：

**核心改进**：
1. **近 5 小时用量提取**：放弃正则匹配，改用按行分割后查找
   - 原因：页面实际文本是"近 5 小时用量"（无空格），正则容易匹配失败
   - 方法：`text.split('\n')` 后遍历，找到包含"5"+"小时"+"用量"的行
   - 结构：第 i 行=标签，第 i+1 行=重置时间，第 i+2 行=用量百分比

2. **日志过滤**：在 bash 中过滤 `openclaw browser evaluate` 的日志输出
   - 用 `grep -v '^\['` 过滤插件日志
   - 用 `grep -v '^🦞'` 过滤浏览器状态
   - 确保 jq 能正确解析 JSON

3. **其他用量**：保持正则匹配（近一周/一月用量正则工作正常）

**提取规则**：
- 套餐状态：`text.includes('生效中')`
- 剩余天数：`/剩余天数 (\d+) 天/`
- 到期日期：`/结束时间 (\d{4}-\d{2}-\d{2})/`
- 最后统计时间：`/最后统计时间 (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})/`
- 近 5 小时用量：**按行分割查找**（核心优化）
- 近一周/一月用量：正则匹配 `/\w+ 用量 [\s\S]{0,150}?(\d+)%/`

## 注意事项

1. **每次直接登录** - 无 cookie 依赖，更简单可靠
2. **高风控场景** - 若触发短信/滑块验证，需人工完成验证
3. **用量刷新时间** - 可能滞后，以页面显示为准
4. **浏览器管理** - 遵循省内存策略，主动关闭非必要 tab

## 快捷命令

- "查百炼额度" → 调用本 Skill
- "看看阿里云还剩多少额度" → 调用本 Skill
- "百炼用量情况" → 调用本 Skill
- "百炼 Token" → 调用本 Skill
- "百炼套餐用量" → 调用本 Skill

## 边界说明

- 本 Skill **只负责阿里云百炼 / Coding Plan / 套餐 / 额度 / 百炼 Token** 相关查询。
- 像"查 Token 用量""Token 消耗""过去 24 小时 Token 用量"这类**未明确提到百炼**的说法，**不应**由本 Skill 处理，应转交 `token-usage-analysis`。

## 相关文件

- **Skill 目录**: `~/.openclaw/workspace/skills/bailian-usage/`
- **脚本**: `~/.openclaw/workspace/skills/bailian-usage/query_browser.sh`
- **账号信息**: `~/.openclaw/workspace/TOOLS.md`
