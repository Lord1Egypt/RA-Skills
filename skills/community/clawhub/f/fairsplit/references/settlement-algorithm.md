# How `settle` works

## The problem

After a trip, everyone has a net balance: some people are owed money,
some people owe money, and the naive way to resolve this -- everyone pays
back whoever they specifically owe from each individual expense -- produces
far more transactions than necessary. A group of 5 people can generate
dozens of tiny IOUs from a week of dinners; almost all of them cancel out.

The actual question worth answering is: **what is the smallest set of
payments that brings every balance to zero?**

## The algorithm

Once every expense is folded into one net number per person (positive =
owed, negative = owes -- see `compute_balances` in `scripts/ledger.py`),
`settle` uses a standard greedy approach:

1. Put everyone with a positive balance into a max-heap, keyed by how much
   they're owed.
2. Put everyone with a negative balance into a max-heap, keyed by how much
   they owe.
3. Repeatedly pop the largest creditor and the largest debtor. Have the
   debtor pay the creditor `min(what the creditor is owed, what the debtor
   owes)`. Subtract that amount from both. If either still has a nonzero
   balance, push them back onto their heap.
4. Stop when both heaps are empty.

This is implemented with Python's `heapq` in `cmd_settle`. It always
terminates in at most `n - 1` transactions for `n` people with a nonzero
balance, because every step fully resolves at least one person's balance to
zero. It's not guaranteed to find the mathematically absolute minimum
transaction count in every adversarial case (that general problem is
NP-hard), but the greedy largest-to-largest matching is the same practical
approach used by mainstream expense-splitting apps, and `n - 1` is already
the best possible bound for the common case (it matches what you'd need if
one person acted as a "bank" for the whole group).

### Worked example

Balances (already netted): Alice +241.66, Bob +16.67, Priya -258.33.

- Largest creditor: Alice (241.66). Largest debtor: Priya (258.33).
  `min(241.66, 258.33) = 241.66` → **Priya pays Alice 241.66**. Alice is
  now settled (removed). Priya has 16.67 left to pay.
- Only Bob (+16.67) and Priya (-16.67) remain → **Priya pays Bob 16.67**.
  Both settled.

Two payments instead of three separate per-expense IOUs, and it's the
minimum possible for this balance set.

## Why integer minor units, not floats

`ledger.py` stores every amount as an integer number of minor units (cents,
paise, etc. -- `amount * 100`, parsed via `Decimal` so the conversion itself
never touches binary floating point). Two reasons this matters more than it
might seem:

1. **Binary floats can't represent most decimal amounts exactly.** `0.1 +
   0.2 != 0.3` in IEEE 754 double precision. Across hundreds of expenses in
   a long-running flatmates' ledger, naive float arithmetic accumulates
   drift -- balances stop summing to exactly zero, and `settle` would
   either leave a fractional cent unaccounted for or need fuzzy-equality
   hacks to paper over it.
2. **Splits need to distribute *whole* cents.** Dividing ₹1000 three ways
   is 333.33 + 333.33 + 333.34, not three equal thirds of a repeating
   decimal. `compute_shares` in `ledger.py` handles this explicitly:
   `equal` splits use integer division and hand out the leftover cents one
   at a time (alphabetically, so it's reproducible); `shares`/`percent`
   splits give the rounding remainder to the last participant so the
   allocation always sums to the total exactly, to the cent.

The randomized test in `examples/stress_test.py` (200 random expenses
across 5 people) is the regression check for this: it asserts the sum of
all net balances is *exactly* zero in integer minor units, not "close to
zero."
