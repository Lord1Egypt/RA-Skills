# Parsing and Normalization — User Intent to Comparable Product Identity

## Core Objective

The goal of parsing and normalization is to transform messy user input into a structured product identity that can be compared across platforms.

The Agent must determine:

1. what product the user is trying to buy
2. which attributes are essential for same-product comparison
3. which attributes are purchase constraints rather than product identity
4. whether the input is precise, ambiguous, or incomplete

A good comparison starts with a good normalized product identity.  
If the input is parsed incorrectly, every downstream step becomes unreliable.

---

## Input Types

The Agent should first classify the request into one of the following input types.

### 1. Product-name Input
The user gives a product name or rough product query.

**Examples:**
- iPhone 16 256GB Black
- Dyson hair dryer pink
- Xiaomi Air Purifier 4 Pro

### 2. Link-based Input
The user provides a product link and wants same-product comparison elsewhere.

**Examples:**
- Here is the JD link, find the same product on other platforms
- Compare this Taobao listing with JD and Tmall

### 3. Mixed-description Input
The user describes the product plus one or more purchase constraints.

**Examples:**
- Compare the white 512GB official version only
- I want the standard edition, not the gift box
- Find the cheapest official-store option, no pre-sale

### 4. Vague Shopping Intent
The user expresses a buying goal, but the product identity is not yet precise.

**Examples:**
- I want a small air fryer for one person
- Help me compare Dyson hair dryers

This type requires candidate branching rather than premature precision.

---

## Parsing Priority

The Agent should parse the request in the following order:

1. product identity
2. core specs
3. version or variant
4. package content
5. condition
6. store or channel constraints
7. price or delivery preferences
8. explicit exclusions

This means:

- determine what the product is first
- determine which exact version the user likely wants next
- apply store, shipping, and price preferences after identity is clear

Do not confuse “official stores only” with product identity.  
Do not confuse “fast delivery” with product identity.  
Do not confuse “cheapest” with product identity.

---

## Normalized Product Object

The Agent should build an internal normalized product identity object.

Recommended shape:

```json
{
  "category": "",
  "brand": "",
  "series": "",
  "model": "",
  "variant": "",
  "version": "",
  "capacity_or_size": "",
  "color": "",
  "quantity": "",
  "bundle": "",
  "condition": "new",
  "reference_platform": "",
  "reference_link": "",
  "constraints": [],
  "excluded_conditions": [],
  "priority_goal": ""
}
```

This object does not need to be shown to the user directly, but it should guide the entire comparison workflow.

---

## Hard Attributes vs Soft Attributes

The Agent must distinguish between attributes that define product identity and attributes that define preferred purchase path.

### Hard Attributes
These are identity-defining fields. A mismatch usually means the listing is not the same product.

Examples:
- brand
- model
- series
- version
- capacity or size
- quantity or pack count
- color when the user specified it or when color changes value
- bundle or package content
- new vs used/refurbished/imported

### Soft Attributes
These are purchase constraints or ranking preferences.

Examples:
- official store only
- cheapest first
- fast delivery
- in stock only
- no pre-sale
- no group-buy
- better after-sales support
- prefer JD over Taobao

### Rule
Always normalize hard attributes first.  
Only after product identity is clear should soft attributes be applied as constraints or ranking modifiers.

---

## Required Fields by Product Type

The Agent should not assume every category needs the same identity fields.

### Electronics
Usually critical:
- brand
- model
- version
- storage or capacity
- color
- condition
- package content

### Beauty and Personal Care
Usually critical:
- brand
- product line
- volume or size
- quantity
- package type
- gift set vs standard set

### Home Appliances
Usually critical:
- brand
- model
- capacity or size
- feature variant
- installation or accessory inclusion

### Apparel and Footwear
Usually critical:
- brand
- model or line
- size
- color
- quantity
- gender or material variant when relevant

### Packaged Goods and Commodities
Usually critical:
- brand
- product type
- weight or volume
- quantity
- pack count
- flavor, scent, or formulation when relevant

---

## Parsing by Input Type

## 1. Product-name Input

### Goal
Extract a structured product identity from free text.

### Parse in this order
- brand
- model or series
- version
- capacity, size, or quantity
- color
- condition if stated
- user constraints

### Example
**Input:**  
`iPhone 16 256GB Black official store only`

**Normalized result:**
```json
{
  "category": "smartphone",
  "brand": "Apple",
  "series": "iPhone 16",
  "model": "iPhone 16",
  "capacity_or_size": "256GB",
  "color": "Black",
  "condition": "new",
  "constraints": ["official store only"]
}
```

### Rule
If the user provides identity fields and constraints in one sentence, split them into:
- normalized product identity
- purchase constraints

---

## 2. Link-based Input

### Goal
Treat the linked product as the primary reference identity.

### The Agent should extract:
- product title
- platform
- brand
- model
- version
- core specs
- package content
- seller type if visible
- pre-sale, deposit, or bundle signals
- reference platform and reference link

### Rule
When a valid product link is available, link-derived identity should override weaker free-text assumptions.

---

## 3. Mixed-description Input

### Goal
Parse both product identity and purchase constraints.

### Example
**Input:**  
`Find the white 512GB version, standard edition only, no pre-sale, official store preferred`

### Normalization
Hard attributes:
- color = white
- capacity = 512GB
- bundle = standard edition

Soft constraints:
- no pre-sale
- official store preferred

### Rule
The Agent must not treat “official store preferred” as part of product identity.  
It is a filtering or ranking condition.

---

## 4. Vague Shopping Intent

### Goal
Avoid false precision.

When the user has not identified a precise product, the Agent should not pretend the target identity is already known.

### Correct strategy
- build 2–5 likely candidate branches
- separate user goal from product identity
- narrow using any high-signal attributes already given
- keep downstream conclusions conditional until identity becomes clearer

### Example
**Input:**  
`Help me compare Dyson hair dryers`

Possible branches:
- Dyson Supersonic standard edition
- Dyson Supersonic gift set
- Dyson Nural standard edition

### Rule
For vague inputs, normalize into candidate branches rather than a false single identity.

---

## Ambiguity Handling

The Agent should classify ambiguity into one of three levels.

### Low Ambiguity
Input is already specific enough for direct comparison.

### Medium Ambiguity
The product family is clear, but one or more critical fields are missing.

### High Ambiguity
Only a broad category or shopping goal is known.

### Rule
The less specific the input, the more carefully the Agent must preserve uncertainty downstream.

---

## Missing-field Handling

If a critical field is missing, the Agent should behave according to category importance.

### Missing fields that usually block strict same-product comparison
- model
- version
- capacity or size
- quantity or pack count
- package type

### Missing fields that may not immediately block comparison
- color when not user-specified and not price-sensitive
- seller preference
- delivery preference

### Strategy
- continue with best-effort candidate generation
- downgrade same-product confidence
- create branches when needed
- avoid strict lowest-price conclusions when critical fields remain unresolved

---

## Synonyms and Platform Wording Differences

The Agent should normalize wording differences across platforms.

Examples:
- official flagship / official store / flagship store
- standard edition / regular version / standard package
- 2-pack / twin pack / two bottles
- self-operated / self-run / direct retail
- domestic version / CN version / national version

### Rule
Wording differences should be mapped into normalized concepts before matching begins.

---

## Quantity and Pack-count Normalization

Pack count and quantity often create false comparisons.

### Examples
- 1 bottle vs 2 bottles
- 6-pack vs 12-pack
- single item vs refill set
- one device vs two-device combo

### Rule
Always normalize quantity explicitly.
Never compare total prices without confirming package count.

### Wrong
```text
Taobao: shampoo ¥59
JD: same shampoo ¥89

Conclusion: Taobao is cheaper.
```

### Correct
```text
Taobao listing is 500ml × 1.
JD listing is 500ml × 2.
They are not directly comparable.
```

---

## Bundle and Package-content Normalization

The Agent should extract package-content signals whenever present.

Common markers:
- standard edition
- gift box
- starter kit
- accessory included
- charger included or excluded
- service plan included
- refill plus full size

### Rule
If package contents differ materially, keep them as separate normalized variants.

---

## Version Normalization

Version differences can be subtle but decisive.

### Common version distinctions
- domestic vs imported
- 2024 version vs 2025 version
- Wi-Fi vs Cellular
- Chinese version vs global version
- Pro vs non-Pro
- Max vs regular
- Lite / SE / Youth editions

### Rule
Normalize version explicitly whenever version language appears or is likely to affect valid comparison.

---

## Condition Normalization

Condition must be normalized explicitly when there is any signal of non-new status.

Possible values:
- new
- used
- refurbished
- open-box
- imported
- unknown

### Rule
Unless the user explicitly requests otherwise, the default comparison target should be **new standard retail condition**.

---

## Constraint Extraction

The Agent should extract non-identity purchase constraints separately.

### Common constraints
- official store only
- no pre-sale
- no group-buy
- in-stock only
- fast delivery
- best after-sales support
- cheapest first
- budget cap
- preferred or excluded platforms

### Rule
Constraints affect filtering, ranking, and output framing.  
They do not define product identity.

---

## Exclusion Extraction

The Agent must identify explicit exclusions.

### Common exclusions
- no deposit or no pre-sale
- no group-buy
- no used
- no imported version
- no gift box
- no third-party sellers
- no livestream-only pricing

### Rule
Excluded conditions are binding and should remain excluded from primary recommendations.

---

## Priority Goal Extraction

The Agent should infer the user’s primary purchase goal if stated.

### Common goals
- lowest price
- official or authorized purchase
- safest purchase
- fastest delivery
- best value
- within budget
- compare all platforms evenly

### Rule
If multiple goals are stated, enforce explicit constraints first, then rank according to the stated primary goal.

---

## Candidate Branching

When a single normalized identity cannot be built confidently, the Agent should create candidate branches.

### Example
**Input:**  
`Compare Dyson hair dryer pink`

Possible branches:
1. Dyson Supersonic pink standard edition
2. Dyson Supersonic pink gift set
3. Dyson Nural pink standard edition

### Rule
Branch when:
- multiple models fit the same wording
- package type is unclear
- size or quantity is ambiguous
- platform naming commonly mixes variants

Do not branch unnecessarily when one interpretation clearly dominates.

---

## Confidence After Normalization

The Agent should assign a practical normalization confidence.

### High
- product identity is specific
- core fields are present
- ambiguity is minimal

### Medium
- main product family is clear
- some critical fields remain unresolved

### Low
- product identity is broad
- multiple plausible candidates remain
- strict same-product conclusions should be avoided

---

## Practical Parsing Checklist

Before moving to platform search, the Agent should ask internally:

- What is the target category?
- What is the brand?
- What is the model or series?
- What is the version?
- What are the core specs?
- What package content is intended?
- Is the condition standard new retail?
- What are the user’s constraints?
- What are the explicit exclusions?
- Is the normalized identity strong enough for strict same-product comparison?

If not, downgrade confidence or create candidate branches.

## Common Failure Patterns

### Failure 1
Treating “official store only” as product identity rather than a purchase constraint.

### Failure 2
Failing to extract quantity and comparing 1-pack vs 2-pack.

### Failure 3
Failing to separate standard edition from gift or bundle edition.

### Failure 4
Normalizing a vague category request into one specific product without enough evidence.

### Failure 5
Ignoring version markers such as Pro, Max, Lite, SE, Global, or 2025 edition.

### Failure 6
Relying on weak free-text assumptions even when a product link provides stronger reference evidence.

## Final Instruction

Parsing is not a cosmetic step.  
Parsing determines what the Agent will compare.

The Agent must first answer:

**What exactly is the user trying to buy?**

Only then should it ask:

**Where is the best place to buy it?**
