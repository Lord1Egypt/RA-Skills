# 推拉结合 Manager 模板

根据模块和作用名生成配置管理器，包含推送通知注册逻辑。

## 模板

```kotlin
class {Name}RefreshUtils {

    companion object {
        private const val TAG = "{Name}RefreshUtils"
        private const val PUSH_KEY = "{pushKey}"
        private const val PULL_URL = "{pullUrl}"

        fun register{Name}Notification() {
            val notification = object : IConfigDataNotification {
                override val messagePushEventKey: String
                    get() = PUSH_KEY

                override val digestApiConfig: IDigestApiConfig
                    get() = object : IDigestApiConfig {
                        override val digestApiPath: String
                            get() = PULL_URL

                        override val digestApiParams: Map<String, Any>
                            get() = hashMapOf()

                        override val useBifrost: Boolean
                            get() = true

                        override val requestType: HttpType
                            get() = HttpType.POST
                    }

                override fun receivedDataNotificationCallback(data: IConfigData) {
                    when (data.notificationType) {
                        NotificationType.Pull -> {
                            val json = data.pushMessageData
                            if (!json.isNullOrEmpty()) {
                                runCatching {
                                    {Name}ConfigManager.save{Name}Config(
                                        GsonSingleton.getInstance().fromJson(json, {Name}Config::class.java)
                                    )
                                }
                            }
                        }
                        NotificationType.Push -> {
                            {Name}ConfigManager.query{Name}Config()
                        }
                    }
                }
            }

            MediatorServiceFactory.getInstance().get(IMessageCommonService::class.java)
                ?.registerNotification(notification)
        }
    }
}
```

## 使用说明

- `{Name}` - 配置名称（首字母大写），如 MemberPrice、Activity
- `{name}` - 配置名称（小写），如 memberPrice、activity
- `{pushKey}` - 推送 Key
- `{pullUrl}` - 拉取接口 URL

## 对应的 Manager 示例

```kotlin
object MemberPriceConfigManager {

    private const val TAG = "MemberPriceConfigManager"

    fun queryOfflineMemberPriceConfig() {
        // 拉取配置逻辑
    }

    fun saveActivityConfig(config: ActivityConfig) {
        // 保存配置逻辑
    }
}
```

## 完整示例

```kotlin
class ActivityRefreshUtils {

    companion object {
        private const val TAG = "ActivityRefreshUtils"
        private const val MARKETING_VALID_UPDATE = "marketing_valid_update"
        private const val GIFT_SETTING_UPDATE = "cashierPresentUpdated"
        private const val switchKey = "cashier_present_switch"
        private const val scopeKey = "cashier_present_goods_switch"
        private var supportActivityList: List<MarketingActivityType>? = null
        private var lastUpdateTime: Long = 0

        fun registerMemberPriceNotification() {
            val notification = object : IConfigDataNotification {
                override val messagePushEventKey: String
                    get() = "{KEY}"

                override val digestApiConfig: IDigestApiConfig
                    get() = object : IDigestApiConfig {
                        override val digestApiPath: String
                            get() = "{URL}"

                        override val digestApiParams: Map<String, Any>
                            get() = hashMapOf()

                        override val useBifrost: Boolean
                            get() = true

                        override val requestType: HttpType
                            get() = HttpType.POST
                    }

                override fun receivedDataNotificationCallback(data: IConfigData) {
                    when (data.notificationType) {
                        NotificationType.Pull -> {
                            val json = data.pushMessageData
                            if (!json.isNullOrEmpty()) {
                                runCatching {
                                    MemberPriceConfigManager.saveActivityConfig(
                                        GsonSingleton.getInstance().fromJson(json, ActivityConfig::class.java)
                                    )
                                }
                            }
                        }
                        NotificationType.Push -> {
                            MemberPriceConfigManager.queryOfflineMemberPriceConfig()
                        }
                    }
                }
            }

            MediatorServiceFactory.getInstance().get(IMessageCommonService::class.java)
                ?.registerNotification(notification)
        }
    }
}
```
