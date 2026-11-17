from decimal import Decimal, ROUND_HALF_UP

TWO = Decimal("0.01")


def r2(x: Decimal) -> Decimal:
    """保留 2 位小数（ROUND_HALF_UP），对应 Java BigDecimal.setScale(2, RoundingMode.HALF_UP)"""
    return x.quantize(TWO, rounding=ROUND_HALF_UP)
