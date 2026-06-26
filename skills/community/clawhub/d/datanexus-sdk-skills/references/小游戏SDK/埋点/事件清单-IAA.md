# IAA 小游戏 — 必报与选报事件

> 来源：[腾讯广告-IAA微信小游戏采集行为列表](https://doc.weixin.qq.com/doc/w3_AE8AdwaBACcCNQJfr07c0QriMRK01)
>
> ⚠️ `REGISTER` / `RE_ACTIVE` 的触发判断**必须由服务端完成**，详见 [数据正确性红线](../../通用/埋点/行为类型枚举表.md#️-数据正确性红线务必先看)。

## 一、非游戏行为（必报）

| action_type | 中文名 | 说明 |
|------------|--------|------|
| `REGISTER` | 注册 | ⚠️ 服务端判断 isNew=true 后上报 |
| `RE_ACTIVE` | 沉默唤起 | ⚠️ 服务端判断 isReActive=true 后上报，建议周期 7/14/30 天 |
| `START_APP` | 启动应用 | 自动采集，开启自动采集后可不再手动上报 |
| `LOAD_FINISH` | 完成加载 | loading 页面完成，进入游戏第一帧上报 |
| `SHARE` | 分享 | 分享接口调用成功时上报。⚠️ SDK 自动采集仅用于数据校验，**客户仍需手动上报** |
| `ADD_TO_WISHLIST` | 添加收藏 | 包括普通收藏、添加到我的小程序、添加到桌面等。⚠️ SDK 自动采集仅用于数据校验，**客户仍需手动上报** |
| `SUBSCRIBE` | 订阅 | 玩家完成订阅操作，系统返回订阅成功时上报 |

## 二、新手引导行为（必报）

| action_type | 中文名 | 说明 |
|------------|--------|------|
| `TUTORIAL_START` | 新手引导开始 | 首次进入游戏触发第 1 关新手引导流程时上报。新手引导定义：有手势、文字、图形高亮的教学场景。无该行为可联系运营豁免 |
| `TUTORIAL_FINISH` | 完成新手教程 | 完成新手指引教程或教程关卡后上报。无该行为可联系运营豁免 |

## 三、主玩法行为（必报）

| action_type | 中文名 | 关键参数 | 说明 |
|------------|--------|---------|------|
| `LEVEL_ENTER` | 进入关卡 | `level_id`(必报), `chapter_id`, `enter_level_id`, `enter_level_name`, `game_mode`, `coin_amount`, `stamina_value`, `level_value` | 主玩法关卡场景开始渲染第一帧时上报 |
| `LEVEL_EXIT` | 中途退出关卡 | `level_id`(必报), `ad_cnt`(必报), `chapter_id`, `duration`, `items`, `enter_level_id`, `game_mode`, `coin_amount`, `stamina_value`, `level_value` | 中途退出（终止当下游戏进程）时上报。无该行为可联系运营豁免 |
| `LEVEL_LOSE` | 关卡失败 | `level_id`(必报), `ad_cnt`(必报), `chapter_id`, `duration`, `items`, `enter_level_id`, `game_mode`, `coin_amount`, `stamina_value`, `level_value` | 关卡失败时上报 |
| `LEVEL_PASS` | 通过关卡 | `level_id`(必报), `ad_cnt`(必报), `chapter_id`, `duration`, `items`, `enter_level_id`, `game_mode`, `coin_amount`, `stamina_value`, `level_value` | 关卡通关时上报 |

> 最小循环关卡：用户进入关卡后，每上报一次 `LEVEL_ENTER`，经历 `LEVEL_LOSE` / `LEVEL_EXIT` / `LEVEL_PASS` 任一事件，即为一个循环。

## 四、广告行为（必报）

| action_type | 中文名 | 说明 |
|------------|--------|------|
| `AD_PLACEMENT_SHOW` | 广告位展示 | 激励视频点位在界面中渲染完成（出现）时上报，发生在点击之前 |
| `AD_CLICK` | 广告位点击 | 玩家点击激励视频广告位按钮时上报 |
| `AD_VIDEO_FINISH` | 广告播放结束 | 激励视频完整播放完毕，显示"获得奖励"提示时上报 |
| `AD_IMPRESSION` | 广告曝光 | 插屏、横幅等非激励广告在界面中渲染完成、玩家可见时上报 |

## 五、周边行为（选报）

| action_type | 中文名 | 说明 |
|------------|--------|------|
| `HOMEPAGE_VIEW` | 外围页面浏览 | 游戏外围界面渲染完成时上报 |
| `CHECK_IN` | 点击签到 | 玩家点击"签到"按钮时上报 |
| `GIFT_GET` | 获取礼包 | 玩家点击"礼包"按钮时上报 |
| `RANKLIST_ENTER` | 点击排行榜 | 玩家点击排行榜入口时上报 |
| `GAMECLUB_ENTER` | 进入游戏圈 | 玩家点击游戏圈入口时上报 |
| `LOTTERY_CLICK` | 点击抽奖 | 玩家点击"抽奖"按钮时上报 |
| `MALL_CLICK` | 点击商店 | 玩家点击商店入口时上报 |
| `BUY_PROP` | 商店购买 | 完成支付流程、商品发放成功时上报 |
| `ENTER_CHALLENGE_MODE` | 点击挑战模式 | 玩家点击挑战模式入口时上报 |
| `THEME_CLICK` | 点击主题 | 玩家点击主题选项时上报 |
| `GET_ITEM` | 获取道具 | 玩家获得道具，显示结果提示时上报 |
| `USE_ITEM` | 使用道具 | 玩家使用道具，道具消耗且效果生效时上报 |

> ⚠️ IAA 小游戏发布前请务必在 DataNexus 日志查询中确认所有必报行为均已手动上报。发布后可在[质量看板](https://datanexus.qq.com/web/tool/quality-panel)（IAA 小游戏标签页）查看数据质量校验结果。

## 专用上报方法

| 方法 | 参数 | 对应 action_type |
|------|------|-----------------|
| `sdk.onRegister()` | 无 | REGISTER |
| `sdk.onCreateRole(roleName)` | 角色名 | CREATE_ROLE |
| `sdk.onTutorialFinish()` | 无 | TUTORIAL_FINISH |
| `sdk.onPurchase(value)` | 金额（分） | PURCHASE |
| `sdk.onAddToWishlist()` | 无 | ADD_TO_WISHLIST |

> 专用方法不含业务参数，如需传参请使用通用方法 `sdk.track(action_type, action_param)`。
