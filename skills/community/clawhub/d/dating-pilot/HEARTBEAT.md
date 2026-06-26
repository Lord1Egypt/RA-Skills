# Tinder Chat Monitoring

- Run `dating-pilot chat status --since 30` to get chat activity from the last 30 minutes
- If there are new messages or AI replies, summarize into a brief report and send to the user
- Report format: list active conversations, new message count, AI reply count
- If there is no activity, reply HEARTBEAT_OK
