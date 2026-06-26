from datetime import datetime, timedelta


def normalize_mode(raw):
    if not raw:
        return 'WINDOW_MEALS'
    trimmed = str(raw).strip()
    if trimmed in ('WINDOW_MEALS','WINDOW_DISTINCT_DAYS','WINDOW_PACKS'):
        return trimmed
    return 'WINDOW_MEALS'


def normalize_int(raw, fallback):
    if raw is None:
        return fallback
    try:
        return int(raw)
    except:
        try:
            return int(float(raw))
        except:
            return fallback


def normalize_float(raw):
    if raw is None:
        return 0.0
    try:
        return float(raw)
    except:
        try:
            return float(str(raw).strip())
        except:
            return 0.0


def determine_cost_of_each_date_catering_product(unitCost, additionalModificationCost1, additionalModificationCost2, discountStack, deliveryDates, cateringDiscountMode, cateringDefaultWindowDays):
    print('---- determineCostOfEachDateCateringProduct CALLED ----')
    print('unitCost:', unitCost)
    print('additionalModificationCost1:', additionalModificationCost1)
    print('additionalModificationCost2:', additionalModificationCost2)
    print('cateringDiscountMode (raw):', cateringDiscountMode)
    print('cateringDefaultWindowDays (raw):', cateringDefaultWindowDays)
    print('deliveryDates (raw):', [d.isoformat() for d in (deliveryDates or [])])
    if unitCost is None or not deliveryDates:
        print('Guard triggered: unitCost or deliveryDates invalid, returning None')
        return None
    mode = normalize_mode(cateringDiscountMode)
    defaultWindow = normalize_int(cateringDefaultWindowDays, 7)
    def safeWindowSize(rule):
        return normalize_int(rule.get('windowSizeDays', None), defaultWindow)
    def safeThreshold(rule):
        return normalize_int(rule.get('noOfDaysInWeek', None), 0)
    def safeDiscount(rule):
        return normalize_float(rule.get('discount', 0.0))
    mod1 = normalize_float(getattr(additionalModificationCost1, 'additionalCost', additionalModificationCost1) if additionalModificationCost1 is not None else 0.0)
    mod2 = normalize_float(getattr(additionalModificationCost2, 'additionalCost', additionalModificationCost2) if additionalModificationCost2 is not None else 0.0)
    adjustedUnitCost = float(unitCost) + mod1 + mod2
    print('mod1:', mod1, 'mod2:', mod2, 'adjustedUnitCost:', adjustedUnitCost)
    normalized = [datetime(d.year, d.month, d.day) for d in deliveryDates]
    normalized.sort()
    print('normalized dates:', [d.isoformat() for d in normalized])
    # WINDOW_MEALS
    if mode == 'WINDOW_MEALS':
        W = defaultWindow
        start = normalized[0]
        blocks = {}
        for d in normalized:
            diff = (d - start).days
            blockIndex = diff // W
            blockStart = start + timedelta(days=blockIndex * W)
            blocks.setdefault(blockStart, []).append(d)
        blockPrice = {}
        for entry_start, dates in blocks.items():
            mealCount = len(dates)
            best = 0.0
            if discountStack:
                for rule in discountStack:
                    threshold = safeThreshold(rule)
                    rd = safeDiscount(rule)
                    if mealCount >= threshold:
                        if rd > best:
                            best = rd
            price = adjustedUnitCost - best
            blockPrice[entry_start] = price
        result = []
        for date in deliveryDates:
            d = datetime(date.year, date.month, date.day)
            diff = (d - start).days
            idx = diff // W
            blockStart = start + timedelta(days=idx * W)
            result.append(blockPrice[blockStart])
        return result
    # WINDOW_DISTINCT_DAYS
    if mode == 'WINDOW_DISTINCT_DAYS':
        W = defaultWindow
        start = normalized[0]
        blocks = {}
        for d in normalized:
            diff = (d - start).days
            blockIndex = diff // W
            blockStart = start + timedelta(days=blockIndex * W)
            blocks.setdefault(blockStart, []).append(d)
        blockPrice = {}
        for entry_start, dates in blocks.items():
            distinctCount = len({datetime(d.year,d.month,d.day) for d in dates})
            best = 0.0
            if discountStack:
                for rule in discountStack:
                    threshold = safeThreshold(rule)
                    rd = safeDiscount(rule)
                    if distinctCount >= threshold:
                        if rd > best:
                            best = rd
            price = adjustedUnitCost - best
            blockPrice[entry_start] = price
        result = []
        for date in deliveryDates:
            d = datetime(date.year, date.month, date.day)
            diff = (d - start).days
            idx = diff // W
            blockStart = start + timedelta(days=idx * W)
            result.append(blockPrice[blockStart])
        return result
    # WINDOW_PACKS
    if mode == 'WINDOW_PACKS':
        perMealDiscount = [0.0]*len(normalized)
        debug_rules_applied = []
        if discountStack:
            for rIndex, rule in enumerate(discountStack):
                threshold = safeThreshold(rule)
                W = safeWindowSize(rule)
                rd = safeDiscount(rule)
                print(f'Checking rule[{rIndex}] -> threshold: {threshold}, windowSize: {W}, discount: {rd}')
                if threshold <= 0:
                    print(f' Skipping rule[{rIndex}] because threshold <= 0')
                    continue
                for i in range(len(normalized)):
                    windowStart = normalized[i]
                    j = i
                    while j < len(normalized) and (normalized[j]-windowStart).days < W:
                        j += 1
                    mealsInWindow = j - i
                    print(f' Window from index {i} to {j} (exclusive) has {mealsInWindow} meals')
                    if mealsInWindow >= threshold:
                        print(f' Window qualifies for rule[{rIndex}], applying discount {rd} to indices [{i}, {j-1}]')
                        debug_rules_applied.append({'rule': rIndex, 'indices': [i, j-1], 'discount': rd})
                        for k in range(i, j):
                            if rd > perMealDiscount[k]:
                                print(f' Updating perMealDiscount[{k}] from {perMealDiscount[k]} to {rd}')
                                perMealDiscount[k] = rd
        print('WINDOW_PACKS -> perMealDiscount:', perMealDiscount)
        result = [adjustedUnitCost - perMealDiscount[i] for i in range(len(normalized))]
        print('WINDOW_PACKS -> Final result:', result)
        return result
    # fallback
    return [adjustedUnitCost]*len(normalized)


if __name__ == '__main__':
    from datetime import date
    # simple test
    dates = [date(2026,3,4), date(2026,3,5), date(2026,3,6)]
    print(determine_cost_of_each_date_catering_product(17, 0, 2, [{'discount':0.5,'noOfDaysInWeek':3,'windowSizeDays':7}], dates, 'WINDOW_PACKS', 7))
