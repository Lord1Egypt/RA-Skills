# eframe 框架快速开发技能（eframe-skills）

> 版本：v1.0 | 整理日期：2026-09-12

## 定位

从 linlan-eframe 框架（https://gitee.com/linlannet/linlan-eframe）提炼的快速开发技能，解决"在框架上新增业务模块并端到端跑通"的问题，聚焦快速开发；代码质量审查口径见仓库根目录 `references/`。

## 能力清单

- 新业务模块端到端开发流程（8步）
- 后端三层代码范式（model/view/api，含字典模块全链路示例）
- 读写分离 Entry/Op 约定与命名规范
- module-generator 代码生成器使用
- 前端 api + views 开发范式
- 关键注解与 BaseController 工具清单

## 文件结构

```
eframe-skills/
  SKILL.md                          技能主过程（分层总览/8步流程/范式/检查清单）
  README.md                         本文件
  references/
    backend-layers.md               后端三层完整代码范式（字典模块真实代码）
    frontend-pattern.md             前端 api + request + views 范式
```

## 框架分层速览

```
Controller(api) -> Service(view) -> Service(model) -> Dao(model)
net.linlan.frame.api.{域}    net.linlan.frame.view.{域}   net.linlan.sys.{域}
```

后端 10 个 Maven 模块，新增业务只落在 model / view / api 三层；前端 Vue3 + Element Plus + Ant Design Vue。

## 快速上手

1. 建表（字段全大写下划线，含标准字段）
2. model 层：entity(含init) + dto + param + dao + service
3. view 层：vo(静态DTO/INITO+transTo) + voParam(toModelParam)
4. api 层：Controller 继承 BaseController，加 @PreAuthorize + @PlatLog + @Encrypt
5. 前端：src/api/{域}/{实体}.js + src/views/{域}/{实体}/index.vue

完整代码范式见 `references/`，或直接用框架内置 module-generator 从库表一键生成。
