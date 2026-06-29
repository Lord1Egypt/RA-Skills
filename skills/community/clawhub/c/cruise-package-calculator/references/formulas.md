# Break-Even and Value Formulas

All currency in USD. Apply the gratuity rule for every cruise line listed in `cruise_line_quirks.md`.

## 1. Effective Daily Cost (EDC)

```
EDC = Quoted_Daily_Price × (1 + Gratuity_Rate)
```

- Default gratuity rate = 0.18 unless the cruise line uses a different rate (see `cruise_line_quirks.md`).
- Royal Caribbean, Celebrity, Carnival, NCL, Princess, Holland America = 18%
- MSC = 18%, but some packages already include gratuity — verify before applying.
- Disney Cruise Line = no automatic gratuity on packages, but tip onboard.

## 2. Break-Even (Drink Package)

```
Break_Even_Drinks_Per_Day = EDC / Average_Drink_Price
```

- Use cruise line's average drink price from `cruise_line_quirks.md`.
- For lines with à-la-carte cocktail prices in $13–$16 range, use the midpoint of that line's range.
- For mixed consumption (cocktails + sodas + coffee + water), compute weighted average:

```
Avg_Drink_Price = (Cocktails × $14 + Beers × $9 + Wine × $13 + Sodas × $4 + Premium_Coffee × $5 + Bottled_Water × $4.50) / Total_Drinks
```

## 3. Break-Even (Wi-Fi Package)

Wi-Fi is sold per device per day. À-la-carte alternatives:
- Use port Wi-Fi at coffee shops / cruise terminals = $0
- Buy 1-day Wi-Fi pass on sea days only = (Sea_Days × Per_Day_Rate)

```
Wi-Fi_Break_Even = if (Sea_Days × Daily_Pass_Rate) < (Total_Nights × Package_Daily_Rate × 1.18)
                   then SKIP package, buy daily on sea days
                   else BUY package
```

## 4. Break-Even (Specialty Dining)

```
Break_Even_Meals = (Package_Price × 1.18) / Average_Specialty_Cover_Charge
```

- Royal Caribbean specialty cover ranges: $35 (Giovanni's) to $65 (Chef's Table)
- Carnival specialty cover: $20 (lunch) to $48 (Steakhouse dinner)
- NCL specialty cover: $30–$59 range

If user has a Latitudes/Crown & Anchor/etc. status that includes free specialty dining, subtract that from the package value.

## 5. Photo Package Break-Even

```
Photos_Needed = (Package_Price × 1.18) / À-la-carte_Per_Photo_Price
```

- Average à-la-carte digital photo: $25
- Average physical print: $20
- Photo packages typically priced for 5–8 photo equivalents.

## 6. Value Score Computation

See `value_score_rubric.md` for the weighted formula. The Value Score is the headline number the user sees — always compute it.

## 7. Multi-Person Discount Logic

When the cruise line requires all adults in the same stateroom to buy the package (Royal Caribbean, NCL, Carnival), the household decision flips to:

```
Household_Break_Even = Sum_of_Individual_Break_Evens
```

If only 1 of 2 adults drinks heavily, the math almost always says SKIP because the light drinker drags the average down.

## 8. À-la-carte Alternative Cost (ACC)

```
ACC_Per_Day = Σ(estimated_consumption_i × per_unit_price_i)
ACC_Total = ACC_Per_Day × Nights
Net_Position = Package_Total - ACC_Total
```

- If Net_Position is positive → SKIP (package costs more than à-la-carte)
- If Net_Position is negative → BUY (package saves money)
- If Net_Position is between -$30 and +$30 → "Depends" verdict; lean on Value Score
