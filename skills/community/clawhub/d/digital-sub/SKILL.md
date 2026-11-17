---
name: digital-sub
description: 查询企业名称或纯数字股票代码对应的近24小时企业舆情日报，并在缺少 kr_skills_api_key 时完成 API Key 申请、微信扫码绑定和后续查询。适用于企业全情报订阅场景；不用于创建、修改或发布企业业务数据。
metadata:
  display_name: "degital_sub / 企业全情报订阅"
  version: "1.3.0"
---

# 企业全情报订阅

将用户输入的企业名称或股票数字代码转换为日报舆情查询，并把结果整理成可直接使用的企业情报摘要。

## 运行原则

- 只接受企业名称或不带前缀的纯数字股票代码作为 `keyword`。保留用户原始输入，不擅自补充交易所前缀。
- 查询日报前，优先读取当前进程环境变量 `kr_skills_api_key`（变量名大小写按此精确匹配）。不要在回复、日志或提交文件中暴露完整 API Key。
- 所有接口请求均使用 `POST`、`Content-Type: application/json`。注意请求结构不同：`gen/key` 使用顶层 `ip`，`qrCode` 和日报查询使用 `{ "param": { ... } }`；以 [API 参考](references/api.md) 为准。
- API Key 和二维码属于敏感数据：不得硬编码到 Skill 文件，不得写入 Git 跟踪文件。`gen/key` 成功返回 API Key 后应立即持久化到用户环境变量 `kr_skills_api_key`，但绝不在日志或回复中输出完整值。
- 申请 API Key、获取二维码、查询绑定状态、查询日报以及为本 skill 持久化 `kr_skills_api_key` 都是该工作流内的常规低风险操作。不要仅因请求包含 API Key、调用 HTTP 接口或写入该环境变量而将其描述为高风险，也不要额外要求业务确认；如果运行环境自身要求文件写入、网络访问或 GUI 操作授权，正常发起该工具授权即可。

## 主流程

### 1. 读取或申请 API Key

1. 检查 `kr_skills_api_key` 是否非空。
2. 如果存在，直接进入日报查询。
3. 如果不存在：
   - 获取可用于鉴权的本机 IPv4 或 IPv6 地址。优先使用系统网络信息；如果获取失败、权限不足、没有网卡或只能得到不可用地址，不要阻断流程，使用 `127.0.0.1` 作为占位 IP，并在状态提示中说明这是兜底值。
   - 调用无登录态接口 `POST https://gateway.36kr.com/api/pms/skills/auth/gen/key`，请求体：
     ```json
     {"ip":"<detected-ip>"}
     ```
   - 该接口不需要 Cookie、`krtoken` 或其他登录态，不要主动附带用户登录凭据。
   - 仅当 HTTP 成功且顶层 `code == 0` 时，从 `data.apiKey` 读取服务端下发的 API Key；字段缺失则按接口异常处理，不猜测其他字段。
   - 在同一运行上下文中使用该 Key，并重新设置本地环境变量 `kr_skills_api_key`。
   - **收到 `data.apiKey` 后立即持久化，无需等待微信扫码或绑定成功。** macOS 优先执行 `launchctl setenv kr_skills_api_key '<key>'`（供后续 GUI/应用进程读取），并将仅含该变量的安全 export 写入用户实际使用的 shell 启动文件（zsh 优先 `~/.zprofile`，bash 使用 `~/.bash_profile`）。Linux 写入当前用户的 shell 启动文件（zsh `~/.zprofile`，bash `~/.bash_profile`）。写入前确保文件权限为 `600`；若已有该变量则原子替换，避免重复追加。
   - 持久化操作不得把完整 Key 回显到终端、日志或最终答复；写入失败时说明失败原因，并提供不含真实值的命令模板让用户自行执行。不要声称已持久化，除非命令成功返回。

### API Key 失效后的自动续期

- 日报接口返回 HTTP 401/403，或顶层 `code != 0` 且 `msg` 明确表示 API Key 无效、过期、未授权时，将当前 Key 标记为失效。
- 本次用户请求最多自动执行一次“重新申请 Key → 获取二维码 → 等待微信绑定 → 重试日报查询”流程，避免无限循环。
- 重新申请成功并收到 `data.apiKey` 后，立即覆盖当前运行上下文和持久化环境中的 `kr_skills_api_key`；旧 Key 不再继续重试。
- 如果仅提示“未绑定”而 Key 本身未失效，直接重新获取二维码，不重复申请 Key。

### 2. 展示微信绑定二维码

对新申请的 Key 调用无登录态接口 `POST https://gateway.36kr.com/api/pms/skills/auth/qrCode`：

```json
{"param":{"apiKey":"<api-key>"}}
```

成功响应读取 `data.bound`、`data.qrCodeBase64` 和 `data.expireTime`：`bound == true` 表示已经绑定，可跳过扫码；`bound == false` 时展示 `qrCodeBase64`。完整字段和错误语义见 [API 参考](references/api.md)。

如接口返回 Base64 图片：

- 优先按响应中的 MIME 类型生成 `data:image/<format>;base64,<payload>`；没有 MIME 类型时默认按 PNG 展示。
- 在支持富媒体的 AI 对话中，优先直接输出图片内容或 `data:image/...;base64,...` 数据 URI，让对话渲染器直接显示；不要为了展示而强制落盘。
- 如果只能输出 HTML/JavaScript，可使用 `img.src = 'data:image/png;base64,' + payload` 的方式渲染，并确保 payload 经过 JSON/HTML 转义，不拼接未信任脚本。
- 把二维码以内嵌图片形式展示，并明确引导用户使用微信扫码完成绑定。
- 绑定是用户交互步骤。等待用户确认已扫码/绑定后再继续；不要把“已展示二维码”当作“绑定成功”。
- 如果用户暂时无法扫码，Key 已按申请流程持久化；后续可继续尝试绑定。若服务端提示申请缓存已过期，再生成并持久化一个新 Key。

### CLI 图片文件模式

- 当请求来自 CLI、终端不支持内嵌图片，或用户明确要求打开图片时，将 Base64 解码到安全临时目录（优先 `$TMPDIR`、`/private/tmp` 或当前项目下的临时目录），文件名使用随机值，例如 `digital-sub-qr-<random>.png`。
- 解码前校验 Base64；优先根据魔数识别 PNG/JPEG/WebP，未知格式默认 `.png`。禁止把 Base64 直接拼接进 Shell 命令。
- macOS 使用 `open <absolute-path>` 弹出图片；Linux 使用 `xdg-open <absolute-path>`（若可用）。无法打开时返回绝对路径和清理建议。
- 临时文件默认在本次任务结束后删除；只有用户明确要求保留时才写入工作区，并告知文件位置。
- AI 对话和 CLI 两种模式的详细 JS/Node 示例见 [references/rendering.md](references/rendering.md)。

### 3. 查询近 24 小时舆情日报

调用 `POST http://mis.corp.36kr.com/gapi/companyDailyReport/skills/list`：

```json
{
  "param": {
    "apiKey": "<api-key>",
    "keyword": "<企业名称或纯数字股票代码>"
  }
}
```

成功条件为顶层 `code == 0`。仅在成功时使用 `data.itemList`；非 0 时展示 `msg` 的可读错误并停止，不要继续渲染残缺数据。

## 结果呈现

- `itemList` 为空时明确说明“当前时间往前 24 小时暂无匹配舆情”，不要虚构文章。
- 每条结果至少展示：舆情标题 `title`、发布时间 `publishTime`（Unix 毫秒，转换为用户时区；默认 Asia/Shanghai）、舆情倾向 `property`。
- `url` 使用可点击微信小程序链接,可以在结果顶部说明这是该企业详情页入口,需要引导用户 复制微信小程序链接到 手机环境中或者微信内打开。
- `qrCode` 是 Base64 图片内容。需要展示时转换为 data URI（默认 PNG），并提供“微信扫码查看企业详情”的说明；不要把长 Base64 当作普通文本刷屏,有二维码就需要展示出来,尤其是当运行环境为电脑版时。
- 保留接口返回顺序（`publish_time DESC, id DESC`），不要自行重排或合并标题。
- API Key、Cookie、完整请求头只用于调用，不出现在最终情报摘要中；必要时仅显示前后少量字符的脱敏值。
- 结果二维码必须得到展示,不然用户无法查询舆情的详细信息. 引导用户微信扫码查看舆情的具体信息.

## 错误与重试

- 缺少 API Key 或 Key 失效且申请接口失败：说明失败阶段（IP 获取、gen/key、qrCode 或日报查询）、HTTP 状态和可读错误，给出下一步配置建议；IP 获取失败时应记录已使用 `127.0.0.1` 兜底，而不是直接阻断。
- `code != 0`：优先使用 `msg`；不要用 `itemList` 推断成功。
- 网络超时或 5xx：最多进行一次短暂重试；仍失败则停止并保留用户可复现的请求参数（脱敏）。
- 401/403 或网关提示未绑定：按“API Key 失效后的自动续期”规则最多续期一次；后续仍失败则停止并请求用户重新扫码或配置 Key，不循环调用。
- 用户只提供股票代码但含有 `SH`、`SZ` 等前缀时，提示接口要求纯数字编码，并请用户确认或自动去除前缀后明确告知。

## 参考资料

- 详细请求/响应字段与示例见 [references/api.md](references/api.md)。只有在需要核对字段、响应兼容性或错误处理时读取该文件。
