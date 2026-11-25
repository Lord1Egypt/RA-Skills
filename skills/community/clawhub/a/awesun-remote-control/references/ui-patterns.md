# UI ELEMENT IDENTIFICATION REFERENCE

## COMMON UI ELEMENT FEATURE TABLE

### BUTTONS

| Type | Visual Feature | Common Location | Identification Key |
|------|----------|----------|----------|
| Primary button | Prominent background (blue, green, orange), rounded | Form bottom, action area | MOST VISIBLE action button |
| Secondary button | Light background or border only | Next to primary button | Lower contrast |
| Text button | Pure text, underlined or special color | Nav bar, toolbar | Simple, no background |
| Icon button | Icon only, no text | Title bar, toolbar | Search, settings, menu icons |
| Ghost button | Transparent background, bordered | Above images, banners | Does not affect background |

### INPUT FIELDS

| Type | Visual Feature | Common Location | Identification Key |
|------|----------|----------|----------|
| Single-line text | Rectangle, bordered or underlined | Form, search area | Placeholder text |
| Multi-line text | Larger rectangular area | Comments, description areas | Resizable |
| Search box | With magnifier icon | Page top, nav bar | Search button or icon |
| Password field | Dots or asterisks | Login form | May have show/hide toggle |
| Dropdown select | With down arrow | Form, filter area | Click to expand options |

### ICONS

| Icon Type | Visual Feature | Common Meaning | Identification Key |
|----------|----------|----------|----------|
| Hamburger menu | Three horizontal lines | Expand nav menu | Common on mobile |
| Magnifier | Circle plus handle | Search function | Often paired with search box |
| Gear | Circle with teeth | Settings | System/app settings |
| User/avatar | Person silhouette | User profile | Login, personal center |
| House | Roof shape | Home | Navigate to homepage |
| Heart | Heart shape | Favorite, like | Common in social apps |
| Bell | Bell shape | Notifications, alerts | New message indicator |
| Shopping cart | Cart shape | E-commerce cart | Shopping apps |
| Share | Three dots plus lines | Share function | Social media |
| Trash | Bin shape | Delete | Delete action |
| X/cross | X shape | Close, delete | Dialog close |
| Arrow | Directional line | Navigate, expand | Direction indicator |

### NAVIGATION

| Type | Visual Feature | Common Location | Identification Key |
|------|----------|----------|----------|
| Tab | Horizontally arranged text labels | Content area top | Current item HIGHLIGHTED |
| Breadcrumb | Path-style text links | Page top | Separated by ">" or "/" |
| Sidebar | Vertical menu list | Page left or right | Expandable/collapsible |
| Pagination | Page numbers or arrows | List bottom | Current page highlighted |
| Steps indicator | Circular nodes + lines | Wizard flow | Done, in-progress, pending states |

### FEEDBACK ELEMENTS

| Type | Visual Feature | Common Location | Identification Key |
|------|----------|----------|----------|
| Toast/message | Colored bar + text | Page top or action area | Success(green), error(red), warning(yellow), info(blue) |
| Loading animation | Spinning circle or progress bar | Action area | Waiting state |
| Badge/count | Small dot or number | Icon top-right | Unread count indicator |
| Tooltip | Bubble-shaped floating box | Mouse hover position | Explanatory note |

## LOCATION STRATEGY

### 1. WHOLE FIRST, THEN LOCAL

1. **UNDERSTAND PAGE STRUCTURE**
    - Identify main page areas (header, sidebar, content, footer)
    - Determine the element's rough region

2. **NARROW THE SEARCH AREA**
    - Define region per user description
    - Example: "top-right" → only look at upper-right of page

3. **PRECISE LOCATION**
    - Find the specific element within the defined area
    - Return CENTER POINT normalized coordinates

### 2. MULTI-FEATURE MATCHING

Combine these features to improve accuracy:
- **POSITION**: top-left, center, bottom-right, etc.
- **COLOR**: red, blue, green, etc.
- **SHAPE**: rectangle, circle, icon shape
- **TEXT**: button text, label content
- **CONTEXT**: adjacent elements, containing region

### 3. HANDLE AMBIGUITY

When user description may have multiple interpretations:

**EXAMPLE:** User says "find the cancel button"

Possible scenarios:
1. "Cancel" button at form bottom
2. "Cancel" action in a dialog
3. "Cancel" button in edit mode

**STRATEGY:**
- Prefer the MOST relevant option in current context
- List all possible options
- Request user clarification

## COORDINATE CALCULATION EXAMPLES

### EXAMPLE 1: STANDARD CENTERED BUTTON

Image size: 1920 x 1080
Button position: centered, size 200 x 50

Calculation:
```
Button center X = 1920 / 2 = 960
Button center Y = 1080 / 2 = 540

x_norm = 960 / 1920 = 0.5
y_norm = 540 / 1080 = 0.5
```

### EXAMPLE 2: TOP-RIGHT ICON

Image size: 1440 x 900
Icon position: top-right, 20px from right edge, 20px from top edge
Icon size: 24 x 24

Calculation:
```
Icon center X = 1440 - 20 - (24 / 2) = 1428
Icon center Y = 20 + (24 / 2) = 32

x_norm = 1428 / 1440 = 0.992
y_norm = 32 / 900 = 0.036
```

### EXAMPLE 3: BOTTOM FORM INPUT FIELD

Image size: 2560 x 1440
Input position: bottom form area
Input center: (800, 1200)

Calculation:
```
x_norm = 800 / 2560 = 0.313
y_norm = 1200 / 1440 = 0.833
```

## COMMON LAYOUT PATTERNS

### F-PATTERN LAYOUT
- User eye moves in F-shape from top-left to bottom-right
- Important elements usually on left and top
- Common in: news sites, blogs

### Z-PATTERN LAYOUT
- Eye moves top-left to top-right, diagonal to bottom-left, then bottom-right
- Fits: landing pages, marketing pages

### GRID LAYOUT
- Content arranged in grid
- Common in: image galleries, e-commerce product lists

### CARD LAYOUT
- Info packaged in standalone cards
- Common in: social media, dashboards

## RESPONSIVE CONSIDERATIONS

Element positions change across device sizes:

| Device Type | Width Range | Common Layout Changes |
|----------|----------|--------------|
| Mobile | < 576px | Single column, hamburger menu, bottom nav |
| Tablet | 576px - 992px | Two columns, collapsible sidebar |
| Desktop | > 992px | Multiple columns, full navigation |

**TIP:** User description may include device info, e.g. "find in the mobile screenshot..."

## DARK MODE vs LIGHT MODE

Consider theme when identifying elements:

**DARK MODE FEATURES:**
- Background: dark gray or black (#121212, #1e1e1e)
- Text: white or light gray
- Accent colors: more vivid variants

**LIGHT MODE FEATURES:**
- Background: white or light gray
- Text: dark gray or black
- Accent colors: standard colors

## ACCESSIBILITY HINTS

Some elements may have accessibility indicators:
- Focus state (highlighted border)
- Disabled state (gray, not clickable)
- Selected state (checkmark, highlighted background)

These states may affect element recognizability and position.
