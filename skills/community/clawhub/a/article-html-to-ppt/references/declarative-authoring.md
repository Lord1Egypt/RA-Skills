# 紧凑作者输入与局部修订

在已选择 create/recreate 并锁定内容后读取。本页说明紧凑 JSON 输入，固定编译器将其展开为完整 task.json。
create 默认使用[受限 HTML 设计面](html-design-authoring.md)测量浏览器布局并编译原生对象，紧凑 JSON 可用于局部修订或无浏览器环境。

## 作者输入

先 init，再读取 task.json 骨架，写 author.json：

```json
{
  "format": "pptsmith-author/1",
  "tokens": {"ink": "132D46", "cjk": "任务环境已验证的字体"},
  "sources": {
    "source-p1": {"kind":"document","source":"报告第1页","checked":true,"uncertainties":[]}
  },
  "styles": {
    "title": {"font":{"family":"$cjk","size":32,"color":"$ink","bold":true}}
  },
  "task": {}
}
```

task 填入 init 产生的信封、设计 brief、逐页 content/notes/scene 与资产记录；空对象不能编译。
这里的配色只是语法例子，不是默认主题。tokens 仅替换设计属性中完整的 $name 值，
不触碰正文、来源、备注；不支持表达式、递归 token 或外部资源地址。

内容可用 source_ref 替代重复 provenance，但核对状态应对应实际完成的工作：

```json
{"id":"title","page_id":"page-1","type":"text","text":"当前页的完整判断",
 "required_edit":"native","source_ref":"source-p1"}
```

无附件逐页文稿先按[逐页稿制作](outline-to-deck.md)保留原文与设计要求。`sources` 可使用用户来源（下例仅为条目片段，放入 `sources`，核对后再填写 `checked: true`）：

```json
{"input-p1-b1":{"kind":"user","source":"user-input.md / page-1 / block-1","checked":false,"uncertainties":[]}}
```

内容条目通过 `source_ref: "input-p1-b1"` 引用；`checked` 只表示与本次输入核对，不表示已做外部事实核查。逐页分析摘要写入既有 `design.pages[].composition`；详细内容定位、关系依据、硬约束/偏好及处理结果留在任务内的 `page-plan.md`，不要向严格 Schema 塞入自定义字段。

节点可省略 page_id、role 和按数组顺序的 z；文字默认左对齐、顶部对齐、允许换行。
引用样式后可局部覆盖字号等属性：

```json
{"id":"title-object","type":"text","content_id":"title","style_ref":"title",
 "box":{"x":48,"y":36,"width":840,"height":70}}
```

symbols 用于可复用装饰，不承载业务文字或数据。定义 width/height/nodes，实例提供
symbol_ref、id、box；固定编译器按等比尺寸展开原生组、形状与路径，生成唯一子对象 ID。
任意非等比拉伸、未知字段、循环引用、越界或超量节点均拒绝。各次任务可自建符号，
不要把它变成固定整页排版。例：

```json
"symbols": {
  "marker": {"width":20,"height":20,"nodes":[
    {"id":"dot","type":"shape","shape":"ellipse",
     "box":{"x":0,"y":0,"width":20,"height":20},"style":{"fill":"$ink"}}
  ]}
}
```

实例：`{"id":"bullet-a","symbol_ref":"marker","box":{"x":48,"y":180,"width":10,"height":10}}`。

```bash
python3 -m engine design author --task-dir "$TASK" --file author.json
python3 -m engine design preflight --task-dir "$TASK" --isolation auto
python3 -m engine design build --task-dir "$TASK" --isolation auto
```

author 保留原始作者输入，并对展开结果执行完整合同与素材校验；身份和路线不能被输入偷偷改写。
不支持的视觉效果需调整设计或登记独立素材，不能用任务作者代码绕过渲染器。
已有任务可用 `compact` 导出可编辑的作者文件，工具会核对展开前后的内容。刚导入的页面也可导出，在作者文件里补齐简报和备注，再运行 `author`。

```bash
python3 -m engine design compact --task-dir "$TASK" --output compact-author.json
python3 -m engine design context --task-dir "$TASK" --page page-1 --section content
```

摘要中的 compact_bytes/expanded_bytes 是同一 JSON 编码口径的字节数，不是实际 token 或计费。

## 轻量元数据与页序维护

逐页 `html-import` 或局部调整整册结构时，无需导出并改写整份 `author.json`：

```bash
python3 -m engine design set-meta --task-dir "$TASK" --brief-file brief.md
python3 -m engine design set-page --task-dir "$TASK" --page page-1 --notes-file notes/p01.txt --composition-file comp/p01.json
python3 -m engine design add-page --task-dir "$TASK" --page page-6 --after page-5
python3 -m engine design remove-page --task-dir "$TASK" --page page-4
python3 -m engine design reorder-pages --task-dir "$TASK" --pages page-1,page-2,page-5,page-3,page-6
```

上述命令逐次保存 `history/` 快照并按未完成态校验，支持在导入阶段渐进填写 `brief`、备注和 `composition`（不允许降级已设置的 `review_profile`）。

## 原子补丁

context 返回当前 task_sha256。patch.json 必须绑定该版本；更新 font.size 等嵌套字段时保留其他字段。
可以修改 node、content、notes、design；page 只支持 background。增删节点等结构性改动使用作者格式。
身份、绑定页、节点类型不能通过补丁修改。

```json
{
  "base_task_sha256":"从当前context得到的真实哈希",
  "updates":[
    {"target":"node","id":"title-object","changes":{"font":{"size":30}}},
    {"target":"notes","id":"page-1","changes":{"text":"核对后的完整备注与来源"}}
  ]
}
```

```bash
python3 -m engine design patch --task-dir "$TASK" --file patch.json
python3 -m engine design build --task-dir "$TASK" --parent-build "$PREVIOUS_BUILD" --isolation auto
python3 -m engine design review-template --task-dir "$TASK" --build-id "$BUILD" \
  --inherit-from previous-review.json --output current-review.json
```

补丁过期、任一更新失败、未知对象或校验失败时，task.json 不变；成功后保存旧任务与补丁。
继承输入是原始独立审核 JSON，不是含 assessment/review 外壳的 CLI 执行报告。
继承审核只对实际未变且具有有效通过记录的页面生效，不为新内容预填通过。
此前其他页的视觉问题不必使通过页重新识读，但全局字体、渲染、编辑验证等失败不能继承。
目标软件编辑验证仍针对当前候选，不从旧候选自动复制。

输出文件不覆盖已存在的作者导出或审核草稿；新修订使用新文件名。所有路径限定在 task-dir 内。
