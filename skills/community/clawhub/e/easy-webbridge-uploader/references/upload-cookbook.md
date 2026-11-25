# Easy WebBridge 上传命令手册

本文件供 `easy-webbridge-uploader` 使用。本 Skill 自带仅连接 loopback Bridge 的精简 CLI；Bridge 服务端和浏览器扩展仍需用户单独安装并运行。

## 变量

- `scripts/bridge-cli.mjs`：随 Skill 提供的精简 CLI；不能启动服务。
- `<browserId>`：用户指定的已连接浏览器 ID。
- `<tabId>`：`list_tabs` 返回的目标标签页 ID。
- `<session>`：本任务使用的唯一标签组名，如 `easy-webbridge-uploader-20261027-01`。

## 1. 检查依赖和浏览器

```bash
node scripts/bridge-cli.mjs status
node scripts/bridge-cli.mjs list
```

Bridge 未运行时请用户启动其现有 Bridge；该 CLI 不提供 `start`。

## 2. 打开目标页面并回读状态

```bash
node scripts/bridge-cli.mjs navigate <browserId> "<用户指定URL>" --new-tab --session <session> --group-title "文件上传"
node scripts/bridge-cli.mjs command <browserId> list_tabs '{}'
node scripts/bridge-cli.mjs snapshot <browserId> <tabId> --compact
```

页面内容、账号线索和目标表单应与用户要求相符后再继续。

## 3. 选择文件输入框

先检查页面当前 DOM 中是否有 `input[type=file]`。存在时可直接上传，避免打开原生文件选择框。只有控件确实动态生成时，才根据当前快照定位唯一、语义明确的上传按钮，再截图复核并点击；随后使用 CLI `wait` 等待 `input[type=file]` 出现并重新快照。不可用固定坐标或页面猜测。

```bash
node scripts/bridge-cli.mjs wait <browserId> <tabId> --selector 'input[type=file]' --state attached --timeout-ms 10000
```

## 4. 上传且核验

必须使用用户指定的绝对文件路径；只要目标页面、浏览器和文件已由任务明确授权，无需逐步确认。仅在目标不明确时澄清。

文件路径需为当前系统的绝对路径；Windows 支持 `C:\Users\...` 和 UNC 绝对路径。

```bash
node scripts/bridge-cli.mjs command <browserId> upload '{"tabId":<tabId>,"selector":"input[type=file]","files":["/absolute/path/to/file.png"]}'
node scripts/bridge-cli.mjs snapshot <browserId> <tabId> --compact
node scripts/bridge-cli.mjs screenshot <browserId> <tabId>
```

`upload` 使用 CDP `DOM.setFileInputFiles`；当前只支持顶层页面的文件输入框，不支持跨域 iframe/OOPIF。返回的文件数量不是服务端已保存或发布证据。回读页面确认状态后停止，不点击发布/提交。最后只关闭本任务拥有的标签组。
