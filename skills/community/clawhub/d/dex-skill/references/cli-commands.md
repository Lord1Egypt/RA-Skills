# Dex CLI Command Reference

All 53 MCP tools map to CLI subcommands. CLIHub generates subcommand names by replacing `_` with `-` in the MCP tool name.

> **The published CLI can lag the MCP server.** The binary is generated from
> the server and republished separately, so a tool that exists over MCP may
> not have a subcommand yet. As of `@getdex/cli@1.0.10` these three are
> server-only: `dex_research_contacts`, `dex_get_contact_research` and
> `dex_list_upcoming_reminders_and_birthdays`. If a command below exits with
> "unknown command", upgrade (`npm i -g @getdex/cli@latest`) and, failing
> that, call the tool over MCP or the REST API instead — do not report the
> capability as missing.

## Command Mapping

| MCP Tool                                    | CLI Command                                                                                                           |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `dex_search_contacts`                       | `dex dex-search-contacts --query "..."`                                                                               |
| `dex_list_contacts`                         | `dex dex-list-contacts --limit 100`                                                                                   |
| `dex_get_contact`                           | `dex dex-get-contact --id "..."`                                                                                      |
| `dex_create_contact`                        | `dex dex-create-contact --first-name "..." --last-name "..."`                                                         |
| `dex_update_contact`                        | `dex dex-update-contact --id "..." --company "..."`                                                                   |
| `dex_complete_keep_in_touch`                | `dex dex-complete-keep-in-touch --contact-id "..."`                                                                   |
| `dex_set_keep_in_touch`                     | `dex dex-set-keep-in-touch --contact-ids "c1,c2" --cadence "1 mon"`                                                   |
| `dex_archive_contacts`                      | `dex dex-archive-contacts --contact-ids "id1,id2" --archived true` (over 20 ids: `--confirm true --expected-count N`) |
| `dex_delete_contacts`                       | `dex dex-delete-contacts --contact-ids "id1,id2"`                                                                     |
| `dex_merge_contacts`                        | `dex dex-merge-contacts --contact-id-groups '[["id1","id2"]]'`                                                        |
| `dex_filter_contacts`                       | `dex dex-filter-contacts --company "..." --tags "Investor"`                                                           |
| `dex_add_related_contacts`                  | `dex dex-add-related-contacts --contact-id "..." --contact-ids "c1,c2"`                                               |
| `dex_remove_related_contacts`               | `dex dex-remove-related-contacts --contact-id "..." --contact-ids "c1"`                                               |
| `dex_list_tags`                             | `dex dex-list-tags`                                                                                                   |
| `dex_get_tag`                               | `dex dex-get-tag --tag-id "..."`                                                                                      |
| `dex_create_tag`                            | `dex dex-create-tag --name "..."`                                                                                     |
| `dex_update_tag`                            | `dex dex-update-tag --tag-id "..." --name "..."`                                                                      |
| `dex_delete_tag`                            | `dex dex-delete-tag --tag-id "..."`                                                                                   |
| `dex_add_tags_to_contacts`                  | `dex dex-add-tags-to-contacts --tag-ids "id1,id2" --contact-ids "c1,c2"`                                              |
| `dex_remove_tags_from_contacts`             | `dex dex-remove-tags-from-contacts --tag-ids "id1" --contact-ids "c1"`                                                |
| `dex_list_groups`                           | `dex dex-list-groups`                                                                                                 |
| `dex_get_group`                             | `dex dex-get-group --group-id "..."`                                                                                  |
| `dex_create_group`                          | `dex dex-create-group --name "..." --emoji "🚀"`                                                                      |
| `dex_update_group`                          | `dex dex-update-group --group-id "..." --name "..."`                                                                  |
| `dex_delete_group`                          | `dex dex-delete-group --group-id "..."`                                                                               |
| `dex_add_contacts_to_group`                 | `dex dex-add-contacts-to-group --group-id "..." --contact-ids "c1,c2"`                                                |
| `dex_remove_contacts_from_group`            | `dex dex-remove-contacts-from-group --group-id "..." --contact-ids "c1"`                                              |
| `dex_list_group_contacts`                   | `dex dex-list-group-contacts --group-id "..." --limit 20`                                                             |
| `dex_list_notes`                            | `dex dex-list-notes --contact-id "..."`                                                                               |
| `dex_get_note`                              | `dex dex-get-note --note-id "..."`                                                                                    |
| `dex_list_note_types`                       | `dex dex-list-note-types`                                                                                             |
| `dex_create_note`                           | `dex dex-create-note --content "..." --contact-id "..."`                                                              |
| `dex_update_note`                           | `dex dex-update-note --note-id "..." --content "..."`                                                                 |
| `dex_delete_note`                           | `dex dex-delete-note --note-id "..."`                                                                                 |
| `dex_list_upcoming_reminders_and_birthdays` | `dex dex-list-upcoming-reminders-and-birthdays --days 7` (needs CLI > 1.0.10)                                         |
| `dex_list_reminders`                        | `dex dex-list-reminders --is-complete false --is-overdue true`                                                        |
| `dex_get_reminder`                          | `dex dex-get-reminder --reminder-id "..."`                                                                            |
| `dex_create_reminder`                       | `dex dex-create-reminder --text "..." --due-at-date "2026-03-15"`                                                     |
| `dex_update_reminder`                       | `dex dex-update-reminder --reminder-id "..." --is-complete true`                                                      |
| `dex_delete_reminder`                       | `dex dex-delete-reminder --reminder-id "..."`                                                                         |
| `dex_list_custom_fields`                    | `dex dex-list-custom-fields`                                                                                          |
| `dex_create_custom_field`                   | `dex dex-create-custom-field --name "..." --field-type "autocomplete"`                                                |
| `dex_update_custom_field`                   | `dex dex-update-custom-field --custom-field-id "..." --name "..."`                                                    |
| `dex_delete_custom_field`                   | `dex dex-delete-custom-field --custom-field-id "..."`                                                                 |
| `dex_set_custom_field_values`               | `dex dex-set-custom-field-values --updates '[{"contact_id":"c1","custom_field_id":"cf1","text_value":"val"}]'`        |
| `dex_list_calendar_events`                  | `dex dex-list-calendar-events --start "..." --end "..."`                                                              |
| `dex_get_calendar_event`                    | `dex dex-get-calendar-event --event-id "..." --account-email "..."`                                                   |
| `dex_create_calendar_event`                 | `dex dex-create-calendar-event --from-json '{"summary":"Catch-up","start_date":"2026-08-03"}'`                        |
| `dex_update_calendar_event`                 | `dex dex-update-calendar-event --from-json '{"event_id":"...","summary":"New title"}'`                                |
| `dex_delete_calendar_event`                 | `dex dex-delete-calendar-event --event-id "..." --account-email "..."`                                                |
| `dex_search_emails`                         | `dex dex-search-emails --query "Acme partnership"`                                                                    |
| `dex_research_contacts`                     | `dex dex-research-contacts --contact-ids '["..."]'`                                                                   |
| `dex_get_contact_research`                  | `dex dex-get-contact-research --contact-ids '["..."]'`                                                                |

## Usage Notes

- Use `--output json` for machine-readable output, `--output text` (default) for human-readable
- Run `dex --help` for all commands, or `dex <command> --help` for command-specific help
- For complex/array parameters, use `--from-json` to pass the full JSON input: `dex dex-delete-contacts --from-json '{"contact_ids":["id1","id2"]}'`
- Before destructive commands, show the target and consequence and obtain explicit user confirmation
- For calendar writes, prefer `--from-json` so datetimes, attendees, and account selectors stay together
- Calendar create/update accept `idempotency_key` (`--idempotency-key` on regenerated CLI builds, or in `--from-json`); choose a key before the first attempt, reuse only for identical retries within 24 hours, and use a new key for a new operation
- Reuse the `email` returned by calendar reads as `account_email`; get/create/update/delete also accept `account_provider` for duplicate-address connections
- Calendar update cannot move an event between accounts; that requires a separately confirmed create on the target and delete from the source
- Timeout default is 30 seconds, override with `--timeout <ms>`
- The exact flag names for each command are generated by CLIHub — run `dex <command> --help` to see available flags
- If a command is missing, update the generated CLI with `npm install -g @getdex/cli@latest`
