# AI Tools Chrome 扩展（预览版）

给 Claude 用户提供主动 KYC 查询、浏览器 IPv4/IPv6 出口和语言时区查看，以及需要每次确认的 WebRTC 候选检测。结果留在当前弹窗，关闭后不保存。

解压 ZIP 后，在 Chrome 扩展管理页开启开发者模式，选择“加载已解压的扩展程序”，选择本 extension 目录。打开已登录的 Claude 页面，再从工具栏点击扩展。仅供试用，尚未上架商店。

KYC 使用当前页同源请求，不读取 Cookie；HTTP 403 仅表示请求被拒，不等于审核被拒。真实账号接口仍待验收。未知状态原样显示，复制结果会隐藏未知原值、组织名与 UUID。

浏览器网络检查会访问 ipify，WebRTC 确认后联系 Google STUN；这些服务会看到网络地址。不会给账号风险评分，也不代表 Claude Code 的实际出口。默认不运行 WebRTC。

依赖 Chrome 的 MV3、activeTab 和 scripting；回显请求权限仅限 api.ipify.org、api6.ipify.org。无后台、无持久存储。

开发测试：`node self-test.cjs` 与 `node network-test.cjs`（测试文件只在源码目录中，不进入发布 ZIP）。
