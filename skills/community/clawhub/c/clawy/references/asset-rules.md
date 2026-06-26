# Clawy Asset Rules

## Default base

- Default mother image comes from **Halfire Labs**.
- The bundled default file is `assets/default-mother-image.png`.
- Use it automatically unless the user explicitly asks to replace it.
- The default mother image is the main stability anchor for avatar generation.
- Keep the bundled default mother image as a square, non-stretched avatar reference whenever possible.
- Prefer padding/extension over distortion when converting a mother image into square format.

## Stable base body

- floating lobster-like mascot
- no lower limbs
- no legs, feet, knees, shoes, or humanoid walking structure
- two large rounded claws
- visible lobster tail
- full screen face
- all expressions shown on the screen
- no physical mouth
- no open mouth
- no antennae by default
- no biological face parts should appear outside the screen face
- claws must never be replaced by hands or humanoid arms

## Asset protection rule

- protect the base character asset before adding style
- do not redesign the creature into a humanoid, mammal, robot with legs, or other species
- if inspiration references a character with legs, only borrow equipment language, color language, props, and vibe
- never inherit limb structure from the inspiration source
- preserve the original body family first, then apply theme changes second

## Stable proportions

- keep the same perspective as the mother image
- keep the same head-body ratio
- keep the same claw-body ratio
- keep the same tail placement
- keep the same silhouette family

## Flexible equipment

- hats
- headwear
- visors
- hoods
- crowns
- outfits
- jackets
- robes
- armor
- claw materials/styles
- tail styles
- coordinated color themes

## Template purpose

Templates are reusable prompt modules that stabilize avatar generation.

Each template should bundle:
- vibe
- equipment language
- color direction
- role/archetype cues
- body-preserving wording

## Signature feature rule

When the inspiration comes from a recognizable character, do not stop at overall mood or genre.

Also extract the inspiration's concrete signature features, such as:
- hats
- wands
- earrings
- overalls
- ribbons
- staffs
- robes
- belts or armor cues
- iconic accessory structures

These signature features should be translated into mascot-friendly equipment details.
This usually improves recognizability much more than vibe-only prompting.

## Image capability rule

Clawy should first use any existing image-edit capability already available in the environment.

If multiple supported options are available, prefer:
1. nano
2. openai
3. fast

Only ask the user to configure an API if there is no usable image-edit capability.

## Avatar composition

- square output
- centered portrait
- upper-body framing
- character fills most of the frame
- simple NFT-style background
- no wide shot
- no complex scene by default

## Verified useful template directions

- hero-tech-armor
- platform-adventurer
- monster-trainer
- hiphop-streetwear
- royal-regalia
- candy-cyber
- cosmic-companion
- animal-hood
- mascot-crown
