# concept Todo
coverage: complete
## purpose
Remember unfinished work and distinguish it from completed work.
## state
tasks: set Task
text: Task -> Text
done: set Task
Task is a local identity, never reused; Text is any string, including empty text.
Initially tasks and done are empty.
text has domain exactly tasks, with one Text per task; done is a subset of tasks.
Missing is the singleton error for an unknown task.
## actions
add [text: Text] => [task: Task]
  requires true
  ensures creates and returns one fresh t; tasks = old tasks union {t};
          text = old text plus (t, input text); done is unchanged
// Retain identity and text so the task can be reopened.
complete [task: Task] => []
  requires task belongs to tasks
  ensures done = old done union {task}; other state is unchanged
complete [task: Task] => [error: Missing]
  requires task does not belong to tasks
  ensures returns Missing; state is unchanged
reopen [task: Task] => []
  requires task belongs to tasks
  ensures done = old done minus {task}; other state is unchanged
reopen [task: Task] => [error: Missing]
  requires task does not belong to tasks
  ensures returns Missing; state is unchanged
## operational principle
after add [text: "report"] => [task: t], pending work includes t;
then complete [task: t] => [] removes it from pending work;
then reopen [task: t] => [] restores the same t and text.
## queries
_pending [] => [task: Task; text: Text]
  returns exactly tasks minus done, one row per task with its text;
  zero rows when empty; order unspecified; no completion

## Execution constraints
- Completion: the declared result and local state effects are observable to subsequent queries before the action completes.
- Concurrency: each state change atomically preserves the declared invariants.
- Failure/repetition: use the action cases above; repeated add calls create distinct tasks.
- Timing/recovery: no timing bound is specified; durability and restart recovery are outside this example.
