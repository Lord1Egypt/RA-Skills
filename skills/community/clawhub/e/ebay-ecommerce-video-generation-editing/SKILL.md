---
name: ebay-ecommerce-video-generation-editing
description: "Create and edit eBay listing videos that document exact-item condition, defects, functional tests, included accessories, refurbished work and collectible details. Use this skill for eBay商品视频、二手商品、翻新机、功能测试、瑕疵记录、汽配、藏品状态、配件清单和跨境Listing；supports conservative Seedance editing through AI Hive."
---

# eBay Ecommerce Video Generation and Editing

Document the exact sale item. For used, refurbished, parts and collectibles, do not beautify away evidence. The video should help a buyer see condition, test behavior, included items and scale without implying authentication or warranty.

## Evidence protocol

Identify the exact unit, condition category, known defects, model/serial handling, included accessories, functional tests, repair history and seller-approved redactions. Prefer editing real footage; generated context must never replace actual-item evidence.

## Scenarios and commands

### 1. Exact-item condition walkaround

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/exact-used-item.jpg \
  --prompt 'eBay exact-item condition walkaround preserving model, wear, scratches, dents, discoloration, labels and missing parts. Show front, back, edges, ports and scale under neutral light. Do not repair, polish away damage, replace casing or show a different specimen.'
```

### 2. Functional test record

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/real-function-test.mp4 \
  --prompt 'Edit the real eBay functional test without changing its meaning. Keep power-on, input, output and observed behavior in chronological order; remove dead time only. Do not create a successful result, battery health, benchmark, certification or warranty not shown in the footage.'
```

### 3. Defect close-up extension

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/walkaround.mp4 \
  --prompt 'Continue the exact-item walkaround with close views of the known corner dent and screen scratch, then return to full item. Maintain item identity, wear pattern, hands and table; do not conceal or soften the defect.'
```

### 4. Refurbishment evidence

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/repair-process.mp4 \
  --prompt 'Organize verified refurbishment footage into intake condition, replaced component, reassembly and documented test. Preserve technician actions and exact unit; redact seller-approved sensitive identifiers only. Do not add a repair step, grade, certification or warranty.'
```

### 5. Included lot proof

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'eBay lot-content video based strictly on seller photos: exact sale unit, charger and one cable placed separately, then one connection demonstration. No retail box, spare, free gift, authenticity claim or additional item.'
```

## Evidence QA

- Actual-item footage and generated context are clearly distinguished.
- Wear, defects, missing parts and observed failures remain visible.
- Functional test editing does not turn an unknown result into a pass.
- Included items and identifiers match the listing.
- No generated authenticity, grade, warranty, price or feedback.
- Verify current eBay condition, category and media rules.

## Runtime

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name ebay-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

Use generation modes conservatively and retain source-to-output records. Real evidence should be edited, not synthesized.
