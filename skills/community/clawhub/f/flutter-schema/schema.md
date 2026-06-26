# Flutter GetX 三层架构规范

**平台**：Flutter（Dart）  
**状态管理**：GetX  
**思路**：core / shared / modules 纵向分层，业务模块 GetX 化  
**适用**：中大型项目迭代，保持结构清晰、易于维护

---

## 一、架构总览

**三层纵向依赖**（自上而下）：

| 层级 | 说明 |
|------|------|
| **core** | 配置、路由、服务、工具、通用 UI |
| **shared** | 共享能力、存储、网络、业务基类 |
| **modules** | 业务功能实现，按功能拆模块 |

**依赖方向**：仅允许上层依赖下层（modules → core → shared）

```
shared（底）← core ← modules（顶）
```

**模块内 GetX 结构**：

```
Binding（注入） + View ← Logic → State
```

---

## 二、目录结构示例

```
lib/
├── main.dart
│
├── core/
│   ├── config/              # app_pages、app_routes、app_theme
│   ├── constants/           # 环境、多语言
│   ├── navigation/
│   ├── utils/
│   ├── services/            # 网络、存储、语言等
│   └── widgets/             # 空视图、弹窗、相机等通用组件
│
├── shared/
│   ├── data/
│   │   ├── base_business/   # 业务基类（BaseController、BasePage）
│   │   ├── local/           # 本地存储
│   │   ├── download/
│   │   ├── upload/
│   │   └── rest_client.dart
│   └── domain/              # 领域事件等
│
└── modules/
    ├── auth/
    │   ├── bindings/
    │   ├── controllers/
    │   ├── views/
    │   └── model/
    │
    ├── home/
    │   ├── home_page.dart
    │   ├── home_state.dart
    │   └── model/
    │
    ├── tabbar/
    │   ├── index_binding.dart
    │   └── index_view.dart
    │
    └── {module}/
        ├── {feature}/       # 子功能
        │   ├── xxx_binding.dart
        │   ├── xxx_logic.dart
        │   ├── xxx_state.dart
        │   ├── xxx_view.dart
        │   ├── model/
        │   └── view/
        ├── binding/
        ├── model/
        ├── view/
        ├── db/              # 可选
        └── upload/          # 可选
```

---

## 三、各层职责

### shared（最底层）

可被多个业务模块复用的基础能力：业务基类、本地存储、上传下载、API 封装等。

### core（中间层）

全局配置与通用能力：主题、路由、核心服务、通用 Widget、工具类。不包含业务逻辑。

### modules（最上层）

业务实现：按功能拆模块，模块间通过路由通信，不互相 import。

---

## 四、GetX 分层职责

| 角色 | 职责 |
|------|------|
| **Binding** | 依赖注入，注册 Controller，与路由绑定 |
| **Logic** | 业务逻辑入口，管理状态，调用数据层，不持有 BuildContext |
| **State** | 页面状态、列表数据、筛选条件等 |
| **View** | UI 渲染、事件响应，通过 GetView/Obx 监听 Logic |
| **Model** | 数据结构、实体/DTO |

---

## 五、目录与命名规范

- 一个页面/子功能 = 一个文件夹，含 binding、logic、state、view
- 文件/类名：`xxx_binding.dart` → `XxxBinding` 等
- 文件夹：小写下划线（如 order_list、user_profile）
- 视图类：以 `Page` 或 `View` 结尾，避免以 `widget` 结尾

---

## 六、依赖约束

- 上层可依赖下层，下层不可依赖上层
- 同级模块不互相 import，通过路由（Get.toNamed）通信
- Logic 不持有 BuildContext、不直接操作 UI

---

## 七、路由规范

- 路由统一在 `core/config/app_pages.dart`
- 路由常量在 `app_routes.dart`（part）
- 每个 GetPage 需指定 name、page、binding

---

## 八、开发约束（Code Review）

1. View 不写业务逻辑，逻辑放在 Logic
2. Logic 不持有 BuildContext、不操作 UI
3. 网络/数据库操作写在 Logic，通过 Repository 或 DB 调用
4. 业务模块之间不互相 import，通过路由跳转
5. 页面统一使用 GetX 结构（binding、logic、state、view）
6. 多页面拆分子模块，不堆在同一文件夹
7. 命名规范：小写下划线、大驼峰，避免拼音、缩写
8. Logic 继承项目内 BaseController 基类
9. 新建页面可用 create-file / create-list 的 validate.py 生成

---

## 九、页面生成脚本

- 普通页：`python ~/flutter-schema/scripts/validate.py <name> [dir]`

生成后需在 `app_pages.dart` 中手动添加路由。
