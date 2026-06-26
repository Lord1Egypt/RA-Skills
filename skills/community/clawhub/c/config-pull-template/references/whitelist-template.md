# 白名单 Manager 模板

根据模块和作用名生成白名单检查方法。

## 模板

```kotlin
object WhiteListManager {

    fun {methodName}() {
        WhiteListTask.isInWhiteList({key}).subscribe({ result ->
            // TODO 待实现
        }, { error ->
            // TODO 待实现
        })
    }
}
```

## 使用说明

- `{methodName}` - 方法名，根据配置作用命名，如 `isANREnabled`
- `{key}` - 白名单 Key

## 示例

```kotlin
object WhiteListManager {

    fun isANREnabled() {
        WhiteListTask.isInWhiteList("anr_feature").subscribe({ result ->
            // TODO 待实现
        }, { error ->
            // TODO 待实现
        })
    }
}
```
