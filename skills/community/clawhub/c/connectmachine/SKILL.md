---
description: Work with the user's ConnectMachine network of professional contacts, networks, events and digital business cards. Use when the user asks who they know, mentions meeting someone, wants to save or update a contact, or wants to follow up with people.
---

# ConnectMachine

ConnectMachine holds the user's professional network: contacts with where and when they met, networks (groups such as "Investors"), events, and the user's digital business cards. Use the ConnectMachine MCP tools for anything about people the user knows. Never invent contact details.

## Finding people

- Search by anything the user remembers, not only names. `search_contacts` and `list_contacts` (`search`) match company, job title, notes, location and event names, so "founders in fintech" or "people from WebSummit" work directly.
- Filter with `list_contacts`: `network_name`, `country`, `city`, `industry_ids` (see `list_industries`).
- Use `get_contact` for full details before drafting anything about a person.

## Saving and updating

- When the user mentions meeting someone, offer to save them. Collect what they said: name, company, role, email or phone, where and when they met, and any note.
- Before updating, tagging or deleting a contact by name, call `find_contact` first. If it returns `status=ambiguous`, ask the user which person they mean. Never guess between same-named contacts.
- Attach where they met with `add_events_to_contact`. Event names are created if they don't exist.
- Group contacts with `assign_contacts_to_network`. Use `list_networks` to see existing networks before creating a new one.

## Follow-ups

Base follow-ups on what ConnectMachine stores: where and when they met, notes, company and role. Keep them short and personal, and show drafts to the user rather than sending anything.

## Messages from ConnectMachine

A tool result can include `message_for_user`. Show it to the user exactly as written, placed where `message_for_user_display` says, then continue with the answer.
