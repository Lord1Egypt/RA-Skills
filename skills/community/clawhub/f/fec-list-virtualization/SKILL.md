---
name: fec-list-virtualization
description: Use when optimizing or reviewing large lists, virtual scrolling, windowing, react-window, TanStack Virtual, variable-height rows, dynamic measurement, infinite scroll, grid virtualization, or scroll performance; Chinese triggers include virtual lists, large list optimization, scroll performance.
---

# List virtualization optimization

## Purpose

Only the visible area is rendered through windowing, which solves the problem of excessive DOM and stuck scrolling in large lists.

## Procedure

1. First confirm the list size and bottleneck: 500+ items, scrolling frame drops, too many DOM nodes, or memory surge before introducing virtualization.
2. First follow the existing framework, dependencies and design system constraints of the project, and then select the library according to the scenario: React can consider `react-window` or TanStack Virtual; Vue/Solid/Svelte, dynamic measurement, grid or cross-framework scenarios give priority to TanStack Virtual; the legacy `react-virtualized` is only maintained and not added.
3. Clarify item size, overscan, container height, key, rolling container and resize behavior.
4. Separate data paging and DOM virtualization during infinite scrolling; data acquisition can be combined with the data acquisition workflow.
5. Verify DOM node count, scrolling FPS, keyboard/screen reader experience, and Ctrl+F/SEO limitations.

## Detailed reference

Load [references/virtualization-patterns.md](references/virtualization-patterns.md) when it comes to the need for virtualization, library selection, fixed height, variable/dynamic height, infinite scrolling, grid virtualization, and performance considerations.

## Constraints

- SEO key content doesn’t exist only in dummy items.
- Browser native Ctrl+F cannot search for unmounted items.
- The Row root element must transparently transmit the style/measure ref provided by the virtual library.
- If overscan is too high, memory will be wasted; if overscan is too low, the screen will be white.
- Dynamic height measurement to handle ResizeObserver and layout jitter.

## Expected Output

The scrolling of the 10,000+ item list is close to 60fps, the number of DOM nodes is stable within the visible area and buffer range, and the memory is reduced from O(n) to O(visible).
