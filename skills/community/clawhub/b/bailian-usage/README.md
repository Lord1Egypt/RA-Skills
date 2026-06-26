# 百炼套餐用量查询 Skill

## 安装

本 Skill 已内置于 workspace，无需额外安装。

## 使用方法

### 快捷命令

直接发送以下任一消息即可触发：

- `查百炼额度`
- `查 Token`
- `Token 用量`
- `看看阿里云还剩多少额度`
- `百炼用量情况`
- `查一下百炼套餐用量`

### 手动调用

告诉 AI："调用 bailian-usage Skill 查询百炼套餐"

## 输出示例

```markdown
## 📊 百炼 Coding Plan 套餐详情

**套餐状态：** ✅ 生效中 | 剩余 **18 天**（2026-04-03 到期）
**自动续费：** ❌ 未开启

**用量消耗：**
- 最后统计时间：2026-03-15 19:54:33
- 近 5 小时：**47%**（2026-03-15 19:54:34 **重置**）
- 近一周：**42%**（2026-03-16 00:00:00 **重置**）
- 近一月：**39%**（2026-04-03 00:00:00 **重置**）

**可用模型：** 千问系列 / 智谱 / Kimi / MiniMax

---

### 💡 用量分析
- ✅ 用量充足
```

## 登录方式

### 自动化登录（默认）

脚本会自动从 `TOOLS.md` 读取账号密码并登录：

```markdown
## 🔐 阿里云百炼账号
- **网址**: https://bailian.console.aliyun.com/cn-beijing/?tab=coding-plan#/efm/index
- **账号**: your-account@example.com
- **密码**: your-password-here
```

**流程**：
1. 打开百炼控制台
2. 检查登录状态
3. 如未登录，自动填写账号密码并登录
4. 提取数据并返回结果

### 人工验证（备选）

如果自动登录触发滑块/短信验证：
1. 脚本会提示需要人工完成验证
2. 在浏览器窗口中完成验证
3. 验证成功后继续执行查询

## 技术实现

- **浏览器**：使用 `openclaw browser` tool 控制
- **登录态**：复用 `openclaw` browser profile 的持久化 Cookie
- **登录检查**：智能检测登录状态，未登录时自动使用 TOOLS.md 账号密码
- **数据提取**：浏览器 snapshot 提取页面结构化数据
- **代码量**：~50 行（精简版）

## 注意事项

1. **登录态复用** - 优先使用 browser profile 的持久化 Cookie，无需每次重新登录
2. **自动 fallback** - 如检测到未登录，自动使用 TOOLS.md 账号密码登录
3. **高风控场景** - 若触发短信/滑块验证，需人工完成验证
4. **用量刷新时间** - 可能滞后，以页面显示为准
5. **浏览器管理** - 遵循省内存策略，查询完成后主动关闭页面

## 🔐 安全说明

- **凭证存储**：账号密码仅存储在用户本地 `TOOLS.md` 文件中，不提交到 Git/版本控制
- **凭证使用**：脚本读取凭证后仅在内存中使用，不在日志中输出或传输到外部
- **浏览器会话**：登录态保存在本地 `~/.openclaw/browser/openclaw/user-data` Profile 中，不上传到任何服务器
- **登录态复用**：优先使用已有 Cookie，减少登录频率，降低风控风险
- **网络请求**：所有请求直接发往 `bailian.console.aliyun.com`，无第三方中转
- **ClawHub 安全扫描**：v1.1.0+ 已通过 ClawHub 安全扫描（无 suspicious patterns 警告）

## 相关文件

- **脚本**: `~/.openclaw/workspace/skills/bailian-usage/query_browser.sh`
- **配置**: `~/.openclaw/workspace/TOOLS.md`（账号密码）
- **文档**: `~/.openclaw/workspace/skills/bailian-usage/SKILL.md`
