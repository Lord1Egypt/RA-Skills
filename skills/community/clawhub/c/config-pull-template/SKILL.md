---
name: config-pull-template
description: |
  生成配置拉取代码模板。用于在 Android 项目中接入配置中心、白名单、单独接口或推拉结合的配置。
  触发条件：用户想要创建配置拉取功能，需要生成对应的 Kotlin/Java 代码模板。
---

# 配置拉取代码生成

根据用户提供的配置信息，生成对应的代码模板。

## 交互流程

### 第一步：询问配置作用

向用户确认：这个配置的作用是什么？
例如：ANR 监控配置、服务费配置、活动配置等。

### 第二步：确认接入方式

让用户选择接入方式：

1. **配置中心** - 需要提供：
   - 配置中心组件 Key（如 `com.youzan.retailHD.anr`）
   - 字段 Key（如 `config`）
   - 模板 Value（JSON 字符串，可选）

2. **白名单** - 需要提供：
   - 白名单 Key（如 `anr_feature`）

3. **单独接口** - 需要提供：
   - 接口 URL（如 `youzan.retail.trade.misc.shopsetting.query/1.0.0`）

4. **推拉结合** - 需要提供：
   - 推送 Key
   - 拉取接口 URL

### 第三步：确认所属模块

让用户选择配置所属模块：
- 商品模块（module_goods）
- 营销模块（module_marketing）
- 其他模块

## 代码生成规则

### 通用规则

- 代码优先使用 Kotlin 编写
- 数据模型如果跟网络相关需要添加 `@Keep` 注解
- **生成代码后，必须写入到 workspace 对应文件，并展示给用户看**

### 白名单接入

**生成 WhiteListManager**（如果已存在则复用）：

```kotlin
object WhiteListManager {

    fun is{Feature}Enabled() {
        WhiteListTask.isInWhiteList("{key}").subscribe({ result ->
            // TODO 待实现
        }, { error ->
            // TODO 待实现
        })
    }
}
```

**生成 Plugin 钩子**（方法名必须与注解名一致！）

在对应模块的 PluginModule 中添加三个方法：

```kotlin
// 文件位置：/modules/module_xxx/src/common/java/com/youzan/retail/xxx/PluginModule.kt

@ShopSwitched
fun onShopSwitched() {
    WhiteListManager.is{Feature}Enabled()
}

@AppStart
fun onAppStart() {
    WhiteListManager.is{Feature}Enabled()
}

@ConfigFetch
fun onConfigFetch() {
    WhiteListManager.is{Feature}Enabled()
}
```

### 配置中心

参考 [config-center-template.md](config-center-template.md)

根据模块 + 作用，在对应模块的 common 下创建 `XXXConfigManager` 类：
- 路径：`/modules/module_xxx/src/common/java/com/youzan/retail/xxx/`
- `CONFIG_KEY_CONFIG_VERSION` 固定为 `1.0.0`
- 如果提供了模板 JSON，需要生成对应的配置类（使用 `@Keep` 注解）

**同时生成 Plugin 钩子**（方法名必须与注解名一致！）：

```kotlin
@ShopSwitched
fun onShopSwitched() {
    {Name}ConfigManager.init()
}

@AppStart
fun onAppStart() {
    {Name}ConfigManager.init()
}

@ConfigFetch
fun onConfigFetch() {
    {Name}ConfigManager.init()
}
```

### 单独接口

参考 [api-template.md](api-template.md)

在对应模块的 common 下创建：
- `XXXConfigManager` - 业务逻辑
- `XXXTask` - Task 层
- `XXXService` - Service 接口（包含 @POST 注解和 URL）

**同时生成 Plugin 钩子**（方法名必须与注解名一致！）：

```kotlin
@ShopSwitched
fun onShopSwitched() {
    {Name}ConfigManager.query{Name}Config()
}

@AppStart
fun onAppStart() {
    {Name}ConfigManager.query{Name}Config()
}

@ConfigFetch
fun onConfigFetch() {
    {Name}ConfigManager.query{Name}Config()
}
```

### 推拉结合

参考 [push-pull-template.md](push-pull-template.md)

在对应模块的 common 下创建 `XXXRefreshUtils` 类，内部实现 `IConfigDataNotification` 接口注册推送通知。

**同时生成 Plugin 钩子**（方法名必须与注解名一致！）：

```kotlin
@ShopSwitched
fun onShopSwitched() {
    {Name}RefreshUtils.register{Name}Notification()
    {Name}ConfigManager.query{Name}Config()
}

@AppStart
fun onAppStart() {
    {Name}RefreshUtils.register{Name}Notification()
    {Name}ConfigManager.query{Name}Config()
}

@ConfigFetch
fun onConfigFetch() {
    {Name}ConfigManager.query{Name}Config()
}
```

## Plugin 钩子说明

配置拉取的调用时机通过 Plugin 实现。不同模块的 Plugin 位置：

- 商品模块：`modules/module_goods/src/common/java/com/youzan/retail/goods/PluginModule.kt`
- 营销模块：`modules/module_marketing/src/common/java/com/youzan/retail/marketing/PluginModule.kt`

可用的注解：
- `@ShopSwitched` - 店铺切换时调用
- `@AppStart` - 应用启动时调用
- `@ConfigFetch` - 配置同步时调用

**重要规则**：
1. 每次生成配置时，必须同时生成这三个 Plugin 钩子方法！
2. **方法名必须与注解名一致**：`@ShopSwitched` → `onShopSwitched()`，`@AppStart` → `onAppStart()`，`@ConfigFetch` → `onConfigFetch()`
3. 生成代码后，必须写入到 workspace 对应文件
