# 35 · 登录 / 授权 / Web UI 统一流程

> 目标：所有网盘都按同一套安全顺序处理，避免重复出现“聊天里贴 Cookie”“下载进度刷屏”“临时页面绕开 Skill”的问题。

## 0. 秒级提醒
- 收到网盘链接后，优先一次调用 `pan route <链接> --json --brief`；它只返回下一步决策需要的字段，避免长 JSON 消耗 token。
- 这一步只识别域名和检查本机登录态，不联网、不读凭据明文；服务内路由通常 <20ms，CLI 冷启动一般 <1 秒。
- Web UI `/api/download` 也会在投递前做同一检查；需要登录时立刻打开登录页，不先进入下载。

## 1. 优先级
1. **官方 OAuth / 扫码 / 浏览器授权**
2. **系统凭据库 / 工具自身配置**
3. **本机浏览器手工 Cookie（仅在必要时）**
4. **账号密码（最后手段，且必须在安全输入框/终端完成）**

## 2. 全网盘铁律
- 不要把密码、Cookie、BDUSS、STOKEN、refresh_token、API Token 发进聊天。
- 不绕过验证码、风控、限速、会员限制、DRM。
- 需要网页登录时，先让用户在浏览器完成；Agent 只负责识别结果和启动下载。
- 下载必须进入网盘通 Web UI 的任务中心和 `/live`，不使用聊天轮询展示进度。

## 3. 分网盘默认顺序
- 百度：公开分享先走匿名 `baiduweb`；一旦 `auth_required`/`dlink_missing`，立刻用 `pan login baidu --qr` 官方扫码（写入 BaiduPCS-Go），分享链接先转存，再 `--engine baidupcs`。
- 阿里：官方 OAuth > AList 扫码 / refresh_token。
- 夸克、115、123、移动、天翼、迅雷：AList 驱动扫码 / OAuth / Cookie 授权。
- OneDrive / Google Drive / Dropbox / SharePoint：OAuth。
- 坚果云：WebDAV 应用密码。
- 其他：官方客户端、CLI、AList、公开直链。

## 4. Web UI
- `/`：任务中心，显示状态、进度、速度、剩余时间。
- `/live`：实时速度和进度曲线。
- `/login`：统一登录入口，按网盘显示优先级和禁止事项。
- `/test`：下载前检查。
- 下载中的任务不应靠 Agent 在聊天里轮询状态；页面每 10 秒自动刷新，粘贴/输入后立即投递并回执受理耗时。

## 4.5 硬规则：登录只走统一入口
- **禁止** Agent 用临时脚本直连网盘登录接口（passport/qrcode/unicookie 等）。
  历史事故：手搓百度扫码脚本轮询带延迟，`v3sign` 过期，扫码成功却拿不到 BDUSS。
- 扫码/授权一律走 `pan login <网盘> --qr` 或 Web UI `/login`；失败按标准错误码处理。
- 报告必须带 `login_required` / `remediation`，不允许"闷头失败 N 个文件"。

## 5. 失败处理
- 官方限制、会员限制、风控、验证码、DRM：如实说明，不绕过。
- 登录态过期：让用户重新完成官方登录，更新系统凭据库。
- 下载中途退出：保留断点文件，Web UI 显示可重试；不要丢任务记录。
