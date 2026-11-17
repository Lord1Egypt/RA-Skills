---
title: "comments"
description: 'Usage: `{{comments}}`'
---

***

The `{{comments}}` helper outputs Ghost’s member-based commenting system. [Learn more about comments.](https://ghost.org/help/commenting)

Comments are visible only when they have been (1) enabled by the publication owner and (2) the person visiting the page has access to the post.

### Basic example

```handlebars
{{comments}}
```

By default,`{{comments}}`outputs a title and comment count. These elements, along with the color mode and the saturation of the avatar's background color, can be customized via attributes.

## Attributes

- **Name**: `title`, **Description**: Header text for comment section, **Options**: Any string, **Default**: Member discussion
- **Name**: `count`, **Description**: Boolean to toggle comment count on or off, **Options**: `true` or `false`, **Default**: `true`
- **Name**: `mode`, **Description**: Set light or dark mode for comments, **Options**: auto, light, or dark, **Default**: auto (determined by the parent element's CSS `color` property)
- **Name**: `saturation`, **Description**: Set saturation of avatar background color, **Options**: `number`, **Default**: `60`

### Example with attributes

```handlebars
{{comments title="Join the club" count=false mode="light" saturation=80}}
{{! Customizes header text, hides comment count, sets element to light mode and avatar background color saturation to 80% }}
```

## Comment count

Use`{{comment_count}}` to output the number of comments a post has. This option is useful for displaying the comment count on the homepage or at the top of the post. Developers can also use it to customize the output of the`{{comments}}` helper.

### Attributes

- **Name**: `singular`, **Description**: The singular name for a comment, **Options**: Any string, **Default**: comment
- **Name**: `plural`, **Description**: The plural name for comments, **Options**: Any string, **Default**: comments
- **Name**: `empty`, **Description**: What to output when there are no comments, **Options**: Any string, **Default**: Output is empty when comment count equals zero
- **Name**: `autowrap`, **Description**: Wraps comment count in an HTML tag, **Options**: `HTML tag` or `false`, **Default**: `span`
- **Name**: `class`, **Description**: Add a custom class to wrapper element, **Options**: Any string, **Default**: ""

### Examples

```handlebars
{{comment_count empty="" singular="comment" plural="comments" autowrap="span" class=""}}
{{! default output: <span>5 comments</span> }}

{{comment_count singular="" plural=""}}
{{! output: <span>5</span> }}

{{comment_count empty="0"}}
{{! output: <span>0</span>. (The default is an empty output.) }}

{{comment_count autowrap="div" class="style-me"}}
{{! output: <div class="style-me">5 comments</span> }}

{{comment_count autowrap="false"}}
{{! output: 5 comments (just text!) }}
```

## Additional customization

Use the `comments` helper with `{{#if}}` for more granular control over output. `{{#if comments}}` returns true when (1) comments have been enabled and (2) the reader has access to the post.

### Advanced example

```handlebars
{{#if comments}}
   <h2>Discussion</h2>
   <a href="/guides">Community guidelines</a>
   {{comment_count}}
   {{comments title="" count=false mode="light" saturation=80}}
{{/if}}
```
