# easybrSearch 真实搜索示例

以下是 v0.1.0 的初次快照；新版验收另见平台覆盖与性能记录。

2026-10-26，在已经连接的 Chrome、Edge 与 EasyBR 环境后台执行。以下是当时的快照，不代表后续结果数量、排序或各账号始终相同。原始页面与私有路由仅留本机，不随开源包分发。

| 问题/查询 | 人工指定或保存的平台 | 去重候选 | 读到正文/简介 | 任务页清理 |
| --- | --- | ---: | ---: | --- |
| 其他模型如何做类似 opus5.5 的代码动画；查询 opus5.5 动画、Gemini 代码动画 | B站、小红书、CSDN | 24 | 5 | 已回读，无残留 |
| Manim Community quickstart | 保存的百度、Google | 7 | 3 | 已回读，无残留 |
| AI 配合 Manim 做数学动画；查询 AI Manim 入门 | 明确仅 B站，覆盖配置的百度、Google | 4 | 1 | 已回读，无残留 |

另外，Google 英文查询 Gemini HTML Canvas animation tutorial 返回 5 个候选，预算内两页未取得足够正文；不能据此复述视频。抖音原生搜索在本次环境只取得搜索外壳，报告加载超时，没有自动换平台。

## 示例回答：其他模型怎么做类似的代码动画？

可以先尝试“代码模型生成动画代码，再用确定的渲染工具输出视频”的路线。本轮找到两类有用资料，尚未比较各模型的实际成片效果，也不据帖子标题核实 Opus 的官方型号或能力：

- [Manim + Cursor 入门](https://www.bilibili.com/video/BV1vbHnecEq7)：已读视频简介，介绍 Manim 与 Cursor 联动，并标有 4:48 的实操章节。未播放或转录视频。
- [代码动画工具与分镜思路](https://www.bilibili.com/video/BV19gp16kEAc)：简介提到工具选择、提示词、风格、分镜与节奏。它在[小红书的同题版本](https://www.xiaohongshu.com/explore/6acf7bf00000000018004f47)属于同题内容，不能算成独立佐证。
- [Manim Community 官方 Quickstart](https://docs.manim.community/en/stable/tutorials/quickstart.html)：已读正文，涵盖创建项目、Scene、几何对象、形变与渲染命令。

建议先让自己已经选择的代码模型制作一个 10 秒样片，再看结果修提示词。数学图形可以先用 Manim；网页动效可另指定 HTML/Canvas 的任务和依赖。后者是实现选择建议，不是本次模型测评结论。

可复制给当前 AI：

> 请生成一个约 10 秒的 Manim Community 动画：出现坐标轴，绘制 y=x²，再标出顶点。先确认使用版本，给完整 Python 文件、依赖和渲染命令，暂不用 LaTeX 或外部素材。每次只修当前报错。渲染后检查坐标、文字和节奏。

## 示例回答：第一个 Manim 动画怎么渲染？

按官方安装说明准备环境，再用 Quickstart 创建样例项目。其流程是在 Scene 中定义对象与动作，然后通过命令行渲染。该页给出的项目初始化与首个场景命令如下；若使用 uv 环境，按文档在命令前添加 uv run 或先激活虚拟环境。[官方 Quickstart](https://docs.manim.community/en/stable/tutorials/quickstart.html)

```sh
manim init project my-project --default
cd my-project
manim -pql main.py CreateCircle
```

搜索示例只核对了网页资料，没有在本轮安装 Manim 或实际渲染这些教程。AI 入门搜索中的 Adobe Illustrator 教程已排除，不能当作数学动画依据。本地排序仍为加权关键词启发式，最终答案需要当前 AI 阅读和筛选。

## 实现验收

39 项离线回归通过，覆盖人工平台替换、配置不覆盖、失败分支、并行证据、链接去重、跳转回读、视频阅读范围、登录/验证码状态及任务页清理。独立用户验收确认“仅查 B站”没有增加百度/Google；根据实际歧义结果调整了专名权重，复测优先读取 Manim 来源。
