# concept Reserving [U, S]
coverage: partial
## purpose
为用户保留未来使用资源时段的承诺。
## state
reservations: set Reservation
user: Reservation -> U
slot: Reservation -> S
status: Reservation -> Status
Reservation 是局部身份；Status = booked | canceled | granted。
Conflict 是表示时段已有 booked 预约的单例错误。
初始 reservations 为空。
每项预约恰有一个 user、slot 和 status。
每个 S 最多有一个 booked 预约；不假定 S 的字段。
## actions
reserve [user: U; slot: S] => [reservation: Reservation]
  requires slot 无 booked 预约
  ensures 原子创建并返回新鲜 r，设为输入 user/slot 和 booked；
          r 加入 reservations；已有事实不变
reserve [user: U; slot: S] => [error: Conflict]
  requires slot 有 booked 预约
  ensures 返回 Conflict；状态不变
cancel [reservation: Reservation] => []
  requires 预约为 booked
  ensures 仅将状态改为 canceled
grant [reservation: Reservation] => []
  requires 预约为 booked；到场条件未决
  ensures 仅将状态改为 granted
## operational principle
after reserve [user: u; slot: s] => [reservation: r]，
then 未取消且满足到场条件时 grant [reservation: r] => []，兑现承诺。

## 执行约束
- 完成：reserve 完成时具有已声明的预约或 Conflict 结果及状态效果。
- 并发：同一时段无 booked 预约的检查与新预约创建原子执行。
- 失败/重复：reserve 沿用声明的分支；重试身份与 cancel/grant 拒绝行为仍未决。
- 时限/恢复：到场条件、时限与重启恢复仍未决。
