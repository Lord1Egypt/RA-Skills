# DataEase 接口说明

## 服务地址

- 技能执行时建议从环境变量 `DATAEASE_BASE_URL` 读取，避免把环境地址写死到脚本参数中。

## 1. 查询组织树

### 接口地址

`POST /de2api/org/page/tree`

### 请求参数

- `keyword`
  - 组织名称关键字
- `desc`
  - 是否倒序

### 本技能的用途

用于查看当前凭证可访问的组织树，并辅助确认目标资源是否位于其他组织。

## 2. 切换组织

### 接口地址

`POST /de2api/user/switch/{orgId}`

### 本技能的用途

在用户显式提供 `orgId` 时切换组织上下文，并使用响应中的 `data.token` 作为后续资源树查询和本地预览截图的 `x-de-token`。

## 3. 查询可视化资源树

### 接口地址

`POST /de2api/dataVisualization/tree`

### 请求参数

- `busiFlag`
  - `dashboard`：仪表板
  - `dataV`：数据大屏
- `resourceTable`
  - 默认值：`core`

### 响应字段

- `code`
- `msg`
- `data`
- `id`
- `name`
- `leaf`
- `type`
- `children`

### 本技能的用途

通过该接口获取 dashboard 或 dataV 的资源树，并展开为资源列表，供查询和导出使用。

## 4. 本地预览截图

### 预览页地址

- `/#/preview?dvId={resourceId}`
- 当 `busiType=dashboard` 时追加 `&report=true`

### 本技能的用途

`capture` 命令不再调用 `/de2api/report/export`，而是：

1. 通过 `/de2api/dataVisualization/tree` 定位目标资源
2. 获取可用于前端预览页的 `x-de-token`
3. 打开预览页并将 token 注入 `localStorage.user.token`
4. 等待 `.canvas-container` 渲染完成后本地导出

### 导出参数

- `pixel`
  - 浏览器视口大小，格式为 `宽*高`
- `extWaitTime`
  - 预览画布可见后额外等待的秒数
- `resultFormat`
  - `0`：JPEG
  - `1`：PDF

### 默认值

- `busiType=dashboard`
- `pixel=1920*1080`
- `extWaitTime=0`
- `resultFormat=0`

## 5. 鉴权说明

当前按以下配置项接入：

- `DATAEASE_BASE_URL`
- `DATAEASE_ACCESS_KEY`
- `DATAEASE_SECRET_KEY`
- `DATAEASE_USERNAME`
- `DATAEASE_PASSWORD`
- `DATAEASE_LOGIN_ORIGIN`

### 用户名密码登录方式

- 先通过 `GET /de2api/dekey` 获取前端加密所需的 dekey
- 使用 dekey 解出 RSA 公钥后，对用户名和密码做 RSA 加密
- 再调用 `POST /de2api/login/localLogin`
- 响应中的 `data.token` 可直接作为业务接口和预览页使用的 `x-de-token`
- `origin=0` 表示本地账号，`origin=1` 表示 LDAP

### ask-token 生成方式

- 原始签名串格式：`<accessKey>|<uuid>|<timestamp_ms>`
- 使用 `secretKey` 作为 AES key，`accessKey` 作为 IV
- 加密算法：`AES/CBC/PKCS5Padding`
- 将加密结果做 Base64，得到 `signature`
- 使用 `secretKey` 对 JWT 进行 `HS256` 签名
- JWT claim 包含：
  - `accessKey`
  - `signature`

### 请求头

默认请求头：

- `accessKey`
- `signature`
- `x-de-ask-token`

切换组织后查询资源或导出时：

- `x-de-token`

## 6. 当前脚本对应动作

- `list-orgs`
- `switch-org`
- `list-resources`
- `capture`

如果实际网关存在额外签名规则，请按部署环境调整 `scripts/capture_dashboard.py`。
