#!/usr/bin/env node
import { renderMermaidSVG, THEMES } from 'beautiful-mermaid'
import { readFileSync, writeFileSync } from 'fs'

// Custom brand themes (violet/indigo palette)
const BRAND = {
  'brand-dark': {
    bg: '#13194A',      // darkSidebar.950
    fg: '#EDE8FF',      // violet.100
    line: '#444A78',    // darkSidebar.800
    accent: '#8447FF',  // violet.500 (primary)
    muted: '#9196BF',   // darkSidebar.500
    surface: '#3C4168', // darkSidebar.900
    border: '#444A78',  // darkSidebar.800
  },
  'brand-light': {
    bg: '#FFFFFF',
    fg: '#111111',      // neutralGray.950
    line: '#D1D1D1',    // neutralGray.200
    accent: '#8447FF',  // violet.500 (primary)
    muted: '#888888',   // neutralGray.400
    surface: '#F5F2FF', // violet.50
    border: '#DCD4FF',  // violet.200
  },
}

const ALL_THEMES = { ...THEMES, ...BRAND }

const args = process.argv.slice(2)
const flags = {}
const positional = []

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--theme' && args[i + 1]) {
    flags.theme = args[++i]
  } else if (args[i] === '--transparent') {
    flags.transparent = true
  } else {
    positional.push(args[i])
  }
}

const input = positional[0]
const output = positional[1] || 'diagram.svg'

if (!input) {
  console.error('Usage: render-diagram.mjs <input.mmd> [output.svg] [--theme <name>] [--transparent]')
  console.error('       echo "graph TD; A-->B" | render-diagram.mjs - [output.svg]')
  console.error(`Themes: ${Object.keys(ALL_THEMES).join(', ')}`)
  process.exit(1)
}

let code
try {
  code = input === '-'
    ? readFileSync('/dev/stdin', 'utf8')
    : readFileSync(input, 'utf8')
} catch (err) {
  console.error(`Error reading input: ${err.message}`)
  process.exit(1)
}

const theme = flags.theme && ALL_THEMES[flags.theme]
  ? { ...ALL_THEMES[flags.theme] }
  : { ...BRAND['brand-dark'] }

if (flags.transparent) theme.transparent = true

try {
  const svg = renderMermaidSVG(code, { ...theme, padding: 48, nodeSpacing: 32, layerSpacing: 48 })
  writeFileSync(output, svg)
  console.log(`Rendered: ${output}`)
} catch (err) {
  console.error(`Error rendering diagram: ${err.message}`)
  process.exit(1)
}
