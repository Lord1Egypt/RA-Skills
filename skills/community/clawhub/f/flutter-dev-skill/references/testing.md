# Flutter 测试指南

> 来源：Flutter 官方文档 — Testing Flutter apps
> URL: https://flutter.cn/docs/testing
> 版本：Flutter 3.x
> 抓取时间：2026-04-24

---

## 单元测试（flutter_test）

```dart
// 待测试的业务代码
class CounterModel extends ChangeNotifier {
  int _count = 0;
  int get count => _count;
  void increment() { _count++; notifyListeners(); }
}

// 测试
test('CounterModel increments correctly', () {
  final model = CounterModel();
  expect(model.count, 0);

  model.increment();
  expect(model.count, 1);

  model.increment();
  expect(model.count, 2);
});
```

## Widget 测试

```dart
// 测试 StatefulWidget
testWidgets('CounterWidget displays count and increments', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: CounterWidget(), // 使用 CounterModel 的 Widget
    ),
  );

  expect(find.text('0'), findsOneWidget);
  expect(find.text('1'), findsNothing);

  await tester.tap(find.byIcon(Icons.add));
  await tester.pump();

  expect(find.text('1'), findsOneWidget);
});
```

## Riverpod Provider 测试

```dart
// 使用 ProviderScope 隔离测试
testProvider('counterProvider increments', (override) async {
  await runProviderScope((ref) async {
    final counter = ref.watch(counterProvider);
    expect(counter, 0);

    ref.read(counterProvider.notifier).increment();
    final newCounter = ref.watch(counterProvider);
    expect(newCounter, 1);
  }, overrides: []);
});
```

## 集成测试（flutter_driver）

```dart
// pubspec.yaml 添加 flutter_driver 依赖
// 测试文件
setUpAll(() async {
  await FlutterDriver.connect();
});

test('app loads and shows home', () async {
  final driver = await FlutterDriver.connect();
  await driver.waitFor(find.byType('MyHomePage'));
  expect(find.text('Home'), findsOneWidget);
});
```

## Mock 与依赖注入

```dart
// 使用 mockito 生成 mock
@GenerateMocks([UserRepository])
void main() {
  late MockUserRepository mockRepo;

  setUp(() {
    mockRepo = MockUserRepository();
  });

  test('loads user data', () async {
    when(mockRepo.getUser('123'))
        .thenAnswer((_) async => User(id: '123', name: 'Alice'));

    final user = await mockRepo.getUser('123');
    expect(user.name, 'Alice');
    verify(mockRepo.getUser('123')).called(1);
  });
}
```

## 测试金字塔

| 层级 | 工具 | 覆盖内容 |
|------|------|---------|
| 单元测试 | `flutter_test` | 纯 Dart 类、业务逻辑 |
| Widget 测试 | `flutter_test` | 单个 Widget 渲染和交互 |
| 集成测试 | `flutter_driver` / `integration_test` | 多 Widget 协作、真实环境 |

## 来源

- [Flutter 测试官方文档](https://flutter.cn/docs/testing)
- [Widget 测试指南](https://flutter.cn/docs/testing/widget-testing)
- [Riverpod 测试](https://riverpod.dev/docs/essentials/testing)
