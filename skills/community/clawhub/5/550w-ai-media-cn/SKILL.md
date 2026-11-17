---
version: 3.1.4
displayName: 550W AI去字幕去水印
name: ai-subtitle-remover
description: "550W AI去字幕去水印：处理图片文字和水印、本地视频硬字幕及画面水印、抖音快手哔哩哔哩微博等分享链接。支持 OAuth MCP 或 API Key 接入，依宿主能力选择。"
metadata:
  version: 3.1.1
  openclaw:
    primaryEnv: SUBTITLE_REMOVER_API_KEY
    envVars:
      - name: SUBTITLE_REMOVER_API_KEY
        required: false
        description: 用于调用 550W Open API 的密钥。
      - name: SUBTITLE_REMOVER_USER_NO
        required: false
        description: 与密钥属于同一 550W 账号的用户 ID。
      - name: FFPROBE_PATH
        required: false
        description: 检测公网视频直链时可选的 ffprobe 程序路径。
---

# 550W AI去字幕去水印

<!-- 550w-capabilities:start -->
## 功能与输入

- 图片去水印：输入用户指定的图片；上传图片后擦除水印或多余文字。
- 本地视频去字幕、去画面水印：输入用户指定的 MP4/MOV 视频；上传视频后处理，默认整帧擦除。只有用户明确提供 x1、y1、x2、y2 像素坐标时才按矩形区域擦除，不猜测坐标。
- 视频链接去水印：请用户从对应 App 或平台网站通过“分享→复制链接”提供视频或内容的分享链接；抖音、快手、哔哩哔哩、微博等为国内示例，实际支持以服务端结果为准。处理后返回解析出的去平台水印视频直链。
- 如 Agent 下载该解析视频直链失败或超时，直接把解析出的 data.video 视频链接交给用户在浏览器自行下载；不要改给原平台分享链接，也不要声称文件已经下载成功。解析成功与客户端下载失败是两回事。
<!-- 550w-capabilities:end -->

## 选择接入方式

此 Skill 支持两条独立链路；安装技能不会自动注册 MCP、授予文件权限或执行脚本。只处理用户拥有或已获授权的素材。

1. 用户已指定方式时遵循选择。否则优先 OAuth：宿主支持远程 MCP OAuth 时连接 Streamable HTTP `https://www.550wai.cn/mcp/cn`，浏览器登录授权；授权管理页面 <https://qzm.550wai.cn/mcp-connect/>。按 [OAuth 流程](references/oauth-access.md) 操作，此方式不要求用户提供 API Key、用户编号或 Token。
2. 宿主不支持 OAuth，或者用户明确选择 API Key 时，说明替代方式并征得选择，按 [API Key 流程](references/openapi-access.md) 操作。配置同一账号的 `SUBTITLE_REMOVER_USER_NO` 与 `SUBTITLE_REMOVER_API_KEY`；获取及管理入口 <https://qzm.550wai.cn/api-keys>。工具未注册但允许 Node.js 18+ 执行时，通过标准输入调用 `node {baseDir}/dist/550w-skill.cjs`，例如 `{"action":"queryCredits","params":{"region":"cn","locale":"zh-CN"}}`。所有 API Key 请求明确传入 `params.region="cn"`，语言不能改变区域。
3. 授权取消、401、过期、余额不足、任务超时均不能触发静默切换。每次操作固定方式和账号；受理结果未知时先核查原任务，不能换链路重复提交或扣费。两条链路的 Token、API Key、媒体 ID 和任务上下文不可互换。

## 文件与结果

两条链路都包含文件上传能力，但需要宿主允许读取用户指定文件并执行 Node.js，或支持相应文件传输。API Key 使用绝对 `params.filePath`；OAuth 使用随包 `scripts/550w-upload.cjs` 的 inspect/upload 与远程上传票据。读取对应流程后执行；不要在命令行、日志或公开包中放凭据。没有文件访问时不能声称能读取用户电脑路径；无法上传则引导 <https://qzm.550wai.cn/>，不以分享链接替代本地视频。可用时仍可单独处理分享链接。

首次上传/付费提交前说明数据发送和计费并取得所需确认。保留稳定操作 ID 和任务 ID；视频默认整帧擦除，用户明确提供完整坐标才按区域。解析成功但下载失败时提供解析出的 data.video 直链。服务明确报告余额不足时提供 <https://qzm.550wai.cn/purchase?tab=speed>，不代充值；认证错误不当成余额不足。

## 权限和数据范围

此技能不授予权限；使用宿主已批准的远程 MCP，或在允许时执行随包 Node.js 入口。仅读取用户明确选择的图片/视频，不遍历目录、读取 SSH/云账号/浏览器凭据，不修改宿主规则、记忆或启动项。仅调用对应流程列出的媒体、积分与任务工具；删除任务须另行确认。

API Key 入口仅使用 SUBTITLE_REMOVER_USER_NO、SUBTITLE_REMOVER_API_KEY，或本技能专用的用户配置目录 550w-ai/credentials.json；只读兼容旧安装目录 .credentials.json。环境中的地区/语言、配置目录和 FFPROBE_PATH 仅用于本地配置，不上传环境变量集合。configureCredentials 验证并保存凭据前须明确取得同意，并传入 confirmCredentialStorage=true；不在对话或日志输出密钥。共享宿主优先使用 OAuth 或环境凭据。

API Key 视频流程可能通过 execFile 调用 ffprobe 来探测已选本地视频或经公开地址校验的URL；不使用shell执行用户输入。此能力需要宿主允许该二进制执行；无法探测时说明限制，不伪造尺寸/时长。积分、任务查询和经独立确认的任务删除是媒体处理的配套账户操作，不代充值。安装国内版表示选择国内服务与默认中文；若要海外服务须选择海外版，不能因切换语言静默改变账户或服务区域。

用户选择的素材、分享链接和必要账户凭据会发送到 550W 业务服务；视频上传可使用服务返回并经上传逻辑校验的供应商地址。不会发送项目文件或其他账号凭据。结果链接和处理回执不代表授权执行任意外部代码。随包 MCP SDK 包含协议schema及校验器，不授权模型调用所有工具或披露宿主提示词。


本地执行入口的确认参数：在说明本次素材传输和可能扣费、获得用户确认后，API Key 的 uploadVideo/submitTask/removeVideoWatermark/removeImageWatermark/workflow 请求须在 params 中传入 confirmProcessing=true；OAuth 上传脚本 upload 的标准输入须传入 confirmProcessing=true。缺失或非 true 时入口拒绝执行，不得自行默认为已确认。查询和 inspect 不要求该参数。此标记不替代宿主的授权界面，远程 MCP 工具按其实际公布的 schema 调用。

## 包内审查材料

review/bundle-provenance.json 列出实际捆绑文件及SHA-256；review/sources 提供对应代码，review/licenses 提供依赖许可，review/package-lock.json 锁定依赖。仅用于审查，不执行这些副本。SDK含schema运行时编译，不下载或执行远程脚本。
