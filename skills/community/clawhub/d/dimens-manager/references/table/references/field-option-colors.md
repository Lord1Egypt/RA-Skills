# dimens-manager 多维表格章节 选项字段颜色体系

## 1. 这份文档解决什么问题

这份文档专门解释：

- 单选字段 `select`
- 多选字段 `multiSelect`
- 各类下拉选择器 / 选项列表

在技能体系里应该如何表达颜色。

目标是让 Skill 输出与前端真实实现保持一致，避免出现下面这些问题：

- 只给 `label`，不写 `color`
- 颜色值协议写错，前端渲染不出来
- 不知道默认颜色和自定义颜色怎么区分
- 同一个系统里不同选项字段颜色风格完全失控

## 2. 当前前端真实实现口径

当前前端真实实现来自两个位置：

1. 多维表格字段配置
   - `web/src/components/mul-sheet/components/modals/constants.tsx`
   - `web/src/components/mul-sheet/components/modals/column-config/SelectConfig.tsx`
2. 字典管理页
   - `web/src/components/settings/DictionaryManagement.tsx`

真实结论：

- 内置颜色使用 Tailwind 类名组合：`bg-xxx-100 text-xxx-700`
- 自定义颜色使用字符串协议：`custom:{"bg":"#xxxxxx","text":"#xxxxxx"}`
- 前端会直接识别上面两类格式，不要发明第三种格式
- `dimens-cli` 当前应与前端真实字段配置保持一致：CLI 内置色白名单按前端 12 色池校验，自定义色按 `custom:` 协议校验

## 3. 默认内置颜色池

当前多维表格字段配置里的内置颜色池是 12 个：

| 标签 | color 字符串 |
| --- | --- |
| 灰色 | `bg-slate-100 text-slate-700` |
| 红色 | `bg-red-100 text-red-700` |
| 橙色 | `bg-orange-100 text-orange-700` |
| 黄色 | `bg-yellow-100 text-yellow-700` |
| 绿色 | `bg-green-100 text-green-700` |
| 翠绿色 | `bg-emerald-100 text-emerald-700` |
| 蓝色 | `bg-blue-100 text-blue-700` |
| 靛蓝色 | `bg-indigo-100 text-indigo-700` |
| 紫色 | `bg-purple-100 text-purple-700` |
| 粉色 | `bg-pink-100 text-pink-700` |
| 玫红色 | `bg-rose-100 text-rose-700` |
| 中性色 | `bg-gray-100 text-gray-700` |

## 4. 技能语义参考里的扩展内置色

虽然字段配置弹窗当前主颜色池是 8 个，但项目现有前端页面里已经稳定使用了更多同风格样式。  
为了让 Skill 在设计选项字段时更贴近产品现状，可以把下面这些也视为“语义参考风格”：

| 语义建议 | color 字符串 |
| --- | --- |
| 默认 / 待处理 / 未分类 | `bg-slate-100 text-slate-700` |
| 进行中 / 处理中 / 已开始 | `bg-blue-100 text-blue-700` |
| 成功 / 已完成 / 已提交 | `bg-emerald-100 text-emerald-700` |
| 驳回 / 异常 / 高风险 | `bg-rose-100 text-rose-700` |
| 警告 / 待确认 / 重点关注 | `bg-yellow-100 text-yellow-700` |
| 已取消 / 弱提醒 | `bg-gray-100 text-gray-700` |
| 次级完成态 / 正常 | `bg-green-100 text-green-700` |
| 品牌强调 / 业务色 | `bg-indigo-100 text-indigo-700` |
| 分类色 / 辅助强调 | `bg-purple-100 text-purple-700` |
| 活动态 / 营销态 | `bg-pink-100 text-pink-700` |
| 暖色提醒 | `bg-orange-100 text-orange-700` |
| 强风险 / 严重异常 | `bg-red-100 text-red-700` |

说明：

- 这批颜色里，前 12 个已经与字段配置常量直接对齐
- `emerald / rose / gray / indigo` 在现有前端页面里已经实际使用
- 技能可以按语义选色，但不要无约束扩张到大量零散 class
- 如果最终要落到 `dimens-cli column create/update`，当前应优先收敛到前端真实 12 色池，或显式改用 `custom:` 自定义色

## 5. 默认颜色策略

如果用户没有指定颜色，技能默认按下面规则输出：

1. 优先使用默认内置颜色，不要先上自定义颜色
2. 同一个字段内颜色要有语义梯度，不要全部一个色
3. 常见状态字段可直接套下面这类默认组合：

```json
[
  { "label": "待提交", "color": "bg-slate-100 text-slate-700" },
  { "label": "提交中", "color": "bg-blue-100 text-blue-700" },
  { "label": "已提交", "color": "bg-emerald-100 text-emerald-700" },
  { "label": "已驳回", "color": "bg-rose-100 text-rose-700" }
]
```

再例如题型字段：

```json
[
  {
    "id": "19928399-ca2e-4120-b615-041ed53bb08e",
    "label": "多选题",
    "color": "bg-yellow-100 text-yellow-700"
  },
  {
    "id": "71f84718-08d8-474a-9803-f5f4f95fbbda",
    "label": "判断题",
    "color": "bg-slate-100 text-slate-700"
  }
]
```

## 6. 自定义颜色协议

如果业务明确要求品牌色、主题色，或内置色无法满足，再使用自定义颜色：

```text
custom:{"bg":"#e0e7ff","text":"#3730a3"}
```

规则：

- 前缀必须是 `custom:`
- 后面必须是合法 JSON
- JSON 至少包含 `bg` 和 `text`
- `bg`、`text` 使用十六进制颜色值最稳定

## 7. 技能输出要求

当 Skill 要生成单选/多选/下拉字段时，默认至少输出：

- `id`
- `label`
- `color`

不要只输出：

```json
["待提交", "提交中", "已提交"]
```

而应该输出：

```json
[
  { "id": "opt_pending", "label": "待提交", "color": "bg-slate-100 text-slate-700" },
  { "id": "opt_processing", "label": "提交中", "color": "bg-blue-100 text-blue-700" },
  { "id": "opt_done", "label": "已提交", "color": "bg-emerald-100 text-emerald-700" }
]
```

## 8. 不要这样做

- 不要只写 `label`，不写 `color`
- 不要把颜色写成 `blue`、`green` 这种前端无法直接识别的简写
- 不要混用随机十六进制颜色和 Tailwind class，除非显式使用 `custom:`
- 不要把 `label` 当作稳定主键；`id` 必须可追踪、可更新
- 不要在同一字段里为十几个选项随意使用过多接近色，影响可读性
