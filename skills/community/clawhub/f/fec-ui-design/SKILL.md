---
name: fec-ui-design
description: Use when building, reviewing, or improving frontend UI that needs product-specific design direction, design-system generation, Master/Page overrides, distinctive visual identity, anti-generic interface choices, first-screen hierarchy, UI polish, chart UX, interaction states, responsive behavior, or visual QA. Interface polishing, interactive state.
---

#UI design

Suitable for UI tasks that require advancing the front-end interface to be "in line with the product context, scannable, trustworthy, recognizable, and stable in details". When systematic design suggestions are needed, load [design-intelligence.md](references/design-intelligence.md); when long-term precipitation of the design system is required, load [master-page-overrides.md](references/master-page-overrides.md); when doing UI/UX QA before going online, load [pre-delivery-checklist.md](references/pre-delivery-checklist.md).

The executable design system generator is located at [design-system.mjs](scripts/design-system.mjs), and its original knowledge package includes [product-rules.json](data/product-rules.json), [style-archetypes.json](data/style-archetypes.json), [ux-quality-rules.json](data/ux-quality-rules.json) and [stack-ui-rules.json](data/stack-ui-rules.json).

## Purpose

Establish design direction for pages, components, dashboards and tool interfaces, and complete implementable visual and interactive polish.

## Procedure

1. Clarify the work of the interface
   - Start by saying what task it helps the user accomplish, rather than choosing a color or layout first.
   - Determine whether this is a daily high-frequency tool, marketing display, content reading, visual exploration, game, or configuration/management backend.
   - If Figma, Sketch, MasterGo, Pixso, Ink Knife, Mockup or screenshots are the source of truth, give priority to restoring the design context and do not invent your own direction.

2. Read the design context
   - Before deciding on layout, colors, fonts, or motion, write out a line of design that reads: page type, target audience, primary mission, brand constraints, and sources of trustworthiness.
   - Determine whether the current interface is a visual website, work/brand display, product marketing, tool workspace, data-intensive interface, mobile native process, or design draft restoration task.
   - If the brief is clearly divergent, e.g. "minimalist yet intensely experimental", only ask a question that will change direction; otherwise make clear choices based on context.
   - Regulated, public service, medical, financial, children, or strong accessibility scenarios prioritize stability, clarity, and recoverability without sacrificing usability for aesthetic adventures.

3. Define aesthetic proposition
   - Write out the target users, usage scenarios, sources of trustworthiness, and a visual anchor that will be remembered.
   - Visual anchors can come from information structure, real media, data form, industry materials, font character, interaction rhythm or spatial organization, rather than empty decoration.
   - Expression must serve the business context: tool-based interfaces focus on efficiency and stability, while display-based pages focus on subject recognition and memory points.
   - Set design dials for page types: visual intensity, motion intensity, information density, media authenticity and content persuasiveness; these dials must change with the task, rather than sticking to the same set of templates.
   - Tool-type and data-type interfaces increase information density and reduce decorative animation by default; marketing, portfolio and brand pages can increase visual tension, but still ensure that the first screen task, main body and CTA are visible.
   - The design dial is used to constrain implementation choices: high visual tension does not equal chaotic typography, high dynamic intensity does not equal scroll hijacking, and high media authenticity does not equal piles of stock atmosphere images.

4. Generate or read design system
   - If the project does not yet have a design system, you can run `node skills/fec-ui-design/scripts/design-system.mjs "<product audience tone>" --project "<name>"` to generate suggestions.
   - If reuse across sessions is required, use `--persist` to generate `design-system/<project>/MASTER.md`; use `--page <page>` to write page differences into `pages/<page>.md`.
   - When building a specific page, read the page override first, and then read the Master; the page rules only cover the differences and do not copy the full design system.

5. Establish above-the-fold and visual hierarchy
   - Tool-based interface: The core workspace, list, table, canvas or editor is directly displayed on the first screen.
   - Landing page: H1 uses the brand, product, place, name or clear category, and the value description is placed in the auxiliary copy.
   - Product/Object page: The real product, object, status or checkable media must be visible on the first screen.
   - The first screen should leave a clear memory point, but should not obscure core tasks, navigation and status feedback.
   - Marketing and product pages need to clearly define the audience, pain points, commitments, evidence and action entry points; the copywriting structure serves conversion, but does not use exaggerated, empty or unverifiable claims.
   - The first screen of a visual page cannot be just text, gradients and decorations; it needs real products, people, spaces, brand applications, data status or checkable generated assets to bear the main information.
   - Navigation should remain single-line and highly restrained on desktop; CTA copy should be kept short and clear, and should not be replaced with multi-line buttons on desktop.

6. Organize visual language
   - Font: Give priority to using the project font system; if the task allows the establishment of a new direction, choose a title/text font combination that can express the character of the product and ensure readability.
   - Color: Clarify the roles of primary, functional, neutral and accent colors to avoid using equal force on all elements.
   - Space: Choose high-density, blank, asymmetric, column, canvas or editor layout according to the task, and do not apply fixed card templates.
   - Motion effects: Only establish rhythm for page entry, hierarchical expansion, status confirmation, error feedback and key guidance, and respect `prefers-reduced-motion`.
   - Media: Prioritize the use of real products, real states, real diagrams, checkable screenshots or locally generated assets; do not replace the main information with vague atmosphere images, placeholder URLs or irrelevant illustrations.
   - Charts: First determine whether the data task is trend, comparison, composition, distribution or process, and then choose charts. Do not make all data into cards or pie charts.
   - Visual reference: When there is no authoritative design draft and the visual quality of the page is the core goal, you can first generate or collect section-level reference images, and then extract the layout, hierarchy, color and media strategy from the images; do not compress the entire site into an unreadable long image.

7. Align design systems, components and tokens
   - First reuse the existing components, tokens, icon libraries, routing and layout conventions of the project.
   - When tokens are missing, centrally complete them or record them clearly. Do not scatter hard coding in multiple components.
   - Write out reused components, new components, responsive strategies and state overrides before implementing complex UI.
   - The design system first defines semantic tokens, component APIs, state matrices and usage boundaries, and then falls to Tailwind, CSS Modules, component libraries or CSS variable implementations.
   - Tailwind's special token, variant, dark mode and class management are offloaded to the Tailwind design system workflow; cross-device layout, container query and touch target are offloaded to the responsive layout workflow.
   - The component API should distinguish between basic components, business components and page-private components; avoid letting a single `variant` bear semantic, size, density and permission implications at the same time.

8. Polish geometry, text and states
   - Nested fillets follow the optical relationship of "the outer fillet is approximately equal to the inner fillet + spacing".
   - Asymmetric icons, play triangles, arrows, stars, etc. need to be fine-tuned according to the visual center.
   - Titles and short text can use `text-wrap: balance` or `text-wrap: pretty`.
   - Tables, prices, counters, and timers use `font-variant-numeric: tabular-nums`.
   - The clickable area of the small control should be at least 40x40px, and 44x44px is preferred if space allows.
   - focus ring is used for keyboard positioning, hover/active is used for mouse feedback, and disabled is not only expressed by transparency.
   - Do not repeat the same three cards, stagger left and right, or have a large title with an explanatory paragraph on the right in multiple consecutive blocks; the layout of each block serves the specific information task of that block.
   - The number of cells in the Bento and feature grid must be determined by the real content, and no empty cells are used to supplement the composition; multi-cell grids must at least have clear distinctions in primary and secondary, media or status.
   - The small uppercase eyebrow should be used with restraint and not become a rhythm crutch for each block.

9. Verify design results
   - Check loading, empty, error, disabled, hover, focus, selected status.
   - Check whether the copy text overflows or is blocked in mobile(375px), tablet(768px), desktop(1440px).
   - For interfaces that rely on pictures, charts, canvases or 3D, confirm that the resources are truly rendered and bear the main information.
   - Review whether there are traces of templates such as default purple gradients, empty heroes, card stacks, single hues, or non-contextual fonts.
   - Check whether the first screen has task entrance, subject identification, credible evidence and content clues for the next screen; if only decoration is left, return to the information architecture and redo it.
   - Complete hover, active, focus-visible, disabled, loading, selected, invalid and skeleton states for production-grade controls.
   - Fatigue when checking scan paths, density, fixed sizes, and reuse for dashboards, tables, editors, and configuration tables.
   - For marketing pages, portfolios and brand pages, check whether the first screen adapts to the height of common small notebooks, whether the navigation is single-line, and whether the CTA is qualified and does not wrap.
   - Review whether there are more than three consecutive paragraphs with the same section structure, repeated zigzag, repeated three cards, cards within a card set, fake screenshots, or visual assets without main information.

## Constraints

- Do not turn tool-based applications into marketing landing pages; the home screen should be the available workspace.
- No generic purple gradients, decorative flares, stacked cards, or empty heroes as the default scheme.
- Don’t use thirds of feature cards, continuous zigzags, repeating eyebrows, fake product screenshots, or uncheckable media as the default page rhythm.
- Don’t use context-free default fonts, uniform unfocused color palettes, repetitive rounded-corner cards, and templated two-column heroes as a substitute for real design judgment.
- Do not put large cards inside cards; give priority to using full-width area or frameless layout for page partitions.
- No visible copy is used to explain the functions that controls should express. Use icons and tooltips first for common actions.
- Do not add large-area decorations, blurry spots, semantic-less gradients or irrelevant rewriting for the sake of texture.
- Do not make the entire interface fall into a single hue in order to unify the style; colors should be hierarchical and semantically differentiated.
- Do not regard the generator output as an unmodifiable design draft; it is the starting point for decision-making and must be corrected based on the existing components, tokens, user tasks and real data of the project.
- No uncheckable remote placeholder images, generic stock mood images, or lorem copy as the delivery body; explicitly generate, produce, or degrade to real structured content when material is lacking.
- Don't let visual polish ruin keyboard paths, touch targets, text readability, or low-end device performance.
- Do not regard implementation vehicles such as Tailwind, component libraries, or Storybook documents as the design direction itself; they should inherit the already clear product context and token boundaries.
- Do not force a framework, icon library, animation library or CSS tool to reference system preferences; always prioritize current project dependencies and design systems.

## Expected Output

The output should include clear design direction, above-the-fold memo, visual language strategy, component/layout boundaries, state overrides, responsiveness strategy, and validation results. When reviewing, the interface should conform to the business context, the visual hierarchy should support fast scanning, the interaction status should be complete, and a generalized template feeling should be avoided.
