---
name: flutter-schema
tags: flutter, schema, getx, scaffold, template
description: Flutter GetX 三层架构规范。core + shared + modules 纵向分层，业务模块 GetX 化。适用于新模块创建、目录设计、代码评审。支持 scaffold 搭建目录结构。
---

# Flutter GetX 三层架构规范

## 架构概览

**纵向分层**（自上而下单向依赖，modules 依赖 core 和 shared）：

```
shared（底）← core ← modules（顶）
```

**模块内 GetX 结构**：

```
Binding（注入） + View ← Logic → State
```

## 层级速查

| 层级 | 职责 |
|------|------|
| **core** | 配置、路由、服务、工具、通用 UI 组件 |
| **shared** | 业务基类、存储、网络、可复用能力 |
| **modules** | 业务功能实现，按功能拆模块，模块间走路由 |

## 模块目录模板

```
{module}/
├── {feature}/                 # 子功能（可选）
│   ├── xxx_binding.dart
│   ├── xxx_logic.dart
│   ├── xxx_state.dart
│   ├── xxx_view.dart
│   ├── model/
│   └── view/
├── binding/
├── model/
├── view/
├── db/                        # 本地数据（可选）
└── upload/                    # 上传（可选）
```

## 命名约定

- binding / logic / state / view：`xxx_binding.dart` → `XxxBinding` 等
- logic 继承项目内 BaseController 基类
- 视图文件以 `_view` 结尾，类名以 `Page` 或 `View` 结尾
- 避免使用 `widget` 作为文件或类名后缀

## 依赖约束

- 仅允许上层依赖下层
- 同级模块不互相 import，通过路由（Get.toNamed）通信
- Logic 不持有 BuildContext、不直接操作 UI

## Scaffold 能力

用户要求**创建目录**、**搭建架构**、**新建模块**时：

**全量**：创建 core/config、constants、navigation、utils、services、widgets；shared/data、domain；modules/{name}

**增量**：在 modules 下新建 `{module_name}/`，可用 validate.py 生成页面骨架

模块名使用小写下划线（如 order_list、user_profile）。

## 页面生成

- 普通页：`python ~/flutter-schema/scripts/validate.py <name> [dir]`

完整说明见 [schema.md](schema.md)。
