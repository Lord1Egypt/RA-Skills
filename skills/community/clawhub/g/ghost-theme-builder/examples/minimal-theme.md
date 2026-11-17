# Minimal theme shape

```text
theme/
  assets/css/screen.css
  partials/card.hbs
  default.hbs
  index.hbs
  post.hbs
  package.json
```

`default.hbs` owns the document shell. `index.hbs` renders a paginated post collection using `partials/card.hbs`; `post.hbs` renders one `#post` block. Extend this structure before adding `tag.hbs`, `author.hbs`, `page.hbs`, or custom templates.
