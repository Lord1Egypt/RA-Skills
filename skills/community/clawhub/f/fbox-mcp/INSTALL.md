# 安装指南

## 在 Claude Code 中安装

1. **获取 API Key**

   联系 FBox 平台管理员获取 `clientId` 和 `clientSecret`，然后调用接口生成 API Key：

   macOS / Linux：
   ```bash
   curl -X POST https://fboxmcp.fbox360.com/api/apikey/generate \
     -H "Content-Type: application/json" \
     -d '{"clientId": "your-client-id", "clientSecret": "your-client-secret"}'
   ```

   Windows (PowerShell)：
   ```powershell
   Invoke-RestMethod -Uri https://fboxmcp.fbox360.com/api/apikey/generate `
     -Method Post -ContentType "application/json" `
     -Body '{"clientId": "your-client-id", "clientSecret": "your-client-secret"}' | ConvertTo-Json
   ```

   成功返回：

   ```json
   {
     "apiKey": "sk-xxxxxx...",
     "usage": "Authorization: Bearer sk-xxxxxx..."
   }
   ```

   > API Key 以 `sk-` 开头，长期有效。服务端自动管理底层 Token 的刷新和缓存，无需手动续期。

2. **设置环境变量**
   ```bash
   # macOS / Linux
   export FBOXMCP_API_KEY=sk-xxxxxx

   # Windows (PowerShell)
   $env:FBOXMCP_API_KEY="sk-xxxxxx"
   ```

3. **添加 MCP Server**

   macOS / Linux：
   ```bash
   claude mcp add --transport http fboxmcp https://fboxmcp.fbox360.com --header "Authorization: Bearer ${FBOXMCP_API_KEY}"
   ```

   Windows (PowerShell)：
   ```powershell
   claude mcp add --transport http fboxmcp https://fboxmcp.fbox360.com --header "Authorization: Bearer $env:FBOXMCP_API_KEY"
   ```

4. **安装插件**
   ```bash
   claude plugin marketplace add https://github.com/flexem/fbox-skills
   claude plugin install fboxmcp
   ```

5. **验证安装**
   ```bash
   claude mcp list
   ```
   确认 `fboxmcp` 出现在列表中即安装成功。

---

## 在 OpenClaw 中安装

1. **获取 API Key**（同上）

2. 打开 OpenClaw，进入 **设置 → MCP Servers → 添加**，填写：
   - 名称：`fboxmcp`
   - 传输协议：`Streamable HTTP`
   - URL：`https://fboxmcp.fbox360.com`
   - 请求头：`Authorization: Bearer <你的 API Key>`

3. 在技能市场搜索 `fboxmcp` 安装，或通过 URL 安装：
   ```
   https://github.com/flexem/fbox-skills
   ```

4. 在对话中描述设备相关需求即可激活技能。
