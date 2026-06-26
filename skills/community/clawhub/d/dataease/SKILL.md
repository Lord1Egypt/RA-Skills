---
name: dataease-resource-skill
description: 通过自然语言查询 DataEase 组织、切换组织、列出仪表板或数据大屏，并把指定资源导出为截图或 PDF。
---

# 目标

根据用户的自然语言请求，调用 DataEase 接口完成以下工作：

- 查询组织列表
- 切换组织
- 查询指定组织下的仪表板或大屏列表
- 导出指定仪表板或大屏的截图或 PDF

# 输入

用户可能会这样表达需求：

- 查询当前可用组织
- 切换到华东组织
- 查看这个组织下有哪些看板
- 列出华东组织的大屏
- 导出“销售总览”看板
- 截一下“门店运营监控”大屏
- 导出华东经营分析为 pdf
- 截销售总览，分辨率 1920*1080，等 5 秒再导出

用户输入中可能包含：

- 组织 ID
- 组织名称
- 资源名称
- 业务类型：`dashboard` 或 `dataV`
- 输出格式：`jpeg` 或 `pdf`
- 分辨率，例如 `1920*1080`
- 额外等待时间

# 输出

输出内容应包括：

1. 实际执行的动作
2. 匹配到的组织或资源
3. 命中的资源 ID
4. 实际使用的导出参数
5. 生成文件本身；如果运行环境不能直接附带文件，则至少返回绝对保存路径
6. 如果无法准确匹配，则说明原因并返回候选项

# 执行规则

## 组织相关

- 只有用户明确要求“查组织”时，才调用组织树接口
- 只有用户明确要求“切组织”或已经指明目标组织时，才调用切换组织接口
- 如果用户只说“查询某组织下的资源”，优先确认是否已给出 `orgId`
- 如果只给了组织名称，没有唯一命中的组织，不要猜测，应返回候选组织

## 资源相关

- 如果用户明确提到“大屏”“数据大屏”“驾驶舱”，则使用 `dataV`
- 其他情况默认使用 `dashboard`
- 查询资源时优先列出叶子节点
- 如果用户只是想“看看有哪些资源”，返回资源列表
- 如果用户要求“导出”或“查看”某个资源，先匹配资源，再执行本地预览页截图流程
- 当存在多个相似候选时，不要直接猜测，应返回候选列表并说明歧义

## 导出默认值

- `busiType=dashboard`
- `pixel=1920*1080`
- `extWaitTime=0`
- `resultFormat=0`，表示 JPEG
- 如果用户明确要求 PDF，则使用 `resultFormat=1`

## 名称匹配规则

在匹配组织名称或资源名称前，需要做标准化处理：

- 去掉前后空格
- 英文统一转小写
- 忽略中英文引号差异
- 忽略常见标点差异
- 资源优先匹配叶子节点
- 如果存在别名映射，先用别名映射转换，再做匹配

# 鉴权与安全

- 不要把 `access key`、`secret key` 等敏感凭证硬编码到 skill 文件中
- 不要要求用户在提问里携带 `base_url`、`access key`、`secret key`、`username`、`password`
- 本技能通过以下配置读取环境：
  - `DATAEASE_BASE_URL`
  - `DATAEASE_ACCESS_KEY`
  - `DATAEASE_SECRET_KEY`
  - `DATAEASE_USERNAME`
  - `DATAEASE_PASSWORD`
  - `DATAEASE_LOGIN_ORIGIN`
- 脚本会自动读取仓库根目录 `.env`
- 如果提供了 `username` 和 `password`，脚本会先调用 `dekey` 和 `/login/localLogin` 获取 `x-de-token`
- 如果提供了 `accessKey` 和 `secretKey`，脚本会自动生成：
  - `signature`
  - `x-de-ask-token`
- 如果已切换组织，则后续查询资源或导出时使用切组织返回的 `x-de-token`
- 如果用户已提供现成的 `x-de-token`，脚本可直接复用

# 失败处理

- 如果组织树接口调用失败，明确说明组织列表加载失败
- 如果切换组织失败，返回 HTTP 状态和响应内容
- 如果资源树接口调用失败，明确说明资源列表加载失败
- 如果没有找到合适资源，返回最接近的候选名称
- 如果本地浏览器启动失败、预览页加载失败或截图失败，明确返回错误原因
- 只有在文件实际写入成功后，才能声明导出成功
- 导出成功后必须返回 `saved_file`

# 使用文件

- 使用 `scripts/capture_dashboard.py` 执行 API 调用和文件保存
- 使用 `scripts/browser_capture.mjs` 打开预览页并完成本地截图
- 使用 `references/api.md` 查看接口说明和鉴权接入方式
- 如需维护资源别名，编辑 `references/resource_aliases.json`

# 推荐命令

- 查询组织：
  - `python3 scripts/capture_dashboard.py list-orgs`
- 切换组织：
  - `python3 scripts/capture_dashboard.py switch-org --org-id 1225813472202330112`
- 查询指定组织下的看板：
  - `python3 scripts/capture_dashboard.py list-resources --org-id 1225813472202330112 --busi-type dashboard`
- 查询指定组织下的大屏：
  - `python3 scripts/capture_dashboard.py list-resources --org-id 1225813472202330112 --busi-type dataV`
- 导出看板截图：
  - `python3 scripts/capture_dashboard.py capture --org-id 1225813472202330112 --resource-name 销售总览 --busi-type dashboard`
- 导出大屏 PDF：
  - `python3 scripts/capture_dashboard.py capture --org-id 1225813472202330112 --resource-name 门店运营监控 --busi-type dataV --result-format 1`
