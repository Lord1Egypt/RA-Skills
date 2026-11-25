---
name: easy-webbridge-uploader
description: 通过用户已安装的 Easy WebBridge，将用户明确指定的本地文件上传到其指定网页中的文件输入框；完成上传核验后停止，不提交或发布。
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins:
        - node
    homepage: https://github.com/aiispower/easy-webbridge
    emoji: "📤"
---

# Easy WebBridge 文件上传

## 适用范围

本 Skill 只协助把用户明确指定的本地文件送入用户指定网页中的文件输入框。它依赖单独安装并运行的 Easy WebBridge 和已连接的目标浏览器；本包提供精简 CLI，不含 Bridge 服务端、扩展、安装器或图片素材。它只负责上传，不提交、发布、发送或确认最终表单。

用户需要明确目标网站/页面、目标账号或 browserId、具体文件路径，以及本次允许上传的内容。若任一项不明确，先确认；不要从目录中自行挑选文件。

## 前置条件

- Node.js 已安装，且用户已有 Easy WebBridge Bridge 正在运行并连接目标浏览器。CLI 使用本 Skill 自带的 `scripts/bridge-cli.mjs`；它不会启动或安装服务。若 Bridge 离线，请用户启动其现有 Bridge。
- Node.js 和 Easy WebBridge 依赖已由用户安装；目标浏览器扩展已连接，且目标站点已由用户本人登录。不要索取密码、Cookie、Token 或验证码。
- 用户指定的文件必须存在于给出的绝对路径，并符合页面显示的文件类型、尺寸和大小要求。不要改名、转码或替换文件，除非用户明确要求。

## 上传流程

1. 先检查本机 Bridge 状态，并列出已连接浏览器：

   ```bash
   node scripts/bridge-cli.mjs status
   node scripts/bridge-cli.mjs list
   ```

   如果 Bridge 未运行，请用户启动其现有 Bridge；本 Skill CLI 不提供服务启动功能。精确选择用户指定的 `browserId`；多个浏览器且目标不明时先确认。

2. 创建该上传任务的标签组，打开用户指定页面：

   ```bash
   node scripts/bridge-cli.mjs navigate <browserId> <URL> --new-tab --session easy-webbridge-uploader-<run-id> --group-title "文件上传"
   node scripts/bridge-cli.mjs command <browserId> list_tabs '{}'
   ```

   读取页面快照，确认域名、账号身份线索、页面标题和表单目的都与用户要求一致。不要在不相关的现有页面上操作。

3. 优先检查当前页面是否已有 `input[type=file]`。如果有，直接使用 `upload`；不要先点击固定坐标或触发系统文件选择框。若输入框尚不存在，先读取快照与截图，定位唯一且语义匹配的上传控件，操作后等待并重新核对文件输入框。无法唯一识别时停止，不猜按钮或坐标。

4. 只使用用户指定的绝对文件路径上传：

   ```bash
   node scripts/bridge-cli.mjs command <browserId> upload '{"tabId":<tabId>,"selector":"input[type=file]","files":["/absolute/path/to/user-selected-file"]}'
   ```

   当前 Bridge 的 CDP 文件上传只支持顶层页面；跨域 iframe/OOPIF 不受支持。遇到输入框不存在、权限错误或 `frameId` 限制时说明阻塞，不改用隐藏路径、坐标猜测或其他上传手段。

5. 回读页面并截图确认文件名、预览或上传状态。成功证据应来自页面实际状态，不能把命令返回 `fileCount` 当作站点已保存或已发布。结束时仅关闭本任务创建的 session；保留用户原有页面和其它任务组。

## 安全边界

- 上传会把本地文件内容交给目标网站。只有用户明确授权了该文件和目标时才进行。不得上传其他文件或向未授权域名发送内容。
- 上传操作后停下并报告状态；不点击提交、发布、发送、支付、删除或公开按钮。用户如另行明确要求这些操作，应按相应 Skill 与任务范围处理。
- 不读取、输出或保存 Cookie、Token、密码、页面私密数据；不绕过 CAPTCHA、登录验证、访问控制或平台限制。遇到验证要求交由用户本人。
- 不调用 `get_cookies`、`set_cookie`、`remove_cookie`、网络请求正文捕获、任意 `evaluate` 或 raw CDP；不使用固定坐标点击。
- 文件路径或页面快照可能包含个人资料；仅在执行时使用，不复制到聊天、日志或生成文件。

## 完成报告

说明目标域名、用户指定文件名、实际页面证据和结果；区分“文件已选择/上传中/页面已显示/已保存”。本 Skill 结束状态是已上传并核验或明确阻塞，不代表表单提交、发布或公开成功。
