# 浏览器扩展

本目录只保留 Chrome 扩展，用于 KYC 查询和浏览器出口检查。原先的 Go 诊断程序、静态下载站和构建脚本已移除：出口 IP、地区、类型、风险分、时区等网络检查已并入根目录 `scripts/check.py`，找回对话改用 `scripts/sessions.py`。

## 使用

在用户指定的 Chrome Profile 扩展管理页开启开发者模式，加载 `extension/`（未上架商店）。详细安装流程见根目录 [references/kyc.md](../../references/kyc.md)。

- KYC：用当前已登录的 Claude 页面，同源请求，不读 Cookie。
- 浏览器网络按钮：访问 ipify 看浏览器出口；WebRTC 每次确认才访问 Google STUN。
- 权限仅 activeTab、scripting 和两个 ipify 域名；无后台进程、无存储、无遥测，结果只留在弹窗。

扩展自带 `node extension/self-test.cjs`、`node extension/network-test.cjs`。

## 限制

真实账号 KYC 接口尚未验收；HTTP 403 只表示请求被拒，不等于审核被拒。浏览器出口不代表运行中的 Claude 真实出口，KYC 查询不保证账号安全。验证记录见根目录 `references/validation.md`。

由 AI优铺维护：https://aiyopu.com/ 。购买及退款说明见根目录 README。
