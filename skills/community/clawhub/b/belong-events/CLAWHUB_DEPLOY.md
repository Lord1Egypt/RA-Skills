# Belong Events ClawHub release

1. Download the admin export bundle and unzip it.
2. Login once with `clawhub login`.
3. Publish the extracted folder:
clawhub publish ./belong-events \
  --slug belong-events \
  --name "Belong Events" \
  --version 0.0.0 \
  --tags latest \
  --changelog "Update Belong Events skill to v0.0.0"

4. Verify the release:
clawhub search "belong-events"
openclaw skills info belong-events
