---
name: flutter-hive-database
description: 在 Flutter 项目中封装 Hive 本地数据库服务，遵循 Repository 模式和 MVVM 架构。当用户需要使用 Hive 数据库、本地持久化存储、离线数据缓存、或提到 hive、本地数据库、数据持久化时使用。支持三种独立模式：创建数据服务、创建数据库操作、创建数据模型并自动注入 CRUD。
---

# Flutter Hive 数据库封装

## 存储策略

模型 → `toJson()` → `Box<Map>` → `fromJson()` → 模型

- 无需 TypeAdapter，无 ~200 个类型上限
- 无需 `build_runner`，依赖精简
- HiveService 懒加载 Box，新增模型无需修改 Service

## 目录结构

```
lib/
├── services/
│   ├── hive_service.dart          # 模式1：数据服务
│   └── hive_repository.dart       # 模式1：基类
└── <feature>/
    └── database/
        ├── <name>_repository.dart # 模式2：数据库操作
        └── models/
            └── <name>_model.dart  # 模式3：数据模型
```

---

## 三种触发模式

### 模式1：创建数据服务

**触发词**：「创建数据服务」「初始化 Hive」「配置 Hive」

**执行命令**：
```bash
python ~/.cursor/skills/flutter-hive-database/scripts/generate.py \
  --mode service \
  --project <项目根目录绝对路径>
```

生成文件：
- `lib/service/hive_service.dart` — 懒加载 Box 管理
- `lib/service/hive_repository.dart` — 通用 CRUD 基类

完成后在 `main.dart` 添加：
```dart
import 'package:<pkg>/service/hive_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await HiveService.init();
  runApp(const MyApp());
}
```

---

### 模式2：创建 xxx 数据库操作

**触发词**：「创建xxx数据库操作」「创建xxx的 Repository」

**执行前询问用户**：
> 请问功能模块的路径是什么？（如 `features/user` 或 `user`）
> Repository 的名称是什么？（PascalCase，如 `User`）

**执行命令**：
```bash
python ~/.cursor/skills/flutter-hive-database/scripts/generate.py \
  --mode repository \
  --project <项目根目录绝对路径> \
  --feature <lib下的功能路径> \
  --name <PascalCase名称>
```

**示例**：
```bash
python generate.py --mode repository \
  --project /Users/me/myapp \
  --feature features/user \
  --name User
```

生成文件：
- `lib/features/user/database/user_repository.dart` — 含原始 Map CRUD，等待模型注入

---

### 模式3：创建数据模型（并注入 CRUD）

**触发词**：「创建xxx数据模型」「提供 JSON 创建数据库模板」

**执行前询问用户**：
> 请提供实体的 JSON 数据或字段定义

**entity 参数格式**：
```json
{
  "name": "User",
  "fields": [
    {"name": "id",        "type": "int",      "nullable": false},
    {"name": "name",      "type": "String",   "nullable": false},
    {"name": "age",       "type": "int",      "nullable": true},
    {"name": "createdAt", "type": "DateTime", "nullable": false}
  ]
}
```

支持的 `type`：`int`、`double`、`String`、`bool`、`DateTime`、`List`、`Map`

**执行命令**：
```bash
python ~/.cursor/skills/flutter-hive-database/scripts/generate.py \
  --mode model \
  --project <项目根目录绝对路径> \
  --feature <lib下的功能路径> \
  --entity '<JSON字符串>'
```

**示例**：
```bash
python generate.py --mode model \
  --project /Users/me/myapp \
  --feature features/user \
  --entity '{"name":"User","fields":[{"name":"id","type":"int","nullable":false},{"name":"name","type":"String","nullable":false}]}'
```

生成 / 更新文件：
- `lib/features/user/database/models/user_model.dart` — 模型（含 toJson/fromJson/copyWith）
- `lib/features/user/database/user_repository.dart` — **自动注入** save/findById/getAll/update/deleteById 方法

> 如果 Repository 不存在，脚本会自动创建后再注入

---

## 依赖配置

```bash
flutter pub add hive_ce hive_ce_flutter
```

无需 `hive_ce_generator`，无需 `build_runner`

## 验证清单

- [ ] `HiveService.init()` 在 `runApp()` 之前调用
- [ ] UI 层只通过 Repository 操作数据，不直接调用 HiveService
- [ ] `fromJson` 中可选字段使用 `as Type?` 保证旧数据兼容

## 参考文件

- 完整生成逻辑参见 [scripts/generate.py](scripts/generate.py)
