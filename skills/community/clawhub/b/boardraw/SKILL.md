---
name: boardraw
description: Turn a natural-language description into a real Excalidraw whiteboard file (.excalidraw) — flowcharts, mind maps, architecture/system diagrams, org charts, wireframes, sticky-note brainstorms, sequence diagrams. Always use this skill whenever the user asks to draw, sketch, diagram, whiteboard, mind-map, or map something out, or mentions "excalidraw", "boardraw", "白板", "画一个", "流程图", "思维导图", "架构图", "组织架构图", "线框图", "泳道图", "看板", or wants a file they can open in Excalidraw or Boardraw. Do NOT hand-write raw .excalidraw JSON directly — the schema has fragile id/seed/binding requirements — always build it with the bundled scripts/excalidraw_builder.py helper instead.
---

# Boardraw — 自然语言生成 Excalidraw 白板文件

这个技能让你把用户的一句话描述（"帮我画个用户注册流程图"、"给这个项目搭个思维导图"、"画一下微服务架构"）直接转成一个可以在 Excalidraw 或 Boardraw 里打开、且元素仍然可编辑、可拖动、可连线的 `.excalidraw` 文件——而不是一张静态图片。

**Language policy: Always respond in English by default. If the user writes in any other language (e.g. Chinese, Japanese, Spanish), mirror that language for all replies in that conversation.**

**Core rule: Never hand-write raw `.excalidraw` JSON.** The format has strict `id`/`seed`/`versionNonce`/`boundElements` two-way binding requirements — hand-writing it almost always breaks things (text detaches from shapes, arrows don't snap to nodes). Always use the `ExcalidrawDoc` class in `scripts/excalidraw_builder.py` to build elements.

---

## 工作流程

### 第 1 步：把用户的描述拆解成结构

先在心里（或简单笔记里）把用户想要的东西拆成：
- **节点/卡片列表**：每个节点的文字、类型（普通步骤/判断/开始结束/便签）
- **连接关系**：谁连谁，方向是什么，连线上要不要写字（比如判断分支的"是/否"）
- **布局方向**：自上而下的流程图？从左到右？中心发散的思维导图？树状组织架构图？网格状的看板/便签墙？
- **分组/分区**：要不要用 frame（命名区域）把一部分节点框起来（比如"前端"、"后端"两个区域）

如果用户的描述比较模糊（比如"帮我画个流程图"没给具体步骤），直接用一个合理的示例流程走完整个骨架，并在回复里简单说明你是怎么理解的。

把设计作为**文字大纲**呈现给用户：

```
📋 图表预览
标题：用户注册流程

  [开始] → [填写表单] → [验证邮箱] → {邮箱有效?}
                                        ├── 是 → [创建账户] → [发送欢迎邮件] → [结束]
                                        └── 否 → [显示错误] → [填写表单]

配色：开始/结束 = 绿色，判断 = 黄色，步骤 = 蓝色
```

然后询问："**这个是你想要的吗？确认后我来生成并上传到 boardraw.com。**"

等用户确认后再继续。

---

### 第 2 步：选布局

`scripts/excalidraw_builder.py` 里带了几个坐标计算的小工具，不用自己心算坐标：

- `vertical_flow_positions(count, ...)` — 自上而下的直线流程图
- `horizontal_flow_positions(count, ...)` — 从左到右的直线流程图
- `grid_positions(count, cols, ...)` — 网格布局（看板、便签墙、并列卡片）

复杂布局（思维导图的放射状分支、树状组织架构图、有分叉/合并的流程图）直接手动算坐标即可——核心是保证同一层级/同一分支的节点间距一致（横向流程图节点间距一般 150–250px，纵向 250–350px 的行高，太挤会导致文字溢出到相邻节点上）。

---

### 第 3 步：用 `ExcalidrawDoc` 搭建元素

```python
import sys
sys.path.insert(0, "scripts")   # 视实际技能挂载路径调整
from excalidraw_builder import ExcalidrawDoc, vertical_flow_positions

doc = ExcalidrawDoc()

positions = vertical_flow_positions(4, x0=300, y0=40, w=200, h=80, gap=80)
labels = ["用户提交需求", "判断是否合规", "生成方案", "交付客户"]

nodes = []
for (x, y), text in zip(positions, labels):
    shape = doc.diamond(x - 20, y, 240, 100, bg="orange") if "判断" in text \
        else doc.rectangle(x, y, 200, 80, bg="blue")
    doc.label(shape, text)   # 文字必须用 label() 绑定进形状，不要单独摆 text 叠在上面
    nodes.append(shape)

for a, b in zip(nodes, nodes[1:]):
    doc.arrow(a, b)          # 相邻节点直接用 arrow()

doc.arrow(nodes[1], nodes[0], label="不合规，退回", stroke="red")

doc.save("/tmp/用户需求处理流程.excalidraw")
```

用 Bash 把脚本写成 `.py` 文件执行，不要在对话里手写 JSON。

---

### 第 4 步：连线方式——直线 vs 直角走线（让图好看的关键）

`arrow()` 只画两个元素中心点之间的**直线**。这在两个节点严格上下相邻、中间没有其它节点时没问题；但只要出现下面任一情况，直线就会斜着穿过别的节点，图会变得很乱：

- **多个节点汇入同一个下游节点**（比如 3 个并列测试项汇入 1 个判断菱形）——直线会斜着交叉成刺眼的"X"
- **跳过好几个节点的回退/循环箭头**（比如"验证失败"要跳回好几步之前的节点）——直线会直接斜穿过中间所有无关节点

这两种情况都要用 `doc.elbow_arrow()`（直角走线）代替 `doc.arrow()`：

```python
# 情况一：3 个测试项汇入 1 个判断节点，走"下 -> 中间横切 -> 下"，不要直线斜交叉
bend_y = (test_nodes[-1]["y"] + test_nodes[-1]["height"] + decision["y"]) / 2
for node in [functest, perftest, sectest]:
    doc.elbow_arrow(node, decision, exit="bottom", enter="top", bend=bend_y)

# 情况二：回退箭头要跳过中间好几个节点——走"侧道"绕开，而不是斜线穿过去
lane_x = doc.right_lane_x(margin=160)
doc.elbow_arrow(rollback_node, deploy_node, exit="right", enter="right",
                 bend=lane_x, stroke="red", label="重新部署")
```

**exit/enter 要用同一个轴向配对**（top/bottom 配 top/bottom，left/right 配 left/right），这样自动算出的拐点路径才会"绕开"而不是"横切"中间的东西。拿不准的复杂路径，直接用 `waypoints=[[x1,y1],[x2,y2],...]` 手动指定完整绕行路径。

**什么时候用 `arrow()`**：只有两个节点严格同列（纵向流程图里紧挨着的上一步/下一步）或严格同行、且中间没有第三个节点卡在直线路径上时。其它一律 `elbow_arrow()`。

---

### 第 5 步：自检——生成完先跑 `find_crossings()`，不能直接交付

```python
crossings = doc.find_crossings()
if crossings:
    print(crossings)   # [(箭头id, 被穿过的节点id, 节点类型), ...]
    # 说明有线穿过了不该穿的节点：把对应连线换成 elbow_arrow()/调整 bend 或 waypoints，
    # 或者加大节点间距，重新生成，直到这里返回空列表再保存交付
```

这是**强制步骤**，不是可选优化——不要在 `find_crossings()` 还有报错的情况下就把文件保存交付给用户。

---

### 第 6 步：保存、校验、上传到 boardraw.com

**1. 保存**到本地（文件名可以用中文，UTF-8 no BOM）。

**2. 校验** JSON 格式：
```bash
python3 -c "import json; json.load(open('output.excalidraw')); print('OK')"
```

**3. 上传** — 从环境变量 `BOARDRAW_API_KEY` 或目录树向上查找 `.env` 文件读取 API Key：

```bash
python scripts/upload.py output.excalidraw
```

或者用 curl：
```bash
curl -s -X POST "https://www.boardraw.com/api/keys/auth" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $BOARDRAW_API_KEY" \
  -d "{\"whiteboard\": $(cat output.excalidraw)}"
```

**API 响应处理：**

| 状态码 | 处理方式 |
|--------|---------|
| 201 | 提取 `file.uuid` → 展示 `https://www.boardraw.com/workspace/{uuid}` |
| 401（缺少 key） | 提示用户设置 `BOARDRAW_API_KEY` |
| 401（key 无效/已撤销） | 提示用户在 boardraw.com 设置页检查 key |
| 403 | 提示用户升级到 Pro 或 Team 计划 |
| 400 | 白板 JSON 格式有误，重新运行 builder 脚本 |

**4. 回复格式**——不需要列举每个节点，一行说明即可：

```
✅ 图表已上传到 boardraw.com！

🔗 在线查看/编辑：https://www.boardraw.com/workspace/{uuid}
📁 文件名：{fileName}
👤 账户：{user.name} ({user.email})

文件也可以直接在 Excalidraw 或任何兼容工具里打开。
```

---

## 文字与字体

`label()`/`text()` 默认用 `font_family=2`（Helvetica/无衬线体）。**不要改成 `font_family=1`（Excalifont 手绘体）去写中文/日文/韩文**——那个字体没有 CJK 字形，中文渲染出来会变形、缺笔画甚至乱码。`font_family=1` 只适合简短英文标题想要手绘风格的场景；中日韩文字一律留默认的 `2`。`font_family=3`（等宽代码字体）可以用在代码片段/接口名标签上。

---

## 常见图形套路

### 流程图（flowchart）
- 开始/结束：圆角矩形或椭圆
- 处理步骤：矩形
- 判断：菱形（`doc.diamond`），从判断菱形出去的每条分支箭头都用 `label=` 写上"是/否"之类的条件
- **同一列相邻的上一步 → 下一步**：直接 `arrow()`
- **多节点汇入一个节点、或分支跳过好几步回退**：一律 `elbow_arrow()`，见第 4 步

### 思维导图（mind map）
- 中心主题：一个大一点的椭圆放在画布中心，比如 `doc.ellipse(x, y, 220, 100, bg="violet")`
- 一级分支：从中心向四周放射状排布（三角函数算角度和半径，8 个分支 `angle = i * 360/8`），用 `doc.line()` 或不带箭头的 `doc.arrow(start_arrowhead=None, end_arrowhead=None)` 连到中心
- 分支颜色可以按主题分组，用 `stroke=` 区分（red/green/blue/orange/violet）

### 架构图/系统图（architecture diagram）
- 用 `doc.frame(x, y, w, h, name="前端")` 把同一层的服务框起来，再用 `doc.put_in_frame(el, frame_el)` 把里面的矩形放进这个 frame
- 服务/组件用矩形，数据库/存储可以用椭圆或圆角矩形加不同底色区分
- 调用关系用箭头，`label=` 标注协议或调用方式（比如 "HTTPS"、"gRPC"）；跨层级、不相邻的调用关系用 `elbow_arrow()` 走线，避免线穿中间层的框

### 组织架构图/树状图
- 从上到下按层级用 `grid_positions` 或手动坐标摆节点，每一层用 `y` 递增
- 上级到 1 个直属下级、且正下方没有别的节点：`arrow()` 即可；上级同时连多个平级下属，一律 `elbow_arrow(exit="bottom", enter="top")` 走"下-横-下"，不要用直线放射状连接（节点一多马上变成"X 交叉"）
- `end_arrowhead="triangle"` 更接近组织图的连接线观感，不需要箭头可以两端都设 `None`

### 看板/便签墙（kanban / sticky notes）
- 用 `grid_positions(count, cols=3)` 排列彩色便签矩形，`bg=` 换不同颜色区分类别/优先级/负责人
- 不需要箭头，纯网格摆放即可

---

## API Key 配置（Key 缺失时展示给用户）

```
要使用此技能，请配置你的 boardraw.com API Key：

1. 登录 boardraw.com → 设置 → API Keys
2. 创建新的 API Key（需要 Pro 或 Team 计划）
3. 添加到项目根目录的 .env 文件：
   BOARDRAW_API_KEY=br_your_api_key_here

   或者设置环境变量：
   export BOARDRAW_API_KEY=br_your_api_key_here
```

---

## 参考

- `references/excalidraw-schema.md` — 完整的原始 JSON 字段说明（元素通用字段、text/arrow/line 专有字段、颜色调色板、frame 规则）。只有当 `excalidraw_builder.py` 提供的方法覆盖不了用户的定制需求（比如自由手绘 freedraw、图片元素、特殊圆角、非默认字体大小）时才需要查阅，直接调 builder 的方法通常已经够用。
