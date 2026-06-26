# 原子能力目录

## 定位

`atomic-capability/` 是 `cocoloop-skill-factory` 的原子能力路由层。
这里不承载具体 Skill 包，不承载动态服务端注册逻辑，只负责汇总当前可引用的原子能力说明，并为主流程提供稳定入口。

当前版本里，这个目录主要承载两类内容：

1. **本地静态能力 ref**
   - 已经写进仓库、可直接读取的能力说明
2. **未来动态能力入口**
   - 后续如果某些能力通过网络 API、注册中心或远端服务动态提供，也应当挂到同一套路由语义下

## 为什么改成 `atomic-capability/`

现在的目录更像“能力目录”而不是“实现集合”。
用单数目录名有两个好处：

- 更适合作为统一入口，主流程里只需要记住一个稳定路由
- 后续无论能力来自本地文档，还是来自动态注册，都能放进同一套索引语义

## 使用顺序

1. 先判定主任务域和并列任务域
2. 再读取对应 `presets/`
3. 然后进入 `atomic-capability/index.md` 选择可复用能力
4. 如果一个能力不够，再做组合
5. 如果本地没有合适能力，再记录缺口并考虑外部方案

## 路由结构

```text
atomic-capability/
  index.md
  browser-access/
  data-parse-transform/
  document-generation/
  external-service/
  file-ops/
  infographic-generation/
  presentation-generation/
  structured-visual-storytelling/
  search-and-info/
  subskill-invocation/
  template-mapping/
```

约定：

- 每个能力一个子目录
- 每个子目录默认入口是 `index.md`
- 如果某个能力有专项附录，放在同级子目录内
- 主流程和设计文档默认只引用 `atomic-capability/<capability>/index.md`

## 当前能力总览

| 能力 | 适用场景 | 当前来源 | 文档 |
| --- | --- | --- | --- |
| 搜索与信息获取 | 搜现成 Skill、补事实和上下文、整理参考 | 本地静态 | [search-and-info/index.md](./search-and-info/index.md) |
| 文件读写与整理 | 读取、改写、归档、重排文档与目录 | 本地静态 | [file-ops/index.md](./file-ops/index.md) |
| 数据解析与转换 | JSON、YAML、CSV、Markdown、表格之间互转 | 本地静态 | [data-parse-transform/index.md](./data-parse-transform/index.md) |
| 外部服务接入 | API、鉴权、回调、限流、配置接入 | 本地静态 | [external-service/index.md](./external-service/index.md) |
| 浏览器访问 | 页面查看、信息提取、表单与页面操作 | 本地静态 | [browser-access/index.md](./browser-access/index.md) |
| 结构化视觉叙事产物 | PPT、信息图、展示图、报告页等视觉叙事型产物的共享生产主线 | 本地静态 | [structured-visual-storytelling/index.md](./structured-visual-storytelling/index.md) |
| 信息图生成 | 长文信息图、视觉卡片、单页 poster、图卡导出 | 本地静态 | [infographic-generation/index.md](./infographic-generation/index.md) |
| PPT 生成 | 演示稿 brief、大纲、HTML slides、`.pptx` 导出 | 本地静态 | [presentation-generation/index.md](./presentation-generation/index.md) |
| 文档生成 | 需求文档、设计文档、Skill 文档、说明文档 | 本地静态 | [document-generation/index.md](./document-generation/index.md) |
| 子 Skill 调用 | 把复杂流程拆给子 Skill 或复用既有子流程 | 本地静态 | [subskill-invocation/index.md](./subskill-invocation/index.md) |
| 模板映射 | 把需求映射到平台模板与落地结构 | 本地静态 | [template-mapping/index.md](./template-mapping/index.md) |

## 选型原则

- 任务域预设优先于原子能力细分。
- 先选最小能力，再考虑组合。
- 先选“结构层”能力，再选“渲染层”能力。
- 能在文本层完成的，不先上浏览器。
- 能在本地文件层完成的，不先上外部服务。
- 模板映射负责落地方向，不负责直接替代其他能力。

## 视觉叙事产物的新规则

从近期深拆结果看，信息图、PPT、展示图和报告型页面都不能只被理解成“生成最终成品”。
后续使用时默认先进入 `structured-visual-storytelling`，再分流到不同 adapter。

默认顺序：

1. 先结构化内容
2. 再确认 `design_md`
3. 再检查文字层级
4. 再规划信息图元素
5. 再选择 `ppt`、`web_infographic`、`showcase_graphic` 等 adapter

## 动态能力扩展约定

后续如果引入网络 API 动态提供原子能力，建议仍然维持相同语义：

- `atomic-capability/index.md` 继续作为主目录
- 动态能力在索引表中标明来源为 `dynamic`
- 主流程先读目录，再决定能力来自本地还是远端

这样未来不会因为能力来源变化而重写主路由。

## 降级总则

- 本地没有匹配能力时，不阻断主流程，先继续研究和设计。
- 动态能力不可用时，优先退回本地静态能力。
- 外部服务不可用时，保留配置位和接入说明。
- 浏览器不可用时，转为文档输入、用户描述或手动核对。
