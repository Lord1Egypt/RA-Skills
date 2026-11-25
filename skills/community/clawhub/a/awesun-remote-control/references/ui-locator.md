## OVERVIEW

Guide the AI vision model to identify UI element positions in desktop screenshots and return NORMALIZED coordinates. Use when analyzing screenshots, locating interface elements (buttons, input fields, icons, menus, etc.) and obtaining normalized position coordinates. Receives image path, understands user intent, outputs normalized coordinates (x_norm, y_norm) in range [0.0, 1.0].

## WORKFLOW

### 1. READ IMAGE

Use the `read` tool to load the screenshot file returned by `awesun-cli session screenshot`.

**STEPS:**
1. Screenshot defaults to the current directory where the command runs
2. Use `--output PATH` to specify output path
3. Use the `read` tool to load the image file
4. The AI vision model then "sees" the image content and analyzes it

**EXAMPLE:**
```bash
# Screenshot
awesun-cli session screenshot <session-id> --output /tmp/screen.png

# Read image for analysis (executed by AI)
read(filePath="/tmp/screen.png")
```

**SUPPORTED FORMATS:**
- PNG (.png)
- JPEG/JPG (.jpg, .jpeg)

**NOTES:**
- Image path MUST be ABSOLUTE
- File MUST EXIST and be readable
- After reading, the vision model auto-parses image content

### 2. UNDERSTAND USER INTENT

Parse the UI element the user wants to locate:
- BUTTONS (e.g. login button, submit button, cancel button)
- INPUT FIELDS (e.g. search box, username field, password field)
- ICONS (e.g. settings icon, menu icon, close button)
- TEXT ELEMENTS (e.g. title, link, label)
- OTHER UI components

### 3. VISUAL ANALYSIS

Use AI vision capability to analyze the image:

**ANALYSIS STEPS:**
1. Observe overall image layout structure
2. Identify each UI component
3. Match the target element per user description
4. Pinpoint the element's PIXEL position in the image
5. Compute normalized coordinates (may use `scripts/coordinates.py`)

**LOCATION TIPS:**
- Note the element's BOUNDING BOX
- Return the element CENTER POINT coordinates
- Consider visual features (color, shape, text, icon)
- Combine context (e.g. "settings button in top-right corner")

### 4. COMPUTE NORMALIZED COORDINATES

May use `scripts/coordinates.py` to assist.

**FORMULA:**
```
x_norm = x_pixel / image_width
y_norm = y_pixel / image_height
```

**RANGE:** [0.0, 1.0]

**COORDINATE SYSTEM:**
- TOP-LEFT origin (0.0, 0.0)
- BOTTOM-RIGHT is (1.0, 1.0)

### 5. RETURN RESULT

Output format:
```json
[
   {
      "found": true,
      "element": "element described by user",
      "coordinates": {
         "x": 0.523,
         "y": 0.234
      },
      "confidence": "high",
      "description": "blue login button at page center"
   }
]
```

**coordinates NOTES:**
- Contains NORMALIZED coords (x, y) in range [0.0, 1.0]
- Formula: x = pixel_x / image_width, y = pixel_y / image_height
- Coordinate system: TOP-LEFT origin (0.0, 0.0), BOTTOM-RIGHT (1.0, 1.0)

## EXAMPLE ANALYSES

### EXAMPLE 1: LOCATE LOGIN BUTTON

**USER INPUT:**
- Image: desktop screenshot
- Intent: "find the login button"

**ANALYSIS PROCESS:**
1. Read image, size 1920x1080
2. See a blue button near center-top with "login" text
3. Button center pixel coords approx (960, 450)
4. Compute normalized coords (may use `scripts/coordinates.py`):
    - x_norm = 960 / 1920 = 0.5
    - y_norm = 450 / 1080 = 0.417

**OUTPUT:**
```json
[
   {
      "found": true,
      "element": "login button",
      "coordinates": {
         "x": 0.5,
         "y": 0.417
      },
      "confidence": "high",
      "description": "blue button near center-top showing 'login' text"
   }
]
```

### EXAMPLE 2: LOCATE TOP-RIGHT MENU

**USER INPUT:**
- Image: app interface screenshot
- Intent: "the hamburger menu icon with three lines at top-right"

**ANALYSIS PROCESS:**
1. Read image, size 1440x900
2. See a hamburger menu icon (three lines) at top-right
3. Icon center pixel coords approx (1350, 60)
4. Compute normalized coords (may use `scripts/coordinates.py`):
    - x_norm = 1350 / 1440 = 0.9375
    - y_norm = 60 / 900 = 0.067

**OUTPUT:**
```json
[
   {
      "found": true,
      "element": "menu icon",
      "coordinates": {
         "x": 0.938,
         "y": 0.067
      },
      "confidence": "high",
      "description": "hamburger menu icon at top-right (three lines)"
   }
]
```

## COMMON UI ELEMENT IDENTIFICATION GUIDE

### BUTTONS
- Feature: rectangular or rounded-rectangular, may have border or background color
- Usually contains text or icon
- May have hover/click state hints

### INPUT FIELDS
- Feature: rectangular box, may have placeholder text
- Common types: text field, password field, search box
- Usually has border or underline

### ICONS
- Feature: small graphic element
- Common types: settings gear, menu hamburger, search magnifier, close X
- Usually located in toolbar or title bar

### TEXT ELEMENTS
- Title (large font, bold)
- Body (regular font size)
- Links (underlined or special color)
- Labels (for form fields)

### NAVIGATION ELEMENTS
- Tabs
- Breadcrumbs
- Pagination controls
- Sidebar menu items

## PRECISION LOCATION TIPS

1. **USE RELATIVE POSITION DESCRIPTIONS**
    - "top-left..."
    - "page center..."
    - "top-right..."
    - "bottom..."

2. **COMBINE COLOR AND STYLE**
    - "blue submit button"
    - "red warning icon"
    - "input field with gray background"

3. **COMBINE TEXT CONTENT**
    - "button showing 'confirm'"
    - "input field labeled 'search'"

4. **CONSIDER HIERARCHY**
    - "close button inside the dialog"
    - "settings option in the sidebar"

## HANDLE EDGE CASES

### MULTIPLE MATCHES
If multiple possible matches found:
1. Choose the one BEST matching user description
2. OR return all matches and explain differences
3. Let user confirm which one

### ELEMENT NOT FOUND
If target element cannot be identified:
```json
[
   {
      "found": false,
      "element": "element described by user",
      "reason": "no matching element found in the image",
      "suggestions": [
         "content may be outside the scroll area",
         "element may be obscured by other content",
         "description may be imprecise, try a more detailed description"
      ]
   }
]
```

### LOW CONFIDENCE MATCH
If confidence is low:
```json
[
   {
      "found": true,
      "element": "element described by user",
      "coordinates": {
         "x": 0.5,
         "y": 0.3
      },
      "confidence": "medium",
      "note": "possible match found, recommend user confirmation",
      "matched_description": "blue button near center-top (text unclear)"
   }
]
```

## COORDINATE VALIDATION

Before returning, validate coordinates are reasonable:
- Range: [0.0, 1.0]
- Center point should be within the element's visible area
- Consider element size, AVOID returning edge coordinates
- May use `python3 scripts/coordinates.py validate <x> <y>`

## REFERENCE

- `references/ui-patterns.md`: common UI element patterns and identification tips
