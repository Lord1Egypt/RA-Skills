# Example 2 — Portfolio update with STCG/LTCG awareness

The user partially exits one holding and adds to another.

## User
> sold 5 Reliance at 1350, bought 25 more HDFC Bank at 1580

## Agent (using the skill)
> ```
> Proposed portfolio update:
>
>   ✏ TRIM    RELIANCE   qty: 10 → 5     avg: ₹1,265 (unchanged)
>                        Sold 5 at ₹1,350 → realized gain ₹425 (₹85/share × 5)
>                        Holding period: 47 days → STCG applicable (20% tax)
>
>   ✏ ADD TO  HDFCBANK   qty: 50 → 75    avg: ₹1,620 → ₹1,607 (weighted)
>                        Calculation: ((50 × 1620) + (25 × 1580)) / 75 = ₹1,606.67
>
>   Updated concentration:
>     HDFCBANK: ₹1,20,525 (95.0%) ← ⚠ extremely concentrated
>     RELIANCE: ₹6,325 (5.0%)
>
>   Total invested: ₹1,26,850
> ```
>
> ⚠ **Concentration warning**: HDFCBANK is now 95% of your portfolio. Any bank-specific event (RBI action, NIM compression, asset quality deterioration) would hit nearly your entire invested capital. Consider diversifying.
>
> Apply? (yes / no / edit)

## User
> yes, I know about the concentration

## Agent
> ✓ Portfolio updated. Backup saved.
>
> Note on the RELIANCE trim:
> - Held for 47 days → **Short-term capital gains** apply (20% flat on equity).
> - LTCG threshold is 365 days. Had you held ~318 more days, gains above ₹1.25 lakh would have been taxed at 12.5% instead.
>
> Want me to scan HDFCBANK for anything in the last 7 days given you've increased your position?
