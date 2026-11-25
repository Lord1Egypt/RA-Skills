# app Reservations
include Availability [VenueId]
include Reserving [UserId, Availability.Slot]
include Requesting

### 发起预约
sync reserve
when { Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request] }
then { Reserving/reserve: [user: ?user; slot: ?slot] }

// 预约结果不含 request，入口完成记录提供响应所需的请求身份。
### 返回预约结果
sync accepted
when {
  Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request]
  Reserving/reserve: [user: ?user; slot: ?slot] => [reservation: ?reservation]
}
then { Requesting/respond: [request: ?request; reservation: ?reservation] }

### 返回预约冲突
sync rejected
when {
  Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request]
  Reserving/reserve: [user: ?user; slot: ?slot] => [error: ?error]
}
then { Requesting/respond: [request: ?request; error: ?error] }

## 执行约束
- flow/关联：每个 Requesting/reserve 开启独立 flow，仅含一次尝试；重复尝试须关联发生记录。
- 读取/顺序：选定时段来自入口；_find 是读取，不满足 when。
- 结果：accepted/rejected 在该 flow 中匹配入口与预约完成记录，并沿用其 RequestId 响应。响应投递失败的处理仍未决。
- 时限/恢复：时限、重试与重启恢复仍未决。
