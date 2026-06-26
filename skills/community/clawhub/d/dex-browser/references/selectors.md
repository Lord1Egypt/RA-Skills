# CSS Selectors Reference

## Basics

| Selector | Matches |
|---|---|
| `#id` | Element with `id="id"` |
| `.class` | Elements with `class="class"` |
| `tag` | All `<tag>` elements |
| `tag.class` | `<tag>` elements with class |
| `tag#id` | `<tag>` with `id="id"` |

## Attributes

| Selector | Matches |
|---|---|
| `[attr]` | Elements with `attr` attribute |
| `[attr="value"]` | Elements where `attr="value"` |
| `[attr*="sub"]` | `attr` contains "sub" |
| `[attr^="start"]` | `attr` starts with "start" |
| `[attr$="end"]` | `attr` ends with "end" |

## Combinators

| Selector | Matches |
|---|---|
| `parent child` | `child` inside `parent` |
| `parent > child` | `child` direct child of `parent` |
| `el1, el2` | Both elements |
| `el.next` | `el` followed by `.next` sibling |

## Common UI Patterns

```css
/* Navigation links */
nav a
nav > ul > li > a
header [role="menuitem"]

/* Form inputs */
input[type="text"]
input[type="email"]
input[type="password"]
input[name="username"]
textarea[name="body"]
select[name="country"]

/* Buttons */
button[type="submit"]
button.btn-primary
button[class*="submit"]
input[type="submit"]
a[role="button"]

/* Article content */
article h1
article h2
.post-content p
.entry-content li

/* Lists of items */
.items > li
.card:not(:last-child)
.product-grid > div

/* Search results */
.search-result h3
.result-title a
.job-listing h2
.article-card

/* Tables */
table tr
table td:nth-child(1)
tbody tr td:first-child

/* Dynamic content */
[aria-expanded="true"]
[data-testid="results"]
[data-v-abc123]

/* Wait for element */
.wait-for-me
.loading:hidden
```

## XPath (when CSS isn't enough)

```python
# XPath selectors
page.locator('xpath=//button[text()="Submit"]')
page.locator('xpath=//div[contains(@class, "result")]')
page.locator('xpath=//a[starts-with(@href, "/products")]')
```

## Pseudo-selectors

```css
:first-child       /* First child of parent */
:last-child       /* Last child of parent */
:nth-child(n)     /* Nth child */
:nth-of-type(n)   /* Nth of this tag type */
:not(.exclude)    /* Not matching */
:hover             /* Mouse over (for events) */
:focus             /* Keyboard focus */
:checked           /* Checked inputs */
```

## Best Practices

1. **Prefer IDs** — `#specific-element` is fastest
2. **Be specific** — `.card` might match dozens of elements; `.product-card-123` is better
3. **Avoid deeply nested** — `body > div > div > div > .target` breaks easily
4. **Use data attributes** — `[data-testid="submit-btn"]` is stable
5. **Avoid text selectors** — `button:has-text("Submit")` works but text changes

## Debugging

```python
# Print all matching elements
page.evaluate("""() => {
    [...document.querySelectorAll('SELECTOR')].forEach((el, i) =>
        console.log(i, el.tagName, el.className, el.id, el.href || el.src)
    )
}""")
```
