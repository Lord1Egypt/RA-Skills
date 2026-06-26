# City Rental Hunt Playbook

## 1. Constraint normalization

Use this compact schema internally:

```yaml
city:
zones: []
budget:
rooms:
must_have: []
soft_preferences: []
vetoes: []
```

Typical fields:
- `must_have`: 整租 / 电梯 / 两居 / 次新 / 可养猫
- `soft_preferences`: 客厅大 / 地铁近 / 房东直租 / 朝南
- `vetoes`: 老小区 / 合租 / 商住 / 非民水民电 / 明显中介轰炸

## 2. Keyword building pattern

### Base phrases
For each zone, combine:
- `<zone> 整租 两居`
- `<zone> 两居 房东直租`
- `<zone> 两居 转租`
- `<zone> 次新 电梯 两居`
- `<zone> 可养猫 两居`

### If neighborhood names are known
Promote them:
- `<neighborhood> 两居`
- `<neighborhood> 房东直租`
- `<neighborhood> 宠物友好`

### Keep phrases short
Prefer:
- `北苑 整租 两居`
- `清河 次新 两居`

Avoid bloated phrases like:
- `北京 北苑 地铁附近 次新电梯大客厅两居房东直租可养猫`

## 3. Evidence schema for every lead

```yaml
platform:
post_id:
url:
title:
summary:
price:
neighborhood:
zone:
transit_hint:
freshness:
poster_type:
pet_signal:
classification: keep|maybe|discard
reason:
```

### Poster type heuristics
- `landlord-direct`: explicitly says 房东直租 / 业主直租 / 个人转租
- `transfer`: 转租 / 合同剩余 / 因工作变动转出
- `agent`: 贝壳 / 我爱我家 / 连续发多盘 / 广告口吻 / 强引流
- `unclear`: not enough signal

## 4. Red-flag checklist

Discard or heavily downgrade when any of these is present:
- obvious shared rental / 合租 smell
- commercial apartment / 商住 unless explicitly acceptable
- very old walk-up when elevator/newness matters
- vague location + suspiciously low price
- ad-only post with no concrete listing facts
- stale post with no recent engagement
- price clearly outside budget with no redeeming upside

## 5. Freshness tiers

- **Tier A**: today / yesterday
- **Tier B**: within 7 days
- **Tier C**: within 30 days
- **Tier D**: older than 30 days

Default: prioritize A > B >>> C > D

## 6. Shortlist logic

### Keep
Use when:
- fresh enough
- plausible fit on rooms/budget/building quality
- enough info to justify contact

### Maybe
Use when:
- one key fact missing (price / pet / building age)
- otherwise promising

### Discard
Use when:
- clearly mismatched
- stale + vague
- low-trust ad spam

## 7. Morning brief template

```markdown
# Morning brief

## Best zone tonight

## Top leads to contact first
1. ...
2. ...
3. ...

## Why these matter
- ...

## Backup pool
- ...

## Risks to verify on first contact
- still available?
- monthly rent + fees?
- cat allowed?
- landlord direct or agent?
- exact neighborhood / building age / elevator?
```

## 8. Privacy / de-identification rules

When converting a private hunt into a reusable asset:
- remove personal names
- remove exact home/work identities
- keep only generic examples
- do not embed private note ids from a user's real search unless explicitly intended for public release
- abstract city-specific conclusions into reusable search patterns
