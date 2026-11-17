# Ghost Utility Helpers

Reference for Ghost CMS utility helpers.

| Helper | Usage | Definition | Attributes |
| -------- | ------- | ------------ | ------------ |
| asset | `{{asset "css/style.css"}}` | Outputs cacheable, cache-busting URLs to assets | hasMinFile |
| block | `{{{block "name"}}}` | Creates a placeholder for child template content | — |
| contentFor | `{{#contentFor "name"}}...{{/contentFor}}` | Adds content to a block placeholder | — |
| default | `{{!< default}}` | Extends the default.hbs layout | — |
| body_class | `{{body_class}}` | Outputs dynamic CSS classes for `<body>` | — |
| concat | `{{concat "a" "b"}}` | Concatenates strings together | separator |
| encode | `{{encode value}}` | Encodes a string for URL use | — |
| ghost_head | `{{ghost_head}}` | Outputs metadata, scripts, and styles in `<head>` | — |
| ghost_foot | `{{ghost_foot}}` | Outputs code injection before `</body>` | — |
| link_class | `{{link_class for="/"}}` | Adds dynamic CSS classes for nav links | for, activeClass, class |
| log | `{{log value}}` | Debug output to server console | — |
| pagination | `{{pagination}}` | Outputs newer/older post navigation | page, prev, next, pages, total, limit, page_url |
| partials | `{{> "name"}}` | Includes a partial template | property |
| plural | `{{plural count}}` | Outputs singular/plural strings | empty, singular, plural |
| post_class | `{{post_class}}` | Outputs dynamic CSS classes for post container | — |
| prev_post | `{{#prev_post}}{{/prev_post}}` | Fetches previous post in order | in |
| next_post | `{{#next_post}}{{/next_post}}` | Fetches next post in order | in |
| reading_time | `{{reading_time}}` | Outputs estimated reading time | minute, minutes |
| search | `{{search}}` | Outputs a search button | — |
| translate | `{{t "text"}}` | Outputs text in the site's language | placeholder, subexpressions |

Source: [Ghost Docs — Helpers](https://ghost.org/docs/themes/helpers/)
