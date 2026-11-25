# 闲鱼多账号工作台

把多个闲鱼账号的任务按 EasyBR 浏览器环境分开执行，结果不会串号。可做商品草稿、竞品搜索和消息摘要，免费使用，不需要第三方 API Key。

## 使用前先准备

macOS（仅 Apple 芯片）和 Windows 用户打开 EasyBR 即可使用内置 Easy WebBridge；从[官方客户端下载页](https://www.ebrower.com/down.html)选择版本，也可用 [GitHub Release 镜像](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)。其他系统按 [Easy WebBridge GitHub 源码说明](https://github.com/xxjrq/easy-webbridge)安装（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)）。把 Skill 交给 Codex、Claude 或 WorkBuddy，先确认浏览器名称和 `browserId`，再指定已登录的环境。

## 示例

“使用 `$easy-xianyu-multi-account-ops`，主店用 `easybr-xianyu-a`、副店用 `easybr-xianyu-b`，分别整理商品草稿和消息摘要，同一浏览器串行，全部停在需要我确认的地方。”

发送消息、改价、下架、删除和最终发布不会自动执行；登录、验证码和风控由你在对应环境中处理。

