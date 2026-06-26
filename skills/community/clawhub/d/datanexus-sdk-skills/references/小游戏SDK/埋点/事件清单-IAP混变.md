# IAP / 混变小游戏 — 必报与选报事件

> 来源：[腾讯广告-小游戏 SDK 开发指引](https://doc.weixin.qq.com/doc/w3_ANYALQY-AEkzz9MDrwwS7KEbhTij7) §3.2.4.1
>
> ⚠️ `REGISTER` / `RE_ACTIVE` 的触发判断**必须由服务端完成**，详见 [数据正确性红线](../../通用/埋点/行为类型枚举表.md#️-数据正确性红线务必先看)。

## 必报事件

| action_type | 中文名 | 说明 |
|------------|--------|------|
| `START_APP` | 启动应用 | 用于广告效果优化。自动采集，开启自动采集后可不再手动上报 |
| `PURCHASE` | 付费 | 用于广告归因、广告效果优化。**必须传 `value`（单位：分）**，完整上报所有用户所有支付方式的全部付费行为 |
| `REGISTER` | 注册 | 用于广告归因、广告效果优化。⚠️ 必须等服务端返回 `isNew=true` 后调用 `sdk.onRegister()`，先 `setOpenId` 再 `onRegister`。**禁止**用 wx.storage 自判 |
| `RE_ACTIVE` | 沉默唤起 | 用于广告归因、广告效果优化。⚠️ 必须由服务端判断 `isReActive=true` 后调用，**禁止**客户端自判。建议周期 7/14/30 天，一个小游戏只需回传一个周期。如回流周期是永久可不上报 |
| `ADD_TO_WISHLIST` | 收藏小游戏 | 用于广告效果优化。包括普通收藏、添加到我的小程序、添加到桌面等。⚠️ SDK 自动采集仅用于数据校验，**客户仍需手动上报** |
| `SHARE` | 分享小游戏 | 用于广告效果优化。需区分【转发给朋友】和【分享到朋友圈】。⚠️ SDK 自动采集仅用于数据校验，**客户仍需手动上报** |

## 条件必报事件（无该行为可不报）

| action_type | 中文名 | 说明 |
|------------|--------|------|
| `CREATE_ROLE` | 创建角色 | 用于广告效果优化。无该行为可不报 |
| `TUTORIAL_FINISH` | 完成新手教程 | 用于广告效果优化。完成新手指引教程或教程关卡后上报。无该行为可不报 |

## 选报事件

| action_type | 中文名 | 说明 |
|------------|--------|------|
| `UPDATE_LEVEL` | 游戏等级提升 | 用于广告效果优化。可传当前等级、能量等参数 |
| `VIEW_CONTENT` | 浏览商城/活动 | 用于广告效果优化。浏览商城页面或活动页面时上报 |

## 专用上报方法

| 方法 | 参数 | 对应 action_type |
|------|------|-----------------|
| `sdk.onRegister()` | 无 | REGISTER |
| `sdk.onCreateRole(roleName)` | 角色名 | CREATE_ROLE |
| `sdk.onTutorialFinish()` | 无 | TUTORIAL_FINISH |
| `sdk.onPurchase(value)` | 金额（分） | PURCHASE |
| `sdk.onAddToWishlist()` | 无 | ADD_TO_WISHLIST |

> 专用方法不含业务参数，如需传参请使用通用方法 `sdk.track(action_type, action_param)`。
