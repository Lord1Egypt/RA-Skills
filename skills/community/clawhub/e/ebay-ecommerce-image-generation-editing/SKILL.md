---
name: ebay-ecommerce-image-generation-editing
description: "Create and edit eBay listing images for new, used, refurbished, parts and collectible items, including condition disclosure, defects, identifiers, included accessories and scale. Use this skill for eBay商品图、二手商品、翻新机、藏品、配件清单、瑕疵展示、序列号处理、汽配兼容和跨境Listing；supports AI Hive reference editing."
---

# eBay Ecommerce Image Generation and Editing

Make the exact sale item inspectable. For used, refurbished, collectible or parts listings, condition evidence is more important than beautification. Never remove a material defect, replace a missing part, fabricate authenticity or show a different unit as the item for sale.

## Sale-item record

Record listing condition, exact unit photos, model and identifiers, included accessories, known defects, repair history, functional status, dimensions and any redaction needed for personal or security-sensitive numbers. Separate stock-like context images from actual-item evidence.

## Scenarios and commands

### 1. Used-item listing hero

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'eBay listing primary image for this exact used item. Preserve model, color, wear, scratches, discoloration, labels and missing parts. Remove only unrelated background clutter, use neutral lighting and show the complete unit. Do not make the item look new, repair damage or add accessories.' \
  --image /path/to/exact-item.jpg
```

### 2. Condition and defect gallery

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create four eBay condition views of the same exact unit: front, back, ports and known corner damage. Keep every scratch, dent, label and color consistent; improve visibility only. Do not conceal defects, replace casing or use a different specimen.' \
  --image /path/to/item-front.jpg \
  --image /path/to/item-damage.jpg \
  --batch 4
```

### 3. Included-accessories proof

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Top-down eBay included-items image showing the exact sale unit, charger and one cable, each once. Preserve condition and connector shapes, with clear separation. Do not add retail box, manual, spare part, warranty or anything not included.' \
  --image /path/to/lot-contents.jpg
```

### 4. Refurbished item disclosure base

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'eBay refurbished-item information base: exact unit plus close-up areas for replaced component, tested port and cosmetic grade, using seller-provided evidence. Leave all grade and test text blank for technician approval; do not create a certification, battery result or warranty.' \
  --image /path/to/refurbished-unit.jpg
```

### 5. Collectible or vintage detail

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'eBay collectible detail image preserving exact patina, maker mark, serial plate, edge wear and restoration evidence. Use raking neutral light for legibility. Redact only the seller-approved sensitive characters; do not imply authentication, grade or provenance.' \
  --image /path/to/collectible.jpg
```

## Condition QA

- Every evidence image shows the exact sale item or is explicitly contextual.
- Defects, wear, missing parts and repairs remain visible.
- Included items match the listing precisely.
- Sensitive identifiers are redacted consistently without altering model evidence.
- No generated authenticity, grade, test result, warranty, rating or price.
- Verify current eBay condition, category and image policies.

## Run

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name ebay-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

Use reference-guided generation conservatively. For condition evidence, editing should improve visibility, not the item. Record which source photo produced each output.
