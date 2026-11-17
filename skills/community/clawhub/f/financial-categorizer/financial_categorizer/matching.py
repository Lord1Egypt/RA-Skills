"""Shared matching helpers for transaction deduplication.

Bank reservation ("Reserverat") and settled descriptions frequently differ
in Swedish umlaut usage: reservations keep "å/ä/ö" while settled rows often
transliterate them to "a/a/o" (e.g. "Täby" vs "TABY"). These helpers fold
such variants so a settled charge can be recognized as the counterpart of
its reservation.
"""

import re

# Fold Swedish (and other common Nordic) diacritics to ASCII lookalikes.
_FOLD_TABLE = str.maketrans(
    "åäöéüèàçñÅÄÖÉÜÈÀÇÑ",
    "aaoeueacnAAOEUEACN",
)


def fold_nordic(text: str) -> str:
    """Fold Nordic diacritics to their ASCII lookalikes."""
    return text.translate(_FOLD_TABLE)


def clean_description(desc: str) -> str:
    """Normalize a bank description for matching.

    Lowercases, strips bank transaction prefixes ("Reservation Kortköp",
    "Kortköp YYMMDD", standalone "Reservation") and folds diacritics so
    umlaut variants compare equal.
    """
    d = desc.lower()
    # Matches 'reservation kortköp', 'reservation kortkp', 'reservation kortk\xf6p', etc.
    d = re.sub(r'^reservation\s+kortk[\xf6\ufffd\w]+p\s+', '', d)
    # Matches 'kortköp YYMMDD', 'kortkp YYMMDD', etc.
    d = re.sub(r'^kortk[\xf6\ufffd\w]+p\s+\d{6}\s+', '', d)
    # Fallback to remove standalone reservation prefix
    d = re.sub(r'^reservation\s+', '', d)
    return fold_nordic(d.strip())


def descriptions_match(desc_a: str, desc_b: str) -> bool:
    """True if either cleaned description contains the other."""
    a = clean_description(desc_a)
    b = clean_description(desc_b)
    return a in b or b in a


def aggregate_tolerance(amount: float) -> float:
    """Amount tolerance when matching a settled charge against the SUM of
    several reservations (split authorizations).

    Split authorizations routinely settle for a slightly different total
    (substitutions, tip adjustments), so allow 0.5% of the amount with a
    1.0 SEK floor — a small margin above the flat 1.0 SEK rule used for
    single-transaction matches.
    """
    return max(1.0, abs(amount) * 0.005)


# Amount band for inexact settlement matching. Some merchants (notably ICA
# Maxi with weighed goods) authorize a reservation and settle a different
# final amount, beyond the exact (1.0 SEK) and split-aggregate tolerances.
# A settled charge qualifies as the inexact counterpart of a reservation when
# |settled| is between INEXACT_LOW and INEXACT_HIGH times |reservation|
# (same sign). Asymmetric on purpose: reservations buffer UP for weighed
# items (settle lower), while currency conversion or tips settle higher.
# The floor is deliberately conservative: typical buffer haircuts are modest,
# and a settlement far below the reservation could instead be a genuinely
# separate purchase from the same merchant. Larger gaps stay unresolved for
# manual review (candidates + cleanup-pending --force-id).
INEXACT_LOW = 0.85
INEXACT_HIGH = 1.05


def inexact_amount_match(
    reservation_amount: float,
    settled_amount: float,
    low: float = INEXACT_LOW,
    high: float = INEXACT_HIGH,
) -> bool:
    """True if settled_amount is plausibly the final charge for a
    reservation authorized at a different amount: same sign and
    |settled| within [low * |auth|, high * |auth|].
    """
    if (reservation_amount < 0) != (settled_amount < 0):
        return False
    lo = abs(reservation_amount) * low
    hi = abs(reservation_amount) * high
    return lo <= abs(settled_amount) <= hi
