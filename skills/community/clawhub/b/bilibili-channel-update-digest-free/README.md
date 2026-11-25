# B站UP主近期更新摘要

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

把指定 UP 主主页中当前可见的最多 10 条视频整理成近期更新清单。你提供一个已连接的浏览器 `browserId` 和主页链接，即可得到标题、页面显示日期、主题、链接、逐条来源与缺项说明；日期未显示就留空，不会编造投稿时间或播放数据。

![B站UP主近期更新摘要推广图](assets/promo.png)

## 输入与结果

输入：一个明确的 `browserId`、一个 UP 主主页 URL，及“最多 10 条当前可见视频”。

结果：可复制的 Markdown 表格，包含标题、日期、主题、链接、可见来源和限制；只是一份一次性清单，不创建监控，也不分析私密运营数据。

## 安装

```bash
npx skills add xxjrq/bilibili-channel-update-digest-free
```

这是浏览器类 Skill。先安装 [Easy WebBridge（GitHub）](https://github.com/xxjrq/easy-webbridge)，GitHub 不可用时使用 [Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)。在目标浏览器安装扩展并连接后，运行时由你指定唯一 `browserId`；Skill 每次只创建并关闭自己的 session 分组，不接管已有页面或其他账号。

## 使用

```text
使用我指定的 browserId 和这个UP主主页，最多整理10条当前可见视频为标题、日期、主题、链接与来源；未显示日期留空，不要编造数据。
```

遇到登录、验证码或风控会暂停且不绕过。默认只读；即便授权填充草稿，也绝不点击最终发布或发送。

## 本地校验

```bash
node scripts/self-test.mjs
```

校验仅检查离线 fixtures 的解析与仓库结构。成功和失败 fixtures 都是模拟页面资料，不是在线采集结果。

## 来源与许可证

业务用途参考 [Easy WebBridge](https://github.com/xxjrq/easy-webbridge) 与其 [Bilibili adapter 文档](https://github.com/xxjrq/easy-webbridge/blob/main/docs/adapters/browser/bilibili.md)；本仓库未复制其实现或原文。代码与文档以 [MIT-0](LICENSE) 发布。
