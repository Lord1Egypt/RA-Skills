# Fence Line Negotiator

**Fences are the #1 trigger of neighbor legal disputes** — not because fences are complicated, but because three questions get answered by assumption instead of evidence: *Whose line is it on? Who pays? Whose problem is the broken panel?* When two households assume differently, a $2,000 fence becomes a $12,000 feud.

## What It Does

```bash
# Fair cost split: baseline shared, premium delta to whoever wants cedar
python3 scripts/fence_deal.py cost --length 160 --price-base 28 --price-upgrade 41 --share 0.5

# Who pays for the damage?
python3 scripts/fence_deal.py damage --cause "neighbor tree fell" --boundary yes

# Statutory-style cost-sharing notice letter (required BEFORE shares arise,
# e.g. California Civil Code 841) — ready to send, certified mail
python3 scripts/fence_deal.py notice --length 160 --cost 4480 --share 0.5 \
    --neighbor "J. Alvarez, 14 Maple St" --deadline 21

# 5-rung de-escalation ladder for your specific conflict
python3 scripts/fence_deal.py ladder --issue "neighbor says fence is 2ft onto his land"
```

## The Three Questions, Answered With Law and Math

1. **Line** — fences drift; the plat/GIS is free, a boundary survey ($500-1,500) is the only binding answer when it's close. Fence ON the line → cost-sharing doctrines apply. Fully on one side → that owner owns it, full stop. Encroaching → fix it before adverse possession matures (mowing 5 ft past the fence for 10-20 years can quietly transfer a strip worth more than the fence).

2. **Money** — ~20+ states put boundary-fence cost on BOTH owners (partition/good-neighbor statutes, notice letter usually required first); the rest leave it to agreement. The fair split: **share the baseline, the premium delta belongs to whoever wants cedar**. One signed page — recorded with the county — outlives both owners.

3. **Peace** — damage router (storm vs neighbor's dead tree vs rot vs contractor), the coffee-first ladder (conversation → letter → surveyor → mediation → attorney), and the exact words to open with: *"Our fence is failing — I got two quotes, want to split it fairly?"*

## Why It Matters

Boundary disputes escalate because each side treats its assumption as fact. The ladder exists because every rung is cheaper than the next: conversation (free) → letter ($7 certified) → survey ($1,000) → mediation ($300) → litigation ($5,000-50,000 — always more than the fence). Small claims judges read photos and letters; this skill manufactures the exhibit list before you need it.

## Who Needs This

Homeowners planning, repairing, or replacing a shared fence; anyone whose neighbor started building on the line unannounced; buyers/sellers where a survey surfaced an encroachment; rural landowners under line-fence/fence-viewer statutes; and anyone who wants the spite-fence line (deliberate over-height nuisance) and permit norms (6 ft back / 3.5-4 ft front, finished face out) checked before posts go in the ground.

*Practical guidance, not legal advice — state statutes vary; the reference includes the doctrine map and what to verify.*
