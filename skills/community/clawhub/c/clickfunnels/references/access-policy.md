# ClickFunnels access policy

An access policy limits which endpoints ClickFunnels connections may call through Maton. ClickFunnels doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/clickfunnels#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for ClickFunnels: its 232 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create clickfunnels --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v2/addresses/countries"},
    {"method": "GET", "path": "api/v2/addresses/countries/{id}"},
    {"method": "GET", "path": "api/v2/addresses/countries/{id}/regions"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/appointments/scheduled_events"},
    {"method": "GET", "path": "api/v2/blogs/authors/{id}"},
    {"method": "GET", "path": "api/v2/blogs/categories/{id}"},
    {"method": "GET", "path": "api/v2/blogs/posts/{id}"},
    {"method": "GET", "path": "api/v2/blogs/tags/{id}"},
    {"method": "GET", "path": "api/v2/blogs/{id}"},
    {"method": "GET", "path": "api/v2/blogs/{id}/authors"},
    {"method": "GET", "path": "api/v2/blogs/{id}/categories"},
    {"method": "GET", "path": "api/v2/blogs/{id}/posts"},
    {"method": "GET", "path": "api/v2/blogs/{id}/tags"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/blogs"},
    {"method": "GET", "path": "api/v2/communities/bans/export_actions/{id}"},
    {"method": "GET", "path": "api/v2/communities/bans/unban_actions/{id}"},
    {"method": "GET", "path": "api/v2/communities/bans/{id}"},
    {"method": "GET", "path": "api/v2/communities/memberships/add_to_group_actions/{id}"},
    {"method": "GET", "path": "api/v2/communities/memberships/ban_actions/{id}"},
    {"method": "GET", "path": "api/v2/communities/memberships/export_actions/{id}"},
    {"method": "GET", "path": "api/v2/communities/memberships/remove_from_group_actions/{id}"},
    {"method": "GET", "path": "api/v2/communities/memberships/{id}"},
    {"method": "GET", "path": "api/v2/communities/space_groups/{id}"},
    {"method": "GET", "path": "api/v2/communities/space_groups/{id}/spaces"},
    {"method": "GET", "path": "api/v2/communities/spaces/posts/comments/{id}"},
    {"method": "GET", "path": "api/v2/communities/spaces/posts/comments/{id}/likes"},
    {"method": "GET", "path": "api/v2/communities/spaces/posts/video_embeds/{id}"},
    {"method": "GET", "path": "api/v2/communities/spaces/posts/{id}"},
    {"method": "GET", "path": "api/v2/communities/spaces/posts/{id}/comments"},
    {"method": "GET", "path": "api/v2/communities/spaces/posts/{id}/likes"},
    {"method": "GET", "path": "api/v2/communities/spaces/posts/{id}/video_embeds"},
    {"method": "GET", "path": "api/v2/communities/spaces/{id}"},
    {"method": "GET", "path": "api/v2/communities/spaces/{id}/posts"},
    {"method": "GET", "path": "api/v2/communities/{id}"},
    {"method": "GET", "path": "api/v2/communities/{id}/bans"},
    {"method": "GET", "path": "api/v2/communities/{id}/bans/export_actions"},
    {"method": "GET", "path": "api/v2/communities/{id}/memberships"},
    {"method": "GET", "path": "api/v2/communities/{id}/memberships/export_actions"},
    {"method": "GET", "path": "api/v2/communities/{id}/space_groups"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/communities"},
    {"method": "GET", "path": "api/v2/contacts/applied_tags/{id}"},
    {"method": "GET", "path": "api/v2/contacts/enroll_actions/{id}"},
    {"method": "GET", "path": "api/v2/contacts/events/notes/{id}"},
    {"method": "GET", "path": "api/v2/contacts/events/{id}"},
    {"method": "GET", "path": "api/v2/contacts/export_actions/{id}"},
    {"method": "GET", "path": "api/v2/contacts/filters/{id}"},
    {"method": "GET", "path": "api/v2/contacts/run_workflow_actions/{id}"},
    {"method": "GET", "path": "api/v2/contacts/subscription_changes/{id}"},
    {"method": "GET", "path": "api/v2/contacts/tag_actions/{id}"},
    {"method": "GET", "path": "api/v2/contacts/tags/{id}"},
    {"method": "GET", "path": "api/v2/contacts/unsubscribe_actions/{id}"},
    {"method": "GET", "path": "api/v2/contacts/unsubscribed_topics/{id}"},
    {"method": "GET", "path": "api/v2/contacts/{id}"},
    {"method": "GET", "path": "api/v2/contacts/{id}/applied_tags"},
    {"method": "GET", "path": "api/v2/contacts/{id}/billing_address"},
    {"method": "GET", "path": "api/v2/contacts/{id}/events"},
    {"method": "GET", "path": "api/v2/contacts/{id}/events/notes"},
    {"method": "GET", "path": "api/v2/contacts/{id}/shipping/addresses"},
    {"method": "GET", "path": "api/v2/contacts/{id}/subscription_changes"},
    {"method": "GET", "path": "api/v2/contacts/{id}/unsubscribed_topics"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/contacts"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/contacts/enroll_actions"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/contacts/export_actions"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/contacts/run_workflow_actions"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/contacts/tag_actions"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/contacts/tags"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/contacts/unsubscribe_actions"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/contacts/unsubscribed_topics"},
    {"method": "GET", "path": "api/v2/courses/enrollments/{id}"},
    {"method": "GET", "path": "api/v2/courses/lesson_completions/{id}"},
    {"method": "GET", "path": "api/v2/courses/lessons/{id}"},
    {"method": "GET", "path": "api/v2/courses/sections/publish_actions/{id}"},
    {"method": "GET", "path": "api/v2/courses/sections/{id}"},
    {"method": "GET", "path": "api/v2/courses/sections/{id}/lessons"},
    {"method": "GET", "path": "api/v2/courses/{id}"},
    {"method": "GET", "path": "api/v2/courses/{id}/enrollments"},
    {"method": "GET", "path": "api/v2/courses/{id}/lesson_completions"},
    {"method": "GET", "path": "api/v2/courses/{id}/sections"},
    {"method": "GET", "path": "api/v2/courses/{id}/sections/publish_actions"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/courses"},
    {"method": "GET", "path": "api/v2/discounts/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/discounts"},
    {"method": "GET", "path": "api/v2/domains/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/domains"},
    {"method": "GET", "path": "api/v2/downloads/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/downloads"},
    {"method": "GET", "path": "api/v2/emails/addresses/{id}"},
    {"method": "GET", "path": "api/v2/emails/broadcasts/send_actions/{id}"},
    {"method": "GET", "path": "api/v2/emails/broadcasts/{id}"},
    {"method": "GET", "path": "api/v2/emails/broadcasts/{id}/send_actions"},
    {"method": "GET", "path": "api/v2/emails/broadcasts/{id}/sent_content"},
    {"method": "GET", "path": "api/v2/emails/broadcasts/{id}/stats"},
    {"method": "GET", "path": "api/v2/emails/domains/{id}"},
    {"method": "GET", "path": "api/v2/emails/templates/{id}"},
    {"method": "GET", "path": "api/v2/emails/topics/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/emails/addresses"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/emails/broadcasts"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/emails/domains"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/emails/settings"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/emails/templates"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/emails/topics"},
    {"method": "GET", "path": "api/v2/form_submissions/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/form_submissions"},
    {"method": "GET", "path": "api/v2/forms/field_sets/{id}"},
    {"method": "GET", "path": "api/v2/forms/field_sets/{id}/fields"},
    {"method": "GET", "path": "api/v2/forms/fields/options/{id}"},
    {"method": "GET", "path": "api/v2/forms/fields/{id}"},
    {"method": "GET", "path": "api/v2/forms/fields/{id}/options"},
    {"method": "GET", "path": "api/v2/forms/submissions/answers/{id}"},
    {"method": "GET", "path": "api/v2/forms/submissions/{id}"},
    {"method": "GET", "path": "api/v2/forms/submissions/{id}/answers"},
    {"method": "GET", "path": "api/v2/forms/{id}"},
    {"method": "GET", "path": "api/v2/forms/{id}/field_sets"},
    {"method": "GET", "path": "api/v2/forms/{id}/submissions"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/forms"},
    {"method": "GET", "path": "api/v2/fulfillments/locations/{id}"},
    {"method": "GET", "path": "api/v2/fulfillments/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/fulfillments"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/fulfillments/locations"},
    {"method": "GET", "path": "api/v2/funnels/clone_actions/{id}"},
    {"method": "GET", "path": "api/v2/funnels/tags/{id}"},
    {"method": "GET", "path": "api/v2/funnels/{id}"},
    {"method": "GET", "path": "api/v2/funnels/{id}/clone_actions"},
    {"method": "GET", "path": "api/v2/funnels/{id}/conditional_split_steps"},
    {"method": "GET", "path": "api/v2/funnels/{id}/conditional_split_steps/{id}"},
    {"method": "GET", "path": "api/v2/funnels/{id}/split_test_steps"},
    {"method": "GET", "path": "api/v2/funnels/{id}/split_test_steps/{id}"},
    {"method": "GET", "path": "api/v2/funnels/{id}/stats"},
    {"method": "GET", "path": "api/v2/funnels/{id}/structure"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/funnels"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/funnels/tags"},
    {"method": "GET", "path": "api/v2/images/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/images"},
    {"method": "GET", "path": "api/v2/me"},
    {"method": "GET", "path": "api/v2/orders/applied_tags/{id}"},
    {"method": "GET", "path": "api/v2/orders/invoices/restocks/{id}"},
    {"method": "GET", "path": "api/v2/orders/invoices/{id}"},
    {"method": "POST", "path": "api/v2/orders/line_items/{id}/changes"},
    {"method": "GET", "path": "api/v2/orders/tags/{id}"},
    {"method": "GET", "path": "api/v2/orders/transactions/{id}"},
    {"method": "GET", "path": "api/v2/orders/{id}"},
    {"method": "GET", "path": "api/v2/orders/{id}/applied_tags"},
    {"method": "GET", "path": "api/v2/orders/{id}/invoices"},
    {"method": "GET", "path": "api/v2/orders/{id}/transactions"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/orders"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/orders/invoices"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/orders/invoices/restocks"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/orders/tags"},
    {"method": "GET", "path": "api/v2/pages/{id}"},
    {"method": "GET", "path": "api/v2/pages/{id}/custom_html"},
    {"method": "GET", "path": "api/v2/pages/{id}/stats"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/pages"},
    {"method": "GET", "path": "api/v2/products/collections/{id}"},
    {"method": "GET", "path": "api/v2/products/prices/{id}"},
    {"method": "GET", "path": "api/v2/products/prices/{id}/change_options"},
    {"method": "GET", "path": "api/v2/products/tags/{id}"},
    {"method": "GET", "path": "api/v2/products/variants/{id}"},
    {"method": "GET", "path": "api/v2/products/{id}"},
    {"method": "GET", "path": "api/v2/products/{id}/prices"},
    {"method": "GET", "path": "api/v2/products/{id}/variants"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/products"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/products/collections"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/products/tags"},
    {"method": "GET", "path": "api/v2/refine_filters/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/refine_filters"},
    {"method": "GET", "path": "api/v2/sales/opportunities/notes/{id}"},
    {"method": "GET", "path": "api/v2/sales/opportunities/{id}"},
    {"method": "GET", "path": "api/v2/sales/opportunities/{id}/notes"},
    {"method": "GET", "path": "api/v2/sales/pipelines/stages/{id}"},
    {"method": "GET", "path": "api/v2/sales/pipelines/{id}"},
    {"method": "GET", "path": "api/v2/sales/pipelines/{id}/stages"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/sales/opportunities"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/sales/pipelines"},
    {"method": "GET", "path": "api/v2/segments/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/segments"},
    {"method": "GET", "path": "api/v2/shipping/addresses/{id}"},
    {"method": "GET", "path": "api/v2/shipping/location_groups/{id}"},
    {"method": "GET", "path": "api/v2/shipping/location_groups/{id}/zones"},
    {"method": "GET", "path": "api/v2/shipping/packages/{id}"},
    {"method": "GET", "path": "api/v2/shipping/profiles/{id}"},
    {"method": "GET", "path": "api/v2/shipping/profiles/{id}/location_groups"},
    {"method": "GET", "path": "api/v2/shipping/rates/names/{id}"},
    {"method": "GET", "path": "api/v2/shipping/rates/{id}"},
    {"method": "GET", "path": "api/v2/shipping/zones/{id}"},
    {"method": "GET", "path": "api/v2/shipping/zones/{id}/rates"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/shipping/packages"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/shipping/profiles"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/shipping/rates/names"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/site"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/stats"},
    {"method": "GET", "path": "api/v2/stores/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/stores"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/styles"},
    {"method": "GET", "path": "api/v2/survey_workflows/runs/{id}"},
    {"method": "GET", "path": "api/v2/survey_workflows/{id}"},
    {"method": "GET", "path": "api/v2/survey_workflows/{id}/runs"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/survey_workflows"},
    {"method": "GET", "path": "api/v2/teams"},
    {"method": "GET", "path": "api/v2/teams/{id}"},
    {"method": "GET", "path": "api/v2/teams/{id}/workspaces"},
    {"method": "GET", "path": "api/v2/themes/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/themes"},
    {"method": "GET", "path": "api/v2/url_redirects/{id}"},
    {"method": "GET", "path": "api/v2/url_redirects/{id}/stats"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/url_redirects"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/url_redirects/availability"},
    {"method": "GET", "path": "api/v2/users"},
    {"method": "GET", "path": "api/v2/users/{id}"},
    {"method": "GET", "path": "api/v2/videos/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/videos"},
    {"method": "GET", "path": "api/v2/webhooks/incoming/external_purchase_endpoints/{id}"},
    {"method": "GET", "path": "api/v2/webhooks/incoming/external_purchase_endpoints/{id}/events"},
    {"method": "GET", "path": "api/v2/webhooks/incoming/external_purchase_endpoints/{id}/product_mappings"},
    {"method": "GET", "path": "api/v2/webhooks/incoming/external_purchase_events/{id}"},
    {"method": "GET", "path": "api/v2/webhooks/incoming/external_purchase_product_mappings/{id}"},
    {"method": "GET", "path": "api/v2/webhooks/outgoing/endpoints/{id}"},
    {"method": "GET", "path": "api/v2/webhooks/outgoing/event_types"},
    {"method": "GET", "path": "api/v2/webhooks/outgoing/events/{id}"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/webhooks/incoming/external_purchase_endpoints"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/webhooks/outgoing/endpoints"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/webhooks/outgoing/events"},
    {"method": "GET", "path": "api/v2/workflows/runs/{id}"},
    {"method": "GET", "path": "api/v2/workflows/steps/{id}"},
    {"method": "GET", "path": "api/v2/workflows/steps/{id}/stats"},
    {"method": "GET", "path": "api/v2/workflows/triggers/{id}"},
    {"method": "GET", "path": "api/v2/workflows/{id}"},
    {"method": "GET", "path": "api/v2/workflows/{id}/runs"},
    {"method": "GET", "path": "api/v2/workflows/{id}/steps"},
    {"method": "GET", "path": "api/v2/workflows/{id}/structure"},
    {"method": "GET", "path": "api/v2/workflows/{id}/triggers"},
    {"method": "GET", "path": "api/v2/workspaces/{id}/workflows"},
    {"method": "GET", "path": "api/v2/workspaces/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The ClickFunnels endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/v2/addresses/countries | read | addresses | List all countries, each with its ISO 3166-1 alpha-2 code (iso2). |
| GET | api/v2/addresses/countries/{id} | read | addresses | Retrieve a single country by its ISO 3166-1 alpha-2 code. |
| GET | api/v2/addresses/countries/{id}/regions | read | addresses | List the regions (states/provinces) of a country. |
| GET | api/v2/workspaces/{id}/appointments/scheduled_events | read | appointments | List Scheduled Events. |
| GET | api/v2/blogs/authors/{id} | read | blogs | Retrieve a blog author. |
| GET | api/v2/blogs/categories/{id} | read | blogs | Retrieve a blog category. |
| GET | api/v2/blogs/posts/{id} | read | blogs | Retrieve a blog post. |
| PATCH | api/v2/blogs/posts/{id} | write | blogs | Update a blog post. |
| DELETE | api/v2/blogs/posts/{id} | write | blogs | Delete a blog post. |
| GET | api/v2/blogs/tags/{id} | read | blogs | Retrieve a blog tag. |
| GET | api/v2/blogs/{id} | read | blogs | Retrieve a blog. |
| PATCH | api/v2/blogs/{id} | write | blogs | Update a blog's metadata. |
| GET | api/v2/blogs/{id}/authors | read | blogs | List the authors within the given blog. |
| GET | api/v2/blogs/{id}/categories | read | blogs | List the categories within the given blog. |
| GET | api/v2/blogs/{id}/posts | read | blogs | List posts for the given blog. |
| POST | api/v2/blogs/{id}/posts | write | blogs | Create a new post within the given blog. |
| GET | api/v2/blogs/{id}/tags | read | blogs | List tags for the given blog. |
| POST | api/v2/blogs/{id}/tags | write | blogs | Create a new tag within the given blog. |
| GET | api/v2/workspaces/{id}/blogs | read | blogs | List blogs for the given workspace. |
| GET | api/v2/communities/bans/export_actions/{id} | read | communities | Retrieve the current status of a ban export action. |
| GET | api/v2/communities/bans/unban_actions/{id} | read | communities | Retrieve the current status of a ban unban action. |
| GET | api/v2/communities/bans/{id} | read | communities | Retrieve a community ban. |
| DELETE | api/v2/communities/bans/{id} | write | communities | Unban a contact from a community. |
| GET | api/v2/communities/memberships/add_to_group_actions/{id} | read | communities | Retrieve the current status of a membership add-to-group action. |
| GET | api/v2/communities/memberships/ban_actions/{id} | read | communities | Retrieve the current status of a membership ban action. |
| GET | api/v2/communities/memberships/export_actions/{id} | read | communities | Retrieve the current status of a membership export action. |
| GET | api/v2/communities/memberships/remove_from_group_actions/{id} | read | communities | Retrieve the current status of a membership remove-from-group action. |
| GET | api/v2/communities/memberships/{id} | read | communities | Retrieve a community membership. |
| PUT | api/v2/communities/memberships/{id} | write | communities | Update a community membership (e.g. |
| DELETE | api/v2/communities/memberships/{id} | write | communities | Remove a contact's membership from a community. |
| GET | api/v2/communities/space_groups/{id} | read | communities | Retrieve a space group. |
| PUT | api/v2/communities/space_groups/{id} | write | communities | Update a space group. |
| DELETE | api/v2/communities/space_groups/{id} | write | communities | Delete a space group. |
| GET | api/v2/communities/space_groups/{id}/spaces | read | communities | List spaces within a space group. |
| POST | api/v2/communities/space_groups/{id}/spaces | write | communities | Create a space within a space group. |
| DELETE | api/v2/communities/spaces/posts/comments/likes/{id} | write | communities | Unlike a comment by deleting the like record. |
| GET | api/v2/communities/spaces/posts/comments/{id} | read | communities | Retrieve a comment. |
| PUT | api/v2/communities/spaces/posts/comments/{id} | write | communities | Update a comment. |
| DELETE | api/v2/communities/spaces/posts/comments/{id} | write | communities | Delete a comment. |
| POST | api/v2/communities/spaces/posts/comments/{id}/approve | write | communities | Approve a comment. |
| POST | api/v2/communities/spaces/posts/comments/{id}/decline | write | communities | Decline a comment. |
| POST | api/v2/communities/spaces/posts/comments/{id}/dismiss_reports | write | communities | Clear the comment's report flags (reported_at, report_count, report_type) and approve it. |
| GET | api/v2/communities/spaces/posts/comments/{id}/likes | read | communities | List likes for a comment. |
| POST | api/v2/communities/spaces/posts/comments/{id}/likes | write | communities | Like a comment. |
| DELETE | api/v2/communities/spaces/posts/likes/{id} | write | communities | Unlike a post by deleting the like record. |
| GET | api/v2/communities/spaces/posts/video_embeds/{id} | read | communities | Retrieve a video embed. |
| DELETE | api/v2/communities/spaces/posts/video_embeds/{id} | write | communities | Delete a video embed from a post. |
| GET | api/v2/communities/spaces/posts/{id} | read | communities | Retrieve a post. |
| PUT | api/v2/communities/spaces/posts/{id} | write | communities | Update a post. |
| DELETE | api/v2/communities/spaces/posts/{id} | write | communities | Delete a post. |
| POST | api/v2/communities/spaces/posts/{id}/approve | write | communities | Approve a post. |
| GET | api/v2/communities/spaces/posts/{id}/comments | read | communities | List comments for a post. |
| POST | api/v2/communities/spaces/posts/{id}/comments | write | communities | Create a comment on a post. |
| POST | api/v2/communities/spaces/posts/{id}/decline | write | communities | Decline a post. |
| POST | api/v2/communities/spaces/posts/{id}/dismiss_reports | write | communities | Dismiss all pending moderation reports on a post. |
| GET | api/v2/communities/spaces/posts/{id}/likes | read | communities | List likes for a post. |
| POST | api/v2/communities/spaces/posts/{id}/likes | write | communities | Like a post. |
| POST | api/v2/communities/spaces/posts/{id}/pin | write | communities | Pin a post. |
| POST | api/v2/communities/spaces/posts/{id}/unpin | write | communities | Unpin a post. |
| GET | api/v2/communities/spaces/posts/{id}/video_embeds | read | communities | List video embeds for a post. |
| POST | api/v2/communities/spaces/posts/{id}/video_embeds | write | communities | Attach a video embed to a post. |
| GET | api/v2/communities/spaces/{id} | read | communities | Retrieve a space. |
| PUT | api/v2/communities/spaces/{id} | write | communities | Update a space. |
| DELETE | api/v2/communities/spaces/{id} | write | communities | Delete a space. |
| GET | api/v2/communities/spaces/{id}/posts | read | communities | List posts for a space. |
| POST | api/v2/communities/spaces/{id}/posts | write | communities | Create a post in a space. |
| GET | api/v2/communities/{id} | read | communities | Retrieve a community. |
| PUT | api/v2/communities/{id} | write | communities | Update a community. |
| GET | api/v2/communities/{id}/bans | read | communities | List bans for a community. |
| POST | api/v2/communities/{id}/bans | write | communities | Ban a contact from a community. |
| GET | api/v2/communities/{id}/bans/export_actions | read | communities | List previous ban export actions for a community. |
| POST | api/v2/communities/{id}/bans/export_actions | write | communities | Enqueue an async background job to export community ban data to a file. |
| POST | api/v2/communities/{id}/bans/unban_actions | write | communities | Enqueue an async background job to unban one or more contacts from a community. |
| GET | api/v2/communities/{id}/memberships | read | communities | List memberships for a community. |
| POST | api/v2/communities/{id}/memberships | write | communities | Add a contact as a member of a community. |
| POST | api/v2/communities/{id}/memberships/add_to_group_actions | write | communities | Enqueue an async background job to add one or more community members to one or more spaces (groups). |
| POST | api/v2/communities/{id}/memberships/ban_actions | write | communities | Enqueue an async background job to ban one or more community members. |
| GET | api/v2/communities/{id}/memberships/export_actions | read | communities | List previous membership export actions for a community. |
| POST | api/v2/communities/{id}/memberships/export_actions | write | communities | Enqueue an async background job to export community membership data to a file. |
| POST | api/v2/communities/{id}/memberships/remove_from_group_actions | write | communities | Enqueue an async background job to remove one or more community members from one or more spaces (groups). |
| GET | api/v2/communities/{id}/space_groups | read | communities | List space groups for a community. |
| POST | api/v2/communities/{id}/space_groups | write | communities | Create a space group within a community. |
| GET | api/v2/workspaces/{id}/communities | read | communities | List communities for a workspace. |
| POST | api/v2/workspaces/{id}/communities | write | communities | Create a community for a workspace. |
| GET | api/v2/contacts/applied_tags/{id} | read | contacts | Retrieve an applied tag for a contact. |
| DELETE | api/v2/contacts/applied_tags/{id} | write | contacts | Remove a tag from a contact by deleting an applied tag. |
| GET | api/v2/contacts/enroll_actions/{id} | read | contacts | Retrieve a single Contact Enroll Action and its current async progress. |
| DELETE | api/v2/contacts/enroll_actions/{id} | write | contacts | Delete a Contact Enroll Action record. |
| GET | api/v2/contacts/events/notes/{id} | read | contacts | Read a contact note. |
| PUT | api/v2/contacts/events/notes/{id} | write | contacts | Edit content and/or occurred_at while preserving the original author and source, including UI and workflow notes. |
| DELETE | api/v2/contacts/events/notes/{id} | write | contacts | Permanently delete a contact note, including UI and workflow notes. |
| GET | api/v2/contacts/events/{id} | read | contacts | Read the Event rows used by the contact Activity tab. |
| GET | api/v2/contacts/export_actions/{id} | read | contacts | Retrieve a single Contact Export Action and its current async progress. |
| DELETE | api/v2/contacts/export_actions/{id} | write | contacts | Delete a Contact Export Action record. |
| GET | api/v2/contacts/filters/{id} | read | contacts | Fetches a previously saved contact filter by id. |
| GET | api/v2/contacts/run_workflow_actions/{id} | read | contacts | Retrieve a single Contact Run Workflow Action and its current async progress. |
| DELETE | api/v2/contacts/run_workflow_actions/{id} | write | contacts | Delete a Contact Run Workflow Action record. |
| GET | api/v2/contacts/subscription_changes/{id} | read | contacts | Read one immutable subscription-change log entry. |
| GET | api/v2/contacts/tag_actions/{id} | read | contacts | Retrieve a single Contact Tag Action and its current async progress. |
| DELETE | api/v2/contacts/tag_actions/{id} | write | contacts | Delete a Contact Tag Action record. |
| GET | api/v2/contacts/tags/{id} | read | contacts | Retrieve a single Contact Tag. |
| PUT | api/v2/contacts/tags/{id} | write | contacts | Update a Contact Tag. |
| DELETE | api/v2/contacts/tags/{id} | write | contacts | Delete a Contact Tag from your workspace. |
| GET | api/v2/contacts/unsubscribe_actions/{id} | read | contacts | Retrieve a single Contact Unsubscribe Action and its current async progress. |
| DELETE | api/v2/contacts/unsubscribe_actions/{id} | write | contacts | Delete a Contact Unsubscribe Action record. |
| GET | api/v2/contacts/unsubscribed_topics/{id} | read | contacts | Read a contact's topic opt-out. |
| DELETE | api/v2/contacts/unsubscribed_topics/{id} | write | contacts | Resubscribe the contact by removing a topic opt-out. |
| GET | api/v2/contacts/{id} | read | contacts | Retrieve a contact. |
| PUT | api/v2/contacts/{id} | write | contacts | Update a contact. |
| DELETE | api/v2/contacts/{id} | write | contacts | Delete a contact. |
| GET | api/v2/contacts/{id}/applied_tags | read | contacts | List the applied tags for a contact. |
| POST | api/v2/contacts/{id}/applied_tags | write | contacts | Assign a tag to a contact by creating an applied tag. |
| GET | api/v2/contacts/{id}/billing_address | read | contacts | Read the billing address shown in the contact overview. |
| POST | api/v2/contacts/{id}/billing_address | write | contacts | Create the contact's billing address, also shown in the contact overview. |
| PATCH | api/v2/contacts/{id}/billing_address | write | contacts | Partially update the contact's existing billing address in place. |
| GET | api/v2/contacts/{id}/events | read | contacts | Read the Event rows used by the contact Activity tab. |
| GET | api/v2/contacts/{id}/events/notes | read | contacts | Read only contact notes from the Activity tab, including API, UI and workflow notes. |
| POST | api/v2/contacts/{id}/events/notes | write | contacts | Save a note synchronously in the contact's Activity tab with content and optional occurred_at. |
| DELETE | api/v2/contacts/{id}/gdpr_destroy | write | contacts | This will destroy all personally identifiable information for a contact, including their name and phone number, but does not delete the contact record itself. |
| GET | api/v2/contacts/{id}/shipping/addresses | read | contacts | listShippingAddresses. |
| POST | api/v2/contacts/{id}/shipping/addresses | write | contacts | createShippingAddresses. |
| GET | api/v2/contacts/{id}/subscription_changes | read | contacts | Read the contact's subscription-change log, ordered by ID ascending by default. |
| GET | api/v2/contacts/{id}/unsubscribed_topics | read | contacts | List one row per topic the contact has opted out of, including archived topics with existing opt-outs. |
| POST | api/v2/contacts/{id}/unsubscribed_topics | write | contacts | Opt a contact out of one active topic in their workspace. |
| GET | api/v2/workspaces/{id}/contacts | read | contacts | List contacts for the given workspace. |
| POST | api/v2/workspaces/{id}/contacts | write | contacts | Add a new contact to the workspace. |
| GET | api/v2/workspaces/{id}/contacts/enroll_actions | read | contacts | List all Contact Enroll Actions for your workspace. |
| POST | api/v2/workspaces/{id}/contacts/enroll_actions | write | contacts | Bulk-enroll a collection of contacts into course sections. |
| GET | api/v2/workspaces/{id}/contacts/export_actions | read | contacts | List all Contact Export Actions for your workspace. |
| POST | api/v2/workspaces/{id}/contacts/export_actions | write | contacts | Export a collection of contacts to a CSV file. |
| POST | api/v2/workspaces/{id}/contacts/filters | write | contacts | Translates a natural-language audience description into a ClickFunnels contact filter using an AI model. |
| GET | api/v2/workspaces/{id}/contacts/run_workflow_actions | read | contacts | List all Contact Run Workflow Actions for your workspace. |
| POST | api/v2/workspaces/{id}/contacts/run_workflow_actions | write | contacts | Run a workflow against a collection of contacts. |
| GET | api/v2/workspaces/{id}/contacts/tag_actions | read | contacts | List all Contact Tag Actions for your workspace. |
| POST | api/v2/workspaces/{id}/contacts/tag_actions | write | contacts | Bulk-apply or bulk-remove one or more Contact Tags across a filtered set of contacts. |
| GET | api/v2/workspaces/{id}/contacts/tags | read | contacts | List all Contact Tags for your workspace. |
| POST | api/v2/workspaces/{id}/contacts/tags | write | contacts | Add a new Contact Tag to your Workspace. |
| GET | api/v2/workspaces/{id}/contacts/unsubscribe_actions | read | contacts | List all Contact Unsubscribe Actions for your workspace. |
| POST | api/v2/workspaces/{id}/contacts/unsubscribe_actions | write | contacts | Bulk-unsubscribe a collection of contacts from email. |
| GET | api/v2/workspaces/{id}/contacts/unsubscribed_topics | read | contacts | List topic opt-outs across the accessible workspace. |
| POST | api/v2/workspaces/{id}/contacts/upsert | write | contacts | Creates or updates a Contact, matching on the email address. |
| GET | api/v2/courses/enrollments/{id} | read | courses | Retrieve an enrollment. |
| PUT | api/v2/courses/enrollments/{id} | write | courses | Update an enrollment. |
| GET | api/v2/courses/lesson_completions/{id} | read | courses | Retrieve a enrollment-lesson completion record. |
| DELETE | api/v2/courses/lesson_completions/{id} | write | courses | Unmark a lesson as completed. |
| GET | api/v2/courses/lessons/{id} | read | courses | Fetch Lesson. |
| PUT | api/v2/courses/lessons/{id} | write | courses | Update Lesson. |
| POST | api/v2/courses/lessons/{id}/publish | write | courses | Makes a single lesson live by setting `published_at`. |
| GET | api/v2/courses/sections/publish_actions/{id} | read | courses | Retrieve a single course-section publish action and its current async progress. |
| DELETE | api/v2/courses/sections/publish_actions/{id} | write | courses | Delete a course-section publish action record. |
| GET | api/v2/courses/sections/{id} | read | courses | Fetch Section. |
| PUT | api/v2/courses/sections/{id} | write | courses | Update Section. |
| GET | api/v2/courses/sections/{id}/lessons | read | courses | List Lessons. |
| POST | api/v2/courses/sections/{id}/lessons | write | courses | Add a new Lesson. |
| POST | api/v2/courses/sections/{id}/publish | write | courses | Makes a single section live by setting `published_at`, and cascade-publishes its lessons individually so per-lesson side effects fire. |
| GET | api/v2/courses/{id} | read | courses | Retrieve a course. |
| PATCH | api/v2/courses/{id} | write | courses | Update a course's settings and appearance — including its storefront image (`image_id`), title, description, and customer-center access settings (`show_to_non_members`, `upgrade_url`,... |
| GET | api/v2/courses/{id}/enrollments | read | courses | List enrollments for a course. |
| POST | api/v2/courses/{id}/enrollments | write | courses | Add a new enrollment. |
| GET | api/v2/courses/{id}/lesson_completions | read | courses | List of enrollment-completion records showing which lessons have been completed by which enrollments. |
| POST | api/v2/courses/{id}/lesson_completions | write | courses | Mark a lesson as completed by a specific enrollment. |
| POST | api/v2/courses/{id}/publish | write | courses | Makes the course live by setting `published_at`. |
| GET | api/v2/courses/{id}/sections | read | courses | List Sections. |
| POST | api/v2/courses/{id}/sections | write | courses | Add a new Section. |
| GET | api/v2/courses/{id}/sections/publish_actions | read | courses | List course-section publish actions for a course. |
| POST | api/v2/courses/{id}/sections/publish_actions | write | courses | Publish one or more course sections AND the lessons they contain. |
| GET | api/v2/workspaces/{id}/courses | read | courses | List courses for a team. |
| POST | api/v2/workspaces/{id}/courses | write | courses | Create a course for a team. |
| GET | api/v2/discounts/{id} | read | discounts | Retrieve a single discount. |
| PATCH | api/v2/discounts/{id} | write | discounts | Update a discount. |
| DELETE | api/v2/discounts/{id} | write | discounts | Hard-delete a discount. |
| GET | api/v2/workspaces/{id}/discounts | read | discounts | List the discounts in a workspace. |
| POST | api/v2/workspaces/{id}/discounts | write | discounts | Create a discount in a workspace. |
| GET | api/v2/domains/{id} | read | domains | Fetch a single domain by ID. |
| GET | api/v2/workspaces/{id}/domains | read | domains | List all domains for a workspace. |
| GET | api/v2/downloads/{id} | read | downloads | Fetch a single download by ID, including the Asset ID used to configure product-variant access and the file's permanent link. |
| GET | api/v2/workspaces/{id}/downloads | read | downloads | List downloads for a workspace. |
| POST | api/v2/workspaces/{id}/downloads | write | downloads | Create a download from a file at a public URL. |
| GET | api/v2/emails/addresses/{id} | read | emails | Retrieve a single email address. |
| PUT | api/v2/emails/addresses/{id} | write | emails | Update a sender address — most commonly to change its `name` (the from-name). |
| DELETE | api/v2/emails/addresses/{id} | write | emails | Archive (soft-delete) a sender address. |
| GET | api/v2/emails/broadcasts/send_actions/{id} | read | emails | Retrieve a single send action and its current async delivery progress. |
| DELETE | api/v2/emails/broadcasts/send_actions/{id} | write | emails | Cancel a broadcast's scheduled send. |
| GET | api/v2/emails/broadcasts/{id} | read | emails | Retrieve a single email broadcast by ID. |
| PATCH | api/v2/emails/broadcasts/{id} | write | emails | Update an email broadcast. |
| DELETE | api/v2/emails/broadcasts/{id} | write | emails | Delete an email broadcast. |
| POST | api/v2/emails/broadcasts/{id}/resend_unopened | write | emails | Create an independent editable draft from a broadcast that has been complete for at least 24 hours, including the exact 24-hour boundary. |
| GET | api/v2/emails/broadcasts/{id}/send_actions | read | emails | List all send actions for an email broadcast. |
| POST | api/v2/emails/broadcasts/{id}/send_actions | write | emails | Send (or schedule) an email broadcast by creating a Send Action. |
| POST | api/v2/emails/broadcasts/{id}/send_test | write | emails | Send the saved main broadcast content to 1-5 explicit recipients without changing the broadcast or sending its audience. |
| GET | api/v2/emails/broadcasts/{id}/sent_content | read | emails | The HTML an email broadcast actually sent, one entry per distinct document. |
| GET | api/v2/emails/broadcasts/{id}/stats | read | emails | Delivery progress, engagement and revenue for one email broadcast, the same numbers as. |
| GET | api/v2/emails/domains/{id} | read | emails | Retrieve a single email sending domain (DKIM/SPF/DMARC), including its ownership, transport, readiness, and return-path flags plus the DNS records to add at the provider. |
| POST | api/v2/emails/domains/{id}/verify | write | emails | Re-run the DNS checks for DKIM, SPF, DMARC, and the return path, cached for about 10 minutes, and return the refreshed status together with the current ownership state. |
| GET | api/v2/emails/templates/{id} | read | emails | Retrieve a single email template. |
| PATCH | api/v2/emails/templates/{id} | write | emails | Update an email template. |
| DELETE | api/v2/emails/templates/{id} | write | emails | Delete an email template. |
| GET | api/v2/emails/topics/{id} | read | emails | Retrieve a single email topic. |
| PATCH | api/v2/emails/topics/{id} | write | emails | Update an email topic. |
| DELETE | api/v2/emails/topics/{id} | write | emails | Archive an email topic. |
| GET | api/v2/workspaces/{id}/emails/addresses | read | emails | List all email addresses for a workspace. |
| POST | api/v2/workspaces/{id}/emails/addresses | write | emails | Create a sender ("from") email address. |
| GET | api/v2/workspaces/{id}/emails/broadcasts | read | emails | List all email broadcasts for a workspace. |
| POST | api/v2/workspaces/{id}/emails/broadcasts | write | emails | Create a new email broadcast. |
| GET | api/v2/workspaces/{id}/emails/domains | read | emails | List all email sending domains (DKIM/SPF/DMARC) for a workspace. |
| POST | api/v2/workspaces/{id}/emails/domains | write | emails | Provision a sending domain for a workspace. |
| GET | api/v2/workspaces/{id}/emails/settings | read | emails | Retrieve email settings for a workspace. |
| PUT | api/v2/workspaces/{id}/emails/settings | write | emails | Update a workspace's email/marketing settings. |
| GET | api/v2/workspaces/{id}/emails/templates | read | emails | List all email templates for a workspace. |
| POST | api/v2/workspaces/{id}/emails/templates | write | emails | Create an email template from html_body/text_body. |
| GET | api/v2/workspaces/{id}/emails/topics | read | emails | List all email topics for a workspace. |
| POST | api/v2/workspaces/{id}/emails/topics | write | emails | Create a new email topic for a workspace. |
| GET | api/v2/form_submissions/{id} | read | form-submissions | Retrieve a form submission. |
| GET | api/v2/workspaces/{id}/form_submissions | read | form-submissions | List form submissions. |
| GET | api/v2/forms/field_sets/{id} | read | forms | Retrieve a field set. |
| PUT | api/v2/forms/field_sets/{id} | write | forms | Update a field set. |
| DELETE | api/v2/forms/field_sets/{id} | write | forms | Delete a field set. |
| GET | api/v2/forms/field_sets/{id}/fields | read | forms | List fields for a field set. |
| POST | api/v2/forms/field_sets/{id}/fields | write | forms | Add a new field. |
| POST | api/v2/forms/field_sets/{id}/fields/reorder | write | forms | Reorders the fields of a field set. |
| GET | api/v2/forms/fields/options/{id} | read | forms | Retrieve a option for a field. |
| PUT | api/v2/forms/fields/options/{id} | write | forms | Update a option for a field. |
| DELETE | api/v2/forms/fields/options/{id} | write | forms | Delete a option for a field. |
| GET | api/v2/forms/fields/{id} | read | forms | Retrieve a field. |
| PUT | api/v2/forms/fields/{id} | write | forms | Update a field. |
| DELETE | api/v2/forms/fields/{id} | write | forms | Delete a field. |
| GET | api/v2/forms/fields/{id}/options | read | forms | List options for a field. |
| POST | api/v2/forms/fields/{id}/options | write | forms | Add a new option to a field. |
| GET | api/v2/forms/submissions/answers/{id} | read | forms | Retrieve a answer for a submission. |
| PUT | api/v2/forms/submissions/answers/{id} | write | forms | Update a answer for a submission. |
| DELETE | api/v2/forms/submissions/answers/{id} | write | forms | Delete a answer for a submission. |
| GET | api/v2/forms/submissions/{id} | read | forms | Retrieve a submission for a form. |
| PUT | api/v2/forms/submissions/{id} | write | forms | Update a submission for a form. |
| DELETE | api/v2/forms/submissions/{id} | write | forms | Delete a submission for a form. |
| GET | api/v2/forms/submissions/{id}/answers | read | forms | List answers for a submission. |
| POST | api/v2/forms/submissions/{id}/answers | write | forms | Add a new answer to a submission. |
| GET | api/v2/forms/{id} | read | forms | Retrieve a form. |
| PUT | api/v2/forms/{id} | write | forms | Update a form. |
| DELETE | api/v2/forms/{id} | write | forms | Delete a form. |
| GET | api/v2/forms/{id}/field_sets | read | forms | List field sets for a form. |
| POST | api/v2/forms/{id}/field_sets | write | forms | Add a new field set. |
| GET | api/v2/forms/{id}/submissions | read | forms | List submissions for a form. |
| POST | api/v2/forms/{id}/submissions | write | forms | Add a new submission to a form. |
| GET | api/v2/workspaces/{id}/forms | read | forms | List forms for a workspace. |
| POST | api/v2/workspaces/{id}/forms | write | forms | Add a new form. |
| GET | api/v2/fulfillments/locations/{id} | read | fulfillments | Fetch Location. |
| PUT | api/v2/fulfillments/locations/{id} | write | fulfillments | Update Location. |
| DELETE | api/v2/fulfillments/locations/{id} | write | fulfillments | Remove Location. |
| GET | api/v2/fulfillments/{id} | read | fulfillments | Retrieve a specific fulfillment in the current workspace. |
| PUT | api/v2/fulfillments/{id} | write | fulfillments | Update a specific fulfillment. |
| DELETE | api/v2/fulfillments/{id} | write | fulfillments | Remove Fulfillment. |
| POST | api/v2/fulfillments/{id}/cancel | write | fulfillments | This will cancel a Fulfillment. |
| GET | api/v2/workspaces/{id}/fulfillments | read | fulfillments | List all fulfillments for your workspace. |
| POST | api/v2/workspaces/{id}/fulfillments | write | fulfillments | Fulfill an order or a part of an order. |
| GET | api/v2/workspaces/{id}/fulfillments/locations | read | fulfillments | List Locations. |
| POST | api/v2/workspaces/{id}/fulfillments/locations | write | fulfillments | Create Location. |
| GET | api/v2/funnels/clone_actions/{id} | read | funnels | Retrieve a durable funnel clone receipt by integer or public ID. |
| GET | api/v2/funnels/tags/{id} | read | funnels | Fetch Tag. |
| PUT | api/v2/funnels/tags/{id} | write | funnels | Update Tag. |
| DELETE | api/v2/funnels/tags/{id} | write | funnels | Remove Tag. |
| GET | api/v2/funnels/{id} | read | funnels | Fetch a funnel by numeric id or public id. |
| PUT | api/v2/funnels/{id} | write | funnels | Update a funnel's settings, including its path, favicon, domain, and tags, by numeric id or public id with the `funnel` JSON root. |
| DELETE | api/v2/funnels/{id} | write | funnels | Permanently remove an active or archived, unshared funnel only when its workflow has no steps beyond its generated root. |
| POST | api/v2/funnels/{id}/archive | write | funnels | Synchronously archive the funnel and its attached show-page pages. |
| GET | api/v2/funnels/{id}/clone_actions | read | funnels | List retained API clone receipts for a source funnel, including queued, processing, completed, and failed attempts. |
| POST | api/v2/funnels/{id}/clone_actions | write | funnels | Create a durable asynchronous receipt for a new same-workspace copy of the source funnel. |
| GET | api/v2/funnels/{id}/conditional_split_steps | read | funnels | List all conditional split steps in a funnel. |
| POST | api/v2/funnels/{id}/conditional_split_steps | write | funnels | Add a new conditional split step to a funnel. |
| GET | api/v2/funnels/{id}/conditional_split_steps/{id} | read | funnels | Fetch a single conditional split step with its branches and condition. |
| PATCH | api/v2/funnels/{id}/conditional_split_steps/{id} | write | funnels | Update the `condition` and/or attach pages to existing `branches`. |
| DELETE | api/v2/funnels/{id}/conditional_split_steps/{id} | write | funnels | Remove a conditional split from the funnel. |
| GET | api/v2/funnels/{id}/split_test_steps | read | funnels | List all split test steps in a funnel. |
| POST | api/v2/funnels/{id}/split_test_steps | write | funnels | Wrap an existing page in a new split test. |
| GET | api/v2/funnels/{id}/split_test_steps/{id} | read | funnels | Fetch a single split test step with its variants and weights. |
| PATCH | api/v2/funnels/{id}/split_test_steps/{id} | write | funnels | Update a split test's variants: attach a page to an empty branch, swap an existing. |
| DELETE | api/v2/funnels/{id}/split_test_steps/{id} | write | funnels | Remove a split test from the funnel. |
| GET | api/v2/funnels/{id}/stats | read | funnels | Retrieve detailed statistics for a funnel, including a summary of key metrics. |
| GET | api/v2/funnels/{id}/structure | read | funnels | A funnel's steps as a single, flat, ordered list — the same top‑to‑bottom flow you see in the funnel builder. |
| POST | api/v2/funnels/{id}/unarchive | write | funnels | Synchronously restore the funnel and its attached show-page pages. |
| GET | api/v2/workspaces/{id}/funnels | read | funnels | List Funnels. |
| POST | api/v2/workspaces/{id}/funnels | write | funnels | Create a new funnel in the workspace. |
| GET | api/v2/workspaces/{id}/funnels/tags | read | funnels | List Tags. |
| POST | api/v2/workspaces/{id}/funnels/tags | write | funnels | Create Tag. |
| GET | api/v2/images/{id} | read | images | Fetch Image. |
| PUT | api/v2/images/{id} | write | images | Update Image. |
| DELETE | api/v2/images/{id} | write | images | Remove Image. |
| GET | api/v2/workspaces/{id}/images | read | images | List Images. |
| POST | api/v2/workspaces/{id}/images | write | images | Create Image. |
| GET | api/v2/me | read | me | This endpoint returns the user data for the currently authenticated user. |
| GET | api/v2/orders/applied_tags/{id} | read | orders | Retrieve an applied tag for an order. |
| DELETE | api/v2/orders/applied_tags/{id} | write | orders | Remove a tag from an order by deleting an applied tag. |
| GET | api/v2/orders/invoices/restocks/{id} | read | orders | Fetch Restock. |
| GET | api/v2/orders/invoices/{id} | read | orders | Retrieve an invoice for an order. |
| PUT | api/v2/orders/invoices/{id} | write | orders | Update a specific invoice in the current workspace. |
| POST | api/v2/orders/invoices/{id}/abandon | write | orders | Abandon an unpaid, draft, or past-due invoice through ClickFunnels' own abandon path (the. |
| POST | api/v2/orders/line_items/{id}/changes | read | orders | Returns a non-destructive preview of changing the variant and price of a subscription. |
| POST | api/v2/orders/line_items/{id}/changes/perform | write | orders | Commits a variant/price change for a subscription line item. |
| GET | api/v2/orders/tags/{id} | read | orders | Retrieve a single order tag. |
| PUT | api/v2/orders/tags/{id} | write | orders | Update an order tag. |
| DELETE | api/v2/orders/tags/{id} | write | orders | Delete an order tag from your workspace. |
| GET | api/v2/orders/transactions/{id} | read | orders | Retrieve a transaction for an order. |
| POST | api/v2/orders/transactions/{id}/refund | write | orders | Refund this charge, in full, through ClickFunnels' own refund path (the same path the in-app. |
| GET | api/v2/orders/{id} | read | orders | Retrieve a specific order in the current workspace. |
| PUT | api/v2/orders/{id} | write | orders | Update a specific order in the current workspace. |
| GET | api/v2/orders/{id}/applied_tags | read | orders | List the applied tags for an order. |
| POST | api/v2/orders/{id}/applied_tags | write | orders | Assign a tag to an order by creating an applied tag. |
| POST | api/v2/orders/{id}/cancel | write | orders | Cancel a subscription order through ClickFunnels' own cancel path (the same path the. |
| GET | api/v2/orders/{id}/invoices | read | orders | List invoices for a specific order. |
| POST | api/v2/orders/{id}/invoices | write | orders | Create an invoice for an external order. |
| GET | api/v2/orders/{id}/transactions | read | orders | List transactions for an order. |
| GET | api/v2/workspaces/{id}/orders | read | orders | List all orders for the current workspace. |
| POST | api/v2/workspaces/{id}/orders | write | orders | Create a new external order in the current workspace. |
| GET | api/v2/workspaces/{id}/orders/invoices | read | orders | List all invoices for a specific workspace. |
| GET | api/v2/workspaces/{id}/orders/invoices/restocks | read | orders | List Restocks. |
| GET | api/v2/workspaces/{id}/orders/tags | read | orders | List all order tags for your workspace. |
| POST | api/v2/workspaces/{id}/orders/tags | write | orders | Add a new order tag to your workspace. |
| GET | api/v2/pages/{id} | read | pages | Fetch a page by numeric id or public id. |
| PUT | api/v2/pages/{id} | write | pages | Update an existing internal, custom HTML, or external (SDK) page. |
| DELETE | api/v2/pages/{id} | write | pages | Delete a page by ID. |
| GET | api/v2/pages/{id}/custom_html | read | pages | Return the stored HTML body of a ClickFunnels-hosted custom HTML page. |
| DELETE | api/v2/pages/{id}/products | write | pages | Detach one or more products from the page's show page step. |
| GET | api/v2/pages/{id}/stats | read | pages | Retrieve statistics for a page, including views, opt-ins, sales, and earnings. |
| GET | api/v2/workspaces/{id}/pages | read | pages | Page offers extra information about ClickFunnels pages, like those that are part of funnels. |
| POST | api/v2/workspaces/{id}/pages | write | pages | Create a new internal page in the workspace. |
| POST | api/v2/workspaces/{id}/pages/custom_html | write | pages | Create a ClickFunnels-hosted custom HTML page: you supply the complete HTML document and ClickFunnels serves it verbatim at a path on the funnel's domain — no page editor, no PML. |
| POST | api/v2/workspaces/{id}/pages/external | write | pages | Create an externally-hosted (SDK) page. |
| GET | api/v2/products/collections/{id} | read | products | Fetch Collection. |
| PUT | api/v2/products/collections/{id} | write | products | Update Collection. |
| GET | api/v2/products/prices/{id} | read | products | Retrieve a single price. |
| PUT | api/v2/products/prices/{id} | write | products | Update a single price. |
| GET | api/v2/products/prices/{id}/change_options | read | products | Returns the allowed upgrade and downgrade target variants for a price, grouped by. |
| GET | api/v2/products/tags/{id} | read | products | Retrieve a tag for a product. |
| PUT | api/v2/products/tags/{id} | write | products | Update a tag for a product. |
| DELETE | api/v2/products/tags/{id} | write | products | Delete a tag for a product. |
| GET | api/v2/products/variants/{id} | read | products | Retrieve a single variant. |
| PUT | api/v2/products/variants/{id} | write | products | Update a single variant. |
| POST | api/v2/products/variants/{id}/prices | write | products | Create a new price for a given variant. |
| GET | api/v2/products/{id} | read | products | Retrieve a product for a workspace. |
| PUT | api/v2/products/{id} | write | products | Update a product for a workspace. |
| POST | api/v2/products/{id}/archive | write | products | This will archive a Product. |
| GET | api/v2/products/{id}/prices | read | products | List all prices for a given product. |
| POST | api/v2/products/{id}/unarchive | write | products | This will unarchive a Product. |
| GET | api/v2/products/{id}/variants | read | products | List variants for a product. |
| POST | api/v2/products/{id}/variants | write | products | Create a new variant for a product. |
| GET | api/v2/workspaces/{id}/products | read | products | List all products for a workspace. |
| POST | api/v2/workspaces/{id}/products | write | products | Add a new product to a workspace. |
| GET | api/v2/workspaces/{id}/products/collections | read | products | List Collections. |
| POST | api/v2/workspaces/{id}/products/collections | write | products | Create Collection. |
| GET | api/v2/workspaces/{id}/products/tags | read | products | List tags for a product. |
| POST | api/v2/workspaces/{id}/products/tags | write | products | Add a new tag to a product. |
| GET | api/v2/refine_filters/{id} | read | refine-filters | Fetch a single saved filter by its public id. |
| PATCH | api/v2/refine_filters/{id} | write | refine-filters | Update an existing RefineFilter. |
| DELETE | api/v2/refine_filters/{id} | write | refine-filters | Delete a RefineFilter. |
| GET | api/v2/workspaces/{id}/refine_filters | read | refine-filters | List saved filters in a workspace, ordered by id ascending. |
| POST | api/v2/workspaces/{id}/refine_filters | write | refine-filters | Create a new contact RefineFilter in the workspace. |
| GET | api/v2/sales/opportunities/notes/{id} | read | sales | Fetch Note. |
| PUT | api/v2/sales/opportunities/notes/{id} | write | sales | Update Note. |
| DELETE | api/v2/sales/opportunities/notes/{id} | write | sales | Remove Note. |
| GET | api/v2/sales/opportunities/{id} | read | sales | Fetch Opportunity. |
| PUT | api/v2/sales/opportunities/{id} | write | sales | Update Opportunity. |
| DELETE | api/v2/sales/opportunities/{id} | write | sales | Remove Opportunity. |
| GET | api/v2/sales/opportunities/{id}/notes | read | sales | List Notes. |
| POST | api/v2/sales/opportunities/{id}/notes | write | sales | Create Note. |
| GET | api/v2/sales/pipelines/stages/{id} | read | sales | Fetch Stage. |
| PUT | api/v2/sales/pipelines/stages/{id} | write | sales | Update Stage. |
| DELETE | api/v2/sales/pipelines/stages/{id} | write | sales | Remove Stage. |
| GET | api/v2/sales/pipelines/{id} | read | sales | Fetch Pipeline. |
| PUT | api/v2/sales/pipelines/{id} | write | sales | Update Pipeline. |
| DELETE | api/v2/sales/pipelines/{id} | write | sales | Delete a pipeline and its stages. |
| GET | api/v2/sales/pipelines/{id}/stages | read | sales | List Stages. |
| POST | api/v2/sales/pipelines/{id}/stages | write | sales | Create Stage. |
| GET | api/v2/workspaces/{id}/sales/opportunities | read | sales | List Opportunities. |
| POST | api/v2/workspaces/{id}/sales/opportunities | write | sales | Create Opportunity. |
| GET | api/v2/workspaces/{id}/sales/pipelines | read | sales | List Pipelines. |
| POST | api/v2/workspaces/{id}/sales/pipelines | write | sales | Create Pipeline. |
| GET | api/v2/segments/{id} | read | segments | Fetch a named contact audience. |
| PATCH | api/v2/segments/{id} | write | segments | Update a named contact audience. |
| DELETE | api/v2/segments/{id} | write | segments | Delete the segment, leaving its stored filter copy in place. |
| GET | api/v2/workspaces/{id}/segments | read | segments | List the workspace's contact segments, including those created in the UI. |
| POST | api/v2/workspaces/{id}/segments | write | segments | Create a named contact audience from a saved or serialized contact filter, which the segment copies. |
| GET | api/v2/shipping/addresses/{id} | read | shipping | getShippingAddresses. |
| PATCH | api/v2/shipping/addresses/{id} | write | shipping | updateShippingAddresses. |
| DELETE | api/v2/shipping/addresses/{id} | write | shipping | Deletes the entry and its street row. |
| GET | api/v2/shipping/location_groups/{id} | read | shipping | Retrieve a location group for a profile. |
| GET | api/v2/shipping/location_groups/{id}/zones | read | shipping | List zones for a location group. |
| POST | api/v2/shipping/location_groups/{id}/zones | write | shipping | Add a new zone to a location group. |
| GET | api/v2/shipping/packages/{id} | read | shipping | Retrieve a package for a workspace. |
| PUT | api/v2/shipping/packages/{id} | write | shipping | Update a package for a workspace. |
| DELETE | api/v2/shipping/packages/{id} | write | shipping | Delete a package for a workspace. |
| GET | api/v2/shipping/profiles/{id} | read | shipping | Retrieve a shipping profile for a workspace. |
| PUT | api/v2/shipping/profiles/{id} | write | shipping | Update a shipping profile for a workspace. |
| DELETE | api/v2/shipping/profiles/{id} | write | shipping | Delete a shipping profile for a workspace. |
| GET | api/v2/shipping/profiles/{id}/location_groups | read | shipping | List location groups for a profile. |
| GET | api/v2/shipping/rates/names/{id} | read | shipping | Retrieve a rate name for a shipping profile. |
| PUT | api/v2/shipping/rates/names/{id} | write | shipping | Update a rate name for a shipping profile. |
| DELETE | api/v2/shipping/rates/names/{id} | write | shipping | Delete a rate name for a shipping profile. |
| GET | api/v2/shipping/rates/{id} | read | shipping | Retrieve a shipping rate for a zone. |
| PUT | api/v2/shipping/rates/{id} | write | shipping | Update a shipping rate for a zone. |
| DELETE | api/v2/shipping/rates/{id} | write | shipping | Delete a shipping rate for a zone. |
| GET | api/v2/shipping/zones/{id} | read | shipping | Retrieve a zone for a location group. |
| PUT | api/v2/shipping/zones/{id} | write | shipping | Update a zone for a location group. |
| DELETE | api/v2/shipping/zones/{id} | write | shipping | Delete a zone for a location group. |
| GET | api/v2/shipping/zones/{id}/rates | read | shipping | List shipping rates for a zone. |
| POST | api/v2/shipping/zones/{id}/rates | write | shipping | Add a new shipping rate to a zone. |
| GET | api/v2/workspaces/{id}/shipping/packages | read | shipping | List packages for a workspace. |
| POST | api/v2/workspaces/{id}/shipping/packages | write | shipping | Add a new package to a workspace. |
| GET | api/v2/workspaces/{id}/shipping/profiles | read | shipping | List shipping profiles for a workspace. |
| POST | api/v2/workspaces/{id}/shipping/profiles | write | shipping | Add a new shipping profile to a workspace. |
| GET | api/v2/workspaces/{id}/shipping/rates/names | read | shipping | List rate names for a shipping profile. |
| POST | api/v2/workspaces/{id}/shipping/rates/names | write | shipping | Add a new rate name to a shipping profile. |
| GET | api/v2/workspaces/{id}/site | read | site | Fetch the site for a workspace. |
| PUT | api/v2/workspaces/{id}/site | write | site | Update the site for a workspace. |
| GET | api/v2/workspaces/{id}/stats | read | stats | Aggregate statistics over a **filtered set of records, without listing the records**. |
| GET | api/v2/stores/{id} | read | stores | Fetch Store. |
| PUT | api/v2/stores/{id} | write | stores | Update Store. |
| DELETE | api/v2/stores/{id} | write | stores | Remove Store. |
| GET | api/v2/workspaces/{id}/stores | read | stores | List Stores. |
| POST | api/v2/workspaces/{id}/stores | write | stores | Create Store. |
| GET | api/v2/workspaces/{id}/styles | read | styles | List Styles. |
| GET | api/v2/survey_workflows/runs/{id} | read | survey-workflows | Fetch one survey run with every saved answer. |
| GET | api/v2/survey_workflows/{id} | read | survey-workflows | Fetch a survey with every current question on every branch, including questions nobody has answered yet. |
| GET | api/v2/survey_workflows/{id}/runs | read | survey-workflows | List every run of a survey, one per respondent, with every saved answer. |
| GET | api/v2/workspaces/{id}/survey_workflows | read | survey-workflows | List a workspace's surveys, including disabled and archived ones. |
| GET | api/v2/teams | read | teams | List all teams for the current account. |
| GET | api/v2/teams/{id} | read | teams | Retrieve a single team. |
| PUT | api/v2/teams/{id} | write | teams | List all teams for the current account. |
| GET | api/v2/teams/{id}/workspaces | read | teams | List workspaces for a team. |
| GET | api/v2/themes/{id} | read | themes | Retrieve a theme. |
| PUT | api/v2/themes/{id} | write | themes | Update a theme. |
| POST | api/v2/themes/{id}/set_default | write | themes | This will set the specified theme as the default theme for the current workspace. |
| GET | api/v2/workspaces/{id}/themes | read | themes | List of all themes available in the workspace. |
| GET | api/v2/url_redirects/{id} | read | url-redirects | Fetch a short link by numeric or public ID. |
| PATCH | api/v2/url_redirects/{id} | write | url-redirects | Update only supplied fields. |
| DELETE | api/v2/url_redirects/{id} | write | url-redirects | Delete Short Link. |
| GET | api/v2/url_redirects/{id}/stats | read | url-redirects | Tracked short-link clicks, including repeated clicks from the same contact and existing bot exclusion. |
| GET | api/v2/workspaces/{id}/url_redirects | read | url-redirects | List workspace short links with standard cursor pagination. |
| POST | api/v2/workspaces/{id}/url_redirects | write | url-redirects | Create a short link. |
| GET | api/v2/workspaces/{id}/url_redirects/availability | read | url-redirects | Read-only check of the normalized path against the same ownership and validation rules as writes. |
| GET | api/v2/users | read | users | List users for the current account. |
| GET | api/v2/users/{id} | read | users | Retrieve a single user. |
| GET | api/v2/videos/{id} | read | videos | Get Video. |
| PUT | api/v2/videos/{id} | write | videos | Also accepts PATCH. |
| DELETE | api/v2/videos/{id} | write | videos | Removes the video and nullifies attached lessons video_id. |
| GET | api/v2/workspaces/{id}/videos | read | videos | List Videos. |
| POST | api/v2/workspaces/{id}/videos | write | videos | Returns queued immediately. |
| GET | api/v2/webhooks/incoming/external_purchase_endpoints/{id} | read | webhooks | Retrieve one incoming external purchase endpoint. |
| PUT | api/v2/webhooks/incoming/external_purchase_endpoints/{id} | write | webhooks | Update the endpoint name or ClickFunnels email-suppression setting. |
| DELETE | api/v2/webhooks/incoming/external_purchase_endpoints/{id} | write | webhooks | Delete an endpoint that has no retained events. |
| GET | api/v2/webhooks/incoming/external_purchase_endpoints/{id}/events | read | webhooks | List the raw events received by one incoming external purchase endpoint. |
| GET | api/v2/webhooks/incoming/external_purchase_endpoints/{id}/product_mappings | read | webhooks | List the external product, plan, or SKU mappings configured for one incoming external purchase endpoint. |
| POST | api/v2/webhooks/incoming/external_purchase_endpoints/{id}/product_mappings | write | webhooks | Map one provider product, plan, or SKU identifier to a ClickFunnels variant and. |
| GET | api/v2/webhooks/incoming/external_purchase_events/{id} | read | webhooks | Retrieve one raw external purchase event, its raw `payload` and its processing outcome. |
| GET | api/v2/webhooks/incoming/external_purchase_product_mappings/{id} | read | webhooks | Retrieve one external purchase product mapping and its ClickFunnels product, variant, and price labels. |
| PUT | api/v2/webhooks/incoming/external_purchase_product_mappings/{id} | write | webhooks | Update the external identifier, ClickFunnels variant, or ClickFunnels price for a mapping. |
| DELETE | api/v2/webhooks/incoming/external_purchase_product_mappings/{id} | write | webhooks | Delete an external purchase product mapping. |
| GET | api/v2/webhooks/outgoing/endpoints/{id} | read | webhooks | Retrieve a webhook endpoint for a workspace. |
| PUT | api/v2/webhooks/outgoing/endpoints/{id} | write | webhooks | Update a webhook endpoint for a workspace. |
| DELETE | api/v2/webhooks/outgoing/endpoints/{id} | write | webhooks | Delete a webhook endpoint for a workspace. |
| GET | api/v2/webhooks/outgoing/event_types | read | webhooks | Returns the complete, authoritative catalog of webhook event types that a webhook endpoint can subscribe to. |
| GET | api/v2/webhooks/outgoing/events/{id} | read | webhooks | Retrieve an webhook event for a workspace. |
| GET | api/v2/workspaces/{id}/webhooks/incoming/external_purchase_endpoints | read | webhooks | List the endpoints that receive purchases from external commerce providers for a workspace. |
| POST | api/v2/workspaces/{id}/webhooks/incoming/external_purchase_endpoints | write | webhooks | Create an endpoint for one external commerce provider. |
| GET | api/v2/workspaces/{id}/webhooks/outgoing/endpoints | read | webhooks | List webhook endpoints for a workspace. |
| POST | api/v2/workspaces/{id}/webhooks/outgoing/endpoints | write | webhooks | Add a new webhook endpoint to a workspace. |
| GET | api/v2/workspaces/{id}/webhooks/outgoing/events | read | webhooks | List webhook events for a workspace. |
| GET | api/v2/workflows/runs/{id} | read | workflows | Retrieve a single workflow run by its id or obfuscated public_id. |
| GET | api/v2/workflows/steps/{id} | read | workflows | Retrieve a single workflow step. |
| PATCH | api/v2/workflows/steps/{id} | write | workflows | Update a workflow step's `name`, `step_type_settings`, and/or placement. |
| DELETE | api/v2/workflows/steps/{id} | write | workflows | Delete a step from a workflow. |
| GET | api/v2/workflows/steps/{id}/stats | read | workflows | Stats for one workflow step — the numbers the workflow builder shows under it. |
| GET | api/v2/workflows/triggers/{id} | read | workflows | Retrieve a single workflow trigger. |
| PATCH | api/v2/workflows/triggers/{id} | write | workflows | Update an existing workflow trigger. |
| DELETE | api/v2/workflows/triggers/{id} | write | workflows | Delete a trigger from a workflow. |
| GET | api/v2/workflows/{id} | read | workflows | Retrieve a single workflow by its integer id or obfuscated public_id. |
| PATCH | api/v2/workflows/{id} | write | workflows | Update a workflow's `name`, `archived` flag or `run_type`. |
| DELETE | api/v2/workflows/{id} | write | workflows | Permanently delete a workflow and all its associated triggers, steps, and run records. |
| POST | api/v2/workflows/{id}/disable | write | workflows | Disable a workflow, stopping new runs from being started. |
| POST | api/v2/workflows/{id}/enable | write | workflows | Enable a workflow so it can accept new runs. |
| GET | api/v2/workflows/{id}/runs | read | workflows | List automation runs for a workflow, with compact contact data in each run. |
| POST | api/v2/workflows/{id}/runs | write | workflows | Manually enroll a contact into a workflow, starting a new run immediately. |
| GET | api/v2/workflows/{id}/steps | read | workflows | List all visible (displayable) steps for a workflow using standard collection. |
| POST | api/v2/workflows/{id}/steps | write | workflows | Add a new step to a workflow. |
| GET | api/v2/workflows/{id}/structure | read | workflows | Returns the workflow's complete tree in a single call: the workflow header,. |
| GET | api/v2/workflows/{id}/triggers | read | workflows | List all triggers attached to a workflow. |
| POST | api/v2/workflows/{id}/triggers | write | workflows | Add a new trigger to a workflow. |
| GET | api/v2/workspaces/{id}/workflows | read | workflows | List the standalone automation workflows for a workspace. |
| POST | api/v2/workspaces/{id}/workflows | write | workflows | Create a new standalone automation workflow. |
| GET | api/v2/workspaces/{id} | read | workspaces | Retrieve a workspace. |
| PUT | api/v2/workspaces/{id} | write | workspaces | Update a workspace. |
