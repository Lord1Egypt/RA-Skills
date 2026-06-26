## 覆盖范围

本篇聚焦 CloudCC 后端 Java 侧二开资产（通过 `cc` 命令）：

- 自定义类（Class）
- 定时类（Scheduled Class / Timer）
- 触发器（Trigger）

并给出“创建 → 拉取 → 编辑 → 发布”的闭环流程。

---

## 目录结构（以本仓库约定为准）

创建后通常会生成在以下目录（项目根下）：

- `classes/{ClassName}/...`
- `schedule/{ScheduleName}/...`
- `triggers/{objectName}/{triggerName}/...`

---

## 源码同步边界（必须理解）

该项目使用“片段同步”策略：

- **自定义类 / 定时类 / 触发器**：只会拉取/发布 `@SOURCE_CONTENT_START` 与 `@SOURCE_CONTENT_END` 之间的内容。

这意味着：

- 你可以在片段外保留模板、import、类结构等；真正可同步的业务逻辑写在片段内。
- 拉取会覆盖片段区域，因此片段内不要放本地专用逻辑（如临时调试代码）。

---

## 自定义类（Class）

### 创建

```bash
# 在项目根目录执行
cc create classes <ClassName>
```

### 拉取 / 发布（片段同步）

```bash
cc pull classes <ClassName>
cc publish classes <ClassName>
```

> 说明：发布/拉取只会处理 `@SOURCE_CONTENT_START` 与 `@SOURCE_CONTENT_END` 之间的代码片段。

---

## 定时类（Scheduled Class）

### 创建

```bash
# 在项目根目录执行
cc create schedule <ScheduleName>
cc pull schedule <ScheduleName>
cc publish schedule <ScheduleName>
```

---

## 触发器（Trigger）

### 创建（关键入参）

触发器的 CLI 创建参数是一个 JSON 对象（需要 `encodeURI` 后作为单参传入）：

```bash
cc create triggers <encodedJson>
```

JSON 字段（示例）：

- `name`: 触发器名（Java 命名规范）
- `schemetableName`: 对象表名（如从对象列表拿到）
- `targetObjectId`: 目标对象 ID
- `triggerTime`: 触发时机（beforeInsert/afterUpdate/.../approval 等）

示例（macOS/zsh，注意引号与编码）：

```bash
cc create triggers "$(node -e 'console.log(encodeURI(JSON.stringify({name:\"MyTrigger\",schemetableName:\"account\",targetObjectId:\"a01...\",triggerTime:\"beforeInsert\"})))')"
```

### 拉取 / 发布

```bash
# namePath 形如：objectName/triggerName（注意 objectName 通常为小写目录）
cc pull triggers <namePath>
cc publish triggers <namePath>
```

> 说明：发布/拉取只会处理 `@SOURCE_CONTENT_START` 与 `@SOURCE_CONTENT_END` 之间的代码片段。

---

## 推荐工作流（AI 执行顺序）

当需求涉及后端逻辑时，建议 AI 按以下顺序执行：

1. 通过对象/字段工具确认数据结构（必要时先建对象字段）
2. 创建类/触发器/定时器骨架（create_*）
3. 拉取线上版本（pull_*）对齐基线（如是增量改造）
4. 编写片段内业务逻辑（注意批量与幂等）
5. 发布（publish_*）
6. 回归验证：单条、批量、权限、异常分支

