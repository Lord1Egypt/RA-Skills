---
name: vue-style-checker
description: "检查 Vue 单文件组件（.vue）中的 CSS 样式规范问题并输出提示。用于用户提到样式规范检查、CSS 代码审查、Vue 页面样式质量巡检时。"
---

# Skill Instructions

## 适用场景
当用户希望检查 `.vue` 文件中的样式规范问题（如 `!important` 滥用、ID 选择器、非 kebab-case 类名、深度选择器、缺少 scoped）时，使用本技能。

---

## 一、快速检查流程

### 1) 执行样式巡检脚本
在项目根目录执行：

```bash
bash ./scripts/check-vue-style.sh
```

### 2) 理解输出结果
输出格式为：

```text
文件路径:行号: ⚠️ 问题说明
```

### 3) 修复后复查
修复完成后再次运行同一命令，直到没有警告为止。

---

## 二、当前规则（默认内置）
脚本会对每个 `.vue` 文件的 `<style>` 区块执行以下检查：

1. 检查是否缺少 `scoped`
2. 检查是否使用 `!important`
3. 检查是否使用 ID 选择器（如 `#app`）
4. 检查是否使用深度选择器（`/deep/`、`>>>`、`::v-deep`）
5. 检查类名是否为 kebab-case（如 `.user-card-title`）
6. 检查样式嵌套层级是否超过 3 层（粗略规则）

---

## 三、执行约定
1. 默认扫描当前目录下全部 `.vue` 文件。
2. 若脚本返回非 0，表示发现规范问题，需要提示并给出修复建议。
3. 如项目已有 Stylelint，可在此脚本基础上再补充团队规则。

---

## Resources
- `scripts/check-vue-style.sh`
