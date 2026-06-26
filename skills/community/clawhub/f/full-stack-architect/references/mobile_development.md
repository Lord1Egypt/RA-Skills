# 移动开发最佳实践总结

> 整理日期：2026-05-25
> 归属：full-stack-architect技能

---

## 一、移动开发技术选型

### 1.1 原生 vs 跨平台

**原生开发：**
- **iOS**：Swift/Objective-C
- **Android**：Kotlin/Java
- **优势**：性能最佳、原生体验、完整API访问
- **劣势**：开发成本高、代码复用低

**跨平台开发：**
- **React Native**：JavaScript/TypeScript
- **Flutter**：Dart
- **Ionic**：Web技术
- **优势**：代码复用、开发效率高、统一UI
- **劣势**：性能略逊、平台特性访问受限

**选型建议：**
- 性能要求高 → 原生
- 快速开发 → 跨平台
- 预算有限 → 跨平台
- 特定平台特性 → 原生

---

### 1.2 React Native vs Flutter

**React Native：**
- **语言**：JavaScript/TypeScript
- **生态**：丰富的第三方库
- **热更新**：支持
- **学习曲线**：较低（Web开发者）
- **性能**：良好

**Flutter：**
- **语言**：Dart
- **生态**：快速增长
- **热更新**：需要插件
- **学习曲线**：中等
- **性能**：优秀（自绘UI）

**选择因素：**
- 团队技术栈
- 性能要求
- 生态需求
- 开发效率

---

## 二、React Native 最佳实践

### 2.1 项目结构

**推荐结构：**

```
project/
├── src/
│   ├── components/      # 可复用组件
│   ├── screens/        # 页面
│   ├── navigation/     # 导航
│   ├── services/       # API服务
│   ├── utils/          # 工具函数
│   ├── hooks/          # 自定义Hooks
│   ├── context/        # 全局状态
│   └── assets/         # 静态资源
├── App.js              # 入口文件
├── package.json
└── .gitignore
```

**命名规范：**
- 组件：PascalCase（Button.js）
- 文件：kebab-case（user-profile.js）
- 变量：camelCase
- 常量：UPPERCASE

---

### 2.2 性能优化

**列表优化：**

```javascript
// 使用FlatList而不是ScrollView
import { FlatList } from 'react-native';

const UserList = ({ users }) => {
  const renderItem = ({ item }) => (
    <UserItem user={item} />
  );

  return (
    <FlatList
      data={users}
      renderItem={renderItem}
      keyExtractor={item => item.id}
      initialNumToRender={10}
      maxToRenderPerBatch={5}
      windowSize={10}
      removeClippedSubviews={true}
    />
  );
};
```

**内存管理：**
- 避免内存泄漏
- 正确清理定时器和事件监听器
- 使用`useEffect`清理函数

**图片优化：**
- 使用适当尺寸的图片
- 图片懒加载
- 缓存策略

---

### 2.3 状态管理

**选项：**
- **Context API**：简单状态
- **Redux**：复杂状态
- **MobX**：响应式状态
- **Zustand**：轻量级状态

**Redux 示例：**

```javascript
// store.js
import { configureStore } from '@reduxjs/toolkit';
import userReducer from './slices/userSlice';

export const store = configureStore({
  reducer: {
    user: userReducer
  }
});

// userSlice.js
import { createSlice } from '@reduxjs/toolkit';

export const userSlice = createSlice({
  name: 'user',
  initialState: {
    user: null,
    loading: false
  },
  reducers: {
    setUser: (state, action) => {
      state.user = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    }
  }
});

export const { setUser, setLoading } = userSlice.actions;

export default userSlice.reducer;
```

---

### 2.4 导航

**React Navigation：**

```javascript
// navigation/AppNavigator.js
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

const Stack = createStackNavigator();

const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen 
          name="Home" 
          component={HomeScreen} 
          options={{ title: 'Home' }} 
        />
        <Stack.Screen 
          name="Profile" 
          component={ProfileScreen} 
          options={{ title: 'Profile' }} 
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
```

**导航类型：**
- Stack Navigation：页面堆栈
- Tab Navigation：标签页
- Drawer Navigation：抽屉菜单
- Bottom Tabs：底部标签

---

### 2.5 网络请求

**使用Axios：**

```javascript
// services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // 处理认证错误
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

### 2.6 原生模块集成

**创建原生模块：**

```java
// Android模块
public class MyNativeModule extends ReactContextBaseJavaModule {
  public MyNativeModule(ReactApplicationContext reactContext) {
    super(reactContext);
  }

  @Override
  public String getName() {
    return "MyNativeModule";
  }

  @ReactMethod
  public void showToast(String message) {
    Toast.makeText(getReactApplicationContext(), message, Toast.LENGTH_SHORT).show();
  }
}

// 注册模块
public class MyPackage implements ReactPackage {
  @Override
  public List<NativeModule> createNativeModules(ReactApplicationContext reactContext) {
    List<NativeModule> modules = new ArrayList<>();
    modules.add(new MyNativeModule(reactContext));
    return modules;
  }
}
```

**JavaScript端使用：**

```javascript
import { NativeModules } from 'react-native';

const { MyNativeModule } = NativeModules;

// 使用
MyNativeModule.showToast('Hello from React Native!');
```

---

## 三、Flutter 最佳实践

### 3.1 项目结构

**推荐结构：**

```
lib/
├── main.dart              # 入口文件
├── screens/              # 页面
│   ├── home_screen.dart
│   └── profile_screen.dart
├── widgets/              # 可复用组件
├── services/             # API服务
├── models/               # 数据模型
├── providers/            # 状态管理
├── routes/               # 路由
├── utils/                # 工具函数
└── assets/               # 静态资源
```

**命名规范：**
- 文件：snake_case（user_profile.dart）
- 类：PascalCase（UserProfile）
- 变量：camelCase
- 常量：UPPERCASE

---

### 3.2 状态管理

**选项：**
- **setState**：简单状态
- **Provider**：轻量级状态
- **Bloc**：复杂状态
- **Riverpod**：新一代状态管理

**Provider 示例：**

```dart
// providers/user_provider.dart
import 'package:flutter/material.dart';

class UserProvider extends ChangeNotifier {
  String _name = '';
  bool _isLoading = false;

  String get name => _name;
  bool get isLoading => _isLoading;

  void setName(String name) {
    _name = name;
    notifyListeners();
  }

  void setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  Future<void> fetchUser() async {
    setLoading(true);
    // 模拟网络请求
    await Future.delayed(Duration(seconds: 2));
    setName('John Doe');
    setLoading(false);
  }
}

// 使用
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => UserProvider(),
      child: MyApp(),
    ),
  );
}

// 在组件中使用
class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final userProvider = Provider.of<UserProvider>(context);
    
    return Scaffold(
      body: Center(
        child: userProvider.isLoading
            ? CircularProgressIndicator()
            : Text('Hello, ${userProvider.name}'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => userProvider.fetchUser(),
        child: Icon(Icons.refresh),
      ),
    );
  }
}
```

---

### 3.3 布局与UI

**响应式布局：**

```dart
class ResponsiveLayout extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth > 600) {
          // 平板布局
          return TabletLayout();
        } else {
          // 手机布局
          return MobileLayout();
        }
      },
    );
  }
}
```

**主题管理：**

```dart
class AppTheme {
  static ThemeData lightTheme = ThemeData(
    primaryColor: Colors.blue,
    brightness: Brightness.light,
    scaffoldBackgroundColor: Colors.white,
  );

  static ThemeData darkTheme = ThemeData(
    primaryColor: Colors.blue,
    brightness: Brightness.dark,
    scaffoldBackgroundColor: Colors.black,
  );
}

// 使用
void main() {
  runApp(
    MaterialApp(
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      home: HomeScreen(),
    ),
  );
}
```

---

### 3.4 网络请求

**使用Dio：**

```dart
// services/api_service.dart
import 'package:dio/dio.dart';

class ApiService {
  static final Dio _dio = Dio(
    BaseOptions(
      baseUrl: 'https://api.example.com',
      connectTimeout: 10000,
      receiveTimeout: 10000,
    ),
  )..interceptors.add(LogInterceptor());

  static Future<Response> get(String path, {Map<String, dynamic>? queryParameters}) {
    return _dio.get(path, queryParameters: queryParameters);
  }

  static Future<Response> post(String path, {dynamic data}) {
    return _dio.post(path, data: data);
  }
}

// 使用
Future<void> fetchUsers() async {
  try {
    final response = await ApiService.get('/users');
    final users = response.data;
    // 处理数据
  } catch (e) {
    // 处理错误
  }
}
```

---

### 3.5 导航

**Flutter Navigation 2.0：**

```dart
// routes/app_router.dart
import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'screens/profile_screen.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(builder: (_) => HomeScreen());
      case '/profile':
        final args = settings.arguments as Map<String, dynamic>;
        return MaterialPageRoute(
          builder: (_) => ProfileScreen(userId: args['userId']),
        );
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(
              child: Text('Page not found'),
            ),
          ),
        );
    }
  }
}

// 使用
void main() {
  runApp(
    MaterialApp(
      initialRoute: '/',
      onGenerateRoute: AppRouter.generateRoute,
    ),
  );
}

// 导航
Navigator.pushNamed(context, '/profile', arguments: {'userId': '123'});
```

---

### 3.6 性能优化

**构建优化：**
- 使用`const`构造器
- 避免在build方法中创建对象
- 使用`ListView.builder`处理长列表
- 合理使用`const`和`final`

**示例：**

```dart
// 优化前
Widget build(BuildContext context) {
  return Container(
    child: Text('Hello', style: TextStyle(fontSize: 16)),
  );
}

// 优化后
const TextStyle _textStyle = TextStyle(fontSize: 16);

Widget build(BuildContext context) {
  return const Text('Hello', style: _textStyle);
}
```

**列表优化：**

```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListItem(item: items[index]);
  },
  cacheExtent: 20.0, // 预加载
  addAutomaticKeepAlives: true, // 保持活跃
);
```

---

## 四、移动应用安全

### 4.1 安全最佳实践

**数据安全：**
- 加密存储敏感数据
- 使用Keychain（iOS）或Keystore（Android）
- 避免硬编码敏感信息
- 安全的网络传输（HTTPS）

**React Native 安全存储：**

```javascript
import * as SecureStore from 'expo-secure-store';

// 存储
await SecureStore.setItemAsync('userToken', token);

// 读取
const token = await SecureStore.getItemAsync('userToken');

// 删除
await SecureStore.deleteItemAsync('userToken');
```

**Flutter 安全存储：**

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

final storage = FlutterSecureStorage();

// 存储
await storage.write(key: 'userToken', value: token);

// 读取
final token = await storage.read(key: 'userToken');

// 删除
await storage.delete(key: 'userToken');
```

---

### 4.2 网络安全

**SSL Pinning：**

**React Native：**

```javascript
import { NetworkSecurity } from 'react-native-network-security';

// 设置SSL Pinning
NetworkSecurity.setSSLPinning({
  certs: [{
    domain: 'api.example.com',
    cert: 'base64 encoded cert'
  }]
});
```

**Flutter：**

```dart
import 'package:http/http.dart' as http;

class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback = (X509Certificate cert, String host, int port) {
        // 验证证书
        return cert.pem == expectedCert;
      };
  }
}

// 启用
HttpOverrides.global = MyHttpOverrides();
```

---

## 五、移动应用测试

### 5.1 测试策略

**测试类型：**
- **单元测试**：测试单独的函数或类
- **集成测试**：测试组件和服务的交互
- **端到端测试**：测试整个应用流程

**React Native 测试：**

```javascript
// 单元测试
import { render, screen, fireEvent } from '@testing-library/react-native';
import LoginScreen from '../screens/LoginScreen';

describe('LoginScreen', () => {
  test('should render login form', () => {
    render(<LoginScreen />);
    expect(screen.getByPlaceholderText('Email')).toBeTruthy();
    expect(screen.getByPlaceholderText('Password')).toBeTruthy();
  });

  test('should call onLogin when form is submitted', () => {
    const onLogin = jest.fn();
    render(<LoginScreen onLogin={onLogin} />);
    
    fireEvent.changeText(
      screen.getByPlaceholderText('Email'),
      'test@example.com'
    );
    fireEvent.changeText(
      screen.getByPlaceholderText('Password'),
      'password123'
    );
    fireEvent.press(screen.getByText('Login'));
    
    expect(onLogin).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });
});
```

**Flutter 测试：**

```dart
// 单元测试
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/models/user.dart';

void main() {
  test('User model should create correctly', () {
    final user = User(id: '1', name: 'John', email: 'john@example.com');
    
    expect(user.id, '1');
    expect(user.name, 'John');
    expect(user.email, 'john@example.com');
  });
}

// 部件测试
void main() {
  testWidgets('Login form should render', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: LoginScreen()));
    
    expect(find.text('Email'), findsOneWidget);
    expect(find.text('Password'), findsOneWidget);
    expect(find.text('Login'), findsOneWidget);
  });
}
```

---

## 六、移动应用部署

### 6.1 iOS 部署

**App Store发布流程：**
1. 注册Apple Developer Account
2. 创建App ID
3. 配置证书和配置文件
4. 构建应用
5. 提交到App Store Connect
6. 应用审核
7. 发布

**构建命令：**

```bash
# React Native
npx react-native run-ios --configuration Release

# Flutter
flutter build ios --release
```

### 6.2 Android 部署

**Google Play发布流程：**
1. 注册Google Play Developer Account
2. 创建应用
3. 配置应用信息
4. 构建应用
5. 提交到Google Play Console
6. 应用审核
7. 发布

**构建命令：**

```bash
# React Native
npx react-native run-android --variant=release

# Flutter
flutter build apk --release
```

### 6.3 持续集成

**GitHub Actions 示例：**

```yaml
name: Mobile CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 16
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test

  build-android:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 16
      - name: Install dependencies
        run: npm install
      - name: Build Android
        run: npx react-native run-android --variant=release

  build-ios:
    needs: test
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 16
      - name: Install dependencies
        run: npm install
      - name: Build iOS
        run: npx react-native run-ios --configuration Release
```

---

## 七、常见问题与解决方案

### 7.1 性能问题

**问题：** 应用卡顿
**解决方案：**
- 优化渲染性能
- 使用`shouldComponentUpdate`或`PureComponent`
- 避免在render中创建对象
- 使用`FlatList`而非`ScrollView`

**问题：** 启动时间长
**解决方案：**
- 延迟加载非关键组件
- 使用React Native的`AppLoading`
- 优化资源加载

### 7.2 兼容性问题

**问题：** 不同设备显示不一致
**解决方案：**
- 使用响应式布局
- 测试不同尺寸设备
- 使用`Dimensions` API获取屏幕尺寸

**问题：** 平台特定功能
**解决方案：**
- 使用条件渲染
- 平台特定代码分离
- 原生模块集成

### 7.3 网络问题

**问题：** 网络请求失败
**解决方案：**
- 错误处理
- 重试机制
- 离线支持
- 网络状态监测

**问题：** 网络延迟
**解决方案：**
- 加载状态显示
- 缓存策略
- 预加载数据

---

## 八、最佳实践总结

1. **项目结构**：清晰的目录结构和命名规范
2. **性能优化**：列表优化、内存管理、构建优化
3. **状态管理**：选择合适的状态管理方案
4. **导航**：使用官方推荐的导航库
5. **网络请求**：统一的API服务和错误处理
6. **安全**：数据加密、SSL Pinning、安全存储
7. **测试**：单元测试、集成测试、端到端测试
8. **部署**：CI/CD集成、应用商店发布
9. **用户体验**：响应式布局、主题支持、加载状态
10. **维护性**：代码组织、文档、版本控制

---

## 相关资源

- [React Native 官方文档](https://reactnative.dev/docs/getting-started)
- [Flutter 官方文档](https://flutter.dev/docs)
- [React Navigation 文档](https://reactnavigation.org/docs/getting-started)
- [Flutter Navigation 文档](https://flutter.dev/docs/development/ui/navigation)
- [Expo 文档](https://docs.expo.dev/)
- [Dart 语言文档](https://dart.dev/guides)
- [App Store 审核指南](https://developer.apple.com/app-store/review/guidelines/)
- [Google Play 政策](https://play.google.com/about/developer-content-policy/)

