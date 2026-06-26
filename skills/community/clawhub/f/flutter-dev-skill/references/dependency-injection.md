# Flutter 依赖注入指南

> 来源：Flutter 官方生态
> URL: https://pub.dev/packages/get_it
> 版本：Flutter 3.x
> 抓取时间：2026-04-24

---

## get_it（推荐）

```dart
import 'package:get_it/get_it.dart';

final getIt = GetIt.instance;

// 注册服务
void setupDependencies() {
  // 懒加载单例
  getIt.registerLazySingleton<Dio>(() => Dio());

  // 工厂：每次获取新实例
  getIt.registerFactory<UserRepository>(
    () => UserRepository(dio: getIt<Dio>()),
  );

  // 预注册实例
  getIt.registerSingleton<SharedPreferences>(prefs);
}

// 使用
final repo = getIt<UserRepository>();
```

## Riverpod + get_it 结合

```dart
// Riverpod 声明依赖 get_it
final dioProvider = Provider<Dio>((ref) => getIt<Dio>());
final userRepoProvider = Provider<UserRepository>(
  (ref) => UserRepository(dio: ref.watch(dioProvider)),
);

// 这样在 Provider 测试时可以单独 mock Dio 层
```

## injectable（代码生成）

```dart
// pubspec: injectable, injectable_generator, build_runner

// 声明式注入
@injectable
class AuthRepository {
  final Dio dio;
  AuthRepository({required this.dio});
}

// 注册（main.dart）
configureInjection();

@injectableInit
void main() {
  configureDependencies();
  runApp(MyApp());
}
```

## 常见 DI 陷阱

| 错误 | 正确 |
|------|------|
| ❌ 在 `build()` 中 `GetIt.instance<Dio>()` | ✅ 顶层 `setupDependencies()` 中注册 |
| ❌ 单例中引用非单例 | ✅ 确保生命周期一致 |
| ❌ 直接 `Dio()` 硬编码 | ✅ 通过 `getIt<Dio>()` 注入，便于测试时替换 mock |

## 来源

- [get_it | Pub](https://pub.dev/packages/get_it)
- [injectable | Pub](https://pub.dev/packages/injectable)
- [Riverpod DI 文档](https://riverpod.dev/docs/essentials/auto_dispose)
