# 配置中心 Manager 模板

根据模块和作用名生成 XXXConfigManager 类。

## 模板

```kotlin
object {Name}ConfigManager {

    private const val CONFIG_KEY_CONFIG_VERSION = "1.0.0"
    private const val CONFIG_KEY_YZ_HD_{NAME}_CONFIG = "{componentKey}"
    private const val TAG = "{Name}ConfigManager"
    private const val CONFIG_KEY_YZ_HD_{NAME}_CONFIG_KEY = "{fieldKey}"
    private var {name}Config = {Name}Config({defaultValues})

    fun init() {
        ConfigCenter.init(Navigator.getApplication())
            .setConfigKey(CONFIG_KEY_YZ_HD_{NAME}_CONFIG, CONFIG_KEY_CONFIG_VERSION, "", SecurityKey.clientId, SecurityKey.clientSecret, null)
        try {
            val jsonObject = ConfigCenter.getInstance().getJsonObjectByKey(CONFIG_KEY_YZ_HD_{NAME}_CONFIG, CONFIG_KEY_YZ_HD_{NAME}_CONFIG_KEY)
            if (jsonObject != null) {
                {name}Config = GsonSingleton.getInstance().fromJson(jsonObject.toString(), {Name}Config::class.java)
            }
            Log.e(TAG, "获取 {Name} 配置成功 ${'$'}{name}Config")
        } catch (e: Exception) {
            Log.e(TAG, "获取 {Name} 配置失败 ${'$'}{e.message}")
        }
    }

    class {Name}Config(
        {constructorParams}
    ) {{
        override fun toString(): String {{
            return "{Name}Config({toStringParams})"
        }}
    }}
}}
```

## 使用说明

- `{Name}` - 配置名称（首字母大写），如 ANR
- `{name}` - 配置名称（小写），如 anr
- `{componentKey}` - 配置中心组件 Key
- `{fieldKey}` - 配置中心字段 Key
- `{defaultValues}` - 默认值，如果提供了模板 JSON 则从中提取
- `{constructorParams}` - 构造参数，从模板 JSON 提取字段生成
- `{toStringParams}` - toString 参数

## 示例：ANR 配置

```kotlin
object ANRConfigManager {

    private const val CONFIG_KEY_CONFIG_VERSION = "1.0.0"
    private const val CONFIG_KEY_YZ_HD_ANR_CONFIG = "com.youzan.retailHD.anr"
    private const val TAG = "ANRConfigManager"
    private const val CONFIG_KEY_YZ_HD_ANR_CONFIG_KEY = "config"
    private var anrConfig = ANRConfig(enable = false, enableKdtIds = listOf(), enableKdtIdSuffix = listOf(), disableX5 = false, disableX5KdtIdSuffix = listOf())

    fun init() {
        ConfigCenter.init(Navigator.getApplication())
            .setConfigKey(CONFIG_KEY_YZ_HD_ANR_CONFIG, CONFIG_KEY_CONFIG_VERSION, "", SecurityKey.clientId, SecurityKey.clientSecret, null)
        try {
            val jsonObject = ConfigCenter.getInstance().getJsonObjectByKey(CONFIG_KEY_YZ_HD_ANR_CONFIG, CONFIG_KEY_YZ_HD_ANR_CONFIG_KEY)
            if (jsonObject != null) {
                anrConfig = GsonSingleton.getInstance().fromJson(jsonObject.toString(), ANRConfig::class.java)
            }
            Log.e(TAG, "获取 ANR 配置成功 $anrConfig")
        } catch (e: Exception) {
            Log.e(TAG, "获取 ANR 配置失败 ${e.message}")
        }
    }

    class ANRConfig(
        val enable: Boolean = false,
        val enableKdtIds: List<String> = listOf(),
        val enableKdtIdSuffix: List<String> = listOf(),
        val disableX5: Boolean = false,
        val disableX5KdtIdSuffix: List<String> = listOf()
    ) {
        override fun toString(): String {
            return "ANRConfig(enable=$enable, enableKdtIds=$enableKdtIds, enableKdtIdSuffix=$enableKdtIdSuffix, disableX5=$disableX5, disableX5KdtIdSuffix=$disableX5KdtIdSuffix)"
        }
    }
}
```
