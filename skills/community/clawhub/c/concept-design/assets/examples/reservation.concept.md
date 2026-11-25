# concept Reserving [U, S]
coverage: partial
## purpose
Commit a resource slot to a user for future use.
## state
reservations: set Reservation
user: Reservation -> U
slot: Reservation -> S
status: Reservation -> Status
Reservation is local; Status = booked | canceled | granted.
Conflict is the singleton error for a slot with a booked reservation.
Initially reservations is empty.
Each reservation has one user, slot, and status.
Each S has at most one booked reservation; S has no assumed fields.
## actions
reserve [user: U; slot: S] => [reservation: Reservation]
  requires slot has no booked reservation
  ensures atomically creates and returns fresh r with input user/slot and booked status;
          adds r to reservations; existing facts are unchanged
reserve [user: U; slot: S] => [error: Conflict]
  requires slot has a booked reservation
  ensures returns Conflict; state is unchanged
cancel [reservation: Reservation] => []
  requires reservation is booked
  ensures changes only its status to canceled
grant [reservation: Reservation] => []
  requires reservation is booked; arrival conditions are open
  ensures changes only its status to granted
## operational principle
after reserve [user: u; slot: s] => [reservation: r],
then, if not canceled and arrival conditions hold, grant [reservation: r] => [] fulfills the commitment.

## Execution constraints
- Completion: reserve completes with its declared reservation or Conflict result and state effects.
- Concurrency: the no-booked-reservation check and reservation creation are atomic for each slot.
- Failure/repetition: reserve uses its declared cases; retry identity and cancel/grant refusal behavior remain open.
- Timing/recovery: arrival conditions, timing, and restart recovery remain open.
