# Ghost Helper Attributes

Reference for Ghost helper attributes and their usage.

## @config

| Attribute | Usage | Definition |
| ----------- | ------- | ------------ |
| posts_per_page | `@config.posts_per_page` | The number of posts per page as defined in `package.json` |
| image_sizes | `@config.image_sizes` | Responsive image sizes as defined in `package.json` |
| card_assets | `@config.card_assets` | Configure the card CSS and JS Ghost includes in `package.json` |

## {{#foreach}} and {{#get}} attributes

| Attribute | Usage | Definition |
| ----------- | ------- | ------------ |
| limit | `limit="3"` | Specifies a number of items to get |
| from | `from="3"` | Changes the starting point from which items are output |
| to | `to="8"` | Limits the number of items output |
| page | `page="4"` | Choose which page of a paginated collection to get |
| order | `order="published_at asc"` | Specify how data is ordered |
| include | `include="tags"` | Expand the data that is returned |
| filter | `filter="featured:true"` | Make complex, logic-based queries on the data |

## @site attributes

| Attribute | Usage | Definition |
| ----------- | ------- | ------------ |
| description | `{{@site.description}}` | Site description from General settings |
| icon | `{{@site.icon}}` | Publication icon from Design > Brand settings |
| logo | `{{@site.logo}}` | Publication logo from Design > Brand settings |
| cover_image | `{{@site.cover_image}}` | Publication cover image from Design > Brand settings |
| signup_url | `{{@site.signup_url}}` | URL for members signup via Portal or RSS |
| members_enabled | `{{@site.members_enabled}}` | `true` if subscription access is not set to Nobody |
| members_invite_only | `{{@site.members_invite_only}}` | `true` if access is set to Only people I invite |
| paid_members_enabled | `{{@site.paid_members_enabled}}` | `true` if members is enabled and Stripe is connected |
| meta_description | `{{@site.meta_description}}` | Site meta description |
| twitter_image | `{{@site.twitter_image}}` | Site Twitter image card |
| twitter_title | `{{@site.twitter_title}}` | Site Twitter card title |
| twitter_description | `{{@site.twitter_description}}` | Site Twitter card description |
| og_image | `{{@site.og_image}}` | Site open graph image |
| og_title | `{{@site.og_title}}` | Site open graph title |
| og_description | `{{@site.og_description}}` | Site open graph description |

Source: [Ghost Docs — Config Helper](https://ghost.org/docs/themes/helpers/config/) · [Ghost Docs — Site Helper](https://ghost.org/docs/themes/helpers/site/) · [Ghost Docs — Foreach Helper](https://ghost.org/docs/themes/helpers/foreach/) · [Ghost Docs — Get Helper](https://ghost.org/docs/themes/helpers/get/)
