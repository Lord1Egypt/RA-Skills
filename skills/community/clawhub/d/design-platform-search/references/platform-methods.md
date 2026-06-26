# Platform Methods

## Shared Rules

- Use a real browser for search pages.
- Prefer search-card fields over detail-page fields.
- Keep `cover_image_url` from the search page unless the platform exposes an obvious tiny fixed-size variant.
- Use detail pages mainly for `publish_time`.
- In restricted networks, validate VPN/proxy reachability before changing selectors.

## Dribbble

### Search URL

`https://dribbble.com/search/<urlencoded-tag>`

### Search-page collection

- Query `a.shot-thumbnail-link.js-shot-link[href*="/shots/"]`.
- Keep only anchors whose `href` matches `/shots/<numeric-id>`.
- For `title`, prefer:
  - `.shot-title`
  - `img.alt`
  - anchor `title`
  - accessibility text
- For `cover_image_url`, prefer:
  - highest `srcset` candidate
  - or upgrade `resize=320x240|400x300|800x600` to a larger variant such as `1600x1200`
- For `author_name`, prefer non-shot profile links already visible on the card.
- For metrics, public cards may expose `likes`, `views`, and `comments`.

### Detail-page backfill

- Use detail pages mainly for `publish_time`.
- Useful public signals:
  - `article:published_time`
  - `og:updated_time`
  - JSON text fields such as `datePublished`, `uploadDate`, `dateCreated`
- Do not depend on detail pages for cover image or author unless search cards are clearly insufficient.

### Practical notes

- Public publish time is still unstable.
- Dribbble is usually the strongest source for `dashboard`, `scene3d`, `motion`, and UI-heavy `icon3d`.

## Pinterest

### Search URL

`https://www.pinterest.com/search/pins/?q=<urlencoded-tag>&rs=typed`

### Search-page collection

- Query `a[href*="/pin/"]`.
- Keep only anchors whose `href` matches `/pin/<numeric-id>/`.
- For `title`, prefer:
  - `img.alt`
  - `aria-label`
  - cleaned anchor text
- For `cover_image_url`, prefer the search-page image and only do light upgrades such as:
  - `236x -> 736x`
  - `474x -> 736x`
- Search cards rarely expose a reliable `author_name`; leave it empty if needed.

### Detail-page backfill

- Use detail pages only for `publish_time` when the environment can afford it.
- Preferred public field:
  - `meta[property="og:updated_time"]`
- On slow servers or VPN-only environments, disable Pinterest detail backfill and keep search-page-only extraction.

### Practical notes

- Pinterest is often the most network-sensitive source.
- Search cards are usually enough for `chart`, `icon3d`, and `color`.
- If the environment is slow, protect throughput by avoiding detail requests.

## Behance

### Search URL

`https://www.behance.net/search/projects?search=<urlencoded-tag>`

### Search-page collection

- Query `a.ProjectCoverNeue-coverLink-U39[href*="/gallery/"]`.
- Keep only anchors whose `href` matches `/gallery/<numeric-id>`.
- For `title`, prefer:
  - project title link text
  - `aria-label`
  - `title`
  - `img.alt`
- For `cover_image_url`, prefer:
  - `picture img`
  - `img` `srcset`
  - current `img.src`
- Search cards may not expose `author_name`; do not fabricate it.

### Detail-page backfill

- Use detail pages mainly for `publish_time`.
- Useful public signals:
  - page text patterns such as `发布时间`
  - `application/ld+json` with `VisualArtwork`
  - `datePublished`, `uploadDate`, `dateCreated`

### Practical notes

- Behance can be region-sensitive.
- It is strong for `dashboard`, `scene3d`, `chart`, and `icon3d`.
- Search-page covers are often good enough; do not force extra image enrichment unless they are placeholders.

## Proxy Notes

- Browser automation may work better through `socks5://...`.
- Image download and pHash download may need `http://...` mixed-port proxies even when the browser uses SOCKS5.
- When debugging a restricted server:
  - verify platform reachability with `curl`
  - verify the browser can load the search page
  - only then tune selectors or timeouts
