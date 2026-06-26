# 📐 Layout Templates (The Blueprint)

This directory maps vague user descriptions to concrete geometric layouts.

## Available Layouts

| Layout ID | Name | Description | User Intent Examples |
|-----------|------|-------------|----------------------|
| `hero-split` | Hero + Split Columns | Top banner, bottom divided columns | "Top 1/3 banner, bottom 3 columns" |
| `sidebar-fixed` | Fixed Sidebar | Left nav, right content | "Left menu, right dashboard" |
| `masonry-grid` | Masonry Grid | Staggered cards | "Pinterest style", "Photo wall" |
| `poster-zine` | Poster / Zine | Bold typography, overlap | "Magazine cover", "Event poster" |
| `mobile-feed` | Mobile Feed | Vertical stack, bottom nav | "Instagram feed", "Phone app" |

## Template Definition Schema

Each layout defines:
1.  **Structure**: HTML semantic structure (header, main, aside, footer).
2.  **CSS Strategy**: Grid/Flexbox code snippets.
3.  **Responsive Behavior**: How it breaks down on mobile.
