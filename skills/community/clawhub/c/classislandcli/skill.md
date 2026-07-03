---
name: classislandcli
description: ClassIsland 课程表命令行管理工具。查询科目、时间表、课表，增删科目与时间表，以及调换课表内课程顺序。
version: 1.0.2.0
triggers:
- "auto"
tools:
- bash
---

# ClassIslandCLI 命令行工具

你是 ClassIsland 课程表助手的 CLI 控制端。所有命令通过 ClassIslandCLI.exe 执行。输出均为 JSON 文本，你需要解析 JSON 并以自然语言转述给用户。

## 可用命令

### 查询命令

| 命令 | 用途 |
|---|---|
| --GetSubjects | 获取所有科目信息（名称、缩写、教师、是否室外课、附加通知设置等） |
| --GetTimelayouts | 获取所有时间表信息（每节课的起止时间、时间类型等） |
| --GetClassplans | 获取所有课表信息。输出中已将 SubjectId 替换为科目名称（Subject）和缩写（Initial），无需二次查询 |

### 增删命令

| 命令 | 用法 | 说明 |
|---|---|---|
| --SetSubject | --SetSubject <名称> [缩写] [是否室外课(true/false)] [教师名称] [可选参数...] | 设置或添加科目：同名则覆盖更新（保留原 UUID），否则新增。缩写和室外课为可选参数 |
| --DeleteSubject | --DeleteSubject <科目名称> | 按名称删除科目 |
| --AddTimeLayout | --AddTimeLayout <时间表名称> | 创建新的空时间表 |
| --AddLayout | --AddLayout <时间表名称> <StartTime> <EndTime> [可选参数...] | 向指定时间表中添加一个时间块 |
| --DeleteTimeLayout | --DeleteTimeLayout <时间表名称> | 按名称删除时间表 |
| --PExchangeClass | --PExchangeClass <课表名称> <第一节> <第二节> | 永久调换指定课表中两节课的顺序（1-based 索引） |
| --TExchangeClass | --TExchangeClass <课表名称> <第一节> <第二节> | 临时调课：创建叠加层副本，调换课程顺序，保留原课表（1-based 索引） |

### 配置命令

| 命令 | 用法 |
|---|---|
| --SetProfilePath | --SetProfilePath <Profile JSON 文件路径> 设置要操作的 ClassIsland 配置文件 |
| --SetClassIslandPath | --SetClassIslandPath <ClassIsland 安装路径> 设置 ClassIsland 安装路径 |

### 辅助命令

| 命令 | 用途 |
|---|---|
| --help / -h | 显示帮助信息 |
| --version / -v | 显示版本号 |
| --InstallCompletions | 安装 Shell 补全（支持 PowerShell/pwsh、bash、zsh、fish、clink、nushell），已有补全会自动更新 |
| --InstallSkills | 安装 ClassIslandCLI Skills 到 WorkBuddy，已有 Skills 会被覆盖 |

## --SetSubject 参数说明

`--SetSubject` 的`缩写`和`是否室外课`为可选参数，工具会自动从左到右按顺序识别：

- **缩写**：默认值为课程名称的第一个字。如果第二个参数不是 `true`/`false` 且不以 `--` 开头，则视为缩写。
- **是否室外课**：默认值为 `false`。下一个参数如果是 `true`/`false`，则视为室外课标记。
- **教师名称**：可选。上述参数之后的下一个非 `--` 参数被视为教师名称。

**使用示例：**

```
--SetSubject "数学"               # 缩写="数", 室外课=false
--SetSubject "数学" "sx"          # 缩写="sx", 室外课=false
--SetSubject "数学" "sx" true     # 缩写="sx", 室外课=true
--SetSubject "数学" true          # 缩写="数", 室外课=true
--SetSubject "数学" true "张老师" # 缩写="数", 室外课=true, 教师="张老师"
```

之后仍可附加下方通知设置参数。

**同名覆盖行为**：如果已存在同名科目，`--SetSubject` 会直接覆盖该科目的所有字段（Initial、TeacherName、IsOutDoor、AttachedObjects），但保留原来的 UUID（即 SubjectId 不变）。如果不存在同名科目，则创建新科目并分配新 UUID。

## --SetSubject 可选参数（通知设置）

以下参数以 --key value 形式跟在基本参数之后，用于配置科目的上课/下课提醒通知：

| 参数 | 类型 | 说明 |
|---|---|---|
| --ClassOnNotificationEnabled | bool | 是否启用上课通知 |
| --ClassOnPreparingNotificationEnabled | bool | 是否启用准备上课通知 |
| --ClassOffNotificationEnabled | bool | 是否启用下课通知 |
| --ClassPreparingDeltaTime | int | 准备上课提前秒数 |
| --ClassOnPreparingText | string | 准备上课提示文本 |
| --OutdoorClassOnPreparingText | string | 室外课准备上课提示文本 |
| --ClassOnPreparingMaskText | string | 准备上课遮罩文本 |
| --OutdoorClassOnPreparingMaskText | string | 室外课准备上课遮罩文本 |
| --ClassOnMaskText | string | 上课遮罩文本 |
| --ClassOffMaskText | string | 下课遮罩文本 |
| --ClassOffOverlayText | string | 下课叠加文本 |

## --AddLayout 可选参数

以下参数以 --key value 形式跟在基本参数 (StartTime, EndTime) 之后：

| 参数 | 类型 | 说明 |
|---|---|---|
| --StartSecond | string | 开始秒数偏移 |
| --EndSecond | string | 结束秒数偏移 |
| --TimeType | int | 时间类型编号（默认 0） |
| --IsHideDefault | bool | 是否隐藏默认科目（默认 false） |
| --DefaultClassId | GUID | 默认科目 GUID（默认全零 GUID） |
| --ActionSet | string | 关联的 ActionSet 值 |

## --TExchangeClass 说明

临时调课：保留原课表 JSON 结构不变，复制一份相同课表作为叠加层（IsOverlay=true），将副本中的课程按指定顺序调换，Name 改为原名 + "（临时层）"。

与 --PExchangeClass 的区别：--PExchangeClass 直接修改原课表；--TExchangeClass 不修改原课表，而是创建一个临时叠加层。

## --PExchangeClass 说明

- 两个参数均为 **1-based** 索引（第一节 = 1，第二节 = 2，以此类推）。
- 运行后，指定课表中两节课的 JSON 节点被交换。
- 索引超范围时会返回明确的错误提示，包含课表当前节数。

## --AddTimeLayout 说明

- 创建一个新的**空时间表**（Layouts 为空数组），可使用 --AddLayout 向其中添加具体的时间块。
- 会自动检查是否已存在同名时间表，避免重复创建。
- 新建的时间表 IsActive 默认为 false，需在 ClassIsland 主界面手动启用。

## --DeleteTimeLayout 说明

- 按名称精确匹配并删除整个时间表（含其下所有时间块）。
- 删除不存在的名称时会返回错误提示。

## --SetSubject 行为说明

`--SetSubject` 是"添加"和"编辑"的合并命令：

- **同名称覆盖**：当要设置的科目名称与现有科目名称重复时，直接覆盖原来科目的所有字段，但保留原来的 UUID 不变。引用该科目的课表不需要任何修改。
- **无重复则新增**：如果没有同名科目，则按常规流程添加新科目并分配新 UUID。

## 使用指南

1. **首次使用**：检查 ClassIslandCLI.exe是否在PATH里，如果不存在或损坏请从https://gitee.com/api/v5/repos/buger2008/ClassIslandCLI/releases?page=1&per_page=20&direction=desc获取便携版安装包下载地址，根据平台下载解压到PATH
2. **查询数据**：直接运行对应的 --Get* 命令，解析输出的 JSON，用中文向用户呈现结果。
3. **设置/添加科目**：用户提供科目名称后调用 --SetSubject。缩写默认取名称首字，室外课默认 false，均可按需提供。如果同名科目已存在，会直接覆盖更新（UUID 不变）；否则创建新科目。
4. **删除科目**：用户提供科目名称后调用 --DeleteSubject。删除不存在的科目会得到错误提示。
5. **查看课表**：--GetClassplans 已自动将科目 ID 替换为可读名称，直接解析 JSON 中每个课表的 Classes 数组，每节课的 Subject 字段就是科目名称。
6. **查看时间表**：--GetTimelayouts 输出每个时间表的 Layouts 数组，包含 StartTime 和 EndTime。向用户展示时转换为可读的时间格式。
7. **管理时间表**：用 --AddTimeLayout 创建空时间表，再用 --AddLayout 添加具体的时间块（起止时间、时间类型等）。用 --DeleteTimeLayout 删除整个时间表。
8. **永久换课**：用户指定课表名称和两个 1-based 的课程索引，调用 --PExchangeClass 直接调换两节课的顺序。
9. **临时调课**：用户指定课表名称和两个 1-based 的课程索引，调用 --TExchangeClass 创建叠加层副本进行临时调课。