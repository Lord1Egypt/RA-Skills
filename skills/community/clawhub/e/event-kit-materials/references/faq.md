# When a run goes wrong

## A task stays queued

Keep polling that task with `beatra.tasks.get`. The copy is already usable.

## The create response never came back

Retry the identical payload and the same `client_request_id`. If the task id disappeared, list tasks and match the frozen request first.

## The price on the card looks wrong

Read `beatra.models.list` again and show the number it just returned.

## The poster lost the time or the offer

One `beatra.images.edit` sets the exact name, time, and offer and keeps the picture. Own card, own id. Do not animate a poster that states a different time.
