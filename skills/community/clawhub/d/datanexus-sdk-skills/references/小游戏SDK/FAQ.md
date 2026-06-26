# 微信小游戏 SDK 常见问题（FAQ）

## Q1：SDK 是否可以在小程序中使用？

**不可以。** 小游戏 SDK 仅适用于微信小游戏环境。

---

## Q2：多数据源上报是否有上限？

**最多 4 个实例。**

---

## Q5：调用 track() 后无网络请求？

未设置 openid/unionid。

---

## Q6：START_APP 重复上报？

自动采集开启时不要手动调用 `sdk.onAppStart()`。

---

## Q7：data not valid 错误？

SDK 被混淆，将 SDK 排除在混淆范围外。CocosCreator 标记为插件，LayaAir 放 bin/libs/。

---

## Q8-Q10：51000 错误码

- Action Set Not Exist：检查 user_action_set_id
- SecretKey Error：检查密钥匹配
- 重复初始化：同一 ID 只创建一个实例

---

## Q11：IAA 小游戏质量看板

数据 T+1 更新。支持【复审】提交功能。

---

## Q12：如何确认数据上报成功？

`SDK.setDebug(true)` + Network `code: 0` + DataNexus 日志查询。
