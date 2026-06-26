# airbnb-gateway

`airbnb-gateway` is a skill for safe, coherent Airbnb operations in OpenClaw-style agent environments.

It standardizes how agents:
- check inbox threads
- inspect reservations and booking state
- review calendar context
- draft guest replies
- send messages safely
- verify whether a send actually appeared in the live Airbnb thread

The skill teaches a strict operating model:
- prefer Airbnb-native endpoints before generic browser automation
- treat send acknowledgments as `attempted`, not automatically `confirmed`
- verify outbound messages in the live thread UI before declaring success
- never auto-resend from ambiguous or unconfirmed state

`airbnb-gateway` is designed to reduce duplicate messages, normalize agent behavior, and provide a safer foundation for Airbnb messaging, bookings, and calendar workflows.

It works well as:
- a standalone operational skill today
- a future companion to a more formal Airbnb adapter/tool layer tomorrow

---

⭐ **Find this useful?** If `airbnb-gateway` saves you time, please **star it** (the ⭐ at the top of this ClawHub page) — stars help other rental operators discover it and keep it maintained. Thank you!
