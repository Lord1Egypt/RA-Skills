---
name: android-unused-resource-cleanup
description: 分析 Android 项目 Git 改动，找出本次修改后不再使用的资源文件（drawable、layout、string、color 等），并检查这些资源是否还在项目其他位置被引用。当用户需要清理 Android 项目中因代码改动而变得无用的资源文件时使用此 skill。支持分析暂存区、工作区或历史提交的改动。
---

# Android 未使用资源清理

分析 Git 改动，智能识别因代码修改而变得不再使用的 Android 资源文件。

## 使用场景

- 替换了一个背景图/颜色/字符串后，旧资源不再使用
- 重构布局后，旧的 layout 文件未被删除
- 资源命名调整后，遗留下旧名称的资源文件
- 批量清理项目中无用的资源文件

## 工作原理

1. 获取 Git diff，分析代码改动中的资源引用变化
2. 识别被替换的资源（旧资源引用被删除，新资源引用被添加）
3. 在项目中搜索旧资源的引用情况
4. 如果旧资源不再被任何代码引用，标记为可安全删除

## 使用方法

### 命令行运行

```bash
# 分析暂存的改动（git add 后的内容）
python .agents/skills/android-unused-resource-cleanup/scripts/cleanup_unused_resources.py --source staged

# 分析未暂存的改动（工作区修改）
python .agents/skills/android-unused-resource-cleanup/scripts/cleanup_unused_resources.py --source unstaged

# 分析最近的一次提交
python .agents/skills/android-unused-resource-cleanup/scripts/cleanup_unused_resources.py --source HEAD~1
```

### 支持的资源类型

| 类型 | 示例 | 文件位置 |
|------|------|----------|
| drawable | `R.drawable.bg_main`, `@drawable/bg_main` | `res/drawable*/` |
| mipmap | `R.mipmap.ic_launcher` | `res/mipmap*/` |
| layout | `R.layout.activity_main` | `res/layout/` |
| string | `R.string.app_name`, `@string/app_name` | `res/values/` |
| color | `R.color.primary`, `@color/primary` | `res/values/` |
| dimen | `R.dimen.spacing`, `@dimen/spacing` | `res/values/` |
| style | `@style/AppTheme` | `res/values/` |
| anim | `@anim/fade_in` | `res/anim/` |
| raw | `R.raw.sound` | `res/raw/` |
| font | `@font/roboto` | `res/font/` |

## 示例输出

```
============================================================
Android 未使用资源分析报告
============================================================

[可删除] 可以安全删除的资源 (2 个):
------------------------------------------------------------

  [drawable] bg_old_main
    [文件] app/src/main/res/drawable/bg_old_main.xml

  [string] old_title
    [文件] app/src/main/res/values/strings.xml


[保留] 仍在使用，不能删除的资源 (1 个):
------------------------------------------------------------

  [color] primary_old
    [使用位置] 仍在以下位置使用:
       - app/src/main/res/layout/activity_settings.xml

============================================================

[删除建议]:
   del "app/src/main/res/drawable/bg_old_main.xml"
```

## 注意事项

1. **仅作为辅助工具**：脚本分析基于文本匹配，可能存在误判，删除前请人工确认
2. **动态引用无法检测**：通过字符串拼接动态生成的资源引用无法被检测
3. **反射调用无法检测**：通过反射获取的资源无法被检测
4. **跨模块引用**：如果资源被其他模块引用，可能无法正确检测
5. **建议操作**：
   - 先运行脚本获取可删除列表
   - 人工确认这些资源确实不再需要
   - 删除后编译项目验证无错误

## 实现细节

脚本通过以下方式识别资源引用：
- Java/Kotlin 代码: `R.type.name` 模式
- XML 文件: `@type/name` 模式

支持从以下位置获取改动：
- `staged`：`git diff --cached`
- `unstaged`：`git diff`
- `HEAD~N`：`git diff HEAD~N`
