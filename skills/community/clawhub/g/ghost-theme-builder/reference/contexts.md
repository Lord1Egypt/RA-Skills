# Ghost Contexts

Each page in a Ghost theme belongs to a context, which determines the template used, data available, and what `{{body_class}}` outputs.

| Context | Detection | Description |
| --------- | ----------- | ------------- |
| index | `{{#is "index"}}{{/is}}` | Any page with a collection of posts (home, author, tag pages) |
| page | `{{#is "page"}}{{/is}}` | A static page |
| post | `{{#is "post"}}{{/is}}` | A single post |
| author | `{{#author}}...{{/author}}` | Author archive page listing their posts |
| tag | `{{#tag}}...{{/tag}}` | Tag archive page listing posts with that tag |
| error | Use in `error.hbs` | 4xx and 5xx error pages |

Source: [Ghost Docs — Contexts](https://ghost.org/docs/themes/contexts/)
