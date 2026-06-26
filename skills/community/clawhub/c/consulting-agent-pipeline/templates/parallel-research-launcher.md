# 并行调研启动模板 · Parallel Research Launcher

> 用于同时启动 N 个互无依赖的 Research Agent 实例。每个专题一个子目录 + 一份 Prompt。

---

## 适用场景

- Phase 1（调研阶段）启动时
- 多个专题调研可并行执行时
- Leroy 需要一次性分发 N 份调研任务时

## 使用方式

1. 填写下方的专题配置表
2. 对每个专题，Research Agent 复制对应的 Prompt 块
3. N 个 Research Agent 并行执行，完成后汇总

## 专题配置表

| 专题ID | 专题名称 | Research Agent | 状态 | 产出路径 |
|--------|---------|----------------|------|---------|
| G1 | {专题1} | gemini | ⏳ 待启动 | |
| G2 | {专题2} | gemini | ⏳ 待启动 | |
| G3 | {专题3} | gemini | ⏳ 待启动 | |
| G4 | {专题4} | gemini | ⏳ 待启动 | |

---

## 专题 Prompt 块（G1）

> 复制以下内容给第1个 Research Agent 实例

```
【调研任务 G1】{专题1名称}

请读取文件夹：
{项目根目录}/07_Gemini调研资料/01_{专题1名称}/

先读文件夹内的文件，然后执行以下任务：

{将 research-topic-template.md 的内容填入，去掉"专题配置表"部分}

产出路径：
- 主输出：{项目根目录}/07_Gemini调研资料/01_{专题1名称}/产出文档.md
- 备份：{Obsidian项目目录}/05_深度调研/01_{专题1名称}/产出文档.md
```

---

## 专题 Prompt 块（G2）

> 复制以下内容给第2个 Research Agent 实例

```
【调研任务 G2】{专题2名称}

请读取文件夹：
{项目根目录}/07_Gemini调研资料/02_{专题2名称}/

[同上格式]
```

---

## 汇总任务

所有专题完成后，由 Orion 执行汇总：

1. 读取每个专题的 `产出文档.md`
2. 填写调研汇总表：

| 专题 | 核心结论 | 可直接引用的数据 | 需客户确认的数据 | 风险点 |
|------|---------|----------------|----------------|-------|
| G1 | | | | |
| G2 | | | | |

3. 通知下游 Agent（Framework/Execution）调研阶段已完成
4. 更新 PROJECT_STATE.yaml：`research: completed: true`

---

## 执行检查清单

- [ ] 所有专题 Prompt 已分发
- [ ] 每个 Research Agent 已确认启动
- [ ] 产出目录已创建
- [ ] PROJECT_STATE.yaml 已更新（research: started: true）
- [ ] 汇总任务已安排
