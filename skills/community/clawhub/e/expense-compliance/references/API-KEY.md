# API 密钥配置

推荐在平台创建通用 Key，并执行 `openclaw config set env.AI_SKILLS_API_KEY "你的平台APIKey"` 和 `openclaw gateway restart`，全平台 Skill 只需配置一次。仍需开通目标产品。下列 `EXPENSE_COMPLIANCE_API_KEY` 配置是兼容的产品专用覆盖项；调用优先使用该变量，为空时回退到 `AI_SKILLS_API_KEY`。两个变量均缺失时停止调用，不发送空 Bearer 请求。不要把旧请求换 Key 自动重试；幂等记录按 Key 隔离。


本 Skill 使用产品专属环境变量 `EXPENSE_COMPLIANCE_API_KEY`。通用 Key 可调用账号已开通的 API 产品，原产品专用 Key 只授权报销合规产品的 operation，不要写入命令参数、日志、报销材料或导出报告。

```sh
openclaw config set env.EXPENSE_COMPLIANCE_API_KEY "你的平台APIKey"
openclaw gateway restart
```

所有请求使用：

```http
Authorization: Bearer ais_...
```

密钥失效、撤销或产品未开通时停止请求并说明原因，不要改用其他产品密钥。
