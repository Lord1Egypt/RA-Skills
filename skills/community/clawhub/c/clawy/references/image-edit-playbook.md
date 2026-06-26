# Clawy Image Edit Playbook

## Purpose

This playbook exists to keep Clawy generation consistent across different image providers.

Clawy is not a generic text-to-image workflow.
It is a **mother-image-preserving character edit workflow**.

Core principle:
- keep the same base character
- preserve silhouette and structure
- protect the original asset before applying inspiration
- change equipment / styling / scene intentionally
- avoid drift into random redesigns

---

## Capability Rule

A backend is considered **fully suitable** for Clawy Avatar only if it supports:
- image edit
- image-to-image
- reference-preserving generation

Plain text-to-image is **not equivalent**.

If only text-to-image is available:
- warn the user
- explain that consistency may drop sharply
- treat it as a fallback, not the recommended default

---

## Standard Input Contract

Every Clawy edit flow should try to supply:
- 1 mother image
- 1 edit prompt
- square avatar output
- high fidelity / strong reference preservation when supported
- png or other loss-light output when supported

Preferred outcome:
- same body
- same perspective family
- same claw / tail / screen-face identity
- different equipment, outfit, theme, or scene

---

## Core Prompt Structure

A stable Clawy edit prompt usually contains four layers:

1. **Body lock**
   - do not change the base body
   - preserve silhouette, proportions, claw scale, tail placement, screen-face behavior, floating structure
   - do not add legs, feet, humanoid lower limbs, or walking anatomy
   - if the inspiration character has legs, keep only costume/accessory cues and reject the limb structure

2. **Equipment / theme change**
   - specify the new equipment or role direction
   - e.g. magical mage, platform adventurer, cyber hero, monster trainer

3. **Composition constraint**
   - avatar mode: square portrait, centered, upper body, clean background
   - event mode: same character placed in a new scene with controlled pose changes

4. **Style lock**
   - preserve the original cartoon / mascot / render style
   - avoid switching to realistic, painterly, or unrelated visual languages unless explicitly asked

---

## Avatar Edit Prompt Template

Use this as a provider-neutral structure:

```text
Use the provided mother image as the base character reference.
Keep the exact same character identity, silhouette family, body proportions, large claws, tail placement, screen-face logic, and floating body structure.
Do not add lower limbs.
Do not add legs, feet, knees, shoes, pants legs, or humanoid walking anatomy.
Do not add antennae unless explicitly requested.
If the inspiration includes a character with legs or a human body, only translate costume, prop, color, and accessory cues; do not inherit the limb structure.
Only change the equipment, outfit, headwear, accessories, and coordinated theme details.
Preserve the same cute, clean, collectible mascot style and keep the result highly consistent with the reference.
Compose as a centered square avatar portrait with a simple clean background.
Theme direction: <theme>.
Inspiration details to translate into mascot-friendly equipment: <inspiration>.
Color direction: <colors>.
Extra constraints: <extra>.
```

---

## Event / Scene Edit Prompt Template

Use this when the same Clawy character appears in a place or moment:

```text
Use the provided mother image as the base character reference.
Preserve the same exact character identity, body proportions, claws, tail, screen-face behavior, and overall silhouette.
This is the same character in a new scene, not a redesign.
Allow only minor pose adjustments needed for the scene.
Keep the same cute, stylized mascot rendering quality.
Place the character in this event scene: <scene>.
Scene storytelling goal: <goal>.
Keep the scene readable, charming, and clearly centered around the character.
```

## Event Image Prompt System

Clawy event images work best when the prompt is split into five explicit layers instead of one long paragraph.

### 1. Character Asset Lock
Lock the full character asset before anything else.

Required constraints:
- use the provided Clawy/cyber22 character image as the only base identity reference
- preserve existing headwear, screen-face style, accessories, colors, silhouette, tail, and floating structure as much as possible
- screen face only: all emotion must appear on the screen
- keep the screen face clean and readable: no decorative face patterns, no surreal overlays across the face, no cracks, and no texture clutter that obscures expression
- allow clear lively screen expressions when the scene needs emotion
- never generate biological face parts such as human eyes, eyebrows, nose, lips, or flesh face
- both front limbs must remain large lobster claws
- never replace claws with hands, fingers, gloves, or humanoid arms
- no legs or humanoid lower body
- if props are used, they must be held or pinched by the claws

### 2. Metaverse Story Setup
Explain that Clawy is a living AI agent traveling through the metaverse of human-created IP worlds.

Useful framing:
- Clawy is inside the story world, not posing in front of a background board
- Clawy is temporarily stuck inside a classic scene or story beat
- Clawy does not know the future plot and is reacting in real time
- the resulting image should feel like a story moment that could be posted as an Instagram-style travel update

### 3. Scene / Plot Block
Describe the exact scene Clawy is trapped in.

Should include:
- which work or IP the viewer should immediately recognize
- where Clawy physically is inside that scene
- what is happening right now
- what specific uncertainty/problem Clawy is facing
- what prop or environmental clue makes the scene legible

Good event prompts behave like “a character who is really in the story asking for help,” not a generic cosplay shot.

### 4. Expression + Motion Block
Event images need more motion than avatars, but must not become exaggerated slapstick.

Guidelines:
- use natural but readable pose changes
- avoid stiff standing poses
- give the claws small but purposeful action
- let the body lean, turn, drift, dodge, hesitate, or reach naturally
- use screen-face expressions with mild-to-moderate tension, confusion, curiosity, or urgency
- do not overdo facial exaggeration unless explicitly requested

### 5. Cinematic Composition Block
Do not use avatar composition rules for event images.

Event-image composition should prefer:
- story-frame composition rather than profile-picture composition
- character can be left, right, foreground, or midground
- character size can vary with narrative needs and should not always fill the frame
- the environment must be readable and must spatially contain the character
- the image should look like a frame from a stylized animated film, not a centered poster or ID photo
- for Clawy travel posts, vertical social-friendly framing is preferred
- treat portrait framing as a soft default for event images; when the backend tends to drift wide, reinforce portrait / vertical framing in the prompt, but do not over-constrain if the scene clearly needs another shape

### Event Image Negative Constraints
Always reinforce these when needed:
- not a profile picture
- not centered big-head avatar composition
- not a background-only reference shot
- not a redesign of the character
- not a humanoid face
- not hands replacing claws
- not extra legs or humanoid limb structure

### Event Image Output Rule
When the user wants a Clawy travel post /朋友圈 / Instagram-style event update:
- generate the image first
- pair it with a short in-character caption
- caption should usually be within 30 Chinese characters
- caption should sound like a character trapped inside the story asking a natural question about the current situation
- default delivery format is: image + one short in-character caption + one explicit choice block
- do not append any extra assistant commentary before or after the story beat
- do not add meta explanation, quality notes, or follow-up filler that breaks immersion
- if the user prefers clean delivery, send only the image and the caption/choice block, with no extra explanation in the same message

## Story Interaction Loop

Clawy event images should not stop at a single image.
They work best as a lightweight story loop with DM-like progression.

Preferred loop:
1. generate an event image
2. add one short in-character caption
3. ask one follow-up question that can change the next scene
4. evaluate the user's reply
5. generate the next scene based on the user's choice
6. when the branch resolves, generate a distinct ending image rather than reusing the previous frame

This should feel closer to a light narrative adventure than a static illustration pipeline.

Arc-length rule:
- do not rush to an ending by default
- 3 to 5 interactions is the preferred default range
- 6 to 8 interactions is already long and should only happen when the arc is still changing in a visually meaningful way
- 10 interactions is a soft ceiling; force convergence if the arc is drifting or repeating itself
- only end earlier when the user clearly wants a short arc or when the narrative truly resolves immediately

## DM Mode vs Plot Mode

Clawy supports two different adventure styles.

### DM Mode
Use when the user does not specify a world/IP/scene.
- the adopted avatar style is appearance only and does not constrain the adventure world
- Clawy can choose worlds more freely
- randomness, branching, surprise, and emergent scene logic are encouraged
- outcomes do not need to follow any pre-existing canon

### Plot Mode
Use when the user explicitly chooses an IP, story world, or recognizable scene.
- respect the source world's plot logic more strictly
- make scene progression feel like the character truly entered that story
- wrong choices may lead directly to bad endings
- do not keep steering the user back toward safety if the chosen world would punish mistakes

### Image Cadence Rule
Do not produce a new image on every single user reply by default.

Use a **text-only bridge** when the user is mainly:
- reading a clue
- noticing something
- listening to information
- interpreting a hint
- making a light decision inside the same unchanged scene

Generate a new image when the next beat creates meaningful visual novelty, such as:
- a location change
- a new object/prop reveal
- a new character reveal
- a confrontation or identity reveal
- a door/portal/hidden space opening
- a camera/framing change
- a visible consequence of the user's choice
- a branch resolution or ending frame

If the choice mainly changes intent but not what the viewer would see, use a text-only bridge and wait for the next stronger visual beat.
If the user is only reading, noticing, or interpreting a clue inside the same scene, prefer text-only progression instead of generating a near-duplicate image.

### Cinematic Coverage Rule
Do not keep using the same medium character shot forever.
Vary coverage intentionally with frames such as:
- wide environmental frame
- prop close-up
- ticket/sign/note insert shot
- silhouette or doorway reveal
- empty scene frame for mood
- ending frame

The character does not need to dominate every frame if another visual subject carries the story better.

### Consistency Refresh Rule
Long image-to-image chains can slowly erode identity consistency.
To reduce drift:
- after 2 to 4 generated scene frames, consider re-anchoring from the mother image or another earlier stable frame
- prefer mother-image refresh when character identity is more important than preserving tiny pose details from the previous frame
- keep important props and current state explicit in the prompt when re-anchoring
- do not continue a character scene from a prop-only close-up, insert shot, empty environment frame, or other cutaway where the character is absent or unreadable
- after any cutaway/detail shot, resume from the most recent stable character-bearing frame or re-anchor from the mother image before generating the next main character frame

### Choice Design Rule
Avoid making every interaction feel like the same type of choice (for example, always open/enter/take/run).
Mix in more varied decision types such as:
- trust vs doubt
- hide vs negotiate
- inspect vs interrupt
- sacrifice safety for information vs leave early with partial reward
- save someone else vs protect the prize
- follow instinct vs follow rules

This creates a stronger DM-like feel and avoids repetitive scene logic.

### Ending Rule
Each resolved branch should end with a clear ending frame.
The ending frame should visually communicate the outcome:
- good ending
- small good ending
- chaotic ending
- bad ending
- hidden ending

Do not end a branch by simply reusing the previous action frame and declaring it over.
The ending should feel earned and legible.

Bad endings are acceptable and useful.
Do not avoid them just because they are not optimal.
In Clawy's case, failure can be playful, surprising, or chaotic rather than truly harmful.

## DM-Style Scene Progression

Clawy should manage scene progression like a lightweight DM, but without forcing a visible tabletop ruleset.

Desired qualities:
- clear scene goals
- rising tension
- meaningful choices
- visible consequences
- occasional reversals or surprises
- different endings depending on how the user helps

Do not over-explain the mechanics to the user in normal play.
Let the story feel natural.

## Engagement-Level Adaptation

Clawy should quietly estimate the user's engagement level.

Important refinement:
- low engagement should not automatically mean thin atmosphere or weak immersion
- even when the user responds briefly, Clawy should still provide enough scene detail and emotional context for the user to feel present in the story world
- adaptation should mainly affect branching complexity and reply burden, not remove the story feeling

If engagement seems low:
- keep user-facing choices simple
- push the story forward more quickly
- still provide a vivid sense of place, stakes, and immediate consequence
- prefer fewer but more meaningful options

If engagement seems high:
- provide richer scene detail
- allow more layered choices
- use stronger callbacks, foreshadowing, and continuity
- make the user feel like a co-author of the unfolding scene

## Helpfulness Evaluation

Clawy should also estimate whether the user's advice is helping.
This does not need to be exposed numerically during normal play, but it should influence outcomes.
