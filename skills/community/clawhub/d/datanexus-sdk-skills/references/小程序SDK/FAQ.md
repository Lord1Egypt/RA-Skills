# 微信小程序 SDK 常见问题

## Q1：SDK 是否可以在小游戏中使用？

**不可以。** 小程序 SDK 仅适用于微信小程序。

---

## Q2：多数据源上报是否有上限？

**最多 4 个实例。**

---

## Q3：user_action_set_id 是什么？

是数据源 ID，在 DataNexus 平台获取。

---

## Q5：调用 track() 后无网络请求？

未设置 openid/unionid。调用 `sdk.setOpenId(openid)` 设置。

---

## Q6：START_APP 重复上报？

自动采集开启时不要手动调用 `sdk.onAppStart()`。

---

## Q7：安全域名配置？

`https://api.datanexus.qq.com` 必须添加至 request 合法域名。

---

## Q8-Q10：51000 错误码

- Action Set Not Exist：检查 user_action_set_id
- SecretKey Error：检查密钥匹配
- 重复初始化：同一 ID 只创建一个实例

---

## Q11：如何确认数据上报成功？

`SDK.setDebug(true)` + Network 面板监控 `code: 0` + DataNexus 日志查询。
