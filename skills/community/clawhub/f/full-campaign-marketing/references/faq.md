# When a run goes wrong

## A task stays queued

Keep polling that task with `beatra.tasks.get`. The plan and any finished poster stay usable.

## The create response never came back

Retry the identical payload and the same `client_request_id`. If the task id disappeared, list tasks and match the frozen request first.

## The price on the card looks wrong

Read `beatra.models.list` or `beatra.social.tools.get` again and show the number it just returned.

## The poster lost the product

One `beatra.images.edit` restores the product's shape and color and keeps the layout. Own card, own id. Do not start the clip from a poster that no longer shows the product.
