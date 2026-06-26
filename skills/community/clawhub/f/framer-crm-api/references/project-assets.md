# Project Assets & Configuration

Reference for managing non-CMS project assets: styles, code files, fonts, pages, localization, and redirects.

---

## Color styles

```javascript
// List all
const styles = await framer.getColorStyles()

// Get by ID
const style = await framer.getColorStyle("styleId")

// Create
const newStyle = await framer.createColorStyle({
  name: "Brand Blue",
  light: "rgba(59, 130, 246, 1)",
  dark: "rgba(96, 165, 250, 1)",  // optional dark mode variant
})
```

---

## Text styles

```javascript
// List all
const styles = await framer.getTextStyles()

// Get by ID
const style = await framer.getTextStyle("styleId")

// Create
const newStyle = await framer.createTextStyle({
  name: "Heading 1",
  font: "Inter",
  fontSize: 48,
  fontWeight: 700,
  lineHeight: "1.2",
  letterSpacing: "-0.02em",
})
```

---

## Code files (overrides)

Custom code files that can be attached to Framer components.

```javascript
// List all
const files = await framer.getCodeFiles()

// Get by ID
const file = await framer.getCodeFile("fileId")

// Create — takes two positional arguments: (name, code)
const newFile = await framer.createCodeFile(
  "analytics.js",
  `export default function Analytics() { console.log("loaded") }`
)
```

---

## Custom code injection

Get the head/body code injection slots:

```javascript
const customCode = await framer.getCustomCode()
// Returns head and body injection content
```

---

## Fonts

```javascript
const fonts = await framer.getFonts()
for (const font of fonts) {
  console.log(font.family, font.style, font.weight)
}
```

---

## Pages

### Create a page

```javascript
const page = await framer.createWebPage("/blog/new-page")
```

### Remove a page

```javascript
await framer.removeNode(page.id)
```

### List pages

```javascript
const pages = await framer.getNodesWithType("WebPageNode")
```

---

## Node tree traversal

```javascript
// Get root
const root = await framer.getCanvasRoot()

// Navigate
const children = await framer.getChildren(nodeId)
const parent = await framer.getParent(nodeId)
const node = await framer.getNode(nodeId)

// Read text content
const text = await framer.getText(nodeId)
```

---

## Screenshots

Capture a PNG screenshot of any node:

```javascript
const buffer = await framer.screenshot(nodeId, { format: "png" })
// Returns a Buffer with the PNG image data
```

---

## Localization

```javascript
// Current project locales
const locales = await framer.getLocales()
const defaultLocale = await framer.getDefaultLocale()

// All available languages
const languages = await framer.getLocaleLanguages()

// Localization groups (pages/CMS items grouped for translation)
const groups = await framer.getLocalizationGroups()
```

---

## Redirects (paid plans only)

```javascript
// List
const redirects = await framer.getRedirects()

// Add
await framer.addRedirects([
  { from: "/old-path", to: "/new-path", expandToAllLocales: true }
])
```

Note: Redirects require a paid Framer plan. Free plans will get an error.

---

## Vector sets (icons)

```javascript
const sets = await framer.getVectorSets()
// Lists available icon sets (Iconic, Phosphor, Hero Icons, Feather, etc.)
```
