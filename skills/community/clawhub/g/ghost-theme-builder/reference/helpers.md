# Ghost Data Helpers

Reference for Ghost CMS data helpers.

| Helper | Usage | Attributes | Variables |
| -------- | ------- | ------------ | ----------- |
| config | `@config.posts_per_page` | posts_per_page, image_sizes, card_assets, custom | — |
| custom | `@custom.property` | — | — |
| site | `@site.property` | url, title, description, icon, logo, cover_image, twitter, facebook, navigation, timezone, locale, signup_url, members_enabled, members_invite_only, paid_members_enabled, meta_title, meta_description, twitter_image, twitter_title, twitter_description, og_title, og_description | — |
| authors | `{{authors}}` | separator, prefix, autolink, limit, from, to, visibility | id, name, slug, bio, website, location, twitter, facebook, profile_image, cover_image, meta_title, meta_description, url |
| comments | `{{comments}}` | title, count, mode, saturation | — |
| comment_count | `{{comment_count}}` | singular, plural, empty, autowrap, class | — |
| content | `{{content}}` | words | — |
| date | `{{date published_at}}` | format, locale, timezone, timeago | — |
| excerpt | `{{excerpt}}` | words, characters | — |
| facebook_url | `{{facebook_url}}` | — | — |
| img_url | `{{img_url feature_image}}` | absolute, size, format | — |
| link | `{{#link href=""}}` | activeClass | — |
| navigation | `{{navigation}}` | type | — |
| post | `{{#post}}{{/post}}` | — | id, comment_id, title, slug, excerpt, content, url, feature_image, feature_image_alt, feature_image_caption, featured, page, meta_title, meta_description, published_at, updated_at, created_at, primary_author, tags, primary_tag |
| price | `{{price plan}}` | currency, locale, numberFormat, currencyFormat | — |
| tags | `{{tags}}` | separator, prefix, autolink, limit, from, to, visibility | — |
| tiers | `{{tiers}}` | prefix, separator, lastSeparator, suffix | — |
| title | `{{title}}` | — | — |
| total_members | `{{total_members}}` | — | — |
| total_paid_members | `{{total_paid_members}}` | — | — |
| twitter_url | `{{twitter_url}}` | — | — |
| url | `{{url}}` | absolute | — |
| @page | `@page` | show_title_and_feature_image | — |
| @member | `@member` | paid | — |

Source: [Ghost Docs — Helpers](https://ghost.org/docs/themes/helpers/)
