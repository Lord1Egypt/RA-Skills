---
name: flutter-dev
description: >
  Flutter 跨平台移动开发技能。覆盖 Flutter 入门、Material 3 迁移、布局约束、动画
  （Hero/Staggered）、自适应响应式布局、平台适配、大型屏幕支持、State 管理方案对比、
  持久化、网络请求、性能优化。当用户提到 Flutter、Dart、移动开发、跨平台、Material Design、
  Flutter Widget、热重载、StatelessWidget、StatefulWidget、setState、Provider、Riverpod、
  BLoC、布局约束、BoxConstraints、动画、Animation、Hero、Staggered、响应式、自适应时触发。
trigger: Flutter|flutter|Dart|移动开发|跨平台|Material Design|Flutter Widget|热重载|Hot Reload|StatelessWidget|StatefulWidget|setState|BuildContext|InheritedWidget|Provider|Riverpod|BLoC|布局约束|BoxConstraints|动画|Animation|Hero|Staggered|响应式|自适应|adaptive|MediaQuery|LayoutBuilder|平台适配|SharedPreferences|Hive|Dio|性能优化|重绘|rebuild
tags:
  - flutter
  - dart
  - mobile-development
  - cross-platform
  - ui-design
hermes:
  platform: hermes
  version: "1.1"
  last_updated: "2026-04-24"
  source: |
    https://flutter.cn/docs
    https://flutter.cn/docs/release/breaking-changes/material-3-migration
    https://flutter.cn/docs/development/ui/layout/constraints
    https://flutter.cn/docs/development/ui/animations/hero-animations
    https://flutter.cn/docs/development/ui/animations/staggered-animations
---

# Widget 体系与 State 管理

## Widget 类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **StatelessWidget** | 不可变，props 决定 UI | `Text`, `Icon`, `Container` |
| **StatefulWidget** | 可变，通过 State 管理变化 | `Checkbox`, `TextField`, `Scaffold` |

## State 管理基础

```dart
class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  int _counter = 0;

  void _increment() {
    setState(() { _counter++; }); // 触发重建
  }
}
```

## BuildContext

每个 Widget 的 `build()` 方法接收 `BuildContext`。Context 包含：
- 当前 widget 在 widget 树中的位置
- 访问 `Theme.of(context)`、`MediaQuery.of(context)`
- 访问祖先 widget 提供的 `InheritedWidget`

---

# 布局约束

## 核心规则

> **"Constraints go down. Sizes go up. Parent sets position."**

父 widget 向下传递约束；子 widget 向上报告尺寸；父 widget 决定子 widget 的位置。

## BoxConstraints

| 类型 | 说明 | 场景 |
|------|------|------|
| **Tight** | `max == min`，固定尺寸 | `SizedBox(width: 100)` |
| **Loose** | `min == 0`，尺寸可变 | `Container()` 默认 |
| **Unbounded** | `max == double.infinity` | Scrollable、Flex 延伸方向 |

## 常用布局 Widget

| Widget | 用途 |
|--------|------|
| `Container` | 通用盒子 |
| `SizedBox` | 固定尺寸盒子 |
| `ConstrainedBox` | 施加额外约束 |
| `Padding` | 内边距 |
| `Row` / `Column` | 线性布局（Flex） |
| `Expanded` | 填充剩余空间 |
| `Flexible` | 类似 Expanded，可控制策略 |
| `Stack` | 绝对定位布局 |
| `Positioned` | Stack 中定位 |
| `LayoutBuilder` | 布局阶段获取约束 |

## 常见布局错误

```dart
// ❌ Expanded 在 Stack 中无效 → 用 Positioned 或 Align
// ❌ 在 unbounded 约束中 Expanded 无效 → 用 Slivers

// ✅ ConstrainedBox 在 Loose 约束内
ConstrainedBox(
  constraints: BoxConstraints(minWidth: 100, maxWidth: 200),
  child: Text('Hello'),
)
```

详细参考：[layout-constraints.md](references/layout-constraints.md)

---

# Material 3 迁移

## 核心开关

```dart
MaterialApp(
  theme: ThemeData(useMaterial3: true),
);
```

## 关键变化

| M2 | M3 |
|----|-----|
| `background` | `surface` |
| `primarySwatch` | `ColorScheme.fromSeed()` |
| `ButtonTheme` | `FilledButtonTheme` |
| `MaterialState` | `WidgetState` |
| `FlatButton` | `FilledButton` |

## 种子色

```dart
ColorScheme.fromSeed(seedColor: Colors.blue)
```

详细参考：[material-3.md](references/material-3.md)

---

# 动画系统

## Hero 动画

```dart
// 页面 A 和 B
Hero(
  tag: 'photo',
  child: Image.asset('photo.jpg'),
)
```

## Staggered 动画

```dart
// 一个控制器驱动多个 Interval 动画
Animation<double> get _opacity => Tween(begin: 0.0, end: 1.0).animate(
  CurvedAnimation(parent: _controller, curve: Interval(0.0, 0.5)),
);
Animation<double> get _scale => Tween(begin: 0.0, end: 1.0).animate(
  CurvedAnimation(parent: _controller, curve: Interval(0.5, 1.0)),
);
```

详细参考：[hero-animations.md](references/hero-animations.md) | [staggered-animations.md](references/staggered-animations.md)

---

# State 管理方案对比

## Provider（入门级）

```dart
// ChangeNotifier
class CounterModel extends ChangeNotifier {
  int _count = 0;
  int get count => _count;
  void increment() { _count++; notifyListeners(); }
}

// 注册
runApp(ChangeNotifierProvider(
  create: (_) => CounterModel(),
  child: MyApp(),
));

// 重建 UI
Consumer<CounterModel>(
  builder: (context, model, child) => Text('${model.count}'),
);

// 读取（不重建）
final count = context.read<CounterModel>().count;
```

## Riverpod（生产推荐）

```dart
// 纯 Dart，无 context 依赖
final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);
  void increment() => state++;
}

// 使用
Widget build(BuildContext context, WidgetRef ref) {
  final count = ref.watch(counterProvider);
  return Text('$count');
}

// ref.watch vs ref.read
// watch: 重建 UI（监听变化）
// read: 不重建，仅读取当前值（事件处理中常用）

// 强制刷新 Provider
ref.invalidate(counterProvider);  // 重置状态，重新执行 Provider 回调
// 或者基于现有状态刷新
ref.invalidate(myProvider);  // 下次访问时重新创建

// Family Provider（带参数）
final userProvider = Provider.family<User, String>((ref, id) {
  return User(id: id, name: 'User $id');
});
// 使用
final user = ref.watch(userProvider('abc'));
```

### Provider 作用域

```dart
// ✅ 顶层 Provider：全局单例
final prefsProvider = Provider<SharedPreferences>((ref) {
  return SharedPreferences.getInstance() as SharedPreferences;
});

// ✅ 作用域 Provider：仅在子树内有效
ProviderScope(
  overrides: [counterProvider.overrideWith(() => MockCounter())],
  child: MyApp(),
);

// ✅ Child Provider：可读取父 Provider
final userProvider = Provider((ref) {
  final prefs = ref.watch(prefsProvider); // 依赖父 Provider
  return UserRepo(prefs: prefs);
});
```

## BLoC（大型项目）

```dart
class CounterBloc extends Bloc<CounterEvent, int> {
  CounterBloc() : super(0) {
    on<Increment>((event, emit) => emit(state + 1));
  }
}

BlocBuilder<CounterBloc, int>(
  builder: (context, count) => Text('$count'),
)
```

## 方案选型

| 方案 | 复杂度 | 适用场景 |
|------|--------|---------|
| `setState` | 低 | 简单 widget |
| Provider | 中 | 中小型应用 |
| Riverpod | 中高 | **生产推荐** |
| BLoC | 高 | 团队协作/大型项目 |

---

# 持久化存储

## SharedPreferences（轻量配置）

```dart
final prefs = await SharedPreferences.getInstance();
await prefs.setString('username', 'yhong');
await prefs.setInt('counter', 42);
final name = prefs.getString('username') ?? '';
await prefs.remove('counter');
```

## SQLite（结构化数据）

```dart
final db = await openDatabase('myapp.db', version: 1,
  onCreate: (db, version) async {
    await db.execute(
      'CREATE TABLE tasks(id INTEGER PRIMARY KEY, title TEXT)');
  });

await db.insert('tasks', {'title': 'Finish report'});
final maps = await db.query('tasks', where: 'id = ?', whereArgs: [1]);

// 批量事务
await db.transaction((txn) async {
  for (final task in tasks) await txn.insert('tasks', task);
});
```

## Hive（高性能 KV）

```dart
Hive.registerAdapter(TaskAdapter());
final box = await Hive.openBox<Task>('tasks');
box.put('task1', Task(title: 'Hello'));
final task = box.get('task1');
```

---

# 网络请求

## Dio（推荐）

```dart
final dio = Dio(BaseOptions(
  baseUrl: 'https://api.example.com',
  connectTimeout: Duration(seconds: 10),
  headers: {'Content-Type': 'application/json'},
));

// 全局拦截器：Token 自动附加
dio.interceptors.add(InterceptorsWrapper(
  onRequest: (options, handler) {
    final token = getToken(); // 从安全存储读取
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  },
  onError: (error, handler) {
    // Token 过期自动刷新重试
    if (error.response?.statusCode == 401) {
      refreshToken().then((newToken) {
        // 重试原请求
        final opts = error.requestOptions;
        opts.headers['Authorization'] = 'Bearer $newToken';
        dio.fetch(opts).then(
          (r) => handler.resolve(r),
          (e) => handler.reject(e),
        );
      }).catchError((e) => handler.reject(error));
    } else {
      handler.next(error);
    }
  },
));

// GET / POST
final resp = await dio.get('/users', queryParameters: {'page': 1});
final resp = await dio.post('/users', data: {'name': 'yhong'});
```

### 统一响应体处理

```dart
// 常见后端响应格式：{ code, data, message }
class ApiResp<T> {
  final int code;
  final T? data;
  final String? message;

  bool get ok => code == 0;
}

// Dio 响应拦截器统一解析
dio.interceptors.add(InterceptorsWrapper(
  onResponse: (resp, handler) {
    final body = resp.data;
    if (body is Map && body.containsKey('code')) {
      if (body['code'] != 0) {
        // 业务错误，转为异常
        handler.reject(
          DioException(
            requestOptions: resp.requestOptions,
            error: body['message'] ?? 'Unknown error',
            type: DioExceptionType.badResponse,
          ),
        );
        return;
      }
      // 替换为 data 部分
      resp.data = body['data'];
    }
    handler.next(resp);
  },
));

// 使用时直接取 data
final List users = await dio.get('/users').then((r) => r.data);
```

### 错误处理

```dart
try {
  final resp = await dio.get('/users');
} on DioException catch (e) {
  switch (e.type) {
    case DioExceptionType.connectionTimeout:
      // 网络超时
    case DioExceptionType.badResponse:
      final statusCode = e.response?.statusCode;
      if (statusCode == 401) { /* 未授权 */ }
      if (statusCode == 403) { /* 禁止 */ }
      if (statusCode == 404) { /* 资源不存在 */ }
      if (statusCode != null && statusCode >= 500) { /* 服务器错误 */ }
    case DioExceptionType.cancel:
      // 请求被取消
    default:
      // 网络不可达等
  }
}
```

## JSON 解析

```dart
@JsonSerializable()
class User {
  final String name;
  final int age;
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

---

# 性能优化

## 重建控制

```dart
// ✅ Selector 精确重建（替代 Consumer）
Selector<Model, String>(
  selector: (_, m) => m.title,
  builder: (_, title, __) => Text(title),
);

// ✅ const 构造
const Text('Hello');
const Padding(padding: EdgeInsets.all(16));

// ❌ build 中创建新对象
Widget build(BuildContext context) {
  return SomeWidget(items: List.generate(100, (i) => Item(i))); // 每次重建
}

// ✅ initState 中初始化
final items = List.generate(100, (i) => Item(i));
```

## 长列表优化

```dart
// ✅ ListView.builder 懒加载
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ListTile(title: Text(items[index])),
);

// ✅ cacheExtent
ListView.builder(cacheExtent: 200, itemBuilder: ...);

// ✅ RepaintBoundary 隔离重绘
RepaintBoundary(child: MyComplexWidget());
```

---

# 响应式布局实战

## 自适应 Scaffold

```dart
class AdaptiveScaffold extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;

    if (width < 600) {
      return Scaffold(
        body: body,
        bottomNavigationBar: NavigationBar(
          selectedIndex: currentIndex,
          onDestinationSelected: onIndexChanged,
          destinations: _destinations,
        ),
      );
    }

    return Scaffold(
      body: Row(
        children: [
          NavigationRail(
            selectedIndex: currentIndex,
            onDestinationSelected: onIndexChanged,
            labelType: width > 840
                ? NavigationRailLabelType.all
                : NavigationRailLabelType.selected,
            destinations: _destinations
                .map((d) => NavigationRailDestination(
                      icon: d.icon,
                      label: d.label,
                    ))
                .toList(),
          ),
          const VerticalDivider(thickness: 1, width: 1),
          Expanded(child: body),
        ],
      ),
    );
  }
}
```

## 响应式列数

```dart
LayoutBuilder(
  builder: (context, constraints) {
    final cols = constraints.maxWidth > 900 ? 3
               : constraints.maxWidth > 600 ? 2
               : 1;
    return GridView.count(
      crossAxisCount: cols,
      childAspectRatio: 1.5,
      children: items.map((item) => Card(child: item)).toList(),
    );
  },
);
```

详细参考：[adaptive-responsive.md](references/adaptive-responsive.md) | [large-screens.md](references/large-screens.md)

---

# 平台适配

## 平台检测

```dart
final idiom = MediaQuery.of(context).size.shortestSide >= 600 ? 'tablet' : 'phone';
final platform = Theme.of(context).platform;
```

## 键盘快捷键

```dart
Shortcuts(
  shortcuts: {
    LogicalKeySet(LogicalKeyboardKey.control, LogicalKeyboardKey.keyS): SaveIntent(),
  },
  child: Actions(
    actions: { SaveIntent: CallbackAction(onInvoke: (_) => _save()) },
    child: focusNode,
  ),
)
```

## 鼠标 Hover

```dart
MouseRegion(
  onEnter: (_) => setState(() => _isHovered = true),
  onExit: (_) => setState(() => _isHovered = false),
  child: MyWidget(),
)
```

详细参考：[platform-idioms.md](references/platform-idioms.md)

---

# 避坑指南

### State 管理

| 错误 | 正确 |
|------|------|
| ❌ 在 `build()` 中调用 `setState()` | ✅ 在回调中调用 |
| ❌ `initState()` 中直接使用 `context` | ✅ `didChangeDependencies()` |
| ❌ 大型对象放 State | ✅ `const` 构造函数 |

### 布局

| 错误 | 正确 |
|------|------|
| ❌ `Expanded` 在 `Stack` 中 | ✅ `Positioned`/`Align` |
| ❌ 硬编码尺寸 | ✅ `MediaQuery`/`LayoutBuilder` |

### M3 迁移

| 错误 | 正确 |
|------|------|
| ❌ `ButtonTheme` | ✅ `FilledButtonTheme` |
| ❌ `background`/`onBackground` | ✅ `surface`/`onSurface` |
| ❌ `MaterialState` | ✅ `WidgetState` |

---

# 快速参考

## 热重载 vs 热重启

| 操作 | 效果 |
|------|------|
| **R** (Hot Reload) | 保持 State，仅重建 Widget 树 |
| **Shift+R** (Hot Restart) | State 丢失，重新执行 `main()` |

## 常用 EdgeInsets

```dart
EdgeInsets.all(16.0)
EdgeInsets.symmetric(v: 8)
EdgeInsets.only(left: 16)
EdgeInsets.fromLTRB(4,8,4,8)
```

## AnimationController 生命周期

```dart
_controller = AnimationController(
  duration: Duration(milliseconds: 300),
  vsync: this,
);

@override
void dispose() {
  _controller.dispose();
  super.dispose();
}
```

## 组件速查

| 按钮 | 导航 | 容器 |
|------|------|------|
| `FilledButton` | `AppBar` | `Card` |
| `FilledButton.tonal` | `NavigationBar` | `Dialog` |
| `OutlinedButton` | `NavigationRail` | `SnackBar` |
| `TextButton` | `NavigationDrawer` | `BottomSheet` |

详细参考：[buttons-input.md](references/buttons-input.md) | [navigation-components.md](references/navigation-components.md) | [display-components.md](references/display-components.md)

---

## 来源

> 文档版本：Flutter 3.x + Material 3
> URL: https://flutter.cn/docs
> 抓取时间：2026-04-24

## 参考文档

| 文件 | 行数 | 覆盖内容 |
|------|------|---------|
| material-3.md | 767 | Material 3 迁移完整指南 |
| layout-constraints.md | 368 | 布局约束与约束传递机制 |
| overview-getting-started.md | 376 | Flutter 入门与平台能力 |
| buttons-input.md | 424 | 按钮与输入组件 |
| adaptive-responsive.md | 298 | 自适应响应式布局 |
| platform-idioms.md | 358 | 平台适配与设备类型 |
| large-screens.md | 264 | 大屏幕与折叠屏支持 |
| navigation-components.md | 350 | 导航组件 |
| display-components.md | 300 | 展示组件 |
| hero-animations.md | 239 | Hero 动画 |
| staggered-animations.md | 354 | 交错动画 |
| testing.md | 121 | 测试指南（单元/Widget/集成/Mock） |
| dependency-injection.md | 81 | 依赖注入（get_it/Riverpod/injectable） |

---

| testing.md | 参考文档：测试指南 |

## 单元测试（flutter_test）

> 详见 [testing.md](references/testing.md)（flutter_test / widget / integration / Mock）

```dart
class CounterModel extends ChangeNotifier {
  int _count = 0;
  int get count => _count;
  void increment() { _count++; notifyListeners(); }
}

test('CounterModel increments correctly', () {
  final model = CounterModel();
  expect(model.count, 0);
  model.increment();
  expect(model.count, 1);
});
```

## Widget 测试

```dart
testWidgets('CounterWidget displays count and increments', (tester) async {
  await tester.pumpWidget(MaterialApp(home: CounterWidget()));
  expect(find.text('0'), findsOneWidget);
  await tester.tap(find.byIcon(Icons.add));
  await tester.pump();
  expect(find.text('1'), findsOneWidget);
});
```

## Riverpod Provider 测试

```dart
testProvider('counterProvider increments', (override) async {
  await runProviderScope((ref) async {
    final counter = ref.watch(counterProvider);
    expect(counter, 0);
    ref.read(counterProvider.notifier).increment();
    expect(ref.watch(counterProvider), 1);
  }, overrides: []);
});
```

## 集成测试

```dart
setUpAll(() async { await FlutterDriver.connect(); });

test('app loads and shows home', () async {
  final driver = await FlutterDriver.connect();
  await driver.waitFor(find.byType('MyHomePage'));
  expect(find.text('Home'), findsOneWidget);
});
```

## Mock + mockito

```dart
@GenerateMocks([UserRepository])
void main() {
  late MockUserRepository mockRepo;
  setUp(() { mockRepo = MockUserRepository(); });

  test('loads user data', () async {
    when(mockRepo.getUser('123'))
        .thenAnswer((_) async => User(id: '123', name: 'Alice'));
    final user = await mockRepo.getUser('123');
    expect(user.name, 'Alice');
    verify(mockRepo.getUser('123')).called(1);
  });
}
```

---

## 依赖注入

> 详见 [dependency-injection.md](references/dependency-injection.md)（get_it / injectable / DI 陷阱）

```dart
import 'package:get_it/get_it.dart';
final getIt = GetIt.instance;

void setupDependencies() {
  getIt.registerLazySingleton<Dio>(() => Dio());
  getIt.registerFactory<UserRepository>(
    () => UserRepository(dio: getIt<Dio>()),
  );
  getIt.registerSingleton<SharedPreferences>(prefs);
}

final repo = getIt<UserRepository>();
```

## Riverpod + get_it

```dart
final dioProvider = Provider<Dio>((ref) => getIt<Dio>());
final userRepoProvider = Provider<UserRepository>(
  (ref) => UserRepository(dio: ref.watch(dioProvider)),
);
```

## injectable

```dart
@injectable
class AuthRepository {
  final Dio dio;
  AuthRepository({required this.dio});
}
// configureDependencies(); // 自动生成
```

## DI 陷阱

| 错误 | 正确 |
|------|------|
| ❌ 在 `build()` 中 `GetIt.instance<Dio>()` | ✅ 顶层 `setupDependencies()` 中注册 |
| ❌ 单例中引用非单例 | ✅ 确保生命周期一致 |
| ❌ 直接 `Dio()` 硬编码 | ✅ 通过 `getIt<Dio>()` 注入 |

---

## 输出格式规范

### 回复结构

1. **直接回答** — 一段简洁的话给出核心答案
2. **代码示例** — 提供完整的 Dart/Flutter 代码
3. **实现要点** — 关键步骤和注意事项
4. **避坑提醒** — 常见错误 + 正确做法

### 禁用格式

- ❌ 不要显式分层（避免"第一层/第二层/框架分析"等字眼）
- ❌ 不要长篇解释概念，要直接给出实现
- ❌ 不要只给代码片段，要给完整可运行的示例
- ✅ 输出应是一段干净的话 + 完整代码
