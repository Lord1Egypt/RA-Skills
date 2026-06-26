#!/usr/bin/env bash
# AccessLint — Accessibility Violation Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|WCAG_CRITERION|RECOMMENDATION
#
# Severity levels:
#   critical — Directly prevents access for users with disabilities
#   high     — Significant barrier to accessible use
#   medium   — Best practice violation, degraded experience
#   low      — Informational, improvement opportunity
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - Avoid Perl-only features (\d, \w, etc.)

set -euo pipefail

# -- Pattern registries by accessibility category ----------------------------
#
# Format: "regex|severity|check_id|description|wcag_criterion|recommendation"
# Patterns use POSIX extended grep regex (ERE) syntax.

# ===========================================================================
# 1. MISSING ARIA & ROLES (20 patterns)
# ===========================================================================

declare -a ACCESSLINT_ARIA_PATTERNS=()

ACCESSLINT_ARIA_PATTERNS+=(
  # Images without alt attribute
  '<img[[:space:]][^>]*>|critical|AR-001|Image missing alt attribute (filter: exclude if alt= present)|1.1.1|Add alt attribute: <img alt="description"> or alt="" for decorative images'

  # Button without accessible name (empty button)
  '<button[^>]*>[[:space:]]*</button>|critical|AR-002|Empty button — no accessible name|4.1.2|Add text content, aria-label, or aria-labelledby to button'

  # Input without aria-label or associated label
  '<input[^>]*type=["\x27](text|email|password|search|tel|url|number)["\x27][^>]*>|high|AR-003|Input may lack accessible name (filter: exclude if aria-label present)|4.1.2|Add associated <label>, aria-label, or aria-labelledby attribute'

  # Interactive element without role
  '<div[^>]*onclick|<div[^>]*onClick|<span[^>]*onclick|<span[^>]*onClick|high|AR-004|Non-semantic element with click handler — missing role attribute|4.1.2|Use a <button> element or add role="button" with tabindex="0"'

  # Custom element missing ARIA
  '<[a-z]+-[a-z]+[^>]*>|medium|AR-005|Custom element may need ARIA attributes (filter: exclude if role= or aria- present)|4.1.2|Add appropriate role and ARIA attributes to custom elements'

  # Icon-only button without aria-label
  '<button[^>]*>[[:space:]]*<(i|svg|span|img)[[:space:]]|high|AR-006|Icon-only button — may lack accessible name|4.1.2|Add aria-label to button: <button aria-label="Close"><svg ...></button>'

  # Link with no text content
  '<a[^>]*>[[:space:]]*</a>|critical|AR-007|Empty link — no accessible text|4.1.2|Add text content, aria-label, or accessible child to link'

  # Link with only an image and no alt
  '<a[^>]*>[[:space:]]*<img[^>]*>|high|AR-008|Link contains image without alt text (filter: exclude if alt= present)|1.1.1|Add alt text to image inside link for accessible link name'

  # SVG without title or aria-label
  '<svg[^>]*>|high|AR-009|SVG missing aria-label or role attribute (filter: exclude if aria-label or role= present)|1.1.1|Add role="img" and aria-label, or include a <title> element inside SVG'

  # Audio without track/captions
  '<audio[^>]*>|high|AR-010|Audio element — ensure captions or transcript available|1.2.1|Provide captions via <track> or a separate transcript'

  # Video without track/captions
  '<video[^>]*>|high|AR-011|Video element may lack captions/subtitles (filter: exclude if track present)|1.2.2|Add <track kind="captions" src="..."> for closed captions'

  # tabindex greater than 0
  'tabindex=["\x27][1-9]|medium|AR-012|tabindex > 0 disrupts natural tab order|2.4.3|Remove positive tabindex; use DOM order for tab sequence'

  # aria-hidden on focusable element
  'aria-hidden=["\x27]true["\x27][^>]*(tabindex|href=|<button|<input|<select|<textarea)|critical|AR-013|aria-hidden="true" on focusable element|4.1.2|Remove aria-hidden or make element non-focusable (tabindex="-1")'

  # Missing aria-expanded on toggle
  '<button[^>]*(toggle|collapse|expand|dropdown|menu)|medium|AR-014|Toggle button may need aria-expanded attribute (filter: exclude if aria-expanded present)|4.1.2|Add aria-expanded="true/false" to buttons that toggle content'

  # Missing aria-current for navigation
  'class=["\x27][^"]*active[^"]*["\x27][^>]*(href=|<a )|low|AR-015|Active navigation item — consider aria-current attribute|1.3.1|Add aria-current="page" to active navigation links'

  # Missing role on interactive div
  '<div[^>]*tabindex=["\x27]0["\x27][^>]*>|high|AR-016|Focusable div without role attribute (filter: exclude if role= present)|4.1.2|Add appropriate role (button, link, etc.) to focusable div elements'

  # Img with empty alt in non-decorative context
  'alt=["\x27]["\x27][^>]*class=["\x27][^"]*hero|banner|feature|low|AR-017|Possibly meaningful image has empty alt text|1.1.1|Review if image conveys information; add descriptive alt if so'

  # Missing role on list-like div
  '<div[^>]*>[[:space:]]*(<div[^>]*>[[:space:]]*<(a|button)[[:space:]]|medium|AR-018|Div structure may need list role (role="list")|1.3.1|Use semantic <ul>/<ol> or add role="list" with role="listitem" children'

  # iframe without title
  '<iframe[^>]*>|high|AR-019|iframe missing title attribute (filter: exclude if title= present)|2.4.1|Add title attribute to iframe describing its content'

  # Missing aria-describedby for complex widgets
  'role=["\x27](dialog|alertdialog|slider|spinbutton)["\x27][^>]*>|medium|AR-020|Complex widget missing aria-describedby or aria-label (filter: exclude if aria-describedby or aria-label present)|4.1.2|Add aria-describedby or aria-label to complex interactive widgets'
)

# ===========================================================================
# 2. SEMANTIC HTML ISSUES (18 patterns)
# ===========================================================================

declare -a ACCESSLINT_SEMANTIC_PATTERNS=()

ACCESSLINT_SEMANTIC_PATTERNS+=(
  # Div/span used as button
  '<(div|span)[^>]*role=["\x27]button["\x27]|medium|SH-001|Div/span used as button — prefer native <button>|4.1.2|Replace with native <button> element for built-in keyboard and screen reader support'

  # Div/span used as link
  '<(div|span)[^>]*role=["\x27]link["\x27]|medium|SH-002|Div/span used as link — prefer native <a href>|4.1.2|Replace with native <a href="..."> for built-in accessibility'

  # Nested interactive elements
  '<(button|a)[^>]*>.*<(button|a|input|select|textarea)[[:space:]]|critical|SH-003|Nested interactive elements — screen readers cannot parse|4.1.1|Remove nested interactive elements; restructure markup'

  # Heading hierarchy skip (h1 to h3)
  '<h1[[:space:]>].*<h3[[:space:]>]|high|SH-004|Heading level skip — h1 directly to h3|1.3.1|Do not skip heading levels; use h1, h2, h3 in sequence'

  # Heading hierarchy skip (h2 to h4)
  '<h2[[:space:]>].*<h4[[:space:]>]|high|SH-005|Heading level skip — h2 directly to h4|1.3.1|Do not skip heading levels; use sequential heading structure'

  # Multiple h1 tags
  '<h1[[:space:]>].*<h1[[:space:]>]|high|SH-006|Multiple h1 elements on page|1.3.1|Use only one h1 per page; use h2+ for subsections'

  # Missing lang attribute
  '<html[^>]*>|critical|SH-007|HTML element missing lang attribute (filter: exclude if lang= present)|3.1.1|Add lang attribute: <html lang="en"> for correct language identification'

  # Missing document title
  '<head[^>]*>|high|SH-008|Document missing <title> element (filter: exclude if <title> found in document)|2.4.2|Add <title> element inside <head> describing the page'

  # Non-semantic layout (div soup indicators)
  '<div[^>]*>[[:space:]]*<div[^>]*>[[:space:]]*<div[^>]*>[[:space:]]*<div[^>]*>[[:space:]]*<div|low|SH-009|Deeply nested divs — consider semantic elements|1.3.1|Replace generic divs with <main>, <nav>, <aside>, <section>, <article>'

  # Deprecated HTML elements
  '<(font|center|marquee|blink|big|strike|tt)[[:space:]>]|medium|SH-010|Deprecated HTML element used|4.1.1|Replace deprecated elements with modern CSS and semantic HTML'

  # Using heading for visual styling only
  '<h[1-6][^>]*class=["\x27][^"]*small|subtitle|caption|low|SH-011|Heading element may be used for styling — not semantic structure|1.3.1|Use CSS classes on appropriate elements; reserve headings for document structure'

  # b/i instead of strong/em
  '<(b|i)[[:space:]>]|low|SH-012|Use <strong>/<em> instead of <b>/<i> for semantic emphasis|1.3.1|Replace <b> with <strong> and <i> with <em> for semantic meaning'

  # Missing main landmark
  'PLACEHOLDER_MISSING_MAIN|medium|SH-013|Page may be missing <main> landmark|1.3.1|Wrap primary content in <main> for landmark navigation'

  # Missing nav landmark
  'PLACEHOLDER_MISSING_NAV|low|SH-014|Navigation may lack <nav> landmark|1.3.1|Wrap navigation links in <nav> element for screen reader landmarks'

  # Table without caption or summary
  '<table[^>]*>|medium|SH-015|Table missing caption or accessible description (filter: exclude if aria-label, aria-describedby, or caption present)|1.3.1|Add <caption> or aria-label to describe table purpose'

  # Table used for layout
  '<table[^>]*role=["\x27]presentation["\x27]|low|SH-016|Table used for layout — consider CSS Grid or Flexbox|1.3.1|Replace layout tables with CSS Grid or Flexbox'

  # Missing scope on th
  '<th[^>]*>|medium|SH-017|Table header missing scope attribute (filter: exclude if scope= present)|1.3.1|Add scope="col" or scope="row" to <th> elements'

  # Inline event handlers (not semantic)
  'javascript:|low|SH-018|javascript: URI — use event listeners instead|4.1.2|Replace javascript: URIs with proper event handlers for accessibility'
)

# ===========================================================================
# 3. KEYBOARD NAVIGATION (15 patterns)
# ===========================================================================

declare -a ACCESSLINT_KEYBOARD_PATTERNS=()

ACCESSLINT_KEYBOARD_PATTERNS+=(
  # onClick without onKeyDown/onKeyPress/onKeyUp — JSX
  'onClick=[{"\x27][^>]*>|high|KB-001|onClick without keyboard handler -- check for onKeyDown/onKeyUp|2.1.1|Add onKeyDown handler for keyboard equivalent of click action'

  # onclick without onkeydown — HTML
  'onclick=["\x27][^>]*>|high|KB-002|onclick without keyboard handler -- check for onkeydown|2.1.1|Add onkeydown handler for keyboard equivalent of click action'

  # @click without @keydown — Vue
  '@click[^>]*>|high|KB-003|Vue @click without @keydown equivalent -- check for @keydown|2.1.1|Add @keydown.enter handler alongside @click for keyboard access'

  # on:click without on:keydown — Svelte
  'on:click[^>]*>|high|KB-004|Svelte on:click without on:keydown equivalent -- check for on:keydown|2.1.1|Add on:keydown handler alongside on:click for keyboard access'

  # Mouse-only events without keyboard
  'onmouseover=["\x27]|onMouseOver=[{"\x27]|high|KB-005|mouseover event without keyboard equivalent (onfocus)|2.1.1|Add onfocus/onblur as keyboard equivalents for mouseover/mouseout'

  # onmousedown without onkeydown
  'onmousedown=["\x27]|onMouseDown=[{"\x27]|medium|KB-006|mousedown event without keyboard equivalent|2.1.1|Add onkeydown handler for keyboard equivalent of mousedown'

  # Missing focus styles (outline:none or outline:0)
  'outline:[[:space:]]*(none|0)|:focus[[:space:]]*\{[^}]*outline:[[:space:]]*(none|0)|high|KB-007|Focus outline removed — keyboard users cannot see focus|2.4.7|Provide visible focus indicator via outline, box-shadow, or border'

  # tabindex=-1 on interactive elements
  '<(button|a|input|select|textarea)[^>]*tabindex=["\x27]-1["\x27]|medium|KB-008|Negative tabindex on interactive element — removed from tab order|2.1.1|Remove tabindex="-1" from interactive elements unless programmatic focus management'

  # autofocus attribute
  'autofocus|medium|KB-009|autofocus may disorient screen reader users|3.2.1|Avoid autofocus; let users navigate to elements naturally'

  # Scroll container not keyboard accessible
  'overflow:[[:space:]]*(auto|scroll)|medium|KB-010|Scrollable container may not be keyboard accessible (filter: exclude if tabindex present)|2.1.1|Add tabindex="0" and role to scrollable containers for keyboard scrolling'

  # Drag-only interaction
  'draggable=["\x27]true["\x27]|ondrag|onDrag|medium|KB-011|Drag interaction — ensure keyboard alternative exists|2.1.1|Provide keyboard-based alternative for drag-and-drop functionality'

  # onDblClick without keyboard alternative
  'ondblclick|onDoubleClick|onDblClick|medium|KB-012|Double-click event — ensure keyboard equivalent|2.1.1|Provide keyboard alternative for double-click actions (Enter/Space)'

  # Focus trap indicator (prevent default on Tab)
  'preventDefault.*Tab|event\.key.*Tab.*preventDefault|high|KB-013|Potential focus trap — Tab key prevented|2.1.2|Ensure focus can escape the component; provide Escape key handler'

  # accesskey attribute
  'accesskey=["\x27]|low|KB-014|accesskey conflicts with assistive technology shortcuts|4.1.2|Avoid accesskey; use visible keyboard shortcuts or ARIA instead'

  # user-select: none on interactive
  'user-select:[[:space:]]*none|low|KB-015|user-select: none may prevent text selection for assistive technology|1.3.1|Avoid user-select: none on content areas; limit to UI chrome only'
)

# ===========================================================================
# 4. FORM ACCESSIBILITY (18 patterns)
# ===========================================================================

declare -a ACCESSLINT_FORM_PATTERNS=()

ACCESSLINT_FORM_PATTERNS+=(
  # Input without label (general)
  '<input[^>]*type=["\x27](text|email|password|search|tel|url|number|date|time)["\x27][^>]*>|critical|FM-001|Form input without label or aria-label (filter: exclude if aria-label or id= present)|1.3.1|Add <label for="id"> or aria-label attribute to input'

  # Select without accessible name
  '<select[^>]*>|high|FM-002|Select element without accessible name (filter: exclude if aria-label or id= present)|1.3.1|Add <label for="id"> or aria-label to select element'

  # Textarea without label
  '<textarea[^>]*>|high|FM-003|Textarea without accessible name (filter: exclude if aria-label or id= present)|1.3.1|Add <label for="id"> or aria-label to textarea element'

  # Missing fieldset/legend for radio groups
  '<input[^>]*type=["\x27]radio["\x27].*<input[^>]*type=["\x27]radio["\x27]|medium|FM-004|Radio button group may need fieldset/legend|1.3.1|Wrap related radio buttons in <fieldset> with <legend> describing the group'

  # Missing fieldset/legend for checkbox groups
  '<input[^>]*type=["\x27]checkbox["\x27].*<input[^>]*type=["\x27]checkbox["\x27]|medium|FM-005|Checkbox group may need fieldset/legend|1.3.1|Wrap related checkboxes in <fieldset> with <legend> describing the group'

  # Placeholder used as only label
  '<input[^>]*placeholder=["\x27][^"]+["\x27][^>]*>|high|FM-006|Placeholder used as only label -- disappears on input (filter: exclude if aria-label or id= present)|1.3.1|Add visible <label> element; placeholder is not a substitute for labels'

  # Required field without aria-required
  'required[^>]*>|medium|FM-007|Required field -- consider adding aria-required="true" (filter: exclude if aria-required present)|3.3.2|Add aria-required="true" for consistent screen reader support'

  # Error messages not linked with aria-describedby
  'class=["\x27][^"]*error[^"]*["\x27][^>]*>|medium|FM-008|Error message may not be linked to input via aria-describedby (filter: exclude if aria-describedby or role=alert present)|3.3.1|Link error messages to inputs with aria-describedby="error-id"'

  # Missing autocomplete on common fields
  'type=["\x27]email["\x27][^>]*>|low|FM-009|Email input missing autocomplete attribute (filter: exclude if autocomplete= present)|1.3.5|Add autocomplete="email" for autofill support'

  # Missing autocomplete on name fields
  'type=["\x27]text["\x27][^>]*(name|Name)[^>]*>|low|FM-010|Name input missing autocomplete attribute (filter: exclude if autocomplete= present)|1.3.5|Add autocomplete="name" or "given-name"/"family-name"'

  # Missing autocomplete on password
  'type=["\x27]password["\x27][^>]*>|low|FM-011|Password input missing autocomplete attribute (filter: exclude if autocomplete= present)|1.3.5|Add autocomplete="current-password" or "new-password"'

  # Form without accessible error display
  '<form[^>]*>|low|FM-012|Form may lack accessible error announcement region (filter: exclude if aria-live or role=alert present)|3.3.1|Add aria-live="polite" region for form validation error announcements'

  # Label without for attribute
  '<label[[:space:]>]|medium|FM-013|Label element may be missing for attribute (filter: exclude if for= present)|1.3.1|Add for="input-id" to label, matching the id of the associated input'

  # Hidden input used for visible data
  'type=["\x27]hidden["\x27][^>]*value=["\x27][[:space:]]*[[:alnum:]]|low|FM-014|Hidden input contains visible data — verify it should be hidden|1.3.1|Review if hidden input data should be visible and accessible to users'

  # Missing form instructions
  'PLACEHOLDER_FORM_INSTRUCTIONS|low|FM-015|Complex form may need instructions|3.3.2|Add descriptive instructions before the form or for individual fields'

  # Color-only required indicator (asterisk may not suffice)
  'class=["\x27][^"]*required[^"]*["\x27]|low|FM-016|Required indicator may use color only|1.4.1|Ensure required fields are indicated by text ("required") not just visual cues'

  # Disabled submit without explanation
  '<(button|input)[^>]*disabled[^>]*type=["\x27]submit["\x27]|medium|FM-017|Disabled submit button — users may not understand why|3.3.1|Explain why submit is disabled; provide aria-describedby with instructions'

  # File input without label
  '<input[^>]*type=["\x27]file["\x27][^>]*>|high|FM-018|File input without accessible name (filter: exclude if aria-label or id= present)|1.3.1|Add <label for="id"> or aria-label to file input'
)

# ===========================================================================
# 5. COLOR & VISUAL (12 patterns)
# ===========================================================================

declare -a ACCESSLINT_VISUAL_PATTERNS=()

ACCESSLINT_VISUAL_PATTERNS+=(
  # Color-only information (common patterns)
  'color:[[:space:]]*(red|green)[^;]*;|medium|VS-001|Color may be only indicator -- provide additional cue (filter: exclude if border, text-decoration, or font-weight also present)|1.4.1|Add icon, text, border, or other non-color indicator alongside color'

  # White text on light background patterns
  'color:[[:space:]]*#?[fFeE][fFeE][fFeE]|color:[[:space:]]*white|medium|VS-002|Light text detected — verify sufficient contrast|1.4.3|Ensure text meets WCAG contrast ratio: 4.5:1 for normal, 3:1 for large text'

  # Very small font sizes
  'font-size:[[:space:]]*[0-9]px|font-size:[[:space:]]*1[01]px|medium|VS-003|Very small font size — may be difficult to read|1.4.4|Use font size of at least 16px (1rem) for body text; minimum 12px for UI'

  # Missing prefers-reduced-motion
  '@keyframes|animation:|animation-name:|medium|VS-004|CSS animation — consider prefers-reduced-motion|2.3.1|Wrap animations in @media (prefers-reduced-motion: no-preference)'

  # Transition without motion preference
  'transition:[^;]*[0-9]+m?s|medium|VS-005|CSS transition — consider reducing for motion-sensitive users|2.3.1|Reduce or remove transitions inside @media (prefers-reduced-motion: reduce)'

  # Blinking/flashing content
  'text-decoration:[[:space:]]*blink|animation:[^;]*blink|high|VS-006|Blinking content — seizure risk for photosensitive users|2.3.1|Remove blinking effects; never flash content more than 3 times per second'

  # Missing dark mode hint
  'PLACEHOLDER_DARK_MODE|low|VS-007|Consider providing prefers-color-scheme support|1.4.3|Use @media (prefers-color-scheme: dark) for dark mode styles'

  # Background image with text overlay (no alt text)
  'background-image:[[:space:]]*url\(|medium|VS-008|Background image — ensure text on top has sufficient contrast|1.4.3|Verify text contrast over background images; add overlay or fallback color'

  # Text in images patterns
  '<img[^>]*alt=["\x27][[:space:]]*[A-Z][a-z].*[a-z][[:space:]]*["\x27]|low|VS-009|Image with text-like alt — consider using real text instead|1.4.5|Use HTML text instead of text in images when possible'

  # opacity: 0 may hide content from screen readers inappropriately
  'opacity:[[:space:]]*0[^.]|medium|VS-010|opacity: 0 hides content visually but not from screen readers|1.3.1|Use visibility: hidden or display: none to truly hide content; or aria-hidden="true"'

  # Fixed viewport width
  'width=["\x27][0-9]+["\x27]|initial-scale=1[^,]*maximum-scale=1|medium|VS-011|Viewport may prevent zoom — users with low vision need to zoom|1.4.4|Allow user zoom: do not set maximum-scale=1 or user-scalable=no'

  # user-scalable=no
  'user-scalable=["\x27]?(no|0)|high|VS-012|user-scalable=no prevents pinch-to-zoom — low vision barrier|1.4.4|Remove user-scalable=no to allow users to zoom in'
)

# ===========================================================================
# 6. DYNAMIC CONTENT (12+ patterns)
# ===========================================================================

declare -a ACCESSLINT_DYNAMIC_PATTERNS=()

ACCESSLINT_DYNAMIC_PATTERNS+=(
  # Live region without aria-live
  'class=["\x27][^"]*live[^"]*["\x27][^>]*>|medium|DY-001|Live region class without aria-live attribute (filter: exclude if aria-live present)|4.1.3|Add aria-live="polite" or "assertive" to announce dynamic updates'

  # Loading state without announcement
  'class=["\x27][^"]*loading|spinner|skeleton[^"]*["\x27][^>]*>|medium|DY-002|Loading indicator without accessibility announcement (filter: exclude if aria- or role= present)|4.1.3|Add aria-live="polite" with aria-busy="true" for loading states'

  # Modal/dialog without role
  'class=["\x27][^"]*modal|dialog[^"]*["\x27][^>]*>|high|DY-003|Modal/dialog without role="dialog" (filter: exclude if role=dialog or role=alertdialog present)|4.1.2|Add role="dialog" and aria-modal="true" to modal containers'

  # Modal without aria-modal
  'role=["\x27]dialog["\x27][^>]*>|medium|DY-004|Dialog missing aria-modal attribute (filter: exclude if aria-modal present)|4.1.2|Add aria-modal="true" to prevent screen reader from accessing background'

  # Toast/notification without role=alert or aria-live
  'class=["\x27][^"]*toast|notification|snackbar[^"]*["\x27][^>]*>|high|DY-005|Toast/notification without role="alert" or aria-live (filter: exclude if role=alert or aria-live present)|4.1.3|Add role="alert" or aria-live="assertive" to notification elements'

  # Alert without role=alert
  'class=["\x27][^"]*alert[^"]*["\x27][^>]*>|high|DY-006|Alert element without role="alert" (filter: exclude if role=alert or role=status present)|4.1.3|Add role="alert" for important messages that need immediate announcement'

  # Status message without role=status
  'class=["\x27][^"]*status[^"]*["\x27][^>]*>|medium|DY-007|Status element without role="status" (filter: exclude if role=status or aria-live present)|4.1.3|Add role="status" for non-urgent status messages'

  # Tab panel without proper roles
  'class=["\x27][^"]*tab-panel|tabpanel[^"]*["\x27][^>]*>|medium|DY-008|Tab panel without role="tabpanel" (filter: exclude if role=tabpanel present)|4.1.2|Add role="tabpanel" with aria-labelledby pointing to the tab'

  # Tab without proper role
  'class=["\x27][^"]*tab["\x27][^>]*>|medium|DY-009|Tab element without role="tab" (filter: exclude if role=tab present)|4.1.2|Add role="tab" with aria-selected and aria-controls attributes'

  # Accordion without aria-expanded
  'class=["\x27][^"]*accordion[^"]*["\x27][^>]*>|medium|DY-010|Accordion trigger without aria-expanded (filter: exclude if aria-expanded present)|4.1.2|Add aria-expanded="true/false" to accordion toggle buttons'

  # Progress bar without aria-valuenow
  'class=["\x27][^"]*progress[^"]*["\x27][^>]*>|medium|DY-011|Progress indicator without progressbar role (filter: exclude if role=progressbar or aria-valuenow present)|4.1.2|Add role="progressbar" with aria-valuenow, aria-valuemin, aria-valuemax'

  # Auto-updating content without aria-live
  'setInterval|setTimeout.*innerHTML|medium|DY-012|Auto-updating content — ensure screen reader announcement|4.1.3|Use aria-live region for content that updates automatically'

  # SPA route change without announcement
  'pushState|replaceState|navigate\(|router\.(push|replace)|low|DY-013|SPA route change — announce page transition to screen readers|4.1.3|Announce route changes via aria-live region or focus management'

  # Tooltip without accessible association
  'class=["\x27][^"]*tooltip[^"]*["\x27][^>]*>|medium|DY-014|Tooltip not associated with trigger via aria-describedby (filter: exclude if aria-describedby or role=tooltip present)|4.1.2|Add aria-describedby on trigger pointing to tooltip, and role="tooltip" on tooltip'
)

# ===========================================================================
# Utility functions
# ===========================================================================

# Get total pattern count across all categories
accesslint_pattern_count() {
  local count=0
  count=$((count + ${#ACCESSLINT_ARIA_PATTERNS[@]}))
  count=$((count + ${#ACCESSLINT_SEMANTIC_PATTERNS[@]}))
  count=$((count + ${#ACCESSLINT_KEYBOARD_PATTERNS[@]}))
  count=$((count + ${#ACCESSLINT_FORM_PATTERNS[@]}))
  count=$((count + ${#ACCESSLINT_VISUAL_PATTERNS[@]}))
  count=$((count + ${#ACCESSLINT_DYNAMIC_PATTERNS[@]}))
  echo "$count"
}

# List patterns by category
accesslint_list_patterns() {
  local filter_type="${1:-all}"
  local -n _patterns_ref

  case "$filter_type" in
    ARIA)      _patterns_ref=ACCESSLINT_ARIA_PATTERNS ;;
    SEMANTIC)  _patterns_ref=ACCESSLINT_SEMANTIC_PATTERNS ;;
    KEYBOARD)  _patterns_ref=ACCESSLINT_KEYBOARD_PATTERNS ;;
    FORM)      _patterns_ref=ACCESSLINT_FORM_PATTERNS ;;
    VISUAL)    _patterns_ref=ACCESSLINT_VISUAL_PATTERNS ;;
    DYNAMIC)   _patterns_ref=ACCESSLINT_DYNAMIC_PATTERNS ;;
    all)
      accesslint_list_patterns "ARIA"
      accesslint_list_patterns "SEMANTIC"
      accesslint_list_patterns "KEYBOARD"
      accesslint_list_patterns "FORM"
      accesslint_list_patterns "VISUAL"
      accesslint_list_patterns "DYNAMIC"
      return
      ;;
    *)
      echo "Unknown category: $filter_type"
      return 1
      ;;
  esac

  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description wcag recommendation <<< "$entry"
    # Skip placeholder patterns
    [[ "$regex" == PLACEHOLDER_* ]] && continue
    printf "%-8s %-8s %-8s %s\n" "$check_id" "$severity" "$wcag" "$description"
  done
}

# Get patterns array name for a category
get_patterns_for_category() {
  local category="$1"
  case "$category" in
    aria)      echo "ACCESSLINT_ARIA_PATTERNS" ;;
    semantic)  echo "ACCESSLINT_SEMANTIC_PATTERNS" ;;
    keyboard)  echo "ACCESSLINT_KEYBOARD_PATTERNS" ;;
    form)      echo "ACCESSLINT_FORM_PATTERNS" ;;
    visual)    echo "ACCESSLINT_VISUAL_PATTERNS" ;;
    dynamic)   echo "ACCESSLINT_DYNAMIC_PATTERNS" ;;
    *)         echo "" ;;
  esac
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}

# WCAG 2.1 success criterion reference
get_wcag_reference() {
  local check_id="$1"
  local prefix="${check_id%%-*}"
  case "$prefix" in
    AR) echo "WCAG 2.1 — 1.1.1 Non-text Content / 4.1.2 Name, Role, Value" ;;
    SH) echo "WCAG 2.1 — 1.3.1 Info and Relationships / 4.1.1 Parsing" ;;
    KB) echo "WCAG 2.1 — 2.1.1 Keyboard / 2.4.7 Focus Visible" ;;
    FM) echo "WCAG 2.1 — 1.3.1 Info and Relationships / 3.3.2 Labels or Instructions" ;;
    VS) echo "WCAG 2.1 — 1.4.1 Use of Color / 1.4.3 Contrast / 2.3.1 Three Flashes" ;;
    DY) echo "WCAG 2.1 — 4.1.2 Name, Role, Value / 4.1.3 Status Messages" ;;
    *)  echo "" ;;
  esac
}

# WCAG conformance level mapping
get_wcag_level() {
  local wcag_criterion="$1"
  case "$wcag_criterion" in
    1.1.1|1.2.1|1.2.2|1.2.3|1.3.1|1.3.2|1.3.3|1.4.1|1.4.2)  echo "A" ;;
    2.1.1|2.1.2|2.1.4|2.2.1|2.2.2|2.3.1|2.4.1|2.4.2|2.4.3|2.4.4|2.5.1|2.5.2|2.5.3|2.5.4) echo "A" ;;
    3.1.1|3.1.2|3.2.1|3.2.2|3.3.1|3.3.2) echo "A" ;;
    4.1.1|4.1.2|4.1.3) echo "A" ;;
    1.3.4|1.3.5|1.4.3|1.4.4|1.4.5|1.4.10|1.4.11|1.4.12|1.4.13) echo "AA" ;;
    2.4.5|2.4.6|2.4.7) echo "AA" ;;
    3.1.2|3.2.3|3.2.4|3.3.3|3.3.4) echo "AA" ;;
    1.4.6|1.4.7|1.4.8|1.4.9) echo "AAA" ;;
    2.4.8|2.4.9|2.4.10) echo "AAA" ;;
    *)  echo "A" ;;
  esac
}
