# 4+1 架构视图自动生成器 (arc4plus1)

一个强大的 OpenClaw 技能，可自动分析代码结构并生成完整的软件架构 4+1 视图（逻辑视图、过程视图、物理视图、开发视图、场景视图），全部使用 Mermaid 图表渲染。

## 功能特性

- **逻辑视图**：展示类/组件及其关系（UML类图）
- **过程视图**：展示运行时控制流和调用链（序列图/流程图）
- **物理视图**：展示部署结构和节点拓扑
- **开发视图**：展示代码目录结构和模块组织
- **场景视图**：展示关键用例与架构的映射关系

## 使用方法

### 命令行调用
```bash
/dev:arc4plus1 /path/to/your/project
```

### 支持的编程语言
- Java (.java)
- Python (.py)
- TypeScript/JavaScript (.ts, .js)
- Go (.go)
- C# (.cs)
- C++ (.cpp, .h)
- Rust (.rs)
- Ruby (.rb)
- PHP (.php)
- Kotlin (.kt)

## 输出文件

生成的视图将保存在目标项目的 `arcview/` 目录下：
- `01_logical_view.md` - 逻辑视图
- `02_process_view.md` - 过程视图
- `03_physical_view.md` - 物理视图
- `04_development_view.md` - 开发视图
- `05_scenario_view.md` - 场景视图
- `README.md` - 视图说明和使用指引

## 技术细节

- 自动检测项目结构和入口点
- 支持单文件模式和工程模式
- 智能推断循环依赖并标注警告
- 自动处理大图，使用 subgraph 折叠聚合
- 严格遵循 Mermaid 语法规范，确保图表可正常渲染

## 示例

对于一个 Spring Boot 项目：
```bash
/dev:arc4plus1 ./my-spring-project
```

将在 `./my-spring-project/arcview/` 下生成完整的架构视图文档。

## 依赖要求

- Bash 环境
- Python 3.10+
- Node.js（用于 Mermaid 渲染验证）

## 许可证

MIT License - 可自由使用、修改和分发。

## 版本历史

- **v1.1.0** - 增强错误处理、添加阶段化执行流程、强制 Mermaid 语法校验
- **v1.0.0** - 初始版本，支持 4+1 视图自动生成
