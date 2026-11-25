# app Reservations
include Availability [VenueId]
include Reserving [UserId, Availability.Slot]
include Requesting

### Request a reservation
sync reserve
when { Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request] }
then { Reserving/reserve: [user: ?user; slot: ?slot] }

// The entry completion supplies the request ID absent from the reservation result.
### Return the reservation
sync accepted
when {
  Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request]
  Reserving/reserve: [user: ?user; slot: ?slot] => [reservation: ?reservation]
}
then { Requesting/respond: [request: ?request; reservation: ?reservation] }

### Return the reservation conflict
sync rejected
when {
  Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request]
  Reserving/reserve: [user: ?user; slot: ?slot] => [error: ?error]
}
then { Requesting/respond: [request: ?request; error: ?error] }

## Execution constraints
- Flow/correlation: each Requesting/reserve starts its own flow with one attempt; repeated attempts need occurrence correlation.
- Reads/order: the selected slot comes from the entry; _find is a read and never satisfies when.
- Outcomes: accepted/rejected match the entry and reservation completion in that flow and respond using its RequestId. Response-delivery failure handling remains open.
- Timing/recovery: timing, retry, and restart recovery remain open.
