# UI Design Patterns — Figma Best Practices

## Layout Patterns

### Z-Pattern Layout
- Usato per landing page e hero sections
- L'occhio umano scansiona da in alto a sinistra a in basso a destra
- Posiziona elementi chiave lungo questo percorso

### F-Pattern Layout
- Prevalente in pagine content-heavy (blog, documentazione)
- L'utente scansiona la prima riga completa, poi le successive solo a sinistra
- Dai più peso ai primi elementi di ogni riga

### Grid System
- Standard 12-column grid per design responsive
- Gutter: 16-24px
- Margin: 24-80px (desktop), 16-24px (mobile)

## Component Patterns

### Card Component
- Corner radius: 8-16px
- Shadow: blurred drop shadow con opacità 10-20%
- Padding interno: 16-24px

### Button
- Minimum touch target: 48×48px
- Padding orizzontale: 16-32px
- Padding verticale: 12-16px
- Border radius: 6-12px
- State: default, hover, active, disabled

### Input Field
- Height: 40-56px
- Padding: 12-16px
- Border: 1-2px solid
- Label: 12-14px sopra il campo
- Error state: colore rosso + messaggio sotto

## Navigation

### Top Navigation
- Height: 56-80px
- Padding: 16-24px
- Active state: underline o fill color
- Logo: lato sinistro, nav items: centro o destra

### Sidebar Navigation
- Width: 240-320px
- Item height: 40-48px
- Padding: 12-16px
- Active state: background highlight

## Typography Scale

| Role | Size | Weight | Example |
|------|------|--------|---------|
| Display | 48-96px | Bold/ExtraBold | H1 hero |
| Heading 1 | 32-48px | Bold | Section title |
| Heading 2 | 24-32px | SemiBold | Subsection |
| Heading 3 | 20-24px | Medium | Card title |
| Body | 14-18px | Regular | Paragraph |
| Small | 12-14px | Regular | Caption, meta |
| Label | 11-13px | Medium | Button, badge |

## Color Systems

### Accessible Palettes
- Primary: colore brand principale
- Secondary: colore brand di supporto
- Neutral: scala di grigi per testi e sfondi
- Success: verde (#2ECC71)
- Warning: arancione (#F39C12)
- Error: rosso (#E74C3C)
- Info: blu (#3498DB)

### Contrast Guidelines
- Text on dark bg: rapporto ≥ 4.5:1 (AA), ≥ 7:1 (AAA)
- Large text (≥18px bold or ≥24px regular): ≥ 3:1 (AA), ≥ 4.5:1 (AAA)
- Interactive elements: focus state visible, non solo colore

## Spacing System

Base unit: 4px o 8px

| Token | Size | Usage |
|-------|------|-------|
| xs | 4px | Gap tra icone e testo |
| sm | 8px | Padding compatto |
| md | 16px| Padding standard |
| lg | 24px| Gap tra sezioni |
| xl | 32px| Margin tra blocchi |
| 2xl | 48px | Sezioni maggiori |
| 3xl | 64px| Hero/section margin |
