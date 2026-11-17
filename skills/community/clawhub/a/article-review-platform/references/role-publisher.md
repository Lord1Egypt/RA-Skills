# 发布管家角色指引

## 职责
从审阅平台拉取待发布文章，发布到各目标平台，同步发布状态。

## 查询待发布文章
```bash
# 拉取 approved 和 publishing 状态
curl -s "http://localhost:3100/api/articles?status=approved"
curl -s "http://localhost:3100/api/articles?status=publishing"
```

### 过滤逻辑
对每篇文章检查 `platform_status`：
- 所有目标平台都已 `published` → 跳过
- 有 `pending` / `failed` / `publishing` 的平台 → 需要处理

## 发布流程

### 1. 开始发布
```bash
# 如果文章还是 approved，改为 publishing
curl -s -X PUT http://localhost:3100/api/articles/{id} \
  -H "Content-Type: application/json" \
  -d '{"status":"publishing"}'
```

### 2. 发布前记录
```bash
curl -s -X POST http://localhost:3100/api/articles/{id}/publish-logs \
  -H "Content-Type: application/json" \
  -d '{"platform":"zhihu","stage":"prepare","status":"in_progress","message":"开始准备发布到知乎"}'
```

### 3. 发布中记录
```bash
curl -s -X POST http://localhost:3100/api/articles/{id}/publish-logs \
  -H "Content-Type: application/json" \
  -d '{"platform":"zhihu","stage":"publishing","status":"in_progress","message":"正在注入内容"}'
```

### 4. 平台完成
```bash
# 更新平台状态
curl -s -X PUT http://localhost:3100/api/articles/{id} \
  -H "Content-Type: application/json" \
  -d '{"platform_status":{"zhihu":"published"}}'

# 记录成功日志
curl -s -X POST http://localhost:3100/api/articles/{id}/publish-logs \
  -H "Content-Type: application/json" \
  -d '{"platform":"zhihu","stage":"completed","status":"success","message":"知乎发布成功"}'
```

### 5. 平台失败
```bash
curl -s -X PUT http://localhost:3100/api/articles/{id} \
  -H "Content-Type: application/json" \
  -d '{"platform_status":{"toutiao":"failed"}}'

curl -s -X POST http://localhost:3100/api/articles/{id}/publish-logs \
  -H "Content-Type: application/json" \
  -d '{"platform":"toutiao","stage":"completed","status":"failed","error_code":"CAPTCHA_BLOCKED","message":"验证码拦截","retry_count":3}'
```

### 6. 全部完成
```bash
curl -s -X PUT http://localhost:3100/api/articles/{id} \
  -H "Content-Type: application/json" \
  -d '{"status":"published"}'
```

## 平台字段对照
zhihu, jianshu, segmentfault, devto, baijiahao, juejin, csdn, sohu, wechat_mp, medium, oschina, toutiao, linkedin, hashnode, github, hackernoon, aliyun_dev, tencent_dev, substack

## publish-logs 字段
- `platform`: 平台名（见上方对照）
- `stage`: `prepare` / `publishing` / `completed`
- `status`: `in_progress` / `success` / `failed`
- `message`: 人类可读描述
- `error_code`（失败时）: `CAPTCHA_BLOCKED` / `LOGIN_REQUIRED` / `BUTTON_BLOCKED` / `TIMEOUT` / `UNKNOWN`
- `retry_count`（失败时）: 已重试次数
