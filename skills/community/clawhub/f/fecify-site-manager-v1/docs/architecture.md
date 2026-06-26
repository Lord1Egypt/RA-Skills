# 架构与核心模块

## 目录结构

```
SKILL.md                    路由器（入口）
scripts/
  base/
    site-config.js          配置 / init 数据读写
    api-client.js           通用 HTTP 客户端（含插件校验）
    check-config.js         检测配置状态
    save-config.js          保存 URL+Token + 拉取 init
  init/
    get-addons.js           获取已安装插件列表
  proxy/
    api-call.js            通用 API 代理（exec 调用入口）
  csv-import/
    detect-shopify-csv.js  Shopify CSV 格式检测
    import-shopify-csv.js  Shopify CSV → Fecify 导入
sessions/                  所有 session 数据集中存储
  current_<SESSION>.txt    当前会话的域名绑定
  current_default.txt      默认会话域名绑定
  <domain>/
    config.json             { url, token, updatedAt }
    init-data.json          /api/skill/base/init 返回的 data
docs/
  architecture.md          本文件 — 架构与核心模块
  extending.md             扩展指南（新模块 / 新 CSV 格式）
  products.md              商品 API 汇总
  products/                商品各 API 详细文档
  base-image.md            图片 API 汇总
  base-images/             图片各 API 详细文档
  csv-import.md            CSV 批量导入指南
  orders.md                订单 API（待补充）
  coupons.md               优惠券 API（待补充）
temp/                      临时文件（dry-run 输出，可清理）
```

## api-client — 通用 HTTP 客户端

```js
const api = require('../base/api-client');
api.get(path)     // → { code, data, message }
api.post(path, body)
api.put(path, body)
api.del(path)
```

**路径校验**：`/api/xxxx/...` 直接请求；`/api/apps/{addon}/...` 先查 `init.data.addons` 是否存在。

**响应处理**：自动检测 JSON 解析失败，区分 HTML 异常（PHP ErrorException）和网络错误。

## site-config — 配置与数据读取

```js
const cfg = require('../base/site-config');
cfg.getCurrentConfig()    // → { url, token }
cfg.getCurrentInitData()  // → { data: { addons, ... }}
cfg.isConfigured()        // → boolean
cfg.hasInitData()         // → boolean
cfg.getConfig(domain)     // 跨站点读取
cfg.getInitData(domain)
```

## api-call — 通用 API 代理

所有 API 调用通过此入口，自动读取当前会话配置：

```
node scripts/proxy/api-call.js <METHOD> <PATH> [BODY_JSON]
```

必须带 `env: { FECIFY_SESSION: "<标识>" }`。
