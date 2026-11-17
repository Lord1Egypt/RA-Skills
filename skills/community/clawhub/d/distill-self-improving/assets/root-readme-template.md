# 本机知识库

此目录保存路径导航、文件处理台账和由原文件形成的独立整理结果。索引和整理结果用于定位与理解，不替代原文件或当前现场；使用结论前必须回查来源和时点。

## 路径导航

```text
indexes/
├── projects.md
├── files.md
├── projects/<project-slug>/
│   ├── README.md
│   └── inventory.csv
└── collections/<collection-slug>/
    ├── README.md
    ├── scope.csv
    ├── inventory.csv
    ├── manifest.csv
    ├── distillations/<group-slug>/
    └── summaries/
```

- `projects.md` 与项目二级索引记录项目根、类型证据和关键入口。
- `files.md` 记录高价值文件与受控资料根，不复制全盘文件清单。
- collection 的 scope、inventory、manifest 记录完整逐文件范围和处理状态。
- `distillations/` 一份有价值原文件对应一份独立结果；`summaries/` 只做跨文件综合和版本脉络。

目录内容类型与版本控制事实分开：类型由用户明示、入口文档、源码布局和文件分布等多种证据判断，Git 只作可选佐证。代码项目侧重关键入口；文档资料集逐文件处理；mixed 按不重叠子树或全文件根范围执行。

## 使用边界

- 原文件只读，敏感信息和长原文不进入知识库。
- 结构检查通过不表示事实正确；路径、版本和易变结论仍需现场复核。
- 此初始化只创建索引结构，不创建知识或经验生命周期条目。
- `recurrence/` 由知识经验维护流程按需创建，用于保存既有条目后来被独立事件再次证实的最小证据；文件整理流程不写该目录。
