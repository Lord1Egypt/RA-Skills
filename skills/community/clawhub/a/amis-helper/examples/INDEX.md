# examples 索引

6 个片段：4 个由原整页示例 crud-full.json 1:1 平移拆出（该文件已删除），2 个独立保留。组合方式见 §2。

## 1. 片段清单

| 文件 | 场景 | 宿主依赖 | 覆盖规则 ID | 行数 |
|---|---|---|---|---|
| crud-base.json | 列表页骨架：Service 包层 + crud（分页/统计条/mapping/filter/导出） | 自包含 | C-01~C-08, D-02, D-08, D-09, A-01, A-02, F-01, F-03, F-04, F-06 | 141 |
| dialog-import.json | Excel 导入弹层（asBlob + form-data + 模板下载） | pageStateService 的 templateDownloading + mainCrud.id | D-01, D-02, D-04, D-05, D-08, F-05 | 71 |
| dialog-form-add.json | 新增弹层 | mainCrud.id | D-01, D-04, D-05, F-02, F-03, F-04 | 56 |
| dialog-form-edit.json | 编辑弹层（static + hidden） | mainCrud.id + 行上下文 ${code}/${name}/${id} | D-01, D-04, D-05, F-08 | 41 |
| dialog-confirm.json | 危险操作确认弹层 | mainCrud.id + 行上下文 ${code}/${id} | D-01, D-04, D-05, D-07 | 41 |
| bulk-actions-picker.json | 弹层内数据选择器（loadDataOnce + bulkActions + 跨页保留选中） | mainCrud.name + 行上下文 ${groupCode}/${groupId} | D-10, D-12, A-02 | 61 |

注：
- bulk-actions-picker 的 `"reload": "mainCrud"` 是 ajax 按钮的顶层 reload 属性（指向 name），
  属 `D-12`（业务按钮顶层 reload，操作完成后刷新）；内层 crud 非 reload 目标，符合 `C-02` 限定
- dialog-import 模板下载按钮已按 D-08 补 loadingOn 三件套，机制已实测生效
  （dialog 内 setValue componentId 可定位外层 Service）；button loading 视觉在 6.13.0 SDK 下待复核

## 2. 组合成整页（原 crud-full.json 的组合方式）

page
└─ service (id=pageStateService, data: exportDownloading / templateDownloading)
   └─ crud (id=name=mainCrud)
      ├─ api(adaptor) / filter / columns(mapping) / footerToolbar 统计条 / headerToolbar[reload, filter-toggler, Export] ← crud-base 自带
      ├─ headerToolbar += Import ← dialog-import（粘进 headerToolbar 数组）
      ├─ headerToolbar += Add ← dialog-form-add（粘进 headerToolbar 数组）
      └─ operation.buttons ← dialog-form-edit / dialog-confirm / bulk-actions-picker

**crud-base 的 operation 列 `buttons: []` 是骨架占位**。多个行内按钮必须包进单个 `button-group`（`C-08`），三个片段按序填入其 `buttons` 数组：

```json
{ "type": "button-group", "buttons": [ <dialog-form-edit>, <dialog-confirm>, <bulk-actions-picker> ] }
```
