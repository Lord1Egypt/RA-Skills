# Seats, Upgrades, and Sitting Together

Scope: where everyone ends up sitting, and what it costs to change that.

**Contents:** [Reading A Seat Map](#reading-a-seat-map) · [Which Seat Is Actually Better](#which-seat-is-actually-better) · [When Seats Open](#when-seats-open) · [Paying For Seats Or Not](#paying-for-seats-or-not) · [Sitting Together](#sitting-together) · [Upgrades](#upgrades) · [Aircraft Swaps](#aircraft-swaps) · [At The Gate](#at-the-gate)

## Reading A Seat Map

- The airline's own map at booking is authoritative for availability; independent cabin-layout references are better for what the seat is actually like, because airline maps do not mark misaligned windows, reduced recline or proximity to galleys.
- Layout references go stale after a cabin refit. Cross-check the aircraft subtype and configuration for the specific flight number, not the fleet.
- A map showing almost every seat blocked usually means seats are held for elites and check-in, not that the flight is full.
- Where the map differs from what the seat-selection screen sells, the selling screen wins — the map may be a generic template for the type.

## Which Seat Is Actually Better

| Position | Gains | Costs |
|---|---|---|
| Exit row | Legroom, sometimes free for elites | No under-seat storage at some exits, limited or no recline, restrictions on who may sit there, colder |
| Bulkhead | Legroom, bassinet position on long-haul | No under-seat storage at all, tray in the armrest narrows the seat, near a galley or lavatory |
| Row behind an exit | Occasionally extra pitch | Frequently the row that does not recline |
| Last rows | Empty middle seats more often, first to be assigned free | Near lavatories and galleys, last off, most turbulence-sensitive |
| Forward economy | Off the aircraft faster, meal service first | Often paid on legacy carriers |
| Window versus aisle | Window: sleep, wall, no interruption. Aisle: stretch, exit freely | On a long-haul with a tight connection, aisle wins on time |
| Over the wing | Smoothest ride, best for motion sensitivity | Restricted or no view |

Restrictions on exit rows are legal requirements, not preferences: age minimums, physical capability, no infants, no assistance animals, and the row cannot be pre-assigned to some passenger categories.

## When Seats Open

- Paid selection: available from purchase on most carriers.
- Free selection: often unlocks at check-in, T-24h, and the good rows are gone within minutes on busy routes. Put the exact opening time in `## Due` when it matters.
- Elite tiers unlock free selection earlier, and preferred seats that never appear to others.
- Award tickets sometimes cannot select until ticketed, and partner-issued awards may not be able to select on the operating carrier's site at all — call, or use the operating carrier's own record locator (`booking.md`).
- Blocked seats often release at T-24h, at airport check-in, and at the gate, in that order.

## Paying For Seats Or Not

Pay when: the flight is over roughly four hours, someone needs an aisle for a medical reason, a connection is tight and being near the front saves the transfer, or a family needs to be adjacent and the carrier does not guarantee it.

Do not pay when: the flight is short and full-fare-flexible, the fare family already includes selection at some later point, or the user holds a tier that unlocks it. On many carriers, checking in the moment the window opens gets an acceptable seat for nothing.

Assign-at-check-in fares put families and pairs at the mercy of what is left — which is the actual argument against Basic fares for anyone travelling with someone else (`fares.md`).

## Sitting Together

- Book everyone on one reservation. Split reservations are seated independently and are also handled independently in a disruption (`passengers.md`).
- Several regulators now require or strongly push carriers to seat young children next to an accompanying adult at no extra cost, and several carriers implement it as policy. Do not rely on it silently: verify the specific carrier's stated policy, and if it applies, use it rather than paying.
- Where nothing is guaranteed and the flight is full, paying for two adjacent seats is cheaper than the gate negotiation, and far cheaper than a family split across a wide-body.
- Two-adult trick on a three-seat row: book the aisle and the window. Middle seats are chosen last, and if it does fill, the occupant will happily trade for either of yours.
- Bassinet positions are limited, bulkhead-only, weight- and length-limited, and allocated by request order — request at booking and reconfirm at T-48h (`passengers.md`).

## Upgrades

| Route | How it works | Realistic odds |
|---|---|---|
| Paid at booking | The cabin's cash price, sometimes discounted as a bundle | Certain, and the honest baseline to compare everything else against |
| Bid upgrade | You name a price after ticketing; the airline accepts near departure | Winning bids cluster near a real fraction of the fare gap; low bids on full flights do not clear |
| Points or certificates | Programme-specific, and usually requires an eligible fare class — deep-discount economy is excluded | Depends entirely on upgrade inventory, not on the cabin having empty seats |
| Elite instrument (systemwide, upgrade credits) | Clears by tier, then fare class, then request time | Best on off-peak routes and days |
| Operational | The airline moves you when economy is oversold | Order is roughly tier, then fare class, then check-in time; asking at the gate does not change it |

Two facts that end most upgrade arguments: an empty seat in business does not mean upgrade inventory exists, because upgrade space is a separate bucket; and a cheap fare class is often ineligible whatever the balance in the account (`fares.md`).

## Aircraft Swaps

A change of aircraft type reassigns everyone. Seat numbers may map onto something completely different — the exit row becomes a middle seat, the bassinet position disappears. Any schedule change or equipment change is a signal to re-open the seat map, and it is also frequently grounds to change flights free of charge (`refunds.md`).

## At The Gate

- Seat changes at the gate are possible once boarding starts and the no-shows are known; ask the gate agent, not the crew.
- Swapping for a family is a request to the crew, politely and before everyone is seated. Nobody is obliged to move to a worse seat.
- If a paid seat was not delivered — a swap, a downgrade of position — that is refundable, and it is claimed after the flight with the receipt (`refunds.md`).

**When the user states a seat preference** — aisle, window, exit row, forward cabin, never a bulkhead — write it to `config.yaml` under `comfort`, not to memory: it is a declaration, not an observation. **When a specific aircraft or route produces a finding worth reusing** ("row 30 on this subtype has no window", "the bassinet row is 21 on this configuration"), that is an artifact: `~/Clawic/data/flight/artifacts/seats-<aircraft-or-route>.md`, with its `## Boxes` line added in the same turn.
