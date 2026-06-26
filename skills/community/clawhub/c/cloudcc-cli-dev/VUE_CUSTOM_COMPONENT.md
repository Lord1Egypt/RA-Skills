## 覆盖范围

本篇聚焦 CloudCC Vue2.x 自定义组件（Custom Component）：

- 创建组件骨架
- 编辑与最佳实践入口
- 编译与发布到服务器

---

## 创建自定义组件

### CLI 命令

```bash
# 在项目根目录执行（会生成到 plugins/<pluginName>/）
cc create plugin <pluginName>
```

创建后会生成组件主文件、子组件目录与配置文件（以项目模板为准）。

---

## 发布组件

```bash
cc publish plugin <pluginName>
```

> 发布会执行编译/打包/上传；如果组件依赖复杂，注意依赖收集与发布策略。

---

## 编辑要点（CLI 项目约束）

- 组件目录通常为 `plugins/<pluginName>/`
- 确保所有 `<style>` 标签带 `scoped`，避免全局样式污染
- 发布通过 `cc publish plugin <pluginName>` 执行编译与上传

---

## 选型建议（组件 vs 客户端脚本）

- **自定义组件**：复杂交互、强 UI、可复用组件化、需要更完整工程化能力。
- **客户端脚本**：轻量联动、页面钩子逻辑、少量 UI 提示与校验。

一般建议：

- 先用脚本满足基础联动；当逻辑与 UI 复杂度上升时，再升级为组件方案。

