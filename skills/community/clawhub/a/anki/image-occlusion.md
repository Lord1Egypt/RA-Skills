# Image Occlusion — Carding Anything With A Labelled Picture

Occlusion masks part of an image and asks you to recall what is under the mask. It is the correct format whenever **spatial position is part of the fact**: anatomy, maps, circuits, UI layouts, histology, chord shapes, pathology slides. It is built into Anki (`anki >=23.10`) as a shipped note type — installing Image Occlusion Enhanced on a current version is the classic redundant add-on.

## The Note Type

| Field | Holds | Notes |
|---|---|---|
| Occlusion | The mask shapes, stored as cloze-style ordinals | Written by the editor; never hand-edit |
| Image | The picture itself | One image per note, however many cards it generates |
| Header | The figure's name and orientation ("Brachial plexus, anterior view") | Shows on every card of the note — this is where the context prefix lives (SKILL.md rule 2) |
| Back Extra | Function, innervation, mnemonic, source page | Answer side only; the place to hang the non-spatial facts |
| Comments | Your notes about the card, not shown during review | Repair notes for future you |

One note, N masks, N cards. Adding a mask later generates a new card with a fresh review history; deleting a mask deletes its card and that history.

## Making The Masks

1. Editor → the Image Occlusion button (Notes → Image Occlusion on desktop; the same tool exists in the mobile editors on current clients).
2. Pick the image, then draw shapes: **rectangle, ellipse, polygon, text**. Polygon is what makes irregular anatomy work — a rectangle over a curved muscle masks its neighbours too.
3. **Grouping**: select several shapes and group them so they count as ONE card. Use it for a structure that appears twice in the figure (bilateral organs, a nerve crossing behind another), which otherwise becomes two cards with one answer.
4. Set the mode (below) before saving — it applies to the whole note.
5. Fill Header and Back Extra in the same pass. A figure you card without its name is unrepairable in a year.

Coordinates are stored relative to the image, so the masks survive scaling to a phone screen. What does not survive is a low-resolution source: occlude from the largest version of the figure you have.

## The Mode Decision (this is the one that matters)

The editor offers two modes. Picking the wrong one is why an anatomy deck feels either impossible or useless.

| Mode | What the card shows | Use when |
|---|---|---|
| **Hide All, Guess One** | Every region masked; you name the one highlighted | You must produce the labels on a blank figure — practical anatomy exams, spot tests, "draw and label" |
| **Hide One, Guess One** | Only the target masked; every other label visible | The neighbours ARE the fact (maps, circuit topology, UI layout, "which vessel runs between these two"), or it is your first pass on a dense figure |

Decision rule: **will the figure be labelled when you actually need the knowledge?** Labelled in real use → Hide One. Blank in real use → Hide All. Default to Hide All for anatomy and Hide One for maps and diagrams read for relationships.

The cost of getting it wrong runs both ways: Hide One on exam anatomy grades you on recognition with the answer key half-visible; Hide All on a 30-region figure produces 30 near-identical black rectangles that interfere with each other and become leeches together (SKILL.md Card Diseases, "Right answer, wrong card").

Escape hatch: start a hard figure on Hide One, and re-occlude it as Hide All once the region names are solid. Two notes, and delete the first when it stops earning its reviews.

## How Much To Occlude

Budgets, not measurements — the same intake arithmetic as any other card (SKILL.md rule 8):

- **5-12 masks per figure** is the working band. A 40-label plate is not one note: split it by region (upper limb → shoulder, arm, forearm, hand) and occlude each crop separately.
- Occlude what is **tested**, not what is drawn. Most atlas figures label structures no exam asks for; every extra mask is a card you own for years.
- Keep some named landmarks visible even in Hide All mode — an entirely black figure gives no orientation and the card becomes unanswerable rather than hard.
- One figure occluded twice from different sources is a duplicate you will not detect with Find Duplicates (it matches field 1, and field 1 here is the Occlusion data). Track figures by Header text.

## Pair It With Text Cards

Occlusion teaches **where**. It never teaches what a structure does, and a deck of pure occlusion produces students who can label a diagram and cannot answer a question about it.

- For each occluded figure, add plain cards for the facts that hang off it: function, innervation, blood supply, failure mode, the clinical sign.
- Cross-reference by tag (`figure::brachial-plexus`), not by deck, so the text cards and the occlusion cards can be studied and suspended together.
- The reverse direction — "which structure is innervated by the musculocutaneous nerve?" — is a Basic card, not an occlusion card. Occlusion only goes picture → name.

## Subject Recipes

| Material | Occlude | Mode | The detail that makes it work |
|---|---|---|---|
| Gross anatomy (atlas plate) | Structures named in your syllabus | Hide All | Header names the view; Back Extra carries innervation and function |
| Histology / pathology slides | The diagnostic feature, not the whole field | Hide One | The card must be "which feature is this", or you are carding image quality |
| Geography | One region per card, neighbours visible | Hide One | Orientation comes from the neighbours; a masked continent is unanswerable |
| Circuit / schematic | Components and their nodes | Hide One | Topology is the fact; hiding everything destroys it |
| UI / software layout | Panels and controls you must find fast | Hide One | Matches how you meet the interface: everything visible but the one you need |
| Chemical structures, pathways | Functional groups, enzyme steps | Hide All | Sequence recall is the point; visible neighbours give the answer away |
| Music (fretboard, keyboard, staff) | Note or interval positions | Hide All | Performance still needs the instrument, not the card |

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Installing Image Occlusion Enhanced on a current Anki | The feature ships built in; the add-on adds a second, incompatible note type | Use the built-in type; migrate old IO notes rather than running both |
| Occluding every label on the plate | Thirty cards on one figure, all failing together | Occlude the tested subset; split the plate by region |
| Hide All on a figure with no visible landmarks | A black rectangle with no orientation is not a hard card, it is an impossible one | Leave two anchor labels visible |
| Rectangles over irregular structures | The mask covers the neighbour, so the answer is ambiguous | Polygon tool |
| A bilateral structure masked twice | Two cards, one answer, and each one cues the other | Group the shapes into one card |
| Occlusion deck with no text cards | Labels a diagram, cannot answer a question | Pair every figure with its function cards |
| Hand-editing the Occlusion field | Breaks the shape data and orphans cards | Reopen the note in the occlusion editor |
| A screenshot-quality source image | Illegible on a phone, and the deck stops being reviewed | Occlude from the highest-resolution copy you have |
