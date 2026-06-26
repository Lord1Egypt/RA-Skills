# 全局/页面级差异覆盖

当项目需要长期保持 UI 一致性时，用 `design-system/MASTER.md` 存放全局设计系统，用 `design-system/pages/<page>.md` 存放页面级差异。

## 读取顺序

1. 先检查当前页面是否有 `design-system/<project>/pages/<page>.md`。
2. 如果存在，页面文件里的规则覆盖 Master 中相同维度。
3. 如果不存在，完全遵循 `design-system/<project>/MASTER.md`。
4. 页面文件只记录差异，不复制 Master 全文。

## 生成命令

```bash
node skills/fec-ui-design/scripts/design-system.mjs "saas analytics dashboard" --project "Acme Console" --persist --output-dir .
```

生成页面 overrides：

```bash
node skills/fec-ui-design/scripts/design-system.mjs "saas analytics dashboard" --project "Acme Console" --page dashboard --persist --output-dir .
```

## 页面 override 应包含

- 页面任务和信息密度差异
- 布局差异：工作区、表格、图表、表单、详情页或营销首屏
- token 差异：只写需要覆盖的语义色、间距、状态或图表色
- 组件差异：只写当前页面新增或改变的组件行为
- QA 焦点：当前页面最容易出错的响应式、可访问性、性能或交互风险
