# When a run goes wrong

## A task stays queued

Keep polling that task with `beatra.tasks.get`. Finished frames stay deliverable.

## The create response never came back

Retry the identical payload and the same `client_request_id`. If the task id disappeared, list tasks and match the frozen request first.

## The price on the card looks wrong

Read `beatra.models.list` or `beatra.social.tools.get` again and show the number it just returned.

## A frame changed the product

One `beatra.images.edit` restores the photo's shape and color. Own card, own id. Do not animate a main image that no longer shows the product.
