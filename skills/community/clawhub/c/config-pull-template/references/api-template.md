# 单独接口 Manager 模板

根据模块和作用名生成 XXXConfigManager、XXXTask、XXXService。

## Manager 模板

```kotlin
object {Name}ConfigManager {

    private const val TAG = "{Name}ConfigManager"

    fun query{Name}Config() {
        {name}Task.query{Name}Config()
            .subscribe({
                save{Name}Config(it)
            }, { error ->
                Log.e(TAG, "拉取 {Name} 配置失败：${'$'}{error.message}")
            })
    }

    private fun save{Name}Config(response: {Name}Response) {
        // TODO 保存配置
    }
}
```

## Task 模板

```kotlin
public class {Name}Task {

    public Observable<{Name}Response> query{Name}Config() {
        return {name}Service.query{Name}Config(new {Name}Request());
    }
}
```

## Service 模板

```kotlin
public interface {Name}Service {
    @POST("{apiUrl}")
    Observable<{Name}Response> query{Name}Config(@Body {Name}Request request);
}
```

## 使用说明

- `{Name}` - 配置名称（首字母大写），如 ServiceFee
- `{name}` - 配置名称（小写），如 serviceFee
- `{apiUrl}` - 接口 URL，如 youzan.retail.trade.misc.shopsetting.query/1.0.0

## 示例

```kotlin
// Manager
object ServiceFeeConfigManager {

    private const val TAG = "ServiceFeeConfigManager"

    fun queryServiceFeeConfig() {
        saleTask.queryServiceFeeConfig()
            .subscribe({
                saveServiceFeeConfig(it.status)
            }, {
                Log.e(TAG, "拉取服务费配置失败：${it.message}")
            })
    }

    private fun saveServiceFeeConfig(status: Int) {
        // TODO 保存配置
    }
}

// Task
public class SaleTask {
    public Observable<ServiceFeeResponse> queryServiceFeeConfig() {
        return saleService.queryServiceFeeConfig(new ServiceFeeRequest());
    }
}

// Service
public interface SaleService {
    @POST("youzan.retail.trade.misc.shopsetting.query/1.0.0")
    Observable<ServiceFeeResponse> queryServiceFeeConfig(@Body ServiceFeeRequest request);
}
```
