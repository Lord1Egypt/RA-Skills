# B站合集学习顺序单

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

把你已打开且可访问的 B 站合集或收藏夹，整理成一份按学习目标排序、按每日时间预算分配的观看计划。结果保留每条可见来源、简介、时长与缺项；不会把标题当成内容验证，也不会把离线样例说成在线采集结果。

![B站合集学习顺序单推广图](assets/promo.png)

## 输入与结果

输入：合集/收藏夹 URL、学习目标、每日时间预算，以及用户指定的 `browserId`。

结果：最多 100 条的观看顺序表和每日预算草稿，包含标题、可见简介、可见时长、来源链接、匹配理由及缺项。私人收藏夹未授权、登录/验证码/风控会暂停；时长不可见则标“未知”，不计入预算。

## 安装

```bash
npx skills add xxjrq/bilibili-learning-playlist-plan-free
```

## 浏览器前置依赖

本 Skill 需要 [Easy WebBridge（GitHub）](https://github.com/xxjrq/easy-webbridge)，Gitee 备用：[easy-webbridge](https://gitee.com/xxjrq/easy-webbridge)。安装并连接目标浏览器后，由用户指定单个 `browserId`；每项任务仅使用自己的 session 与标签组，绝不广播到全部账号或接管已有页面。

运行时把 `EASY_WEBBRIDGE_CLI` 配置为已安装 Easy WebBridge 的 CLI。流程会先读取 CLI help，使用 `snapshot --text-mode page` 读取网页可见内容并在翻页后刷新 refs。默认只读；若获授权填写草稿，也不会点击最终发布或发送。

## 离线自测

```bash
node scripts/self-test.mjs
```

自测仅执行 `fixtures/` 的离线页面资料模拟，验证可见资料规划与未授权失败分支；它不冒充真实网站采集，也不替代浏览器 Agent 的现场授权与页面核验。

## 来源与许可

业务用途参考 [OpenCLI](https://github.com/jackwener/OpenCLI) 与其 [Bilibili adapter 文档](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/bilibili.md)。本仓库原创编写，未复制其实现或文案；使用前请核对上游许可证。

MIT-0，见 [LICENSE](LICENSE)。

## 离线成功与失败样例

[成功输入](fixtures/visible-success.json) → [脚本实际输出](fixtures/success-output.md)；[失败输入](fixtures/failure-private-unauthorized.json) → [实际拒绝结果](fixtures/failure-output.md)。失败输入与原 private-unauthorized.json 逐字一致，仅补便于识别的文件名；这些示例是离线资料模拟，不是在线采集。

## 时长输入二选一

每条只提供 `visibleMinutes` 或 `visibleDuration`；两字段同时出现时拒绝，即使换算值相同或其中一个为空。[单项时长正例](fixtures/success-duration-exclusive.json) → [实际排期](fixtures/success-duration-exclusive-output.md)；[同值冲突](fixtures/failure-duration-equal.json)、[异值冲突](fixtures/failure-duration-conflicting.json)、[空值仍双字段](fixtures/failure-duration-null.json)均须拒绝。以上仅是离线资料测试。
