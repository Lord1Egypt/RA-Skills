# 免费闲鱼商品上架

把已有的商品资料和图片填到闲鱼发布页，生成发布前草稿；也可先按关键词查看公开同款。免费使用，不需要第三方 API Key。

## 使用前先准备

macOS（仅 Apple 芯片）和 Windows 用户打开 EasyBR 即可使用内置 Easy WebBridge；从[官方客户端下载页](https://www.ebrower.com/down.html)选择版本，也可用 [GitHub Release 镜像](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)。其他系统按 [Easy WebBridge GitHub 源码说明](https://github.com/xxjrq/easy-webbridge)安装（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)）。把 Skill 交给 Codex、Claude 或 WorkBuddy，先确认浏览器名称和 `browserId`，再指定已登录的环境。

## 怎么说

“使用 `$easy-xianyu-publish-free`，用 `easybr-xianyu-a` 的闲鱼主店，把 `./product.json` 填成发布草稿，发布前停住。”

可选提供搜索词，先整理公开同款的标题、价格带和卖点，再填写自己的草稿。默认会检查字段并停在发布按钮前。登录、验证码、实名和风控需要你自己处理；不保存账号信息，也不保证成交或流量。
