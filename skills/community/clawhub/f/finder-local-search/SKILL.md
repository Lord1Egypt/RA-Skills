---
name: finder-local-search
description: 当需要搜索或推荐 TikTok、YouTube、Instagram 红人时使用，通过 Finder 获取候选红人。
---

# Finder 本地搜索

这个 skill 用 Finder 开放接口搜索普通达人。

## 什么时候用

- 用户想搜某个平台、某地区、某语言、某标签的达人
- 用户想按粉丝区间、平均播放、互动率筛选达人
- 用户第一次配置 Finder 访问秘钥

## 核心规则

- 默认服务地址：`https://finder.optell.com`
- 本地配置文件：
  - macOS / Linux：`~/.finder/config.json`
  - Windows PowerShell：`$HOME/.finder/config.json`
- 优先自动执行；做不到时再给用户可复制命令
- 用户把 `api key` 发到对话里时，直接帮他写入本地配置文件
- 不要让用户重复描述需求
- 只支持普通达人搜索，不调用相似达人搜索
- 如果搜索返回“搜索次数已超出当前限制”，提醒用户发邮件到 `developer.optell@gmail.com` 申请增加使用量

## 工作流

1. 先检查本地是否已有 `config.json`。
2. 如果没有：
   - 引导用户登录 `https://finder.optell.com`
   - 打开 `https://finder.optell.com/api-key`
   - 生成访问秘钥
   - 如果用户把 key 发到对话里，直接帮他创建 `.finder/config.json`
3. 读取 `references/filters.json`，把用户需求转成搜索参数。
4. 先查项目；如果没有项目，先说明原因，再征求确认创建默认项目。
5. 调用 Finder 搜索接口并返回结果。
6. 如果返回“搜索次数已超出当前限制。如需增加使用量，请发送邮件至 developer.optell@gmail.com”，直接告诉用户已达到当前限制，并引导他发邮件申请增加使用量。
7. 如果结果为空，建议放宽 1 到 2 个条件继续搜索。

## 对话要求

- 用中文，简短直接
- 先帮用户做，再提示用户补必要信息
- 能自动做的就直接做
- 用户给过的 key 不要重复要求输入
- 回复风格尽量自然，比如：
  - `我先帮你检查一下 Finder 配置。`
  - `我已经帮你把访问秘钥写到 ~/.finder/config.json 里了，后面就不用再重复输入了。`
  - `你现在还没有项目，要我顺手帮你建一个默认项目吗？`
  - `你当前的搜索次数已经达到限制了。如果你想增加使用量，可以发邮件到 developer.optell@gmail.com，我也可以帮你整理一段邮件内容。`

## 参考文件

- 安装与配置说明：`references/config.md`
- 搜索词典与别名：`references/filters.json`
- 示例对话：`references/examples.md`
