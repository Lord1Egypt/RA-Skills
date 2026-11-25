# concept Todo
coverage: complete
## purpose
记住未完成工作，并区分已完成工作。
## state
tasks: set Task
text: Task -> Text
done: set Task
Task 是不复用的局部身份；Text 是任意字符串，允许空文本。
初始 tasks 与 done 为空。
text 定义域恰为 tasks，每任务恰有一个 Text；done 是 tasks 的子集。
Missing 是表示未知任务的单例错误。
## actions
add [text: Text] => [task: Task]
  requires true
  ensures 创建并返回一个新鲜 t；tasks = 旧 tasks union {t}；
          text = 旧 text 加 (t, 输入 text)；done 不变
// 保留身份与文本，支持重新打开。
complete [task: Task] => []
  requires task 属于 tasks
  ensures done = 旧 done union {task}；其余状态不变
complete [task: Task] => [error: Missing]
  requires task 不属于 tasks
  ensures 返回 Missing；状态不变
reopen [task: Task] => []
  requires task 属于 tasks
  ensures done = 旧 done minus {task}；其余状态不变
reopen [task: Task] => [error: Missing]
  requires task 不属于 tasks
  ensures 返回 Missing；状态不变
## operational principle
after add [text: "报告"] => [task: t]，待办包含 t；
then complete [task: t] => [] 后待办不含 t；
then reopen [task: t] => [] 后恢复同一 t 与文本。
## queries
_pending [] => [task: Task; text: Text]
  恰返回 tasks minus done，每任务一行并附文本；
  空状态返回零行；无顺序；不产生完成记录

## 执行约束
- 完成：声明的结果与局部状态效果可被后续查询观察后，动作才完成。
- 并发：每次状态变更原子保持已声明不变量。
- 失败/重复：沿用上述动作分支；重复 add 创建不同任务。
- 时限/恢复：未声明时限要求；持久化与重启恢复不在本例范围。
