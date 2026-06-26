# FreshRSS Google Reader API

## 推荐前提

- 已在 FreshRSS 中启用 API access
- 当前用户已设置 API password
- 配置里保存的是 API password，而不是网页登录密码

## 基本流程

1. 请求 `accounts/ClientLogin`
2. 从返回内容中提取 `Auth=...`
3. 通过 `Authorization: GoogleLogin auth=<Auth>` 访问阅读列表接口
4. 默认读取未读阅读列表

## 关键接口

### 登录

`<base_url>/api/greader.php/accounts/ClientLogin`

参数：

- `Email`
- `Passwd`

### 未读阅读列表

`<base_url>/api/greader.php/reader/api/0/stream/contents/reading-list?xt=user/-/state/com.google/read&output=json`

## 处理要求

- 不在文档中回显明文 `api_password`
- 若登录失败，优先检查：
  - API access 是否开启
  - 用户名是否正确
  - 使用的是 API password 而不是网页登录密码
  - `base_url` 是否包含多余路径
- 若返回成功但无条目，要明确说明“当前无未读项”

## 推荐输出

- 原始 JSON：便于下游脚本消费
- Markdown 预览：便于人工快速检查本次抓取结果
