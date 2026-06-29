# 07_migration_engine — 迁移引擎规范

**层级：L1（执行层规格）**

---

## 一、迁移定义

迁移是系统在运行时从一种 State 版本过渡到另一种版本的过程。

```
Migration: (old_state, migration_steps) → new_state
```

## 二、迁移的三图分离

### 2.1 三张图

| 图名称 | 内容 | 用途 |
|-------|------|------|
| L0 依赖图 | core_essence 文件间的概念依赖关系 | 维护 L0 语义完整性 |
| L1 执行图 | reducer 之间的数据流方向 | 维护步序正确性 |
| 迁移 DAG | Block Store 的字段升级顺序 | 维护数据版本兼容 |

### 2.2 迁移 DAG 的构造约束

迁移 DAG 不是 runtime 执行模型。它是**施工顺序的排列关系**：

```
向现有 block 添加新字段：
  1. 在 DAG 中注册新字段
  2. 确定该字段的默认值
  3. 确定旧 block 到新 block 的转换规则
  4. 逐批执行迁移（不影响当前交互）
```

## 三、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| 具体迁移路径 | 05_migration_executor |
| Block Store 的 schema 版本管理 | L2 或 L3 区域 |
