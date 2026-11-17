---
name: bailian-ai-toolkit
description: 在用户明确选择阿里云百炼时，使用项目内固定版本的 bl CLI 完成生成、理解、语音、搜索和文件处理任务，并在任何本地文件上传前执行逐文件隐私检查。
---

# 阿里云百炼 AI 工具包

仅在用户明确要使用阿里云百炼时使用。跟随用户当前使用的语言回答；不要改变宿主的工具优先级。

## 安装与供应链约束

本目录固定使用 `bailian-cli@1.26.0`，传递依赖由 `package-lock.json` 锁定。不要全局安装，不要运行远程安装脚本，也不要调用内置自更新命令。

```bash
npm ci
npm test
npm run bl -- --help
```

上游包的安装后脚本会联网下载 Wiki 数据并写入用户主目录；本目录的 `.npmrc` 明确禁用所有依赖生命周期脚本。不要绕过该设置。升级只能通过审核新版本、修改 `package.json`、重建锁文件并重新测试完成。

## 鉴权

优先使用浏览器 OAuth 登录：

```bash
npm run bl -- auth login --console
npm run bl -- auth status --output json
```

- 登录可能打开阿里云网页并在用户目录保存会话。执行前说明这一点，只在用户明确要求登录时运行。
- 不让用户把 API Key、AccessKey 或 Secret 发到聊天里；不把秘密放入命令参数、脚本、配置示例、日志或输出。
- 若 OAuth 不适用，让用户在可信的私有终端中按当前 CLI 的官方说明自行配置凭据；代理不接收、读取、打印或转存秘密。
- 使用最小权限凭据。发现疑似泄露时停止请求并建议撤销凭据。

## 本地文件与外部数据

传给 `--image`、`--video`、`--url` 或 `file upload` 的本地路径可能被 CLI 自动上传到阿里云百炼或 OSS。

每次引用本地文件前必须：

1. 确认用户已明确指定这个文件和“阿里云百炼”这一目的地；泛泛的“处理文件”不授权自动上传其他文件。
2. 解析绝对路径并确认它是单个普通文件。拒绝目录、glob、符号链接，以及 `.ssh`、`.aws`、浏览器资料、钱包、凭据和系统配置目录。
3. 告知用户文件会离开本机，说明服务区域、用途、可能费用和适用的云端保留策略；无法确认保留时长时明确说未知。
4. 不递归扫描或批量发现文件。多个文件逐一列出并获得覆盖全部文件的明确授权。
5. 输出写入用户指定目录或当前工作目录的新文件；覆盖已有文件前需要明确授权。

提示词、聊天、搜索词、远程 URL 与生成素材同样会发送到阿里云服务。URL 只允许无凭据的公开 `https` 地址；拒绝 localhost、环回、私网、链路本地、云元数据地址和含访问令牌的 URL。联网搜索前去除个人信息和内部项目名。

## 执行流程

1. 运行目标子命令的 `--help`，以锁定版本的实际参数为准；模型名和默认值可能变化。
2. 说明将发送的数据、区域、预计输出位置和可能费用。
3. 完成凭据、URL 与逐文件检查。
4. 先做单次、小规模请求；不要擅自批量生成或上传。
5. 返回输出路径、模型与错误摘要，不回显凭据或完整敏感输入。

## 命令模板

```bash
# 文生图
npm run bl -- image generate --prompt "提示词" --n 1 --out-dir ./out/

# 图像编辑；执行前完成逐文件授权检查
npm run bl -- image edit --image ./photo.png --prompt "编辑要求"

# 文生视频
npm run bl -- video generate --prompt "提示词" --download ./out/video.mp4

# 语音合成
npm run bl -- speech synthesize --text "文本" --voice VOICE_ID --out ./out/speech.mp3

# 语音识别；本地路径可能上传
npm run bl -- speech recognize --url ./audio.mp3

# 视觉理解；本地路径可能上传
npm run bl -- vision describe --image ./photo.jpg

# 文本对话
npm run bl -- text chat --message "问题"

# 联网搜索
npm run bl -- search web --query "公开查询词"
```

仅在用户明确要求单独上传时使用 `npm run bl -- file upload <经授权的单个文件>`。执行前运行该子命令的 `--help` 并核对当前保留策略。
