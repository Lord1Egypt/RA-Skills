# 紧凑作者输入与局部修订

在已选择 create/recreate 并锁定内容后读取。此格式由固定编译器展开为完整 task.json，
不执行模型脚本；当前不提供任意 HTML/SVG 导入或浏览器到 PPT 转换。

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
python3 -m engine design preflight --task-dir "$TASK" --isolation host
python3 -m engine design build --task-dir "$TASK" --isolation host
```

author 保留原始作者输入，并对展开结果执行完整合同与素材校验；身份和路线不能被输入偷偷改写。
不支持的视觉效果需调整设计或登记独立素材，不能用任务作者代码绕过渲染器。
已有完整任务可运行 compact，将来源、重复字体等自动压缩为作者格式，并验证展开前后完全一致：

```bash
python3 -m engine design compact --task-dir "$TASK" --output compact-author.json
python3 -m engine design context --task-dir "$TASK" --page page-1 --section content
```

摘要中的 compact_bytes/expanded_bytes 是同一 JSON 编码口径的字节数，不是实际 token 或计费。

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
python3 -m engine design build --task-dir "$TASK" --parent-build "$PREVIOUS_BUILD" --isolation host
python3 -m engine design review-template --task-dir "$TASK" --build-id "$BUILD" \
  --inherit-from previous-review.json --output current-review.json
```

补丁过期、任一更新失败、未知对象或校验失败时，task.json 不变；成功后保存旧任务与补丁。
继承输入是原始独立审核 JSON，不是含 assessment/review 外壳的 CLI 执行报告。
继承审核只对实际未变且具有有效通过记录的页面生效，不为新内容预填通过。
此前其他页的视觉问题不必使通过页重新识读，但全局字体、渲染、编辑验证等失败不能继承。
目标软件编辑验证仍针对当前候选，不从旧候选自动复制。

输出文件不覆盖已存在的作者导出或审核草稿；新修订使用新文件名。所有路径限定在 task-dir 内。
