## 覆盖范围

本篇聚焦用 `cloudcc-cli` 的 `cc` 命令完成：

- 创建自定义对象（Custom Object）
- 查询对象列表
- 查询对象字段
- 为对象创建字段（支持多字段类型）
-（可选）创建菜单、创建应用（把对象挂到导航中）

---

## 自定义对象（Custom Object）

### 你需要准备什么信息

- **对象显示标签（label）**：例如“客户”“合同”“付款计划”
- **项目路径（projectPath）**：模板项目根目录

### CLI 命令（项目已有实现）

```bash
cc create object <projectPath> <label>
```

示例：

```bash
cc create object . 客户
```

---

## 查询对象列表

### CLI 命令（输出 JSON）

```bash
# type 可选：standard / custom / both（默认：both）
cc get object <projectPath> [type]
```

示例：

```bash
cc get object . both
```

用途：

- 获取对象 `objprefix` / 对象 `id`（后续创建字段、触发器会用到）

---

## 查询对象字段列表

### CLI 命令（输出 JSON）

```bash
cc get fields <projectPath> <objprefix>
```

示例：

```bash
cc get fields . a01
```

用途：

- 在创建字段前，先确认是否已存在同名/同含义字段，避免重复与冲突。

---

## 创建字段（Field）

### CLI 命令形态（项目已有实现）

字段创建命令由工具根据字段类型拼装，典型形态：

```bash
cc create fields <projectPath> <fieldType> <objid> <nameLabel> [ptext|lookupObj]
```

### 字段类型选择建议（常用）

- **S**：文本（最常用）
- **N**：数字
- **D / F**：日期 / 日期时间
- **B**：复选框
- **L / Q**：选项列表（单选/多选）
- **Y / MR / M**：关系字段（查找/查找多选/主详）
- **E / H / U**：邮箱/电话/URL

---

## 菜单与应用（让对象可访问）

### 创建菜单（CLI）

```bash
cc create menu <type> <projectPath> <resourceId> <tabName> [tabStyle] [mobileimg] [cloudccservicetab]
```

示例：

```bash
cc create menu object . <objectId> "我的对象菜单"
```

### 创建应用（CLI）

```bash
cc create application <projectPath> <appName> <appCode> [menuIds]
```

说明：

- `menuIds`：可选，多个用逗号分隔；系统会确保默认菜单 `acf000001` 被包含。

