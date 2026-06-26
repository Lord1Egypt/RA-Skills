# Execution Mode

本次运行模式：`mock_orchestration_demo`。

原因：当前运行环境能读取相邻 Skill 的本地说明文件，但不能把这些平行目录作为可直接触发的 Skill runtime 自动调用。因此本轮生成 mock artifacts 和 handoff packets，供人工复制到下游 Skill 中执行。
