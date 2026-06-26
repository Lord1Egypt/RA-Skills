
# Defuddle Reference

## Basic usage

URL conversion:

curl defuddle.md/example.com/article

Returns markdown with YAML frontmatter.

## CLI

defuddle parse https://example.com/article --markdown

Options:

--markdown
--json
--property
--output

## Returned Metadata

- title
- author
- description
- site
- domain
- favicon
- image
- published
- wordCount
- parseTime
